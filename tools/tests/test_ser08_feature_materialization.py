"""Synthetic FE materialization controls; Delta effects are simulated locally."""
from __future__ import annotations

import copy
import importlib.util
import os
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import jdk4py
os.environ["JAVA_HOME"] = str(jdk4py.JAVA_HOME)
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = Path(os.environ.get("SER08_ASSISTANT_ROOT", str(ROOT / "ambiente_fonte/.assistant")))
sys.path.insert(0, str(ASSISTANT))
from hub_scripts.skill_execution.domain_context import digest


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fe_dir = ASSISTANT / "skills/hub-ml-feature-engineering/scripts"
materializer = load(Path(os.environ.get("SER08_MATERIALIZER_STAGED",
                                        str(fe_dir / "run_pit_materialization.py"))),
                    "_ser08_materializer_test")
view_runner = load(fe_dir / "run_pit_features.py", "_ser08_view_test")
delta = load(Path(os.environ.get("SER08_DELTA_STAGED",
                              str(ASSISTANT / "skills/hub-ml-pipeline-builder/scripts/run_delta.py"))),
             "_ser08_delta_test")
pit_test = load(Path(os.environ.get("SER08_FIXTURE_STAGED",
                                 str(Path(__file__).with_name("test_ser08_feature_pit.py")))),
                "_ser08_fixture_test")


class Row:
    def __init__(self, **value):
        self.value = value
    def asDict(self):
        return dict(self.value)


class Result:
    def __init__(self, values=()):
        self.values = values
    def collect(self):
        return list(self.values)


class Catalog:
    def __init__(self, owner):
        self.owner = owner
    def tableExists(self, name):
        return self.owner.exists
    def dropTempView(self, name):
        return self.owner.views.pop(name, None) is not None


class Conf:
    def __init__(self, timezone):
        self.timezone = timezone
    def get(self, key):
        assert key == "spark.sql.session.timeZone"
        return self.timezone


class FakeSpark:
    def __init__(self, *, timezone="UTC", existing=False, tamper=False,
                 bad_readback=False, equal_type_readback=None,
                 create_timeout=False, table_id_swap=False, on_identity=None):
        self.catalog = Catalog(self)
        self.conf = Conf(timezone)
        self.exists = existing
        self.tamper = tamper
        self.bad_readback = bad_readback
        self.equal_type_readback = equal_type_readback
        self.create_timeout = create_timeout
        self.table_id_swap = table_id_swap
        self.detail_reads = 0
        self.on_identity = on_identity
        self.calls = []
        self.views = {}
        self.table = {}
        self.properties = {}
        self.version = 0
    def sql(self, statement):
        self.calls.append(statement)
        if statement.startswith("SELECT current_catalog()"):
            if self.on_identity:
                self.on_identity()
            return Result([Row(catalog="workspace", schema="default",
                               principal="synthetic@example.invalid")])
        if statement.startswith("CREATE TABLE "):
            assert not self.exists
            self.exists = True
            self.properties = dict(re.findall(r"'([^']+)' = '([^']+)'", statement))
            if self.create_timeout:
                raise TimeoutError("uncertain CREATE")
            return Result()
        if statement.startswith("SHOW TBLPROPERTIES "):
            props = dict(self.properties)
            if self.tamper:
                props["skills_delivery.view_sha256"] = "0" * 64
            return Result([Row(key=k, value=v) for k, v in props.items()])
        if statement.startswith("SELECT decision_id, entity_id, decision_at, feature_value, available_at FROM "):
            rows = list(self.table.values())
            if self.bad_readback and rows:
                rows = copy.deepcopy(rows)
                rows[0]["feature_value"] = 999
            if self.equal_type_readback is not None and rows:
                rows = copy.deepcopy(rows)
                rows[0]["feature_value"] = self.equal_type_readback
            return Result([Row(**row) for row in rows])
        if statement.startswith("MERGE INTO "):
            view = re.search(r"USING `([^\x60]+)` AS s", statement).group(1)
            for row in self.views[view]:
                self.table.setdefault(row["decision_id"], dict(row))
            self.version += 1
            return Result()
        if statement.startswith("DESCRIBE HISTORY "):
            return Result([Row(version=self.version)])
        if statement.startswith("DESCRIBE DETAIL "):
            self.detail_reads += 1
            value = "replacement-table-id" if self.table_id_swap and self.detail_reads > 1 else "synthetic-delta-table-id"
            return Result([Row(id=value)])
        if statement.startswith("DROP TABLE "):
            self.exists = False
            self.table = {}
            return Result()
        raise AssertionError("Unexpected SQL: " + statement)


class FeatureMaterializationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyspark.sql import SparkSession
        cls.spark = SparkSession.builder.master("local[1]").appName(
            "ser08-feature-materialization").config("spark.sql.session.timeZone", "UTC").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")
        cls.context, cls.datasets = pit_test.fixture()
        cls.bound = {"expected_context": cls.context, "expected_datasets": cls.datasets,
                     "expected_window_days": 5, "expected_upstream_run_id": "SER08-FM-UP",
                     "expected_view_run_id": "SER08-FM-VIEW"}
        cls.view = view_runner.compose(cls.context, cls.datasets, cls.spark,
                                       window_days=5, upstream_run_id="SER08-FM-UP",
                                       view_run_id="SER08-FM-VIEW")
        assert cls.view["status"] == "PASS", cls.view.get("issues")
        cls.request = materializer.effect_request(cls.view, **cls.bound)

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def authority(self):
        return {"authorized": True, "effect": "SYNTHETIC_FEATURE_MATERIALIZATION_PROBE",
                "target_table": "workspace.default.skills_delivery_" + "a" * 32,
                "request_digest": digest(self.request), "run_id": "ser08-fm-test",
                "nonce": "b" * 32, "cleanup": "DROP_OWNED",
                "expected_principal": "synthetic@example.invalid",
                "expected_catalog": "workspace", "expected_schema": "default"}

    def execute(self, fake, view=None, authority=None, bound=None):
        with patch.object(materializer, "_modules", return_value=(view_runner, delta)), \
             patch.object(delta, "_temp_view", side_effect=lambda spark, rows, name, **kwargs:
                          spark.views.__setitem__(name, copy.deepcopy(rows))):
            return materializer.execute(
                self.view if view is None else view, fake,
                self.authority() if authority is None else authority,
                run_id="ser08-fm-test", **(self.bound if bound is None else bound))

    def test_owned_projection_replay_versions_and_cleanup(self):
        fake = FakeSpark()
        effect = self.execute(fake)
        self.assertEqual("PASS", effect["status"], effect)
        self.assertEqual(effect["first_merge_rows_sha256"], effect["replay_rows_sha256"])
        self.assertGreaterEqual(effect["replay_delta_version"], effect["first_delta_version"])
        self.assertEqual("synthetic-delta-table-id", effect["table_id"])
        self.assertEqual("PASS", effect["cleanup"])
        self.assertFalse(fake.exists)
        self.assertIn("skills_delivery.receipt_sha256", fake.properties)
        self.assertEqual(2, sum(sql.startswith("MERGE INTO ") for sql in fake.calls))

    def test_bad_authority_and_utc_block_before_create(self):
        for change in ({"authorized": False}, {"request_digest": "0" * 64},
                       {"effect": "SYNTHETIC_DELTA_PROBE"},
                       {"target_table": "main.default.skills_delivery_" + "a" * 32}):
            fake = FakeSpark()
            result = self.execute(fake, authority={**self.authority(), **change})
            self.assertEqual("BLOCKED", result["status"], result)
            self.assertFalse(any(sql.startswith("CREATE TABLE ") for sql in fake.calls))
        fake = FakeSpark(timezone="America/Sao_Paulo")
        self.assertEqual("BLOCKED", self.execute(fake)["status"])
        self.assertFalse(any(sql.startswith("CREATE TABLE ") for sql in fake.calls))

    def test_forged_view_missing_postflight_and_mutated_context_block(self):
        forged = copy.deepcopy(self.view)
        forged["result"]["features"][0]["feature_value"] = 999
        forged["feature_view_sha256"] = digest(forged["result"])
        for view, bound in ((forged, self.bound),
                            ({**self.view, "upstream_evidence": {**self.view["upstream_evidence"],
                              "postflight": None}}, self.bound),
                            (self.view, {**self.bound, "expected_window_days": 6})):
            fake = FakeSpark()
            result = self.execute(fake, view=view, bound=bound)
            self.assertEqual("BLOCKED", result["status"], result)
            self.assertFalse(any(sql.startswith("CREATE TABLE ") for sql in fake.calls))

    def test_readback_and_marker_tamper_or_timeout(self):
        bad = FakeSpark(bad_readback=True)
        result = self.execute(bad)
        self.assertEqual("BLOCKED", result["status"], result)
        self.assertFalse(bad.exists)
        equal_float = FakeSpark(equal_type_readback=2.0)
        result = self.execute(equal_float)
        self.assertEqual("BLOCKED", result["status"], result)
        self.assertIn("FE_READBACK_TYPE_INVALID", str(result["issues"]))
        bool_readback = FakeSpark()
        bool_readback.exists = True
        bool_readback.table = {"one": {"decision_id": "one", "entity_id": "a",
                                       "decision_at": "2026-01-10T00:00:00.000000Z",
                                       "feature_value": True, "available_at": "2026-01-09T00:00:00.000000Z"}}
        with self.assertRaisesRegex(RuntimeError, "FE_READBACK_TYPE_INVALID"):
            delta._rows(bool_readback, "`workspace`.`default`.`skills_delivery_" + "a"*32 + "`",
                        profile="FE_PIT")
        for fake in (FakeSpark(tamper=True), FakeSpark(create_timeout=True)):
            result = self.execute(fake)
            self.assertEqual("UNKNOWN", result["status"], result)
            self.assertTrue(fake.exists)
            self.assertFalse(any(sql.startswith("DROP TABLE ") for sql in fake.calls))

    def test_caller_mutation_cannot_change_bound_target_or_rows(self):
        view = copy.deepcopy(self.view)
        bound = copy.deepcopy(self.bound)
        auth = self.authority()
        def mutate():
            auth["target_table"] = "workspace.default.skills_delivery_" + "c" * 32
            view["result"]["features"][0]["feature_value"] = 999
            bound["expected_datasets"]["history"][0]["feature_value"] = 999
        fake = FakeSpark(on_identity=mutate)
        result = self.execute(fake, view=view, authority=auth, bound=bound)
        self.assertEqual("PASS", result["status"], result)
        self.assertIn("skills_delivery_" + "a" * 32,
                      next(sql for sql in fake.calls if sql.startswith("CREATE TABLE ")))

    def test_final_release_check_failure_never_preserves_pass(self):
        fake = FakeSpark()
        first = {"manifest_sha256": "same"}
        with patch.object(materializer, "release_integrity",
                          side_effect=[first, RuntimeError("release changed")]):
            result = self.execute(fake)
        self.assertEqual("BLOCKED", result["status"], result)
        self.assertTrue(result["table_absent_after_cleanup"])
        self.assertFalse(fake.exists)
        self.assertIn("release changed", str(result["issues"]))

    def test_replaced_table_identity_is_not_dropped(self):
        fake = FakeSpark(table_id_swap=True)
        result = self.execute(fake)
        self.assertEqual("UNKNOWN", result["status"], result)
        self.assertTrue(fake.exists)
        self.assertFalse(any(sql.startswith("DROP TABLE ") for sql in fake.calls))
        self.assertIn("DELTA_TABLE_ID_CHANGED", str(result["issues"]))


if __name__ == "__main__":
    unittest.main()
