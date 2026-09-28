#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tomllib
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parents[1]
A0_PROFILE = "ser-controller-a0"
A1_PROFILE = "ser-b1-a1"
A0_WINDOWS_SCRATCH = "~/codex-scratch/Ambiente_Databricks"
LEGACY_WINDOWS_QUALIFIED_PYTHON_ROOT = r"~\AppData\Local\Programs\Python\Python312"
EXTERNAL_SURFACE_MATCHER = r"^(mcp__.*|codex_app.*|cua_repl.*|codex_tui.*|list_mcp_resources|list_mcp_resource_templates|read_mcp_resource|web__run)$"
EXPECTED_AGENTS = {
    "explorer": ("explorer.toml", A0_PROFILE, "gpt-6-luna", "high"),
    "executor": ("executor.toml", A1_PROFILE, "gpt-6-sol", "medium"),
    "domain-auditor": ("domain-auditor.toml", A0_PROFILE, "gpt-6-astra", "high"),
    "evidence-auditor": ("evidence-auditor.toml", A0_PROFILE, "gpt-6-astra", "high"),
    "architecture-auditor": ("architecture-auditor.toml", A0_PROFILE, "gpt-6-astra", "high"),
}


def _read_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_write_root(path: str) -> str:
    value = path.replace("\\", "/").rstrip("/")
    if value.endswith("/**"):
        value = value[:-3].rstrip("/")
    return value


def _powershell_parameter_assignment_collisions(text: str) -> set[str]:
    param_match = re.search(r"(?is)^\s*param\s*\((.*?)\)\s*Set-StrictMode", text)
    if not param_match:
        return set()
    parameters = {
        name.lower()
        for name in re.findall(r"\$([A-Za-z_][A-Za-z0-9_]*)", param_match.group(1))
    }
    assignments = {
        name.lower()
        for name in re.findall(r"(?mi)^\s*\$([A-Za-z_][A-Za-z0-9_]*)\s*=", text)
    }
    return parameters & assignments


def _git_index_mode(root: Path, path: str) -> str | None:
    proc = subprocess.run(
        ["git", "ls-files", "-s", "--", path],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return proc.stdout.split()[0]


def _validate_envelope_schema(root: Path, envelope: dict[str, Any]) -> list[str]:
    if Draft202012Validator is None:
        return ["DEPENDENCY_MISSING:jsonschema"]
    schema_path = root / "docs" / "operations" / "autonomy" / "autonomy-envelope.schema.json"
    try:
        schema = _read_json(schema_path)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(envelope), key=lambda e: list(e.absolute_path))
    except Exception as exc:
        return ["ENVELOPE_SCHEMA_VALIDATOR:" + type(exc).__name__]
    issues = []
    for error in errors:
        path = ".".join(str(part) for part in error.absolute_path) or "<root>"
        issues.append("ENVELOPE_SCHEMA_ERROR:" + path + ":" + error.validator)
    return issues


def validate_envelope_data(envelope: dict[str, Any], *, max_threads: int) -> list[str]:
    issues: list[str] = []
    if envelope.get("schema_version") != "SER-AUTONOMY-ENVELOPE-2":
        issues.append("ENVELOPE_SCHEMA_VERSION")

    activation = envelope.get("activation") or {}
    state = activation.get("state")
    classes = envelope.get("authority_classes") or {}
    a0, a1, a2, a3 = (classes.get(k) or {} for k in ("A0", "A1", "A2", "A3"))

    if state == "ACTIVE_A0_A1":
        if a0.get("autonomous") is not True or a1.get("autonomous") is not True:
            issues.append("A0_A1_ACTIVATION_MISMATCH")

    if a2.get("autonomous") is True:
        if state != "ACTIVE_A0_A1_A2":
            issues.append("A2_STATE_MISMATCH")
        if not activation.get("a2_reference"):
            issues.append("A2_REFERENCE_REQUIRED")
        if not isinstance(envelope.get("a2_contract"), dict):
            issues.append("A2_CONTRACT_REQUIRED")
    elif state == "ACTIVE_A0_A1_A2":
        issues.append("A2_FALSE_BUT_STATE_ACTIVE")

    if a3.get("autonomous") is not False:
        issues.append("A3_MUST_BE_HUMAN_ONLY")

    budgets = envelope.get("budgets") or {}
    if budgets.get("same_state_same_command_retries") != 0:
        issues.append("BLIND_RETRY_MUST_BE_ZERO")
    if budgets.get("max_write_capable_agents") != 1:
        issues.append("SINGLE_WRITER_REQUIRED")

    concurrent = budgets.get("max_concurrent_subagents")
    if not isinstance(concurrent, int) or concurrent < 1 or concurrent > max_threads:
        issues.append("CONCURRENCY_EXCEEDS_CODEX_CONFIG")

    if not isinstance(budgets.get("max_causal_repair_rounds_per_gate"), int) or budgets["max_causal_repair_rounds_per_gate"] < 1:
        issues.append("CAUSAL_REPAIR_BUDGET_INVALID")
    if not isinstance(budgets.get("max_hypotheses_per_root_cause"), int) or budgets["max_hypotheses_per_root_cause"] < 1:
        issues.append("HYPOTHESIS_BUDGET_INVALID")
    if not isinstance(budgets.get("max_unknown_effects_before_human"), int) or budgets["max_unknown_effects_before_human"] < 1:
        issues.append("UNKNOWN_BUDGET_INVALID")

    scope = envelope.get("repo_scope") or {}
    if not isinstance(scope.get("write_roots"), list) or not scope["write_roots"]:
        issues.append("WRITE_ROOTS_REQUIRED")
    if not isinstance(scope.get("protected_roots"), list) or not scope["protected_roots"]:
        issues.append("PROTECTED_ROOTS_REQUIRED")
    return issues


