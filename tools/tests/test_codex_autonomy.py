from __future__ import annotations

import ast
import copy
import json
import os
import sys
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

    def test_cli_controller_narrows_client_owned_features(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        features = cfg["features"]
        for key in (
            "apps",
            "remote_plugin",
            "plugins",
            "enable_mcp_apps",
            "codex_apps_mcp_2026_07_28",
            "browser_use",
            "browser_use_external",
            "browser_use_full_cdp_access",
            "computer_use",
        ):
            self.assertIs(False, features[key], key)
        self.assertNotIn("connectors", features)


    @staticmethod
    def _wire_is_denial(payload):
        # Strict subset of the public Codex PreToolUse output contract.
        # Extra root keys (the former ser_controller metadata) invalidate a denial.
        if not isinstance(payload, dict) or set(payload) != {"hookSpecificOutput"}:
            return False
        nested = payload["hookSpecificOutput"]
        return (
            isinstance(nested, dict)
            and set(nested) == {"hookEventName", "permissionDecision", "permissionDecisionReason"}
            and nested["hookEventName"] == "PreToolUse"
            and nested["permissionDecision"] == "deny"
            and isinstance(nested["permissionDecisionReason"], str)
            and bool(nested["permissionDecisionReason"].strip())
        )

    def _invoke_guard_wire(self, script, raw, *, windows=False, cwd=None):
        if windows:
            command = ["powershell.exe", "-NoProfile", "-NonInteractive",
                       "-ExecutionPolicy", "Bypass", "-File", str(ROOT / script)]
        else:
            command = [sys.executable, "-I", "-B", str(ROOT / script)]
        return subprocess.run(
            command, input=raw, text=True, encoding="utf-8", capture_output=True,
            cwd=cwd or ROOT, timeout=20, check=False,
        )

    def _external_wire_cases(self, windows=False):
        script = ".codex/hooks/external_surface_guard." + ("ps1" if windows else "py")
        names = (
            "mcp__codex_app__get_usage_limits", "codex_appget_usage_limits",
            "codex_tuilist_threads", "cua_repljs", "mcp__example__write",
            "list_mcp_resources", "list_mcp_resource_templates", "read_mcp_resource",
            "web__run", "mcp__node_repl__", "MCP__NODE_REPL__js",
        )
        for name in names:
            with self.subTest(windows=windows, tool=name):
                proc = self._invoke_guard_wire(script, json.dumps({"tool_name": name}), windows=windows)
                self.assertEqual(0, proc.returncode, proc.stderr)
                self.assertTrue(self._wire_is_denial(json.loads(proc.stdout)), proc.stdout)
        for raw in ("not json", "null", "[]", "{}", '"text"', '{"tool_name":42}',
                    '{"tool_name":[]}', '{"tool_name":""}'):
            with self.subTest(windows=windows, invalid=raw):
                proc = self._invoke_guard_wire(script, raw, windows=windows)
                self.assertEqual(0, proc.returncode, proc.stderr)
                self.assertTrue(self._wire_is_denial(json.loads(proc.stdout)), proc.stdout)
        proc = self._invoke_guard_wire(script, '{"tool_name":"mcp__node_repl__js"}', windows=windows)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertEqual("", proc.stdout.strip())

    def test_external_guard_python_normal_stdin_emits_valid_wire(self):
        self._external_wire_cases()

    @unittest.skipUnless(os.name == "nt", "Windows PowerShell must be tested on the host")
    def test_external_guard_windows_normal_stdin_emits_valid_wire(self):
        # A missing powershell.exe on Windows is an error, not a skip or a PASS.
        self._external_wire_cases(windows=True)

    def test_wire_oracle_rejects_legacy_metadata_and_malformed_denials(self):
        good = {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                "permissionDecision": "deny", "permissionDecisionReason": "test"}}
        self.assertTrue(self._wire_is_denial(good))
        bad = copy.deepcopy(good)
        bad["ser_controller"] = {"policy": "legacy"}
        self.assertFalse(self._wire_is_denial(bad))
        for key in ("hookEventName", "permissionDecision", "permissionDecisionReason"):
            bad = copy.deepcopy(good)
            del bad["hookSpecificOutput"][key]
            self.assertFalse(self._wire_is_denial(bad))
        bad = copy.deepcopy(good)
        bad["hookSpecificOutput"]["permissionDecision"] = "allow"
        self.assertFalse(self._wire_is_denial(bad))

    def _scope_failure_wire_cases(self, windows=False):
        # Temporary directory is deliberately outside Git. No tool backend, repo
        # edit or network access is attempted; these are hook subprocesses only.
        with tempfile.TemporaryDirectory() as directory:
            for guard in ("pre_scope_guard", "post_scope_guard"):
                script = ".codex/hooks/" + guard + (".ps1" if windows else ".py")
                for raw in ("null", "[]", "not json", "{}",
                            '{"tool_name":"apply_patch","tool_input":{"path":"allowed/x.txt"}}'):
                    with self.subTest(windows=windows, guard=guard, raw=raw):
                        proc = self._invoke_guard_wire(script, raw, windows=windows, cwd=directory)
                        self.assertEqual(0, proc.returncode, proc.stderr)
                        value = json.loads(proc.stdout)
                        if guard == "pre_scope_guard":
                            self.assertTrue(self._wire_is_denial(value), proc.stdout)
                        else:
                            self.assertEqual({"decision", "reason"}, set(value))
                            self.assertEqual("block", value["decision"])
                            self.assertTrue(value["reason"])

    def test_scope_guards_python_failures_emit_blocking_wire(self):
        self._scope_failure_wire_cases()

    @unittest.skipUnless(os.name == "nt", "Windows PowerShell must be tested on the host")
    def test_scope_guards_windows_failures_emit_blocking_wire(self):
        self._scope_failure_wire_cases(windows=True)

    def test_executor_active_instructions_separate_operational_and_cq_transport(self):
        agent = val._read_toml(ROOT / ".codex/agents/executor.toml")
        instructions = agent["developer_instructions"]
        self.assertIn("a1_operational_git_transport.ps1", instructions)
        self.assertIn("a1_git_transport.ps1", instructions)
        self.assertIn("canonical", instructions)
        self.assertNotIn("host preflight v6", instructions)

    def test_cli_control_source_producer_and_operational_consumer_agree(self):
        def source_map(path, marker):
            text = (ROOT / path).read_text(encoding="utf-8")
            block = text.split(marker, 1)[1].split("\n}", 1)[0]
            return dict(re.findall(r'(?m)^\s+(\w+)\s*=\s*"([^"\n]+)"\s*$', block))
        producer = source_map("tools/codex_cli_cq_host_preflight.ps1", "$sourcePaths = [ordered]@{")
        consumer = source_map(".codex/transport/a1_operational_git_transport.ps1", "$ControlSourcePaths = [ordered]@{")
        self.assertEqual(producer, consumer)

    def test_generated_prompt_placeholders_have_preflight_producers(self):
        template = (ROOT / "docs/operations/CODEX_CLI_CQ_RUN_PROMPT_TEMPLATE.md").read_text(encoding="utf-8")
        preflight = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        required = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", template))
        produced = set(re.findall(r'\.Replace\("\{\{([A-Z0-9_]+)\}\}"', preflight))
        self.assertTrue(required)
        self.assertEqual(required, produced)

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
        self.assertNotIn("HOOK_JSON_DUPLICATE_SOURCE_FORBIDDEN", result["issues"])
        self.assertFalse((ROOT / ".codex/hooks.json").exists())

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
            self.assertIn("shell/Bash execution surface", text, role)
            self.assertIn("apply_patch/Edit/Write is forbidden", text, role)

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
        self.assertIn("shell/Bash execution surface", text)
        self.assertIn("apply_patch/Edit/Write is forbidden", text)

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
            "CQ3_SHELL_CONTROL",
            "shell/Bash execution surface",
            "WriteAllText",
        ):
            self.assertIn(token, text)


    def test_cli_cq3_rejects_instruction_refusal_as_enforcement_proof(self):
        text = (ROOT / "docs/operations/CODEX_RUNTIME_QUALIFICATION.md").read_text(encoding="utf-8")
        self.assertIn("Recusa por instrução não conta como PASS", " ".join(text.split()))
        self.assertIn("CQ3_EXECUTOR_PERMISSION_PROBES", text)
        self.assertIn("CQ3_A1_POSITIVE_PROBE", text)

    def test_desktop_profile_is_historical_and_cli_is_canonical(self):
        desktop = (ROOT / "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md").read_text(encoding="utf-8")
        cli = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("HISTORICAL_UNQUALIFIED", desktop)
        self.assertIn("CODEX_CLI_WINDOWS_CQ.md", desktop)
        self.assertIn("CODEX_CLI_WINDOWS_TUI", cli)
        result = val.validate(ROOT)
        self.assertTrue(result["cli_windows_cq_contract"])
        self.assertTrue(result["cli_host_preflight"])
        self.assertEqual("UNQUALIFIED", result["desktop_controller_runtime"])

    def test_cli_contract_names_host_preflight_artifact_explicitly(self):
        text = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("CQ_HOST_PREFLIGHT.json", text)
        self.assertIn("CQ_RUN_REQUEST.json", text)
        self.assertIn("CQ_RUN_PROMPT.md", text)
        self.assertIn("AC-R2-CLI-HOST-PREFLIGHT-1", text)

    def test_cli_host_preflight_uses_diagnostics_process_for_windows_exit_code(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("System.Diagnostics.ProcessStartInfo", text)
        self.assertIn("$process.Refresh()", text)
        self.assertIn("$exitCode = [int]$process.ExitCode", text)
        self.assertIn("ReadToEndAsync()", text)
        self.assertNotIn("Start-Process -FilePath $FilePath", text)
        self.assertNotIn("CQ_HOST_PREFLIGHT_CHILD_EXIT_NOT_OBSERVED", text)

    def test_cli_host_preflight_runs_validator_and_metatests_host_side(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("AC-R2-CLI-HOST-PREFLIGHT-1", text)
        self.assertIn("SER-CODEX-AUTONOMY-VALIDATION-21", text)
        self.assertIn("tools/validate_codex_autonomy.py", text)
        self.assertIn("tools.tests.test_codex_autonomy", text)
        self.assertIn("HOST_VALIDATOR = PASS", text)
        self.assertIn("HOST_METATESTS = PASS", text)
        self.assertIn('execution_surface="HOST_ONLY"', text)

    def test_cli_host_preflight_binds_raw_tcp_baseline_and_probe_source(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
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
        self.assertEqual(set(), val._powershell_parameter_assignment_collisions(text))
        self.assertIn("$hostSerializationSelfTestEvidence = $evidence.network_probe.serialization_selftest", text)


    def test_cli_host_preflight_requires_probe_serialization_selftest_before_network_baseline(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn('"powershell.exe"', text)
        self.assertIn('"-SelfTest"', text)
        self.assertIn("CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_INVALID_JSON", text)
        self.assertIn("CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_CONTRACT_FAIL", text)
        self.assertIn("NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS", text)
        self.assertLess(text.index("CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_CONTRACT_FAIL"), text.index("$networkProbeAddresses = @("))

    def test_cli_contract_requires_host_probe_serialization_selftest(self):
        text = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS", text)
        self.assertIn("HOST_NETWORK_BASELINE = PASS", text)
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


    def test_cli_host_preflight_emits_locale_independent_epoch(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("recorded_at_unix_seconds = $recordedAt.ToUnixTimeSeconds()", text)
        contract = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("recorded_at_unix_seconds", contract)
        self.assertIn("<= 1800", contract)

    def test_cli_contract_requires_observed_cli_version(self):
        text = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("CODEX_CLI_VERSION", text)
        self.assertIn("same CLI version recorded by preflight", text)

    def test_cli_contract_forbids_python_execution_in_sandbox(self):
        text = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("DO_NOT_EXECUTE_PYTHON_IN_SANDBOX"), 2)
        self.assertIn("HOST_VALIDATOR = PASS", text)
        self.assertIn("HOST_METATESTS = PASS", text)

    def test_cli_host_evidence_binds_critical_source_hashes(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for token in (
            "source_sha256",
            "validate_codex_autonomy.py",
            "test_codex_autonomy.py",
            "check_codex_autonomy_delta.py",
            "B1_AUTONOMY_ENVELOPE.json",
            "CODEX_CLI_TOOL_SURFACE_POLICY.json",
        ):
            self.assertIn(token, text)

    def test_cli_host_preflight_preserves_head_and_tree_after_host_validation(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("CQ_HOST_PREFLIGHT_GIT_IDENTITY_CHANGED_DURING_HOST_VALIDATION", text)
        self.assertIn("final_head=$finalHead", text)
        self.assertIn("final_tree=$finalTree", text)

    def test_cli_host_preflight_uses_safe_powershell_variable_boundaries(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn('CQ_HOST_PREFLIGHT_LOCAL_REMOTE_DIVERGENCE:$($head):$($originHead)', text)
        self.assertNotIn('CQ_HOST_PREFLIGHT_LOCAL_REMOTE_DIVERGENCE:$head:$originHead', text)

    def test_cli_host_preflight_does_not_persist_raw_remote_url(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("origin_identity=$ExpectedRepoFragment", text)
        self.assertNotIn("origin_url", text)

    def test_cli_host_preflight_is_fail_closed_without_installer(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("git fetch origin $ExpectedBranch", text)
        self.assertIn("CQ_HOST_PREFLIGHT_NO_QUALIFIED_CPYTHON312_WITH_JSONSCHEMA", text)
        self.assertIn("CQ_HOST_PREFLIGHT_CODEX_CLI_MISSING", text)
        self.assertIn("CQ_HOST_PREFLIGHT_CODEX_CLI_VERSION_FAILED", text)
        self.assertIn("CQ_HOST_PREFLIGHT_VALIDATOR_FAILED", text)
        self.assertIn("CQ_HOST_PREFLIGHT_METATESTS_FAILED", text)
        self.assertNotIn("pip install", text)
        self.assertNotIn("python -m pip", text)

    def test_cli_surface_is_explicitly_observable(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("CODEX_CLI = $codexCli", text)
        self.assertIn("CODEX_CLI_VERSION = $codexVersion", text)

    def test_cli_cq_defers_pr_metadata_to_external_adjudication(self):
        text = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("DEFERRED_TO_EXTERNAL_ADJUDICATION", text)

    def test_desktop_policy_is_historical_and_superseded(self):
        payload = json.loads(
            (ROOT / "docs/operations/autonomy/CODEX_DESKTOP_TOOL_SURFACE_POLICY.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual("UNQUALIFIED_AFTER_REPEATED_BACKEND_REACH", payload["controller_runtime_status"])
        self.assertEqual(
            "docs/operations/autonomy/CODEX_CLI_TOOL_SURFACE_POLICY.json",
            payload["superseded_by"],
        )
    def test_cli_windows_controller_contract_is_canonical(self):
        text = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn("CODEX_CLI_WINDOWS_TUI", text)
        self.assertIn("AC-R2-CLI-HOST-PREFLIGHT-1", text)
        self.assertIn("SER-CODEX-CLI-CQ-REQUEST-1", text)
        self.assertIn("FORBIDDEN_SURFACE_PROBE = NOT_APPLICABLE_ABSENT", text)
        self.assertIn("UNQUALIFIED_FOR_CONTROLLER", text)
        result = val.validate(ROOT)
        self.assertTrue(result["cli_windows_cq_contract"])
        self.assertTrue(result["cli_host_preflight"])
        self.assertEqual("UNQUALIFIED", result["desktop_controller_runtime"])

    def test_cli_runtime_is_bound_to_no_daemon_embedded_mode(self):
        preflight = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        contract = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        prompt = (ROOT / "docs/operations/CODEX_CLI_CQ_RUN_PROMPT_TEMPLATE.md").read_text(encoding="utf-8")
        start = (ROOT / "docs/operations/CODEX_AUTONOMOUS_START_PROMPT.md").read_text(encoding="utf-8")
        self.assertIn('runtime_mode="EMBEDDED_NO_DAEMON"', preflight)
        self.assertIn('required_launch_args=@("--no-daemon","--strict-config")', preflight)
        self.assertIn("strict_config=$true", preflight)
        self.assertIn("EMBEDDED_NO_DAEMON", contract)
        self.assertIn("--no-daemon", contract)
        self.assertIn("EMBEDDED_NO_DAEMON", prompt)
        self.assertIn("--no-daemon", prompt)
        self.assertIn('& "$env:APPDATA\\npm\\codex.cmd" --no-daemon --strict-config', start)

    def test_cli_preflight_binds_explicit_launcher_version_and_control_sources(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for token in (
            'Join-Path $env:APPDATA "npm\\codex.cmd"',
            "CODEX_CLI_VERSION =",
            "AC-R2-CLI-HOST-PREFLIGHT-1",
            "SER-CODEX-CLI-CQ-REQUEST-1",
            'cli_contract = "docs\\operations\\CODEX_CLI_WINDOWS_CQ.md"',
            'cli_preflight = "tools\\codex_cli_cq_host_preflight.ps1"',
            "SER-CODEX-AUTONOMY-VALIDATION-21",
        ):
            self.assertIn(token, text)
        self.assertNotIn("CODEX_DESKTOP_WINDOWS", text)

    def test_cli_tool_policy_blocks_desktop_surfaces_and_allows_absent_probe(self):
        payload = json.loads(
            (ROOT / "docs/operations/autonomy/CODEX_CLI_TOOL_SURFACE_POLICY.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual("SER-CODEX-CLI-TOOL-SURFACE-1", payload["schema_version"])
        self.assertEqual("CODEX_CLI_WINDOWS_TUI", payload["canonical_runtime"])
        self.assertTrue(payload["cq_rules"]["desktop_client_surface_presence_blocks"])
        self.assertTrue(payload["cq_rules"]["no_probe_is_valid_when_no_probeable_forbidden_surface_is_loaded"])
        self.assertEqual(0, payload["cq_rules"]["probe_retry_count"])
        self.assertIn("codex_tui.*", payload["enforcement"]["matcher"])

    def test_desktop_preflight_is_explicitly_retired(self):
        text = (ROOT / "tools/codex_desktop_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("CODEX_DESKTOP_RUNTIME_UNQUALIFIED_USE_TOOLS_CODEX_CLI_CQ_HOST_PREFLIGHT_PS1", text)
        policy = json.loads(
            (ROOT / "docs/operations/autonomy/CODEX_DESKTOP_TOOL_SURFACE_POLICY.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual("UNQUALIFIED_AFTER_REPEATED_BACKEND_REACH", policy["controller_runtime_status"])

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

    def test_a0_windows_scratch_uses_cli_portable_home_relative_syntax(self):
        self.assertEqual("~/codex-scratch/Ambiente_Databricks", val.A0_WINDOWS_SCRATCH)
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        a0 = cfg["permissions"]["ser-controller-a0"]
        self.assertIn(val.A0_WINDOWS_SCRATCH, a0["workspace_roots"])
        self.assertIn(val.A0_WINDOWS_SCRATCH, a0["filesystem"])
        self.assertFalse(any(path.startswith("~\\") for path in a0["workspace_roots"]))
        self.assertFalse(any(path.startswith("~\\") for path in a0["filesystem"]))

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
        self.assertNotIn('"powershell.exe -NoProfile', rule)
        self.assertIn('match = [', rule)
        self.assertIn('not_match = [', rule)
        self.assertIn("A1_GIT_TRANSPORT_LINKED_WORKTREE_UNSUPPORTED", script)
        self.assertIn("A1_GIT_TRANSPORT_HOST_EVIDENCE_CHECKOUT_MODE", script)

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

    def test_parameter_collision_guard_rejects_historical_selftest_bug(self):
        bad = (
            "param(\n"
            "    [switch]$SelfTest\n"
            ")\n"
            "Set-StrictMode -Version Latest\n"
            "$selfTest = $evidence.network_probe.serialization_selftest\n"
        )
        self.assertEqual({"selftest"}, val._powershell_parameter_assignment_collisions(bad))

    def test_parameter_collision_guard_accepts_renamed_runtime_variable(self):
        good = (
            "param(\n"
            "    [switch]$SelfTest\n"
            ")\n"
            "Set-StrictMode -Version Latest\n"
            "$hostSerializationSelfTestEvidence = $evidence.network_probe.serialization_selftest\n"
        )
        self.assertEqual(set(), val._powershell_parameter_assignment_collisions(good))

    def test_permission_profile_rejects_a0_extra_filesystem_write(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        cfg["permissions"]["ser-controller-a0"]["filesystem"]["C:/unexpected"] = "write"
        self.assertIn(
            "A0_FILESYSTEM_KEYS_MISMATCH",
            val._validate_permission_profile(cfg, self.envelope()),
        )

    def test_permission_profile_rejects_a0_extra_workspace_write(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        cfg["permissions"]["ser-controller-a0"]["filesystem"][":workspace_roots"]["README.md"] = "write"
        self.assertIn(
            "A0_WORKSPACE_ROOT_MAP_MISMATCH",
            val._validate_permission_profile(cfg, self.envelope()),
        )

    def test_permission_profile_rejects_a1_extra_filesystem_write(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        cfg["permissions"]["ser-b1-a1"]["filesystem"]["C:/unexpected"] = "write"
        self.assertIn(
            "A1_FILESYSTEM_KEYS_MISMATCH",
            val._validate_permission_profile(cfg, self.envelope()),
        )

    def test_permission_profile_rejects_a1_extra_workspace_entry(self):
        cfg = copy.deepcopy(val._read_toml(ROOT / ".codex/config.toml"))
        cfg["permissions"]["ser-b1-a1"]["filesystem"][":workspace_roots"]["README.md"] = "read"
        self.assertIn(
            "A1_WORKSPACE_ROOT_MAP_MISMATCH",
            val._validate_permission_profile(cfg, self.envelope()),
        )

    def test_validator_git_mode_is_executable(self):
        self.assertEqual("100755", val._git_index_mode(ROOT, "tools/validate_codex_autonomy.py"))


    def test_cli_tool_surface_policy_is_canonical_and_fail_closed(self):
        payload = json.loads(
            (ROOT / "docs/operations/autonomy/CODEX_CLI_TOOL_SURFACE_POLICY.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual("SER-CODEX-CLI-TOOL-SURFACE-1", payload["schema_version"])
        self.assertEqual("CODEX_CLI_WINDOWS_TUI", payload["canonical_runtime"])
        self.assertEqual(val.EXTERNAL_SURFACE_MATCHER, payload["enforcement"]["matcher"])
        self.assertEqual(
            "DENY_EXTERNAL_SURFACES_ALLOW_INTERNAL_NODE_REPL",
            payload["enforcement"]["policy"],
        )
        self.assertTrue(payload["cq_rules"]["desktop_client_surface_presence_blocks"])
        self.assertTrue(payload["cq_rules"]["no_probe_is_valid_when_no_probeable_forbidden_surface_is_loaded"])
        self.assertEqual(0, payload["cq_rules"]["probe_retry_count"])
    def test_hooks_include_fail_closed_mcp_guard(self):
        hooks = val._read_toml(ROOT / ".codex/config.toml")["hooks"]
        serialized = json.dumps(hooks)
        self.assertIn(val.EXTERNAL_SURFACE_MATCHER, serialized)
        self.assertIn("external_surface_guard", serialized)
        self.assertIn("list_mcp_resources", serialized)
        self.assertIn("web__run", serialized)

    def test_external_surface_matcher_covers_dynamic_client_hook_names(self):
        hooks = val._read_toml(ROOT / ".codex/config.toml")["hooks"]
        external_groups = [
            group
            for group in hooks["PreToolUse"]
            if "external_surface_guard" in json.dumps(group)
        ]
        self.assertEqual(1, len(external_groups))
        matcher = external_groups[0]["matcher"]
        self.assertEqual(val.EXTERNAL_SURFACE_MATCHER, matcher)
        for sample in (
            "mcp__codex_app__get_usage_limits",
            "codex_appget_usage_limits",
            "codex_app__get_usage_limits",
            "mcp__cua_repl.js",
            "cua_repljs",
            "codex_tuilist_threads",
        ):
            self.assertIsNotNone(re.fullmatch(matcher, sample), sample)

        ps = (ROOT / ".codex/hooks/external_surface_guard.ps1").read_text(encoding="utf-8")
        py = (ROOT / ".codex/hooks/external_surface_guard.py").read_text(encoding="utf-8")
        for token in ("codex_app", "cua_repl", "codex_tui", "codex_appget_usage_limits"):
            self.assertIn(token, ps)
            self.assertIn(token, py)

    def test_windows_scope_guards_have_host_selftests_and_fail_closed_inspection(self):
        pre = (ROOT / ".codex/hooks/pre_scope_guard.ps1").read_text(encoding="utf-8")
        post = (ROOT / ".codex/hooks/post_scope_guard.ps1").read_text(encoding="utf-8")
        self.assertIn("[switch]$SelfTest", pre)
        self.assertIn("[switch]$SelfTest", post)
        self.assertIn("could not resolve target path", pre)
        for token in (
            "A1 post-scope guard git diff failed",
            "A1 post-scope guard git cached diff failed",
            "A1 post-scope guard git untracked inspection failed",
        ):
            self.assertIn(token, post)
        self.assertNotIn('TrimStart("./")', pre)
        self.assertNotIn('TrimStart("./")', post)

    def test_python_scope_guards_use_precise_normalization_and_fail_closed_git(self):
        pre = (ROOT / ".codex/hooks/pre_scope_guard.py").read_text(encoding="utf-8")
        post = (ROOT / ".codex/hooks/post_scope_guard.py").read_text(encoding="utf-8")
        self.assertIn('while value.startswith("./")', pre)
        self.assertIn('while value.startswith("./")', post)
        self.assertNotIn('.lstrip("./")', pre)
        self.assertNotIn('.lstrip("./")', post)
        self.assertIn("git inspection failed", post)

    def test_transport_binds_host_python_push_url_remote_readback_and_cq_journal_only(self):
        text = (ROOT / ".codex/transport/a1_git_transport.ps1").read_text(encoding="utf-8")
        for token in (
            "evidence.python.executable",
            "git remote get-url --push origin",
            "CQ_JOURNAL_ONLY",
            "git ls-remote origin",
            "A1_GIT_TRANSPORT_REMOTE_ADVANCED",
            "A1_GIT_TRANSPORT_CQ_JOURNAL_NOT_EXCLUSIVE",
            "A1_GIT_TRANSPORT_REMOTE_READBACK_FAIL",
        ):
            self.assertIn(token, text)
        self.assertIsNone(re.search(r"(?m)^\s*&\s+python(?:\.exe)?\s", text))

    def test_qualification_transport_requires_cli_host_evidence(self):
        text = (ROOT / ".codex/transport/a1_git_transport.ps1").read_text(encoding="utf-8")
        self.assertIn("AC-R2-CLI-HOST-PREFLIGHT-1", text)
        self.assertNotIn("AC-R2-DESKTOP-HOST-PREFLIGHT-6", text)

    def test_transport_selftest_is_non_mutating_contract_surface(self):
        text = (ROOT / ".codex/transport/a1_git_transport.ps1").read_text(encoding="utf-8")
        self.assertIn("[switch]$SelfTest", text)
        self.assertIn("SER-A1-GIT-TRANSPORT-SELFTEST-1", text)
        self.assertLess(
            text.index("if ($SelfTest)"),
            text.index("A1_GIT_TRANSPORT_HOST_EVIDENCE_MISSING"),
        )

    def test_network_probe_offline_runtime_selftest_uses_powershell_ast(self):
        text = (ROOT / ".codex/probes/cq3_executor_network_probe.ps1").read_text(encoding="utf-8")
        for token in (
            "[switch]$OfflineRuntimeSelfTest",
            "AssignmentStatementAst",
            "CQ3_NETWORK_PROBE_PARAMETER_ASSIGNMENT_COLLISION",
            "AC-R2-CQ3-NETWORK-PROBE-OFFLINE-RUNTIME-SELFTEST-1",
            "parameter_assignment_collisions = 0",
            "network_attempt_count = 0",
        ):
            self.assertIn(token, text)


    def test_cli_preflight_v1_generates_machine_handoff_and_runs_contract_selftests(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for token in (
            "AC-R2-CLI-HOST-PREFLIGHT-1",
            "SER-CODEX-CLI-CQ-REQUEST-1",
            "CODEX_CLI_WINDOWS_TUI",
            "CODEX_CLI_VERSION =",
            "CQ_RUN_REQUEST.json",
            "CQ_RUN_PROMPT.md",
            "NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST = PASS",
            "MCP_GUARD_SELFTEST = PASS",
            "SCOPE_GUARDS_SELFTEST = PASS",
            "A1_GIT_TRANSPORT_SELFTEST = PASS",
            "A1_OPERATIONAL_TRANSPORT_SELFTEST = PASS",
            "CQ_READY_TO_RUN",
            "HOOK_TRUST_REVIEW_REQUIRED",
            "PROJECT_HOOKS_SHA256",
            "CQ_HOST_PREFLIGHT_RUN_REQUEST_ROUNDTRIP_MISMATCH",
            "CQ_HOST_PREFLIGHT_PROMPT_TEMPLATE_UNRESOLVED",
            "CQ_HOST_PREFLIGHT_LINKED_WORKTREE_UNSUPPORTED",
            "CHECKOUT_MODE = STANDALONE",
        ):
            self.assertIn(token, text)
    def test_runtime_contract_keeps_final_state_outside_repo_after_cq4(self):
        text = (ROOT / "docs/operations/CODEX_RUNTIME_QUALIFICATION.md").read_text(encoding="utf-8")
        self.assertIn("não realizar nova escrita repo-side depois de CQ4", text)
        self.assertIn("pacote externo de evidências", text)

    def test_start_prompt_uses_machine_generated_handoff(self):
        text = (ROOT / "docs/operations/CODEX_AUTONOMOUS_START_PROMPT.md").read_text(encoding="utf-8")
        self.assertIn("CQ_RUN_REQUEST.json", text)
        self.assertIn("CQ_RUN_PROMPT.md", text)
        self.assertIn("HOOK_TRUST_REVIEW_REQUIRED", text)
        self.assertIn("PROJECT_HOOK_TRUST", text)
        self.assertIn("/hooks", text)
        self.assertNotIn("Settings > Hooks", text)
        self.assertIn("standalone checkout", text)


    def test_readiness_contract_requires_human_hook_trust_before_cli_cq(self):
        start = (ROOT / "docs/operations/CODEX_AUTONOMOUS_START_PROMPT.md").read_text(encoding="utf-8")
        cli = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        preflight = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for text in (start, cli, preflight):
            self.assertIn("CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST", text)
        self.assertNotIn("CQ_READY_TO_RUN = PASS", start)
        self.assertNotIn("CQ_READY_TO_RUN = PASS", cli)
        self.assertIn("standalone checkout", cli)
    def test_protocol_stabilization_is_v6_surface_policy_and_external_result_consistent(self):
        text = (ROOT / "docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("CLI host preflight v1", text)
        self.assertIn("CODEX_CLI_TOOL_SURFACE_POLICY.json", text)
        self.assertIn("UNQUALIFIED_FOR_CONTROLLER", text)
        self.assertIn("external_surface_guard", text)
        self.assertIn("Depois de CQ4 não há segunda escrita repo-side", text)
        self.assertIn("standalone checkout", text)

    def test_validator_v20_enforces_start_protocol_and_inline_hooks_consistency(self):
        text = (ROOT / "tools/validate_codex_autonomy.py").read_text(encoding="utf-8")
        self.assertIn("SER-CODEX-AUTONOMY-VALIDATION-21", text)
        self.assertIn("HOOK_JSON_DUPLICATE_SOURCE_FORBIDDEN", text)
        self.assertIn("CODEX_AUTONOMOUS_START_PROMPT_PREMATURE_READY_PASS", text)
        self.assertIn("CODEX_AUTONOMOUS_PROTOCOL_STABILIZATION_DRIFT", text)
        self.assertIn("DESKTOP_WINDOWS_CQ_NOT_MARKED_HISTORICAL", text)

    def test_operational_policy_separates_cq_from_multi_commit_operation(self):
        payload = json.loads(
            (ROOT / "docs/operations/autonomy/A1_OPERATIONAL_POLICY.json").read_text(encoding="utf-8")
        )
        self.assertEqual("SER-CODEX-A1-OPERATIONAL-2", payload["schema_version"])
        self.assertIn("single-shot", payload["invariants"]["qualification_transport"])
        self.assertEqual(0, payload["recovery"]["same_state_same_command_retries"])
        self.assertIn("unresolved UNKNOWN effect", payload["human_gates"])

    def test_operational_transport_uses_external_checkpoint_not_journal_authority(self):
        text = (ROOT / ".codex/transport/a1_operational_git_transport.ps1").read_text(encoding="utf-8")
        for token in (
            "SER-A1-OPERATIONAL-CHECKPOINT-2",
            "SER-A1-OPERATIONAL-TRANSPORT-SELFTEST-2",
            "InitializeCheckpoint",
            "ReconcileOnly",
            "A1_OPERATIONAL_RECONCILE=PUBLISHED_SUCCESSOR",
            "A1_OPERATIONAL_RECONCILE=RESUMED_PUSH",
            "A1_OPERATIONAL_UNKNOWN_DIVERGENCE",
            "A1_OPERATIONAL_PUSH_FAILED_LOCAL_COMMIT_PRESERVED",
            "A1_OPERATIONAL_PUSH_READBACK_UNKNOWN_LOCAL_COMMIT_PRESERVED",
        ):
            self.assertIn(token, text)
        self.assertNotIn("lastJournal", text)
        self.assertNotIn("CQ3_A1_POSITIVE_PROBE", text)

    def test_operational_transport_allows_checkpoint_successor_instead_of_preflight_head_only(self):
        text = (ROOT / ".codex/transport/a1_operational_git_transport.ps1").read_text(encoding="utf-8")
        self.assertIn("$checkpointHead=[string]$cp.last_published_head", text)
        self.assertIn("--base $checkpointHead --head $newHead", text)
        self.assertNotIn("A1_GIT_TRANSPORT_BASE_NOT_PREFLIGHT_HEAD", text)

    def test_operational_transport_preserves_local_commit_on_publish_failure(self):
        text = (ROOT / ".codex/transport/a1_operational_git_transport.ps1").read_text(encoding="utf-8")
        self.assertIn("PUSH_FAILED_LOCAL_COMMIT_PRESERVED", text)
        self.assertIn("PUSH_READBACK_UNKNOWN_LOCAL_COMMIT_PRESERVED", text)
        self.assertIn("LOCAL_SUCCESSOR_PENDING_PUSH", text)
        self.assertIn("A1_OPERATIONAL_RECONCILE_LOCAL_DELTA_INVALID", text)
        self.assertIn("A1_OPERATIONAL_UNKNOWN_DIVERGENCE", text)

    def test_operational_transport_is_non_force_and_validates_push_remote(self):
        text = (ROOT / ".codex/transport/a1_operational_git_transport.ps1").read_text(encoding="utf-8")
        self.assertIn("git remote get-url --push origin", text)
        self.assertIn("git ls-remote origin", text)
        self.assertNotIn("--force", text)
        self.assertIn("A1_OPERATIONAL_LINKED_WORKTREE_UNSUPPORTED", text)
        self.assertIn("A1_OPERATIONAL_HOST_EVIDENCE_CHECKOUT_MODE", text)

    def test_operational_autonomy_does_not_expand_envelope_schema_or_write_roots(self):
        envelope = self.envelope()
        self.assertNotIn("operational_autonomy", envelope)
        self.assertEqual("SER-AUTONOMY-ENVELOPE-2", envelope["schema_version"])
        self.assertEqual(10, len(envelope["repo_scope"]["write_roots"]))
        self.assertFalse(envelope["authority_classes"]["A2"]["autonomous"])

    def test_protocol_routes_recoverable_a1_failures_to_repairing(self):
        text = (ROOT / "docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("Falha recuperável não é Human Gate", text)
        self.assertIn("RECOVERABLE_A1", text)
        self.assertIn("PRECONDITION", text)
        self.assertIn("UNKNOWN_EFFECT", text)
        self.assertIn("AUTHORITY_BOUNDARY", text)
        self.assertIn("Qualificação versus transporte operacional", text)

    def test_operational_transport_rule_is_separate_and_prompt_reviewed(self):
        text = (ROOT / ".codex/rules/a1_git_transport.rules").read_text(encoding="utf-8")
        self.assertIn("a1_git_transport.ps1", text)
        self.assertIn("a1_operational_git_transport.ps1", text)
        self.assertGreaterEqual(text.count('decision = "prompt"'), 2)

    def test_validator_source_is_python_syntax_valid(self):
        text = (ROOT / "tools/validate_codex_autonomy.py").read_text(encoding="utf-8")
        ast.parse(text)

    def test_operational_transport_has_no_powershell_parameter_assignment_collision(self):
        text = (ROOT / ".codex/transport/a1_operational_git_transport.ps1").read_text(encoding="utf-8")
        self.assertEqual(set(), val._powershell_parameter_assignment_collisions(text))

    def test_operational_transport_selftest_does_not_require_host_evidence(self):
        text = (ROOT / ".codex/transport/a1_operational_git_transport.ps1").read_text(encoding="utf-8")
        self.assertLess(text.index("if($SelfTest)"), text.index("$evidence=Load-Evidence"))
        self.assertIn("A1_OPERATIONAL_SELFTEST_RECONCILIATION_MATRIX", text)

    def test_operational_bootstrap_requires_canonical_pass_and_runtime_blocker_removal(self):
        text = (ROOT / ".codex/transport/a1_operational_git_transport.ps1").read_text(encoding="utf-8")
        for token in (
            "A1_OPERATIONAL_RUNTIME_NOT_CANONICAL_PASS",
            "A1_OPERATIONAL_EFFECTIVE_CONFIG_NOT_CANONICAL_PASS",
            "A1_OPERATIONAL_RUNTIME_BLOCKER_STILL_PRESENT",
            "A1_OPERATIONAL_QUALIFIED_HEAD_NOT_ANCESTOR",
            "A1_OPERATIONAL_BOOTSTRAP_UNEXPECTED_PATH",
        ):
            self.assertIn(token, text)


    def test_operational_transport_binds_all_control_sources_to_host_evidence(self):
        text = (ROOT / ".codex/transport/a1_operational_git_transport.ps1").read_text(encoding="utf-8")
        for token in (
            "Require-ControlIdentity",
            "A1_OPERATIONAL_CONTROL_HASH_MISSING",
            "A1_OPERATIONAL_CONTROL_IDENTITY_DRIFT",
            'rules = ".codex\\rules\\a1_git_transport.rules"',
            'executor_agent = ".codex\\agents\\executor.toml"',
            'protocol = "docs\\operations\\CODEX_AUTONOMOUS_PROTOCOL.md"',
            'runtime_contract = "docs\\operations\\CODEX_RUNTIME_QUALIFICATION.md"',
            'cli_contract = "docs\\operations\\CODEX_CLI_WINDOWS_CQ.md"',
            'cli_preflight = "tools\\codex_cli_cq_host_preflight.ps1"',
            'tool_surface_policy = "docs\\operations\\autonomy\\CODEX_CLI_TOOL_SURFACE_POLICY.json"',
            'prompt_template = "docs\\operations\\CODEX_CLI_CQ_RUN_PROMPT_TEMPLATE.md"',
            'start_prompt = "docs\\operations\\CODEX_AUTONOMOUS_START_PROMPT.md"',
            'envelope_schema = "docs\\operations\\autonomy\\autonomy-envelope.schema.json"',
            'agents_md = "AGENTS.md"',
            'controller_skill = ".agents\\skills\\ser-autonomous-controller\\SKILL.md"',
            'explorer_agent = ".codex\\agents\\explorer.toml"',
            'domain_auditor_agent = ".codex\\agents\\domain-auditor.toml"',
            'evidence_auditor_agent = ".codex\\agents\\evidence-auditor.toml"',
            'architecture_auditor_agent = ".codex\\agents\\architecture-auditor.toml"',
        ):
            self.assertIn(token, text)

    def test_cli_preflight_hashes_operational_control_identity(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for token in (
            'operational_transport = ".codex\\transport\\a1_operational_git_transport.ps1"',
            'operational_policy = "docs\\operations\\autonomy\\A1_OPERATIONAL_POLICY.json"',
            'rules = ".codex\\rules\\a1_git_transport.rules"',
            'executor_agent = ".codex\\agents\\executor.toml"',
            'protocol = "docs\\operations\\CODEX_AUTONOMOUS_PROTOCOL.md"',
            'runtime_contract = "docs\\operations\\CODEX_RUNTIME_QUALIFICATION.md"',
            'cli_contract = "docs\\operations\\CODEX_CLI_WINDOWS_CQ.md"',
            'cli_preflight = "tools\\codex_cli_cq_host_preflight.ps1"',
            "A1_OPERATIONAL_TRANSPORT_SELFTEST = PASS",
        ):
            self.assertIn(token, text)
    def test_operational_policy_checkpoint_is_progress_not_authority(self):
        payload = json.loads(
            (ROOT / "docs/operations/autonomy/A1_OPERATIONAL_POLICY.json").read_text(encoding="utf-8")
        )
        self.assertEqual("progress tracking only; not an authority source", payload["checkpoints"]["role"])
        self.assertTrue(payload["bootstrap"]["qualified_head_must_be_ancestor"])
        self.assertTrue(payload["bootstrap"]["current_local_must_equal_remote"])
        self.assertTrue(payload["bootstrap"]["worktree_must_be_clean"])
        self.assertEqual(4, len(payload["bootstrap"]["allowed_bridge_paths"]))

    def test_operational_policy_is_separate_from_authority_envelope(self):
        envelope = self.envelope()
        policy = json.loads(
            (ROOT / "docs/operations/autonomy/A1_OPERATIONAL_POLICY.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("operational_autonomy", envelope)
        self.assertEqual("SER-CODEX-A1-OPERATIONAL-2", policy["schema_version"])
        self.assertEqual(4, len(policy["bootstrap"]["allowed_bridge_paths"]))
        self.assertIn("qualified control identity", policy["invariants"]["control_identity"].lower())

    def test_two_successive_allowed_commits_validate_independently(self):
        repo, root_patch, envelope_patch = self._temporary_git_repo()
        with root_patch, envelope_patch:
            (repo / "allowed").mkdir()
            (repo / "allowed/x.txt").write_text("0", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            base = self._git(repo, "rev-parse", "HEAD")

            (repo / "allowed/x.txt").write_text("1", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "step1")
            head1 = self._git(repo, "rev-parse", "HEAD")
            self.assertEqual("PASS", delta.check_delta(base, head1)["status"])

            (repo / "allowed/x.txt").write_text("2", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "step2")
            head2 = self._git(repo, "rev-parse", "HEAD")
            self.assertEqual("PASS", delta.check_delta(head1, head2)["status"])

    def test_windows_hook_commands_use_direct_file_execution(self):
        hooks = val._read_toml(ROOT / ".codex/config.toml")["hooks"]
        commands = []
        for event in ("PreToolUse", "PostToolUse"):
            for group in hooks[event]:
                for hook in group.get("hooks", []):
                    command = hook.get("command_windows", hook.get("commandWindows", ""))
                    if ".codex\\hooks\\" in command:
                        commands.append(command)
        self.assertEqual(3, len(commands))
        self.assertTrue(all(" -File .codex\\hooks\\" in command for command in commands))
        self.assertTrue(all(" -Command " not in command for command in commands))

    def test_scope_guards_explicitly_exit_zero_after_normal_success(self):
        pre = (ROOT / ".codex/hooks/pre_scope_guard.ps1").read_text(encoding="utf-8")
        post = (ROOT / ".codex/hooks/post_scope_guard.ps1").read_text(encoding="utf-8")
        self.assertIn('if ($violations.Count -gt 0) { Deny', pre)
        self.assertIn('exit 0\n}\ncatch {', pre)
        self.assertIn('if($violations.Count -gt 0){ Block', post)
        self.assertIn('exit 0\n}\ncatch {', post)

    def test_cli_preflight_treats_empty_hook_stdout_as_empty_string_on_windows_powershell(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        self.assertIn("$preWireText = [string](Get-Content", text)
        self.assertIn("$postWireText = [string](Get-Content", text)
        self.assertIn("$nodeWireText = [string](Get-Content", text)
        self.assertIn("[string]::IsNullOrWhiteSpace($preWireText)", text)
        self.assertNotIn("(Get-Content -LiteralPath $preWireOut -Raw -Encoding UTF8).Trim()", text)
        self.assertNotIn("(Get-Content -LiteralPath $postWireOut -Raw -Encoding UTF8).Trim()", text)
        self.assertNotIn("(Get-Content -LiteralPath $nodeWireOut -Raw -Encoding UTF8).Trim()", text)

    def test_cli_preflight_wire_payload_matches_upstream_required_shape(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for token in ("New-HookWireInput", "session_id", "turn_id", "transcript_path", "cwd", "hook_event_name", "model", "permission_mode", "tool_name", "tool_input", "tool_use_id", "tool_response"):
            self.assertIn(token, text)

    def test_cli_preflight_runs_normal_hook_wire_probes(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for token in (
            "Invoke-CapturedProcessWithInput",
            "CQ_HOST_PREFLIGHT_PRE_SCOPE_NORMAL_WIRE_EXIT",
            "CQ_HOST_PREFLIGHT_POST_SCOPE_NORMAL_WIRE_EXIT",
            "CQ_HOST_PREFLIGHT_EXTERNAL_NORMAL_WIRE_CONTRACT",
            "CQ_HOST_PREFLIGHT_NODE_REPL_NORMAL_WIRE_EXIT",
            "HOOK_WIRE_RUNTIME_SELFTEST = PASS",
        ):
            self.assertIn(token, text)

    def test_legacy_connectors_alias_is_absent(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        self.assertNotIn("connectors", cfg["features"])
        self.assertIs(False, cfg["features"]["apps"])

    def test_cq3_negative_filesystem_probes_bypass_pre_scope_hook(self):
        cfg = val._read_toml(ROOT / ".codex/config.toml")
        pre = cfg["hooks"]["PreToolUse"]
        groups = [group for group in pre if "pre_scope_guard" in json.dumps(group.get("hooks", []))]
        self.assertEqual(1, len(groups))
        self.assertEqual("apply_patch|Edit|Write", groups[0]["matcher"])
        self.assertIsNone(re.fullmatch(groups[0]["matcher"], "Bash"))
        runtime = (ROOT / "docs/operations/CODEX_RUNTIME_QUALIFICATION.md").read_text(encoding="utf-8")
        self.assertIn("CQ3_SHELL_CONTROL", runtime)
        self.assertIn("WriteAllText", runtime)

    def test_cli_runtime_requires_strict_config_and_no_daemon(self):
        preflight = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        contract = (ROOT / "docs/operations/CODEX_CLI_WINDOWS_CQ.md").read_text(encoding="utf-8")
        self.assertIn('required_launch_args=@("--no-daemon","--strict-config")', preflight)
        self.assertIn("strict_config=$true", preflight)
        self.assertIn("--no-daemon --strict-config", contract)

    def test_host_preflight_execpolicy_oracles_cover_exact_and_negative_forms(self):
        text = (ROOT / "tools/codex_cli_cq_host_preflight.ps1").read_text(encoding="utf-8")
        for token in (
            "Invoke-ExecPolicyOracle",
            'ExpectedDecision "prompt"',
            'ExpectedDecision ""',
            "CQ_HOST_PREFLIGHT_EXECPOLICY_NEGATIVE_MATCHED",
            "EXECPOLICY_HOST_SELFTEST = PASS",
        ):
            self.assertIn(token, text)

    def test_runtime_sidecars_are_null_safe(self):
        for path in (
            ".codex/probes/cq3_executor_network_probe.ps1",
            ".codex/transport/a1_git_transport.ps1",
            ".codex/transport/a1_operational_git_transport.ps1",
        ):
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertNotIn("(Get-Content -LiteralPath $SidecarPath -Raw).Trim()", text)
            self.assertNotIn("(Get-Content -LiteralPath $EvidenceSidecarPath -Raw).Trim()", text)
            self.assertNotIn("(Get-Content -LiteralPath $CheckpointSidecarPath -Raw).Trim()", text)
            self.assertIn("IsNullOrWhiteSpace", text)

    def test_external_surface_hook_windows_path_is_normalized(self):
        hooks = val._read_toml(ROOT / ".codex/config.toml")["hooks"]
        commands = [
            hook.get("command_windows", hook.get("commandWindows", ""))
            for group in hooks["PreToolUse"]
            for hook in group.get("hooks", [])
            if "external_surface_guard" in hook.get("command_windows", hook.get("commandWindows", ""))
        ]
        self.assertEqual(1, len(commands))
        self.assertIn(".codex\\hooks\\external_surface_guard.ps1", commands[0])
        self.assertNotIn(".codex\\\\hooks\\\\external_surface_guard.ps1", commands[0])

    def test_validator_uses_current_external_surface_contract_name(self):
        text = (ROOT / "tools/validate_codex_autonomy.py").read_text(encoding="utf-8")
        self.assertIn("HOOK_EXTERNAL_SURFACE_MATCHER_MISMATCH", text)
        self.assertNotIn("MCP_PRETOOL_GUARD", text)

    def test_claude_uses_progressive_changelog_disclosure(self):
        text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("Não carregue `CHANGELOG.md` integralmente", text)


if __name__ == "__main__":
    unittest.main()
