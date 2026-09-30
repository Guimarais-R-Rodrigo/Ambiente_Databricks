"""Synthetic mature-label monitoring with independent metrics and policy oracles."""
from __future__ import annotations

import copy
import importlib.util
import os
import sys
import unittest
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[2] / "ambiente_fonte/.assistant"
ASSISTANT = Path(os.environ.get("SER12_ASSISTANT_ROOT", str(DEFAULT))).resolve()
if str(ASSISTANT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT))
SKILL = ASSISTANT / "skills/hub-ml-monitoramento-modelo"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PREFLIGHT = load(SKILL / "scripts/preflight_performance.py", "_ser12_test_preflight")
RUN = load(SKILL / "scripts/run_performance.py", "_ser12_test_run")
VERIFY = load(SKILL / "scripts/verify_performance.py", "_ser12_test_verify")
DRIFT = load(SKILL / "scripts/run.py", "_ser11_test_drift_after_ser12")


def fixture(ref_scores=(.1, .2, .3, .4, .6, .7, .8, .9),
            cur_scores=(.1, .4, .6, .8, .2, .3, .5, .7)):
    def rows(prefix, observed, label_at, scores):
        return [{"id": f"{prefix}{i}", "observed_at": observed,
                 "label_available_at": label_at, "score": score,
                 "label": int(i >= 4)} for i, score in enumerate(scores)]
    return {"schema_version": "SER12-REQUEST-1", "profile": "BINARY_MATURE_PERFORMANCE_V1",
            "synthetic": True, "requested_effect": "NONE", "model_id": "synthetic-model",
            "model_version": "v1", "population_id": "synthetic-population",
            "score_name": "score", "evaluation_at": "2025-03-10T00:00:00Z",
            "reference_start": "2025-01-01T00:00:00Z",
            "reference_end": "2025-01-31T23:59:59Z",
            "current_start": "2025-02-01T00:00:00Z",
            "current_end": "2025-02-28T23:59:59Z",
            "auc_thresholds": {"warning": 0.1, "critical": 0.2,
                               "direction": "higher", "delta": "absolute"},
            "reference": rows("R", "2025-01-15T00:00:00Z",
                              "2025-02-05T00:00:00Z", ref_scores),
            "current": rows("C", "2025-02-15T00:00:00Z",
                            "2025-03-01T00:00:00Z", cur_scores)}