def _validate_permission_profile(cfg: dict[str, Any], envelope: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    if "sandbox_mode" in cfg or "sandbox_workspace_write" in cfg:
        issues.append("LEGACY_SANDBOX_MUST_BE_ABSENT")
    if cfg.get("default_permissions") != A0_PROFILE:
        issues.append("ROOT_PERMISSIONS_PROFILE")
    if cfg.get("approval_policy") != "never":
        issues.append("ROOT_APPROVAL_POLICY_MUST_BE_NEVER")
    if (cfg.get("windows") or {}).get("sandbox") != "elevated":
        issues.append("WINDOWS_SANDBOX_NOT_ELEVATED")

    profiles = cfg.get("permissions") or {}
    a0 = profiles.get(A0_PROFILE) if isinstance(profiles, dict) else None
    a1 = profiles.get(A1_PROFILE) if isinstance(profiles, dict) else None

    if not isinstance(a0, dict):
        issues.append("A0_PERMISSION_PROFILE_MISSING")
    else:
        filesystem = a0.get("filesystem") or {}
        workspace = filesystem.get(":workspace_roots") or {}
        profile_roots = a0.get("workspace_roots") or {}
        expected_filesystem_keys = {
            ":root", ":minimal", ":tmpdir", ":slash_tmp",
            ":workspace_roots", A0_WINDOWS_SCRATCH,
        }
        if set(filesystem) != expected_filesystem_keys:
            issues.append("A0_FILESYSTEM_KEYS_MISMATCH")
        if workspace != {".": "read"}:
            issues.append("A0_WORKSPACE_ROOT_MAP_MISMATCH")
        if profile_roots != {A0_WINDOWS_SCRATCH: True}:
            issues.append("A0_PROFILE_WORKSPACE_ROOT_MAP_MISMATCH")
        if filesystem.get(":root") != "read":
            issues.append("A0_WINDOWS_ROOT_READ_REQUIRED")
        if filesystem.get(":minimal") != "read" or workspace.get(".") != "read":
            issues.append("A0_REPOSITORY_READ_ONLY_REQUIRED")
        if filesystem.get(":tmpdir") != "write":
            issues.append("A0_TMPDIR_WRITE_REQUIRED")
        if filesystem.get(":slash_tmp") != "write":
            issues.append("A0_SLASH_TMP_WRITE_REQUIRED")
        if profile_roots.get(A0_WINDOWS_SCRATCH) is not True:
            issues.append("A0_WINDOWS_SCRATCH_WORKSPACE_ROOT_REQUIRED")
        if filesystem.get(A0_WINDOWS_SCRATCH) != "write":
            issues.append("A0_WINDOWS_SCRATCH_WRITE_REQUIRED")
        if LEGACY_WINDOWS_QUALIFIED_PYTHON_ROOT in filesystem:
            issues.append("A0_HOST_PYTHON_READ_MUST_BE_ABSENT")
        if (a0.get("network") or {}).get("enabled") is not False:
            issues.append("A0_NETWORK_MUST_BE_DISABLED")
        if (a0.get("network") or {}) != {"enabled": False}:
            issues.append("A0_NETWORK_POLICY_MUST_BE_EXACT_DISABLED")

    if not isinstance(a1, dict):
        issues.append("A1_PERMISSION_PROFILE_MISSING")
        return issues

    filesystem = a1.get("filesystem") or {}
    workspace = filesystem.get(":workspace_roots") or {}
    expected_filesystem_keys = {
        ":root", ":minimal", ":tmpdir", ":slash_tmp", ":workspace_roots",
    }
    if set(filesystem) != expected_filesystem_keys:
        issues.append("A1_FILESYSTEM_KEYS_MISMATCH")
    if filesystem.get(":root") != "read":
        issues.append("A1_WINDOWS_ROOT_READ_REQUIRED")
    if filesystem.get(":minimal") != "read":
        issues.append("A1_MINIMAL_READ_REQUIRED")
    if filesystem.get(":tmpdir") != "write":
        issues.append("A1_TMPDIR_WRITE_REQUIRED")
    if filesystem.get(":slash_tmp") != "write":
        issues.append("A1_SLASH_TMP_WRITE_REQUIRED")
    if LEGACY_WINDOWS_QUALIFIED_PYTHON_ROOT in filesystem:
        issues.append("A1_HOST_PYTHON_READ_MUST_BE_ABSENT")
    if workspace.get(".") != "read":
        issues.append("A1_WORKSPACE_DEFAULT_MUST_BE_READ")

    actual_writes = {
        _normalize_write_root(path)
        for path, access in workspace.items()
        if path != "." and access == "write"
    }
    expected_writes = {
        _normalize_write_root(path)
        for path in (envelope.get("repo_scope") or {}).get("write_roots", [])
    }
    normalized_workspace = {
        "." if path == "." else _normalize_write_root(path): access
        for path, access in workspace.items()
    }
    expected_workspace = {".": "read", **{path: "write" for path in expected_writes}}
    if normalized_workspace != expected_workspace:
        issues.append("A1_WORKSPACE_ROOT_MAP_MISMATCH")
    if actual_writes != expected_writes:
        issues.append(
            "A1_PERMISSION_WRITE_ROOT_MISMATCH:expected="
            + ",".join(sorted(expected_writes))
            + ":actual="
            + ",".join(sorted(actual_writes))
        )
    if any(access not in {"read", "write", "deny"} for access in workspace.values()):
        issues.append("A1_PERMISSION_ACCESS_VALUE")
    if ".git" in actual_writes or any(path.startswith(".git/") for path in actual_writes):
        issues.append("A1_DIRECT_GIT_METADATA_WRITE_FORBIDDEN")
    if (a1.get("network") or {}).get("enabled") is not False:
        issues.append("A1_DIRECT_NETWORK_MUST_BE_DISABLED")
    if (a1.get("network") or {}) != {"enabled": False}:
        issues.append("A1_NETWORK_POLICY_MUST_BE_EXACT_DISABLED")
    if any("*" in path or "?" in path or "[" in path for path in expected_writes):
        issues.append("A1_WRITE_ROOTS_MUST_BE_CONCRETE")

    forbidden_exact = {
        ".codex/config.toml",
        "docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md",
        "docs/operations/CODEX_RUNTIME_QUALIFICATION.md",
        "docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md",
        "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json",
        "tools/validate_codex_autonomy.py",
        "tools/check_codex_autonomy_delta.py",
        "tools/tests/test_codex_autonomy.py",
    }
    overlap = sorted(expected_writes & forbidden_exact)
    if overlap:
        issues.append("A1_GOVERNANCE_WRITE_OVERLAP:" + ",".join(overlap))

    return issues

def validate(root: Path = ROOT) -> dict[str, Any]:
    issues: list[str] = []
    config_path = root / ".codex" / "config.toml"
    try:
        cfg = _read_toml(config_path)
    except Exception as exc:
        return {
            "schema_version": "SER-CODEX-AUTONOMY-VALIDATION-21",
            "status": "FAIL",
            "issues": ["CONFIG_UNREADABLE:" + type(exc).__name__],
        }

    if _git_index_mode(root, "tools/validate_codex_autonomy.py") != "100755":
        issues.append("VALIDATOR_GIT_MODE_MUST_BE_100755")

    if cfg.get("model") != "gpt-6-astra":
        issues.append("ROOT_MODEL_NOT_ASTRA")
    if cfg.get("model_reasoning_effort") != "high":
        issues.append("ROOT_REASONING_NOT_HIGH")

    features = cfg.get("features") or {}
    if features.get("apps") is not False:
        issues.append("APPS_MUST_BE_DISABLED")
    if features.get("remote_plugin") is not False:
        issues.append("REMOTE_PLUGIN_MUST_BE_DISABLED")
    if features.get("plugins") is not False:
        issues.append("PLUGINS_MUST_BE_DISABLED")
    if features.get("connectors") is not False:
        issues.append("CONNECTORS_MUST_BE_DISABLED")
    if features.get("enable_mcp_apps") is not False or features.get("codex_apps_mcp_2026_07_28") is not False:
        issues.append("MCP_APPS_MUST_BE_DISABLED")
    if (
        features.get("browser_use") is not False
        or features.get("browser_use_external") is not False
        or features.get("browser_use_full_cdp_access") is not False
    ):
        issues.append("BROWSER_USE_MUST_BE_DISABLED")
    if features.get("computer_use") is not False:
        issues.append("COMPUTER_USE_MUST_BE_DISABLED")
    if features.get("multi_agent") is not True:
        issues.append("MULTI_AGENT_NOT_ENABLED")
    if features.get("goals") is not True:
        issues.append("GOALS_NOT_ENABLED")
    if features.get("hooks") is not True:
        issues.append("HOOKS_NOT_ENABLED")

    agents_cfg = cfg.get("agents") or {}
    if agents_cfg.get("enabled") is not True:
        issues.append("AGENTS_NOT_ENABLED")

    max_threads = agents_cfg.get("max_concurrent_threads_per_session")
    if max_threads != 5:
        issues.append("THREAD_LIMIT")
        max_threads = max_threads if isinstance(max_threads, int) and max_threads > 0 else 1

    if agents_cfg.get("default_subagent_model") != "gpt-6-sol":
        issues.append("DEFAULT_SUBAGENT_MODEL")
    if agents_cfg.get("default_subagent_reasoning_effort") != "medium":
        issues.append("DEFAULT_SUBAGENT_EFFORT")

    roles = {k: v for k, v in agents_cfg.items() if isinstance(v, dict)}
    if set(roles) != set(EXPECTED_AGENTS):
        issues.append("ROLE_SET")

    write_capable = 0
    for role, (file_name, permission_profile, model, effort) in EXPECTED_AGENTS.items():
        role_cfg = roles.get(role) or {}
        if role_cfg.get("config_file") != "agents/" + file_name:
            issues.append("ROLE_CONFIG_FILE:" + role)
        if not isinstance(role_cfg.get("description"), str) or not role_cfg["description"].strip():
            issues.append("ROLE_DESCRIPTION:" + role)

        path = root / ".codex" / "agents" / file_name
        try:
            data = _read_toml(path)
        except Exception as exc:
            issues.append("AGENT_UNREADABLE:" + role + ":" + type(exc).__name__)
            continue

        for required in ("name", "description", "developer_instructions"):
            if not isinstance(data.get(required), str) or not data[required].strip():
                issues.append("AGENT_REQUIRED_FIELD:" + role + ":" + required)
        if data.get("name") != role:
            issues.append("AGENT_NAME:" + role)
        if data.get("model") != model:
            issues.append("AGENT_MODEL:" + role)
        if data.get("model_reasoning_effort") != effort:
            issues.append("AGENT_REASONING:" + role)
        if data.get("default_permissions") != permission_profile:
            issues.append("AGENT_PERMISSIONS:" + role)
        if "sandbox_mode" in data or "sandbox_workspace_write" in data:
            issues.append("AGENT_LEGACY_SANDBOX:" + role)
        if "permissions" in data:
            issues.append("AGENT_DUPLICATE_PERMISSION_PROFILE:" + role)
        instructions = data.get("developer_instructions") or ""
        if role == "executor":
            required_cq3_tokens = (
                "CQ3_EXECUTOR_PERMISSION_PROBES",
                ".codex/.cq3_executor_governance_probe.txt",
                ".cq3_executor_unlisted_probe.txt",
                "BLOCKED_ALLOWED_WRITE_DENIED",
                "SECURITY_STOP",
                "do not stop merely because",
                "For ordinary A1 work and outside the qualification-only exception above",
                "Outside the exact negative probe attempts above, obey envelope write_roots",
                "Except for the exact one-attempt governance sentinel probe above",
                ".codex\\probes\\cq3_executor_network_probe.ps1",
                "AccessDenied",
                "10013",
                "Do not use Invoke-WebRequest",
                "serialization self-test PASS",
            )
            if any(token not in instructions for token in required_cq3_tokens):
                issues.append("EXECUTOR_CQ3_BEHAVIORAL_PROBE_CONTRACT:" + role)
        else:
            required_cq3_tokens = (
                "CQ3_NEGATIVE_PERMISSION_PROBE",
                "exactly one direct filesystem write attempt",
                "do not retry",
                "SECURITY_STOP",
                "Outside this exact task label",
                "For ordinary work and outside the qualification-only exception above",
            )
            if any(token not in instructions for token in required_cq3_tokens):
                issues.append("READ_ONLY_CQ3_NEGATIVE_PROBE_CONTRACT:" + role)

        if role == "executor":
            write_capable += int(data.get("default_permissions") == A1_PROFILE)
            granular = (data.get("approval_policy") or {}).get("granular") if isinstance(data.get("approval_policy"), dict) else None
            expected_granular = {
                "sandbox_approval": False,
                "rules": True,
                "mcp_elicitations": False,
                "request_permissions": False,
                "skill_approval": False,
            }
            if granular != expected_granular:
                issues.append("EXECUTOR_GRANULAR_APPROVALS")
            if data.get("approvals_reviewer") != "auto_review":
                issues.append("EXECUTOR_APPROVAL_REVIEWER")
        elif data.get("approval_policy") != "never":
            issues.append("READ_ONLY_AGENT_APPROVAL_POLICY:" + role)
        if (data.get("agents") or {}).get("enabled") is not False:
            issues.append("SUBAGENT_NESTING_NOT_DISABLED:" + role)

    if write_capable != 1:
        issues.append("WRITE_CAPABLE_AGENT_COUNT")

    envelope_path = root / "docs" / "operations" / "autonomy" / "B1_AUTONOMY_ENVELOPE.json"
    try:
        envelope = _read_json(envelope_path)
        issues.extend(_validate_envelope_schema(root, envelope))
        issues.extend(validate_envelope_data(envelope, max_threads=max_threads))
        issues.extend(_validate_permission_profile(cfg, envelope))

    except Exception as exc:
        issues.append("ENVELOPE_UNREADABLE:" + type(exc).__name__)

    required_paths = [
        "docs/decisions/ADR-0024-codex-autonomous-controller.md",
        "docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md",
        "docs/operations/CODEX_AUTONOMOUS_RETROSPECTIVE.md",
        "docs/operations/CODEX_AUTONOMOUS_START_PROMPT.md",
        "docs/operations/CODEX_RUNTIME_QUALIFICATION.md",
        "docs/operations/autonomy/autonomy-envelope.schema.json",
        ".agents/skills/ser-autonomous-controller/SKILL.md",
        ".codex/hooks/pre_scope_guard.py",
        ".codex/hooks/post_scope_guard.py",
        ".codex/hooks/pre_scope_guard.ps1",
        ".codex/hooks/post_scope_guard.ps1",
        "tools/requirements-codex-autonomy.txt",
        "tools/codex_desktop_cq_host_preflight.ps1",
        ".codex/rules/a1_git_transport.rules",
        ".codex/transport/a1_git_transport.ps1",
        ".codex/transport/a1_operational_git_transport.ps1",
        "docs/operations/autonomy/A1_OPERATIONAL_POLICY.json",
        ".codex/probes/cq3_executor_network_probe.ps1",
        ".codex/hooks/external_surface_guard.ps1",
        ".codex/hooks/external_surface_guard.py",
        "docs/operations/autonomy/CODEX_DESKTOP_TOOL_SURFACE_POLICY.json",
        "docs/operations/CODEX_DESKTOP_CQ_RUN_PROMPT_TEMPLATE.md",
        "docs/operations/CODEX_CLI_WINDOWS_CQ.md",
        "docs/operations/autonomy/CODEX_CLI_TOOL_SURFACE_POLICY.json",
        "docs/operations/CODEX_CLI_CQ_RUN_PROMPT_TEMPLATE.md",
        "tools/codex_cli_cq_host_preflight.ps1",
        "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl",
    ]
    for rel in required_paths:
        if not (root / rel).is_file():
            issues.append("REQUIRED_PATH_MISSING:" + rel)

    cli_cq_path = root / "docs" / "operations" / "CODEX_CLI_WINDOWS_CQ.md"
    cli_preflight_path = root / "tools" / "codex_cli_cq_host_preflight.ps1"
    if cli_cq_path.is_file():
        cli_text = cli_cq_path.read_text(encoding="utf-8")
        required_cli_tokens = (
            "CODEX_CLI_WINDOWS_TUI",
            "AC-R2-CLI-HOST-PREFLIGHT-1",
            "SER-CODEX-CLI-CQ-REQUEST-1",
            "CODEX_CLI_VERSION",
            "PROJECT_CONFIG_LAYER = ENABLED",
            "PreToolUse  Installed 2  Active 2",
            "PostToolUse Installed 1  Active 1",
            "CODEX_CLI_TOOL_SURFACE_POLICY.json",
            "FORBIDDEN_SURFACE_PROBE = NOT_APPLICABLE_ABSENT",
            "BLOCK_UNEXPECTED_IN_CANONICAL_CLI_RUNTIME",
            "DO_NOT_EXECUTE_PYTHON_IN_SANDBOX",
            "HOST_VALIDATOR",
            "HOST_METATESTS",
            "HOST_NETWORK_BASELINE",
            "CQ_RUN_REQUEST.json",
            "CQ_RUN_PROMPT.md",
            "CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST",
            "standalone checkout",
            "AccessDenied",
            "10013",
        )
        if any(token not in cli_text for token in required_cli_tokens):
            issues.append("CLI_WINDOWS_CQ_CONTRACT_INVALID")
    else:
        issues.append("CLI_WINDOWS_CQ_CONTRACT_MISSING")

    if cli_preflight_path.is_file():
        cli_preflight_text = cli_preflight_path.read_text(encoding="utf-8")
        required_cli_preflight_tokens = (
            "AC-R2-CLI-HOST-PREFLIGHT-1",
            "SER-CODEX-CLI-CQ-REQUEST-1",
            "CODEX_CLI_WINDOWS_TUI",
            'Join-Path $env:APPDATA "npm\\codex.cmd"',
            "CODEX_CLI_VERSION =",
            "SER-CODEX-AUTONOMY-VALIDATION-21",
            "docs\\operations\\CODEX_CLI_WINDOWS_CQ.md",
            "docs\\operations\\autonomy\\CODEX_CLI_TOOL_SURFACE_POLICY.json",
            "docs\\operations\\CODEX_CLI_CQ_RUN_PROMPT_TEMPLATE.md",
            'cli_preflight = "tools\\codex_cli_cq_host_preflight.ps1"',
            "CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST",
            "CHECKOUT_MODE = STANDALONE",
        )
        if any(token not in cli_preflight_text for token in required_cli_preflight_tokens):
            issues.append("CLI_WINDOWS_HOST_PREFLIGHT_INVALID")
        if "CODEX_DESKTOP_WINDOWS" in cli_preflight_text:
            issues.append("CLI_WINDOWS_HOST_PREFLIGHT_DESKTOP_SURFACE_LEAK")
    else:
        issues.append("CLI_WINDOWS_HOST_PREFLIGHT_MISSING")

    desktop_cq_path = root / "docs" / "operations" / "CODEX_DESKTOP_WINDOWS_CQ.md"
    desktop_preflight_path = root / "tools" / "codex_desktop_cq_host_preflight.ps1"
    if desktop_cq_path.is_file():
        desktop_text = desktop_cq_path.read_text(encoding="utf-8")
        required_desktop_tokens = (
            "CODEX_DESKTOP_WINDOWS",
            "CQ_HOST_PREFLIGHT.json",
            "AC-R2-DESKTOP-HOST-PREFLIGHT-6",
            "NOT_OBSERVABLE_DESKTOP",
            "PASS_BEHAVIORALLY",
            "INTERNAL_CLIENT_CONTROL_PLANE",
            "EXTERNAL_MUTATING_PLUGIN_SURFACE",
            "DO_NOT_EXECUTE_PYTHON_IN_SANDBOX",
            "HOST_VALIDATOR",
            "HOST_METATESTS",
            "HOST_NETWORK_BASELINE",
            "NETWORK_PROBE_SERIALIZATION_SELFTEST",
            "EXTERNAL_SURFACE_PRETOOL_GUARD",
            "CQ_RUN_REQUEST.json",
            "CQ_RUN_PROMPT.md",
            "HOOK_TRUST_REVIEW_REQUIRED",
            "PROJECT_HOOK_TRUST",
            "AccessDenied",
            "10013",
            "standalone checkout",
        )
        if any(token not in desktop_text for token in required_desktop_tokens):
            issues.append("DESKTOP_WINDOWS_CQ_CONTRACT_INVALID")
        if "CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST" not in desktop_text:
            issues.append("DESKTOP_WINDOWS_CQ_READINESS_CONTRACT")
        if "CQ_READY_TO_RUN = PASS" in desktop_text:
            issues.append("DESKTOP_WINDOWS_CQ_PREMATURE_READY_PASS")
    if desktop_preflight_path.is_file():
        preflight_text = desktop_preflight_path.read_text(encoding="utf-8")
        if "CODEX_DESKTOP_RUNTIME_UNQUALIFIED_USE_TOOLS_CODEX_CLI_CQ_HOST_PREFLIGHT_PS1" not in preflight_text:
            issues.append("DESKTOP_WINDOWS_HOST_PREFLIGHT_NOT_RETIRED")
        required_preflight_tokens = (
            "git fetch origin $ExpectedBranch",
            "AC-R2-DESKTOP-HOST-PREFLIGHT-6",
            "CQ_HOST_PREFLIGHT.json",
            "jsonschema",
            "recorded_at_unix_seconds",
            "tools/validate_codex_autonomy.py",
            "tools.tests.test_codex_autonomy",
            "Invoke-CapturedProcess",
            "host_validation",
            "runtime_test_count",
            "static_test_count",
            "source_sha256",
            "network_probe",
            "network_probe_script",
            "networkSelfTestPayload",
            "NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS",
            "NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST = PASS",
            "MCP_GUARD_SELFTEST = PASS",
            "SCOPE_GUARDS_SELFTEST = PASS",
            "A1_GIT_TRANSPORT_SELFTEST = PASS",
            "CQ_RUN_REQUEST.json",
            "CQ_RUN_PROMPT.md",
            "HOOK_TRUST_REVIEW_REQUIRED",
            "PROJECT_HOOKS_SHA256",
            "CQ_HOST_PREFLIGHT_RUN_REQUEST_ROUNDTRIP_MISMATCH",
            "CQ_HOST_PREFLIGHT_PROMPT_TEMPLATE_UNRESOLVED",
            "external_surface_guard_python",
            "pre_scope_guard_python",
            "post_scope_guard_python",
            "operational_transport",
            "operational_policy",
            "rules",
            "executor_agent",
            "protocol",
            "runtime_contract",
            "desktop_contract",
            "start_prompt",
            "envelope_schema",
            "agents_md",
            "controller_skill",
            "explorer_agent",
            "domain_auditor_agent",
            "evidence_auditor_agent",
            "architecture_auditor_agent",
            "A1_OPERATIONAL_TRANSPORT_SELFTEST = PASS",
            "HOST_NETWORK_BASELINE = PASS",
            "$NetworkProbeHost",
            "selected_ipv4",
            "CQ_HOST_PREFLIGHT_GIT_IDENTITY_CHANGED_DURING_HOST_VALIDATION",
            "final_head",
            "final_tree",
            "final_clean",
            "CQ_HOST_PREFLIGHT_LINKED_WORKTREE_UNSUPPORTED",
            "checkout_mode",
            "CHECKOUT_MODE = STANDALONE",
        )
        if any(token not in preflight_text for token in required_preflight_tokens):
            issues.append("DESKTOP_WINDOWS_HOST_PREFLIGHT_INVALID")
        if "pip install" in preflight_text or "python -m pip" in preflight_text:
            issues.append("DESKTOP_WINDOWS_HOST_PREFLIGHT_INSTALL_FORBIDDEN")
        if "CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST" not in preflight_text:
            issues.append("DESKTOP_WINDOWS_HOST_PREFLIGHT_READINESS_CONTRACT")

    start_prompt_path = root / "docs" / "operations" / "CODEX_AUTONOMOUS_START_PROMPT.md"
    if start_prompt_path.is_file():
        start_text = start_prompt_path.read_text(encoding="utf-8")
        required_start_tokens = (
            "HOOK_TRUST_REVIEW_REQUIRED = true",
            "CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST",
            "CODEX_CLI_WINDOWS_TUI",
            "codex_cli_cq_host_preflight.ps1",
            "/hooks",
            "CQ_RUN_REQUEST.json",
            "CQ_RUN_PROMPT.md",
            "standalone checkout",
        )
        if any(token not in start_text for token in required_start_tokens):
            issues.append("CODEX_AUTONOMOUS_START_PROMPT_INVALID")
        if "Settings > Hooks" in start_text:
            issues.append("CODEX_AUTONOMOUS_START_PROMPT_LEGACY_HOOK_TRUST_UI")
        if "CQ_READY_TO_RUN = PASS" in start_text:
            issues.append("CODEX_AUTONOMOUS_START_PROMPT_PREMATURE_READY_PASS")
    else:
        issues.append("CODEX_AUTONOMOUS_START_PROMPT_MISSING")

    protocol_path = root / "docs" / "operations" / "CODEX_AUTONOMOUS_PROTOCOL.md"
    if protocol_path.is_file():
        protocol_text = protocol_path.read_text(encoding="utf-8")
        required_protocol_tokens = (
            "Falha recuperável não é Human Gate",
            "Qualificação versus transporte operacional",
            "a1_operational_git_transport.ps1",
            "A1_OPERATIONAL_POLICY.json",
            "runtime_validation=PASS",
            "effective_config_observation=PASS",
            "qualified HEAD",
            "operational base",
            "CLI host preflight v1",
            "CODEX_CLI_TOOL_SURFACE_POLICY.json",
            "external_surface_guard",
            "Depois de CQ4 não há segunda escrita repo-side",
            "AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION",
            "standalone checkout",
            "UNQUALIFIED_FOR_CONTROLLER",
        )
        if any(token not in protocol_text for token in required_protocol_tokens):
            issues.append("CODEX_AUTONOMOUS_PROTOCOL_STABILIZATION_DRIFT")
        if "host preflight v5" in protocol_text:
            issues.append("CODEX_AUTONOMOUS_PROTOCOL_LEGACY_PREFLIGHT")
    else:
        issues.append("CODEX_AUTONOMOUS_PROTOCOL_MISSING")

    network_probe_path = root / ".codex" / "probes" / "cq3_executor_network_probe.ps1"
    if network_probe_path.is_file():
        network_probe_text = network_probe_path.read_text(encoding="utf-8")
        required_network_probe_tokens = (
            "AC-R2-CLI-HOST-PREFLIGHT-1",
            "network_probe_script",
            "BeginConnect",
            "EndConnect",
            "PASS_NETWORK_DENIED",
            "FAIL_NETWORK_BOUNDARY_OPEN",
            "NOT_PROVEN",
            "AccessDenied",
            "10013",
            "attempt_count",
            "TCP_RAW",
            "dns_in_sandbox",
            "CQ_HOST_PREFLIGHT.sha256",
            "AC-R2-CQ3-NETWORK-PROBE-SELFTEST-1",
            "Convert-ProbePayloadToJson",
            "New-ProbePayload",
            "network_attempt_count",
            "$hostSerializationSelfTestEvidence",
            "OfflineRuntimeSelfTest",
            "AC-R2-CQ3-NETWORK-PROBE-OFFLINE-RUNTIME-SELFTEST-1",
            "AssignmentStatementAst",
        )
        if any(token not in network_probe_text for token in required_network_probe_tokens):
            issues.append("DESKTOP_WINDOWS_NETWORK_PROBE_INVALID")
        if network_probe_text.count(".BeginConnect(") != 1:
            issues.append("DESKTOP_WINDOWS_NETWORK_PROBE_NOT_SINGLE_CONNECT")
        if "New-Object System.Collections.Generic.List[object]" in network_probe_text:
            issues.append("DESKTOP_WINDOWS_NETWORK_PROBE_UNSAFE_GENERIC_LIST")
        if "exception_type = $(if" in network_probe_text:
            issues.append("DESKTOP_WINDOWS_NETWORK_PROBE_INLINE_DYNAMIC_PAYLOAD_FORBIDDEN")
        collisions = _powershell_parameter_assignment_collisions(network_probe_text)
        if collisions:
            issues.append(
                "DESKTOP_WINDOWS_NETWORK_PROBE_PARAMETER_ASSIGNMENT_COLLISION:"
                + ",".join(sorted(collisions))
            )
        forbidden_network_probe_tokens = (
            "Invoke-WebRequest",
            "HttpClient",
            "SslStream",
            "Dns.GetHostAddresses",
            "curl ",
        )
        if any(token in network_probe_text for token in forbidden_network_probe_tokens):
            issues.append("DESKTOP_WINDOWS_NETWORK_PROBE_HIGH_LEVEL_NETWORK_FORBIDDEN")

    rule_path = root / ".codex" / "rules" / "a1_git_transport.rules"
    transport_path = root / ".codex" / "transport" / "a1_git_transport.ps1"
    if rule_path.is_file():
        rule_text = rule_path.read_text(encoding="utf-8")
        if 'decision = "prompt"' not in rule_text or "a1_git_transport.ps1" not in rule_text:
            issues.append("A1_GIT_RULE_INVALID")
        if "a1_operational_git_transport.ps1" not in rule_text:
            issues.append("A1_OPERATIONAL_GIT_TRANSPORT_RULE_MISSING")
        if '"powershell.exe -NoProfile' in rule_text:
            issues.append("A1_GIT_RULE_STRING_EXAMPLE_FORBIDDEN")
        if 'match = [' not in rule_text or 'not_match = [' not in rule_text:
            issues.append("A1_GIT_RULE_EXAMPLES_MISSING")
    if transport_path.is_file():
        transport_text = transport_path.read_text(encoding="utf-8")
        required_transport_tokens = (
            'ser/B1-ser03-ser05-authoring',
            'tools/check_codex_autonomy_delta.py --worktree',
            'tools/check_codex_autonomy_delta.py --index',
            'HEAD:refs/heads/$ExpectedBranch',
            'A1_GIT_TRANSPORT_ENVELOPE_PATH_MISMATCH',
            'CQ_JOURNAL_ONLY',
            'git remote get-url --push origin',
            'git ls-remote origin',
            'AC-R2-DESKTOP-HOST-PREFLIGHT-6',
            'evidence.python.executable',
            'A1_GIT_TRANSPORT_LINKED_WORKTREE_UNSUPPORTED',
            'A1_GIT_TRANSPORT_HOST_EVIDENCE_CHECKOUT_MODE',
        )
        if any(token not in transport_text for token in required_transport_tokens):
            issues.append("A1_GIT_TRANSPORT_INVALID")
        if "--force" in transport_text:
            issues.append("A1_GIT_TRANSPORT_FORCE_FORBIDDEN")
        if re.search(r"(?m)^\s*&\s+python(?:\.exe)?\s", transport_text):
            issues.append("A1_GIT_TRANSPORT_BARE_PYTHON_FORBIDDEN")

    operational_policy_path = root / "docs" / "operations" / "autonomy" / "A1_OPERATIONAL_POLICY.json"
    operational_transport_path = root / ".codex" / "transport" / "a1_operational_git_transport.ps1"
    if operational_policy_path.is_file():
        try:
            operational_policy = _read_json(operational_policy_path)
            if operational_policy.get("schema_version") != "SER-CODEX-A1-OPERATIONAL-2":
                issues.append("A1_OPERATIONAL_POLICY_SCHEMA")
            invariants = operational_policy.get("invariants") or {}
            if "single-shot" not in str(invariants.get("qualification_transport") or ""):
                issues.append("A1_OPERATIONAL_POLICY_CQ_SEPARATION")
            if "qualified control identity" not in str(invariants.get("control_identity") or "").lower():
                issues.append("A1_OPERATIONAL_POLICY_CONTROL_IDENTITY")
            bootstrap = operational_policy.get("bootstrap") or {}
            canonical = bootstrap.get("canonical_state_required") or {}
            if canonical.get("runtime_validation") != "PASS" or canonical.get("effective_config_observation") != "PASS":
                issues.append("A1_OPERATIONAL_POLICY_CANONICAL_PASS")
            if canonical.get("runtime_blocker_absent") != "AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION":
                issues.append("A1_OPERATIONAL_POLICY_RUNTIME_BLOCKER")
            if bootstrap.get("qualified_head_must_be_ancestor") is not True:
                issues.append("A1_OPERATIONAL_POLICY_ANCESTRY")
            if bootstrap.get("current_local_must_equal_remote") is not True:
                issues.append("A1_OPERATIONAL_POLICY_LOCAL_REMOTE_BINDING")
            if bootstrap.get("worktree_must_be_clean") is not True:
                issues.append("A1_OPERATIONAL_POLICY_CLEAN_BOOTSTRAP")
            if len(bootstrap.get("allowed_bridge_paths") or []) != 4:
                issues.append("A1_OPERATIONAL_POLICY_BRIDGE_PATHS")
            recovery = operational_policy.get("recovery") or {}
            if recovery.get("same_state_same_command_retries") != 0:
                issues.append("A1_OPERATIONAL_POLICY_BLIND_RETRY")
            checkpoint = operational_policy.get("checkpoints") or {}
            if checkpoint.get("role") != "progress tracking only; not an authority source":
                issues.append("A1_OPERATIONAL_POLICY_CHECKPOINT_AUTHORITY")
        except Exception as exc:
            issues.append("A1_OPERATIONAL_POLICY_UNREADABLE:" + type(exc).__name__)
    else:
        issues.append("A1_OPERATIONAL_POLICY_MISSING")

    if operational_transport_path.is_file():
        operational_transport_text = operational_transport_path.read_text(encoding="utf-8")
        required_operational_tokens = (
            "SER-A1-OPERATIONAL-CHECKPOINT-2",
            "SER-A1-OPERATIONAL-TRANSPORT-SELFTEST-2",
            "InitializeCheckpoint",
            "ReconcileOnly",
            "Require-ControlIdentity",
            "Require-CanonicalRuntimePass",
            "Get-ReconcileDecision",
            "A1_OPERATIONAL_RUNTIME_NOT_CANONICAL_PASS",
            "A1_OPERATIONAL_EFFECTIVE_CONFIG_NOT_CANONICAL_PASS",
            "A1_OPERATIONAL_RUNTIME_BLOCKER_STILL_PRESENT",
            "A1_OPERATIONAL_QUALIFIED_HEAD_NOT_ANCESTOR",
            "A1_OPERATIONAL_BOOTSTRAP_UNEXPECTED_PATH",
            "A1_OPERATIONAL_CONTROL_IDENTITY_DRIFT",
            "A1_OPERATIONAL_RECONCILE=PUBLISHED_SUCCESSOR",
            "A1_OPERATIONAL_RECONCILE=RESUMED_PUSH",
            "A1_OPERATIONAL_UNKNOWN_DIVERGENCE",
            "A1_OPERATIONAL_PUSH_FAILED_LOCAL_COMMIT_PRESERVED",
            "A1_OPERATIONAL_PUSH_READBACK_UNKNOWN_LOCAL_COMMIT_PRESERVED",
            "check_codex_autonomy_delta.py --base",
            "git remote get-url --push origin",
            "git ls-remote origin",
            "A1_OPERATIONAL_LINKED_WORKTREE_UNSUPPORTED",
            "A1_OPERATIONAL_HOST_EVIDENCE_CHECKOUT_MODE",
        )
        if any(token not in operational_transport_text for token in required_operational_tokens):
            issues.append("A1_OPERATIONAL_TRANSPORT_CONTRACT")
        if re.search(r"(?m)^\s*&\s+python(?:\.exe)?\s", operational_transport_text):
            issues.append("A1_OPERATIONAL_TRANSPORT_BARE_PYTHON_FORBIDDEN")
        if "--force" in operational_transport_text:
            issues.append("A1_OPERATIONAL_TRANSPORT_FORCE_FORBIDDEN")
        if "lastJournal" in operational_transport_text or "CQ3_A1_POSITIVE_PROBE" in operational_transport_text:
            issues.append("A1_OPERATIONAL_TRANSPORT_JOURNAL_AUTHORITY_FORBIDDEN")
        selftest_pos = operational_transport_text.find("if($SelfTest)")
        evidence_pos = operational_transport_text.find("$evidence=Load-Evidence")
        if selftest_pos < 0 or evidence_pos < 0 or selftest_pos > evidence_pos:
            issues.append("A1_OPERATIONAL_SELFTEST_REQUIRES_EVIDENCE")
        operational_collisions = _powershell_parameter_assignment_collisions(operational_transport_text)
        if operational_collisions:
            issues.append(
                "A1_OPERATIONAL_PARAMETER_ASSIGNMENT_COLLISION:"
                + ",".join(sorted(operational_collisions))
            )
    else:
        issues.append("A1_OPERATIONAL_TRANSPORT_MISSING")

    tool_policy_path = root / "docs" / "operations" / "autonomy" / "CODEX_DESKTOP_TOOL_SURFACE_POLICY.json"
    if tool_policy_path.is_file():
        try:
            tool_policy = _read_json(tool_policy_path)
            if tool_policy.get("schema_version") != "SER-CODEX-DESKTOP-TOOL-SURFACE-2":
                issues.append("DESKTOP_TOOL_SURFACE_POLICY_SCHEMA")
            if tool_policy.get("controller_runtime_status") != "UNQUALIFIED_AFTER_REPEATED_BACKEND_REACH":
                issues.append("DESKTOP_TOOL_SURFACE_POLICY_RUNTIME_STATUS")
            enforcement = tool_policy.get("enforcement") or {}
            if (
                enforcement.get("matcher") != EXTERNAL_SURFACE_MATCHER
                or enforcement.get("policy") != "DENY_EXTERNAL_SURFACES_ALLOW_INTERNAL_NODE_REPL"
            ):
                issues.append("DESKTOP_TOOL_SURFACE_POLICY_ENFORCEMENT")
            cq_rules = tool_policy.get("cq_rules") or {}
            if cq_rules.get("builtin_browser_presence_alone_blocks") is not False:
                issues.append("DESKTOP_TOOL_SURFACE_POLICY_PRESENCE_RULE")
            if cq_rules.get("project_hook_trust_required") is not True:
                issues.append("DESKTOP_TOOL_SURFACE_POLICY_HOOK_TRUST")
            if cq_rules.get("dynamic_client_hook_aliases_required") is not True:
                issues.append("DESKTOP_TOOL_SURFACE_POLICY_DYNAMIC_ALIAS_REQUIREMENT")
            if enforcement.get("dynamic_hook_name_prefixes") != ["codex_app", "cua_repl", "codex_tui"]:
                issues.append("DESKTOP_TOOL_SURFACE_POLICY_DYNAMIC_ALIAS_BINDING")
            for sample in (
                "mcp__codex_app__get_usage_limits",
                "codex_appget_usage_limits",
                "codex_app__get_usage_limits",
                "mcp__cua_repl.js",
                "cua_repljs",
                "codex_tuilist_threads",
            ):
                if re.fullmatch(EXTERNAL_SURFACE_MATCHER, sample) is None:
                    issues.append("DESKTOP_TOOL_SURFACE_POLICY_DYNAMIC_ALIAS_NOT_MATCHED:" + sample)
            classes = tool_policy.get("presence_classes") or []
            serialized_classes = json.dumps(classes)
            if "INTERNAL_CODE_MODE_CONTROL" not in serialized_classes or "mcp__node_repl__*" not in serialized_classes:
                issues.append("DESKTOP_TOOL_SURFACE_POLICY_NODE_REPL_CLASS")
        except Exception as exc:
            issues.append("DESKTOP_TOOL_SURFACE_POLICY_UNREADABLE:" + type(exc).__name__)
    else:
        issues.append("DESKTOP_TOOL_SURFACE_POLICY_MISSING")

    cli_tool_policy_path = root / "docs" / "operations" / "autonomy" / "CODEX_CLI_TOOL_SURFACE_POLICY.json"
    if cli_tool_policy_path.is_file():
        try:
            cli_tool_policy = _read_json(cli_tool_policy_path)
            if cli_tool_policy.get("schema_version") != "SER-CODEX-CLI-TOOL-SURFACE-1":
                issues.append("CLI_TOOL_SURFACE_POLICY_SCHEMA")
            if cli_tool_policy.get("canonical_runtime") != "CODEX_CLI_WINDOWS_TUI":
                issues.append("CLI_TOOL_SURFACE_POLICY_RUNTIME")
            cli_enforcement = cli_tool_policy.get("enforcement") or {}
            if cli_enforcement.get("matcher") != EXTERNAL_SURFACE_MATCHER:
                issues.append("CLI_TOOL_SURFACE_POLICY_MATCHER")
            cli_rules = cli_tool_policy.get("cq_rules") or {}
            if cli_rules.get("desktop_client_surface_presence_blocks") is not True:
                issues.append("CLI_TOOL_SURFACE_POLICY_DESKTOP_PRESENCE")
            if cli_rules.get("no_probe_is_valid_when_no_probeable_forbidden_surface_is_loaded") is not True:
                issues.append("CLI_TOOL_SURFACE_POLICY_ABSENCE_RULE")
            if cli_rules.get("probe_retry_count") != 0:
                issues.append("CLI_TOOL_SURFACE_POLICY_RETRY")
        except Exception as exc:
            issues.append("CLI_TOOL_SURFACE_POLICY_UNREADABLE:" + type(exc).__name__)
    else:
        issues.append("CLI_TOOL_SURFACE_POLICY_MISSING")

    hooks_configured = False
    hooks_json_path = root / ".codex" / "hooks.json"
    if hooks_json_path.exists():
        issues.append("HOOK_JSON_DUPLICATE_SOURCE_FORBIDDEN")
    try:
        hooks = cfg.get("hooks") or {}
        pre = hooks.get("PreToolUse") or []
        post = hooks.get("PostToolUse") or []
        if not isinstance(hooks, dict) or not pre or not post:
            issues.append("HOOK_CONFIG_MISSING_PRE_OR_POST")
        else:
            hooks_configured = True
        serialized = json.dumps(hooks)
        if (
            "pre_scope_guard" not in serialized
            or "post_scope_guard" not in serialized
            or "external_surface_guard" not in serialized
            or EXTERNAL_SURFACE_MATCHER not in serialized
        ):
            issues.append("HOOK_CONFIG_INVALID")
        external_matchers = [
            str(group.get("matcher") or "")
            for group in pre
            if any(
                "external_surface_guard" in json.dumps(hook)
                for hook in (group.get("hooks") or [])
            )
        ]
        if external_matchers != [EXTERNAL_SURFACE_MATCHER]:
            issues.append("HOOK_EXTERNAL_SURFACE_MATCHER_MISMATCH")
        for sample in ("codex_appget_usage_limits", "cua_repljs"):
            if not external_matchers or re.fullmatch(external_matchers[0], sample) is None:
                issues.append("HOOK_DYNAMIC_CLIENT_ALIAS_NOT_MATCHED:" + sample)

        guard_ps_path = root / ".codex" / "hooks" / "external_surface_guard.ps1"
        guard_py_path = root / ".codex" / "hooks" / "external_surface_guard.py"
        if guard_ps_path.is_file() and guard_py_path.is_file():
            guard_ps_text = guard_ps_path.read_text(encoding="utf-8")
            guard_py_text = guard_py_path.read_text(encoding="utf-8")
            for token in ("codex_app", "cua_repl", "codex_tui", "codex_appget_usage_limits"):
                if token not in guard_ps_text or token not in guard_py_text:
                    issues.append("HOOK_EXTERNAL_SURFACE_GUARD_DYNAMIC_ALIAS_MISSING:" + token)

        for group in pre:
            for hook in group.get("hooks") or []:
                windows_command = str(
                    hook.get("commandWindows")
                    or hook.get("command_windows")
                    or ""
                )
                if ".codex\\\\hooks\\\\external_surface_guard.ps1" in windows_command:
                    issues.append("HOOK_WINDOWS_EXTERNAL_SURFACE_PATH_DOUBLE_SEPARATOR")
    except Exception as exc:
        issues.append("HOOK_CONFIG_UNREADABLE:" + type(exc).__name__)

    agents_md = root / "AGENTS.md"
    if agents_md.is_file():
        text = agents_md.read_text(encoding="utf-8")
        if "CODEX_AUTONOMOUS_PROTOCOL.md" not in text or "Autonomous Controller Mode" not in text:
            issues.append("AGENTS_ADAPTER_BINDING")
    else:
        issues.append("AGENTS_MD_MISSING")

    adr_index = root / "docs" / "decisions" / "README.md"
    if adr_index.is_file():
        text = adr_index.read_text(encoding="utf-8")
        if "ADR-0024-codex-autonomous-controller.md" not in text:
            issues.append("ADR_INDEX_BINDING")
    else:
        issues.append("ADR_INDEX_MISSING")

    return {
        "schema_version": "SER-CODEX-AUTONOMY-VALIDATION-21",
        "status": "PASS" if not issues else "FAIL",
        "issues": sorted(set(issues)),
        "custom_agents": len(EXPECTED_AGENTS),
        "write_capable_agents": write_capable,
        "max_concurrent_threads_per_session": max_threads,
        "root_permissions": cfg.get("default_permissions"),
        "executor_permissions": A1_PROFILE,
        "direct_a1_network": False,
        "direct_git_metadata_write": False,
        "hooks_configured": hooks_configured,
        "cli_windows_cq_contract": cli_cq_path.is_file(),
        "cli_host_preflight": cli_preflight_path.is_file(),
        "desktop_windows_cq_contract": desktop_cq_path.is_file(),
        "desktop_host_preflight": desktop_preflight_path.is_file(),
        "desktop_controller_runtime": "UNQUALIFIED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("CODEX_AUTONOMY = " + result["status"])
        for issue in result["issues"]:
            print("FAIL " + issue)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
