"""Validador read-only do inventário operacional V13-S1.

Esta ferramenta valida somente o contrato declarativo criado na S1. Ela não executa
preflight de ambiente (S2), não chama Databricks e não realiza mutação remota.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

if __package__:
    from .project_policy import SIMULATED_ROOT
else:
    from project_policy import SIMULATED_ROOT

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "docs/sprints/sistema_temas/V13/MATRIZ_OPERACIONAL.json"

EXPECTED_SURFACES = {
    "notebook_visual_core",
    "visual_lab",
    "transition_bundle",
    "databricks_app",
    "aibi_dashboard",
    "workspace_theme",
}
ALLOWED_ACTION_MODES = {
    "read_only",
    "local_artifact_mutation",
    "persistent_mutation",
    "remote_mutation",
}
FORBIDDEN_DUPLICATE_KEYS = {
    "tokens",
    "roles",
    "bindings",
    "direct_bindings",
    "required_paths",
    "role_matrix",
    "token_map",
}
EXPECTED_TOP_LEVEL = {
    "contract_version",
    "kind",
    "sprint",
    "canonical_plan_ref",
    "governance_policy_ref",
    "rules",
    "relationships",
    "surfaces",
}


class OperationalContractError(ValueError):
    """Contrato operacional inválido."""


def _fail(code: str, message: str) -> None:
    raise OperationalContractError(f"{code}: {message}")


def _no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail("JSON_DUPLICATE_KEY", f"chave JSON duplicada: {key}")
        result[key] = value
    return result


def load_matrix(path: Path = DEFAULT_MATRIX) -> dict[str, Any]:
    """Carrega a matriz rejeitando chave JSON duplicada."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        _fail("MATRIX_READ", f"não foi possível ler {path}: {exc}")
    try:
        data = json.loads(raw, object_pairs_hook=_no_duplicate_object)
    except json.JSONDecodeError as exc:
        _fail("MATRIX_JSON", f"JSON inválido: {exc}")
    if not isinstance(data, dict):
        _fail("MATRIX_TYPE", "a raiz deve ser objeto JSON")
    return data


def _walk_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def _check_repo_ref(ref: Any, field: str) -> None:
    if not isinstance(ref, str) or not ref.strip():
        _fail("REF_TYPE", f"{field} deve ser caminho relativo não vazio")
    candidate = Path(ref)
    if candidate.is_absolute() or ".." in candidate.parts:
        _fail("REF_PATH", f"{field} deve permanecer dentro do repositório: {ref}")
    if ref.startswith(("Novo_Ambiente_Simulado/", SIMULATED_ROOT.as_posix() + "/")):
        _fail("DERIVED_REF", f"{field} não pode usar o derivado como owner/fonte: {ref}")
    if not (ROOT / candidate).exists():
        _fail("REF_MISSING", f"{field} aponta para artefato inexistente: {ref}")


def _check_refs(refs: Any, field: str, *, require_nonempty: bool = True) -> None:
    if not isinstance(refs, list):
        _fail("REFS_TYPE", f"{field} deve ser lista")
    if require_nonempty and not refs:
        _fail("REFS_EMPTY", f"{field} não pode ser vazio")
    for index, ref in enumerate(refs):
        _check_repo_ref(ref, f"{field}[{index}]")


def _check_owner(owner: Any, field: str) -> None:
    if not isinstance(owner, dict):
        _fail("OWNER_TYPE", f"{field} deve ser objeto")
    if set(owner) != {"version", "contract_ref"}:
        _fail("OWNER_FIELDS", f"{field} deve conter somente version e contract_ref")
    version = owner["version"]
    if not isinstance(version, str) or not re_full_version(version):
        _fail("OWNER_VERSION", f"{field}.version inválida: {version!r}")
    _check_repo_ref(owner["contract_ref"], f"{field}.contract_ref")


def re_full_version(value: str) -> bool:
    if len(value) != 3 or not value.startswith("V") or not value[1:].isdigit():
        return False
    number = int(value[1:])
    return 1 <= number <= 12


