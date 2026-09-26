from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import validate_codex_autonomy as val
from tools import check_codex_autonomy_delta as delta

ROOT = Path(__file__).resolve().parents[2]


class CodexAutonomyTests(unittest.TestCase):
    def test_current_repository_passes(self):
        result = val.validate(ROOT)
        self.assertEqual("PASS", result["status"], result["issues"])
        self.assertEqual(5, result["custom_agents"])
        self.assertEqual(1, result["write_capable_agents"])
        self.assertEqual(":read-only", result["root_permissions"])
        self.assertEqual("ser-b1-a1", result["executor_permissions"])

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
        self.assertEqual("HUMAN_GATE_REQUIRED", delta.classify_path(".codex/config.toml"))

    def test_delta_classifier_rejects_unlisted_paths(self):
        self.assertEqual("OUTSIDE_A1", delta.classify_path("README.md"))

    def test_hooks_are_enabled_and_configured(self):
        result = val.validate(ROOT)
        self.assertTrue(result["hooks_configured"])
        self.assertNotIn("HOOKS_NOT_ENABLED", result["issues"])
        self.assertNotIn("HOOK_CONFIG_INVALID", result["issues"])
        self.assertNotIn("HOOK_CONFIG_MISSING_PRE_OR_POST", result["issues"])

    def test_runtime_qualification_document_exists(self):
        self.assertTrue((ROOT / "docs/operations/CODEX_RUNTIME_QUALIFICATION.md").is_file())

    def test_delta_classifier_protects_frozen_g6(self):
        self.assertEqual(
            "PROTECTED",
            delta.classify_path("tools/skill_enforcement/real_campaigns/b1/g6/ser03_free_probe.py"),
        )

    def test_delta_classifier_rejects_qualified_b1_adapter(self):
        self.assertEqual(
            "OUTSIDE_A1",
            delta.classify_path("tools/skill_enforcement/real_campaigns/b1/adapter.py"),
        )

    def test_delta_classifier_protects_historical_b1_evidence(self):
        self.assertEqual(
            "PROTECTED",
            delta.classify_path("docs/sprints/skill_enforcement_rollout/PARALELO/B1/G6/G6_R10_REMOTE_PASS.md"),
        )

    def test_delta_classifier_allows_live_b1_state(self):
        self.assertEqual(
            "ALLOWED_A1",
            delta.classify_path("docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTHORING_STATE.json"),
        )

    def test_delta_classifier_allows_autonomy_journal(self):
        self.assertEqual(
            "ALLOWED_A1",
            delta.classify_path("docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/RUN-001.md"),
        )

    def test_delta_classifier_requires_human_for_controller_requirements(self):
        self.assertEqual(
            "HUMAN_GATE_REQUIRED",
            delta.classify_path("tools/requirements-codex-autonomy.txt"),
        )

    def test_permission_profile_matches_envelope_write_roots(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        issues = val._validate_permission_profile(cfg, self.envelope())
        self.assertEqual([], issues)

    def test_root_and_agents_use_permission_profiles_not_legacy_sandbox(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        self.assertEqual(":read-only", cfg["default_permissions"])
        self.assertNotIn("sandbox_mode", cfg)
        for role, (filename, expected_profile, _model, _effort) in val.EXPECTED_AGENTS.items():
            agent = val._read_toml(ROOT / ".codex/agents" / filename)
            self.assertEqual(expected_profile, agent["default_permissions"], role)
            self.assertNotIn("sandbox_mode", agent, role)

    def test_approval_escalation_is_fail_closed(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        granular = cfg["approval_policy"]["granular"]
        self.assertFalse(granular["sandbox_approval"])
        self.assertFalse(granular["request_permissions"])
        self.assertFalse(granular["mcp_elicitations"])
        self.assertFalse(granular["skill_approval"])
        self.assertTrue(granular["rules"])

    def _temporary_git_repo(self) -> tuple[Path, mock._patch, mock._patch]:
        repo = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
        envelope = repo / "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json"
        envelope.parent.mkdir(parents=True)
        envelope.write_text(json.dumps({
            "repo_scope": {
                "write_roots": ["allowed/**"],
                "protected_roots": ["protected/**"],
                "shared_roots_requiring_human_gate": ["governance/**"],
            }
        }), encoding="utf-8")
        return repo, mock.patch.object(delta, "ROOT", repo), mock.patch.object(delta, "ENVELOPE", envelope)

    @staticmethod
    def _git(repo: Path, *args: str, input_text: str | None = None) -> str:
        proc = subprocess.run(
            ["git", *args], cwd=repo, input=input_text, capture_output=True, text=True, check=True
        )
        return proc.stdout.strip()

    def test_delta_rejects_protected_to_allowed_rename(self):
        repo, root_patch, envelope_patch = self._temporary_git_repo()
        with root_patch, envelope_patch:
            (repo / "protected").mkdir()
            (repo / "protected/x.txt").write_text("x", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            base = self._git(repo, "rev-parse", "HEAD")
            (repo / "allowed").mkdir()
            self._git(repo, "mv", "protected/x.txt", "allowed/x.txt")
            self._git(repo, "commit", "-m", "rename")
            head = self._git(repo, "rev-parse", "HEAD")
            result = delta.check_delta(base, head)
            self.assertEqual("FAIL", result["status"])
            self.assertTrue(any(row["path"] == "protected/x.txt" for row in result["violations"]))

    def test_delta_rejects_allowed_to_protected_rename(self):
        repo, root_patch, envelope_patch = self._temporary_git_repo()
        with root_patch, envelope_patch:
            (repo / "allowed").mkdir()
            (repo / "allowed/x.txt").write_text("x", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            base = self._git(repo, "rev-parse", "HEAD")
            (repo / "protected").mkdir()
            self._git(repo, "mv", "allowed/x.txt", "protected/x.txt")
            self._git(repo, "commit", "-m", "rename")
            head = self._git(repo, "rev-parse", "HEAD")
            result = delta.check_delta(base, head)
            self.assertEqual("FAIL", result["status"])
            self.assertTrue(any(row["path"] == "protected/x.txt" for row in result["violations"]))

    def test_delta_rejects_protected_delete(self):
        repo, root_patch, envelope_patch = self._temporary_git_repo()
        with root_patch, envelope_patch:
            (repo / "protected").mkdir()
            (repo / "protected/x.txt").write_text("x", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            base = self._git(repo, "rev-parse", "HEAD")
            self._git(repo, "rm", "protected/x.txt")
            self._git(repo, "commit", "-m", "delete")
            head = self._git(repo, "rev-parse", "HEAD")
            self.assertEqual("FAIL", delta.check_delta(base, head)["status"])

    def test_delta_rejects_tracked_symlink_even_under_allowed_root(self):
        repo, root_patch, envelope_patch = self._temporary_git_repo()
        with root_patch, envelope_patch:
            (repo / "allowed").mkdir()
            (repo / "allowed/x.txt").write_text("x", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            base = self._git(repo, "rev-parse", "HEAD")
            blob = self._git(repo, "hash-object", "-w", "--stdin", input_text="../protected/x.txt")
            self._git(repo, "update-index", "--add", "--cacheinfo", f"120000,{blob},allowed/link")
            self._git(repo, "commit", "-m", "symlink")
            head = self._git(repo, "rev-parse", "HEAD")
            result = delta.check_delta(base, head)
            self.assertEqual("FAIL", result["status"])
            self.assertTrue(any(row["classification"] == "SYMLINK_NOT_ALLOWED" for row in result["violations"]))

    def _state(self):
        return {
            "schema_version": "SER-B1-AUTHORING-2",
            "base_commit": "a" * 40,
            "policy_changed": False,
            "gates": {
                "G7_PROMOTION_PROPOSAL": "NOT_AUTHORIZED",
                "G8_POST_POLICY": "NOT_RUN",
                "G9_INTEGRATION": "NOT_AUTHORIZED",
            },
            "blocked_by": ["AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION"],
            "stage": "B1_WORK",
            "launchable": False,
            "autonomous_controller": {
                "envelope_state": "ACTIVE_A0_A1",
                "runtime_validation": "NOT_RUN",
                "effective_config_observation": "NOT_RUN",
                "first_material_controller_session": "NOT_RUN",
            },
        }

    def test_state_transition_rejects_controller_authority_mutation(self):
        base = self._state()
        candidate = copy.deepcopy(base)
        candidate["autonomous_controller"]["envelope_state"] = "ACTIVE_A0_A1_A2"
        issues = delta.validate_state_transition(base, candidate)
        self.assertIn(
            "STATE_CONTROLLER_AUTHORITY_MUTATION:autonomous_controller.envelope_state", issues
        )

    def test_state_transition_rejects_unproven_blocker_removal(self):
        base = self._state()
        candidate = copy.deepcopy(base)
        candidate["blocked_by"] = []
        issues = delta.validate_state_transition(base, candidate)
        self.assertIn(
            "STATE_BLOCKER_REMOVAL_UNPROVEN:AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION", issues
        )

    def test_state_transition_accepts_runtime_blocker_removal_after_proof(self):
        base = self._state()
        candidate = copy.deepcopy(base)
        candidate["blocked_by"] = []
        candidate["autonomous_controller"]["runtime_validation"] = "PASS"
        candidate["autonomous_controller"]["effective_config_observation"] = "PASS"
        self.assertEqual([], delta.validate_state_transition(base, candidate))

    def test_state_transition_rejects_launchable_with_blockers(self):
        base = self._state()
        candidate = copy.deepcopy(base)
        candidate["launchable"] = True
        self.assertIn("STATE_LAUNCHABLE_WITH_BLOCKERS", delta.validate_state_transition(base, candidate))

    def test_claude_uses_progressive_changelog_disclosure(self):
        text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("Não carregue `CHANGELOG.md` integralmente", text)


if __name__ == "__main__":
    unittest.main()
