import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "ambiente_fonte/.assistant/skills/hub-ml-baseline-ml"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


RUN = load(SKILL / "scripts/run.py", "_test_ser09_run")
VERIFY = load(SKILL / "scripts/verify.py", "_test_ser09_verify")
PREFLIGHT = load(SKILL / "scripts/preflight.py", "_test_ser09_preflight")


def fixture():
    return {"schema_version": "SER09-REQUEST-1", "profile": "BINARY_TEMPORAL_LOCAL_V1",
            "synthetic": True, "requested_effect": "NONE", "population_id": "SYNTHETIC-P01",
            "target": "target", "positive_class": 1, "unit": "synthetic_entity",
            "date_column": "observed_at", "feature_order": ["feature"], "train_pct": 0.5,
            "val_pct": 0.25, "gap_periods": 0, "period_unit": "M", "threshold": 0.5, "seed": 17,
            "rows": [{"id": f"B{i:02d}", "observed_at": f"2024-{i:02d}-01T00:00:00Z",
                      "feature": float(i % 5), "target": i % 2} for i in range(1, 13)]}


class BaselineCandidateTests(unittest.TestCase):
    def test_real_execution(self):
        request = fixture()
        self.assertEqual(PREFLIGHT.preflight(request)["status"], "PASS")
        payload = RUN.run(request, run_id="ser09-positive")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        self.assertTrue(VERIFY.verify(payload, expected_request=request, expected_run_id="ser09-positive")["valid"])
        self.assertEqual(payload["result"]["partitions"]["train"]["ids"], [f"B{i:02d}" for i in range(1, 7)])
        self.assertEqual(set(payload["result"]["partitions"]["holdout"]["metrics"]), {"auc_roc", "brier_score"})

    def test_replay_tamper_and_fit(self):
        request = fixture()
        payload = RUN.run(request, run_id="ser09-replay")
        self.assertFalse(VERIFY.verify(payload, expected_request=request, expected_run_id="other")["valid"])
        self.assertFalse(VERIFY.verify(payload, expected_request=request, expected_run_id=None)["valid"])
        for path in ("metric", "fit"):
            altered = copy.deepcopy(payload)
            if path == "metric":
                altered["result"]["partitions"]["holdout"]["metrics"]["auc_roc"] = 0.1234
            else:
                altered["result"]["scaler_mean"][0] += 1
            self.assertFalse(VERIFY.verify(altered, expected_request=request, expected_run_id="ser09-replay")["valid"])
        altered = copy.deepcopy(payload)
        altered["result"]["partitions"]["holdout"]["metrics"]["f1"] = 0.123456
        self._rehash(altered)
        verdict = VERIFY.verify(altered, expected_request=request, expected_run_id="ser09-replay")
        self.assertIn("METRICS_ORACLE_MISMATCH:holdout", verdict["issues"])

    @staticmethod
    def _rehash(payload):
        from hub_scripts.skill_execution.domain_context import digest
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        payload["trace"]["output_digest"] = digest(payload["result"])
        payload["receipt"] = build_execution_receipt(
            payload["trace"], payload["result"], expected_skill=RUN.SKILL,
            expected_entrypoint=RUN.ENTRYPOINT, protected_primitive=RUN.PRIMITIVE_ID)
        assert payload["receipt"] is not None

    def test_rehashed_extra_partition_rejected(self):
        request = fixture()
        payload = RUN.run(request, run_id="ser09-extra-partition")
        self.assertEqual(payload["status"], "PASS")
        payload["result"]["partitions"]["production"] = {
            "metrics": {"auc_roc": 1.0}, "promotion_authorized": True}
        self._rehash(payload)
        verdict = VERIFY.verify(payload, expected_request=request, expected_run_id="ser09-extra-partition")
        self.assertIn("PARTITION_SET_MISMATCH", verdict["issues"])

    def test_extreme_holdout_feature(self):
        request = fixture()
        request["rows"][9]["feature"] = -1e9
        request["rows"][10]["feature"] = 1e9
        payload = RUN.run(request, run_id="ser09-extreme")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        self.assertTrue(VERIFY.verify(payload, expected_request=request, expected_run_id="ser09-extreme")["valid"])

    def test_unauthorized_effect_and_unknown_field(self):
        request = fixture()
        request["requested_effect"] = "PROMOTE"
        self.assertEqual(RUN.run(request, run_id="ser09-block")["status"], "BLOCKED")
        request = fixture()
        request["mlflow_uri"] = "synthetic"
        self.assertEqual(PREFLIGHT.preflight(request)["status"], "BLOCKED")

    def test_helper_failure(self):
        original = RUN._canonical
        try:
            RUN._canonical = lambda *args: (_ for _ in ()).throw(RuntimeError("INJECTED_FAILURE"))
            payload = RUN.run(fixture(), run_id="ser09-fail")
            self.assertEqual(payload["status"], "BLOCKED")
            self.assertIsNone(payload["receipt"])
        finally:
            RUN._canonical = original


if __name__ == "__main__":
    unittest.main()
