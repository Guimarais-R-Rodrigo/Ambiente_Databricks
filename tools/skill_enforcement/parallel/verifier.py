from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from .contract import validate_campaign, validate_result
from .registry import RegistryError, resolve_command

_TERMINAL = {"PASS", "FAIL", "BLOCKED_DEPENDENCY", "BLOCKED_GLOBAL_STOP", "BLOCKED_RESOURCE", "BLOCKED_ENVIRONMENT", "NOT_APPLICABLE"}
_EXECUTED = {"PASS", "FAIL"}
_AUDITOR_ROLES = {"domain_auditor", "evidence_auditor"}


def _canonical_first_failure(results: Mapping[str, Mapping[str, Any]]) -> str | None:
    failures = [
        (row.get("wave_index"), task_id)
        for task_id, row in results.items()
        if isinstance(row, Mapping) and row.get("status") == "FAIL" and type(row.get("wave_index")) is int
    ]
    return min(failures)[1] if failures else None


def _record_log_issues(task_id: str, command_id: str, row: Mapping[str, Any], evidence_root: Path | None) -> list[str]:
    issues: list[str] = []
    try:
        expected_argv, _ = resolve_command(command_id)
    except RegistryError as exc:
        return [f"{task_id}:COMMAND_REGISTRY_ERROR:{command_id}:{exc}"]
    if row.get("name") != command_id.replace(":", "_"):
        issues.append(f"{task_id}:COMMAND_NAME_BINDING_MISMATCH:{command_id}")
    if row.get("argv") != expected_argv:
        issues.append(f"{task_id}:COMMAND_ARGV_BINDING_MISMATCH:{command_id}")
    for key in ("stdout_sha256", "stderr_sha256"):
        value = row.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            issues.append(f"{task_id}:COMMAND_HASH_INVALID:{command_id}:{key}")
    if evidence_root is not None:
        prefix = evidence_root / task_id / command_id.replace(":", "_")
        for suffix, key in ((".stdout.txt", "stdout_sha256"), (".stderr.txt", "stderr_sha256")):
            path = prefix.with_suffix(suffix)
            if not path.is_file():
                issues.append(f"{task_id}:COMMAND_LOG_MISSING:{command_id}:{suffix}")
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != row.get(key):
                issues.append(f"{task_id}:COMMAND_LOG_HASH_MISMATCH:{command_id}:{suffix}")
    return issues


