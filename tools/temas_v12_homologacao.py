"""V12 — validação fail-closed de evidências de homologação do Sistema de Temas.

Este módulo NÃO acessa Databricks, não executa deploy, não importa temas e não
substitui observação humana. Ele valida somente o formato e a coerência de um
registro de evidência produzido por uma execução autorizada separada.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "docs" / "sprints" / "sistema_temas" / "V12" / "matriz_homologacao.json"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_ALLOWED_ENVIRONMENTS = {
    "databricks_free_lab",
    "databricks_nonprod_authorized",
    "databricks_work_authorized_test",
}
_ALLOWED_HUMAN_ROLES = {
    "nontechnical_user",
    "technical_user",
    "workspace_admin",
    "maintainer",
}


class V12EvidenceError(ValueError):
    """Erro de validação com código estável e mensagem sanitizada."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


def _fail(code: str, message: str) -> None:
    raise V12EvidenceError(code, message) from None


def load_matrix(path: Path = DEFAULT_MATRIX) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        _fail("V12_MATRIX_READ", "A matriz V12 não pôde ser lida.")
    if type(data) is not dict or data.get("schema_version") != 1 or data.get("sprint") != "V12":
        _fail("V12_MATRIX_CONTRACT", "A matriz V12 não atende ao contrato esperado.")
    cases = data.get("cases")
    if type(cases) is not list or not cases:
        _fail("V12_MATRIX_CASES", "A matriz V12 precisa declarar casos.")
    seen: set[str] = set()
    for case in cases:
        if type(case) is not dict or type(case.get("id")) is not str or case["id"] in seen:
            _fail("V12_MATRIX_CASES", "Caso V12 ausente, duplicado ou inválido.")
        seen.add(case["id"])
        if case.get("evidence_class") not in set(data.get("evidence_classes", [])):
            _fail("V12_MATRIX_CLASS", "Classe de evidência não reconhecida.")
        if type(case.get("required_facts")) is not list:
            _fail("V12_MATRIX_FACTS", "Caso V12 sem fatos obrigatórios.")
    return data


def _case(matrix: dict[str, Any], case_id: str) -> dict[str, Any]:
    for item in matrix["cases"]:
        if item["id"] == case_id:
            return item
    _fail("V12_CASE_UNKNOWN", "Caso de homologação não existe na matriz V12.")


def _require_bool(facts: dict[str, Any], name: str, expected: bool | None = None) -> bool:
    value = facts.get(name)
    if type(value) is not bool:
        _fail("V12_FACT_TYPE", f"O fato {name} precisa ser booleano.")
    if expected is not None and value is not expected:
        _fail("V12_FACT_VALUE", f"O fato {name} não atende ao valor obrigatório.")
    return value


def _require_sha(facts: dict[str, Any], name: str) -> str:
    value = facts.get(name)
    if type(value) is not str or _SHA256_RE.fullmatch(value) is None:
        _fail("V12_HASH", f"O fato {name} precisa ser SHA-256 completo.")
    return value


