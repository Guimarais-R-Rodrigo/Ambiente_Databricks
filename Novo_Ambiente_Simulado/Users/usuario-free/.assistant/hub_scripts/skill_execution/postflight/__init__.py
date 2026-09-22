from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping


POSTFLIGHT_VERSION = "1.0"
POSTFLIGHT_ID_PREFIX = "pf1:"
SUPPORTED_POLICY = "fail_closed"
SUPPORTED_STATES = {"PASS", "FAIL", "BLOCKED", "REVIEW"}


@dataclass(frozen=True)
class PostflightIssue:
    severity: str
    code: str
    message: str
    item_type: str | None = None
    item_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PostflightVerification:
    status: str
    valid: bool
    issues: tuple[str, ...]
    postflight_id: str | None = None
    completion_authorized: bool = False

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


def _is_hex_digest(value: Any, length: int = 64) -> bool:
    if not isinstance(value, str) or len(value) != length:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _state(issues: list[PostflightIssue]) -> str:
    severities = {issue.severity for issue in issues}
    if "BLOCKED" in severities:
        return "BLOCKED"
    if "FAIL" in severities:
        return "FAIL"
    if "REVIEW" in severities:
        return "REVIEW"
    return "PASS"


def _meaningful_handoff_value(value: Any, *, allow_empty: bool) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Mapping):
        return bool(value) or allow_empty
    if isinstance(value, (list, tuple, set)):
        return bool(value) or allow_empty
    return True


def _postflight_config(contract: Mapping[str, Any]) -> tuple[dict[str, Any] | None, list[PostflightIssue]]:
    issues: list[PostflightIssue] = []
    metadata = contract.get("metadata")
    if not isinstance(metadata, Mapping):
        issues.append(PostflightIssue("BLOCKED", "POSTFLIGHT_CONFIG_MISSING", "metadata do contrato ausente/inválido"))
        return None, issues
    raw = metadata.get("postflight")
    if not isinstance(raw, Mapping):
        issues.append(PostflightIssue("BLOCKED", "POSTFLIGHT_CONFIG_MISSING", "metadata.postflight ausente"))
        return None, issues
    if raw.get("schema_version") != POSTFLIGHT_VERSION:
        issues.append(
            PostflightIssue(
                "BLOCKED",
                "POSTFLIGHT_CONFIG_VERSION",
                f"schema_version de postflight não suportada: {raw.get('schema_version')!r}",
            )
        )
    if raw.get("policy") != SUPPORTED_POLICY:
        issues.append(
            PostflightIssue(
                "BLOCKED",
                "POSTFLIGHT_POLICY_UNSUPPORTED",
                f"policy de postflight não suportada: {raw.get('policy')!r}",
            )
        )
    handoff = raw.get("handoff")
    if not isinstance(handoff, Mapping):
        issues.append(PostflightIssue("BLOCKED", "HANDOFF_CONFIG_INVALID", "postflight.handoff deve ser objeto"))
    else:
        required = handoff.get("required")
        allow_empty = handoff.get("allow_empty", [])
        if not isinstance(required, list) or any(not isinstance(item, str) or not item for item in required):
            issues.append(PostflightIssue("BLOCKED", "HANDOFF_CONFIG_INVALID", "handoff.required deve ser lista de strings não vazias"))
        if not isinstance(allow_empty, list) or any(not isinstance(item, str) or not item for item in allow_empty):
            issues.append(PostflightIssue("BLOCKED", "HANDOFF_CONFIG_INVALID", "handoff.allow_empty deve ser lista de strings"))
    return dict(raw), issues


