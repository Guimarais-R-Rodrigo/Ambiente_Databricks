from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from .bundle import BUNDLE_SCHEMA_VERSION, RAW_SHARE_SCHEMA_VERSION, SECRET_SCAN_POLICY_VERSION, scan_share
from .contract import validate_campaign, validate_result
from .registry import RegistryError, resolve_command
from .scheduler import detect_cycle

_TERMINAL = {"PASS", "FAIL", "BLOCKED_DEPENDENCY", "BLOCKED_GLOBAL_STOP", "BLOCKED_RESOURCE", "BLOCKED_ENVIRONMENT", "NOT_APPLICABLE"}
_EXECUTED = {"PASS", "FAIL"}
_AUDITOR_ROLES = {"domain_auditor", "evidence_auditor"}


def _time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _canonical_first_failure(results: Mapping[str, Any]) -> str | None:
    failures = [
        (row.get("wave_index"), task_id)
        for task_id, row in results.items()
        if isinstance(row, Mapping) and row.get("status") == "FAIL" and type(row.get("wave_index")) is int
    ]
    return min(failures)[1] if failures else None


def _first_observed_failure(results: Mapping[str, Any]) -> str | None:
    failures = []
    for task_id, row in results.items():
        if not isinstance(row, Mapping) or row.get("status") != "FAIL":
            continue
        ended = _time(row.get("ended_at_utc"))
        if ended is not None:
            failures.append((ended, task_id))
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


def _overlap(a: tuple[datetime, datetime], b: tuple[datetime, datetime]) -> bool:
    return a[0] < b[1] and b[0] < a[1]


def _max_concurrency(items: list[tuple[datetime, datetime]]) -> int:
    events: list[tuple[datetime, int]] = []
    for start, end in items:
        events.append((start, 1)); events.append((end, -1))
    active = 0; peak = 0
    for _, delta in sorted(events, key=lambda item: (item[0], item[1])):
        active += delta; peak = max(peak, active)
    return peak


