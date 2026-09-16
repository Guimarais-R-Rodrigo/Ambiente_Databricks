from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "docs" / "sprints" / "sistema_temas" / "V14" / "MATRIZ_OWNERSHIP.json"

EXPECTED_SURFACES = {
    "notebook_visual_core": "V02",
    "visual_lab": "V05",
    "transition_bundle": "V09",
    "databricks_app": "V10",
    "aibi_dashboard": "V11",
    "workspace_theme": "V11",
}

EXPECTED_ROLES = {
    "operational_owner",
    "backup_operational_owner",
    "change_approver",
    "incident_responsible",
    "go_live_authority",
    "residual_risk_authority",
}

EXPECTED_INHERITED = {
    "A11-01": "FAIL",
    "issue_57": "OPEN",
    "V12-LAB-01": "BLOQUEADO_AUTORIZACAO",
    "V12-APP-01": "BLOQUEADO_AUTORIZACAO",
    "V12-AIBI-02": "BLOQUEADO_AUTORIZACAO",
    "HUMAN-01": "PASS_FORMATIVO",
}


class OwnershipContractError(ValueError):
    """Contrato S1 inválido, sem ecoar conteúdo potencialmente sensível."""


def load_matrix(path: Path = DEFAULT_MATRIX) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise OwnershipContractError("matriz S1 ilegível ou JSON inválido") from exc
    if not isinstance(data, dict):
        raise OwnershipContractError("matriz S1 deve ser objeto JSON")
    return data


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise OwnershipContractError(message)


def _validate_repo_ref(value: Any, field: str) -> None:
    _require(isinstance(value, str) and value.strip() == value and value, f"{field}: referência ausente")
    _require(not value.startswith(("/", "http://", "https://")), f"{field}: referência deve ser relativa ao repositório")
    _require(".." not in Path(value).parts, f"{field}: traversal proibido")
    _require((ROOT / value).is_file(), f"{field}: referência inexistente")


def validate_matrix(data: dict[str, Any]) -> None:
    _require(data.get("kind") == "hub_theme_operational_ownership", "kind S1 inválido")
    _require(data.get("version") == 1, "version S1 inválida")
    _require(data.get("sprint") == "V14-S1", "sprint S1 inválida")
    _require(data.get("references_only") is True, "S1 deve ser references_only")
    _require(data.get("remote_mutation_performed_by_s1") is False, "S1 não pode declarar mutação remota")
    _require(data.get("production_readiness_declared") is False, "S1 não pode declarar production readiness")
    _require(data.get("go_live_decision") == "NOT_DECIDED", "S1 não decide go-live")
    _require(data.get("s2_started") is False, "S2 não pode estar iniciada")

    _require(data.get("role_policy_ref") == "docs/sprints/sistema_temas/V01/GOVERNANCA.md", "política de papéis deve permanecer V01")
    _require(data.get("operational_inventory_ref") == "docs/sprints/sistema_temas/V13/MATRIZ_OPERACIONAL.json", "inventário técnico deve permanecer V13")
    _validate_repo_ref(data["role_policy_ref"], "role_policy_ref")
    _validate_repo_ref(data["operational_inventory_ref"], "operational_inventory_ref")

    rules = data.get("authority_rules")
    _require(isinstance(rules, dict), "authority_rules ausente")
    expected_rules = {
        "missing_owner_backup_or_authority": "BLOCKED",
        "self_approval_forbidden": True,
        "approval_does_not_imply_publication": True,
        "technical_ownership_does_not_imply_operational_authority": True,
        "invented_identity_or_channel_forbidden": True,
    }
    _require(rules == expected_rules, "regras de autoridade divergentes")

    _require(data.get("inherited_states") == EXPECTED_INHERITED, "estados herdados foram reclassificados")
    _require(set(data.get("operational_role_slots", [])) == EXPECTED_ROLES, "slots operacionais divergentes")

    surfaces = data.get("surfaces")
    _require(isinstance(surfaces, list), "surfaces deve ser lista")
    by_id: dict[str, dict[str, Any]] = {}
    for item in surfaces:
        _require(isinstance(item, dict), "superfície inválida")
        surface_id = item.get("surface_id")
        _require(isinstance(surface_id, str) and surface_id not in by_id, "surface_id ausente ou duplicado")
        by_id[surface_id] = item
    _require(set(by_id) == set(EXPECTED_SURFACES), "conjunto de superfícies S1 divergente")

    for surface_id, expected_owner in EXPECTED_SURFACES.items():
        item = by_id[surface_id]
        technical = item.get("technical_owner")
        _require(isinstance(technical, dict), f"{surface_id}: technical_owner ausente")
        _require(technical.get("status") == "EVIDENCED", f"{surface_id}: owner técnico não evidenciado")
        _require(technical.get("owner_ref") == expected_owner, f"{surface_id}: owner técnico divergente")
        evidence = technical.get("evidence_refs")
        _require(isinstance(evidence, list) and len(evidence) >= 2, f"{surface_id}: evidência técnica insuficiente")
        for ref in evidence:
            _validate_repo_ref(ref, f"{surface_id}.technical_owner.evidence")

        roles = item.get("operational_roles")
        _require(isinstance(roles, dict) and set(roles) == EXPECTED_ROLES, f"{surface_id}: slots operacionais incompletos")
        evidenced_principals: dict[str, str] = {}
        for role_name in sorted(EXPECTED_ROLES):
            role = roles[role_name]
            _require(isinstance(role, dict), f"{surface_id}.{role_name}: slot inválido")
            status = role.get("status")
            _require(status in {"BLOCKED", "EVIDENCED"}, f"{surface_id}.{role_name}: status inválido")
            principal = role.get("principal_ref")
            refs = role.get("evidence_refs")
            _require(isinstance(refs, list), f"{surface_id}.{role_name}: evidence_refs inválido")
            reason = role.get("reason_code")
            _require(isinstance(reason, str) and reason, f"{surface_id}.{role_name}: reason_code ausente")

            if status == "BLOCKED":
                _require(principal is None, f"{surface_id}.{role_name}: BLOCKED não pode fingir principal")
                _require(refs == [], f"{surface_id}.{role_name}: BLOCKED não pode fingir evidência")
            else:
                _require(isinstance(principal, str) and principal.strip() == principal and principal, f"{surface_id}.{role_name}: principal evidenciado ausente")
                lowered = principal.lower()
                _require("invented" not in lowered and "placeholder" not in lowered and "example" not in lowered, f"{surface_id}.{role_name}: autoridade não verificável")
                _require(len(refs) > 0, f"{surface_id}.{role_name}: evidência obrigatória")
                for ref in refs:
                    _validate_repo_ref(ref, f"{surface_id}.{role_name}.evidence")
                evidenced_principals[role_name] = principal

        operator = evidenced_principals.get("operational_owner")
        approver = evidenced_principals.get("change_approver")
        if operator is not None and approver is not None:
            _require(operator != approver, f"{surface_id}: self-approval proibido")

    readiness = ROOT / "docs" / "sprints" / "sistema_temas" / "V14" / "MATRIZ_READINESS.json"
    _require(not readiness.exists(), "S2 materializada prematuramente")


def validate_file(path: Path = DEFAULT_MATRIX) -> None:
    validate_matrix(load_matrix(path))


def validated_copy(data: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(data)
    validate_matrix(candidate)
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida ownership/autoridade V14 S1 em modo local e read-only.")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--check", action="store_true", help="mantido para deixar a intenção do gate explícita")
    args = parser.parse_args()
    validate_file(args.matrix)
    print("V14 S1 ownership/autoridade: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
