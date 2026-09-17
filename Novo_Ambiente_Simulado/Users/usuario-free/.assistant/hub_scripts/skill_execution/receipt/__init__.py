from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping


RECEIPT_VERSION = "1.0"
SUPPORTED_RECEIPT_VERSIONS = {RECEIPT_VERSION}
SUPPORTED_TRACE_VERSION = "0.1"
CANONICAL_SERIALIZATION = "json-utf8-sort-keys-compact"
DIGEST_ALGORITHM = "sha256"
RECEIPT_ID_PREFIX = "er1:"


@dataclass(frozen=True)
class ReceiptVerification:
    status: str
    valid: bool
    issues: tuple[str, ...]
    receipt_version: str | None = None
    receipt_id: str | None = None
    run_id: str | None = None
    canonical_compliance: str = "FAIL"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")


def sha256_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _is_hex_digest(value: Any, length: int) -> bool:
    if not isinstance(value, str) or len(value) != length:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _normalized_strings(raw: Any) -> list[str] | None:
    if not isinstance(raw, list) or any(not isinstance(item, str) or not item for item in raw):
        return None
    return sorted(set(raw))


def _normalized_decisions(raw: Any) -> list[dict[str, Any]] | None:
    if not isinstance(raw, list):
        return None
    normalized: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, Mapping):
            return None
        item_id = item.get("item_id")
        item_type = item.get("item_type")
        applicable = item.get("applicable")
        resolved = item.get("resolved")
        if not isinstance(item_id, str) or not item_id:
            return None
        if item_type not in {"resource", "template"}:
            return None
        if applicable is not None and not isinstance(applicable, bool):
            return None
        if resolved is not None and not isinstance(resolved, bool):
            return None
        normalized.append(
            {
                "item_id": item_id,
                "item_type": item_type,
                "applicable": applicable,
                "resolved": resolved,
            }
        )
    return sorted(normalized, key=lambda item: (item["item_type"], item["item_id"]))


def _provenance_summary(raw: Any) -> dict[str, dict[str, Any]] | None:
    if not isinstance(raw, Mapping):
        return None
    summary: dict[str, dict[str, Any]] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not isinstance(value, Mapping):
            return None
        source = value.get("source")
        if source not in {"runtime_derived", "user_intent", "agent_declared"}:
            return None
        conflict = value.get("conflict", False)
        if not isinstance(conflict, bool):
            return None
        summary[key] = {
            "source": source,
            "conflict": conflict,
        }
    return dict(sorted(summary.items()))


