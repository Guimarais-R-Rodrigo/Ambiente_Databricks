#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENVELOPE = ROOT / "docs" / "operations" / "autonomy" / "B1_AUTONOMY_ENVELOPE.json"
STATE_PATH = "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTHORING_STATE.json"

ALLOWED_A1_CONTROLLER_STATE_FIELDS = {
    "runtime_validation",
    "effective_config_observation",
    "first_material_controller_session",
}
HUMAN_GATE_KEYS = {"G7_PROMOTION_PROPOSAL", "G8_POST_POLICY", "G9_INTEGRATION"}
TERMINAL_STAGE_TOKENS = ("PROMOT", "READY", "MERGE", "COMPLETE")


def _patterns() -> tuple[list[str], list[str], list[str]]:
    payload = json.loads(ENVELOPE.read_text(encoding="utf-8"))
    scope = payload["repo_scope"]
    return (
        list(scope["write_roots"]),
        list(scope["protected_roots"]),
        list(scope["shared_roots_requiring_human_gate"]),
    )


def _matches(path: str, patterns: list[str]) -> bool:
    normalized = path.replace("\\", "/")
    return any(fnmatch.fnmatchcase(normalized, pattern) for pattern in patterns)


def classify_path(path: str) -> str:
    write_roots, protected, shared = _patterns()
    if _matches(path, protected):
        return "PROTECTED"
    if _matches(path, shared):
        return "HUMAN_GATE_REQUIRED"
    if _matches(path, write_roots):
        return "ALLOWED_A1"
    return "OUTSIDE_A1"


def _run_git(argv: list[str], *, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *argv],
        cwd=ROOT,
        capture_output=True,
        text=text,
        check=False,
    )


def _diff_entries(base: str, head: str) -> list[dict[str, Any]]:
    proc = _run_git([
        "diff",
        "--raw",
        "--no-abbrev",
        "-z",
        "--find-renames",
        "--find-copies",
        f"{base}..{head}",
    ])
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace")
        stdout = proc.stdout.decode("utf-8", errors="replace")
        raise RuntimeError("GIT_DIFF_FAILED:" + (stderr.strip() or stdout.strip()))

    parts = proc.stdout.split(b"\0")
    entries: list[dict[str, Any]] = []
    index = 0
    while index < len(parts):
        raw_header = parts[index]
        index += 1
        if not raw_header:
            break
        header = raw_header.decode("utf-8", errors="strict")
        if not header.startswith(":"):
            raise RuntimeError("GIT_RAW_DIFF_PARSE_FAILED:" + header)
        fields = header[1:].split()
        if len(fields) != 5:
            raise RuntimeError("GIT_RAW_DIFF_HEADER_FIELDS:" + header)
        old_mode, new_mode, old_sha, new_sha, status = fields
        if index >= len(parts):
            raise RuntimeError("GIT_RAW_DIFF_PATH_MISSING")
        source = parts[index].decode("utf-8", errors="strict")
        index += 1
        destination = None
        if status[:1] in {"R", "C"}:
            if index >= len(parts):
                raise RuntimeError("GIT_RAW_DIFF_DESTINATION_MISSING")
            destination = parts[index].decode("utf-8", errors="strict")
            index += 1
        entries.append({
            "status": status,
            "old_mode": old_mode,
            "new_mode": new_mode,
            "old_sha": old_sha,
            "new_sha": new_sha,
            "source": source,
            "destination": destination,
        })
    return entries


def _entry_rows(entry: dict[str, Any]) -> list[dict[str, Any]]:
    code = entry["status"][:1]
    source = entry["source"]
    destination = entry["destination"]
    rows: list[dict[str, Any]] = []

    if code == "R":
        rows.append({
            "path": source,
            "role": "rename_source",
            "operation": entry["status"],
            "classification": classify_path(source),
            "old_mode": entry["old_mode"],
            "new_mode": "000000",
            "enforced": True,
        })
        rows.append({
            "path": destination,
            "role": "rename_destination",
            "operation": entry["status"],
            "classification": classify_path(destination),
            "old_mode": "000000",
            "new_mode": entry["new_mode"],
            "enforced": True,
        })
    elif code == "C":
        rows.append({
            "path": source,
            "role": "copy_source",
            "operation": entry["status"],
            "classification": classify_path(source),
            "old_mode": entry["old_mode"],
            "new_mode": entry["old_mode"],
            "enforced": False,
        })
        rows.append({
            "path": destination,
            "role": "copy_destination",
            "operation": entry["status"],
            "classification": classify_path(destination),
            "old_mode": "000000",
            "new_mode": entry["new_mode"],
            "enforced": True,
        })
    else:
        rows.append({
            "path": source,
            "role": "path",
            "operation": entry["status"],
            "classification": classify_path(source),
            "old_mode": entry["old_mode"],
            "new_mode": entry["new_mode"],
            "enforced": True,
        })
    return rows


def _json_at(ref: str, path: str) -> dict[str, Any] | None:
    proc = _run_git(["show", f"{ref}:{path}"], text=True)
    if proc.returncode != 0:
        return None
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"STATE_JSON_INVALID:{ref}:{exc.msg}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"STATE_JSON_NOT_OBJECT:{ref}")
    return payload


