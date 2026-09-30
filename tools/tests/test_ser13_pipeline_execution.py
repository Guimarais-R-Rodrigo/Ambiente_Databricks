"""Real local Spark test for bounded SER13 MERGE and external verification."""
import copy
import importlib.util
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = Path(os.environ.get("SER13_CANDIDATE_ASSISTANT_ROOT",
                                ROOT / "ambiente_fonte/.assistant"))
SKILL = ASSISTANT / "skills/hub-ml-pipeline-builder"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = load(SKILL / "scripts/run_local.py", "_ser13_local_test_runner")
verifier = load(SKILL / "scripts/verify_local.py", "_ser13_local_test_verifier")


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


def expected():
    q = request()
    return [q["batch_rows"][0], q["prior_rows"][1], q["batch_rows"][1]]


class PipelineExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import jdk4py
        os.environ["JAVA_HOME"] = str(jdk4py.JAVA_HOME)
        os.environ["PYSPARK_PYTHON"] = os.sys.executable
        os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
        from pyspark.sql import SparkSession
        cls.spark = SparkSession.builder.master("local[1]").appName("ser13-local").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_real_spark_merge_helper_receipt_replay_and_cleanup(self):
        q = request()
        with patch.object(runner.uuid, "uuid4", return_value=SimpleNamespace(hex="a" * 32)):
            first = runner.run(q, self.spark, run_id="ser13-first")
        self.assertEqual("PASS", first["status"], first["trace"]["blocking_issues"])
        self.assertEqual(expected(), first["result"]["rows"])
        self.assertEqual(["data_quality_check"], first["trace"]["resources_completed"])
        self.assertTrue(verifier.verify(first, expected_request=q, expected_rows=expected(),
                                        expected_run_id="ser13-first")["valid"])
        self.assertFalse(self.spark.catalog.tableExists("_ser13_" + "a" * 32))
        replay = copy.deepcopy(q)
        replay["prior_rows"] = first["result"]["rows"]
        with patch.object(runner.uuid, "uuid4", return_value=SimpleNamespace(hex="b" * 32)):
            second = runner.run(replay, self.spark, run_id="ser13-second")
        self.assertEqual("PASS", second["status"], second["trace"]["blocking_issues"])
        self.assertEqual(first["result"]["output_sha256"], second["result"]["output_sha256"])
        self.assertTrue(verifier.verify(second, expected_request=replay, expected_rows=expected(),
                                        expected_run_id="ser13-second")["valid"])
        self.assertFalse(self.spark.catalog.tableExists("_ser13_" + "b" * 32))

    def test_stale_replay_tamper_and_wrong_oracle(self):
        q = request()
        out = runner.run(q, self.spark, run_id="ser13-tamper")
        self.assertEqual("PASS", out["status"], out["trace"]["blocking_issues"])
        self.assertFalse(verifier.verify(out, expected_request=q, expected_rows=expected(),
                                         expected_run_id="another-run")["valid"])
        changed = copy.deepcopy(q)
        changed["spec"]["destination"] = "synthetic_elsewhere"
        self.assertFalse(verifier.verify(out, expected_request=changed, expected_rows=expected(),
                                         expected_run_id="ser13-tamper")["valid"])
        wrong = copy.deepcopy(expected())
        wrong[0]["value"] = 999
        self.assertFalse(verifier.verify(out, expected_request=q, expected_rows=wrong,
                                         expected_run_id="ser13-tamper")["valid"])
        forged = copy.deepcopy(out)
        forged["result"]["deployment_status"] = "COMPLETED"
        self.assertFalse(verifier.verify(forged, expected_request=q, expected_rows=expected(),
                                         expected_run_id="ser13-tamper")["valid"])

    def test_invalid_inputs_block_before_helper(self):
        cases = [
            ("operation", "DEPLOY"), ("synthetic", False),
            ("float", 1.0), ("huge", 2**53 + 1),
            ("timestamp", "2026-01-01T00:00:00+00:00")]
        for kind, value in cases:
            with self.subTest(kind=kind):
                q = request()
                if kind in ("operation", "synthetic"):
                    q[kind] = value
                elif kind in ("float", "huge"):
                    q["batch_rows"][0]["value"] = value
                else:
                    q["batch_rows"][0]["event_at"] = value
                out = runner.run(q, self.spark, run_id="ser13-bad")
                self.assertEqual("BLOCKED", out["status"])
                self.assertEqual([], out["trace"]["resources_called"])
        conflict = request()
        conflict["batch_rows"][0]["event_at"] = conflict["prior_rows"][0]["event_at"]
        self.assertEqual("BLOCKED", runner.run(conflict, self.spark, run_id="ser13-conflict")["status"])

    def test_helper_failure_blocks_and_cleans_view(self):
        with patch.object(runner.uuid, "uuid4", return_value=SimpleNamespace(hex="c" * 32)):
            with patch.object(runner, "_primitive", side_effect=RuntimeError("injected helper failure")):
                out = runner.run(request(), self.spark, run_id="ser13-failure")
        self.assertEqual("BLOCKED", out["status"])
        self.assertIsNone(out["receipt"])
        self.assertFalse(self.spark.catalog.tableExists("_ser13_" + "c" * 32))

    def test_cleanup_failure_reports_unknown_residue(self):
        name = "_ser13_" + "d" * 32
        catalog = self.spark.catalog
        original_drop = catalog.dropTempView
        try:
            with patch.object(runner.uuid, "uuid4", return_value=SimpleNamespace(hex="d" * 32)):
                with patch.object(catalog, "dropTempView", return_value=False):
                    out = runner.run(request(), self.spark, run_id="ser13-cleanup")
            self.assertEqual("BLOCKED", out["status"])
            self.assertIn("TEMP_VIEW_CLEANUP_FAILED_RESIDUE_UNKNOWN",
                          out["trace"]["blocking_issues"])
            self.assertIsNone(out["receipt"])
            self.assertTrue(catalog.tableExists(name))
        finally:
            if catalog.tableExists(name):
                original_drop(name)


if __name__ == "__main__":
    unittest.main()
