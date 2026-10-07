import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "ambiente_databricks/.assistant/skills/hub-ml-monitoramento-modelo"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


RUN = load(SKILL / "scripts/run.py", "_test_ser11_run")
VERIFY = load(SKILL / "scripts/verify.py", "_test_ser11_verify")
PREFLIGHT = load(SKILL / "scripts/preflight.py", "_test_ser11_preflight")


def fixture():
    return {"schema_version": "SER11-REQUEST-1", "profile": "DRIFT_NUMERIC_LOCAL_V1",
            "synthetic": True, "requested_effect": "NONE", "model_id": "SYNTH-M01",
            "model_version": "v1", "population_id": "SYNTHETIC-P01", "score_name": "score",
            "reference_start": "2025-01-01T00:00:00Z", "reference_end": "2025-01-31T23:59:59Z",
            "current_start": "2025-02-01T00:00:00Z", "current_end": "2025-02-28T23:59:59Z",
            "n_bins": 4, "eps": 1e-6,
            "reference": [{"id": f"R{i}", "observed_at": "2025-01-15T00:00:00Z", "score": value}
                          for i, value in enumerate((0.1, 0.1, 0.3, 0.6, 0.9, None))],
            "current": [{"id": f"C{i}", "observed_at": "2025-02-15T00:00:00Z", "score": value}
                        for i, value in enumerate((0.2, 0.5, 0.7, 0.7, 0.95, None))]}


class MonitorCandidateTests(unittest.TestCase):
    def test_real_metrics_with_ties_and_nulls(self):
        request = fixture()
        self.assertEqual(PREFLIGHT.preflight(request)["status"], "PASS")
        payload = RUN.run(request, run_id="ser11-positive")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        self.assertTrue(VERIFY.verify(payload, expected_request=request, expected_run_id="ser11-positive")["valid"])
        self.assertEqual(payload["result"]["windows"]["reference"]["missing_count"], 1)
        self.assertFalse(payload["result"]["performance_evaluated"])
        self.assertFalse(payload["result"]["action_performed"])

    def test_replay_and_tamper(self):
        request = fixture()
        payload = RUN.run(request, run_id="ser11-replay")
        self.assertFalse(VERIFY.verify(payload, expected_request=request, expected_run_id="other")["valid"])
        self.assertFalse(VERIFY.verify(payload, expected_request=request, expected_run_id=None)["valid"])
        for key in ("psi", "ks_statistic", "ks_pvalue"):
            changed = copy.deepcopy(payload)
            changed["result"][key] += 0.123456
            self._rehash(changed)
            verdict = VERIFY.verify(changed, expected_request=request, expected_run_id="ser11-replay")
            self.assertFalse(verdict["valid"])
            self.assertTrue(any("ORACLE_MISMATCH" in issue for issue in verdict["issues"]))

    @staticmethod
    def _rehash(payload):
        from hub_scripts.skill_execution.domain_context import digest
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        payload["trace"]["output_digest"] = digest(payload["result"])
        payload["receipt"] = build_execution_receipt(
            payload["trace"], payload["result"], expected_skill=RUN.SKILL,
            expected_entrypoint=RUN.ENTRYPOINT, protected_primitive=RUN.PRIMITIVE_ID)
        assert payload["receipt"] is not None

    def test_rehashed_extra_window_rejected(self):
        request = fixture()
        payload = RUN.run(request, run_id="ser11-extra-window")
        self.assertEqual(payload["status"], "PASS")
        payload["result"]["windows"]["future"] = {"count": 999999}
        self._rehash(payload)
        verdict = VERIFY.verify(payload, expected_request=request, expected_run_id="ser11-extra-window")
        self.assertIn("WINDOW_SET_MISMATCH", verdict["issues"])

    def test_effect_windows_and_unknown_field(self):
        request = fixture()
        request["requested_effect"] = "RETRAIN"
        self.assertEqual(RUN.run(request, run_id="ser11-block")["status"], "BLOCKED")
        request = fixture()
        request["current_start"] = request["reference_start"]
        self.assertEqual(PREFLIGHT.preflight(request)["status"], "BLOCKED")
        request = fixture()
        request["label"] = 1
        self.assertEqual(PREFLIGHT.preflight(request)["status"], "BLOCKED")

    def test_helper_failure(self):
        original = RUN._canonical
        try:
            RUN._canonical = lambda: (_ for _ in ()).throw(RuntimeError("INJECTED_FAILURE"))
            payload = RUN.run(fixture(), run_id="ser11-fail")
            self.assertEqual(payload["status"], "BLOCKED")
            self.assertIsNone(payload["receipt"])
        finally:
            RUN._canonical = original


if __name__ == "__main__":
    unittest.main()