def _nested(payload: dict[str, Any], *path: str) -> Any:
    current: Any = payload
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _passish(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("PASS")


def _authorized(value: Any) -> bool:
    return isinstance(value, str) and (value.startswith("AUTHORIZED") or value == "PASS")


def _blocker_has_evidence(blocker: str, candidate: dict[str, Any]) -> bool:
    if blocker == "AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION":
        return (
            _nested(candidate, "autonomous_controller", "runtime_validation") == "PASS"
            and _nested(candidate, "autonomous_controller", "effective_config_observation") == "PASS"
        )
    if blocker == "G6_SER05_RECOVERY_LOCAL_QUALIFICATION":
        return (
            _passish(_nested(candidate, "g6", "ser05_residual_recovery", "local_validation"))
            and _passish(_nested(candidate, "g6", "ser05_residual_recovery", "unit_tests"))
        )
    if blocker == "G6_PARTIAL_REMOTE_STATE_RECONCILIATION":
        return _passish(_nested(candidate, "g6", "ser05_residual_recovery", "remote_reconciliation"))
    if blocker == "G6_SER05_RESIDUAL_WRITE_AUTHORIZATION":
        recovery = _nested(candidate, "g6", "ser05_residual_recovery")
        return (
            isinstance(recovery, dict)
            and _authorized(recovery.get("remote_write"))
            and isinstance(recovery.get("authorization_ref"), str)
            and bool(recovery["authorization_ref"].strip())
        )
    if blocker == "G6_FREE_PROBES":
        return _passish(_nested(candidate, "g6", "remaining_external", "free_probe_run", "state"))
    if blocker == "G6_GENIE":
        return _passish(_nested(candidate, "g6", "remaining_external", "genie", "state"))
    if blocker == "G6_EXTERNAL_EVIDENCE_VERIFICATION":
        return _passish(_nested(candidate, "g6", "external_execution_result"))
    return False


def validate_state_transition(base_state: dict[str, Any], candidate_state: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    for key in ("schema_version", "base_commit", "policy_changed"):
        if base_state.get(key) != candidate_state.get(key):
            issues.append("STATE_A1_IMMUTABLE:" + key)

    base_gates = base_state.get("gates") or {}
    candidate_gates = candidate_state.get("gates") or {}
    for key in sorted(HUMAN_GATE_KEYS):
        if base_gates.get(key) != candidate_gates.get(key):
            issues.append("STATE_HUMAN_GATE_MUTATION:gates." + key)

    base_controller = base_state.get("autonomous_controller") or {}
    candidate_controller = candidate_state.get("autonomous_controller") or {}
    for key in sorted(set(base_controller) | set(candidate_controller)):
        if key in ALLOWED_A1_CONTROLLER_STATE_FIELDS:
            continue
        if base_controller.get(key) != candidate_controller.get(key):
            issues.append("STATE_CONTROLLER_AUTHORITY_MUTATION:autonomous_controller." + key)

    base_blockers = base_state.get("blocked_by")
    candidate_blockers = candidate_state.get("blocked_by")
    if not isinstance(base_blockers, list) or not all(isinstance(x, str) for x in base_blockers):
        issues.append("STATE_BASE_BLOCKERS_INVALID")
        base_blockers = []
    if not isinstance(candidate_blockers, list) or not all(isinstance(x, str) for x in candidate_blockers):
        issues.append("STATE_CANDIDATE_BLOCKERS_INVALID")
        candidate_blockers = []
    if len(set(candidate_blockers)) != len(candidate_blockers):
        issues.append("STATE_CANDIDATE_BLOCKERS_DUPLICATE")

    removed = sorted(set(base_blockers) - set(candidate_blockers))
    for blocker in removed:
        if not _blocker_has_evidence(blocker, candidate_state):
            issues.append("STATE_BLOCKER_REMOVAL_UNPROVEN:" + blocker)

    stage = candidate_state.get("stage")
    if base_state.get("stage") != stage and isinstance(stage, str):
        upper = stage.upper()
        if any(token in upper for token in TERMINAL_STAGE_TOKENS):
            issues.append("STATE_TERMINAL_STAGE_REQUIRES_HUMAN_GATE:" + stage)

    if candidate_state.get("launchable") is True and candidate_blockers:
        issues.append("STATE_LAUNCHABLE_WITH_BLOCKERS")

    return sorted(set(issues))


def check_delta(base: str, head: str) -> dict[str, Any]:
    entries = _diff_entries(base, head)
    rows: list[dict[str, Any]] = []
    for entry in entries:
        rows.extend(_entry_rows(entry))

    violations = [
        row for row in rows
        if row["enforced"] and row["classification"] != "ALLOWED_A1"
    ]
    symlink_rows = [
        row for row in rows
        if row["old_mode"] == "120000" or row["new_mode"] == "120000"
    ]
    for row in symlink_rows:
        violations.append({**row, "classification": "SYMLINK_NOT_ALLOWED"})

    state_transition_issues: list[str] = []
    if any(row["path"] == STATE_PATH for row in rows):
        base_state = _json_at(base, STATE_PATH)
        candidate_state = _json_at(head, STATE_PATH)
        if base_state is None or candidate_state is None:
            state_transition_issues.append("STATE_SOURCE_MISSING_IN_DELTA")
        else:
            state_transition_issues.extend(validate_state_transition(base_state, candidate_state))

    status = "PASS" if not violations and not state_transition_issues else "FAIL"
    return {
        "schema_version": "SER-CODEX-AUTONOMY-DELTA-2",
        "base": base,
        "head": head,
        "status": status,
        "files": rows,
        "violations": violations,
        "state_transition_issues": state_transition_issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()
    result = check_delta(args.base, args.head)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