def _receipt_body(
    trace: Mapping[str, Any],
    result: Any,
    *,
    expected_skill: str,
    expected_entrypoint: str,
    protected_primitive: str,
) -> dict[str, Any] | None:
    if trace.get("trace_version") != SUPPORTED_TRACE_VERSION:
        return None
    if trace.get("skill") != expected_skill or trace.get("entrypoint") != expected_entrypoint:
        return None
    if trace.get("status") != "PASS" or trace.get("preflight_status") != "PASS":
        return None
    run_id = trace.get("run_id")
    manifest_name = trace.get("manifest")
    manifest_digest = trace.get("manifest_digest")
    contract_digest = trace.get("contract_digest")
    runner_digest = trace.get("runner_digest")
    input_digest = trace.get("input_digest")
    output_digest = trace.get("output_digest")
    if not isinstance(run_id, str) or not run_id:
        return None
    if not isinstance(manifest_name, str) or not manifest_name:
        return None
    if not _is_hex_digest(manifest_digest, 64):
        return None
    if not _is_hex_digest(contract_digest, 40) or not _is_hex_digest(runner_digest, 40):
        return None
    if not _is_hex_digest(input_digest, 64) or not _is_hex_digest(output_digest, 64):
        return None
    if output_digest != sha256_digest(result):
        return None
    resolved = _normalized_strings(trace.get("resources_resolved"))
    called = _normalized_strings(trace.get("resources_called"))
    completed = _normalized_strings(trace.get("resources_completed"))
    if resolved is None or called is None or completed is None:
        return None
    if protected_primitive not in called or protected_primitive not in completed:
        return None
    decisions = _normalized_decisions(trace.get("decisions"))
    provenance = _provenance_summary(trace.get("context_provenance"))
    if decisions is None or provenance is None:
        return None
    numeric = provenance.get("numeric_columns")
    if not isinstance(numeric, Mapping):
        return None
    if numeric.get("source") != "runtime_derived" or numeric.get("conflict") is not False:
        return None
    blocking = trace.get("blocking_issues")
    if not isinstance(blocking, list) or blocking:
        return None
    if trace.get("fallback_used") is not False or trace.get("writes_performed") is not False:
        return None

    return {
        "receipt_version": RECEIPT_VERSION,
        "run_id": run_id,
        "skill": expected_skill,
        "entrypoint": expected_entrypoint,
        "execution_status": "PASS",
        "canonical_compliance": "PASS",
        "preflight_status": "PASS",
        "release": {
            "manifest_name": manifest_name,
            "manifest_sha256": manifest_digest,
            "contract_git_blob_sha1": contract_digest,
            "runner_git_blob_sha1": runner_digest,
        },
        "bindings": {
            "trace_sha256": sha256_digest(trace),
            "input_sha256": input_digest,
            "output_sha256": output_digest,
        },
        "resources": {
            "resolved": resolved,
            "imported": {"status": "NOT_OBSERVABLE", "items": []},
            "called": called,
            "completed": completed,
            "protected_primitive": protected_primitive,
        },
        "decisions": decisions,
        "templates_consumed": {"status": "NOT_OBSERVABLE", "items": []},
        "provenance_summary": provenance,
        "fallback_used": False,
        "writes_performed": False,
        "blocking_issue_codes": [],
        "integrity": {
            "release_integrity": "PASS",
            "canonical_serialization": CANONICAL_SERIALIZATION,
            "digest_algorithm": DIGEST_ALGORITHM,
            "receipt_id_scheme": "er1:sha256(body)",
        },
    }


def build_execution_receipt(
    trace: Mapping[str, Any],
    result: Any,
    *,
    expected_skill: str,
    expected_entrypoint: str,
    protected_primitive: str,
) -> dict[str, Any] | None:
    """Constrói Receipt V1 apenas a partir de evidência canônica coerente."""
    if not isinstance(trace, Mapping):
        return None
    body = _receipt_body(
        trace,
        result,
        expected_skill=expected_skill,
        expected_entrypoint=expected_entrypoint,
        protected_primitive=protected_primitive,
    )
    if body is None:
        return None
    return {
        **body,
        "receipt_id": RECEIPT_ID_PREFIX + sha256_digest(body),
    }


