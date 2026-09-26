from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools import validate_codex_autonomy as val

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

    def test_a2_requires_explicit_reference(self):
        payload = self.envelope()
        payload["activation"]["state"] = "ACTIVE_A0_A1_A2"
        payload["activation"]["a2_reference"] = None
        payload["authority_classes"]["A2"]["autonomous"] = True
        issues = val.validate_envelope_data(payload, max_threads=5)
        self.assertIn("A2_REFERENCE_REQUIRED", issues)

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

    def test_initial_b1_envelope_keeps_a2_disabled(self):
        payload = self.envelope()
        self.assertEqual("ACTIVE_A0_A1", payload["activation"]["state"])
        self.assertIsNone(payload["activation"]["a2_reference"])
        self.assertFalse(payload["authority_classes"]["A2"]["autonomous"])
        self.assertFalse(payload["authority_classes"]["A3"]["autonomous"])


if __name__ == "__main__":
    unittest.main()