def verify_campaign_run(
    campaign: Mapping[str, Any],
    results: Mapping[str, Mapping[str, Any]],
    evidence_root: Path | None = None,
) -> dict[str, Any]:
    issues = list(validate_campaign(campaign))
    tasks = {t["task_id"]: t for t in campaign.get("tasks", []) if isinstance(t, Mapping) and "task_id" in t}
    if set(results) != set(tasks):
        issues.append("RESULT_SET_MISMATCH")

    first_failure = _canonical_first_failure(results)
    global_failures = sorted(
        (
            ((results.get(task_id) or {}).get("wave_index"), task_id)
            for task_id, task in tasks.items()
            if task.get("failure_scope") == "GLOBAL_CAMPAIGN" and (results.get(task_id) or {}).get("status") == "FAIL"
        ),
        key=lambda x: (x[0], x[1]),
    )
    first_global = global_failures[0] if global_failures else None
    executed_by_wave: dict[int, list[str]] = {}

    for task_id, task in tasks.items():
        result = results.get(task_id)
        if result is None:
            continue
        for issue in validate_result(result):
            issues.append(f"{task_id}:{issue}")

        status = result.get("status")
        if status not in _TERMINAL:
            issues.append(f"{task_id}:RESULT_NOT_TERMINAL")
        if result.get("task_id") != task_id:
            issues.append(f"{task_id}:TASK_ID_BINDING_MISMATCH")
        if task.get("candidate_sha") != campaign.get("candidate_sha"):
            issues.append(f"{task_id}:TASK_CANDIDATE_BINDING_MISMATCH")
        if result.get("candidate_sha") != campaign.get("candidate_sha"):
            issues.append(f"{task_id}:CANDIDATE_BINDING_MISMATCH")
        if result.get("effect_state") != task.get("expected_effect"):
            issues.append(f"{task_id}:EFFECT_BINDING_MISMATCH")
        if result.get("protected_fingerprint_before") != result.get("protected_fingerprint_after"):
            issues.append(f"{task_id}:PROTECTED_PATH_MUTATED")
        if result.get("first_failure") != first_failure:
            issues.append(f"{task_id}:FIRST_FAILURE_INCONSISTENT")

        records = result.get("command_records") or []
        command_ids = task.get("command_ids") or []
        if status in _EXECUTED:
            wave = result.get("wave_index")
            if type(wave) is int:
                executed_by_wave.setdefault(wave, []).append(task_id)
            if status == "PASS" and len(records) != len(command_ids):
                issues.append(f"{task_id}:PASS_COMMAND_COUNT_MISMATCH")
            if status == "FAIL" and (not records or len(records) > len(command_ids)):
                issues.append(f"{task_id}:FAIL_COMMAND_COUNT_INVALID")
            for idx, row in enumerate(records):
                if idx >= len(command_ids):
                    issues.append(f"{task_id}:UNDECLARED_COMMAND_RECORD")
                    continue
                if not isinstance(row, Mapping):
                    issues.append(f"{task_id}:COMMAND_RECORD_INVALID")
                    continue
                issues.extend(_record_log_issues(task_id, command_ids[idx], row, evidence_root))
            if status == "PASS":
                if result.get("issues"):
                    issues.append(f"{task_id}:PASS_WITH_ISSUES")
                for row in records:
                    if not isinstance(row, Mapping) or row.get("exit_code") != 0 or row.get("command_started") is not True or row.get("cleanup") not in {"COMPLETE", "COMPLETE_ALREADY_EXITED"}:
                        issues.append(f"{task_id}:PASS_COMMAND_INVALID")
            if status == "FAIL" and not any(isinstance(row, Mapping) and row.get("exit_code") != 0 for row in records):
                issues.append(f"{task_id}:FAIL_WITHOUT_FAILED_COMMAND")
        elif records:
            issues.append(f"{task_id}:BLOCKED_OR_NA_TASK_EXECUTED")

        dep_states = {d: (results.get(d) or {}).get("status") for d in task.get("depends_on") or []}
        failed_deps = {d for d, state in dep_states.items() if state not in {"PASS", "NOT_APPLICABLE"}}
        if status in _EXECUTED:
            if failed_deps:
                issues.append(f"{task_id}:EXECUTED_WITH_UNSATISFIED_DEPENDENCY")
            for dep in task.get("depends_on") or []:
                dep_result = results.get(dep) or {}
                if type(dep_result.get("wave_index")) is int and type(result.get("wave_index")) is int and dep_result["wave_index"] >= result["wave_index"]:
                    issues.append(f"{task_id}:DEPENDENCY_WAVE_ORDER_INVALID:{dep}")
        if status == "BLOCKED_DEPENDENCY":
            blockers = set(result.get("blocked_by") or [])
            if blockers != failed_deps or not blockers:
                issues.append(f"{task_id}:BLOCKED_BY_MISMATCH")
        elif failed_deps and status != "BLOCKED_GLOBAL_STOP":
            issues.append(f"{task_id}:DEPENDENCY_FAILURE_NOT_BLOCKED")

        if first_global is not None:
            global_wave, global_id = first_global
            wave = result.get("wave_index")
            if type(wave) is int and wave > global_wave:
                if status != "BLOCKED_GLOBAL_STOP":
                    issues.append(f"{task_id}:GLOBAL_STOP_ESCAPE")
                elif (result.get("blocked_by") or []) != [global_id]:
                    issues.append(f"{task_id}:GLOBAL_STOP_BLOCKER_INVALID")
        if status == "BLOCKED_GLOBAL_STOP" and first_global is None:
            issues.append(f"{task_id}:GLOBAL_STOP_WITHOUT_GLOBAL_FAILURE")

    for wave, task_ids in executed_by_wave.items():
        if len(task_ids) > campaign.get("max_parallel", 0):
            issues.append(f"WAVE_{wave}:MAX_PARALLEL_EXCEEDED")
        keys = [tasks[t].get("exclusivity_key") for t in task_ids]
        if any(count > 1 for count in Counter(keys).values()):
            issues.append(f"WAVE_{wave}:EXCLUSIVITY_VIOLATION")
        auditors = sum(tasks[t].get("role") in _AUDITOR_ROLES for t in task_ids)
        if auditors > campaign.get("max_auditors", 0):
            issues.append(f"WAVE_{wave}:AUDITOR_LIMIT_EXCEEDED")
        resources = Counter(tasks[t].get("resource_class") for t in task_ids)
        for resource, count in resources.items():
            limit = (campaign.get("resource_limits") or {}).get(resource)
            if limit is not None and count > limit:
                issues.append(f"WAVE_{wave}:RESOURCE_LIMIT_EXCEEDED:{resource}")

    return {
        "valid": not issues,
        "issues": issues,
        "first_failure": first_failure,
        "global_failures": [task_id for _, task_id in global_failures],
        "verification_scope": "SER_PARALLEL_LOCAL_CAMPAIGN_INTEGRITY",
    }


