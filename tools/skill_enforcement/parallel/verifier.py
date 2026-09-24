from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from .contract import validate_campaign, validate_result
from .registry import RegistryError, command_template, resolve_command

_FINAL_STATUSES = {
    "PASS",
    "FAIL",
    "BLOCKED_DEPENDENCY",
    "BLOCKED_GLOBAL_STOP",
    "BLOCKED_RESOURCE",
    "BLOCKED_ENVIRONMENT",
    "NOT_APPLICABLE",
}
_EXECUTED_STATUSES = {"PASS", "FAIL"}
_AUDITOR_ROLES = {"domain_auditor", "evidence_auditor"}
_HEX64 = set("0123456789abcdef")


def _canonical_first_failure(results: Mapping[str, Mapping[str, Any]]) -> str | None:
    failures = [
        (row.get("wave_index"), task_id)
        for task_id, row in results.items()
        if isinstance(row, Mapping)
        and row.get("status") == "FAIL"
        and type(row.get("wave_index")) is int
    ]
    return min(failures)[1] if failures else None


def _canonical_global_stop(
    tasks: Mapping[str, Mapping[str, Any]],
    results: Mapping[str, Mapping[str, Any]],
) -> tuple[int, str] | None:
    failures = [
        (result.get("wave_index"), task_id)
        for task_id, task in tasks.items()
        if task.get("failure_scope") == "GLOBAL_CAMPAIGN"
        and isinstance((result := results.get(task_id)), Mapping)
        and result.get("status") == "FAIL"
        and type(result.get("wave_index")) is int
    ]
    return min(failures) if failures else None


