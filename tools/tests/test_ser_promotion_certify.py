from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "promotion", ROOT / "tools/skill_enforcement/ser_promotion_certify.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def synthetic_summary():
    state = {
        "head": "a" * 40,
        "tree": "b" * 40,
        "branch": m.BRANCH,
        "origin_main": "c" * 40,
        "merge_base": "c" * 40,
        "shallow": "false",
        "status": "",
        "behind": 0,
        "ahead": 1,
    }
    steps = [
        {
            "name": name,
            "exit_code": 0,
            "command_started": True,
            "process_cleanup": "COMPLETE",
        }
        for name in sorted(m._required_zero_steps())
    ]
    steps.extend(
        {
            "name": name,
            "exit_code": 1,
            "command_started": True,
            "process_cleanup": "COMPLETE",
        }
        for name in m.HISTORICAL_EXPECTATIONS
    )
    historical = [
        {
            "name": name,
            "status": "EXPECTED_TEMPORAL_FAIL",
            "exit_code": 1,
            "expected_failures": sorted(expected),
            "observed_failures": sorted(expected),
            "observed_errors": [],
            "summary_counts": {"failures": len(expected)},
            "unexpected_failures": [],
            "missing_failures": [],
        }
        for name, expected in m.HISTORICAL_EXPECTATIONS.items()
    ]
    payload = {
        "version": m.VERSION,
        "profile": m.PROFILE,
        "run_id": "synthetic",
        "started_at_utc": "2026-09-23T00:00:00+00:00",
        "ended_at_utc": "2026-09-23T00:01:00+00:00",
        "status": "PASS",
        "issues": [],
        "steps": steps,
        "promotion_gate": {"status": "PASS", "issues": []},
        "route_gate": {"status": "PASS", "issues": []},
        "evidence_gate": {"status": "PASS", "issues": []},
        "historical_channels": historical,
        "git_before": state,
        "git_after": copy.deepcopy(state),
        "claims": m._claims(),
        "certifier_sha256": "d" * 64,
        "policy_sha256": "e" * 64,
    }
    return m._seal(payload)


class PromotionCertifierTests(unittest.TestCase):
    def test_identity_is_distinct_and_versioned_after_r1(self):
        self.assertEqual("SER-PROMOTION-CERT-2", m.VERSION)
        self.assertEqual("ser01-object-validation-post-promotion", m.PROFILE)
        self.assertEqual("serprom2:", m.ID_PREFIX)

    def test_current_tree_is_promotion_ready(self):
        result = m._promotion_gate()
        self.assertEqual("PASS", result["status"], result)
        route = m._route_gate_post_promotion()
        self.assertEqual("PASS", route["status"], route)

    def test_pre_promotion_policy_fixture_is_rejected_without_mutating_real_policy(self):
        fixture = dict(m._policy_entry())
        fixture["current_level"] = "L2"
        fixture["policy_status"] = "defined"
        with mock.patch.object(m, "_policy_entry", return_value=fixture):
            result = m._promotion_gate()
        self.assertEqual("FAIL", result["status"])
        self.assertIn("POLICY_LEVEL_NOT_L3", result["issues"])
        self.assertIn("POLICY_STATUS_NOT_IMPLEMENTED", result["issues"])

    def test_historical_classifier_accepts_only_exact_failures_and_zero_errors(self):
        expected = {"test_a", "test_b"}
        clean = (
            "FAIL: test_a (x)\n"
            "FAIL: test_b (x)\n"
            "FAILED (failures=2)\n"
        )
        result = m._historical_result("hist", 1, clean, expected)
        self.assertEqual("EXPECTED_TEMPORAL_FAIL", result["status"])

        for output in (
            clean + "FAIL: test_other (x)\n",
            clean + "ERROR: test_other (x)\nFAILED (failures=2, errors=1)\n",
            "FAIL: test_a (x)\nFAILED (failures=1)\n",
        ):
            with self.subTest(output=output):
                result = m._historical_result("hist", 1, output, expected)
                self.assertEqual("UNEXPECTED_RESULT", result["status"])

    def test_certification_verifier_rejects_tamper_head_and_historical_errors(self):
        payload = synthetic_summary()
        self.assertTrue(m.verify_certification(payload, expected_head="a" * 40)["valid"])

        tampered = copy.deepcopy(payload)
        tampered["claims"]["merge_authorized"] = True
        m._seal(tampered)
        self.assertFalse(m.verify_certification(tampered, expected_head="a" * 40)["valid"])

        self.assertFalse(m.verify_certification(payload, expected_head="f" * 40)["valid"])

        broken = synthetic_summary()
        broken["historical_channels"][0]["observed_errors"] = ["test_unexpected"]
        m._seal(broken)
        self.assertFalse(m.verify_certification(broken, expected_head="a" * 40)["valid"])

    def test_required_step_set_includes_regression_legacy_and_non_sef_ci(self):
        required = m._required_zero_steps()
        self.assertIn("promotion_certifier_regression", required)
        self.assertIn("legacy_create_l3", required)
        self.assertIn("policy_io_regression", required)
        self.assertIn("local_certifier_regression", required)
        for stage in m.CI_NON_SEF_STAGES:
            self.assertIn("ci_" + stage, required)


if __name__ == "__main__":
    unittest.main()