def _malformed_issues(receipt: Mapping[str, Any]) -> tuple[str, ...]:
    required = {
        "receipt_version",
        "receipt_id",
        "run_id",
        "skill",
        "entrypoint",
        "execution_status",
        "canonical_compliance",
        "preflight_status",
        "release",
        "bindings",
        "resources",
        "decisions",
        "templates_consumed",
        "provenance_summary",
        "fallback_used",
        "writes_performed",
        "blocking_issue_codes",
        "integrity",
    }
    issues = [f"RECEIPT_FIELD_MISSING:{item}" for item in sorted(required - set(receipt))]

    for key in (
        "receipt_version",
        "receipt_id",
        "run_id",
        "skill",
        "entrypoint",
        "execution_status",
        "canonical_compliance",
        "preflight_status",
    ):
        if key in receipt and (not isinstance(receipt[key], str) or not receipt[key]):
            issues.append(f"RECEIPT_FIELD_TYPE:{key}")

    release = receipt.get("release")
    if release is not None:
        if not isinstance(release, Mapping):
            issues.append("RECEIPT_FIELD_TYPE:release")
        else:
            release_required = {
                "manifest_name",
                "manifest_sha256",
                "contract_git_blob_sha1",
                "runner_git_blob_sha1",
            }
            issues.extend(
                f"RECEIPT_FIELD_MISSING:release.{item}"
                for item in sorted(release_required - set(release))
            )
            if "manifest_name" in release and (
                not isinstance(release["manifest_name"], str) or not release["manifest_name"]
            ):
                issues.append("RECEIPT_FIELD_TYPE:release.manifest_name")
            for key, length in (
                ("manifest_sha256", 64),
                ("contract_git_blob_sha1", 40),
                ("runner_git_blob_sha1", 40),
            ):
                if key in release and not _is_hex_digest(release[key], length):
                    issues.append(f"RECEIPT_FIELD_TYPE:release.{key}")

    bindings = receipt.get("bindings")
    if bindings is not None:
        if not isinstance(bindings, Mapping):
            issues.append("RECEIPT_FIELD_TYPE:bindings")
        else:
            binding_required = {"trace_sha256", "input_sha256", "output_sha256"}
            issues.extend(
                f"RECEIPT_FIELD_MISSING:bindings.{item}"
                for item in sorted(binding_required - set(bindings))
            )
            for key in binding_required:
                if key in bindings and not _is_hex_digest(bindings[key], 64):
                    issues.append(f"RECEIPT_FIELD_TYPE:bindings.{key}")

    resources = receipt.get("resources")
    if resources is not None:
        if not isinstance(resources, Mapping):
            issues.append("RECEIPT_FIELD_TYPE:resources")
        else:
            resource_required = {"resolved", "imported", "called", "completed", "protected_primitive"}
            issues.extend(
                f"RECEIPT_FIELD_MISSING:resources.{item}"
                for item in sorted(resource_required - set(resources))
            )
            for key in ("resolved", "called", "completed"):
                if key in resources and _normalized_strings(resources[key]) is None:
                    issues.append(f"RECEIPT_FIELD_TYPE:resources.{key}")
            if "protected_primitive" in resources and (
                not isinstance(resources["protected_primitive"], str)
                or not resources["protected_primitive"]
            ):
                issues.append("RECEIPT_FIELD_TYPE:resources.protected_primitive")
            imported = resources.get("imported")
            if imported is not None and (
                not isinstance(imported, Mapping)
                or imported.get("status") != "NOT_OBSERVABLE"
                or imported.get("items") != []
            ):
                issues.append("RECEIPT_FIELD_TYPE:resources.imported")

    decisions = receipt.get("decisions")
    if decisions is not None and _normalized_decisions(decisions) is None:
        issues.append("RECEIPT_FIELD_TYPE:decisions")

    templates_consumed = receipt.get("templates_consumed")
    if templates_consumed is not None and (
        not isinstance(templates_consumed, Mapping)
        or templates_consumed.get("status") != "NOT_OBSERVABLE"
        or templates_consumed.get("items") != []
    ):
        issues.append("RECEIPT_FIELD_TYPE:templates_consumed")

    provenance = receipt.get("provenance_summary")
    if provenance is not None and _provenance_summary(provenance) is None:
        issues.append("RECEIPT_FIELD_TYPE:provenance_summary")

    for key in ("fallback_used", "writes_performed"):
        if key in receipt and not isinstance(receipt[key], bool):
            issues.append(f"RECEIPT_FIELD_TYPE:{key}")

    blocking = receipt.get("blocking_issue_codes")
    if blocking is not None and (
        not isinstance(blocking, list)
        or any(not isinstance(item, str) or not item for item in blocking)
    ):
        issues.append("RECEIPT_FIELD_TYPE:blocking_issue_codes")

    integrity = receipt.get("integrity")
    if integrity is not None:
        if not isinstance(integrity, Mapping):
            issues.append("RECEIPT_FIELD_TYPE:integrity")
        else:
            integrity_required = {
                "release_integrity",
                "canonical_serialization",
                "digest_algorithm",
                "receipt_id_scheme",
            }
            issues.extend(
                f"RECEIPT_FIELD_MISSING:integrity.{item}"
                for item in sorted(integrity_required - set(integrity))
            )

    return tuple(issues)