def _contract_items(contract: Mapping[str, Any], key: str) -> tuple[list[dict[str, Any]], list[PostflightIssue]]:
    raw = contract.get(key)
    if not isinstance(raw, list):
        return [], [PostflightIssue("BLOCKED", "CONTRACT_INVALID", f"{key} deve ser lista")]
    items: list[dict[str, Any]] = []
    issues: list[PostflightIssue] = []
    seen: set[str] = set()
    for index, value in enumerate(raw):
        if not isinstance(value, Mapping):
            issues.append(PostflightIssue("BLOCKED", "CONTRACT_INVALID", f"{key}[{index}] deve ser objeto"))
            continue
        item_id = value.get("id")
        if not isinstance(item_id, str) or not item_id or item_id in seen:
            issues.append(PostflightIssue("BLOCKED", "CONTRACT_INVALID", f"id inválido/duplicado em {key}[{index}]"))
            continue
        seen.add(item_id)
        items.append(dict(value))
    return items, issues


def _decision_index(trace: Mapping[str, Any]) -> tuple[dict[tuple[str, str], Mapping[str, Any]], list[PostflightIssue]]:
    raw = trace.get("decisions")
    if not isinstance(raw, list):
        return {}, [PostflightIssue("BLOCKED", "TRACE_DECISIONS_INVALID", "trace.decisions deve ser lista")]
    result: dict[tuple[str, str], Mapping[str, Any]] = {}
    issues: list[PostflightIssue] = []
    for value in raw:
        if not isinstance(value, Mapping):
            issues.append(PostflightIssue("BLOCKED", "TRACE_DECISIONS_INVALID", "decision deve ser objeto"))
            continue
        item_type = value.get("item_type")
        item_id = value.get("item_id")
        if item_type not in {"resource", "template"} or not isinstance(item_id, str) or not item_id:
            issues.append(PostflightIssue("BLOCKED", "TRACE_DECISIONS_INVALID", "decision sem item_type/item_id canônico"))
            continue
        key = (item_type, item_id)
        if key in result:
            issues.append(PostflightIssue("BLOCKED", "TRACE_DECISION_DUPLICATE", f"decision duplicada: {item_type}:{item_id}"))
            continue
        result[key] = value
    return result, issues


def _string_set(trace: Mapping[str, Any], key: str, issues: list[PostflightIssue]) -> set[str]:
    raw = trace.get(key)
    if not isinstance(raw, list) or any(not isinstance(item, str) or not item for item in raw):
        issues.append(PostflightIssue("BLOCKED", "TRACE_EVIDENCE_INVALID", f"trace.{key} deve ser lista de strings"))
        return set()
    return set(raw)


def _resource_evidence(
    item: Mapping[str, Any],
    *,
    decision: Mapping[str, Any],
    resolved: set[str],
    imported: set[str],
    called: set[str],
    completed: set[str],
    artifacts: Mapping[str, Any],
    issues: list[PostflightIssue],
) -> None:
    item_id = str(item["id"])
    evidence = item.get("evidence")
    if decision.get("resolved") is not True:
        issues.append(PostflightIssue("FAIL", "REQUIRED_RESOURCE_UNRESOLVED", f"recurso aplicável não foi resolvido: {item_id}", "resource", item_id))
        return
    if item_id not in resolved:
        issues.append(PostflightIssue("FAIL", "RESOURCE_RESOLUTION_NOT_EVIDENCED", f"receipt/trace não evidencia resolução de {item_id}", "resource", item_id))
    if evidence == "resolved":
        return
    if evidence == "imported":
        if item_id not in imported:
            issues.append(PostflightIssue("FAIL", "REQUIRED_RESOURCE_NOT_IMPORTED", f"recurso aplicável não foi importado: {item_id}", "resource", item_id))
        return
    if evidence == "call":
        if item_id not in called:
            issues.append(PostflightIssue("FAIL", "REQUIRED_RESOURCE_NOT_CALLED", f"recurso aplicável não foi chamado: {item_id}", "resource", item_id))
        elif item_id not in completed:
            issues.append(PostflightIssue("FAIL", "REQUIRED_RESOURCE_NOT_COMPLETED", f"recurso aplicável foi chamado mas não concluiu: {item_id}", "resource", item_id))
        return
    if evidence == "result":
        if item_id not in completed or item_id not in artifacts:
            issues.append(PostflightIssue("FAIL", "REQUIRED_RESULT_MISSING", f"resultado aplicável ausente: {item_id}", "resource", item_id))
        return
    if evidence in {"decision", "authorization"}:
        issues.append(PostflightIssue("REVIEW", "RESOURCE_EVIDENCE_REQUIRES_REVIEW", f"evidência {evidence!r} ainda exige regra específica: {item_id}", "resource", item_id))
        return
    issues.append(PostflightIssue("BLOCKED", "RESOURCE_EVIDENCE_UNSUPPORTED", f"evidence não suportada no postflight: {evidence!r}", "resource", item_id))