def validate_evidence(record: dict[str, Any], matrix: dict[str, Any] | None = None) -> dict[str, Any]:
    """Valida um registro sem promover evidência local a ambiente ou UAT."""
    matrix = load_matrix() if matrix is None else matrix
    if type(record) is not dict:
        _fail("V12_RECORD_TYPE", "O registro precisa ser objeto JSON.")
    required = {
        "schema_version", "sprint", "record_id", "case_id", "evidence_class",
        "status", "source_commit", "observed_at", "environment", "human",
        "facts", "artifacts", "notes",
    }
    if set(record) != required:
        _fail("V12_RECORD_SHAPE", "O registro possui campos ausentes ou inesperados.")
    if record["schema_version"] != 1 or record["sprint"] != "V12":
        _fail("V12_RECORD_VERSION", "Versão ou sprint divergente.")
    if type(record["record_id"]) is not str or not re.fullmatch(r"V12-[A-Z0-9][A-Z0-9_-]{2,80}", record["record_id"]):
        _fail("V12_RECORD_ID", "Use record_id sanitizado e estável.")
    if type(record["case_id"]) is not str:
        _fail("V12_CASE_UNKNOWN", "case_id inválido.")
    case = _case(matrix, record["case_id"])
    if record["evidence_class"] != case["evidence_class"]:
        _fail("V12_CLASS_MISMATCH", "Classe do registro diverge da matriz canônica.")
    if record["status"] not in matrix["status_values"]:
        _fail("V12_STATUS", "Status não reconhecido.")
    if type(record["source_commit"]) is not str or _COMMIT_RE.fullmatch(record["source_commit"]) is None:
        _fail("V12_COMMIT", "A evidência precisa fixar commit Git completo.")
    if type(record["observed_at"]) is not str or len(record["observed_at"]) < 16:
        _fail("V12_OBSERVED_AT", "A evidência precisa registrar data/hora observada.")
    try:
        observed = datetime.fromisoformat(record["observed_at"])
    except ValueError:
        _fail("V12_OBSERVED_AT", "Use data/hora ISO 8601 válida.")
    if observed.tzinfo is None:
        _fail("V12_OBSERVED_AT", "A data/hora observada precisa incluir timezone.")
    if type(record["facts"]) is not dict or type(record["artifacts"]) is not list:
        _fail("V12_RECORD_SHAPE", "facts/artifacts inválidos.")
    if type(record["notes"]) is not str:
        _fail("V12_RECORD_SHAPE", "notes precisa ser texto.")
    for name in case["required_facts"]:
        if name not in record["facts"]:
            _fail("V12_FACT_MISSING", f"Fato obrigatório ausente: {name}.")

    env = record["environment"]
    human = record["human"]
    if type(env) is not dict or type(human) is not dict:
        _fail("V12_RECORD_SHAPE", "environment/human inválidos.")

    if record["status"] != "PASS":
        return record

    if not record["artifacts"]:
        _fail("V12_PASS_WITHOUT_EVIDENCE", "PASS exige ao menos um artefato/evidência referenciada.")
    for item in record["artifacts"]:
        if type(item) is not dict or set(item) != {"kind", "sha256", "path"}:
            _fail("V12_ARTIFACT_SHAPE", "Artefato precisa declarar kind, sha256 e path sanitizado.")
        if type(item["kind"]) is not str or not item["kind"].strip():
            _fail("V12_ARTIFACT_SHAPE", "kind de artefato inválido.")
        if type(item["sha256"]) is not str or _SHA256_RE.fullmatch(item["sha256"]) is None:
            _fail("V12_ARTIFACT_HASH", "Artefato precisa de SHA-256 completo.")
        if type(item["path"]) is not str or not item["path"].strip():
            _fail("V12_ARTIFACT_SHAPE", "path de artefato inválido.")
    _require_bool(record["facts"], "oracle_met", True)

    if case["evidence_class"] == "databricks_environment":
        _validate_environment_pass(record, case)
    elif case["evidence_class"] == "human_uat":
        _validate_human_pass(record, case)
    elif case["evidence_class"] == "git_local":
        if env or human:
            _fail("V12_LOCAL_CROSS_CLASS", "PASS local não deve fabricar ambiente ou participante.")
    else:
        _fail("V12_CLASS_MISMATCH", "Classe de evidência desconhecida.")

    return record


