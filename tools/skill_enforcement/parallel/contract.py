from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any, Mapping

CAMPAIGN_SCHEMA_VERSION = "SER-PARALLEL-CAMPAIGN-3"
TASK_SCHEMA_VERSION = "SER-PARALLEL-TASK-3"
RESULT_SCHEMA_VERSION = "SER-PARALLEL-RESULT-3"
COMMAND_RECORD_SCHEMA_VERSION = "SER-PARALLEL-COMMAND-RECORD-1"

CAMPAIGN_STATES = {
    "PLANNED", "AUTHORING_READY", "LOCAL_RUNNING", "LOCAL_PASS", "LOCAL_FAIL",
    "BLOCKED_ENVIRONMENT", "BLOCKED_DESIGN", "AUDIT_PENDING", "AUDIT_PASS",
    "EXTERNAL_PENDING", "EXTERNAL_PASS", "PROMOTION_CANDIDATE", "CERTIFIED",
    "WAITING_HUMAN", "MERGED",
}
TASK_STATES = {
    "PLANNED", "READY", "RUNNING", "PASS", "FAIL", "BLOCKED_DEPENDENCY",
    "BLOCKED_GLOBAL_STOP", "BLOCKED_RESOURCE", "BLOCKED_ENVIRONMENT", "NOT_APPLICABLE",
}
EFFECT_STATES = {"NONE", "CREATED", "MODIFIED", "PARTIAL", "UNKNOWN", "CLEANUP_REQUIRED"}
ROLES = {"coordinator", "executor", "domain_auditor", "evidence_auditor", "integrator"}
RESOURCE_CLASSES = {"light", "cpu", "spark", "tracking", "external_effect", "audit"}
FAILURE_SCOPES = {"LOCAL_CHAIN", "GLOBAL_CAMPAIGN"}
CLEANUP_STATES = {
    "NOT_STARTED", "COMPLETE_ALREADY_EXITED", "COMPLETE",
    "COMPLETE_DESCENDANTS_TERMINATED", "INCOMPLETE",
}
SUPERVISION_STATES = {"NOT_STARTED", "POSIX_PROCESS_GROUP", "WINDOWS_JOB_OBJECT"}

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{2,127}$")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest_json(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _closed_keys(obj: Mapping[str, Any], required: set[str], optional: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    issues.extend(f"{prefix}:MISSING:{key}" for key in sorted(required - set(obj)))
    issues.extend(f"{prefix}:UNKNOWN:{key}" for key in sorted(set(obj) - required - optional))
    return issues


def _strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(x, str) and x for x in value)


def _safe_rel(value: str) -> bool:
    if not value or "\\" in value:
        return False
    p = PurePosixPath(value)
    return not p.is_absolute() and ".." not in p.parts and "." not in p.parts