def verify_campaign_run(campaign: Mapping[str, Any], results: Any, evidence_root: Path | None = None) -> dict[str, Any]:
    issues = list(validate_campaign(campaign))
    raw_tasks = campaign.get("tasks", []) if isinstance(campaign, Mapping) else []
    tasks = {t["task_id"]: t for t in raw_tasks if isinstance(t, Mapping) and isinstance(t.get("task_id"), str)}
    if detect_cycle(list(tasks.values())):
        issues.append("CAMPAIGN_DAG_CYCLE")
    if not isinstance(results, Mapping):
        issues.append("RESULT_MAP_INVALID"); results = {}
    if set(results) != set(tasks):
        issues.append("RESULT_SET_MISMATCH")

    first_failure = _canonical_first_failure(results)
    first_observed_failure = _first_observed_failure(results)
    global_failures: list[tuple[int, str]] = []
    for task_id, task in tasks.items():
        row = results.get(task_id)
        if task.get("failure_scope") == "GLOBAL_CAMPAIGN" and isinstance(row, Mapping) and row.get("status") == "FAIL" and type(row.get("wave_index")) is int:
            global_failures.append((row["wave_index"], task_id))
    global_failures.sort()
    first_global = global_failures[0] if global_failures else None

    intervals: dict[str, tuple[datetime, datetime]] = {}
    waves: dict[int, list[str]] = {}
    for task_id, task in tasks.items():
        if task_id not in results:
            issues.append(f"{task_id}:RESULT_MISSING"); continue
        result = results.get(task_id)
        if result is None:
            issues.append(f"{task_id}:RESULT_NULL"); continue
        if not isinstance(result, Mapping):
            issues.append(f"{task_id}:RESULT_NOT_MAPPING"); continue
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
        if result.get("round_id") != campaign.get("round_id"):
            issues.append(f"{task_id}:ROUND_BINDING_MISMATCH")
        if result.get("release_spec_digest") != campaign.get("release_spec_digest"):
            issues.append(f"{task_id}:RELEASE_SPEC_BINDING_MISMATCH")
        if result.get("effect_state") != task.get("expected_effect"):
            issues.append(f"{task_id}:EFFECT_BINDING_MISMATCH")
        if result.get("protected_fingerprint_before") != result.get("protected_fingerprint_after"):
            issues.append(f"{task_id}:PROTECTED_PATH_MUTATED")
        if result.get("first_failure") != first_failure:
            issues.append(f"{task_id}:FIRST_FAILURE_INCONSISTENT")

        start = _time(result.get("started_at_utc")); end = _time(result.get("ended_at_utc"))
        if status in _EXECUTED and start is not None and end is not None:
            intervals[task_id] = (start, end)
            if type(result.get("wave_index")) is int:
                waves.setdefault(result["wave_index"], []).append(task_id)

        records = result.get("command_records") if isinstance(result.get("command_records"), list) else []
        command_ids = task.get("command_ids") or []
        if status in _EXECUTED:
            if not command_ids:
                issues.append(f"{task_id}:EXECUTED_WITHOUT_DECLARED_COMMANDS")
            if status == "PASS" and len(records) != len(command_ids):
                issues.append(f"{task_id}:PASS_COMMAND_COUNT_MISMATCH")
            if status == "FAIL" and (not records or len(records) > len(command_ids)):
                issues.append(f"{task_id}:FAIL_COMMAND_COUNT_INVALID")
            for idx, row in enumerate(records):
                if idx >= len(command_ids):
                    issues.append(f"{task_id}:UNDECLARED_COMMAND_RECORD"); continue
                if not isinstance(row, Mapping):
                    issues.append(f"{task_id}:COMMAND_RECORD_INVALID"); continue
                issues.extend(_record_log_issues(task_id, command_ids[idx], row, evidence_root))
            if status == "PASS":
                if result.get("issues"):
                    issues.append(f"{task_id}:PASS_WITH_ISSUES")
                for row in records:
                    if not isinstance(row, Mapping):
                        issues.append(f"{task_id}:PASS_COMMAND_INVALID"); continue
                    valid_exit = type(row.get("exit_code")) is int and row.get("exit_code") == 0
                    if (
                        not valid_exit or row.get("command_started") is not True
                        or row.get("timed_out") is not False
                        or row.get("cleanup") not in {"COMPLETE", "COMPLETE_ALREADY_EXITED"}
                        or row.get("residual_descendants_detected") is not False
                    ):
                        issues.append(f"{task_id}:PASS_COMMAND_INVALID")
            if status == "FAIL":
                def failed_record(row: Any) -> bool:
                    return isinstance(row, Mapping) and type(row.get("exit_code")) is int and row.get("exit_code") != 0
                if not any(failed_record(row) for row in records):
                    issues.append(f"{task_id}:FAIL_WITHOUT_FAILED_COMMAND")
        elif records:
            issues.append(f"{task_id}:BLOCKED_OR_NA_TASK_EXECUTED")

        if status == "NOT_APPLICABLE":
            if task.get("required") is not False:
                issues.append(f"{task_id}:REQUIRED_TASK_NOT_APPLICABLE")
            reason = task.get("not_applicable_reason")
            if not isinstance(reason, str) or not reason.strip():
                issues.append(f"{task_id}:NOT_APPLICABLE_REASON_MISSING")

        dep_states = {d: (results.get(d) or {}).get("status") if isinstance(results.get(d), Mapping) else None for d in task.get("depends_on") or []}
        failed_deps = {d for d, state in dep_states.items() if state not in {"PASS", "NOT_APPLICABLE"}}
        if status in _EXECUTED:
            if failed_deps:
                issues.append(f"{task_id}:EXECUTED_WITH_UNSATISFIED_DEPENDENCY")
            for dep in task.get("depends_on") or []:
                dep_result = results.get(dep)
                if not isinstance(dep_result, Mapping):
                    continue
                if type(dep_result.get("wave_index")) is int and type(result.get("wave_index")) is int and dep_result["wave_index"] >= result["wave_index"]:
                    issues.append(f"{task_id}:DEPENDENCY_WAVE_ORDER_INVALID:{dep}")
                dep_end = _time(dep_result.get("ended_at_utc"))
                if dep_end is not None and start is not None and dep_end > start:
                    issues.append(f"{task_id}:DEPENDENCY_TIME_ORDER_INVALID:{dep}")
        if status == "BLOCKED_DEPENDENCY":
            blockers = set(result.get("blocked_by") or [])
            if blockers != failed_deps or not blockers:
                issues.append(f"{task_id}:BLOCKED_BY_MISMATCH")
        elif failed_deps and status != "BLOCKED_GLOBAL_STOP":
            issues.append(f"{task_id}:DEPENDENCY_FAILURE_NOT_BLOCKED")

        if status == "BLOCKED_GLOBAL_STOP":
            if first_global is None:
                issues.append(f"{task_id}:GLOBAL_STOP_WITHOUT_GLOBAL_FAILURE")
            else:
                global_wave, global_id = first_global
                if type(result.get("wave_index")) is not int or result["wave_index"] <= global_wave:
                    issues.append(f"{task_id}:GLOBAL_STOP_WAVE_INVALID")
                if (result.get("blocked_by") or []) != [global_id]:
                    issues.append(f"{task_id}:GLOBAL_STOP_BLOCKER_INVALID")
                global_row = results.get(global_id)
                global_end = _time(global_row.get("ended_at_utc")) if isinstance(global_row, Mapping) else None
                blocked_start = _time(result.get("started_at_utc"))
                if global_end is not None and blocked_start is not None and blocked_start < global_end:
                    issues.append(f"{task_id}:GLOBAL_STOP_TIME_INVALID")
        elif first_global is not None:
            global_wave, _ = first_global
            wave = result.get("wave_index")
            if type(wave) is int and wave > global_wave:
                issues.append(f"{task_id}:GLOBAL_STOP_ESCAPE")

    previous_end: datetime | None = None
    for wave in sorted(waves):
        valid_intervals = [intervals[t] for t in waves[wave] if t in intervals]
        if not valid_intervals:
            continue
        wave_start = min(start for start, _ in valid_intervals)
        wave_end = max(end for _, end in valid_intervals)
        if previous_end is not None and wave_start < previous_end:
            issues.append(f"WAVE_{wave}:TEMPORAL_BARRIER_VIOLATION")
        previous_end = max(previous_end, wave_end) if previous_end is not None else wave_end

    if _max_concurrency(list(intervals.values())) > campaign.get("max_parallel", 0):
        issues.append("MAX_PARALLEL_INTERVAL_EXCEEDED")
    ids = sorted(intervals)
    for idx, left_id in enumerate(ids):
        for right_id in ids[idx + 1:]:
            if _overlap(intervals[left_id], intervals[right_id]) and tasks[left_id].get("exclusivity_key") == tasks[right_id].get("exclusivity_key"):
                issues.append(f"EXCLUSIVITY_INTERVAL_VIOLATION:{left_id}:{right_id}")
    auditor_intervals = [intervals[t] for t in intervals if tasks[t].get("role") in _AUDITOR_ROLES]
    if _max_concurrency(auditor_intervals) > campaign.get("max_auditors", 0):
        issues.append("AUDITOR_INTERVAL_LIMIT_EXCEEDED")
    for resource, limit in (campaign.get("resource_limits") or {}).items():
        resource_intervals = [intervals[t] for t in intervals if tasks[t].get("resource_class") == resource]
        if _max_concurrency(resource_intervals) > limit:
            issues.append(f"RESOURCE_INTERVAL_LIMIT_EXCEEDED:{resource}")

    return {
        "valid": not issues, "issues": issues, "first_failure": first_failure,
        "first_observed_failure": first_observed_failure,
        "global_failures": [task_id for _, task_id in global_failures],
        "verification_scope": "SER_PARALLEL_LOCAL_CAMPAIGN_INTEGRITY_V3",
    }