def _validate_environment_pass(record: dict[str, Any], case: dict[str, Any]) -> None:
    env = record["environment"]
    human = record["human"]
    facts = record["facts"]
    if human:
        _fail("V12_ENV_HUMAN_MIX", "Evidência de ambiente não pode ser promovida a UAT humano no mesmo registro.")
    expected_keys = {"environment_class", "environment_authorized", "authorization_ref"}
    if set(env) != expected_keys:
        _fail("V12_ENV_SHAPE", "Ambiente precisa declarar apenas classe, autorização e referência.")
    if env["environment_class"] not in _ALLOWED_ENVIRONMENTS:
        _fail("V12_ENVIRONMENT", "Classe de ambiente não autorizada pelo protocolo V12.")
    if env["environment_authorized"] is not True:
        _fail("V12_AUTH_REQUIRED", "PASS de ambiente exige ambiente explicitamente autorizado.")
    if facts.get("environment_authorized") is not True:
        _fail("V12_AUTH_REQUIRED", "Fato environment_authorized precisa ser verdadeiro.")
    _require_bool(facts, "synthetic_data_only", True)

    if case["mutation_required"]:
        if type(env["authorization_ref"]) is not str or len(env["authorization_ref"].strip()) < 4:
            _fail("V12_AUTH_REQUIRED", "Mutação real exige referência explícita de autorização.")
        if facts.get("authorization_ref") != env["authorization_ref"]:
            _fail("V12_AUTH_MISMATCH", "A referência de autorização precisa coincidir entre ambiente e fatos.")
        _require_bool(facts, "rollback_plan_verified", True)
    elif env["authorization_ref"] not in (None, ""):
        if type(env["authorization_ref"]) is not str:
            _fail("V12_ENV_SHAPE", "authorization_ref inválido.")

    if record["case_id"] == "V12-LAB-01":
        _require_bool(facts, "browser_observed", True)
        _require_bool(facts, "persistence_observed", True)

    if record["case_id"] == "V12-APP-01":
        _require_bool(facts, "identity_checked", True)
        _require_bool(facts, "permission_checked", True)
        _require_bool(facts, "browser_observed", True)
        _require_bool(facts, "isolation_observed", True)
        _require_bool(facts, "publication_actions_absent", True)

    if record["case_id"] == "SEC-01":
        _require_bool(facts, "identity_checked", True)
        _require_bool(facts, "permission_checked", True)

    if record["case_id"] == "V12-AIBI-01":
        _require_bool(facts, "dashboard_draft", True)
        export_sha = _require_sha(facts, "export_sha256")
        if _require_sha(facts, "reviewed_export_sha256") != export_sha:
            _fail("V12_EXPORT_STALE", "O export revisado diverge do export fixado.")
        if _require_sha(facts, "used_export_sha256") != export_sha:
            _fail("V12_EXPORT_STALE", "O export usado diverge do export revisado.")
        if _require_sha(facts, "semantic_before_sha256") != _require_sha(facts, "semantic_after_sha256"):
            _fail("V12_SEMANTIC_DRIFT", "Datasets/queries/filtros/widgets mudaram durante a jornada de tema.")
        _require_bool(facts, "synthetic_fixture_used_as_databricks_input", False)
        _require_bool(facts, "approximated_automated", False)
        _require_bool(facts, "unsupported_automated", False)
        _require_bool(facts, "published", False)
        _require_bool(facts, "light_dark_observed", True)

    if record["case_id"] == "V12-AIBI-02":
        _require_bool(facts, "identity_checked", True)
        _require_bool(facts, "permission_checked", True)
        _require_bool(facts, "workspace_admin_observed", True)
        _require_bool(facts, "new_dashboard_inheritance_observed", True)
        _require_bool(facts, "snapshot_observed", True)
        _require_bool(facts, "reapply_observed", True)
        _require_bool(facts, "auto_propagation_claimed", False)
        if _require_bool(facts, "published") and not case["publication_may_be_required"]:
            _fail("V12_PUBLICATION_FORBIDDEN", "Publicação não pertence a esta jornada.")
        if facts["published"]:
            pub_ref = facts.get("publication_authorization_ref")
            if type(pub_ref) is not str or len(pub_ref.strip()) < 4:
                _fail("V12_PUBLICATION_AUTH", "Publicação observada exige autorização própria registrada.")


