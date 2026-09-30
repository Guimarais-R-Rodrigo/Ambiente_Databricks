"""Synthetic controls for the Delta effect executor; no local Delta table is written."""
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
ASSISTANT = Path(os.environ.get("SER14_ASSISTANT_ROOT", str(ROOT / "ambiente_fonte/.assistant")))
sys.path.insert(0, str(ASSISTANT))
from hub_scripts.skill_execution.domain_context import digest

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

SKILL = ASSISTANT / "skills/hub-ml-pipeline-builder"
delta = load(SKILL / "scripts/run_delta.py", "_ser14_delta_test")
local = load(SKILL / "scripts/run_local.py", "_ser14_local_test")

def request():
    spec = {
        "schema_version": "SER13-SPEC-1", "synthetic": True,
        "operation": "VALIDATE_SPEC", "environment": "LOCAL_SYNTHETIC",
        "scope": "PERSONAL", "source": "synthetic_source",
        "destination": "synthetic_destination", "write_mode": "MERGE",
        "incremental": "BATCH", "primary_keys": ["id"],
        "columns": ["id", "event_at", "value"], "event_time": "event_at",
        "watermark_seconds": None, "idempotency": "MERGE_ON_KEYS",
        "permissions": "UNKNOWN", "schedule": None,
        "rollback": "NOT_APPLICABLE_NO_EFFECT"}
    return {
        "schema_version": "SER13-LOCAL-RUN-1", "synthetic": True,
        "operation": "RUN_LOCAL_SPARK", "spec": spec,
        "prior_rows": [{"id": 1, "event_at": "2026-01-01T00:00:00Z", "value": 10},
                       {"id": 2, "event_at": "2026-01-01T00:00:00Z", "value": 30}],
        "batch_rows": [{"id": 1, "event_at": "2026-01-02T00:00:00Z", "value": 20},
                       {"id": 3, "event_at": "2026-01-01T00:00:00Z", "value": 40}]}

def authority(q, run_id="ser14-test"):
    return {
        "authorized": True, "effect": "SYNTHETIC_DELTA_PROBE",
        "target_table": "workspace.default.skills_delivery_" + "a" * 32,
        "request_digest": digest(q), "run_id": run_id, "nonce": "b" * 32,
        "cleanup": "DROP_OWNED", "expected_principal": "synthetic@example.invalid",
        "expected_catalog": "workspace", "expected_schema": "default"}

class FakeRow:
    def __init__(self, **items):
        self.items = items
    def asDict(self):
        return dict(self.items)

class FakeResult:
    def __init__(self, rows=()):
        self.rows = rows
    def collect(self):
        return list(self.rows)

class FakeCatalog:
    def __init__(self, owner):
        self.owner = owner
    def tableExists(self, name):
        if self.owner.drop_count:
            if self.owner.post_drop_readback_error:
                raise TimeoutError("simulated cleanup readback timeout")
            if self.owner.post_drop_readback_stale:
                return True
        return self.owner.exists
    def dropTempView(self, name):
        return self.owner.views.pop(name, None) is not None

