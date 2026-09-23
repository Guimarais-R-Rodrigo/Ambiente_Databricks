"""Receipt de domínio para a superfície object_validation da skill criar-objeto.

O produtor canônico continua repo-side e exige checkout Git completo. Este módulo
viaja com a skill para verificar binding e integridade do Receipt, sem alegar
reexecução, autenticação humana, runtime do notebook, apply ou promoção de policy.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any, Mapping

SKILL = "hub-ml-criar-objeto"
PROTECTED_SURFACE = "object_validation"
ROUTE = "repo_side_local_structural_validation"
RECEIPT_VERSION = "SER01-OBJECT-VALIDATION-RECEIPT-1"
LOCAL_RECORD_VERSION = "SER01-LOCAL-VALIDATION-1"
LOCAL_SCOPE = "CREATE_PACKAGE_LOCAL_STRUCTURAL_VALIDATION_ONLY"
RECEIPT_ID_PREFIX = "ov1:"
SUPPORTED_TYPES = {"snippet", "script", "prompt", "notebook", "readme"}
REQUIRED_COMMANDS = {
    "identity_before", "status_before", "history", "preflight",
    "baseline_validator", "clone", "checkout", "stage", "validator",
    "overlay_head", "overlay_index", "overlay_diff", "overlay_untracked",
    "identity_after", "status_after",
}
BASE_CHECKS = {
    "destination_matches_preflight", "canonical_validator",
    "overlay_head_preserved", "overlay_index_exact",
    "overlay_no_other_changes", "overlay_bytes_exact", "original_preserved",
}


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _hex(value: Any, length: int) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(rf"[0-9a-f]{{{length}}}", value))


def _local_projection(record: Mapping[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in record.items()
            if key not in {"record_id", "object_validation_receipt"}}


def _local_record_issues(record: Any) -> list[str]:
    issues: list[str] = []
    if not isinstance(record, Mapping):
        return ["LOCAL_RECORD_NOT_MAPPING"]
    projection = _local_projection(record)
    try:
        expected_record_id = "ser01v1:" + digest(projection)
    except (TypeError, ValueError, UnicodeError):
        return ["LOCAL_RECORD_NOT_CANONICAL_JSON"]
    if record.get("record_id") != expected_record_id:
        issues.append("LOCAL_RECORD_ID_MISMATCH")
    if record.get("record_version") != LOCAL_RECORD_VERSION:
        issues.append("LOCAL_RECORD_VERSION_UNSUPPORTED")
    if record.get("status") != "PASS" or record.get("issues") != []:
        issues.append("LOCAL_VALIDATION_NOT_PASS")
    if record.get("scope") != LOCAL_SCOPE:
        issues.append("LOCAL_SCOPE_INVALID")
    for field, expected, code in (
        ("writes_performed_in_original", False, "ORIGINAL_WRITE_CLAIM_INVALID"),
        ("homologated", False, "HOMOLOGATION_CLAIM_INVALID"),
        ("runtime_validation", "NOT_RUN", "RUNTIME_CLAIM_INVALID"),
        ("execution_authenticated", False, "EXECUTION_AUTH_CLAIM_INVALID"),
        ("policy_promotion_authorized", False, "POLICY_AUTHORITY_CLAIM_INVALID"),
    ):
        if record.get(field) != expected:
            issues.append(code)
    if not isinstance(record.get("run_id"), str) or not record["run_id"]:
        issues.append("RUN_ID_INVALID")
    binding = record.get("binding")
    if not isinstance(binding, Mapping):
        return issues + ["BINDING_INVALID"]
    if binding.get("operation") != "create":
        issues.append("BINDING_OPERATION_INVALID")
    if binding.get("object_type") not in SUPPORTED_TYPES:
        issues.append("BINDING_OBJECT_TYPE_INVALID")
    if not _hex(binding.get("candidate_sha256"), 64):
        issues.append("BINDING_CANDIDATE_DIGEST_INVALID")
    if not _hex(binding.get("base_sha"), 40):
        issues.append("BINDING_BASE_SHA_INVALID")
    if not isinstance(binding.get("destination_relative"), str) or not binding["destination_relative"]:
        issues.append("BINDING_DESTINATION_INVALID")
    if not isinstance(binding.get("files"), list) or not binding["files"]:
        issues.append("BINDING_FILES_INVALID")
    before, after = record.get("original_before"), record.get("original_after")
    if not isinstance(before, Mapping) or before != after or before.get("status") != "":
        issues.append("ORIGINAL_PRESERVATION_INVALID")
    elif before.get("head") != binding.get("base_sha"):
        issues.append("ORIGINAL_BASE_MISMATCH")
    required_commands = set(REQUIRED_COMMANDS)
    if binding.get("object_type") in {"snippet", "script"}:
        required_commands.add("api_publica")
    commands = record.get("commands")
    if not isinstance(commands, list):
        issues.append("COMMAND_EVIDENCE_MISSING")
    else:
        names = [row.get("name") for row in commands if isinstance(row, Mapping)]
        if len(names) != len(commands) or len(set(names)) != len(names) or not required_commands <= set(names):
            issues.append("COMMAND_COVERAGE_INVALID")
        if any(not isinstance(row, Mapping) or type(row.get("exit_code")) is not int
               or row.get("exit_code") != 0 or row.get("process_cleanup") != "COMPLETE"
               or row.get("command_started") is not True for row in commands):
            issues.append("COMMAND_NOT_COMPLETE")
    required_checks = set(BASE_CHECKS)
    if binding.get("object_type") in {"snippet", "script"}:
        required_checks.add("canonical_public_api")
    if binding.get("object_type") == "readme":
        required_checks.add("canonical_aggregator_check")
    checks = record.get("checks")
    if not isinstance(checks, list) or not checks:
        issues.append("CHECK_EVIDENCE_MISSING")
    else:
        names = [row.get("name") for row in checks if isinstance(row, Mapping)]
        if len(names) != len(checks) or len(set(names)) != len(names) or not required_checks <= set(names):
            issues.append("CHECK_COVERAGE_INVALID")
        if any(not isinstance(row, Mapping) or row.get("status") != "PASS" for row in checks):
            issues.append("CHECK_NOT_PASS")
    return issues


def build_receipt(local_record: Mapping[str, Any]) -> dict[str, Any] | None:
    if _local_record_issues(local_record):
        return None
    projection = _local_projection(local_record)
    body = {
        "receipt_version": RECEIPT_VERSION,
        "skill": SKILL,
        "protected_surface": PROTECTED_SURFACE,
        "route": ROUTE,
        "status": "PASS",
        "run_id": local_record["run_id"],
        "local_record_id": local_record["record_id"],
        "local_record_sha256": digest(projection),
        "binding": copy.deepcopy(local_record["binding"]),
        "host": copy.deepcopy(local_record.get("host")),
        "claims": {
            "structural_validation": "PASS",
            "runtime_validation": "NOT_RUN",
            "writes_performed_in_original": False,
            "execution_authenticated": False,
            "human_authority_authenticated": False,
            "policy_promotion_authorized": False,
            "homologated": False,
        },
    }
    return {**body, "receipt_id": RECEIPT_ID_PREFIX + digest(body)}


def verify_receipt(receipt: Any, *, local_record: Mapping[str, Any] | None = None,
                   expected_run_id: str | None = None,
                   expected_base_sha: str | None = None,
                   expected_candidate_sha256: str | None = None) -> dict[str, Any]:
    issues: list[str] = []
    if not isinstance(receipt, Mapping):
        return {"valid": False, "issues": ["RECEIPT_NOT_MAPPING"],
                "verification_scope": "DOMAIN_RECEIPT_INTEGRITY_ONLY",
                "execution_reverified": False, "human_authority_authenticated": False,
                "policy_promotion_authorized": False}
    required = {"receipt_version", "receipt_id", "skill", "protected_surface", "route",
                "status", "run_id", "local_record_id", "local_record_sha256",
                "binding", "host", "claims"}
    if set(receipt) != required:
        issues.append("RECEIPT_FIELDS_INVALID")
    body = {k: copy.deepcopy(v) for k, v in receipt.items() if k != "receipt_id"}
    try:
        expected_id = RECEIPT_ID_PREFIX + digest(body)
    except (TypeError, ValueError, UnicodeError):
        expected_id = None
        issues.append("RECEIPT_NOT_CANONICAL_JSON")
    if receipt.get("receipt_id") != expected_id:
        issues.append("RECEIPT_ID_MISMATCH")
    if receipt.get("receipt_version") != RECEIPT_VERSION:
        issues.append("RECEIPT_VERSION_UNSUPPORTED")
    if receipt.get("skill") != SKILL or receipt.get("protected_surface") != PROTECTED_SURFACE:
        issues.append("RECEIPT_SURFACE_MISMATCH")
    if receipt.get("route") != ROUTE or receipt.get("status") != "PASS":
        issues.append("RECEIPT_ROUTE_OR_STATUS_INVALID")
    binding = receipt.get("binding")
    if not isinstance(binding, Mapping):
        issues.append("RECEIPT_BINDING_INVALID")
        binding = {}
    expected_claims = {"structural_validation": "PASS", "runtime_validation": "NOT_RUN",
                       "writes_performed_in_original": False, "execution_authenticated": False,
                       "human_authority_authenticated": False, "policy_promotion_authorized": False,
                       "homologated": False}
    if receipt.get("claims") != expected_claims:
        issues.append("RECEIPT_CLAIMS_INVALID")
    if expected_run_id is not None and receipt.get("run_id") != expected_run_id:
        issues.append("RUN_BINDING_MISMATCH")
    if expected_base_sha is not None and binding.get("base_sha") != expected_base_sha:
        issues.append("BASE_BINDING_MISMATCH")
    if expected_candidate_sha256 is not None and binding.get("candidate_sha256") != expected_candidate_sha256:
        issues.append("CANDIDATE_BINDING_MISMATCH")
    if local_record is not None:
        local_issues = _local_record_issues(local_record)
        if local_issues:
            issues.extend("LOCAL:" + item for item in local_issues)
        elif build_receipt(local_record) != dict(receipt):
            issues.append("LOCAL_RECORD_BINDING_MISMATCH")
    return {"valid": not issues, "issues": issues,
            "verification_scope": "DOMAIN_RECEIPT_INTEGRITY_ONLY",
            "execution_reverified": False, "human_authority_authenticated": False,
            "policy_promotion_authorized": False}
