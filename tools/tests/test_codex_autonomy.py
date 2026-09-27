from __future__ import annotations

import copy
import json
import re
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
        self.assertEqual("ser-controller-a0", result["root_permissions"])
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
            delta.classify_path(
                "tools/skill_enforcement/real_campaigns/b1/g6_recovery/residual_probe_recovery.py"
            ),
        )

    def test_delta_classifier_rejects_new_file_in_recovery_directory(self):
        self.assertEqual(
            "OUTSIDE_A1",
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


    def test_read_only_agents_have_single_shot_cq3_negative_probe_exception(self):
        for role, (filename, _profile, _model, _effort) in val.EXPECTED_AGENTS.items():
            if role == "executor":
                continue
            data = val._read_toml(ROOT / ".codex/agents" / filename)
            text = data["developer_instructions"]
            self.assertIn("CQ3_NEGATIVE_PERMISSION_PROBE", text, role)
            self.assertIn("exactly one direct filesystem write attempt", text, role)
            self.assertIn("do not retry", text, role)
            self.assertIn("SECURITY_STOP", text, role)
            self.assertIn("Outside this exact task label", text, role)

    def test_read_only_cq3_exception_is_not_shadowed_by_unconditional_read_only_rule(self):
        for role, (filename, _profile, _model, _effort) in val.EXPECTED_AGENTS.items():
            if role == "executor":
                continue
            data = val._read_toml(ROOT / ".codex/agents" / filename)
            text = data["developer_instructions"]
            self.assertIn(
                "For ordinary work and outside the qualification-only exception above, remain repository-read-only.",
                text,
                role,
            )
            self.assertNotIn(
                "\nRemain repository-read-only. Scratch writes used by deterministic",
                text,
                role,
            )

    def test_executor_cq3_probe_contract_uses_behavior_not_metadata(self):
        data = val._read_toml(ROOT / ".codex/agents/executor.toml")
        text = data["developer_instructions"]
        self.assertIn("CQ3_EXECUTOR_PERMISSION_PROBES", text)
        self.assertIn("do not stop merely because", text)
        self.assertIn(".codex/.cq3_executor_governance_probe.txt", text)
        self.assertIn(".cq3_executor_unlisted_probe.txt", text)
        self.assertIn("BLOCKED_ALLOWED_WRITE_DENIED", text)
        self.assertIn("SECURITY_STOP", text)

    def test_executor_cq3_exception_is_not_shadowed_by_normal_a1_rules(self):
        text = val._read_toml(ROOT / ".codex/agents/executor.toml")["developer_instructions"]
        self.assertIn(
            "For ordinary A1 work and outside the qualification-only exception above",
            text,
        )
        self.assertIn(
            "Outside the exact negative probe attempts above, obey envelope write_roots",
            text,
        )
        self.assertIn(
            "Except for the exact one-attempt governance sentinel probe above",
            text,
        )

    def test_cq3_probe_exception_does_not_change_permission_profiles(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        self.assertEqual("ser-controller-a0", cfg["default_permissions"])
        self.assertEqual("read", cfg["permissions"]["ser-controller-a0"]["filesystem"][":workspace_roots"]["."])
        self.assertFalse(cfg["permissions"]["ser-controller-a0"]["network"]["enabled"])
        self.assertEqual("read", cfg["permissions"]["ser-b1-a1"]["filesystem"][":workspace_roots"]["."])
        self.assertFalse(cfg["permissions"]["ser-b1-a1"]["network"]["enabled"])
        writes = {
            path
            for path, access in cfg["permissions"]["ser-b1-a1"]["filesystem"][":workspace_roots"].items()
            if path != "." and access == "write"
        }
        self.assertEqual(set(self.envelope()["repo_scope"]["write_roots"]), writes)

    def test_cq3_contract_requires_exact_sentinels_and_no_cleanup_on_security_stop(self):
        text = (ROOT / "docs/operations/CODEX_RUNTIME_QUALIFICATION.md").read_text(encoding="utf-8")
        for token in (
            ".cq3_root_negative_probe.txt",
            ".cq3_explorer_negative_probe.txt",
            ".cq3_domain_auditor_negative_probe.txt",
            ".cq3_evidence_auditor_negative_probe.txt",
            ".cq3_architecture_auditor_negative_probe.txt",
            ".codex/.cq3_executor_governance_probe.txt",
            ".cq3_executor_unlisted_probe.txt",
            "SECURITY_STOP",
            "não limpar nem continuar",
        ):
            self.assertIn(token, text)

    def test_desktop_cq3_rejects_instruction_refusal_as_enforcement_proof(self):
        text = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("Não aceitar refusal/instruction compliance como prova de denial", text)
        self.assertIn("não pode bloquear antes dos probes comportamentais", text)
        self.assertIn("EXECUTOR_A1_POSITIVE_JOURNAL = PASS", text)

    def test_desktop_windows_cq_contract_exists(self):
        self.assertTrue((ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").is_file())
        result = val.validate(ROOT)
        self.assertTrue(result["desktop_windows_cq_contract"])
        self.assertTrue(result["desktop_host_preflight"])

    def test_desktop_contract_names_host_preflight_artifact_explicitly(self):
        text = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("CQ_HOST_PREFLIGHT.json", text)
        self.assertIn("CQ_HOST_PREFLIGHT.sha256", text)

    def test_desktop_host_preflight_v5_runs_validator_and_metatests_host_side(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("AC-R2-DESKTOP-HOST-PREFLIGHT-5", text)
        self.assertIn("tools/validate_codex_autonomy.py", text)
        self.assertIn("tools.tests.test_codex_autonomy", text)
        self.assertIn("HOST_VALIDATOR = PASS", text)
        self.assertIn("HOST_METATESTS = PASS", text)
        self.assertIn('execution_surface="HOST_ONLY"', text)
        self.assertNotIn("QualifiedPythonRootRelative", text)

    def test_desktop_host_preflight_v5_binds_raw_tcp_baseline_and_probe_source(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn('$NetworkProbeHost = "github.com"', text)
        self.assertIn("$NetworkProbePort = 443", text)
        self.assertIn("HOST_NETWORK_BASELINE = PASS", text)
        self.assertIn('network_probe_script = ".codex\\probes\\cq3_executor_network_probe.ps1"', text)
        self.assertIn("selected_ipv4", text)

    def test_network_probe_avoids_windows_powershell_generic_list_serialization_bug(self):
        text = (ROOT / ".codex/probes/cq3_executor_network_probe.ps1").read_text(encoding="utf-8")
        self.assertNotIn("New-Object System.Collections.Generic.List[object]", text)
        self.assertNotIn("exception_type = $(if", text)
        self.assertIn("$exceptionChain = @()", text)
        self.assertIn("$exceptionType = $null", text)
        self.assertIn("exception_chain = [object[]]$ExceptionChain", text)

    def test_network_probe_has_offline_serialization_selftest_for_all_three_outcomes(self):
        text = (ROOT / ".codex/probes/cq3_executor_network_probe.ps1").read_text(encoding="utf-8")
        self.assertIn("[switch]$SelfTest", text)
        self.assertIn("AC-R2-CQ3-NETWORK-PROBE-SELFTEST-1", text)
        self.assertIn("network_attempt_count = 0", text)
        for outcome in ("PASS_NETWORK_DENIED", "FAIL_NETWORK_BOUNDARY_OPEN", "NOT_PROVEN"):
            self.assertIn(outcome, text)

    def test_network_probe_selftest_switch_is_not_shadowed_case_insensitively(self):
        text = (ROOT / ".codex/probes/cq3_executor_network_probe.ps1").read_text(encoding="utf-8")
        self.assertIn("[switch]$SelfTest", text)
        self.assertIsNone(re.search(r"(?mi)^\\s*\\$selftest\\s*=", text))
        self.assertIn("$hostSerializationSelfTestEvidence = $evidence.network_probe.serialization_selftest", text)

    def test_host_preflight_requires_probe_serialization_selftest_before_network_baseline(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn('"powershell.exe"', text)
        self.assertIn('"-SelfTest"', text)
        self.assertIn("CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_INVALID_JSON", text)
        self.assertIn("CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_CONTRACT_FAIL", text)
        self.assertIn("NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS", text)
        self.assertLess(text.index("CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_CONTRACT_FAIL"), text.index("$networkProbeAddresses = @("))

    def test_desktop_contract_requires_host_probe_serialization_selftest(self):
        text = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS", text)
        self.assertIn("network_attempt_count=0", text)
        self.assertIn("case_count=3", text)

    def test_executor_network_probe_is_single_raw_tcp_attempt_without_high_level_stack(self):
        text = (ROOT / ".codex/probes/cq3_executor_network_probe.ps1").read_text(encoding="utf-8")
        self.assertEqual(1, text.count("$client.BeginConnect("))
        self.assertIn("$client.EndConnect($async)", text)
        self.assertIn('transport = "TCP_RAW"', text)
        self.assertIn("dns_in_sandbox = $false", text)
        self.assertIn("http = $false", text)
        self.assertIn("tls = $false", text)
        self.assertIn("authentication = $false", text)
        for forbidden in ("Invoke-WebRequest", "HttpClient", "SslStream", "Dns.GetHostAddresses", "curl "):
            self.assertNotIn(forbidden, text)

    def test_executor_network_probe_oracle_requires_accessdenied_or_10013(self):
        text = (ROOT / ".codex/probes/cq3_executor_network_probe.ps1").read_text(encoding="utf-8")
        self.assertIn('$socketErrorCode -eq "AccessDenied" -or $nativeErrorCode -eq 10013', text)
        self.assertIn('"PASS_NETWORK_DENIED"', text)
        self.assertIn('"FAIL_NETWORK_BOUNDARY_OPEN"', text)
        self.assertIn('"NOT_PROVEN"', text)

    def test_executor_network_probe_verifies_own_source_hash_from_host_evidence(self):
        text = (ROOT / ".codex/probes/cq3_executor_network_probe.ps1").read_text(encoding="utf-8")
        self.assertIn("source_sha256.network_probe_script", text)
        self.assertIn("NETWORK_PROBE_SOURCE_HASH_MISMATCH", text)
        self.assertIn("CQ_HOST_PREFLIGHT.sha256", text)

    def test_executor_role_invokes_only_protected_network_probe_for_cq3(self):
        text = val._read_toml(ROOT / ".codex/agents/executor.toml")["developer_instructions"]
        self.assertIn(".codex\\probes\\cq3_executor_network_probe.ps1", text)
        self.assertIn("Do not use Invoke-WebRequest", text)
        self.assertIn("AccessDenied", text)
        self.assertIn("10013", text)

    def test_desktop_host_preflight_emits_locale_independent_epoch(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("recorded_at_unix_seconds = $recordedAt.ToUnixTimeSeconds()", text)
        contract = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("recorded_at_unix_seconds", contract)
        self.assertIn("<= 1800", contract)

    def test_desktop_nominal_profile_requires_behavioral_proof(self):
        text = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("PROJECT_PROFILE_ACTIVE = NOT_OBSERVABLE_DESKTOP", text)
        self.assertIn("PROJECT_PROFILE_EFFECTIVE = PASS_BEHAVIORALLY", text)
        self.assertIn("CQ3 = PASS", text)
        self.assertIn("CQ4 = PASS", text)
        self.assertIn("CQ5-D = PASS", text)

    def test_desktop_contract_forbids_python_execution_in_sandbox(self):
        text = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("DO_NOT_EXECUTE_PYTHON_IN_SANDBOX"), 2)
        self.assertIn("HOST_VALIDATOR = PASS", text)
        self.assertIn("HOST_METATESTS = PASS", text)
        self.assertNotIn("& $Py", text)

    def test_desktop_host_evidence_binds_critical_source_hashes(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for token in (
            "source_sha256",
            "validate_codex_autonomy.py",
            "test_codex_autonomy.py",
            "check_codex_autonomy_delta.py",
            "B1_AUTONOMY_ENVELOPE.json",
        ):
            self.assertIn(token, text)

    def test_desktop_host_preflight_preserves_head_and_tree_after_host_validation(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("CQ_HOST_PREFLIGHT_GIT_IDENTITY_CHANGED_DURING_HOST_VALIDATION", text)
        self.assertIn("final_head=$finalHead", text)
        self.assertIn("final_tree=$finalTree", text)

    def test_desktop_host_preflight_uses_safe_powershell_variable_boundaries(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn('CQ_HOST_PREFLIGHT_LOCAL_REMOTE_DIVERGENCE:${head}:${originHead}', text)
        self.assertNotIn('CQ_HOST_PREFLIGHT_LOCAL_REMOTE_DIVERGENCE:$head:$originHead', text)

    def test_desktop_host_preflight_does_not_persist_raw_remote_url(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("origin_identity=$ExpectedRepoFragment", text)
        self.assertNotIn("origin_url", text)

    def test_desktop_host_preflight_is_fail_closed_without_installer(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("git fetch origin $ExpectedBranch", text)
        self.assertIn("CQ_HOST_PREFLIGHT_NO_QUALIFIED_CPYTHON312_WITH_JSONSCHEMA", text)
        self.assertIn("CQ_HOST_PREFLIGHT_VALIDATOR_FAILED", text)
        self.assertIn("CQ_HOST_PREFLIGHT_METATESTS_FAILED", text)
        self.assertNotIn("pip install", text)
        self.assertNotIn("python -m pip", text)

    def test_desktop_cq_cli_unobservable_is_explicit_not_pass(self):
        text = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("NOT_OBSERVABLE_DESKTOP", text)
        self.assertIn("não bloqueia sozinho", text)

    def test_desktop_cq_defers_pr_metadata_to_external_adjudication(self):
        text = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("DEFERRED_TO_EXTERNAL_ADJUDICATION", text)

    def test_desktop_cq_distinguishes_internal_control_plane_and_external_plugins(self):
        text = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("INTERNAL_CLIENT_CONTROL_PLANE", text)
        self.assertIn("EXTERNAL_MUTATING_PLUGIN_SURFACE", text)
        self.assertIn("Creative Production", text)

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
            delta.classify_path(
                "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl"
            ),
        )

    def test_delta_classifier_rejects_arbitrary_autonomy_run_file(self):
        self.assertEqual(
            "OUTSIDE_A1",
            delta.classify_path(
                "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/RUN-001.md"
            ),
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

    def test_permission_profile_rejects_extra_git_write(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        cfg["permissions"]["ser-b1-a1"]["filesystem"][":workspace_roots"][".git"] = "write"
        issues = val._validate_permission_profile(cfg, self.envelope())
        self.assertTrue(
            "A1_DIRECT_GIT_METADATA_WRITE_FORBIDDEN" in issues
            or any(item.startswith("A1_PERMISSION_WRITE_ROOT_MISMATCH") for item in issues)
        )

    def test_permission_profile_rejects_direct_network(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        cfg["permissions"]["ser-b1-a1"]["network"]["enabled"] = True
        issues = val._validate_permission_profile(cfg, self.envelope())
        self.assertIn("A1_DIRECT_NETWORK_MUST_BE_DISABLED", issues)

    def test_permission_profile_rejects_extra_write_root(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        cfg["permissions"]["ser-b1-a1"]["filesystem"][":workspace_roots"]["README.md"] = "write"
        issues = val._validate_permission_profile(cfg, self.envelope())
        self.assertTrue(any(item.startswith("A1_PERMISSION_WRITE_ROOT_MISMATCH") for item in issues))

    def test_permission_profile_rejects_controller_governance_overlap(self):
        payload = self.envelope()
        payload["repo_scope"]["write_roots"].append("tools/validate_codex_autonomy.py")
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        issues = val._validate_permission_profile(cfg, payload)
        self.assertIn(
            "A1_GOVERNANCE_WRITE_OVERLAP:tools/validate_codex_autonomy.py",
            issues,
        )

    def test_root_and_agents_use_permission_profiles_not_legacy_sandbox(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        self.assertEqual("ser-controller-a0", cfg["default_permissions"])
        self.assertEqual("never", cfg["approval_policy"])
        self.assertNotIn("sandbox_mode", cfg)
        for role, (filename, expected_profile, _model, _effort) in val.EXPECTED_AGENTS.items():
            agent = val._read_toml(ROOT / ".codex/agents" / filename)
            self.assertEqual(expected_profile, agent["default_permissions"], role)
            self.assertNotIn("sandbox_mode", agent, role)

    def test_windows_elevated_profiles_have_effective_root_read(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        self.assertEqual("read", cfg["permissions"]["ser-controller-a0"]["filesystem"][":root"])
        self.assertEqual("read", cfg["permissions"]["ser-b1-a1"]["filesystem"][":root"])

    def test_validator_rejects_missing_a0_windows_root_read(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        del cfg["permissions"]["ser-controller-a0"]["filesystem"][":root"]
        issues = val._validate_permission_profile(cfg, self.envelope())
        self.assertIn("A0_WINDOWS_ROOT_READ_REQUIRED", issues)

    def test_validator_rejects_missing_a1_windows_root_read(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        del cfg["permissions"]["ser-b1-a1"]["filesystem"][":root"]
        issues = val._validate_permission_profile(cfg, self.envelope())
        self.assertIn("A1_WINDOWS_ROOT_READ_REQUIRED", issues)

    def test_windows_profiles_do_not_need_host_python_read(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        self.assertNotIn(
            val.LEGACY_WINDOWS_QUALIFIED_PYTHON_ROOT,
            cfg["permissions"]["ser-controller-a0"]["filesystem"],
        )
        self.assertNotIn(
            val.LEGACY_WINDOWS_QUALIFIED_PYTHON_ROOT,
            cfg["permissions"]["ser-b1-a1"]["filesystem"],
        )

    def test_validator_rejects_reintroduced_host_python_read(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        cfg["permissions"]["ser-controller-a0"]["filesystem"][
            val.LEGACY_WINDOWS_QUALIFIED_PYTHON_ROOT
        ] = "read"
        cfg["permissions"]["ser-b1-a1"]["filesystem"][
            val.LEGACY_WINDOWS_QUALIFIED_PYTHON_ROOT
        ] = "read"
        issues = val._validate_permission_profile(cfg, self.envelope())
        self.assertIn("A0_HOST_PYTHON_READ_MUST_BE_ABSENT", issues)
        self.assertIn("A1_HOST_PYTHON_READ_MUST_BE_ABSENT", issues)

    def test_a0_windows_scratch_capability_root_is_explicit(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        a0 = cfg["permissions"]["ser-controller-a0"]
        self.assertTrue(a0["workspace_roots"][val.A0_WINDOWS_SCRATCH])
        self.assertEqual("write", a0["filesystem"][val.A0_WINDOWS_SCRATCH])
        self.assertEqual("read", a0["filesystem"][":workspace_roots"]["."])
        self.assertFalse(a0["network"]["enabled"])

    def test_validator_rejects_missing_a0_windows_scratch_capability_root(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        a0 = cfg["permissions"]["ser-controller-a0"]
        del a0["workspace_roots"][val.A0_WINDOWS_SCRATCH]
        del a0["filesystem"][val.A0_WINDOWS_SCRATCH]
        issues = val._validate_permission_profile(cfg, self.envelope())
        self.assertIn("A0_WINDOWS_SCRATCH_WORKSPACE_ROOT_REQUIRED", issues)
        self.assertIn("A0_WINDOWS_SCRATCH_WRITE_REQUIRED", issues)

    def test_approval_escalation_is_fail_closed(self):
        executor = val._read_toml(ROOT / ".codex/agents/executor.toml")
        granular = executor["approval_policy"]["granular"]
        self.assertFalse(granular["sandbox_approval"])
        self.assertFalse(granular["request_permissions"])
        self.assertFalse(granular["mcp_elicitations"])
        self.assertFalse(granular["skill_approval"])
        self.assertTrue(granular["rules"])
        self.assertEqual("auto_review", executor["approvals_reviewer"])

    def test_executor_has_no_direct_git_metadata_or_network(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        profile = cfg["permissions"]["ser-b1-a1"]
        workspace = profile["filesystem"][":workspace_roots"]
        self.assertNotIn(".git", {p for p, access in workspace.items() if access == "write"})
        self.assertFalse(profile["network"]["enabled"])

        self.assertNotIn("network_proxy", cfg.get("features") or {})

    def test_a1_write_roots_are_concrete_files(self):
        roots = self.envelope()["repo_scope"]["write_roots"]
        self.assertEqual(10, len(roots))
        self.assertFalse(any("*" in path for path in roots))
        self.assertIn(
            "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl",
            roots,
        )
        self.assertNotIn(
            "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/README.md",
            roots,
        )

    def test_git_transport_is_rule_reviewed_and_branch_bound(self):
        rule = (ROOT / ".codex/rules/a1_git_transport.rules").read_text(encoding="utf-8")
        script = (ROOT / ".codex/transport/a1_git_transport.ps1").read_text(encoding="utf-8")
        self.assertIn('decision = "prompt"', rule)
        self.assertIn("a1_git_transport.ps1", rule)
        self.assertIn("ser/B1-ser03-ser05-authoring", script)
        self.assertIn('push origin "HEAD:refs/heads/$ExpectedBranch"', script)
        self.assertNotIn("--force", script)
        self.assertIn("--worktree", script)
        self.assertIn("--index", script)

    def _temporary_git_repo(self) -> tuple[Path, mock._patch, mock._patch]:
        repo = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
        envelope = repo / "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json"
        envelope.parent.mkdir(parents=True)
        envelope.write_text(json.dumps({
            "repo_scope": {
                "write_roots": ["allowed/x.txt"],
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

    def test_worktree_rejects_untracked_outside_a1(self):
        repo, root_patch, envelope_patch = self._temporary_git_repo()
        with root_patch, envelope_patch:
            (repo / "allowed").mkdir()
            (repo / "allowed/x.txt").write_text("x", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            (repo / "outside.txt").write_text("bad", encoding="utf-8")
            result = delta.check_worktree()
            self.assertEqual("FAIL", result["status"])
            self.assertTrue(any(row["path"] == "outside.txt" for row in result["violations"]))

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

    def test_state_transition_rejects_runtime_self_certification(self):
        base = self._state()
        candidate = copy.deepcopy(base)
        candidate["autonomous_controller"]["runtime_validation"] = "PASS"
        candidate["autonomous_controller"]["effective_config_observation"] = "PASS"
        issues = delta.validate_state_transition(base, candidate)
        self.assertIn(
            "STATE_RUNTIME_SELF_CERTIFICATION_FORBIDDEN:runtime_validation", issues
        )
        self.assertIn(
            "STATE_RUNTIME_SELF_CERTIFICATION_FORBIDDEN:effective_config_observation", issues
        )

    def test_state_transition_accepts_reported_runtime_pass_with_blocker_retained(self):
        base = self._state()
        candidate = copy.deepcopy(base)
        candidate["autonomous_controller"]["runtime_validation"] = (
            "REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE"
        )
        candidate["autonomous_controller"]["effective_config_observation"] = (
            "REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE"
        )
        self.assertEqual([], delta.validate_state_transition(base, candidate))

    def test_state_transition_runtime_blocker_removal_requires_controller_maintenance(self):
        base = self._state()
        candidate = copy.deepcopy(base)
        candidate["blocked_by"] = []
        candidate["autonomous_controller"]["runtime_validation"] = (
            "REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE"
        )
        candidate["autonomous_controller"]["effective_config_observation"] = (
            "REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE"
        )
        issues = delta.validate_state_transition(base, candidate)
        self.assertIn(
            "STATE_BLOCKER_REMOVAL_UNPROVEN:AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION",
            issues,
        )

    def test_state_transition_rejects_launchable_with_blockers(self):
        base = self._state()
        candidate = copy.deepcopy(base)
        candidate["launchable"] = True
        self.assertIn("STATE_LAUNCHABLE_WITH_BLOCKERS", delta.validate_state_transition(base, candidate))

    def test_append_only_guard_rejects_rewrite(self):
        issues = delta._append_only_issues("old\n", "replacement\n", "journal.jsonl")
        self.assertEqual(["APPEND_ONLY_HISTORY_REWRITE:journal.jsonl"], issues)
        self.assertEqual([], delta._append_only_issues("old\n", "old\nnew\n", "journal.jsonl"))

    def test_claude_uses_progressive_changelog_disclosure(self):
        text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("Não carregue `CHANGELOG.md` integralmente", text)


if __name__ == "__main__":
    unittest.main()
