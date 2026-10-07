"""Local spec validation is never deployment evidence."""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "ambiente_databricks/.assistant/skills/hub-ml-pipeline-builder/scripts/preflight.py"
spec = importlib.util.spec_from_file_location("pipeline_spec_candidate", PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def request():
    return {"schema_version": "SER13-SPEC-1", "synthetic": True,
            "operation": "VALIDATE_SPEC", "environment": "LOCAL_SYNTHETIC", "scope": "PERSONAL",
            "source": "synthetic_source", "destination": "synthetic_destination",
            "write_mode": "MERGE", "incremental": "WATERMARK",
            "primary_keys": ["id"], "columns": ["id", "event_at", "value"],
            "event_time": "event_at", "watermark_seconds": 60,
            "idempotency": "MERGE_ON_KEYS", "permissions": "UNKNOWN",
            "schedule": None, "rollback": "NOT_APPLICABLE_NO_EFFECT"}


class PipelineSpecTests(unittest.TestCase):
    def test_spec_unknown_permissions_never_authorizes_effect(self):
        q = request()
        out = gate.preflight(q)
        self.assertEqual("PASS", out["status"], out)
        self.assertTrue(out["template_loaded"])
        self.assertFalse(out["permissions_verified"])
        self.assertFalse(out["effects_authorized"])
        self.assertEqual("NOT_RUN", out["deployment_status"])
        self.assertIsNone(out["receipt"])
        self.assertTrue(gate.verify_preflight(out, expected_request=q)["valid"])

    def test_effect_or_unapproved_context_blocks(self):
        for key, value in [("operation", "DEPLOY"), ("operation", "RUN"), ("operation", "WRITE"),
                           ("scope", "CORPORATE"), ("environment", "PROD"),
                           ("synthetic", False), ("synthetic", 1),
                           ("schedule", "daily"), ("authorization", True)]:
            with self.subTest(key=key, value=value):
                q = request()
                q[key] = value
                out = gate.preflight(q)
                self.assertEqual("BLOCKED", out["status"])
                self.assertFalse(out["effects_authorized"])
                self.assertEqual("NOT_RUN", out["deployment_status"])

    def test_contradictory_spec_rejected(self):
        for key, value in [("primary_keys", ["missing"]), ("event_time", "missing"),
                           ("primary_keys", ["id", "id"]), ("columns", ["id", "id"]),
                           ("source", "synthetic_source\n"), ("columns", ["id", "event_at", "value\n"]),
                           ("source", "synthetic_destination"), ("incremental", "BATCH"),
                           ("watermark_seconds", -1), ("watermark_seconds", True),
                           ("watermark_seconds", 60.0), ("idempotency", "REJECT_DUPLICATES")]:
            with self.subTest(key=key, value=value):
                q = request()
                q[key] = value
                self.assertEqual("BLOCKED", gate.preflight(q)["status"])
        q = request()
        q.update(incremental="BATCH", watermark_seconds=None, write_mode="APPEND",
                 idempotency="REJECT_DUPLICATES")
        self.assertEqual("PASS", gate.preflight(q)["status"])

    def test_false_completion_tamper_and_replay_fail(self):
        q = request()
        out = gate.preflight(q)
        for key, value in [("deployment_status", "COMPLETED"), ("writes_performed", True),
                           ("effects_authorized", True), ("completion", {"authorized": True})]:
            tampered = copy.deepcopy(out)
            tampered[key] = value
            self.assertFalse(gate.verify_preflight(tampered, expected_request=q)["valid"])
        changed = copy.deepcopy(q)
        changed["destination"] = "synthetic_other"
        self.assertFalse(gate.verify_preflight(out, expected_request=changed)["valid"])


if __name__ == "__main__":
    unittest.main()