def _timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def validate_task(task: Any) -> list[str]:
    if not isinstance(task, Mapping):
        return ["TASK_NOT_MAPPING"]
    required = {
        "task_schema", "task_id", "role", "stage", "skill", "candidate_sha",
        "command_ids", "depends_on", "read_roots", "write_roots", "protected_paths",
        "resource_class", "exclusivity_key", "required", "expected_effect", "failure_scope",
    }
    optional = {"description", "external_gate", "not_applicable_reason"}
    issues = _closed_keys(task, required, optional, "TASK")
    if task.get("task_schema") != TASK_SCHEMA_VERSION:
        issues.append("TASK_SCHEMA_INVALID")
    task_id = task.get("task_id")
    if not isinstance(task_id, str) or not _ID_RE.fullmatch(task_id):
        issues.append("TASK_ID_INVALID")
    if task.get("role") not in ROLES:
        issues.append("TASK_ROLE_INVALID")
    if not isinstance(task.get("stage"), str) or not task.get("stage"):
        issues.append("TASK_STAGE_INVALID")
    if not isinstance(task.get("skill"), str) or not task.get("skill"):
        issues.append("TASK_SKILL_INVALID")
    if not isinstance(task.get("candidate_sha"), str) or not _SHA_RE.fullmatch(task["candidate_sha"]):
        issues.append("TASK_CANDIDATE_SHA_INVALID")
    for key in ("command_ids", "depends_on", "read_roots", "write_roots", "protected_paths"):
        value = task.get(key)
        if not _strings(value) and value != []:
            issues.append(f"TASK_{key.upper()}_INVALID")
        if isinstance(value, list) and len(value) != len(set(value)):
            issues.append(f"TASK_{key.upper()}_DUPLICATE")
    for key in ("read_roots", "write_roots", "protected_paths"):
        for value in task.get(key) or []:
            if isinstance(value, str) and not _safe_rel(value):
                issues.append(f"TASK_{key.upper()}_UNSAFE:{value}")
    if task.get("resource_class") not in RESOURCE_CLASSES:
        issues.append("TASK_RESOURCE_CLASS_INVALID")
    if not isinstance(task.get("exclusivity_key"), str) or not task.get("exclusivity_key"):
        issues.append("TASK_EXCLUSIVITY_KEY_INVALID")
    if not (task.get("command_ids") or []):
        issues.append("TASK_COMMANDS_EMPTY")
    if type(task.get("required")) is not bool:
        issues.append("TASK_REQUIRED_INVALID")
    elif task.get("required") is False:
        reason = task.get("not_applicable_reason")
        if not isinstance(reason, str) or not reason.strip():
            issues.append("TASK_OPTIONAL_REASON_REQUIRED")
    if task.get("required") is True and "not_applicable_reason" in task:
        issues.append("TASK_REQUIRED_CANNOT_DECLARE_NA_REASON")
    if task.get("expected_effect") not in EFFECT_STATES:
        issues.append("TASK_EXPECTED_EFFECT_INVALID")
    if task.get("failure_scope") not in FAILURE_SCOPES:
        issues.append("TASK_FAILURE_SCOPE_INVALID")
    if set(task.get("read_roots") or []) & set(task.get("write_roots") or []):
        issues.append("TASK_READ_WRITE_ROOT_OVERLAP")
    if set(task.get("protected_paths") or []) & set(task.get("write_roots") or []):
        issues.append("TASK_PROTECTED_WRITE_OVERLAP")
    if task.get("write_roots"):
        issues.append("TASK_REPO_WRITES_NOT_SUPPORTED_BY_B0")
    if task.get("expected_effect") != "NONE":
        issues.append("TASK_EFFECT_NOT_SUPPORTED_BY_B0")
    return issues


def validate_campaign(payload: Any) -> list[str]:
    if not isinstance(payload, Mapping):
        return ["CAMPAIGN_NOT_MAPPING"]
    required = {
        "schema_version", "campaign_id", "round_id", "release_spec_digest",
        "baseline_sha", "candidate_sha", "candidate_tree_sha", "state",
        "max_parallel", "max_auditors", "tasks", "command_registry_digest",
        "coverage_digest", "policy_before_digest", "human_gates", "external_gates",
        "repo_mode",
    }
    optional = {"description", "approved_target_vector", "resource_limits"}
    issues = _closed_keys(payload, required, optional, "CAMPAIGN")
    if payload.get("schema_version") != CAMPAIGN_SCHEMA_VERSION:
        issues.append("CAMPAIGN_SCHEMA_INVALID")
    for key in ("campaign_id", "round_id"):
        value = payload.get(key)
        if not isinstance(value, str) or not _ID_RE.fullmatch(value):
            issues.append(f"CAMPAIGN_{key.upper()}_INVALID")
    for key in ("baseline_sha", "candidate_sha", "candidate_tree_sha"):
        value = payload.get(key)
        if not isinstance(value, str) or not _SHA_RE.fullmatch(value):
            issues.append(f"CAMPAIGN_{key.upper()}_INVALID")
    if payload.get("state") not in CAMPAIGN_STATES:
        issues.append("CAMPAIGN_STATE_INVALID")
    if payload.get("repo_mode") != "READ_ONLY":
        issues.append("CAMPAIGN_REPO_MODE_MUST_BE_READ_ONLY")
    for key in ("max_parallel", "max_auditors"):
        value = payload.get(key)
        if type(value) is not int or value < 1 or value > 8:
            issues.append(f"CAMPAIGN_{key.upper()}_INVALID")
    if type(payload.get("max_parallel")) is int and type(payload.get("max_auditors")) is int:
        if payload["max_auditors"] > payload["max_parallel"]:
            issues.append("CAMPAIGN_AUDITORS_EXCEED_TOTAL_SLOTS")
    tasks = payload.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        issues.append("CAMPAIGN_TASKS_INVALID")
        tasks = []
    task_ids: list[str] = []
    for idx, task in enumerate(tasks):
        for issue in validate_task(task):
            issues.append(f"CAMPAIGN_TASK[{idx}]:{issue}")
        if isinstance(task, Mapping) and isinstance(task.get("task_id"), str):
            task_ids.append(task["task_id"])
    if len(task_ids) != len(set(task_ids)):
        issues.append("CAMPAIGN_TASK_ID_DUPLICATE")
    known = set(task_ids)
    for task in tasks:
        if not isinstance(task, Mapping):
            continue
        unknown = sorted(set(task.get("depends_on") or []) - known)
        if unknown:
            issues.append(f"CAMPAIGN_DEPENDENCY_UNKNOWN:{task.get('task_id')}:{','.join(unknown)}")
        if task.get("task_id") in set(task.get("depends_on") or []):
            issues.append(f"CAMPAIGN_SELF_DEPENDENCY:{task.get('task_id')}")
        if task.get("candidate_sha") != payload.get("candidate_sha"):
            issues.append(f"CAMPAIGN_TASK_CANDIDATE_MISMATCH:{task.get('task_id')}")
    for key in ("release_spec_digest", "command_registry_digest", "coverage_digest", "policy_before_digest"):
        value = payload.get(key)
        if not isinstance(value, str) or _HEX64_RE.fullmatch(value) is None:
            issues.append(f"CAMPAIGN_{key.upper()}_INVALID")
    if not _strings(payload.get("human_gates")) and payload.get("human_gates") != []:
        issues.append("CAMPAIGN_HUMAN_GATES_INVALID")
    if not _strings(payload.get("external_gates")) and payload.get("external_gates") != []:
        issues.append("CAMPAIGN_EXTERNAL_GATES_INVALID")
    resource_limits = payload.get("resource_limits")
    if resource_limits is not None:
        if not isinstance(resource_limits, Mapping):
            issues.append("CAMPAIGN_RESOURCE_LIMITS_INVALID")
        else:
            for key, value in resource_limits.items():
                if key not in RESOURCE_CLASSES or type(value) is not int or value < 1 or value > 8:
                    issues.append(f"CAMPAIGN_RESOURCE_LIMIT_INVALID:{key}")
    return issues


