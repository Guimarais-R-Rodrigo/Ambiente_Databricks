"""Regressões puras do certifier prospectivo SER; não executam campanha FULL."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "ser_certify_under_test", ROOT / "tools/skill_enforcement/ser_certify.py")
cert = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cert)


def synthetic_summary():
    state = {
        "head": "a" * 40, "tree": "b" * 40,
        "branch": cert.BRANCH, "origin_main": "c" * 40,
        "merge_base": "c" * 40, "shallow": "false",
        "status": "", "behind": 0, "ahead": 1,
    }
    payload = {
        "certifier_version": cert.CERTIFIER_VERSION,
        "profile": cert.PROFILE,
        "run_id": "run",
        "started_at_utc": "2026-09-23T00:00:00+00:00",
        "ended_at_utc": "2026-09-23T00:01:00+00:00",
        "status": "PASS", "issues": [],
        "steps": [{"name": "gate", "exit_code": 0}],
        "route_gate": {"status": "PASS", "issues": []},
        "evidence_gate": {"status": "PASS", "issues": []},
        "git_before": state, "git_after": copy.deepcopy(state),
        "host": {}, "certifier_sha256": "d" * 64,
        "historical_se08": "PASS_SEPARATE_CHANNEL",
        "claims": {
            "skill": cert.SKILL, "protected_surface": cert.SURFACE,
            "current_level": "L2", "target_level": "L3",
            "policy_promotion_authorized": False, "merge_authorized": False,
            "execution_authenticated": False, "human_authority_authenticated": False,
        },
    }
    return cert._seal(payload)


class SerCertifierTests(unittest.TestCase):
    def test_profile_is_distinct_from_historical_se08(self):
        self.assertEqual("SER-CERT-1", cert.CERTIFIER_VERSION)
        self.assertNotIn("se08", cert.PROFILE.lower())

    def test_current_tree_route_is_coherent_pre_promotion(self):
        result = cert._route_static_gate()
        self.assertEqual("PASS", result["status"], result)

    def test_certification_record_detects_tamper_and_head_mismatch(self):
        payload = synthetic_summary()
        self.assertTrue(cert.verify_certification(payload, expected_head="a" * 40)["valid"])
        tampered = copy.deepcopy(payload)
        tampered["claims"]["policy_promotion_authorized"] = True
        self.assertFalse(cert.verify_certification(tampered, expected_head="a" * 40)["valid"])
        self.assertFalse(cert.verify_certification(payload, expected_head="e" * 40)["valid"])

    def test_published_receipt_verifier_requires_local_record(self):
        verifier = cert._load_module(
            "_ser_cert_test_verifier",
            cert.ASSISTANT_ROOT / "skills" / cert.SKILL / "scripts/object_validation.py")
        checked = verifier.verify_receipt({})
        self.assertFalse(checked["valid"])
        self.assertIn("LOCAL_RECORD_REQUIRED", checked["issues"])


if __name__ == "__main__":
    unittest.main()