def _template_evidence(
    item: Mapping[str, Any],
    *,
    decision: Mapping[str, Any],
    templates_loaded: set[str],
    template_digests: Mapping[str, Any],
    issues: list[PostflightIssue],
) -> None:
    item_id = str(item["id"])
    if decision.get("resolved") is not True:
        issues.append(PostflightIssue("FAIL", "REQUIRED_TEMPLATE_UNRESOLVED", f"template aplicável não foi resolvido: {item_id}", "template", item_id))
        return
    if item.get("evidence") != "loaded":
        issues.append(PostflightIssue("BLOCKED", "TEMPLATE_EVIDENCE_UNSUPPORTED", f"template {item_id} exige evidence não suportada", "template", item_id))
        return
    if item_id not in templates_loaded:
        issues.append(PostflightIssue("FAIL", "REQUIRED_TEMPLATE_NOT_LOADED", f"template aplicável não foi carregado: {item_id}", "template", item_id))
        return
    digest = template_digests.get(item_id)
    if not _is_hex_digest(digest):
        issues.append(PostflightIssue("BLOCKED", "TEMPLATE_DIGEST_INVALID", f"digest ausente/inválido para template carregado: {item_id}", "template", item_id))


def _evaluate_contract_evidence(
    *,
    contract: Mapping[str, Any],
    trace: Mapping[str, Any],
    artifacts: Mapping[str, Any],
    issues: list[PostflightIssue],
) -> dict[str, Any]:
    resources, resource_contract_issues = _contract_items(contract, "resources")
    templates, template_contract_issues = _contract_items(contract, "templates")
    issues.extend(resource_contract_issues)
    issues.extend(template_contract_issues)
    decisions, decision_issues = _decision_index(trace)
    issues.extend(decision_issues)

    resolved = _string_set(trace, "resources_resolved", issues)
    imported = _string_set(trace, "resources_imported", issues)
    called = _string_set(trace, "resources_called", issues)
    completed = _string_set(trace, "resources_completed", issues)
    templates_loaded = _string_set(trace, "templates_loaded", issues)
    raw_template_digests = trace.get("template_digests")
    template_digests = raw_template_digests if isinstance(raw_template_digests, Mapping) else {}
    if not isinstance(raw_template_digests, Mapping):
        issues.append(PostflightIssue("BLOCKED", "TEMPLATE_DIGESTS_INVALID", "trace.template_digests deve ser objeto"))

    checked_required: list[str] = []
    checked_conditional: list[str] = []
    skipped_conditional: list[dict[str, str]] = []

    for item_type, items in (("resource", resources), ("template", templates)):
        for item in items:
            item_id = str(item["id"])
            policy = item.get("policy")
            decision = decisions.get((item_type, item_id))
            if decision is None:
                issues.append(PostflightIssue("BLOCKED", "DECISION_MISSING", f"decision ausente para {item_type}:{item_id}", item_type, item_id))
                continue
            if policy == "optional":
                continue
            applicable = decision.get("applicable")
            if policy == "required":
                if applicable is not True:
                    issues.append(PostflightIssue("BLOCKED", "REQUIRED_DECISION_INVALID", f"requisito required não ficou applicable=true: {item_id}", item_type, item_id))
                    continue
                checked_required.append(f"{item_type}:{item_id}")
            elif policy == "conditional":
                if not isinstance(applicable, bool):
                    issues.append(PostflightIssue("BLOCKED", "CONDITIONAL_DECISION_INVALID", f"applicability não booleana: {item_id}", item_type, item_id))
                    continue
                if not applicable:
                    reason = decision.get("reason")
                    if not isinstance(reason, str) or not reason.strip():
                        issues.append(PostflightIssue("REVIEW", "CONDITIONAL_SKIP_UNJUSTIFIED", f"skip condicional sem justificativa: {item_id}", item_type, item_id))
                        reason = "<sem justificativa>"
                    skipped_conditional.append({"item_type": item_type, "item_id": item_id, "reason": reason})
                    continue
                checked_conditional.append(f"{item_type}:{item_id}")
            else:
                issues.append(PostflightIssue("BLOCKED", "POLICY_UNSUPPORTED", f"policy não suportada: {policy!r}", item_type, item_id))
                continue

            if item_type == "resource":
                _resource_evidence(
                    item,
                    decision=decision,
                    resolved=resolved,
                    imported=imported,
                    called=called,
                    completed=completed,
                    artifacts=artifacts,
                    issues=issues,
                )
            else:
                _template_evidence(
                    item,
                    decision=decision,
                    templates_loaded=templates_loaded,
                    template_digests=template_digests,
                    issues=issues,
                )

    return {
        "checked_required": sorted(checked_required),
        "checked_conditional": sorted(checked_conditional),
        "skipped_conditional": sorted(skipped_conditional, key=lambda item: (item["item_type"], item["item_id"])),
    }