def _check_action(action: Any, surface_id: str, seen: set[str]) -> None:
    if not isinstance(action, dict):
        _fail("ACTION_TYPE", f"{surface_id}: action deve ser objeto")
    required = {
        "action_id",
        "mode",
        "performed_by_s1",
        "authorization",
        "verification_refs",
        "rollback",
    }
    if set(action) != required:
        _fail("ACTION_FIELDS", f"{surface_id}: campos de action divergentes")
    action_id = action["action_id"]
    if not isinstance(action_id, str) or not action_id:
        _fail("ACTION_ID", f"{surface_id}: action_id inválido")
    if action_id in seen:
        _fail("ACTION_DUPLICATE", f"{surface_id}: action_id duplicado: {action_id}")
    seen.add(action_id)

    mode = action["mode"]
    if mode not in ALLOWED_ACTION_MODES:
        _fail("ACTION_MODE", f"{surface_id}/{action_id}: mode inválido: {mode!r}")
    if action["performed_by_s1"] is not False:
        _fail("S1_MUTATION", f"{surface_id}/{action_id}: S1 não pode executar a ação")

    auth = action["authorization"]
    if not isinstance(auth, dict) or set(auth) != {"required", "basis", "state"}:
        _fail("ACTION_AUTH", f"{surface_id}/{action_id}: autorização incompleta")
    if not isinstance(auth["required"], bool):
        _fail("ACTION_AUTH_REQUIRED", f"{surface_id}/{action_id}: required deve ser booleano")
    if not isinstance(auth["basis"], str) or not auth["basis"]:
        _fail("ACTION_AUTH_BASIS", f"{surface_id}/{action_id}: basis obrigatório")
    if not isinstance(auth["state"], str) or not auth["state"]:
        _fail("ACTION_AUTH_STATE", f"{surface_id}/{action_id}: state obrigatório")

    rollback = action["rollback"]
    if not isinstance(rollback, dict) or set(rollback) != {"required", "strategy", "refs"}:
        _fail("ACTION_ROLLBACK", f"{surface_id}/{action_id}: rollback incompleto")
    if not isinstance(rollback["required"], bool):
        _fail("ACTION_ROLLBACK_REQUIRED", f"{surface_id}/{action_id}: required deve ser booleano")
    if not isinstance(rollback["strategy"], str) or not rollback["strategy"]:
        _fail("ACTION_ROLLBACK_STRATEGY", f"{surface_id}/{action_id}: strategy obrigatória")
    _check_refs(rollback["refs"], f"{surface_id}/{action_id}.rollback.refs")

    if mode == "read_only":
        if auth["required"]:
            _fail("READ_ONLY_AUTH", f"{surface_id}/{action_id}: read-only não deve exigir autorização de mutação")
        if rollback["required"]:
            _fail("READ_ONLY_ROLLBACK", f"{surface_id}/{action_id}: read-only não deve exigir rollback")
    else:
        if not auth["required"]:
            _fail("MUTATION_AUTH", f"{surface_id}/{action_id}: mutação exige autorização explícita")
        if not rollback["required"]:
            _fail("MUTATION_ROLLBACK", f"{surface_id}/{action_id}: mutação exige rollback declarado")

    _check_refs(action["verification_refs"], f"{surface_id}/{action_id}.verification_refs")