def validate_command_record(record: Any) -> list[str]:
    if not isinstance(record, Mapping):
        return ["COMMAND_RECORD_NOT_MAPPING"]
    required = {
        "record_schema", "name", "argv", "command_started", "pid", "exit_code",
        "timed_out", "cleanup", "residual_descendants_detected", "supervision",
        "duration_seconds", "started_at_utc", "ended_at_utc",
        "stdout_sha256", "stderr_sha256",
    }
    optional = {"spawn_error"}
    issues = _closed_keys(record, required, optional, "COMMAND_RECORD")
    if record.get("record_schema") != COMMAND_RECORD_SCHEMA_VERSION:
        issues.append("COMMAND_RECORD_SCHEMA_INVALID")
    if not isinstance(record.get("name"), str) or not record.get("name"):
        issues.append("COMMAND_RECORD_NAME_INVALID")
    argv = record.get("argv")
    if not isinstance(argv, list) or not argv or any(not isinstance(x, str) or not x for x in argv):
        issues.append("COMMAND_RECORD_ARGV_INVALID")
    if type(record.get("command_started")) is not bool:
        issues.append("COMMAND_RECORD_STARTED_INVALID")
    if record.get("pid") is not None and (type(record.get("pid")) is not int or record["pid"] <= 0):
        issues.append("COMMAND_RECORD_PID_INVALID")
    if type(record.get("exit_code")) is not int:
        issues.append("COMMAND_RECORD_EXIT_CODE_INVALID")
    if type(record.get("timed_out")) is not bool:
        issues.append("COMMAND_RECORD_TIMEOUT_INVALID")
    if record.get("cleanup") not in CLEANUP_STATES:
        issues.append("COMMAND_RECORD_CLEANUP_INVALID")
    if type(record.get("residual_descendants_detected")) is not bool:
        issues.append("COMMAND_RECORD_RESIDUAL_INVALID")
    if record.get("supervision") not in SUPERVISION_STATES:
        issues.append("COMMAND_RECORD_SUPERVISION_INVALID")
    duration = record.get("duration_seconds")
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration < 0:
        issues.append("COMMAND_RECORD_DURATION_INVALID")
    start = _timestamp(record.get("started_at_utc"))
    end = _timestamp(record.get("ended_at_utc"))
    if start is None:
        issues.append("COMMAND_RECORD_STARTED_AT_INVALID")
    if end is None:
        issues.append("COMMAND_RECORD_ENDED_AT_INVALID")
    if start is not None and end is not None and end < start:
        issues.append("COMMAND_RECORD_TIME_ORDER_INVALID")
    for key in ("stdout_sha256", "stderr_sha256"):
        value = record.get(key)
        if not isinstance(value, str) or _HEX64_RE.fullmatch(value) is None:
            issues.append(f"COMMAND_RECORD_{key.upper()}_INVALID")
    if record.get("command_started") is True:
        if type(record.get("pid")) is not int or record.get("pid", 0) <= 0:
            issues.append("COMMAND_RECORD_STARTED_PID_REQUIRED")
        if record.get("supervision") == "NOT_STARTED":
            issues.append("COMMAND_RECORD_STARTED_SUPERVISION_REQUIRED")
        if "spawn_error" in record:
            issues.append("COMMAND_RECORD_STARTED_HAS_SPAWN_ERROR")
    elif record.get("command_started") is False:
        if record.get("pid") is not None:
            issues.append("COMMAND_RECORD_NOT_STARTED_PID_PRESENT")
        if record.get("cleanup") != "NOT_STARTED":
            issues.append("COMMAND_RECORD_NOT_STARTED_CLEANUP_INVALID")
        if record.get("supervision") != "NOT_STARTED":
            issues.append("COMMAND_RECORD_NOT_STARTED_SUPERVISION_INVALID")
        if not isinstance(record.get("spawn_error"), str) or not record.get("spawn_error"):
            issues.append("COMMAND_RECORD_SPAWN_ERROR_REQUIRED")
    if record.get("timed_out") is True and record.get("exit_code") == 0:
        issues.append("COMMAND_RECORD_TIMEOUT_EXIT_ZERO")
    if record.get("residual_descendants_detected") is True and record.get("cleanup") not in {"COMPLETE_DESCENDANTS_TERMINATED", "INCOMPLETE"}:
        issues.append("COMMAND_RECORD_RESIDUAL_CLEANUP_INVALID")
    return issues