def build_postflight(
    payload: Mapping[str, Any],
    *,
    contract: Mapping[str, Any],
    receipt_verification: Mapping[str, Any],
    handoff: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Constrói Postflight V1 fail-closed a partir de evidência já vinculada pelo Receipt."""
    issues: list[PostflightIssue] = []
    config, config_issues = _postflight_config(contract)
    issues.extend(config_issues)

    trace = payload.get("trace") if isinstance(payload, Mapping) else None
    receipt = payload.get("receipt") if isinstance(payload, Mapping) else None
    artifacts = payload.get("artifacts", {}) if isinstance(payload, Mapping) else {}
    if not isinstance(trace, Mapping):
        issues.append(PostflightIssue("BLOCKED", "TRACE_MISSING", "payload sem trace estruturado"))
        trace = {}
    if not isinstance(receipt, Mapping):
        issues.append(PostflightIssue("BLOCKED", "RECEIPT_MISSING", "payload sem Receipt estruturado"))
        receipt = {}
    if not isinstance(artifacts, Mapping):
        issues.append(PostflightIssue("BLOCKED", "ARTIFACTS_INVALID", "payload.artifacts deve ser objeto"))
        artifacts = {}

    receipt_status = receipt_verification.get("status") if isinstance(receipt_verification, Mapping) else None
    receipt_valid = receipt_verification.get("valid") if isinstance(receipt_verification, Mapping) else False
    if receipt_status != "VALID" or receipt_valid is not True:
        issues.append(PostflightIssue("BLOCKED", "RECEIPT_NOT_VALID", f"Receipt não está VALID: {receipt_status!r}"))

    skill = contract.get("skill")
    if not isinstance(skill, str) or not skill:
        issues.append(PostflightIssue("BLOCKED", "CONTRACT_INVALID", "contract.skill ausente/inválido"))
        skill = "<invalid>"
    if trace.get("skill") != skill or receipt.get("skill") != skill:
        issues.append(PostflightIssue("BLOCKED", "SKILL_BINDING_MISMATCH", "skill do contrato/trace/Receipt diverge"))

    artifacts_digest = trace.get("artifacts_digest")
    if not _is_hex_digest(artifacts_digest):
        issues.append(PostflightIssue("BLOCKED", "ARTIFACTS_DIGEST_MISSING", "trace.artifacts_digest ausente/inválido"))
    elif artifacts_digest != sha256_digest(artifacts):
        issues.append(PostflightIssue("BLOCKED", "ARTIFACTS_DIGEST_MISMATCH", "artifacts foram alterados após a execução"))

    coverage = _evaluate_contract_evidence(contract=contract, trace=trace, artifacts=artifacts, issues=issues)

    handoff_payload = dict(handoff) if isinstance(handoff, Mapping) else {}
    if not isinstance(handoff, Mapping):
        issues.append(PostflightIssue("REVIEW", "HANDOFF_MISSING", "handoff final ausente"))
    if config is not None:
        handoff_config = config.get("handoff")
        if isinstance(handoff_config, Mapping):
            required = handoff_config.get("required", [])
            allow_empty = set(handoff_config.get("allow_empty", []))
            if isinstance(required, list):
                for field in required:
                    if field not in handoff_payload:
                        issues.append(PostflightIssue("REVIEW", "HANDOFF_FIELD_MISSING", f"campo obrigatório de handoff ausente: {field}", "handoff", field))
                    elif not _meaningful_handoff_value(handoff_payload[field], allow_empty=field in allow_empty):
                        issues.append(PostflightIssue("REVIEW", "HANDOFF_FIELD_EMPTY", f"campo obrigatório de handoff vazio: {field}", "handoff", field))

    status = _state(issues)
    completion_authorized = status == "PASS"
    receipt_id = receipt.get("receipt_id") if isinstance(receipt.get("receipt_id"), str) else None
    run_id = trace.get("run_id") if isinstance(trace.get("run_id"), str) else None
    body = {
        "postflight_version": POSTFLIGHT_VERSION,
        "status": status,
        "completion_authorized": completion_authorized,
        "skill": skill,
        "run_id": run_id,
        "receipt_status": receipt_status,
        "receipt_id": receipt_id,
        "policy": SUPPORTED_POLICY,
        "contract_schema_version": contract.get("schema_version"),
        "bindings": {
            "trace_sha256": sha256_digest(trace),
            "artifacts_sha256": sha256_digest(artifacts),
            "handoff_sha256": sha256_digest(handoff_payload),
        },
        "coverage": coverage,
        "issues": [issue.to_dict() for issue in issues],
        "writes_performed": False,
    }
    return {**body, "postflight_id": POSTFLIGHT_ID_PREFIX + sha256_digest(body)}


def verify_postflight(
    final_payload: Mapping[str, Any],
    *,
    contract: Mapping[str, Any],
    receipt_verification: Mapping[str, Any],
) -> PostflightVerification:
    if not isinstance(final_payload, Mapping):
        return PostflightVerification("MALFORMED", False, ("FINAL_PAYLOAD_NOT_MAPPING",))
    observed = final_payload.get("postflight")
    if observed is None:
        return PostflightVerification("ABSENT", False, ("POSTFLIGHT_ABSENT",))
    if not isinstance(observed, Mapping):
        return PostflightVerification("MALFORMED", False, ("POSTFLIGHT_NOT_MAPPING",))
    expected = build_postflight(
        final_payload,
        contract=contract,
        receipt_verification=receipt_verification,
        handoff=final_payload.get("handoff") if isinstance(final_payload.get("handoff"), Mapping) else None,
    )
    if dict(observed) != expected:
        return PostflightVerification(
            "INVALID",
            False,
            ("POSTFLIGHT_BINDING_MISMATCH",),
            postflight_id=observed.get("postflight_id") if isinstance(observed.get("postflight_id"), str) else None,
            completion_authorized=False,
        )
    authorized = observed.get("completion_authorized") is True and observed.get("status") == "PASS"
    return PostflightVerification(
        "VALID",
        True,
        (),
        postflight_id=observed.get("postflight_id") if isinstance(observed.get("postflight_id"), str) else None,
        completion_authorized=authorized,
    )