def validate_matrix(data: dict[str, Any]) -> None:
    """Valida a matriz S1 sem executar qualquer operação operacional."""
    if set(data) != EXPECTED_TOP_LEVEL:
        _fail("TOP_LEVEL_FIELDS", "campos de topo divergentes do contrato V13-S1")
    if data["contract_version"] != 1:
        _fail("CONTRACT_VERSION", "contract_version deve ser 1")
    if data["kind"] != "hub_theme_operational_inventory":
        _fail("KIND", "kind inválido")
    if data["sprint"] != "V13-S1":
        _fail("SPRINT", "sprint deve ser V13-S1")
    _check_repo_ref(data["canonical_plan_ref"], "canonical_plan_ref")
    _check_repo_ref(data["governance_policy_ref"], "governance_policy_ref")

    forbidden = sorted(set(_walk_keys(data)) & FORBIDDEN_DUPLICATE_KEYS)
    if forbidden:
        _fail(
            "DUPLICATED_CONTRACT",
            "a matriz não pode copiar contratos canônicos: " + ", ".join(forbidden),
        )

    rules = data["rules"]
    expected_rule_keys = {
        "references_only",
        "preflight_stage",
        "remote_mutation_performed_by_s1",
        "source_root",
        "derived_root",
        "derived_root_editable",
    }
    if not isinstance(rules, dict) or set(rules) != expected_rule_keys:
        _fail("RULES", "rules divergentes do contrato")
    if rules["references_only"] is not True:
        _fail("REFERENCES_ONLY", "S1 deve referenciar owners, não copiá-los")
    if rules["preflight_stage"] != "S2_NOT_IMPLEMENTED":
        _fail("PREFLIGHT_BOUNDARY", "S1 não pode implementar o preflight da S2")
    if rules["remote_mutation_performed_by_s1"] is not False:
        _fail("REMOTE_MUTATION", "S1 deve permanecer sem mutação remota")
    if rules["source_root"] != "ambiente_databricks/" or rules["derived_root"] != SIMULATED_ROOT.as_posix() + "/":
        _fail("SOURCE_DERIVED", "raízes fonte/derivado divergentes")
    if rules["derived_root_editable"] is not False:
        _fail("DERIVED_EDITABLE", "saída gerada não pode ser fonte editável")

    relationships = data["relationships"]
    if not isinstance(relationships, list) or not relationships:
        _fail("RELATIONSHIPS", "relationships deve ser lista não vazia")
    relationship_ids: set[str] = set()
    for item in relationships:
        if not isinstance(item, dict):
            _fail("RELATIONSHIP_TYPE", "relationship deve ser objeto")
        expected = {"relationship_id", "from_surface", "to_surface", "relation", "refs"}
        if set(item) != expected:
            _fail("RELATIONSHIP_FIELDS", "relationship com campos divergentes")
        rel_id = item["relationship_id"]
        if not isinstance(rel_id, str) or not rel_id or rel_id in relationship_ids:
            _fail("RELATIONSHIP_ID", f"relationship_id inválido/duplicado: {rel_id!r}")
        relationship_ids.add(rel_id)
        _check_refs(item["refs"], f"relationship[{rel_id}].refs")

    surfaces = data["surfaces"]
    if not isinstance(surfaces, list):
        _fail("SURFACES_TYPE", "surfaces deve ser lista")
    ids = [item.get("surface_id") for item in surfaces if isinstance(item, dict)]
    if len(ids) != len(surfaces) or set(ids) != EXPECTED_SURFACES or len(ids) != len(set(ids)):
        _fail("SURFACE_SET", f"superfícies devem ser exatamente {sorted(EXPECTED_SURFACES)}")

    for surface in surfaces:
        surface_id = surface["surface_id"]
        expected_fields = {
            "surface_id",
            "label",
            "primary_owner",
            "dependency_owners",
            "artifact",
            "preflight",
            "authorization",
            "smoke",
            "rollback",
            "minimum_evidence",
            "known_homologation_states",
            "actions",
            "limitations",
        }
        if set(surface) != expected_fields:
            _fail("SURFACE_FIELDS", f"{surface_id}: campos divergentes")
        if not isinstance(surface["label"], str) or not surface["label"]:
            _fail("SURFACE_LABEL", f"{surface_id}: label obrigatório")
        _check_owner(surface["primary_owner"], f"{surface_id}.primary_owner")
        dependencies = surface["dependency_owners"]
        if not isinstance(dependencies, list):
            _fail("DEPENDENCIES_TYPE", f"{surface_id}: dependency_owners deve ser lista")
        for index, owner in enumerate(dependencies):
            _check_owner(owner, f"{surface_id}.dependency_owners[{index}]")

        artifact = surface["artifact"]
        if not isinstance(artifact, dict) or set(artifact) != {"kind", "refs"}:
            _fail("ARTIFACT", f"{surface_id}: artifact inválido")
        if not isinstance(artifact["kind"], str) or not artifact["kind"]:
            _fail("ARTIFACT_KIND", f"{surface_id}: artifact.kind obrigatório")
        _check_refs(artifact["refs"], f"{surface_id}.artifact.refs")

        preflight = surface["preflight"]
        if not isinstance(preflight, dict) or set(preflight) != {"stage", "existing_check_refs"}:
            _fail("PREFLIGHT", f"{surface_id}: preflight inválido")
        if preflight["stage"] != "S2_NOT_IMPLEMENTED":
            _fail("PREFLIGHT_BOUNDARY", f"{surface_id}: S2 não pode ser antecipada")
        _check_refs(preflight["existing_check_refs"], f"{surface_id}.preflight.existing_check_refs")

        authorization = surface["authorization"]
        expected_auth = {"policy_ref", "required_for_persistent_mutation", "current_state"}
        if not isinstance(authorization, dict) or set(authorization) != expected_auth:
            _fail("AUTHORIZATION", f"{surface_id}: authorization inválida")
        _check_repo_ref(authorization["policy_ref"], f"{surface_id}.authorization.policy_ref")
        if not isinstance(authorization["required_for_persistent_mutation"], bool):
            _fail("AUTHORIZATION_REQUIRED", f"{surface_id}: flag de autorização deve ser booleana")
        if not isinstance(authorization["current_state"], str) or not authorization["current_state"]:
            _fail("AUTHORIZATION_STATE", f"{surface_id}: estado de autorização obrigatório")

        smoke = surface["smoke"]
        if not isinstance(smoke, dict) or set(smoke) != {"refs"}:
            _fail("SMOKE", f"{surface_id}: smoke inválido")
        _check_refs(smoke["refs"], f"{surface_id}.smoke.refs")

        rollback = surface["rollback"]
        if not isinstance(rollback, dict) or set(rollback) != {"strategy", "refs"}:
            _fail("ROLLBACK", f"{surface_id}: rollback inválido")
        if not isinstance(rollback["strategy"], str) or not rollback["strategy"]:
            _fail("ROLLBACK_STRATEGY", f"{surface_id}: rollback.strategy obrigatório")
        _check_refs(rollback["refs"], f"{surface_id}.rollback.refs")

        if not isinstance(surface["minimum_evidence"], str) or not surface["minimum_evidence"]:
            _fail("MINIMUM_EVIDENCE", f"{surface_id}: minimum_evidence obrigatório")
        states = surface["known_homologation_states"]
        if not isinstance(states, list):
            _fail("HOMOLOGATION_STATES", f"{surface_id}: estados devem ser lista")
        for index, state in enumerate(states):
            if not isinstance(state, dict):
                _fail("HOMOLOGATION_STATE_TYPE", f"{surface_id}: estado #{index} inválido")
            required_state_keys = {"case_id", "state", "scope", "evidence_ref"}
            optional_state_keys = {"issue_ref"}
            if not required_state_keys <= set(state) or set(state) - required_state_keys - optional_state_keys:
                _fail("HOMOLOGATION_STATE_FIELDS", f"{surface_id}: estado #{index} com campos divergentes")
            for key in ("case_id", "state", "scope"):
                if not isinstance(state[key], str) or not state[key]:
                    _fail("HOMOLOGATION_STATE_VALUE", f"{surface_id}: {key} obrigatório")
            _check_repo_ref(state["evidence_ref"], f"{surface_id}.known_homologation_states[{index}].evidence_ref")

        actions = surface["actions"]
        if not isinstance(actions, list) or not actions:
            _fail("ACTIONS", f"{surface_id}: actions deve ser lista não vazia")
        seen_actions: set[str] = set()
        for action in actions:
            _check_action(action, surface_id, seen_actions)

        limitations = surface["limitations"]
        if not isinstance(limitations, list) or not limitations:
            _fail("LIMITATIONS", f"{surface_id}: limitations deve ser lista não vazia")
        if any(not isinstance(item, str) or not item for item in limitations):
            _fail("LIMITATION_VALUE", f"{surface_id}: limitation inválida")

    for item in relationships:
        if item["from_surface"] not in EXPECTED_SURFACES or item["to_surface"] not in EXPECTED_SURFACES:
            _fail("RELATIONSHIP_SURFACE", f"relationship referencia superfície desconhecida: {item['relationship_id']}")


def validate_file(path: Path = DEFAULT_MATRIX) -> dict[str, Any]:
    data = load_matrix(path)
    validate_matrix(data)
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida o inventário operacional V13-S1 sem executar preflight.")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    args = parser.parse_args()
    try:
        data = validate_file(args.matrix)
    except OperationalContractError as exc:
        print(f"V13_S1_FAIL: {exc}")
        return 1
    print(f"V13_S1_PASS: {len(data['surfaces'])} superfícies; S2 preflight não implementado; mutação remota=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