def validate_result(result: Any) -> list[str]:
    if not isinstance(result, Mapping):
        return ["RESULT_NOT_MAPPING"]
    required = {
        "result_schema", "task_id", "round_id", "release_spec_digest",
        "candidate_sha", "status", "effect_state", "command_records",
        "first_failure", "wave_index", "started_at_utc", "ended_at_utc",
        "protected_fingerprint_before", "protected_fingerprint_after", "issues",
    }
    optional = {"diagnosis", "evidence_files", "blocked_by"}
    issues = _closed_keys(result, required, optional, "RESULT")
    if result.get("result_schema") != RESULT_SCHEMA_VERSION:
        issues.append("RESULT_SCHEMA_INVALID")
    for key in ("task_id", "round_id"):
        value = result.get(key)
        if not isinstance(value, str) or not _ID_RE.fullmatch(value):
            issues.append(f"RESULT_{key.upper()}_INVALID")
    if not isinstance(result.get("release_spec_digest"), str) or _HEX64_RE.fullmatch(result["release_spec_digest"]) is None:
        issues.append("RESULT_RELEASE_SPEC_DIGEST_INVALID")
    if not isinstance(result.get("candidate_sha"), str) or not _SHA_RE.fullmatch(result["candidate_sha"]):
        issues.append("RESULT_CANDIDATE_SHA_INVALID")
    if result.get("status") not in TASK_STATES:
        issues.append("RESULT_STATUS_INVALID")
    if result.get("effect_state") not in EFFECT_STATES:
        issues.append("RESULT_EFFECT_INVALID")
    records = result.get("command_records")
    if not isinstance(records, list):
        issues.append("RESULT_COMMAND_RECORDS_INVALID")
    else:
        for idx, record in enumerate(records):
            for issue in validate_command_record(record):
                issues.append(f"RESULT_COMMAND_RECORD[{idx}]:{issue}")
    if not isinstance(result.get("issues"), list) or any(not isinstance(x, str) for x in result.get("issues", [])):
        issues.append("RESULT_ISSUES_INVALID")
    if type(result.get("wave_index")) is not int or result.get("wave_index") < 0:
        issues.append("RESULT_WAVE_INDEX_INVALID")
    start = _timestamp(result.get("started_at_utc"))
    end = _timestamp(result.get("ended_at_utc"))
    if start is None:
        issues.append("RESULT_STARTED_AT_INVALID")
    if end is None:
        issues.append("RESULT_ENDED_AT_INVALID")
    if start is not None and end is not None and end < start:
        issues.append("RESULT_TIME_ORDER_INVALID")
    for key in ("protected_fingerprint_before", "protected_fingerprint_after"):
        value = result.get(key)
        if not isinstance(value, str) or _HEX64_RE.fullmatch(value) is None:
            issues.append(f"RESULT_{key.upper()}_INVALID")
    blocked_by = result.get("blocked_by")
    if blocked_by is not None and (not _strings(blocked_by) and blocked_by != []):
        issues.append("RESULT_BLOCKED_BY_INVALID")
    return issues
