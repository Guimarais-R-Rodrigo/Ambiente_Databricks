#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_AGENTS = {
    "explorer": ("explorer.toml", "read-only"),
    "executor": ("executor.toml", "workspace-write"),
    "domain-auditor": ("domain-auditor.toml", "read-only"),
    "evidence-auditor": ("evidence-auditor.toml", "read-only"),
    "architecture-auditor": ("architecture-auditor.toml", "read-only"),
}


def _read_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_envelope_data(
    envelope: dict[str, Any],
    *,
    max_threads: int,
) -> list[str]:
    issues: list[str] = []
    if envelope.get("schema_version") != "SER-AUTONOMY-ENVELOPE-1":
        issues.append("ENVELOPE_SCHEMA")

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

    return issues


def validate(root: Path = ROOT) -> dict[str, Any]:
    issues: list[str] = []
    config_path = root / ".codex" / "config.toml"
    try:
        cfg = _read_toml(config_path)
    except Exception as exc:
        return {
            "schema_version": "SER-CODEX-AUTONOMY-VALIDATION-1",
            "status": "FAIL",
            "issues": ["CONFIG_UNREADABLE:" + type(exc).__name__],
        }

    if cfg.get("model") != "gpt-6-astra":
        issues.append("ROOT_MODEL_NOT_ASTRA")
    if cfg.get("model_reasoning_effort") != "max":
        issues.append("ROOT_REASONING_NOT_MAX")
    if cfg.get("sandbox_mode") != "workspace-write":
        issues.append("ROOT_SANDBOX")
    if cfg.get("approval_policy") != "on-request":
        issues.append("ROOT_APPROVAL_POLICY")
    if cfg.get("approvals_reviewer") != "user":
        issues.append("ROOT_APPROVAL_REVIEWER")

    features = cfg.get("features") or {}
    if features.get("multi_agent") is not True:
        issues.append("MULTI_AGENT_NOT_ENABLED")
    if features.get("goals") is not True:
        issues.append("GOALS_NOT_ENABLED")

    agents_cfg = cfg.get("agents") or {}
    if agents_cfg.get("enabled") is not True:
        issues.append("AGENTS_NOT_ENABLED")

    max_threads = agents_cfg.get("max_concurrent_threads_per_session")
    if max_threads != 5:
        issues.append("THREAD_LIMIT")
        max_threads = max_threads if isinstance(max_threads, int) and max_threads > 0 else 1

    if agents_cfg.get("default_subagent_model") != "gpt-6-sol":
        issues.append("DEFAULT_SUBAGENT_MODEL")
    if agents_cfg.get("default_subagent_reasoning_effort") != "high":
        issues.append("DEFAULT_SUBAGENT_EFFORT")

    roles = {k: v for k, v in agents_cfg.items() if isinstance(v, dict)}
    if set(roles) != set(EXPECTED_AGENTS):
        issues.append("ROLE_SET")

    write_capable = 0
    for role, (file_name, sandbox) in EXPECTED_AGENTS.items():
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
        if data.get("sandbox_mode") != sandbox:
            issues.append("AGENT_SANDBOX:" + role)
        if data.get("sandbox_mode") == "danger-full-access":
            issues.append("DANGER_FULL_ACCESS:" + role)
        if data.get("sandbox_mode") == "workspace-write":
            write_capable += 1
        if (data.get("agents") or {}).get("enabled") is not False:
            issues.append("SUBAGENT_NESTING_NOT_DISABLED:" + role)

    if write_capable != 1:
        issues.append("WRITE_CAPABLE_AGENT_COUNT")

    envelope_path = root / "docs" / "operations" / "autonomy" / "B1_AUTONOMY_ENVELOPE.json"
    try:
        envelope = _read_json(envelope_path)
        issues.extend(validate_envelope_data(envelope, max_threads=max_threads))
    except Exception as exc:
        issues.append("ENVELOPE_UNREADABLE:" + type(exc).__name__)

    required_paths = [
        "docs/decisions/ADR-0024-codex-autonomous-controller.md",
        "docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md",
        "docs/operations/CODEX_AUTONOMOUS_RETROSPECTIVE.md",
        "docs/operations/CODEX_AUTONOMOUS_START_PROMPT.md",
        "docs/operations/autonomy/autonomy-envelope.schema.json",
        ".agents/skills/ser-autonomous-controller/SKILL.md",
    ]
    for rel in required_paths:
        if not (root / rel).is_file():
            issues.append("REQUIRED_PATH_MISSING:" + rel)

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
        "schema_version": "SER-CODEX-AUTONOMY-VALIDATION-1",
        "status": "PASS" if not issues else "FAIL",
        "issues": sorted(set(issues)),
        "custom_agents": len(EXPECTED_AGENTS),
        "write_capable_agents": write_capable,
        "max_concurrent_threads_per_session": max_threads,
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
