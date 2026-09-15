"""Validador de referência da MM01 para o contrato canônico de micromodelos.

Este módulo é ferramenta de construção/CI do repositório. Ele não cria uma nova
skill nem um helper público do Hub. A futura skill `hub-ml-micromodelos` deverá
incorporar ou derivar este contrato somente na sprint em que seu roteamento for
criado.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_VERSION = "1.0.0"
ALLOWED_CATALOG_REFS = frozenset({"CATALOGO_PRODUTO"})

FASES = (
    "IDEIA",
    "EM_DESCOBERTA",
    "EM_ESTUDO",
    "EM_VALIDACAO",
    "VALIDADO",
    "CANDIDATO_PRODUTO",
    "EM_VALIDACAO_GOVERNANCA",
    "PUBLICADO",
)

TRANSICOES_FASE = frozenset(
    {
        (None, "IDEIA"),
        ("IDEIA", "EM_DESCOBERTA"),
        ("EM_DESCOBERTA", "EM_ESTUDO"),
        ("EM_ESTUDO", "EM_VALIDACAO"),
        ("EM_VALIDACAO", "VALIDADO"),
        ("EM_VALIDACAO", "EM_ESTUDO"),
        ("VALIDADO", "CANDIDATO_PRODUTO"),
        ("VALIDADO", "EM_ESTUDO"),
        ("CANDIDATO_PRODUTO", "EM_VALIDACAO_GOVERNANCA"),
        ("CANDIDATO_PRODUTO", "VALIDADO"),
        ("EM_VALIDACAO_GOVERNANCA", "PUBLICADO"),
        ("EM_VALIDACAO_GOVERNANCA", "CANDIDATO_PRODUTO"),
    }
)

FASE_ORDEM = {fase: indice for indice, fase in enumerate(FASES)}


@dataclass(frozen=True)
class Issue:
    path: str
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code} @ {self.path}: {self.message}"


def _path(parts: Iterable[Any]) -> str:
    rendered: list[str] = []
    for part in parts:
        if isinstance(part, int):
            rendered.append(f"[{part}]")
        else:
            if rendered:
                rendered.append(".")
            rendered.append(str(part))
    return "".join(rendered) or "$"


def _pairs_without_duplicates(pairs: list[tuple[Any, Any]]) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"chave duplicada recusada: {key!r}")
        result[key] = value
    return result


def _load_yaml_without_duplicate_keys(text: str) -> Any:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - depende do ambiente
        raise RuntimeError(
            "PyYAML é necessário para ler .yaml/.yml no gate de manutenção; "
            "instale tools/requirements-dev.txt."
        ) from exc

    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(f"chave YAML duplicada recusada: {key!r}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping,
    )
    return yaml.load(text, Loader=UniqueKeyLoader)


def load_document(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        loaded = json.loads(text, object_pairs_hook=_pairs_without_duplicates)
    else:
        loaded = _load_yaml_without_duplicate_keys(text)
    if not isinstance(loaded, dict):
        raise ValueError("o documento raiz precisa ser um mapping/objeto")
    return loaded


def load_schema(path: str | Path) -> dict[str, Any]:
    loaded = json.loads(
        Path(path).read_text(encoding="utf-8"),
        object_pairs_hook=_pairs_without_duplicates,
    )
    if not isinstance(loaded, dict):
        raise ValueError("schema raiz precisa ser um objeto JSON")
    return loaded


def _normalize_semantic_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value).casefold()
    without_accents = "".join(
        char for char in decomposed if not unicodedata.combining(char)
    )
    words_only = re.sub(r"[\W_]+", " ", without_accents, flags=re.UNICODE)
    return " ".join(words_only.split())


def _has_material_text(value: Any) -> bool:
    """Exige ao menos uma letra ou número Unicode após normalização.

    Marcas combinantes, variation selectors, espaços, controles e pontuação
    isolada não constituem identidade/referência auditável.
    """
    if not isinstance(value, str):
        return False
    normalized = unicodedata.normalize("NFKC", value)
    return any(unicodedata.category(char)[0] in {"L", "N"} for char in normalized)


MATERIAL_FORMAT_CHECKER = FormatChecker()


@MATERIAL_FORMAT_CHECKER.checks("material-text")
def _check_material_text_format(value: Any) -> bool:
    """Implementa no schema a mesma política Unicode usada pelos gates semânticos."""
    if not isinstance(value, str):
        return True
    return _has_material_text(value)


def _semver_tuple(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value)
    if not match:
        raise ValueError(f"versão semântica inválida: {value!r}")
    return tuple(int(part) for part in match.groups())


def _validate_previous_state(
    spec: dict[str, Any], previous_spec: dict[str, Any], issues: list[Issue]
) -> None:
    current_identity = spec["identidade"]
    previous_identity = previous_spec["identidade"]
    if current_identity["nome"] != previous_identity["nome"]:
        issues.append(
            Issue(
                "identidade.nome",
                "PREVIOUS_IDENTITY_MISMATCH",
                "a especificação anterior precisa pertencer ao mesmo micromodelo",
            )
        )
        return

    current_version = _semver_tuple(current_identity["micromodel_version"])
    previous_version = _semver_tuple(previous_identity["micromodel_version"])
    if current_version < previous_version:
        issues.append(
            Issue(
                "identidade.micromodel_version",
                "VERSION_REWIND",
                "micromodel_version não pode regredir em relação à especificação anterior",
            )
        )
        return

    # Uma nova versão material inicia seu próprio ciclo; MM02 ainda cuidará do fingerprint.
    if current_version > previous_version:
        return

    current_state = current_identity["estado"]
    previous_state = previous_identity["estado"]
    current_phase = current_state["fase_atual"]
    previous_phase = previous_state["fase_atual"]

    if current_phase == previous_phase:
        if current_state["fase_anterior"] != previous_state["fase_anterior"]:
            issues.append(
                Issue(
                    "identidade.estado.fase_anterior",
                    "PREVIOUS_HISTORY_REWRITE",
                    "a mesma versão não pode reescrever fase_anterior sem mudar de fase",
                )
            )
        return

    if previous_phase == "PUBLICADO":
        issues.append(
            Issue(
                "identidade.estado.fase_atual",
                "STATE_REWIND",
                "uma versão já PUBLICADA não pode voltar a fase anterior; crie versão material superior",
            )
        )
        return

    if current_state["fase_anterior"] != previous_phase:
        issues.append(
            Issue(
                "identidade.estado.fase_anterior",
                "PREVIOUS_STATE_MISMATCH",
                f"fase_anterior deve refletir a fase observada na especificação anterior: {previous_phase}",
            )
        )
        return

    if (previous_phase, current_phase) not in TRANSICOES_FASE:
        issues.append(
            Issue(
                "identidade.estado",
                "STATE_TRANSITION",
                f"transição observada {previous_phase!r} -> {current_phase!r} não é permitida",
            )
        )

def _validate_provenance(prov: dict[str, Any], path: str, issues: list[Issue]) -> None:
    status = prov.get("status")
    approval = prov.get("aprovacao")
    measurement = prov.get("medicao")

    if not _has_material_text(prov.get("origem")):
        issues.append(Issue(f"{path}.origem", "PROV_ORIGIN_REQUIRED", "origem precisa ter conteúdo auditável"))
    if prov.get("referencia") is not None and not _has_material_text(prov.get("referencia")):
        issues.append(Issue(f"{path}.referencia", "PROV_REFERENCE_BLANK", "referencia não pode ser vazia/whitespace"))

    if status == "APROVADO":
        if not isinstance(approval, dict):
            issues.append(
                Issue(path, "PROV_APPROVAL_REQUIRED", "APROVADO exige bloco aprovacao completo")
            )
        elif not (
            _has_material_text(approval.get("por"))
            and _has_material_text(approval.get("referencia"))
        ):
            issues.append(
                Issue(
                    f"{path}.aprovacao",
                    "PROV_APPROVAL_REQUIRED",
                    "APROVADO exige por/referencia com conteúdo auditável",
                )
            )
    elif approval is not None:
        issues.append(
            Issue(path, "PROV_APPROVAL_MISMATCH", "aprovacao só é permitida quando status=APROVADO")
        )

    if status == "MEDIDO":
        if not isinstance(measurement, dict):
            issues.append(
                Issue(
                    path,
                    "PROV_MEASUREMENT_REQUIRED",
                    "MEDIDO exige medicao com referencia_execucao e medido_em_utc",
                )
            )
        elif not _has_material_text(measurement.get("referencia_execucao")):
            issues.append(
                Issue(
                    f"{path}.medicao.referencia_execucao",
                    "PROV_MEASUREMENT_REQUIRED",
                    "MEDIDO exige referencia_execucao com conteúdo auditável",
                )
            )
    elif measurement is not None:
        issues.append(
            Issue(path, "PROV_MEASUREMENT_MISMATCH", "medicao só é permitida quando status=MEDIDO")
        )

def _check_duplicate_ids(items: list[dict[str, Any]], base: str, issues: list[Issue]) -> None:
    seen: set[str] = set()
    for index, item in enumerate(items):
        item_id = item["id"]
        if item_id in seen:
            issues.append(Issue(f"{base}[{index}].id", "DUPLICATE_ID", f"id duplicado: {item_id}"))
        seen.add(item_id)


def validate_spec(
    spec: dict[str, Any],
    schema: dict[str, Any],
    previous_spec: dict[str, Any] | None = None,
) -> list[Issue]:
    issues: list[Issue] = []
    validator = Draft202012Validator(schema, format_checker=MATERIAL_FORMAT_CHECKER)
    for error in sorted(validator.iter_errors(spec), key=lambda e: list(e.absolute_path)):
        issues.append(Issue(_path(error.absolute_path), "SCHEMA", error.message))
    if issues:
        return issues

    if previous_spec is not None:
        previous_issues = validate_spec(previous_spec, schema)
        if previous_issues:
            issues.append(
                Issue(
                    "$previous",
                    "PREVIOUS_SPEC_INVALID",
                    "a especificação anterior fornecida também precisa ser válida no contrato MM01",
                )
            )
            return issues
        _validate_previous_state(spec, previous_spec, issues)

    estado = spec["identidade"]["estado"]
    phase = estado["fase_atual"]
    transition = (estado["fase_anterior"], estado["fase_atual"])
    if transition not in TRANSICOES_FASE:
        issues.append(
            Issue(
                "identidade.estado",
                "STATE_TRANSITION",
                f"transição {transition[0]!r} -> {transition[1]!r} não é permitida",
            )
        )

    condicao = estado["condicao"]
    motivo = estado["motivo_condicao"]
    if condicao == "ATIVO" and motivo not in (None, ""):
        issues.append(
            Issue(
                "identidade.estado.motivo_condicao",
                "STATE_CONDITION",
                "ATIVO não deve carregar motivo de bloqueio/suspensão/depreciação",
            )
        )
    if condicao != "ATIVO" and not (isinstance(motivo, str) and motivo.strip()):
        issues.append(
            Issue(
                "identidade.estado.motivo_condicao",
                "STATE_CONDITION",
                f"{condicao} exige motivo_condicao",
            )
        )
    if estado["fase_atual"] == "PUBLICADO" and condicao == "BLOQUEADO":
        issues.append(
            Issue(
                "identidade.estado.condicao",
                "STATE_CONDITION",
                "PUBLICADO não usa BLOQUEADO; use SUSPENSO ou DEPRECATED",
            )
        )
    if estado["fase_atual"] == "IDEIA" and condicao == "DEPRECATED":
        issues.append(
            Issue(
                "identidade.estado.condicao",
                "STATE_CONDITION",
                "IDEIA não pode nascer DEPRECATED",
            )
        )

    source_ids: set[str] = set()
    for index, source in enumerate(spec["fontes"]):
        source_id = source["id"]
        if source_id in source_ids:
            issues.append(
                Issue(f"fontes[{index}].id", "DUPLICATE_ID", f"id duplicado: {source_id}")
            )
        source_ids.add(source_id)
        if source["catalogo_ref"] not in ALLOWED_CATALOG_REFS:
            issues.append(
                Issue(
                    f"fontes[{index}].catalogo_ref",
                    "CATALOG_SCOPE",
                    f"catalogo_ref {source['catalogo_ref']!r} fora do escopo permitido "
                    f"{sorted(ALLOWED_CATALOG_REFS)!r}",
                )
            )
        _validate_provenance(
            source["proveniencia"], f"fontes[{index}].proveniencia", issues
        )

    def validate_evidence(items: list[dict[str, Any]], base: str) -> None:
        _check_duplicate_ids(items, base, issues)
        for index, item in enumerate(items):
            unknown = sorted(set(item["fontes_ref"]) - source_ids)
            if unknown:
                issues.append(
                    Issue(
                        f"{base}[{index}].fontes_ref",
                        "UNKNOWN_SOURCE_REF",
                        f"fontes inexistentes: {unknown}",
                    )
                )
            _validate_provenance(
                item["proveniencia"], f"{base}[{index}].proveniencia", issues
            )

    validate_evidence(spec["evidencias"], "evidencias")
    validate_evidence(spec["contra_evidencias"], "contra_evidencias")

    classification = spec["classificacao"]
    semantics = classification["semantica"]
    semantics_prov = semantics["proveniencia"]
    _validate_provenance(
        semantics_prov, "classificacao.semantica.proveniencia", issues
    )
    semantic_values = [
        _normalize_semantic_text(semantics["quando_true"]),
        _normalize_semantic_text(semantics["quando_false"]),
        _normalize_semantic_text(semantics["quando_indeterminado"]),
    ]
    if len(set(semantic_values)) != 3:
        issues.append(
            Issue(
                "classificacao.semantica",
                "AMBIGUOUS_BINARY_SEMANTICS",
                "TRUE, FALSE e INDETERMINADO precisam ter definições distintas, "
                "inclusive após normalização editorial",
            )
        )

    absence = classification["ausencia_evidencia"]
    _validate_provenance(
        absence["proveniencia"], "classificacao.ausencia_evidencia.proveniencia", issues
    )
    if absence["tratamento"] == "INDETERMINADO":
        if (
            absence["resultado_sem_evidencia"] != "INDETERMINADO"
            or absence["regra_ref"] is not None
        ):
            issues.append(
                Issue(
                    "classificacao.ausencia_evidencia",
                    "MISSING_POLICY_CONTRADICTION",
                    "tratamento INDETERMINADO exige resultado_sem_evidencia=INDETERMINADO e regra_ref=null",
                )
            )
    else:
        if absence["proveniencia"]["status"] != "APROVADO":
            issues.append(
                Issue(
                    "classificacao.ausencia_evidencia.proveniencia.status",
                    "MISSING_POLICY_APPROVAL",
                    "REGRA_EXPLICITA_APROVADA exige proveniência APROVADO",
                )
            )
        if not _has_material_text(absence["regra_ref"]):
            issues.append(
                Issue(
                    "classificacao.ausencia_evidencia.regra_ref",
                    "MISSING_POLICY_RULE_REF",
                    "REGRA_EXPLICITA_APROVADA exige referência auditável para a regra",
                )
            )

    threshold_ids: set[str] = set()
    for index, threshold in enumerate(classification["limiares"]):
        if threshold["id"] in threshold_ids:
            issues.append(
                Issue(
                    f"classificacao.limiares[{index}].id",
                    "DUPLICATE_ID",
                    f"id duplicado: {threshold['id']}",
                )
            )
        threshold_ids.add(threshold["id"])
        _validate_provenance(
            threshold["proveniencia"],
            f"classificacao.limiares[{index}].proveniencia",
            issues,
        )
        if (
            FASE_ORDEM[phase] >= FASE_ORDEM["EM_VALIDACAO"]
            and threshold["proveniencia"]["status"] != "APROVADO"
        ):
            issues.append(
                Issue(
                    f"classificacao.limiares[{index}].proveniencia.status",
                    "THRESHOLD_APPROVAL",
                    "limiar material exige decisão humana APROVADO",
                )
            )

    experiment_by_id = {item["id"]: item for item in spec["experimentos"]}

    score = spec["score"]
    _validate_provenance(score["proveniencia"], "score.proveniencia", issues)
    _check_duplicate_ids(score["componentes"], "score.componentes", issues)
    if score["habilitado"]:
        if not score["tipo_semantica"]:
            issues.append(
                Issue(
                    "score.tipo_semantica",
                    "SCORE_SEMANTICS",
                    "score habilitado exige tipo_semantica estruturado",
                )
            )
        if (
            not isinstance(score["escala"], dict)
            or score["escala"].get("min") != 0
            or score["escala"].get("max") != 100
        ):
            issues.append(
                Issue(
                    "score.escala",
                    "SCORE_SCALE",
                    "score habilitado neste contrato precisa usar escala 0–100",
                )
            )
        if spec["saida"]["estudo"]["campo_score"] in (None, ""):
            issues.append(
                Issue(
                    "saida.estudo.campo_score",
                    "SCORE_OUTPUT",
                    "score habilitado exige campo_score no contrato de estudo",
                )
            )

        normalization = score["normalizacao"]
        if isinstance(normalization, dict):
            _validate_provenance(
                normalization["proveniencia"],
                "score.normalizacao.proveniencia",
                issues,
            )

        for index, component in enumerate(score["componentes"]):
            _validate_provenance(
                component["proveniencia"],
                f"score.componentes[{index}].proveniencia",
                issues,
            )
            if (
                FASE_ORDEM[phase] >= FASE_ORDEM["EM_VALIDACAO"]
                and component["proveniencia"]["status"] != "APROVADO"
            ):
                issues.append(
                    Issue(
                        f"score.componentes[{index}].proveniencia.status",
                        "WEIGHT_APPROVAL",
                        "peso material exige decisão humana APROVADO",
                    )
                )

        if FASE_ORDEM[phase] >= FASE_ORDEM["EM_VALIDACAO"]:
            if not _has_material_text(score["semantica_ref"]):
                issues.append(
                    Issue(
                        "score.semantica_ref",
                        "SCORE_SEMANTICS",
                        "EM_VALIDACAO ou posterior exige referência auditável da semântica do score",
                    )
                )
            if not isinstance(normalization, dict) or normalization["metodo"] == "PENDENTE":
                issues.append(
                    Issue(
                        "score.normalizacao",
                        "SCORE_NORMALIZATION",
                        "EM_VALIDACAO ou posterior exige método estruturado de normalização",
                    )
                )
            elif normalization["proveniencia"]["status"] != "APROVADO":
                issues.append(
                    Issue(
                        "score.normalizacao.proveniencia.status",
                        "SCORE_NORMALIZATION_APPROVAL",
                        "normalização material exige decisão humana APROVADO",
                    )
                )
            if (
                isinstance(normalization, dict)
                and normalization["metodo"] == "CUSTOM_APROVADO"
                and not _has_material_text(normalization["referencia"])
            ):
                issues.append(
                    Issue(
                        "score.normalizacao.referencia",
                        "SCORE_NORMALIZATION_REF",
                        "CUSTOM_APROVADO exige referência auditável da regra de normalização",
                    )
                )

        if score["tipo_semantica"] == "PROBABILIDADE_CALIBRADA":
            if not isinstance(score["calibracao"], dict):
                issues.append(
                    Issue(
                        "score.calibracao",
                        "CALIBRATION_REQUIRED",
                        "PROBABILIDADE_CALIBRADA exige bloco calibracao",
                    )
                )
            else:
                _validate_provenance(
                    score["calibracao"]["proveniencia"],
                    "score.calibracao.proveniencia",
                    issues,
                )
                if score["calibracao"]["proveniencia"]["status"] != "MEDIDO":
                    issues.append(
                        Issue(
                            "score.calibracao.proveniencia.status",
                            "CALIBRATION_EVIDENCE",
                            "probabilidade só pode ser declarada com calibração MEDIDA",
                        )
                    )
                evidence_ref = score["calibracao"]["evidencia_ref"]
                referenced_experiment = experiment_by_id.get(evidence_ref)
                if referenced_experiment is None:
                    issues.append(
                        Issue(
                            "score.calibracao.evidencia_ref",
                            "CALIBRATION_EVIDENCE_REF",
                            "evidencia_ref deve apontar para experimentos[].id existente",
                        )
                    )
                elif (
                    referenced_experiment["status"] != "EXECUTADO"
                    or referenced_experiment["proveniencia"]["status"] != "MEDIDO"
                ):
                    issues.append(
                        Issue(
                            "score.calibracao.evidencia_ref",
                            "CALIBRATION_EVIDENCE_REF",
                            "calibração exige experimento EXECUTADO com proveniência MEDIDO",
                        )
                    )
        elif score["calibracao"] is not None:
            issues.append(
                Issue(
                    "score.calibracao",
                    "CALIBRATION_UNEXPECTED",
                    "calibração probabilística só é permitida para PROBABILIDADE_CALIBRADA",
                )
            )
    else:
        if any(
            (
                score["tipo_semantica"] is not None,
                score["semantica_ref"] is not None,
                score["escala"] is not None,
                score["normalizacao"] is not None,
                score["componentes"],
                score["calibracao"] is not None,
            )
        ):
            issues.append(
                Issue(
                    "score",
                    "SCORE_DISABLED",
                    "score desabilitado deve manter semântica, escala, normalização, componentes e calibração vazios/nulos",
                )
            )
        if spec["saida"]["estudo"]["campo_score"] is not None:
            issues.append(
                Issue(
                    "saida.estudo.campo_score",
                    "SCORE_DISABLED",
                    "score desabilitado exige campo_score=null",
                )
            )

    _check_duplicate_ids(spec["experimentos"], "experimentos", issues)
    for index, experiment in enumerate(spec["experimentos"]):
        _validate_provenance(
            experiment["proveniencia"], f"experimentos[{index}].proveniencia", issues
        )
        if experiment["status"] == "EXECUTADO":
            if not isinstance(experiment["resultado"], str) or not experiment["resultado"].strip():
                issues.append(
                    Issue(
                        f"experimentos[{index}].resultado",
                        "EXPERIMENT_RESULT",
                        "EXECUTADO exige resultado",
                    )
                )
            if experiment["proveniencia"]["status"] != "MEDIDO":
                issues.append(
                    Issue(
                        f"experimentos[{index}].proveniencia.status",
                        "EXPERIMENT_MEASUREMENT",
                        "EXECUTADO exige proveniência MEDIDO",
                    )
                )
        elif experiment["proveniencia"]["status"] == "MEDIDO":
            issues.append(
                Issue(
                    f"experimentos[{index}].proveniencia.status",
                    "EXPERIMENT_MEASUREMENT",
                    "resultado MEDIDO só é válido para experimento EXECUTADO",
                )
            )

    validation = spec["validacao"]
    if validation["resultado"] is not None:
        _validate_provenance(
            validation["resultado"]["proveniencia"],
            "validacao.resultado.proveniencia",
            issues,
        )
        if validation["resultado"]["proveniencia"]["status"] != "MEDIDO":
            issues.append(
                Issue(
                    "validacao.resultado.proveniencia.status",
                    "VALIDATION_MEASUREMENT",
                    "resultado de validação precisa ser MEDIDO",
                )
            )
    if validation["status"] in {"APROVADO", "REPROVADO"} and validation["resultado"] is None:
        issues.append(
            Issue(
                "validacao.resultado",
                "VALIDATION_RESULT_REQUIRED",
                f"status {validation['status']} exige resultado medido",
            )
        )

    approval = validation["aprovacao_humana"]
    if validation["status"] in {"APROVADO", "REPROVADO"}:
        if (
            approval["status"] != validation["status"]
            or not _has_material_text(approval.get("por"))
            or not approval.get("em_utc")
            or not _has_material_text(approval.get("referencia"))
        ):
            issues.append(
                Issue(
                    "validacao.aprovacao_humana",
                    "VALIDATION_HUMAN_GATE",
                    "decisão humana precisa coincidir com validacao.status e registrar "
                    "por/em_utc/referencia",
                )
            )

    if FASE_ORDEM[phase] >= FASE_ORDEM["EM_VALIDACAO"]:
        required_nonempty = (
            ("fontes", spec["fontes"]),
            ("evidencias", spec["evidencias"]),
            ("contra_evidencias", spec["contra_evidencias"]),
            ("validacao.criterios", validation["criterios"]),
        )
        for path, collection in required_nonempty:
            if not collection:
                issues.append(
                    Issue(
                        path,
                        "PHASE_CONTENT_GATE",
                        f"fase {phase} exige {path} não vazio para validação formal",
                    )
                )

        for base_name in ("evidencias", "contra_evidencias"):
            for index, item in enumerate(spec[base_name]):
                if item["proveniencia"]["status"] != "APROVADO":
                    issues.append(
                        Issue(
                            f"{base_name}[{index}].proveniencia.status",
                            "EVIDENCE_RULE_APPROVAL",
                            "EM_VALIDACAO ou posterior exige regra de "
                            "evidência/contra-evidência APROVADA",
                        )
                    )
        if score["habilitado"] and score["proveniencia"]["status"] != "APROVADO":
            issues.append(
                Issue(
                    "score.proveniencia.status",
                    "SCORE_APPROVAL",
                    "EM_VALIDACAO ou posterior exige semântica do score aprovada",
                )
            )
        if semantics_prov["status"] != "APROVADO":
            issues.append(
                Issue(
                    "classificacao.semantica.proveniencia.status",
                    "SEMANTICS_APPROVAL",
                    "EM_VALIDACAO ou posterior exige semântica "
                    "TRUE/FALSE/INDETERMINADO aprovada",
                )
            )
        if absence["proveniencia"]["status"] != "APROVADO":
            issues.append(
                Issue(
                    "classificacao.ausencia_evidencia.proveniencia.status",
                    "MISSING_POLICY_APPROVAL",
                    "EM_VALIDACAO ou posterior exige política de ausência "
                    "de evidência aprovada",
                )
            )

    if FASE_ORDEM[phase] >= FASE_ORDEM["VALIDADO"] and validation["status"] != "APROVADO":
        issues.append(
            Issue(
                "validacao.status",
                "PHASE_GATE",
                f"fase {phase} exige validacao.status=APROVADO",
            )
        )

    publication_output = spec["saida"]["publicacao"]
    if FASE_ORDEM[phase] >= FASE_ORDEM["CANDIDATO_PRODUTO"]:
        if (
            publication_output["estado"] != "DEFINIDO"
            or publication_output["campo_booleano"] is None
            or publication_output["politica_indeterminado"] is None
        ):
            issues.append(
                Issue(
                    "saida.publicacao",
                    "PUBLICATION_OUTPUT_GATE",
                    f"fase {phase} exige contrato de publicação definido, "
                    "inclusive política de INDETERMINADO",
                )
            )
        else:
            _validate_provenance(
                publication_output["politica_indeterminado"]["proveniencia"],
                "saida.publicacao.politica_indeterminado.proveniencia",
                issues,
            )
            if (
                publication_output["politica_indeterminado"]["proveniencia"]["status"]
                != "APROVADO"
            ):
                issues.append(
                    Issue(
                        "saida.publicacao.politica_indeterminado.proveniencia.status",
                        "PUBLICATION_OUTPUT_APPROVAL",
                        "tratamento de INDETERMINADO na publicação exige APROVADO",
                    )
                )
            policy = publication_output["politica_indeterminado"]
            if policy["indeterminado_vira_false"] is not False:
                issues.append(
                    Issue(
                        "saida.publicacao.politica_indeterminado.indeterminado_vira_false",
                        "INDETERMINATE_FALSE_POLICY",
                        "INDETERMINADO nunca pode ser implicitamente convertido em FALSE",
                    )
                )
            if policy["tratamento"] == "OUTRA_APROVADA":
                if not _has_material_text(policy["regra_ref"]):
                    issues.append(
                        Issue(
                            "saida.publicacao.politica_indeterminado.regra_ref",
                            "PUBLICATION_POLICY_RULE_REF",
                            "OUTRA_APROVADA exige referência auditável da regra externa",
                        )
                    )
            elif policy["regra_ref"] is not None:
                issues.append(
                    Issue(
                        "saida.publicacao.politica_indeterminado.regra_ref",
                        "PUBLICATION_POLICY_RULE_REF",
                        "regra_ref só é usada quando tratamento=OUTRA_APROVADA",
                    )
                )

    publication = spec["publicacao"]
    publication_status = publication["status"]
    if FASE_ORDEM[phase] < FASE_ORDEM["CANDIDATO_PRODUTO"]:
        if publication_status != "NAO_INICIADA":
            issues.append(
                Issue(
                    "publicacao.status",
                    "PUBLICATION_STATUS_PHASE",
                    f"fase {phase} exige publicacao.status=NAO_INICIADA",
                )
            )
    elif phase == "CANDIDATO_PRODUTO":
        if publication_status not in {"CANDIDATA", "REJEITADA"}:
            issues.append(
                Issue(
                    "publicacao.status",
                    "PUBLICATION_STATUS_PHASE",
                    "CANDIDATO_PRODUTO exige status CANDIDATA ou REJEITADA",
                )
            )
    elif phase == "EM_VALIDACAO_GOVERNANCA":
        if (
            publication_status != "EM_VALIDACAO_EXTERNA"
            or not _has_material_text(publication["handoff_ref"])
        ):
            issues.append(
                Issue(
                    "publicacao",
                    "PUBLICATION_GATE",
                    "EM_VALIDACAO_GOVERNANCA exige handoff_ref e status "
                    "EM_VALIDACAO_EXTERNA",
                )
            )
    elif phase == "PUBLICADO":
        if (
            publication_status != "PUBLICADA"
            or not _has_material_text(publication["produto_dados_ref"])
        ):
            issues.append(
                Issue(
                    "publicacao",
                    "PUBLICATION_GATE",
                    "PUBLICADO exige publicação externa confirmada e produto_dados_ref",
                )
            )

    if spec["tracking"]["armazenar_historico_runs_no_yaml"] is not False:
        issues.append(
            Issue(
                "tracking.armazenar_historico_runs_no_yaml",
                "TRACKING_BOUNDARY",
                "histórico de runs pertence ao backend de tracking, não ao YAML",
            )
        )

    for index, record in enumerate(spec["proveniencia"]["registros"]):
        _validate_provenance(
            record["proveniencia"],
            f"proveniencia.registros[{index}].proveniencia",
            issues,
        )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida micromodelo contra contrato MM01")
    parser.add_argument("documento", help="micromodelo.yaml/.yml/.json")
    parser.add_argument(
        "--schema",
        required=True,
        help="caminho para micromodelo.schema.json",
    )
    parser.add_argument(
        "--previous",
        help="especificação anterior confiável para validar evolução/anti-rewind",
    )
    args = parser.parse_args()

    try:
        spec = load_document(args.documento)
        schema = load_schema(args.schema)
        previous_spec = load_document(args.previous) if args.previous else None
        issues = validate_spec(spec, schema, previous_spec=previous_spec)
    except Exception as exc:
        print(f"ERRO_DE_CARGA: {exc}")
        return 2

    if issues:
        for issue in issues:
            print(issue)
        print(f"REPROVADO: {len(issues)} problema(s)")
        return 1
    print("APROVADO: contrato MM01 válido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