def verify_execution_receipt(
    payload: Mapping[str, Any],
    *,
    expected_skill: str,
    expected_entrypoint: str,
    protected_primitive: str,
    expected_run_id: str | None = None,
    expected_release: Mapping[str, str] | None = None,
    release_integrity_ok: bool = True,
) -> ReceiptVerification:
    """Verifica Receipt V1 sem impor postflight/conclusão de produção."""
    if not isinstance(payload, Mapping):
        return ReceiptVerification("MALFORMED", False, ("PAYLOAD_NOT_MAPPING",))
    receipt = payload.get("receipt")
    if receipt is None:
        return ReceiptVerification("ABSENT", False, ("RECEIPT_ABSENT",))
    if not isinstance(receipt, Mapping):
        return ReceiptVerification("MALFORMED", False, ("RECEIPT_NOT_MAPPING",))

    version = receipt.get("receipt_version")
    if version is None:
        return ReceiptVerification("MALFORMED", False, ("RECEIPT_FIELD_MISSING:receipt_version",))
    if version not in SUPPORTED_RECEIPT_VERSIONS:
        return ReceiptVerification(
            "UNSUPPORTED_VERSION",
            False,
            ("RECEIPT_VERSION_UNSUPPORTED",),
            receipt_version=str(version),
            receipt_id=receipt.get("receipt_id") if isinstance(receipt.get("receipt_id"), str) else None,
            run_id=receipt.get("run_id") if isinstance(receipt.get("run_id"), str) else None,
        )

    malformed = _malformed_issues(receipt)
    if malformed:
        return ReceiptVerification(
            "MALFORMED",
            False,
            malformed,
            receipt_version=RECEIPT_VERSION,
            receipt_id=receipt.get("receipt_id") if isinstance(receipt.get("receipt_id"), str) else None,
            run_id=receipt.get("run_id") if isinstance(receipt.get("run_id"), str) else None,
        )

    receipt_dict = dict(receipt)
    receipt_id = receipt_dict.pop("receipt_id")
    expected_receipt_id = RECEIPT_ID_PREFIX + sha256_digest(receipt_dict)
    if receipt_id != expected_receipt_id:
        return ReceiptVerification(
            "INVALID",
            False,
            ("RECEIPT_ID_MISMATCH",),
            receipt_version=RECEIPT_VERSION,
            receipt_id=receipt_id,
            run_id=receipt.get("run_id"),
        )

    trace = payload.get("trace")
    if not isinstance(trace, Mapping):
        return ReceiptVerification(
            "INCOMPATIBLE",
            False,
            ("TRACE_MISSING_OR_INVALID",),
            receipt_version=RECEIPT_VERSION,
            receipt_id=receipt_id,
            run_id=receipt.get("run_id"),
        )

    observed_run_id = receipt.get("run_id")
    if expected_run_id is not None and (
        observed_run_id != expected_run_id or trace.get("run_id") != expected_run_id
    ):
        return ReceiptVerification(
            "STALE_REPLAYED",
            False,
            ("RUN_ID_STALE",),
            receipt_version=RECEIPT_VERSION,
            receipt_id=receipt_id,
            run_id=observed_run_id,
        )

    expected = build_execution_receipt(
        trace,
        payload.get("result"),
        expected_skill=expected_skill,
        expected_entrypoint=expected_entrypoint,
        protected_primitive=protected_primitive,
    )
    if expected is None:
        return ReceiptVerification(
            "INCOMPATIBLE",
            False,
            ("UNDERLYING_EXECUTION_NOT_CANONICAL",),
            receipt_version=RECEIPT_VERSION,
            receipt_id=receipt_id,
            run_id=observed_run_id,
        )
    if dict(receipt) != expected:
        return ReceiptVerification(
            "INCOMPATIBLE",
            False,
            ("RECEIPT_BINDING_MISMATCH",),
            receipt_version=RECEIPT_VERSION,
            receipt_id=receipt_id,
            run_id=observed_run_id,
        )

    if not release_integrity_ok:
        return ReceiptVerification(
            "INCOMPATIBLE",
            False,
            ("CURRENT_RELEASE_INTEGRITY_FAILED",),
            receipt_version=RECEIPT_VERSION,
            receipt_id=receipt_id,
            run_id=observed_run_id,
        )

    if expected_release is not None:
        release = receipt.get("release")
        assert isinstance(release, Mapping)
        for key, value in expected_release.items():
            if release.get(key) != value:
                return ReceiptVerification(
                    "INCOMPATIBLE",
                    False,
                    (f"CURRENT_RELEASE_MISMATCH:{key}",),
                    receipt_version=RECEIPT_VERSION,
                    receipt_id=receipt_id,
                    run_id=observed_run_id,
                )

    return ReceiptVerification(
        "VALID",
        True,
        (),
        receipt_version=RECEIPT_VERSION,
        receipt_id=receipt_id,
        run_id=observed_run_id,
        canonical_compliance="PASS",
    )
