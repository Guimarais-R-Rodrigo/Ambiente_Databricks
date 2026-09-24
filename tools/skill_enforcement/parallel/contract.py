from __future__ import annotations

import hashlib
import json
import re
from pathlib import PurePosixPath
from typing import Any, Mapping

CAMPAIGN_SCHEMA_VERSION = "SER-PARALLEL-CAMPAIGN-2"
TASK_SCHEMA_VERSION = "SER-PARALLEL-TASK-2"
RESULT_SCHEMA_VERSION = "SER-PARALLEL-RESULT-2"

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
RESULT_STATES = {
    "PASS", "FAIL", "BLOCKED_DEPENDENCY", "BLOCKED_GLOBAL_STOP",
    "BLOCKED_RESOURCE", "BLOCKED_ENVIRONMENT", "NOT_APPLICABLE",
}
EFFECT_STATES = {"NONE", "CREATED", "MODIFIED", "PARTIAL", "UNKNOWN", "CLEANUP_REQUIRED"}
ROLES = {"coordinator", "executor", "domain_auditor", "evidence_auditor", "integrator"}
RESOURCE_CLASSES = {"light", "cpu", "spark", "tracking", "external_effect", "audit"}
FAILURE_SCOPES = {"LOCAL_CHAIN", "GLOBAL_CAMPAIGN"}

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{2,127}$")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


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
    if not isinstance(task.get("task_id"), str) or not _ID_RE.fullmatch(task["task_id"]):
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
    if type(task.get("required")) is not bool:
        issues.append("TASK_REQUIRED_INVALID")
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
        "schema_version", "campaign_id", "baseline_sha", "candidate_sha", "state",
        "max_parallel", "max_auditors", "tasks", "command_registry_digest",
        "coverage_digest", "policy_before_digest", "human_gates", "external_gates",
        "repo_mode",
    }
    optional = {"description", "approved_target_vector", "resource_limits"}
    issues = _closed_keys(payload, required, optional, "CAMPAIGN")
    if payload.get("schema_version") != CAMPAIGN_SCHEMA_VERSION:
        issues.append("CAMPAIGN_SCHEMA_INVALID")
    if not isinstance(payload.get("campaign_id"), str) or not _ID_RE.fullmatch(payload["campaign_id"]):
        issues.append("CAMPAIGN_ID_INVALID")
    for key in ("baseline_sha", "candidate_sha"):
        if not isinstance(payload.get(key), str) or not _SHA_RE.fullmatch(payload[key]):
            issues.append(f"CAMPAIGN_{key.upper()}_INVALID")
    if payload.get("state") not in CAMPAIGN_STATES:
        issues.append("CAMPAIGN_STATE_INVALID")
    if payload.get("repo_mode") != "READ_ONLY":
        issues.append("CAMPAIGN_REPO_MODE_MUST_BE_READ_ONLY")
    for key in ("max_parallel", "max_auditors"):
        if type(payload.get(key)) is not int or payload[key] < 1 or payload[key] > 8:
            issues.append(f"CAMPAIGN_{key.upper()}_INVALID")

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
            if task.get("candidate_sha") != payload.get("candidate_sha"):
                issues.append(f"CAMPAIGN_TASK_CANDIDATE_MISMATCH:{task['task_id']}")
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
    for key in ("command_registry_digest", "coverage_digest", "policy_before_digest"):
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


def validate_result(result: Any) -> list[str]:
    if not isinstance(result, Mapping):
        return ["RESULT_NOT_MAPPING"]
    required = {
        "result_schema", "task_id", "candidate_sha", "status", "effect_state",
        "command_records", "first_failure", "wave_index", "started_at_utc", "ended_at_utc",
        "protected_fingerprint_before", "protected_fingerprint_after", "issues",
    }
    optional = {"diagnosis", "evidence_files", "blocked_by"}
    issues = _closed_keys(result, required, optional, "RESULT")
    if result.get("result_schema") != RESULT_SCHEMA_VERSION:
        issues.append("RESULT_SCHEMA_INVALID")
    if not isinstance(result.get("task_id"), str) or not _ID_RE.fullmatch(result["task_id"]):
        issues.append("RESULT_TASK_ID_INVALID")
    if not isinstance(result.get("candidate_sha"), str) or not _SHA_RE.fullmatch(result["candidate_sha"]):
        issues.append("RESULT_CANDIDATE_SHA_INVALID")
    if result.get("status") not in RESULT_STATES:
        issues.append("RESULT_STATUS_INVALID")
    if result.get("effect_state") not in EFFECT_STATES:
        issues.append("RESULT_EFFECT_INVALID")
    if not isinstance(result.get("command_records"), list):
        issues.append("RESULT_COMMAND_RECORDS_INVALID")
    if not isinstance(result.get("issues"), list) or any(not isinstance(x, str) for x in result.get("issues", [])):
        issues.append("RESULT_ISSUES_INVALID")
    if type(result.get("wave_index")) is not int or result.get("wave_index") < 0:
        issues.append("RESULT_WAVE_INDEX_INVALID")
    for key in ("protected_fingerprint_before", "protected_fingerprint_after"):
        value = result.get(key)
        if not isinstance(value, str) or _HEX64_RE.fullmatch(value) is None:
            issues.append(f"RESULT_{key.upper()}_INVALID")
    ff = result.get("first_failure")
    if ff is not None and (not isinstance(ff, str) or not _ID_RE.fullmatch(ff)):
        issues.append("RESULT_FIRST_FAILURE_INVALID")
    for key in ("started_at_utc", "ended_at_utc"):
        if not isinstance(result.get(key), str) or not result[key]:
            issues.append(f"RESULT_{key.upper()}_INVALID")
    if "blocked_by" in result and not _strings(result.get("blocked_by")) and result.get("blocked_by") != []:
        issues.append("RESULT_BLOCKED_BY_INVALID")
    return issues
