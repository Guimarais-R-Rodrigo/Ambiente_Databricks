from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .contract import validate_campaign, validate_result

def verify_campaign_run(campaign: Mapping[str, Any], results: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    issues = list(validate_campaign(campaign))
    tasks = {t["task_id"]: t for t in campaign.get("tasks", []) if isinstance(t, Mapping) and "task_id" in t}
    if set(results) != set(tasks):
        issues.append("RESULT_SET_MISMATCH")
    first_failure = None
    for task_id, task in tasks.items():
        result = results.get(task_id)
        if result is None:
            continue
        for issue in validate_result(result):
            issues.append(f"{task_id}:{issue}")
        if result.get("candidate_sha") != campaign.get("candidate_sha"):
            issues.append(f"{task_id}:CANDIDATE_BINDING_MISMATCH")
        if result.get("protected_fingerprint_before") != result.get("protected_fingerprint_after"):
            issues.append(f"{task_id}:PROTECTED_PATH_MUTATED")
        records = result.get("command_records") or []
        if result.get("status") == "PASS" and any(r.get("exit_code") != 0 for r in records if isinstance(r, Mapping)):
            issues.append(f"{task_id}:PASS_WITH_NONZERO_COMMAND")
        if result.get("status") == "FAIL" and first_failure is None:
            first_failure = task_id
        if result.get("status") == "BLOCKED_DEPENDENCY":
            blockers = set(result.get("blocked_by") or [])
            expected = {d for d in task.get("depends_on") or [] if (results.get(d) or {}).get("status") not in {"PASS", "NOT_APPLICABLE"}}
            if blockers != expected:
                issues.append(f"{task_id}:BLOCKED_BY_MISMATCH")
    declared = [r.get("first_failure") for r in results.values() if isinstance(r, Mapping) and r.get("first_failure")]
    if first_failure and declared and any(x != first_failure for x in declared):
        issues.append("FIRST_FAILURE_INCONSISTENT")
    return {
        "valid": not issues,
        "issues": issues,
        "first_failure": first_failure,
        "verification_scope": "SER_PARALLEL_LOCAL_CAMPAIGN_INTEGRITY",
    }

def verify_bundle(root: Path) -> dict[str, Any]:
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.is_file():
        return {"valid": False, "issues": ["MANIFEST_MISSING"]}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    expected = manifest.get("files")
    if not isinstance(expected, list):
        return {"valid": False, "issues": ["MANIFEST_FILES_INVALID"]}
    listed = set()
    for row in expected:
        if not isinstance(row, Mapping) or not isinstance(row.get("path"), str):
            issues.append("MANIFEST_ROW_INVALID"); continue
        rel = row["path"]; listed.add(rel); p = root / rel
        if not p.is_file():
            issues.append("FILE_MISSING:" + rel); continue
        data = p.read_bytes()
        if len(data) != row.get("size"):
            issues.append("SIZE_MISMATCH:" + rel)
        if hashlib.sha256(data).hexdigest() != row.get("sha256"):
            issues.append("HASH_MISMATCH:" + rel)
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name != "MANIFEST.json"}
    if actual != listed:
        issues.append("MANIFEST_FILESET_MISMATCH")
    return {"valid": not issues, "issues": issues}
