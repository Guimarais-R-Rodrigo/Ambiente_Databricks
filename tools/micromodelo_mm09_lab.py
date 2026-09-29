"""Piloto greenfield MM09–MM10-LAB: E0 sintético, sem Databricks ou MLflow.

Orquestra o entrypoint MM04, contrato MM01, fingerprint MM02 e artefatos MM06.
As regras de avaliação abaixo são escolhas explícitas do cenário de laboratório;
não são parâmetros aprovados de negócio nem um executor corporativo.
"""
from __future__ import annotations

import copy
from datetime import date
from pathlib import Path
from typing import Any

import micromodelo_mm01_contract as mm01
import micromodelo_mm02_fingerprint as mm02
import micromodelo_mm03_metadata as mm03
import micromodelo_mm04_flow as mm04
import micromodelo_mm06_artifacts as mm06


LAB_SCORER_VERSION = "mm09-synthetic-heuristic-v1"
# Perfil material fechado deste cenário. Mudanças válidas de operador, janela,
# semântica, fontes, pesos ou contrato de saída exigem uma nova versão do piloto.
LAB_PROFILE_FINGERPRINT = "85af625b7ea71babeb00051da089dfc63d4faab2e1f995c4f7a191a2aee79e88"
LAB_SOURCE = Path(__file__).resolve().parents[1] / (
    "tools/tests/fixtures/micromodelos_mm03/catalogo_sintetico.json"
)


class LabError(ValueError):
    """Entrada sintética incompatível com o cenário fechado."""


def _proposed(origin: str) -> dict[str, Any]:
    return {"status": "PROPOSTO", "origem": origin, "referencia": None,
            "observado_em_utc": None, "aprovacao": None, "medicao": None}


def _require_valid(spec: dict[str, Any], schema: dict[str, Any],
                   previous: dict[str, Any] | None = None) -> None:
    issues = mm01.validate_spec(spec, schema, previous_spec=previous)
    if issues:
        raise LabError("INVALID_MM01_LAB_SPEC: " + ",".join(issue.code for issue in issues))


def _metadata_fixture() -> dict[str, Any]:
    fixture, _ = mm03.load_fixture(LAB_SOURCE)
    fixture = copy.deepcopy(fixture)
    for stream in fixture["streams"]:
        if stream["operation"] == "columns" and stream["scope"] == ["crm_sintetico", "eventos_sinteticos"]:
            stream["items"].extend([
                {"name": "event_id", "data_type": "STRING", "nullable": False,
                 "description": "Identificador único do evento sintético."},
                {"name": "tipo_evento", "data_type": "STRING", "nullable": False,
                 "description": "Sinal sintético POSITIVO ou CONTRARIO."},
            ])
        if stream["operation"] == "columns" and stream["scope"] == ["crm_sintetico", "apoio_sintetico"]:
            stream["status"] = "OK"
            stream["items"] = [
                {"name": "id_entidade", "data_type": "STRING", "nullable": False,
                 "description": "Chave sintética da população."},
                {"name": "cobertura_completa", "data_type": "BOOLEAN", "nullable": False,
                 "description": "Cobertura sintética da janela observada."},
            ]
    return fixture


