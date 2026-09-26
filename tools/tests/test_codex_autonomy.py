from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools import validate_codex_autonomy as val
from tools import check_codex_autonomy_delta as delta

ROOT = Path(__file__).resolve().parents[2]


class CodexAutonomyTests(unittest.TestCase):
    def test_current_repository_passes(self):
        result = val.validate(ROOT)
        self.assertEqual("PASS", result["status"], result["issues"])
        self.assertEqual(5, result["custom_agents"])
        self.assertEqual(1, result["write_capable_agents"])

    def envelope(self):
        return json.loads(
            (ROOT / "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json")
            .read_text(encoding="utf-8")
        )

    def test_envelope_conforms_to_json_schema(self):
        payload = self.envelope()
        self.assertEqual([], val._validate_envelope_schema(ROOT, payload))

    def test_envelope_schema_rejects_unknown_root_property(self):
        payload = self.envelope()
        payload["unexpected"] = True
        issues = val._validate_envelope_schema(ROOT, payload)
        self.assertTrue(any(item.startswith("ENVELOPE_SCHEMA_ERROR") for item in issues))

    def test_a2_requires_explicit_reference_and_contract(self):
        payload = self.envelope()
        payload["activation"]["state"] = "ACTIVE_A0_A1_A2"
        payload["activation"]["a2_reference"] = None
        payload["authority_classes"]["A2"]["autonomous"] = True
        payload["a2_contract"] = None
        issues = val.validate_envelope_data(payload, max_threads=5)
        self.assertIn("A2_REFERENCE_REQUIRED", issues)
        self.assertIn("A2_CONTRACT_REQUIRED", issues)

    def test_a3_cannot_be_autonomous(self):
        payload = self.envelope()
        payload["authority_classes"]["A3"]["autonomous"] = True
        issues = val.validate_envelope_data(payload, max_threads=5)
        self.assertIn("A3_MUST_BE_HUMAN_ONLY", issues)

    def test_blind_retry_budget_must_be_zero(self):
        payload = self.envelope()
        payload["budgets"]["same_state_same_command_retries"] = 1
        issues = val.validate_envelope_data(payload, max_threads=5)
        self.assertIn("BLIND_RETRY_MUST_BE_ZERO", issues)

    def test_single_writer_budget_is_fixed(self):
        payload = self.envelope()
        payload["budgets"]["max_write_capable_agents"] = 2
        issues = val.validate_envelope_data(payload, max_threads=5)
        self.assertIn("SINGLE_WRITER_REQUIRED", issues)

    def test_envelope_concurrency_cannot_exceed_codex_limit(self):
        payload = self.envelope()
        payload["budgets"]["max_concurrent_subagents"] = 6
        issues = val.validate_envelope_data(payload, max_threads=5)
        self.assertIn("CONCURRENCY_EXCEEDS_CODEX_CONFIG", issues)

    def test_repo_scope_requires_write_and_protected_roots(self):
        payload = self.envelope()
        payload["repo_scope"]["write_roots"] = []
        payload["repo_scope"]["protected_roots"] = []
        issues = val.validate_envelope_data(payload, max_threads=5)
        self.assertIn("WRITE_ROOTS_REQUIRED", issues)
        self.assertIn("PROTECTED_ROOTS_REQUIRED", issues)

    def test_initial_b1_envelope_keeps_a2_disabled(self):
        payload = self.envelope()
        self.assertEqual("ACTIVE_A0_A1", payload["activation"]["state"])
        self.assertIsNone(payload["activation"]["a2_reference"])
        self.assertFalse(payload["authority_classes"]["A2"]["autonomous"])
        self.assertFalse(payload["authority_classes"]["A3"]["autonomous"])

    def test_delta_classifier_allows_b1_recovery(self):
        self.assertEqual(
            "ALLOWED_A1",
            delta.classify_path("tools/skill_enforcement/real_campaigns/b1/g6_recovery/example.py"),
        )

    def test_delta_classifier_protects_product(self):
        self.assertEqual(
            "PROTECTED",
            delta.classify_path("ambiente_fonte/.assistant/skills/example/SKILL.md"),
        )

    def test_delta_classifier_requires_human_for_controller_governance(self):
        self.assertEqual(
            "HUMAN_GATE_REQUIRED",
            delta.classify_path(".codex/config.toml"),
        )

    def test_delta_classifier_rejects_unlisted_paths(self):
        self.assertEqual(
            "OUTSIDE_A1",
            delta.classify_path("README.md"),
        )


if __name__ == "__main__":
    unittest.main()
