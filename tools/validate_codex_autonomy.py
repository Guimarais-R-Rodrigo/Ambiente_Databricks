#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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
A0_WINDOWS_SCRATCH = r"~\\codex-scratch\\Ambiente_Databricks"
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
        if (a0.get("network") or {}).get("enabled") is not False:
            issues.append("A0_NETWORK_MUST_BE_DISABLED")

    if not isinstance(a1, dict):
        issues.append("A1_PERMISSION_PROFILE_MISSING")
        return issues

    filesystem = a1.get("filesystem") or {}
    workspace = filesystem.get(":workspace_roots") or {}
    if filesystem.get(":root") != "read":
        issues.append("A1_WINDOWS_ROOT_READ_REQUIRED")
    if filesystem.get(":minimal") != "read":
        issues.append("A1_MINIMAL_READ_REQUIRED")
    if filesystem.get(":tmpdir") != "write":
        issues.append("A1_TMPDIR_WRITE_REQUIRED")
    if filesystem.get(":slash_tmp") != "write":
        issues.append("A1_SLASH_TMP_WRITE_REQUIRED")
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
            "schema_version": "SER-CODEX-AUTONOMY-VALIDATION-7",
            "status": "FAIL",
            "issues": ["CONFIG_UNREADABLE:" + type(exc).__name__],
        }

    if cfg.get("model") != "gpt-6-astra":
        issues.append("ROOT_MODEL_NOT_ASTRA")
    if cfg.get("model_reasoning_effort") != "high":
        issues.append("ROOT_REASONING_NOT_HIGH")

    features = cfg.get("features") or {}
    if features.get("apps") is not False:
        issues.append("APPS_MUST_BE_DISABLED")
    if features.get("remote_plugin") is not False:
        issues.append("REMOTE_PLUGIN_MUST_BE_DISABLED")
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
        ".codex/hooks.json",
        ".codex/hooks/pre_scope_guard.py",
        ".codex/hooks/post_scope_guard.py",
        ".codex/hooks/pre_scope_guard.ps1",
        ".codex/hooks/post_scope_guard.ps1",
        "tools/requirements-codex-autonomy.txt",
        "tools/codex_desktop_cq_host_preflight.ps1",
        ".codex/rules/a1_git_transport.rules",
        ".codex/transport/a1_git_transport.ps1",
        "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl",
    ]
    for rel in required_paths:
        if not (root / rel).is_file():
            issues.append("REQUIRED_PATH_MISSING:" + rel)

    desktop_cq_path = root / "docs" / "operations" / "CODEX_DESKTOP_WINDOWS_CQ.md"
    desktop_preflight_path = root / "tools" / "codex_desktop_cq_host_preflight.ps1"
    if desktop_cq_path.is_file():
        desktop_text = desktop_cq_path.read_text(encoding="utf-8")
        required_desktop_tokens = (
            "CODEX_DESKTOP_WINDOWS",
            "CQ_HOST_PREFLIGHT.json",
            "DEFERRED_TO_EXTERNAL_ADJUDICATION",
            "NOT_OBSERVABLE_DESKTOP",
            "INTERNAL_CLIENT_CONTROL_PLANE",
            "EXTERNAL_MUTATING_PLUGIN_SURFACE",
        )
        if any(token not in desktop_text for token in required_desktop_tokens):
            issues.append("DESKTOP_WINDOWS_CQ_CONTRACT_INVALID")
    if desktop_preflight_path.is_file():
        preflight_text = desktop_preflight_path.read_text(encoding="utf-8")
        required_preflight_tokens = (
            "git fetch origin $ExpectedBranch",
            "CQ_HOST_PREFLIGHT.json",
            "jsonschema",
            "config_sha256",
            "python_version",
            "final_clean",
        )
        if any(token not in preflight_text for token in required_preflight_tokens):
            issues.append("DESKTOP_WINDOWS_HOST_PREFLIGHT_INVALID")
        if "pip install" in preflight_text or "python -m pip" in preflight_text:
            issues.append("DESKTOP_WINDOWS_HOST_PREFLIGHT_INSTALL_FORBIDDEN")

    rule_path = root / ".codex" / "rules" / "a1_git_transport.rules"
    transport_path = root / ".codex" / "transport" / "a1_git_transport.ps1"
    if rule_path.is_file():
        rule_text = rule_path.read_text(encoding="utf-8")
        if 'decision = "prompt"' not in rule_text or "a1_git_transport.ps1" not in rule_text:
            issues.append("A1_GIT_RULE_INVALID")
    if transport_path.is_file():
        transport_text = transport_path.read_text(encoding="utf-8")
        required_transport_tokens = (
            'ser/B1-ser03-ser05-authoring',
            'tools/check_codex_autonomy_delta.py --worktree',
            'tools/check_codex_autonomy_delta.py --index',
            'HEAD:refs/heads/$ExpectedBranch',
            'A1_GIT_TRANSPORT_ENVELOPE_PATH_MISMATCH',
        )
        if any(token not in transport_text for token in required_transport_tokens):
            issues.append("A1_GIT_TRANSPORT_INVALID")
        if "--force" in transport_text:
            issues.append("A1_GIT_TRANSPORT_FORCE_FORBIDDEN")

    hooks_path = root / ".codex" / "hooks.json"
    if hooks_path.is_file():
        try:
            hooks_payload = _read_json(hooks_path)
            hooks = hooks_payload.get("hooks") or {}
            pre = hooks.get("PreToolUse") or []
            post = hooks.get("PostToolUse") or []
            if not pre or not post:
                issues.append("HOOK_CONFIG_MISSING_PRE_OR_POST")
            serialized = json.dumps(hooks_payload)
            if "pre_scope_guard" not in serialized or "post_scope_guard" not in serialized:
                issues.append("HOOK_CONFIG_INVALID")
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
        "schema_version": "SER-CODEX-AUTONOMY-VALIDATION-7",
        "status": "PASS" if not issues else "FAIL",
        "issues": sorted(set(issues)),
        "custom_agents": len(EXPECTED_AGENTS),
        "write_capable_agents": write_capable,
        "max_concurrent_threads_per_session": max_threads,
        "root_permissions": cfg.get("default_permissions"),
        "executor_permissions": A1_PROFILE,
        "direct_a1_network": False,
        "direct_git_metadata_write": False,
        "hooks_configured": hooks_path.is_file(),
        "desktop_windows_cq_contract": desktop_cq_path.is_file(),
        "desktop_host_preflight": desktop_preflight_path.is_file(),
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