def _is_hex64(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= _HEX64


def _verify_record_files(task_id: str, row: Mapping[str, Any], evidence_root: Path) -> list[str]:
    issues: list[str] = []
    name = row.get("name")
    if not isinstance(name, str) or not name or any(sep in name for sep in ("/", "\\")):
        return [f"{task_id}:COMMAND_RECORD_NAME_INVALID"]
    task_dir = evidence_root / task_id
    stdout_path = task_dir / f"{name}.stdout.txt"
    stderr_path = task_dir / f"{name}.stderr.txt"
    meta_path = task_dir / f"{name}.json"
    for label, path in (("STDOUT", stdout_path), ("STDERR", stderr_path), ("METADATA", meta_path)):
        if not path.is_file():
            issues.append(f"{task_id}:EVIDENCE_{label}_MISSING:{name}")
    if stdout_path.is_file():
        digest = hashlib.sha256(stdout_path.read_bytes()).hexdigest()
        if digest != row.get("stdout_sha256"):
            issues.append(f"{task_id}:STDOUT_HASH_MISMATCH:{name}")
    if stderr_path.is_file():
        digest = hashlib.sha256(stderr_path.read_bytes()).hexdigest()
        if digest != row.get("stderr_sha256"):
            issues.append(f"{task_id}:STDERR_HASH_MISMATCH:{name}")
    if meta_path.is_file():
        try:
            persisted = json.loads(meta_path.read_bytes().decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            issues.append(f"{task_id}:COMMAND_METADATA_UNREADABLE:{name}")
        else:
            if persisted != dict(row):
                issues.append(f"{task_id}:COMMAND_METADATA_BINDING_MISMATCH:{name}")
    return issues


def _verify_command_records(
    task_id: str,
    task: Mapping[str, Any],
    result: Mapping[str, Any],
    evidence_root: Path | None,
) -> list[str]:
    issues: list[str] = []
    records = result.get("command_records")
    if not isinstance(records, list):
        return [f"{task_id}:COMMAND_RECORDS_INVALID"]
    command_ids = task.get("command_ids") or []
    status = result.get("status")

    if status in _EXECUTED_STATUSES:
        if not records:
            issues.append(f"{task_id}:EXECUTED_WITHOUT_COMMAND_RECORD")
        if len(records) > len(command_ids):
            issues.append(f"{task_id}:COMMAND_COUNT_EXCEEDS_DECLARED")
        if status == "PASS" and len(records) != len(command_ids):
            issues.append(f"{task_id}:PASS_COMMAND_COUNT_MISMATCH")
    elif records:
        issues.append(f"{task_id}:NONEXECUTED_TASK_HAS_COMMAND_RECORDS")

    for idx, row in enumerate(records):
        if not isinstance(row, Mapping):
            issues.append(f"{task_id}:COMMAND_RECORD_INVALID:{idx}")
            continue
        if idx >= len(command_ids):
            continue
        expected_id = command_ids[idx]
        if row.get("command_id") != expected_id:
            issues.append(f"{task_id}:COMMAND_ID_BINDING_MISMATCH:{idx}")
        try:
            template = command_template(expected_id)
            resolved, _ = resolve_command(expected_id)
        except RegistryError as exc:
            issues.append(f"{task_id}:COMMAND_REGISTRY_INVALID:{expected_id}:{exc}")
            continue
        if row.get("argv_template") != template:
            issues.append(f"{task_id}:COMMAND_TEMPLATE_BINDING_MISMATCH:{expected_id}")
        if row.get("argv") != resolved:
            issues.append(f"{task_id}:COMMAND_ARGV_BINDING_MISMATCH:{expected_id}")
        expected_name = expected_id.replace(":", "_")
        if row.get("name") != expected_name:
            issues.append(f"{task_id}:COMMAND_NAME_BINDING_MISMATCH:{expected_id}")
        if not _is_hex64(row.get("stdout_sha256")) or not _is_hex64(row.get("stderr_sha256")):
            issues.append(f"{task_id}:COMMAND_LOG_HASH_INVALID:{expected_id}")
        if row.get("command_started") is not True:
            issues.append(f"{task_id}:COMMAND_NOT_STARTED:{expected_id}")
        if row.get("cleanup") not in {"COMPLETE", "COMPLETE_ALREADY_EXITED"}:
            issues.append(f"{task_id}:COMMAND_CLEANUP_INVALID:{expected_id}")
        if evidence_root is not None:
            issues.extend(_verify_record_files(task_id, row, evidence_root))

    if status == "PASS":
        for row in records:
            if isinstance(row, Mapping) and row.get("exit_code") != 0:
                issues.append(f"{task_id}:PASS_COMMAND_INVALID")
                break
    if status == "FAIL":
        if not any(isinstance(row, Mapping) and row.get("exit_code") != 0 for row in records):
            issues.append(f"{task_id}:FAIL_WITHOUT_FAILED_COMMAND")
    return issues


def verify_campaign_run(
    campaign: Mapping[str, Any],
    results: Mapping[str, Mapping[str, Any]],
    *,
    evidence_root: Path | None = None,
) -> dict[str, Any]:
    issues = list(validate_campaign(campaign))
    tasks = {
        t["task_id"]: t
        for t in campaign.get("tasks", [])
        if isinstance(t, Mapping) and isinstance(t.get("task_id"), str)
    }
    if not isinstance(results, Mapping):
        return {
            "valid": False,
            "issues": [*issues, "RESULTS_NOT_MAPPING"],
            "first_failure": None,
            "global_failures": [],
            "global_stop": None,
            "verification_scope": "SER_PARALLEL_LOCAL_CAMPAIGN_INTEGRITY",
        }
    if set(results) != set(tasks):
        issues.append("RESULT_SET_MISMATCH")

    first_failure = _canonical_first_failure(results)
    global_stop_event = _canonical_global_stop(tasks, results)
    global_stop = global_stop_event[1] if global_stop_event else None
    global_failures = sorted(
        task_id
        for task_id, task in tasks.items()
        if task.get("failure_scope") == "GLOBAL_CAMPAIGN"
        and (results.get(task_id) or {}).get("status") == "FAIL"
    )

    # Per-task bindings and state semantics.
    for task_id, task in tasks.items():
        result = results.get(task_id)
        if not isinstance(result, Mapping):
            continue
        for issue in validate_result(result):
            issues.append(f"{task_id}:{issue}")
        if result.get("task_id") != task_id:
            issues.append(f"{task_id}:RESULT_TASK_ID_BINDING_MISMATCH")
        if task.get("candidate_sha") != campaign.get("candidate_sha"):
            issues.append(f"{task_id}:TASK_CANDIDATE_BINDING_MISMATCH")
        if result.get("candidate_sha") != campaign.get("candidate_sha"):
            issues.append(f"{task_id}:RESULT_CANDIDATE_BINDING_MISMATCH")
        if result.get("status") not in _FINAL_STATUSES:
            issues.append(f"{task_id}:RESULT_NOT_TERMINAL")
        if result.get("effect_state") != task.get("expected_effect"):
            issues.append(f"{task_id}:EFFECT_BINDING_MISMATCH")
        if result.get("protected_fingerprint_before") != result.get("protected_fingerprint_after"):
            issues.append(f"{task_id}:PROTECTED_PATH_MUTATED")
        if result.get("first_failure") != first_failure:
            issues.append(f"{task_id}:FIRST_FAILURE_INCONSISTENT")
        if result.get("status") == "PASS" and result.get("issues"):
            issues.append(f"{task_id}:PASS_WITH_OPEN_ISSUES")
        if result.get("status") == "NOT_APPLICABLE" and task.get("required") is True:
            issues.append(f"{task_id}:REQUIRED_TASK_NOT_APPLICABLE")
        issues.extend(_verify_command_records(task_id, task, result, evidence_root))

    # DAG reconstruction: an executed task must have completed predecessors in
    # a strictly earlier wave. A declared blocked state is not trusted as proof.
    for task_id, task in tasks.items():
        result = results.get(task_id)
        if not isinstance(result, Mapping):
            continue
        status = result.get("status")
        wave = result.get("wave_index")
        deps = task.get("depends_on") or []
        expected_blockers = {
            dep
            for dep in deps
            if (results.get(dep) or {}).get("status") not in {"PASS", "NOT_APPLICABLE"}
        }
        if status in _EXECUTED_STATUSES | {"NOT_APPLICABLE"}:
            if expected_blockers:
                issues.append(f"{task_id}:EXECUTED_WITH_UNSATISFIED_DEPENDENCY")
            for dep in deps:
                dep_result = results.get(dep) or {}
                dep_wave = dep_result.get("wave_index")
                if type(wave) is int and type(dep_wave) is int and dep_wave >= wave:
                    issues.append(f"{task_id}:DEPENDENCY_NOT_COMPLETED_IN_PRIOR_WAVE:{dep}")
        if status == "BLOCKED_DEPENDENCY":
            blockers = set(result.get("blocked_by") or [])
            if blockers != expected_blockers or not expected_blockers:
                issues.append(f"{task_id}:BLOCKED_BY_MISMATCH")
        elif status not in {"BLOCKED_GLOBAL_STOP", "BLOCKED_RESOURCE", "BLOCKED_ENVIRONMENT"}:
            if result.get("blocked_by") not in (None, []):
                issues.append(f"{task_id}:UNEXPECTED_BLOCKED_BY")

    # Global stop is determined from the first GLOBAL_CAMPAIGN failure by wave
    # and task id. Anything not already started in that wave must not execute.
    if global_stop_event is not None:
        stop_wave, stop_task = global_stop_event
        for task_id, result in results.items():
            if not isinstance(result, Mapping) or type(result.get("wave_index")) is not int:
                continue
            wave = result["wave_index"]
            status = result.get("status")
            if wave > stop_wave and status != "BLOCKED_GLOBAL_STOP":
                issues.append(f"{task_id}:LATE_TASK_AFTER_GLOBAL_STOP")
            if status == "BLOCKED_GLOBAL_STOP":
                if wave <= stop_wave:
                    issues.append(f"{task_id}:GLOBAL_STOP_WAVE_INVALID")
                if result.get("blocked_by") != [stop_task]:
                    issues.append(f"{task_id}:GLOBAL_STOP_BLOCKER_INVALID")
    else:
        for task_id, result in results.items():
            if isinstance(result, Mapping) and result.get("status") == "BLOCKED_GLOBAL_STOP":
                issues.append(f"{task_id}:GLOBAL_STOP_WITHOUT_GLOBAL_FAILURE")

    # Reconstruct concurrency, exclusivity, resource and auditor limits by wave.
    by_wave: dict[int, list[str]] = defaultdict(list)
    for task_id, result in results.items():
        if (
            isinstance(result, Mapping)
            and result.get("status") in _EXECUTED_STATUSES
            and type(result.get("wave_index")) is int
        ):
            by_wave[result["wave_index"]].append(task_id)
    for wave, task_ids in by_wave.items():
        if len(task_ids) > campaign.get("max_parallel", 0):
            issues.append(f"WAVE_{wave}:MAX_PARALLEL_EXCEEDED")
        keys = [tasks[task_id].get("exclusivity_key") for task_id in task_ids]
        if any(count > 1 for count in Counter(keys).values()):
            issues.append(f"WAVE_{wave}:EXCLUSIVITY_KEY_COLLISION")
        auditors = sum(1 for task_id in task_ids if tasks[task_id].get("role") in _AUDITOR_ROLES)
        if auditors > campaign.get("max_auditors", 0):
            issues.append(f"WAVE_{wave}:MAX_AUDITORS_EXCEEDED")
        resource_counts = Counter(tasks[task_id].get("resource_class") for task_id in task_ids)
        for resource, count in resource_counts.items():
            cap = (campaign.get("resource_limits") or {}).get(resource)
            if cap is not None and count > cap:
                issues.append(f"WAVE_{wave}:RESOURCE_LIMIT_EXCEEDED:{resource}")

    return {
        "valid": not issues,
        "issues": issues,
        "first_failure": first_failure,
        "global_failures": global_failures,
        "global_stop": global_stop,
        "verification_scope": "SER_PARALLEL_LOCAL_CAMPAIGN_INTEGRITY",
    }


def _safe_manifest_rel(rel: str) -> bool:
    if not rel or "\\" in rel or rel.startswith("/"):
        return False
    path = PurePosixPath(rel)
    return not path.is_absolute() and "." not in path.parts and ".." not in path.parts


def verify_bundle(root: Path) -> dict[str, Any]:
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.is_file():
        return {"valid": False, "issues": ["MANIFEST_MISSING"]}
    if manifest_path.is_symlink():
        return {"valid": False, "issues": ["MANIFEST_SYMLINK_FORBIDDEN"]}
    try:
        manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"valid": False, "issues": ["MANIFEST_UNREADABLE:" + type(exc).__name__]}

    issues: list[str] = []
    expected = manifest.get("files")
    if manifest.get("schema_version") != "SER-PARALLEL-BUNDLE-3" or not isinstance(expected, list):
        return {"valid": False, "issues": ["MANIFEST_SCHEMA_INVALID"]}
    listed: set[str] = set()
    for row in expected:
        if (
            not isinstance(row, Mapping)
            or set(row) != {"path", "size", "sha256"}
            or not isinstance(row.get("path"), str)
        ):
            issues.append("MANIFEST_ROW_INVALID")
            continue
        rel = row["path"]
        if rel in listed or not _safe_manifest_rel(rel) or rel == "MANIFEST.json":
            issues.append("MANIFEST_PATH_INVALID:" + rel)
            continue
        listed.add(rel)
        p = root / PurePosixPath(rel)
        if p.is_symlink():
            issues.append("SYMLINK_FORBIDDEN:" + rel)
            continue
        if not p.is_file():
            issues.append("FILE_MISSING:" + rel)
            continue
        data = p.read_bytes()
        if len(data) != row.get("size"):
            issues.append("SIZE_MISMATCH:" + rel)
        if hashlib.sha256(data).hexdigest() != row.get("sha256"):
            issues.append("HASH_MISMATCH:" + rel)

    actual: set[str] = set()
    for p in root.rglob("*"):
        if p == manifest_path:
            continue
        rel = p.relative_to(root).as_posix()
        if p.is_symlink():
            issues.append("SYMLINK_FORBIDDEN:" + rel)
            actual.add(rel)
        elif p.is_file():
            actual.add(rel)
    if actual != listed:
        issues.append("MANIFEST_FILESET_MISMATCH")
    return {"valid": not issues, "issues": sorted(set(issues))}
