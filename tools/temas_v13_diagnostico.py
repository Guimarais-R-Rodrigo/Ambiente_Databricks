"""Observabilidade e diagnóstico local V13-S4.

Consome somente relatórios estruturados S2/S3 e um checklist de evidência por
tipo. Não usa rede, cliente Databricks, credenciais nem executa mutação. A saída
é sanitizada: mensagens, ids, caminhos e referências arbitrárias da entrada nunca
são ecoados; somente enums/códigos estáveis conhecidos aparecem no relatório.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DIAGNOSTIC_VERSION = 1
ENGINE = "V13-S4"
MAX_INPUT_BYTES = 262_144

STATUSES = {"PASS", "BLOCKED", "FAIL", "NOT_APPLICABLE"}
STATUS_PRIORITY = {"NOT_APPLICABLE": 0, "PASS": 1, "BLOCKED": 2, "FAIL": 3}
EVIDENCE_KINDS = {
    "git_ci",
    "artifact",
    "authorization",
    "environment_identity",
    "rollback",
    "human",
    "browser_runtime",
}
EVIDENCE_STATES = {"REFERENCED", "MISSING", "NOT_APPLICABLE"}

SOURCE_CODES = {
    "V13-S2": {
        "REQUEST_VALID", "REQUEST_TYPE", "REQUEST_FIELDS", "REQUEST_VERSION",
        "REQUEST_MODE", "REQUEST_OPERATIONS", "REQUEST_OPERATION_COUNT",
        "REQUEST_OPERATION_DUPLICATE", "OPERATION_FIELDS", "OPERATION_INPUTS",
        "S1_CONTRACT_VALID", "S1_CONTRACT_INVALID", "SURFACE_ACTION_VALID",
        "SURFACE_UNKNOWN", "ACTION_UNKNOWN", "PATH_INVALID", "PATH_MISSING",
        "THEME_VALID", "THEME_INPUT_REQUIRED", "THEME_INVALID",
        "THEME_HASH_STALE", "CONTEXT_INCOMPATIBLE", "BUNDLE_VALID",
        "BUNDLE_INPUT_REQUIRED", "BUNDLE_INCOMPLETE", "APP_BUNDLE_VALID",
        "APP_BUNDLE_INPUT_REQUIRED", "APP_BUNDLE_INVALID", "APP_STORAGE_VALID",
        "APP_STORAGE_NOT_APPLICABLE", "APP_STORAGE_PRECONDITION",
        "AIBI_PROJECTION_VALID", "AIBI_BINDING_VALID",
        "AIBI_BINDING_NOT_APPLICABLE", "AIBI_BINDING_INPUT_REQUIRED",
        "AIBI_BINDING_INVALID", "AIBI_CAPABILITY_FORBIDDEN",
        "NATIVE_TEMPLATE_HASH_STALE", "NATIVE_TEMPLATE_SYNTHETIC",
        "JSON_POINTER_MISSING", "WORKSPACE_POLICY_VALID",
        "AUTHORIZATION_NOT_REQUIRED", "AUTHORIZATION_REQUIRED",
        "AUTHORIZATION_DECLARED", "AUTHORIZATION_CANONICALLY_BLOCKED",
        "IDENTITY_NOT_REQUIRED", "IDENTITY_REQUIRED", "IDENTITY_LIVE_UNVERIFIED",
        "ROLLBACK_NOT_REQUIRED", "ROLLBACK_NOT_PREPARED", "ROLLBACK_PREPARED",
        "ROLLBACK_CANONICALLY_BLOCKED",
    },
    "V13-S3": {
        "REQUEST_VALID", "REQUEST_TYPE", "REQUEST_FIELDS", "REQUEST_VERSION",
        "REQUEST_MODE", "ARTIFACT_DESCRIPTOR", "ARTIFACT_PATH_INVALID",
        "ARTIFACT_INVALID", "ARTIFACT_SOURCE_STALE", "ARTIFACT_READY",
        "TREE_CLEAN", "TREE_DIRTY", "GIT_UNAVAILABLE", "PREFLIGHT_PASS",
        "PREFLIGHT_BLOCKED", "PREFLIGHT_FAILED", "PREFLIGHT_BINDING_MISMATCH",
        "LKG_NOT_REQUIRED", "LKG_REQUIRED", "LKG_DESCRIPTOR_INVALID",
        "LKG_ARTIFACT_INVALID", "LKG_REFERENCE_VALID", "UPDATE_COMPATIBLE",
        "UPDATE_INCOMPATIBLE", "STAGING_VERIFIED", "ROLLBACK_DISCARD_VERIFIED",
        "ROLLBACK_RESTORE_VERIFIED", "LOCAL_OPERATION_FAILED",
    },
}

FAILURE_STAGES = (
    "INPUT_CONTRACT",
    "CANONICAL_CONTRACT",
    "ARTIFACT_INTEGRITY",
    "GIT_STATE",
    "PREFLIGHT_READINESS",
    "GOVERNANCE_AUTHORIZATION",
    "ENVIRONMENT_IDENTITY",
    "RECOVERY_ROLLBACK",
    "COMPATIBILITY_LKG",
    "STAGING_EXECUTION",
    "EVIDENCE_GAP",
)

REQUIRED_EVIDENCE = {
    "INPUT_CONTRACT": {"git_ci"},
    "CANONICAL_CONTRACT": {"git_ci"},
    "ARTIFACT_INTEGRITY": {"artifact"},
    "GIT_STATE": {"git_ci"},
    "PREFLIGHT_READINESS": {"git_ci"},
    "GOVERNANCE_AUTHORIZATION": {"authorization"},
    "ENVIRONMENT_IDENTITY": {"environment_identity"},
    "RECOVERY_ROLLBACK": {"rollback"},
    "COMPATIBILITY_LKG": {"artifact", "rollback"},
    "STAGING_EXECUTION": {"artifact", "rollback"},
    "EVIDENCE_GAP": set(),
}

NEXT_ACTION = {
    "INPUT_CONTRACT": "Corrigir somente a forma/entrada e repetir o owner que recusou o request.",
    "CANONICAL_CONTRACT": "Voltar ao owner canônico do contrato; não inventar campo, contexto ou capacidade.",
    "ARTIFACT_INTEGRITY": "Regenerar ou revalidar o artefato a partir da fonte aprovada; não editar hash manualmente.",
    "GIT_STATE": "Restaurar um checkout identificável e limpo antes de repetir release/preflight.",
    "PREFLIGHT_READINESS": "Resolver o bloqueio/falha apontado pelo S2 antes de avançar no ciclo operacional.",
    "GOVERNANCE_AUTHORIZATION": "Obter autorização específica pelo fluxo existente; o diagnóstico não concede autorização.",
    "ENVIRONMENT_IDENTITY": "Verificar identidade/permissão/recurso no ambiente autorizado; CI local não substitui esse gate.",
    "RECOVERY_ROLLBACK": "Preparar ou provar rollback antes de qualquer mutação persistente.",
    "COMPATIBILITY_LKG": "Identificar LKG real e compatível; não fazer migração automática fora do contrato.",
    "STAGING_EXECUTION": "Interromper o ciclo, preservar evidência e repetir staging/rollback somente após corrigir a causa.",
    "EVIDENCE_GAP": "Coletar a classe de evidência faltante; ausência de evidência não pode ser promovida a PASS.",
    "NO_FAILURE": "Nenhuma correção é indicada por este evento; mantenha o gate de evidência aplicável.",
    "NOT_APPLICABLE": "Nenhuma ação é exigida para esta etapa não aplicável.",
    "UNKNOWN": "Parar e atualizar a taxonomia antes de interpretar um código não registrado.",
}

SAFE_SUMMARY = {
    "INPUT_CONTRACT": "A entrada não atende ao contrato esperado.",
    "CANONICAL_CONTRACT": "Um contrato canônico recusou a operação.",
    "ARTIFACT_INTEGRITY": "A integridade/identidade do artefato não pôde ser comprovada.",
    "GIT_STATE": "O estado Git não atende ao gate operacional.",
    "PREFLIGHT_READINESS": "O preflight não liberou a operação.",
    "GOVERNANCE_AUTHORIZATION": "A autorização necessária não está disponível no escopo observado.",
    "ENVIRONMENT_IDENTITY": "Identidade, permissão ou precondição de ambiente não foi comprovada.",
    "RECOVERY_ROLLBACK": "O rollback requerido não está preparado ou comprovado.",
    "COMPATIBILITY_LKG": "A referência/compatibilidade de last-known-good não foi comprovada.",
    "STAGING_EXECUTION": "Staging ou recuperação local não terminou de forma comprovada.",
    "EVIDENCE_GAP": "Existe uma classe de evidência obrigatória ausente.",
    "NO_FAILURE": "A etapa observada concluiu sem falha no relatório de origem.",
    "NOT_APPLICABLE": "A etapa observada foi marcada como não aplicável.",
    "UNKNOWN": "O relatório contém um código fora da taxonomia registrada.",
}

DIAGNOSTIC_CODES = {
    "DIAG_REQUEST_VALID", "DIAG_REQUEST_TYPE", "DIAG_REQUEST_FIELDS",
    "DIAG_REQUEST_VERSION", "SOURCE_REPORT_TYPE", "SOURCE_ENGINE_UNSUPPORTED",
    "SOURCE_SHAPE_INVALID", "SOURCE_STATUS_INVALID", "SOURCE_STATUS_MISMATCH",
    "SOURCE_CHECK_INVALID", "SOURCE_CODE_UNREGISTERED", "SOURCE_BOUNDARY_VIOLATION",
    "EVIDENCE_TYPE", "EVIDENCE_KIND", "EVIDENCE_STATE", "EVIDENCE_DUPLICATE",
    "EVIDENCE_MISSING", "EVIDENCE_REFERENCED", "EVIDENCE_NOT_APPLICABLE",
}

_CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")


class DiagnosticRequestError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        self.safe_message = message
        super().__init__(f"{code}: {message}")


def _max_status(statuses: list[str]) -> str:
    return max(statuses, key=STATUS_PRIORITY.__getitem__, default="NOT_APPLICABLE")


def _stage_for(code: str) -> str:
    if code.startswith(("REQUEST_", "OPERATION_")) or code in {
        "SURFACE_ACTION_VALID", "SURFACE_UNKNOWN", "ACTION_UNKNOWN", "PATH_INVALID",
        "PATH_MISSING", "THEME_INPUT_REQUIRED", "BUNDLE_INPUT_REQUIRED",
        "APP_BUNDLE_INPUT_REQUIRED", "AIBI_BINDING_INPUT_REQUIRED",
        "ARTIFACT_DESCRIPTOR", "ARTIFACT_PATH_INVALID",
    }:
        return "INPUT_CONTRACT"
    if code.startswith("AUTHORIZATION_"):
        return "GOVERNANCE_AUTHORIZATION"
    if code.startswith("IDENTITY_") or code.startswith("APP_STORAGE_"):
        return "ENVIRONMENT_IDENTITY"
    if code.startswith("ROLLBACK_"):
        return "RECOVERY_ROLLBACK"
    if code.startswith("PREFLIGHT_"):
        return "PREFLIGHT_READINESS"
    if code.startswith(("TREE_", "GIT_")):
        return "GIT_STATE"
    if code.startswith(("LKG_", "UPDATE_")):
        return "COMPATIBILITY_LKG"
    if code.startswith("STAGING_") or code == "LOCAL_OPERATION_FAILED":
        return "STAGING_EXECUTION"
    if code in {
        "THEME_HASH_STALE", "BUNDLE_VALID", "BUNDLE_INCOMPLETE", "APP_BUNDLE_VALID",
        "APP_BUNDLE_INVALID", "NATIVE_TEMPLATE_HASH_STALE", "NATIVE_TEMPLATE_SYNTHETIC",
        "JSON_POINTER_MISSING", "ARTIFACT_INVALID", "ARTIFACT_SOURCE_STALE",
        "ARTIFACT_READY", "LKG_ARTIFACT_INVALID",
    }:
        return "ARTIFACT_INTEGRITY"
    if code.startswith("AIBI_") or code.startswith("S1_CONTRACT_") or code in {
        "THEME_VALID", "THEME_INVALID", "CONTEXT_INCOMPATIBLE", "WORKSPACE_POLICY_VALID",
    }:
        return "CANONICAL_CONTRACT"
    return "UNKNOWN"


def _safe_event(status: str, source_code: str, stage: str) -> dict[str, str]:
    if status == "PASS":
        summary_key = "NO_FAILURE"
    elif status == "NOT_APPLICABLE":
        summary_key = "NOT_APPLICABLE"
    else:
        summary_key = stage
    return {
        "status": status,
        "stage": stage,
        "safe_code": source_code,
        "safe_message": SAFE_SUMMARY.get(summary_key, SAFE_SUMMARY["UNKNOWN"]),
        "next_action": NEXT_ACTION.get(summary_key, NEXT_ACTION["UNKNOWN"]),
    }


def _validate_check(engine: str, raw: Any) -> dict[str, str]:
    if type(raw) is not dict or set(raw) != {"check_id", "status", "code", "message"}:
        raise DiagnosticRequestError("SOURCE_CHECK_INVALID", "Check de origem possui shape inválido.")
    status = raw.get("status")
    code = raw.get("code")
    if status not in STATUSES:
        raise DiagnosticRequestError("SOURCE_STATUS_INVALID", "Status de check fora do contrato.")
    if type(code) is not str or not _CODE_RE.fullmatch(code):
        raise DiagnosticRequestError("SOURCE_CODE_UNREGISTERED", "Código de origem não registrado.")
    if code not in SOURCE_CODES[engine]:
        raise DiagnosticRequestError("SOURCE_CODE_UNREGISTERED", "Código de origem não registrado.")
    return _safe_event(status, code, _stage_for(code))


def _extract_s2(report: dict[str, Any]) -> list[dict[str, str]]:
    allowed = {
        "report_version", "engine", "mode", "overall_status", "request_checks",
        "operations", "network_access", "remote_mutation_performed",
    }
    if set(report) != allowed or report.get("report_version") != 1:
        raise DiagnosticRequestError("SOURCE_SHAPE_INVALID", "Relatório S2 possui shape incompatível.")
    request_checks = report.get("request_checks")
    operations = report.get("operations")
    if type(request_checks) is not list or type(operations) is not list:
        raise DiagnosticRequestError("SOURCE_SHAPE_INVALID", "Relatório S2 possui listas inválidas.")
    events = [_validate_check("V13-S2", item) for item in request_checks]
    for operation in operations:
        if type(operation) is not dict or set(operation) != {"surface_id", "action_id", "status", "checks"}:
            raise DiagnosticRequestError("SOURCE_SHAPE_INVALID", "Operação S2 possui shape inválido.")
        if operation.get("status") not in STATUSES or type(operation.get("checks")) is not list:
            raise DiagnosticRequestError("SOURCE_SHAPE_INVALID", "Operação S2 possui status/checks inválidos.")
        op_events = [_validate_check("V13-S2", item) for item in operation["checks"]]
        if _max_status([item["status"] for item in op_events]) != operation["status"]:
            raise DiagnosticRequestError("SOURCE_STATUS_MISMATCH", "Status da operação S2 diverge dos checks.")
        events.extend(op_events)
    return events


def _extract_s3(report: dict[str, Any]) -> list[dict[str, str]]:
    allowed = {
        "report_version", "engine", "mode", "overall_status", "checks", "network_access",
        "remote_mutation_performed", "publication_performed", "preflight_status", "receipt",
    }
    if not set(report) <= allowed or report.get("report_version") != 1:
        raise DiagnosticRequestError("SOURCE_SHAPE_INVALID", "Relatório S3 possui shape incompatível.")
    required = {
        "report_version", "engine", "mode", "overall_status", "checks", "network_access",
        "remote_mutation_performed", "publication_performed",
    }
    if not required <= set(report) or type(report.get("checks")) is not list:
        raise DiagnosticRequestError("SOURCE_SHAPE_INVALID", "Relatório S3 possui campos obrigatórios inválidos.")
    if report.get("overall_status") == "PASS" and "receipt" not in report:
        raise DiagnosticRequestError("SOURCE_SHAPE_INVALID", "PASS S3 exige recibo técnico.")
    if report.get("overall_status") != "PASS" and "receipt" in report:
        raise DiagnosticRequestError("SOURCE_SHAPE_INVALID", "Relatório S3 não-PASS não pode carregar recibo de sucesso.")
    return [_validate_check("V13-S3", item) for item in report["checks"]]


def _extract_source(report: Any) -> tuple[str, str, list[dict[str, str]]]:
    if type(report) is not dict:
        raise DiagnosticRequestError("SOURCE_REPORT_TYPE", "source_report deve ser objeto JSON.")
    engine = report.get("engine")
    if engine not in SOURCE_CODES:
        raise DiagnosticRequestError("SOURCE_ENGINE_UNSUPPORTED", "Somente relatórios V13-S2/V13-S3 são suportados.")
    overall = report.get("overall_status")
    if overall not in STATUSES:
        raise DiagnosticRequestError("SOURCE_STATUS_INVALID", "overall_status de origem é inválido.")
    if report.get("network_access") is not False or report.get("remote_mutation_performed") is not False:
        raise DiagnosticRequestError("SOURCE_BOUNDARY_VIOLATION", "Relatório de origem declara rede ou mutação remota.")
    if engine == "V13-S3" and report.get("publication_performed") is not False:
        raise DiagnosticRequestError("SOURCE_BOUNDARY_VIOLATION", "Relatório S3 declara publicação.")
    events = _extract_s2(report) if engine == "V13-S2" else _extract_s3(report)
    computed = _max_status([item["status"] for item in events])
    if computed != overall:
        raise DiagnosticRequestError("SOURCE_STATUS_MISMATCH", "overall_status diverge dos checks sanitizados.")
    return engine, overall, events


def _validate_evidence(value: Any) -> dict[str, str]:
    if type(value) is not list:
        raise DiagnosticRequestError("EVIDENCE_TYPE", "evidence deve ser lista.")
    result: dict[str, str] = {}
    for item in value:
        if type(item) is not dict or set(item) != {"kind", "state"}:
            raise DiagnosticRequestError("EVIDENCE_TYPE", "Item de evidence possui shape inválido.")
        kind = item.get("kind")
        state = item.get("state")
        if kind not in EVIDENCE_KINDS:
            raise DiagnosticRequestError("EVIDENCE_KIND", "kind de evidência fora do enum sanitizado.")
        if state not in EVIDENCE_STATES:
            raise DiagnosticRequestError("EVIDENCE_STATE", "state de evidência fora do enum sanitizado.")
        if kind in result:
            raise DiagnosticRequestError("EVIDENCE_DUPLICATE", "Uma classe de evidência não pode aparecer duas vezes.")
        result[kind] = state
    return result


def _required_evidence(source_status: str, events: list[dict[str, str]]) -> set[str]:
    required: set[str] = set()
    for event in events:
        if event["status"] in {"FAIL", "BLOCKED"}:
            required.update(REQUIRED_EVIDENCE.get(event["stage"], set()))
    if source_status == "PASS":
        required.add("git_ci")
    return required


def _evidence_events(required: set[str], declared: dict[str, str]) -> list[dict[str, str]]:
    events: list[dict[str, str]] = []
    for kind in sorted(required):
        state = declared.get(kind, "MISSING")
        if state == "REFERENCED":
            status, code = "PASS", "EVIDENCE_REFERENCED"
        elif state == "NOT_APPLICABLE":
            status, code = "BLOCKED", "EVIDENCE_MISSING"
        else:
            status, code = "BLOCKED", "EVIDENCE_MISSING"
        event = _safe_event(status, code, "EVIDENCE_GAP")
        event["evidence_kind"] = kind
        events.append(event)
    for kind in sorted(set(declared) - required):
        state = declared[kind]
        if state == "REFERENCED":
            status, code = "PASS", "EVIDENCE_REFERENCED"
        elif state == "NOT_APPLICABLE":
            status, code = "NOT_APPLICABLE", "EVIDENCE_NOT_APPLICABLE"
        else:
            status, code = "NOT_APPLICABLE", "EVIDENCE_NOT_APPLICABLE"
        event = _safe_event(status, code, "EVIDENCE_GAP")
        event["evidence_kind"] = kind
        events.append(event)
    return events


def _safe_log(events: list[dict[str, str]]) -> list[str]:
    lines = []
    for index, event in enumerate(events, start=1):
        suffix = f"|{event['evidence_kind']}" if "evidence_kind" in event else ""
        lines.append(
            f"{index:03d}|{event['status']}|{event['stage']}|{event['safe_code']}{suffix}"
        )
    return lines


def _error_report(code: str, message: str) -> dict[str, Any]:
    return {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "engine": ENGINE,
        "diagnostic_status": "FAIL",
        "events": [
            {
                "status": "FAIL",
                "stage": "INPUT_CONTRACT",
                "safe_code": code if code in DIAGNOSTIC_CODES else "SOURCE_SHAPE_INVALID",
                "safe_message": message,
                "next_action": NEXT_ACTION["INPUT_CONTRACT"],
            }
        ],
        "safe_log": [f"001|FAIL|INPUT_CONTRACT|{code if code in DIAGNOSTIC_CODES else 'SOURCE_SHAPE_INVALID'}"],
        "network_access": False,
        "remote_mutation_performed": False,
    }


def run_diagnosis(request: Any) -> dict[str, Any]:
    """Produz diagnóstico determinístico e sanitizado de relatório S2/S3."""
    try:
        if type(request) is not dict:
            raise DiagnosticRequestError("DIAG_REQUEST_TYPE", "Request S4 deve ser objeto JSON.")
        if set(request) != {"diagnostic_version", "source_report", "evidence"}:
            raise DiagnosticRequestError("DIAG_REQUEST_FIELDS", "Campos de topo S4 divergentes.")
        if request.get("diagnostic_version") != DIAGNOSTIC_VERSION:
            raise DiagnosticRequestError("DIAG_REQUEST_VERSION", "diagnostic_version deve ser 1.")
        source_engine, source_status, source_events = _extract_source(request["source_report"])
        declared = _validate_evidence(request["evidence"])
        required = _required_evidence(source_status, source_events)
        evidence_events = _evidence_events(required, declared)
        all_events = [*source_events, *evidence_events]
        diagnostic_status = _max_status([item["status"] for item in all_events])
        counts = {status: 0 for status in ("PASS", "BLOCKED", "FAIL", "NOT_APPLICABLE")}
        for event in all_events:
            counts[event["status"]] += 1
        missing = sorted(
            event["evidence_kind"]
            for event in evidence_events
            if event["safe_code"] == "EVIDENCE_MISSING"
        )
        actions = sorted(
            {
                event["next_action"]
                for event in all_events
                if event["status"] in {"BLOCKED", "FAIL"}
            }
        )
        return {
            "diagnostic_version": DIAGNOSTIC_VERSION,
            "engine": ENGINE,
            "source_engine": source_engine,
            "source_status": source_status,
            "diagnostic_status": diagnostic_status,
            "events": all_events,
            "status_counts": counts,
            "evidence": {
                "required_kinds": sorted(required),
                "missing_kinds": missing,
                "completeness": "INCOMPLETE" if missing else "REFERENCED_COMPLETE",
                "references_authenticated": False,
            },
            "next_actions": actions,
            "safe_log": _safe_log(all_events),
            "network_access": False,
            "remote_mutation_performed": False,
        }
    except DiagnosticRequestError as exc:
        return _error_report(exc.code, exc.safe_message)


def _load_request(path: Path) -> Any:
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_INPUT_BYTES:
            raise OSError
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        raise DiagnosticRequestError("DIAG_REQUEST_TYPE", "Arquivo S4 não pôde ser lido como JSON local.") from None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnostica relatórios V13-S2/S3 sem rede, segredo ou mutação Databricks."
    )
    parser.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()
    try:
        request = _load_request(args.request)
        report = run_diagnosis(request)
    except DiagnosticRequestError as exc:
        report = _error_report(exc.code, exc.safe_message)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"PASS": 0, "NOT_APPLICABLE": 0, "BLOCKED": 2, "FAIL": 1}[report["diagnostic_status"]]


if __name__ == "__main__":
    raise SystemExit(main())