def verify_bundle(root: Path) -> dict[str, Any]:
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.is_file():
        return {"valid": False, "issues": ["MANIFEST_MISSING"]}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"valid": False, "issues": ["MANIFEST_UNREADABLE:" + type(exc).__name__]}
    issues: list[str] = []
    expected = manifest.get("files")
    if manifest.get("schema_version") != "SER-PARALLEL-BUNDLE-2" or not isinstance(expected, list):
        return {"valid": False, "issues": ["MANIFEST_SCHEMA_INVALID"]}
    listed = set()
    for row in expected:
        if not isinstance(row, Mapping) or set(row) != {"path", "size", "sha256"} or not isinstance(row.get("path"), str):
            issues.append("MANIFEST_ROW_INVALID")
            continue
        rel = row["path"]
        if rel in listed or rel.startswith("/") or ".." in Path(rel).parts or rel == "MANIFEST.json":
            issues.append("MANIFEST_PATH_INVALID:" + rel)
            continue
        listed.add(rel)
        p = root / rel
        if not p.is_file():
            issues.append("FILE_MISSING:" + rel)
            continue
        data = p.read_bytes()
        if len(data) != row.get("size"):
            issues.append("SIZE_MISMATCH:" + rel)
        if hashlib.sha256(data).hexdigest() != row.get("sha256"):
            issues.append("HASH_MISMATCH:" + rel)
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p != manifest_path}
    if actual != listed:
        issues.append("MANIFEST_FILESET_MISMATCH")
    return {"valid": not issues, "issues": issues}


def verify_raw_share_binding(raw_root: Path, share_root: Path, binding_path: Path) -> dict[str, Any]:
    issues: list[str] = []
    try:
        binding = json.loads(binding_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"valid": False, "issues": ["RAW_SHARE_BINDING_UNREADABLE:" + type(exc).__name__]}
    required = {"schema_version", "raw_manifest_sha256", "share_manifest_sha256", "identities_are_distinct", "secret_scan"}
    if not isinstance(binding, Mapping) or set(binding) != required or binding.get("schema_version") != "SER-PARALLEL-RAW-SHARE-2":
        return {"valid": False, "issues": ["RAW_SHARE_BINDING_SCHEMA_INVALID"]}
    raw_manifest = raw_root / "MANIFEST.json"
    share_manifest = share_root / "MANIFEST.json"
    if not raw_manifest.is_file() or not share_manifest.is_file():
        return {"valid": False, "issues": ["RAW_SHARE_MANIFEST_MISSING"]}
    raw_bytes = raw_manifest.read_bytes()
    share_bytes = share_manifest.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != binding.get("raw_manifest_sha256"):
        issues.append("RAW_MANIFEST_BINDING_MISMATCH")
    if hashlib.sha256(share_bytes).hexdigest() != binding.get("share_manifest_sha256"):
        issues.append("SHARE_MANIFEST_BINDING_MISMATCH")
    if binding.get("identities_are_distinct") is not True or raw_bytes == share_bytes:
        issues.append("RAW_SHARE_IDENTITIES_NOT_DISTINCT")
    secret_scan = binding.get("secret_scan")
    if not isinstance(secret_scan, Mapping) or secret_scan.get("status") != "PASS" or secret_scan.get("findings") != []:
        issues.append("SHARE_SECRET_SCAN_NOT_PASS")
    raw_v = verify_bundle(raw_root)
    share_v = verify_bundle(share_root)
    if not raw_v["valid"]:
        issues.append("RAW_BUNDLE_INVALID")
    if not share_v["valid"]:
        issues.append("SHARE_BUNDLE_INVALID")
    return {"valid": not issues, "issues": issues, "raw": raw_v, "share": share_v}