def _study_spec(discovery: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    _require_valid(discovery, schema)
    study = copy.deepcopy(discovery)
    study["identidade"]["estado"].update(
        {"fase_anterior": "EM_DESCOBERTA", "fase_atual": "EM_ESTUDO"}
    )
    study["entidade"].update({
        "tipo": "entidade sintética", "chave_logica": "id_entidade",
        "granularidade": "uma classificação por entidade e janela sintética",
        "populacao_elegivel": "seis entidades sintéticas da fixture do piloto",
        "referencia_temporal": "janela sintética fixa de setembro de 2026",
    })
    sources_by_object = {source["objeto"]: source for source in study["fontes"]}
    sources_by_object["apoio_sintetico"]["papel"] = "ELEGIBILIDADE"
    sources_by_object["eventos_sinteticos"]["papel"] = "EVIDENCIA"
    events_ref = sources_by_object["eventos_sinteticos"]["id"]
    study["evidencias"] = [{
        "id": "eventos_positivos", "descricao": "recorrência de sinal sintético positivo",
        "fontes_ref": [events_ref],
        "regra": "dois ou mais eventos POSITIVO na janela com cobertura completa",
        "proveniencia": _proposed("regra de laboratório E0"),
    }]
    study["contra_evidencias"] = [{
        "id": "evento_contrario", "descricao": "sinal sintético contrário explícito",
        "fontes_ref": [events_ref],
        "regra": "um ou mais eventos CONTRARIO prevalecem sobre sinais positivos",
        "proveniencia": _proposed("regra de laboratório E0"),
    }]
    study["classificacao"]["semantica"].update({
        "quando_true": "dois eventos POSITIVO com cobertura completa e nenhum CONTRARIO",
        "quando_false": "ao menos um evento CONTRARIO observado na janela",
        "quando_indeterminado": "sem CONTRARIO, cobertura parcial, sinal insuficiente ou ausência de evidência explícita",
        "proveniencia": _proposed("semântica de laboratório E0"),
    })
    study["classificacao"]["limiares"] = [{
        "id": "minimo_positivos", "descricao": "mínimo de sinais para TRUE",
        "operador": "GTE", "valor": 2, "unidade": "eventos_positivos",
        "proveniencia": _proposed("limiar sintético E0"),
    }]
    study["score"].update({
        "tipo_semantica": "FORCA_EVIDENCIA", "semantica_ref": None,
        "normalizacao": {"metodo": "SOMA_PONDERADA_0_100", "referencia": None,
                          "proveniencia": _proposed("heurística sintética E0")},
        "componentes": [
            {"id": "sinal_positivo", "descricao": "min(contagem POSITIVO/2, 1)",
             "peso": 0.6, "proveniencia": _proposed("heurística sintética E0")},
            {"id": "sem_contrario", "descricao": "1 se nenhum CONTRARIO; 0 caso contrário",
             "peso": 0.4, "proveniencia": _proposed("heurística sintética E0")},
        ],
        "proveniencia": _proposed("heurística sintética E0"),
    })
    _require_valid(study, schema, discovery)
    return study


def _synthetic_rows() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    population = [
        {"id_entidade": "entidade_a", "cobertura_completa": True},
        {"id_entidade": "entidade_b", "cobertura_completa": True},
        {"id_entidade": "entidade_c", "cobertura_completa": True},
        {"id_entidade": "entidade_d", "cobertura_completa": False},
        {"id_entidade": "entidade_e", "cobertura_completa": True},
        {"id_entidade": "entidade_f", "cobertura_completa": True},
    ]
    events = [
        {"event_id": "evento_001", "id_entidade": "entidade_a", "data_evento": "2026-09-01", "tipo_evento": "POSITIVO"},
        {"event_id": "evento_002", "id_entidade": "entidade_a", "data_evento": "2026-09-02", "tipo_evento": "POSITIVO"},
        {"event_id": "evento_003", "id_entidade": "entidade_b", "data_evento": "2026-09-03", "tipo_evento": "CONTRARIO"},
        {"event_id": "evento_004", "id_entidade": "entidade_c", "data_evento": "2026-09-04", "tipo_evento": "POSITIVO"},
        {"event_id": "evento_005", "id_entidade": "entidade_e", "data_evento": "2026-09-05", "tipo_evento": "POSITIVO"},
        {"event_id": "evento_006", "id_entidade": "entidade_e", "data_evento": "2026-09-06", "tipo_evento": "POSITIVO"},
        {"event_id": "evento_007", "id_entidade": "entidade_e", "data_evento": "2026-09-07", "tipo_evento": "CONTRARIO"},
    ]
    return population, events


def evaluate_synthetic_population(
    spec: dict[str, Any], population: list[dict[str, Any]], events: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Avalia somente o contrato fechado da fixture sintética MM09.

    Rejeita shapes/eventos fora do cenário e não converte ausência em FALSE.
    """
    _require_valid(spec, mm01.load_schema(mm04.SCHEMA))
    if mm02.calculate_spec_fingerprint(spec, mm01.load_schema(mm04.SCHEMA)).sha256 != LAB_PROFILE_FINGERPRINT:
        raise LabError("LAB_PROFILE_MISMATCH")
    if spec["identidade"]["estado"]["fase_atual"] != "EM_ESTUDO":
        raise LabError("LAB_PHASE_REQUIRED")
    thresholds = {item["id"]: item for item in spec["classificacao"]["limiares"]}
    components = {item["id"]: item for item in spec["score"]["componentes"]}
    if (set(thresholds) != {"minimo_positivos"} or
            set(components) != {"sinal_positivo", "sem_contrario"} or
            spec["classificacao"]["ausencia_evidencia"]["resultado_sem_evidencia"] != "INDETERMINADO" or
            spec["score"]["tipo_semantica"] != "FORCA_EVIDENCIA"):
        raise LabError("LAB_SPEC_UNSUPPORTED")
    minimum = thresholds["minimo_positivos"]["valor"]
    weights = {key: item["peso"] for key, item in components.items()}
    if (type(minimum) is not int or minimum <= 0 or
            abs(sum(weights.values()) - 1.0) > 1e-12):
        raise LabError("LAB_RULE_INVALID")
    by_entity: dict[str, dict[str, Any]] = {}
    for row in population:
        if (type(row) is not dict or set(row) != {"id_entidade", "cobertura_completa"} or
                type(row["id_entidade"]) is not str or not row["id_entidade"] or
                type(row["cobertura_completa"]) is not bool or
                row["id_entidade"] in by_entity):
            raise LabError("INVALID_POPULATION")
        by_entity[row["id_entidade"]] = row
    if not by_entity:
        raise LabError("EMPTY_POPULATION")
    counts = {key: {"POSITIVO": 0, "CONTRARIO": 0} for key in by_entity}
    seen_event_ids: set[str] = set()
    for event in events:
        if (type(event) is not dict or set(event) != {"event_id", "id_entidade", "data_evento", "tipo_evento"} or
                type(event["event_id"]) is not str or not event["event_id"] or
                type(event["id_entidade"]) is not str or
                type(event["tipo_evento"]) is not str or
                event["id_entidade"] not in counts or
                event["tipo_evento"] not in {"POSITIVO", "CONTRARIO"} or
                type(event["data_evento"]) is not str):
            raise LabError("INVALID_EVENT")
        if event["event_id"] in seen_event_ids:
            raise LabError("DUPLICATE_EVENT_ID")
        seen_event_ids.add(event["event_id"])
        try:
            observed_date = date.fromisoformat(event["data_evento"])
        except ValueError:
            raise LabError("INVALID_EVENT_DATE") from None
        if not (date(2026, 9, 1) <= observed_date <= date(2026, 9, 30)):
            raise LabError("EVENT_OUTSIDE_LAB_WINDOW")
        counts[event["id_entidade"]][event["tipo_evento"]] += 1
    individual = []
    for entity_id, row in sorted(by_entity.items()):
        positive, contrary = counts[entity_id]["POSITIVO"], counts[entity_id]["CONTRARIO"]
        complete = row["cobertura_completa"]
        if contrary:
            classification, reason = "FALSE", "CONTRA_EVIDENCIA_EXPLICITA"
            score = (round(100 * weights["sinal_positivo"] * min(positive / minimum, 1))
                     if complete else None)
        elif not complete:
            classification, reason, score = "INDETERMINADO", "COBERTURA_INCOMPLETA", None
        elif positive >= minimum:
            classification, reason = "TRUE", "EVIDENCIA_SUFICIENTE"
            score = round(100 * (weights["sinal_positivo"] * 1 + weights["sem_contrario"] * 1))
        elif positive:
            classification, reason = "INDETERMINADO", "EVIDENCIA_INSUFICIENTE"
            score = round(100 * (weights["sinal_positivo"] * positive / minimum
                                 + weights["sem_contrario"] * 1))
        else:
            classification, reason, score = "INDETERMINADO", "AUSENCIA_NAO_E_FALSE", None
        individual.append({
            "id_entidade": entity_id, "classificacao": classification,
            "score_heuristico_0_100": score, "motivo": reason,
            "eventos_positivos": positive, "eventos_contrarios": contrary,
            "cobertura_completa": complete,
        })
    class_counts = {label: sum(item["classificacao"] == label for item in individual)
                    for label in ("TRUE", "FALSE", "INDETERMINADO")}
    scores = [item["score_heuristico_0_100"] for item in individual
              if item["score_heuristico_0_100"] is not None]
    aggregate = {
        "populacao": len(individual), "contagens": class_counts,
        "scores_emitidos": len(scores),
        "score_min": min(scores) if scores else None,
        "score_max": max(scores) if scores else None,
        "score_media": sum(scores) / len(scores) if scores else None,
    }
    if sum(class_counts.values()) != aggregate["populacao"]:
        raise LabError("RECONCILIATION_FAILED")
    return individual, aggregate


def run_greenfield_lab() -> dict[str, Any]:
    """Pedido → MM04 → estudo MM01/MM02 → MM06 → scoring sintético E0."""
    fixture = _metadata_fixture()
    brief = mm04.KnownObjective(
        "atividade-recorrente-lab", "Atividade recorrente sintética",
        "atividade recorrente recente em população fictícia",
        "demonstrar descoberta, classificação e incerteza com dados sintéticos",
        "sinais POSITIVO recorrentes na janela, sujeitos a CONTRARIO explícito",
        "pedido_laboratorio_mm09", "2026-09-29T00:00:00Z",
        entity_type="entidade sintética", logical_key="id_entidade",
        grain="uma classificação por entidade e janela sintética",
        eligible_population="seis entidades sintéticas da fixture do piloto",
        reference_time="janela sintética fixa de setembro de 2026",
        intended_uses=("estudo sintético de recorrência e incerteza",),
        prohibited_uses=("decisão real ou automatizada",),
    )
    args = (
        fixture, "catalogo_sintetico", ["crm_sintetico"],
        [("crm_sintetico", "apoio_sintetico"),
         ("crm_sintetico", "eventos_sinteticos")], brief,
    )
    idea = mm04.known_objective(*args)
    flow = mm04.known_objective(*args, previous_spec=idea["spec"],
                                advance_to_discovery=True)
    schema = mm01.load_schema(mm04.SCHEMA)
    spec = _study_spec(flow["spec"], schema)
    digest = mm02.calculate_spec_fingerprint(spec, schema)
    if digest.sha256 != LAB_PROFILE_FINGERPRINT:
        raise LabError("LAB_PROFILE_MISMATCH")
    artifacts = mm06.render_artifacts(spec, schema)
    if artifacts.spec_fingerprint != digest.sha256:
        raise LabError("ARTIFACT_FINGERPRINT_MISMATCH")
    population, events = _synthetic_rows()
    individual, aggregate = evaluate_synthetic_population(spec, population, events)
    return {
        "environment": "E0_SYNTHETIC_IN_MEMORY", "source_kind": "SYNTHETIC_FIXTURE",
        "mm04_mode": flow["mode"], "metadata_coverage": flow["metadata"]["coverage"],
        "metadata_catalog_complete": flow["metadata"]["catalog_complete"],
        "spec_history": {"IDEIA": idea["spec"],
                         "EM_DESCOBERTA": flow["spec"]},
        "spec": spec, "spec_fingerprint": digest.sha256,
        "fingerprint_algorithm": digest.algorithm,
        "artifacts": {"notebook_source": artifacts.notebook_source,
                      "readme_markdown": artifacts.readme_markdown},
        "scoring": {"status": "EXECUTED_E0_SYNTHETIC", "scorer_version": LAB_SCORER_VERSION,
                    "individual": individual, "aggregate": aggregate,
                    "score_semantics": "HEURISTICA_FORCA_EVIDENCIA_NAO_PROBABILIDADE"},
        "tracking": {run_type: {"status": "NOT_RUN", "run_id": None}
                     for run_type in mm06.RUN_TYPES},
        "governance_handoff": {"status": "NOT_READY_VALIDATION_PENDING",
                               "publication_authority": "GOVERNANCA_EXTERNA",
                               "publication_executed": False},
    }