def verify_bundle(root: Path) -> dict[str, Any]:
    root = root.resolve(); manifest_path = root / "MANIFEST.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        return {"valid": False, "issues": ["MANIFEST_MISSING_OR_LINK"]}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"valid": False, "issues": ["MANIFEST_UNREADABLE:" + type(exc).__name__]}
    if not isinstance(manifest, Mapping):
        return {"valid": False, "issues": ["MANIFEST_ROOT_NOT_OBJECT"]}
    expected = manifest.get("files")
    if manifest.get("schema_version") != BUNDLE_SCHEMA_VERSION or not isinstance(expected, list):
        return {"valid": False, "issues": ["MANIFEST_SCHEMA_INVALID"]}
    issues: list[str] = []; listed: set[str] = set()
    for row in expected:
        if not isinstance(row, Mapping) or set(row) != {"path", "size", "sha256"} or not isinstance(row.get("path"), str):
            issues.append("MANIFEST_ROW_INVALID"); continue
        rel = row["path"]; parts = Path(rel).parts
        if rel in listed or rel.startswith("/") or ".." in parts or rel == "MANIFEST.json":
            issues.append("MANIFEST_PATH_INVALID:" + rel); continue
        listed.add(rel); p = root / rel
        if p.is_symlink():
            issues.append("BUNDLE_SYMLINK_FORBIDDEN:" + rel); continue
        try:
            resolved = p.resolve(strict=True)
        except OSError:
            issues.append("FILE_MISSING:" + rel); continue
        if not resolved.is_relative_to(root) or not resolved.is_file():
            issues.append("BUNDLE_PATH_ESCAPE_OR_NONFILE:" + rel); continue
        data = resolved.read_bytes()
        if type(row.get("size")) is not int or len(data) != row.get("size"):
            issues.append("SIZE_MISMATCH:" + rel)
        if hashlib.sha256(data).hexdigest() != row.get("sha256"):
            issues.append("HASH_MISMATCH:" + rel)
    actual: set[str] = set()
    for p in root.rglob("*"):
        if p == manifest_path: continue
        if p.is_symlink():
            issues.append("BUNDLE_SYMLINK_FORBIDDEN:" + p.relative_to(root).as_posix()); continue
        if p.is_file():
            actual.add(p.relative_to(root).as_posix())
    if actual != listed:
        issues.append("MANIFEST_FILESET_MISMATCH")
    return {"valid": not issues, "issues": sorted(set(issues))}