class SER12PerformanceTests(unittest.TestCase):
    def test_degraded_auc_real_helpers_receipt_and_oracle(self):
        request = fixture()
        self.assertEqual(PREFLIGHT.preflight(request)["status"], "PASS")
        payload = RUN.run(request, run_id="ser12-positive")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        self.assertEqual(payload["trace"]["resources_completed"],
                         ["binary_metrics", "performance_monitor"])
        self.assertTrue(VERIFY.verify(payload, expected_request=request,
                                      expected_run_id="ser12-positive")["valid"])
        self.assertEqual(payload["result"]["metrics"]["reference"]["auc_roc"], 1.0)
        self.assertEqual(payload["result"]["monitor_status"], "🔴 Crítico")
        self.assertEqual(payload["result"]["investigation_decision"],
                         "INVESTIGATE_RETRAINING_CANDIDATE")
        self.assertFalse(payload["result"]["automatic_retrain_authorized"])

    def test_scope_finalizer_requires_postflight(self):
        request = fixture()
        raw = RUN.run(request, run_id="ser12-finalized")
        self.assertEqual(raw["status"], "PASS")
        self.assertFalse(raw["scope_completion_authorized"])
        self.assertFalse(VERIFY.verify_finalized(
            raw, expected_request=request, expected_run_id="ser12-finalized")["valid"])
        final = VERIFY.finalize(raw, expected_request=request,
                                expected_run_id="ser12-finalized")
        self.assertEqual(final["postflight"]["status"], "PASS", final["postflight"]["issues"])
        self.assertTrue(final["scope_completion_authorized"])
        self.assertTrue(VERIFY.verify_finalized(
            final, expected_request=request, expected_run_id="ser12-finalized")["valid"])
        altered = copy.deepcopy(final)
        altered["handoff"]["model_id"] = "other"
        self.assertFalse(VERIFY.verify_finalized(
            altered, expected_request=request, expected_run_id="ser12-finalized")["valid"])
        altered = copy.deepcopy(final)
        altered["scope_completion_authorized"] = False
        self.assertFalse(VERIFY.verify_finalized(
            altered, expected_request=request, expected_run_id="ser12-finalized")["valid"])

    def test_improvement_does_not_alert(self):
        request = fixture(ref_scores=(.1, .4, .6, .8, .2, .3, .5, .7),
                          cur_scores=(.1, .2, .3, .4, .6, .7, .8, .9))
        payload = RUN.run(request, run_id="ser12-improved")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        self.assertLess(payload["result"]["auc_deterioration"], 0)
        self.assertEqual(payload["result"]["monitor_status"], "🟢 Saudável")
        self.assertTrue(VERIFY.verify(payload, expected_request=request,
                                      expected_run_id="ser12-improved")["valid"])

    def test_brier_half_unit_rounding_validates_reported_grid(self):
        request = fixture()
        request["current"] = request["current"][:4]
        for row, label, score in zip(
                request["current"], (0, 0, 1, 1), (.2, .43, .26, .07)):
            row["label"], row["score"] = label, score
        payload = RUN.run(request, run_id="ser12-brier-boundary")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        self.assertEqual(payload["result"]["metrics"]["current"]["brier_score"], .4094)
        self.assertTrue(VERIFY.verify(
            payload, expected_request=request,
            expected_run_id="ser12-brier-boundary")["valid"])
        final = VERIFY.finalize(payload, expected_request=request,
                                expected_run_id="ser12-brier-boundary")
        self.assertTrue(VERIFY.verify_finalized(
            final, expected_request=request,
            expected_run_id="ser12-brier-boundary")["valid"])

    def test_auc_half_unit_policy_uses_validated_report(self):
        scores = (.64, .85, .17, .07, .39, .83, .45, .15, .34, .93,
                  .51, .05, .23, .93, .7, .5, .87, .45, .24, .56,
                  .52, .16, .24, .9, .35, .14, .33, .28, .41, .44, .1)
        request = fixture()
        request["current"] = [
            {"id": f"C{i}", "observed_at": "2025-02-15T00:00:00Z",
             "label_available_at": "2025-03-01T00:00:00Z",
             "score": score, "label": int(i >= 15)}
            for i, score in enumerate(scores)]
        request["auc_thresholds"]["critical"] = .55622
        payload = RUN.run(request, run_id="ser12-auc-boundary")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        self.assertEqual(payload["result"]["metrics"]["current"]["auc_roc"], .4438)
        self.assertEqual(payload["result"]["monitor_status"], "🟡 Atenção")
        self.assertTrue(VERIFY.verify(
            payload, expected_request=request, expected_run_id="ser12-auc-boundary")["valid"])

    def test_immature_label_missing_policy_effect_and_duplicate_block(self):
        cases = [
            ("label_available_at", "2025-03-11T00:00:00Z"),
            ("label_available_at", "2025-02-14T00:00:00Z"),
            ("label", True),
            ("score", float("nan")),
            ("id", "R0"),
        ]
        for key, value in cases:
            with self.subTest(key=key, value=value):
                request = fixture()
                request["current"][0][key] = value
                payload = RUN.run(request, run_id="ser12-invalid")
                self.assertEqual(payload["status"], "BLOCKED")
                self.assertIsNone(payload["receipt"])
                self.assertEqual(payload["trace"]["resources_called"], [])
        for change in ({"auc_thresholds": None},
                       {"requested_effect": "RETRAIN"},
                       {"synthetic": False},
                       {"current_start": "2025-01-15T00:00:00Z"}):
            with self.subTest(change=change):
                request = fixture()
                request.update(change)
                self.assertEqual(RUN.run(request, run_id="ser12-invalid")["status"], "BLOCKED")

    def test_replay_and_rehashed_tamper_rejected(self):
        request = fixture()
        payload = RUN.run(request, run_id="ser12-replay")
        self.assertEqual(payload["status"], "PASS")
        self.assertFalse(VERIFY.verify(payload, expected_request=request,
                                       expected_run_id="other")["valid"])
        for key, value in (("auc_roc", 0.99), ("ks_pct", 1.0), ("brier_score", 0.01)):
            with self.subTest(key=key):
                altered = copy.deepcopy(payload)
                altered["result"]["metrics"]["current"][key] = value
                from hub_scripts.skill_execution.domain_context import digest
                from hub_scripts.skill_execution.receipt import build_execution_receipt
                from hub_scripts.skill_execution.postflight import sha256_digest
                altered["artifacts"][RUN.PRIMITIVE_ID] = copy.deepcopy(altered["result"])
                altered["trace"]["artifacts_digest"] = sha256_digest(altered["artifacts"])
                altered["trace"]["output_digest"] = digest(altered["result"])
                altered["receipt"] = build_execution_receipt(
                    altered["trace"], altered["result"], expected_skill=RUN.SKILL,
                    expected_entrypoint=RUN.ENTRYPOINT, protected_primitive=RUN.PRIMITIVE_ID)
                verdict = VERIFY.verify(altered, expected_request=request,
                                        expected_run_id="ser12-replay")
                self.assertFalse(verdict["valid"])
                self.assertIn("RESULT_ORACLE_MISMATCH:metrics", verdict["issues"])

    def test_rehashed_nearby_grid_and_boolean_metric_rejected(self):
        request = fixture()
        payload = RUN.run(request, run_id="ser12-precision-tamper")
        from hub_scripts.skill_execution.domain_context import digest
        from hub_scripts.skill_execution.postflight import sha256_digest
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        for value in (True, .40935, .1234):
            with self.subTest(value=value):
                altered = copy.deepcopy(payload)
                altered["result"]["metrics"]["current"]["brier_score"] = value
                altered["artifacts"][RUN.PRIMITIVE_ID] = copy.deepcopy(altered["result"])
                altered["trace"]["artifacts_digest"] = sha256_digest(altered["artifacts"])
                altered["trace"]["output_digest"] = digest(altered["result"])
                altered["receipt"] = build_execution_receipt(
                    altered["trace"], altered["result"], expected_skill=RUN.SKILL,
                    expected_entrypoint=RUN.ENTRYPOINT, protected_primitive=RUN.PRIMITIVE_ID)
                verdict = VERIFY.verify(altered, expected_request=request,
                                        expected_run_id="ser12-precision-tamper")
                self.assertIn("RESULT_ORACLE_MISMATCH:metrics", verdict["issues"])

    def test_existing_drift_execution_survives_manifest_union(self):
        q = {"schema_version": "SER11-REQUEST-1", "profile": "DRIFT_NUMERIC_LOCAL_V1",
             "synthetic": True, "requested_effect": "NONE", "model_id": "synthetic-model",
             "model_version": "v1", "population_id": "synthetic-population",
             "score_name": "score", "reference_start": "2025-01-01T00:00:00Z",
             "reference_end": "2025-01-31T23:59:59Z",
             "current_start": "2025-02-01T00:00:00Z",
             "current_end": "2025-02-28T23:59:59Z", "n_bins": 4, "eps": 1e-6,
             "reference": [{"id": f"R{i}", "observed_at": "2025-01-15T00:00:00Z",
                            "score": value}
                           for i, value in enumerate((.1, .1, .3, .6, .9, None))],
             "current": [{"id": f"C{i}", "observed_at": "2025-02-15T00:00:00Z",
                          "score": value}
                         for i, value in enumerate((.2, .5, .7, .7, .95, None))]}
        payload = DRIFT.run(q, run_id="ser11-still-valid")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        verifier = load(SKILL / "scripts/verify.py", "_ser11_test_verify_after_ser12")
        self.assertTrue(verifier.verify(
            payload, expected_request=q, expected_run_id="ser11-still-valid")["valid"])

    def test_existing_drift_release_still_checks(self):
        from hub_scripts.skill_execution.domain_context.release import release_integrity
        self.assertEqual(len(release_integrity(SKILL, DRIFT.REQUIRED_RELEASE_PATHS)["artifacts"]), 28)


if __name__ == "__main__":
    unittest.main()