def _validate_human_pass(record: dict[str, Any], case: dict[str, Any]) -> None:
    if record["environment"]:
        _fail("V12_HUMAN_ENV_MIX", "UAT humano deve ter registro próprio; evidência de ambiente é referenciada por artefato.")
    human = record["human"]
    facts = record["facts"]
    expected_keys = {"participant_alias", "participant_authorized", "participant_role"}
    if set(human) != expected_keys:
        _fail("V12_HUMAN_SHAPE", "Registro humano precisa usar alias, autorização e papel.")
    if type(human["participant_alias"]) is not str or not re.fullmatch(r"P-[A-Z0-9_-]{1,32}", human["participant_alias"]):
        _fail("V12_PARTICIPANT_ALIAS", "Use alias não identificável no formato P-...")
    if human["participant_authorized"] is not True or facts.get("participant_authorized") is not True:
        _fail("V12_PARTICIPANT_AUTH", "PASS humano exige participante autorizado.")
    if human["participant_role"] not in _ALLOWED_HUMAN_ROLES:
        _fail("V12_PARTICIPANT_ROLE", "Papel humano não reconhecido.")
    if "observed_seconds" in facts:
        seconds = facts["observed_seconds"]
        if type(seconds) not in (int, float) or type(seconds) is bool or seconds < 0:
            _fail("V12_DURATION", "Tempo observado precisa ser número não negativo.")
    if "help_events" in facts:
        if type(facts["help_events"]) is not list:
            _fail("V12_HELP_EVENTS", "Ajuda recebida precisa ser lista; zero ajuda é lista vazia.")
    if record["case_id"] == "DOC-02":
        _require_bool(facts, "next_action_identified_without_help", True)
        if type(facts.get("document_version")) is not str or not facts["document_version"].strip():
            _fail("V12_DOCUMENT_VERSION", "DOC-02 precisa fixar a versão do documento avaliado.")
    if record["case_id"] == "DOC-03":
        _require_bool(facts, "scope_persistence_explained_correctly", True)
        if type(facts.get("document_version")) is not str or not facts["document_version"].strip():
            _fail("V12_DOCUMENT_VERSION", "DOC-03 precisa fixar a versão do documento avaliado.")
    if record["case_id"] == "A11-01":
        _require_bool(facts, "render_observed", True)
        _require_bool(facts, "keyboard_review", True)
        _require_bool(facts, "zoom_review", True)
        measurements = facts.get("contrast_measurements")
        if type(measurements) is not list or not measurements:
            _fail("V12_CONTRAST", "A11-01 exige medições de contraste do render observado.")
        for measurement in measurements:
            if type(measurement) is not dict or set(measurement) != {"label", "ratio", "required_ratio"}:
                _fail("V12_CONTRAST", "Cada medição deve declarar label, ratio e required_ratio.")
            ratio = measurement["ratio"]
            required_ratio = measurement["required_ratio"]
            if type(ratio) not in (int, float) or type(ratio) is bool or ratio < 0:
                _fail("V12_CONTRAST", "ratio precisa ser número não negativo.")
            if required_ratio not in (3, 3.0, 4.5):
                _fail("V12_CONTRAST", "required_ratio precisa ser 3,0 ou 4,5 conforme classificação do texto.")
            if ratio < required_ratio:
                _fail("V12_CONTRAST", "PASS não pode arredondar contraste abaixo do limiar.")
    if record["case_id"] == "UAT-01":
        _require_bool(facts, "journey_completed", True)
        _require_bool(facts, "shared_change_absent", True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", type=Path, required=True, help="Registro JSON de evidência V12.")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    args = parser.parse_args()
    try:
        matrix = load_matrix(args.matrix)
        record = json.loads(args.validate.read_text(encoding="utf-8"))
        validate_evidence(record, matrix)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, V12EvidenceError) as exc:
        print(f"FAIL V12: {exc}")
        return 1
    print(f"PASS V12 EVIDENCE: {record['record_id']} / {record['case_id']} / {record['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
