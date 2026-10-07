"""Real Spark proof that FE only projects a verified Cross-EDA PIT result."""
from __future__ import annotations

import copy
import importlib.util
import os
import sys
import unittest
from pathlib import Path

import jdk4py
os.environ["JAVA_HOME"] = str(jdk4py.JAVA_HOME)
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = Path(os.environ.get("SER08_ASSISTANT_ROOT", str(ROOT / "ambiente_databricks/.assistant")))
sys.path.insert(0, str(ASSISTANT))
from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.postflight import build_postflight, sha256_digest
from hub_scripts.skill_execution.receipt import build_execution_receipt, verify_execution_receipt

spec = importlib.util.spec_from_file_location(
    "ser08_feature_pit_adapter",
    ASSISTANT / "skills/hub-ml-feature-engineering/scripts/run_pit_features.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def fixture():
    facts = [
        {"decision_id": "d1", "entity_id": "a", "decision_at": "2026-01-10T00:00:00Z"},
        {"decision_id": "d2", "entity_id": "b", "decision_at": "2026-01-10T00:00:00Z"},
        {"decision_id": "d3", "entity_id": "c", "decision_at": "2026-01-10T00:00:00Z"},
    ]
    history = [
        {"entity_id": "a", "reference_at": "2026-01-08T00:00:00Z",
         "available_at": "2026-01-09T00:00:00Z", "feature_value": 1},
        {"entity_id": "a", "reference_at": "2026-01-09T00:00:00Z",
         "available_at": "2026-01-10T00:00:00Z", "feature_value": 2},
        {"entity_id": "a", "reference_at": "2026-01-10T00:00:00Z",
         "available_at": "2026-01-11T00:00:00Z", "feature_value": 3},
        {"entity_id": "b", "reference_at": "2026-01-01T00:00:00Z",
         "available_at": "2026-01-02T00:00:00Z", "feature_value": 9},
    ]
    datasets = {"facts": facts, "history": history}
    context = {
        "schema_version": "SER05-CONTEXT-1", "profile": "CONTEXT_ONLY_PILOT_V1",
        "synthetic": True,
        "sources": [
            {"id": "facts", "snapshot_id": "synthetic-facts-v1",
             "content_sha256": digest(facts), "grain": "ONE_ROW_PER_ENTITY_DECISION",
             "columns": list(facts[0])},
            {"id": "history", "snapshot_id": "synthetic-history-v1",
             "content_sha256": digest(history), "grain": "FEATURE_HISTORY",
             "columns": list(history[0])},
        ],
        "anchor": "facts", "entity_keys": ["entity_id"],
        "anchor_grain": "ONE_ROW_PER_ENTITY_DECISION", "cardinality": "N:1",
        "decision_at": "2026-01-10T00:00:00Z", "pit": "APPLICABLE",
        "temporal": {"reference_column": "reference_at", "availability_column": "available_at",
                     "lag_kind": "CONSTANT", "lag_days": 1, "boundary": "LE",
                     "timezone": "UTC", "tie_break": "REJECT", "bitemporal": False},
        "null_key_policy": "REJECT", "requested_effect": "NONE",
    }
    return context, datasets


class FeaturePitCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyspark.sql import SparkSession
        cls.spark = SparkSession.builder.master("local[1]").appName(
            "ser08-composed-pit").config("spark.sql.session.timeZone", "UTC").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_composed_view_and_adversarial_upstream(self):
        context, datasets = fixture()
        same_id = adapter.compose(context, datasets, self.spark, window_days=5,
                                  upstream_run_id="SER08-SAME", view_run_id="SER08-SAME")
        self.assertEqual("BLOCKED", same_id["status"])
        self.assertIn("RUN_IDS_MUST_DIFFER", str(same_id["issues"]))
        payload = adapter.compose(context, datasets, self.spark, window_days=5,
                                  upstream_run_id="SER08-UP-1", view_run_id="SER08-VIEW-1")
        self.assertEqual("PASS", payload["status"], payload.get("issues"))
        expected = {"expected_context": context, "expected_datasets": datasets,
                    "expected_window_days": 5, "expected_upstream_run_id": "SER08-UP-1",
                    "expected_view_run_id": "SER08-VIEW-1"}
        self.assertTrue(adapter.verify(payload, **expected)["valid"])
        self.assertEqual([2, None, None], [r["feature_value"] for r in payload["result"]["features"]])
        self.assertEqual(payload["upstream_evidence"]["receipt"]["receipt_id"],
                         payload["result"]["upstream_receipt_id"])
        self.assertIsNone(payload["receipt"])
        self.assertFalse(payload["materialization_performed"])
        self.assertFalse(adapter.verify(payload, **{**expected,
            "expected_view_run_id": "SER08-VIEW-REPLAY"})["valid"])
        changed = copy.deepcopy(payload)
        changed["result"]["features"][0]["feature_value"] = 99
        changed["feature_view_sha256"] = digest(changed["result"])
        self.assertFalse(adapter.verify(changed, **expected)["valid"])
        missing = copy.deepcopy(payload)
        missing["upstream_evidence"]["postflight"] = None
        self.assertFalse(adapter.verify(missing, **expected)["valid"])
        forged = copy.deepcopy(payload)
        upstream = forged["upstream_evidence"]
        upstream["result"]["records"][0]["feature_value"] = 999
        upstream["artifacts"]["point_in_time_join"] = upstream["result"]
        upstream["trace"]["output_digest"] = digest(upstream["result"])
        upstream["trace"]["artifacts_digest"] = sha256_digest(upstream["artifacts"])
        run, verify = adapter._upstream()
        upstream["receipt"] = build_execution_receipt(
            upstream["trace"], upstream["result"], expected_skill=run.SKILL,
            expected_entrypoint=run.ENTRYPOINT, protected_primitive=run.PRIMITIVE_ID)
        receipt_check = verify_execution_receipt(
            upstream, expected_skill=run.SKILL, expected_entrypoint=run.ENTRYPOINT,
            protected_primitive=run.PRIMITIVE_ID, expected_run_id="SER08-UP-1").to_dict()
        self.assertTrue(receipt_check["valid"])
        upstream["postflight"] = build_postflight(
            upstream, contract=verify._contract(), receipt_verification=receipt_check,
            handoff=upstream["handoff"])
        self.assertEqual("PASS", upstream["postflight"]["status"])
        self.assertFalse(adapter.verify(forged, **expected)["valid"])


if __name__ == "__main__":
    unittest.main()