class FakeSpark:
    def __init__(self, *, existing=False, wrong_principal=False, tamper_markers=False,
                 bad_readback=False, create_timeout=False, on_identity=None,
                 post_drop_readback_error=False, post_drop_readback_stale=False):
        self.exists = existing
        self.wrong_principal = wrong_principal
        self.tamper_markers = tamper_markers
        self.bad_readback = bad_readback
        self.create_timeout = create_timeout
        self.on_identity = on_identity
        self.post_drop_readback_error = post_drop_readback_error
        self.post_drop_readback_stale = post_drop_readback_stale
        self.drop_count = 0
        self.table = {}
        self.views = {}
        self.properties = {}
        self.calls = []
        self.catalog = FakeCatalog(self)
    def sql(self, statement):
        self.calls.append(statement)
        if statement.startswith("SELECT current_catalog()"):
            if self.on_identity is not None:
                self.on_identity()
            return FakeResult([FakeRow(catalog="workspace", schema="default",
                                      principal="someone-else@example.invalid" if self.wrong_principal
                                      else "synthetic@example.invalid")])
        if statement.startswith("CREATE TABLE "):
            if self.exists:
                raise RuntimeError("already exists")
            self.exists = True
            self.properties = dict(re.findall(r"'([^']+)' = '([^']+)'", statement))
            if self.create_timeout:
                raise TimeoutError("simulated uncertain CREATE acknowledgement")
            return FakeResult()
        if statement.startswith("SHOW TBLPROPERTIES "):
            properties = dict(self.properties)
            if self.tamper_markers:
                properties["skills_delivery.nonce"] = "c" * 32
            return FakeResult([FakeRow(key=k, value=v) for k,v in properties.items()])
        if statement.startswith("INSERT INTO "):
            name = re.search(r"FROM `([^\x60]+)`", statement).group(1)
            self.table = {row["id"]: dict(row) for row in self.views[name]}
            return FakeResult()
        if statement.startswith("MERGE INTO "):
            name = re.search(r"USING `([^\x60]+)` AS s", statement).group(1)
            for row in self.views[name]:
                old = self.table.get(row["id"])
                if old is None or row["event_at"] > old["event_at"]:
                    self.table[row["id"]] = dict(row)
            return FakeResult()
        if statement.startswith("SELECT id, event_at, value FROM "):
            rows = [dict(row) for row in self.table.values()]
            if self.bad_readback and any(x.startswith("MERGE INTO ") for x in self.calls):
                rows[0]["value"] = 999
            return FakeResult([FakeRow(**row) for row in rows])
        if statement.startswith("DROP TABLE "):
            self.drop_count += 1
            self.exists = False
            self.table = {}
            return FakeResult()
        raise AssertionError("Unexpected SQL: " + statement)

class DeltaControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyspark.sql import SparkSession
        cls.spark = SparkSession.builder.master("local[1]").appName("ser14-compute-only").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")
        cls.q = request()
        cls.expected = local._merge(cls.q["prior_rows"], cls.q["batch_rows"])
        cls.compute = local.run(cls.q, cls.spark, run_id="ser14-test-compute")
        assert cls.compute["status"] == "PASS", cls.compute["trace"]["blocking_issues"]

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def execute(self, fake, auth=None, expected=None, compute=None):
        q = self.q
        with patch.object(delta, "_temp_view", side_effect=lambda spark, rows, name:
                          spark.views.__setitem__(name, [
                              {"id": str(r["id"]), "event_at": r["event_at"], "value": r["value"]}
                              for r in rows])):
            return delta.execute(
                q, self.expected if expected is None else expected, fake,
                authority(q) if auth is None else auth, run_id="ser14-test",
                compute_payload=self.compute if compute is None else compute)

    def test_owned_merge_replay_and_cleanup(self):
        fake = FakeSpark()
        result = self.execute(fake)
        self.assertEqual("PASS", result["status"], result)
        self.assertEqual("CLEANED", result["phase"])
        self.assertEqual("PASS", result["cleanup"])
        self.assertFalse(fake.exists)
        self.assertEqual(2, sum(s.startswith("MERGE INTO ") for s in fake.calls))
        self.assertEqual(result["first_merge_rows_sha256"], result["replay_rows_sha256"])
        self.assertEqual(self.compute["receipt"]["receipt_id"], result["compute_receipt_id"])

    def test_authority_and_existing_table_block_before_create(self):
        for change in (
            {"authorized": False}, {"effect": "DEPLOY"},
            {"target_table": "main.default.skills_delivery_" + "a"*32},
            {"request_digest": "0"*64}, {"nonce": "bad"},
            {"cleanup": "KEEP"}, {"expected_catalog": "main"}):
            with self.subTest(change=change):
                auth = {**authority(self.q), **change}
                fake = FakeSpark()
                result = self.execute(fake, auth=auth)
                self.assertEqual("BLOCKED", result["status"])
                self.assertFalse(any(s.startswith("CREATE TABLE ") for s in fake.calls))
        for fake in (FakeSpark(existing=True), FakeSpark(wrong_principal=True)):
            result = self.execute(fake)
            self.assertEqual("BLOCKED", result["status"])
            self.assertFalse(any(s.startswith("CREATE TABLE ") for s in fake.calls))

    def test_untrusted_rows_and_receipt_block_before_create(self):
        fake = FakeSpark()
        altered = [dict(row) for row in self.expected]
        altered[0]["value"] = 999
        result = self.execute(fake, expected=altered)
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual([], fake.calls)
        bad_compute = dict(self.compute)
        bad_compute["receipt"] = None
        result = self.execute(fake, compute=bad_compute)
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual([], fake.calls)

    def test_readback_failure_cleans_only_owned_table(self):
        fake = FakeSpark(bad_readback=True)
        result = self.execute(fake)
        self.assertEqual("BLOCKED", result["status"], result)
        self.assertEqual("PASS_AFTER_FAILURE", result["cleanup"])
        self.assertFalse(fake.exists)
        self.assertTrue(any(s.startswith("DROP TABLE ") for s in fake.calls))

    def test_drop_ack_without_absence_readback_is_not_cleanup_pass(self):
        for options, expected_absence in (
                ({"post_drop_readback_error": True}, None),
                ({"post_drop_readback_stale": True}, False)):
            with self.subTest(options=options):
                fake = FakeSpark(**options)
                result = self.execute(fake)
                self.assertEqual("UNKNOWN", result["status"], result)
                self.assertEqual("DROP_UNCONFIRMED", result["cleanup"])
                self.assertIs(expected_absence, result["table_absent_after_cleanup"])
                self.assertEqual(1, fake.drop_count)

    def test_fallback_drop_ack_without_absence_readback_is_not_cleanup_pass(self):
        fake = FakeSpark(bad_readback=True, post_drop_readback_error=True)
        result = self.execute(fake)
        self.assertEqual("UNKNOWN", result["status"], result)
        self.assertEqual("DROP_UNCONFIRMED", result["cleanup"])
        self.assertIsNone(result["table_absent_after_cleanup"])
        self.assertEqual(1, fake.drop_count)
        self.assertIn("CLEANUP:TimeoutError", result["issues"])

    def test_caller_mutation_during_session_probe_cannot_redirect_effect(self):
        q = copy.deepcopy(self.q)
        expected = copy.deepcopy(self.expected)
        auth = authority(q)
        compute = copy.deepcopy(self.compute)
        original_target = auth["target_table"]
        def mutate():
            q["batch_rows"][0]["value"] = 999
            expected[0]["value"] = 999
            auth["target_table"] = "workspace.default.skills_delivery_" + "c" * 32
            compute["receipt"] = None
        fake = FakeSpark(on_identity=mutate)
        with patch.object(delta, "_temp_view", side_effect=lambda spark, rows, name:
                          spark.views.__setitem__(name, [
                              {"id": str(r["id"]), "event_at": r["event_at"], "value": r["value"]}
                              for r in rows])):
            result = delta.execute(q, expected, fake, auth, run_id="ser14-test",
                                   compute_payload=compute)
        self.assertEqual("PASS", result["status"], result)
        self.assertEqual(original_target, result["target_table"])
        creates = [sql for sql in fake.calls if sql.startswith("CREATE TABLE ")]
        self.assertEqual(1, len(creates))
        self.assertIn("skills_delivery_" + "a"*32, creates[0])
        self.assertNotIn("skills_delivery_" + "c"*32, creates[0])
        self.assertFalse(fake.exists)

    def test_marker_tamper_and_create_timeout_never_drop_unknown(self):
        for fake in (FakeSpark(tamper_markers=True), FakeSpark(create_timeout=True)):
            result = self.execute(fake)
            self.assertEqual("UNKNOWN", result["status"], result)
            self.assertTrue(fake.exists)
            self.assertFalse(any(s.startswith("DROP TABLE ") for s in fake.calls))


if __name__ == "__main__":
    unittest.main()