def verify_raw_share_binding(raw_root: Path, share_root: Path, binding_path: Path) -> dict[str, Any]:
    issues: list[str] = []
    try:
        binding = json.loads(binding_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"valid": False, "issues": ["RAW_SHARE_BINDING_UNREADABLE:" + type(exc).__name__]}
    required = {"schema_version", "raw_manifest_sha256", "share_manifest_sha256", "identities_are_distinct", "secret_scan"}
    if not isinstance(binding, Mapping) or set(binding) != required or binding.get("schema_version") != RAW_SHARE_SCHEMA_VERSION:
        return {"valid": False, "issues": ["RAW_SHARE_BINDING_SCHEMA_INVALID"]}
    raw_manifest = raw_root / "MANIFEST.json"; share_manifest = share_root / "MANIFEST.json"
    if not raw_manifest.is_file() or not share_manifest.is_file():
        return {"valid": False, "issues": ["RAW_SHARE_MANIFEST_MISSING"]}
    raw_bytes = raw_manifest.read_bytes(); share_bytes = share_manifest.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != binding.get("raw_manifest_sha256"):
        issues.append("RAW_MANIFEST_BINDING_MISMATCH")
    if hashlib.sha256(share_bytes).hexdigest() != binding.get("share_manifest_sha256"):
        issues.append("SHARE_MANIFEST_BINDING_MISMATCH")
    if binding.get("identities_are_distinct") is not True or raw_bytes == share_bytes:
        issues.append("RAW_SHARE_IDENTITIES_NOT_DISTINCT")

    actual_scan = scan_share(share_root); declared_scan = binding.get("secret_scan")
    if actual_scan.get("policy_version") != SECRET_SCAN_POLICY_VERSION:
        issues.append("SHARE_SECRET_SCAN_POLICY_INVALID")
    if declared_scan != actual_scan:
        issues.append("SHARE_SECRET_SCAN_DECLARATION_MISMATCH")
    if actual_scan.get("status") != "PASS" or actual_scan.get("findings") != []:
        issues.append("SHARE_SECRET_SCAN_NOT_PASS")

    raw_v = verify_bundle(raw_root); share_v = verify_bundle(share_root)
    if not raw_v["valid"]: issues.append("RAW_BUNDLE_INVALID")
    if not share_v["valid"]: issues.append("SHARE_BUNDLE_INVALID")

    metadata_path = share_root / "SHARE_METADATA.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        metadata = None
    if not isinstance(metadata, Mapping):
        issues.append("SHARE_METADATA_INVALID")
    else:
        if metadata.get("raw_manifest_sha256") != hashlib.sha256(raw_bytes).hexdigest():
            issues.append("SHARE_METADATA_RAW_BINDING_MISMATCH")
        if metadata.get("secret_scan_policy_version") != SECRET_SCAN_POLICY_VERSION:
            issues.append("SHARE_METADATA_SCAN_POLICY_MISMATCH")

    return {
        "valid": not issues, "issues": sorted(set(issues)), "raw": raw_v, "share": share_v, "secret_scan": actual_scan,
    }
