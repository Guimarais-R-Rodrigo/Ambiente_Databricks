"""Fluxo E0 offline MM04/MM05 sobre os contratos MM01–MM03.

Esta ferramenta de construção não é uma skill ou helper de produto. Ao transportar
para o Hub, empacotar explicitamente o contrato, template e dependências; não
importar ``tools`` implicitamente do checkout local.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import micromodelo_mm01_contract as mm01
import micromodelo_mm02_fingerprint as mm02
import micromodelo_mm03_metadata as mm03

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs/sprints/micromodelos/MM01/micromodelo.template.yaml"
SCHEMA = ROOT / "docs/sprints/micromodelos/MM01/micromodelo.schema.json"
_NAME = re.compile(r"[a-z][a-z0-9-]{2,63}\Z")


class FlowError(ValueError):
    """Código estável, sem eco de metadata ou paths de entrada."""


@dataclass(frozen=True)
class KnownObjective:
    name: str
    title: str
    characteristic: str
    objective: str
    operational_definition: str
    request_ref: str
    created_at_utc: str
    entity_type: str | None = None
    logical_key: str | None = None
    grain: str | None = None
    eligible_population: str | None = None
    reference_time: str | None = None
    intended_uses: tuple[str, ...] = ()
    prohibited_uses: tuple[str, ...] = ()


@dataclass(frozen=True)
class OpportunityProposal:
    """Hipótese fornecida pelo solicitante; metadata apenas sustenta fonte/sinal."""
    characteristic: str
    decision: str
    population: str
    grain: str
    decision_time: str
    horizon: str
    candidates: tuple[tuple[str, str], ...]


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise FlowError(code)


def _brief(value: KnownObjective) -> None:
    _require(type(value) is KnownObjective, "INVALID_BRIEF")
    _require(type(value.name) is str and _NAME.fullmatch(value.name) is not None,
             "INVALID_MODEL_NAME")
    for field in (value.title, value.characteristic, value.objective,
                  value.operational_definition, value.request_ref,
                  value.created_at_utc, value.entity_type, value.logical_key,
                  value.grain, value.eligible_population, value.reference_time):
        _require(field is None or (type(field) is str and
                 len(field.encode("utf-8")) <= 2000), "INVALID_BRIEF_FIELD")
    for items in (value.intended_uses, value.prohibited_uses):
        _require(type(items) in (tuple, list) and len(items) <= 20,
                 "INVALID_BRIEF_FIELD")
        for item in items:
            _require(type(item) is str and len(item.encode("utf-8")) <= 2000,
                     "INVALID_BRIEF_FIELD")


def _semantic_key(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _tokens(value: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", value).casefold()
    plain = "".join(c for c in normalized if not unicodedata.combining(c))
    return {token for token in re.findall(r"[a-z0-9]+", plain) if len(token) >= 4}


def _signal_text(item: dict[str, Any]) -> str:
    values = [item["name"]]
    description = item["description"]
    if description["state"] == "OBSERVED":
        values.append(description["text"])
    for tag in item["tags"] or []:
        values.extend(v["text"] for v in (tag["key"], tag["value"])
                      if v["state"] == "OBSERVED")
    return " ".join(values)


def _proposal(value: OpportunityProposal) -> tuple[str, ...]:
    _require(type(value) is OpportunityProposal, "INVALID_PROPOSAL")
    fields = (value.characteristic, value.decision, value.population, value.grain,
              value.decision_time, value.horizon)
    _require(all(type(x) is str and 3 <= len(x.strip()) <= 2000 for x in fields),
             "INVALID_PROPOSAL_FIELD")
    _require(type(value.candidates) in (tuple, list) and 1 <= len(value.candidates) <= 20,
             "INVALID_PROPOSAL_CANDIDATES")
    for pair in value.candidates:
        _require(type(pair) in (tuple, list) and len(pair) == 2,
                 "INVALID_PROPOSAL_CANDIDATES")
        for identifier in pair:
            mm03._identifier(identifier)
    return tuple(_semantic_key(x) for x in fields)


def _observed_objects(discovery: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    observed = {}
    for schema, collection in discovery["objects"].items():
        for item in collection["items"]:
            observed[(schema, item["name"])] = item
    return observed


def _collector(fixture: dict[str, Any], catalog: str, limits: mm03.Limits | None
               ) -> mm03.MetadataCollector:
    return mm03.MetadataCollector(mm03.FixtureProvider(fixture),
                                  mm03.Binding(catalog), limits)


def discover_opportunities(fixture: dict[str, Any], catalog: str,
                           schemas: list[str], *, limits: mm03.Limits | None = None,
                           proposals: list[OpportunityProposal] | None = None
                           ) -> dict[str, Any]:
    """Shortlist de hipóteses explícitas com sinal lexical em metadata observada.

    Sem hipóteses de negócio fornecidas, devolve objetos para triagem, não uma
    shortlist fictícia de oportunidades. Textos de metadata só servem ao teste
    lexical; nunca instruem operações, autorizações ou conteúdo de proposta.
    """
    _require(proposals is None or (type(proposals) is list and len(proposals) <= 100),
             "INVALID_PROPOSAL_COLLECTION")
    grouped: dict[tuple[str, ...], dict[str, Any]] = {}
    for proposal in proposals or []:
        key = _proposal(proposal)
        if key not in grouped:
            grouped[key] = {"proposal": proposal, "sources": [], "merged": 0}
        else:
            grouped[key]["merged"] += 1
        for pair in proposal.candidates:
            candidate = tuple(pair)
            if candidate not in grouped[key]["sources"]:
                grouped[key]["sources"].append(candidate)
    collector = _collector(fixture, catalog, limits)
    discovery = collector.discover(schemas)
    objects = _observed_objects(discovery)
    cap = collector.limits.max_candidates
    selected: list[dict[str, Any]] = []
    rejected = []
    source_union: list[tuple[str, str]] = []
    for entry in grouped.values():
        proposal = entry["proposal"]
        sources = entry["sources"]
        unknown = [pair for pair in sources if pair not in objects]
        if unknown:
            rejected.append({"characteristic": proposal.characteristic,
                             "reason": "SOURCE_NOT_OBSERVED_IN_SCOPE"})
            continue
        terms = _tokens(proposal.characteristic)
        matches = sorted(set().union(*(_tokens(_signal_text(objects[pair])) for pair in sources))
                         & terms)
        if not matches:
            rejected.append({"characteristic": proposal.characteristic,
                             "reason": "NO_SEMANTIC_METADATA_SIGNAL"})
            continue
        new_sources = [pair for pair in sources if pair not in source_union]
        if len(selected) >= cap or len(source_union) + len(new_sources) > cap:
            rejected.append({"characteristic": proposal.characteristic,
                             "reason": "SHORTLIST_LIMIT"})
            continue
        source_union.extend(new_sources)
        selected.append({"proposal": proposal, "sources": sources,
                         "matches": matches, "merged": entry["merged"]})
    details = collector.details(source_union) if source_union else {}
    envelope = collector.envelope(discovery, details)
    shortlist = []
    for entry in selected:
        proposal = entry["proposal"]
        shortlist.append({
            "hypothesis": {"status": "PROPOSTO", "characteristic": proposal.characteristic,
                           "decision": proposal.decision, "population": proposal.population,
                           "grain": proposal.grain, "decision_time": proposal.decision_time,
                           "horizon": proposal.horizon, "requires_human_review": True},
            "observed": {"status": "DESCOBERTO", "basis": "MM03_METADATA_ONLY",
                         "snapshot_id": envelope["snapshot_id"],
                         "sources": [{"schema": schema, "object": obj,
                                      "object_type": objects[(schema, obj)]["object_type"],
                                      "detail_status": {k: v["status"] for k, v in
                                                        details[f"{schema}.{obj}"].items()}}
                                     for schema, obj in entry["sources"]],
                         "lexical_signal_terms": entry["matches"]},
            "variants_merged": entry["merged"],
            "uncertainty": ["sem leitura de registros", "sem regra de classificação aprovada",
                            "sinal lexical de metadata não prova semântica nem utilidade"],
        })
    return {"mode": "DESCOBRIR_OPORTUNIDADES", "metadata": envelope,
            "shortlist": shortlist, "priority_basis": "ORDEM_DAS_HIPOTESES_FORNECIDAS",
            "rejected": rejected, "source_objects_for_triage":
            [{"schema": schema, "object": obj} for schema, obj in sorted(objects)]
            if proposals is None else [],
            "shortlist_truncated": any(x["reason"] == "SHORTLIST_LIMIT" for x in rejected),
            "unreviewed_objects": len(objects) if proposals is None else
            len(set(objects) - set(source_union))}


def known_objective(fixture: dict[str, Any], catalog: str, schemas: list[str],
                    candidates: list[tuple[str, str]], brief: KnownObjective, *,
                    limits: mm03.Limits | None = None,
                    previous_spec: dict[str, Any] | None = None,
                    advance_to_discovery: bool = False) -> dict[str, Any]:
    """Produz uma especificação MM01 válida em IDEIA a partir de pedido explícito.

    Candidatas devem ter sido observadas pela MM03. A metadata livre só viaja no
    envelope MM03; não define objetivo, regras, status de aprovação ou permissões.
    """
    _brief(brief)
    _require(type(advance_to_discovery) is bool, "INVALID_PHASE_OPTION")
    _require(previous_spec is not None or not advance_to_discovery,
             "PREVIOUS_SPEC_REQUIRED")
    schema_contract = mm01.load_schema(SCHEMA)
    if previous_spec is not None:
        _require(type(previous_spec) is dict and
                 not mm01.validate_spec(previous_spec, schema_contract),
                 "INVALID_PREVIOUS_SPEC")
        _require(previous_spec["identidade"]["nome"] == brief.name,
                 "PREVIOUS_IDENTITY_MISMATCH")
        _require(previous_spec["identidade"]["estado"]["fase_atual"] in
                 {"IDEIA", "EM_DESCOBERTA"}, "PHASE_OUT_OF_SCOPE")
    collector = _collector(fixture, catalog, limits)
    discovery = collector.discover(schemas)
    details = collector.details(candidates)
    envelope = collector.envelope(discovery, details)
    objects = _observed_objects(discovery)
    spec = copy.deepcopy(previous_spec) if previous_spec is not None else mm01.load_document(TEMPLATE)
    spec["identidade"]["titulo"] = brief.title
    spec["negocio"]["caracteristica"] = brief.characteristic
    spec["negocio"]["objetivo"] = brief.objective
    spec["negocio"]["definicao_operacional"] = brief.operational_definition
    if previous_spec is None:
        spec["identidade"]["nome"] = brief.name
        spec["proveniencia"]["criado_em_utc"] = brief.created_at_utc
        spec["proveniencia"]["gerado_por"] = "MM04 E0 synthetic flow"
        spec["proveniencia"]["pedido_original_ref"] = brief.request_ref
        spec["fontes"] = []
    entity = spec["entidade"]
    for key, value, pending in (
        ("tipo", brief.entity_type, "PENDENTE: tipo de entidade a confirmar"),
        ("chave_logica", brief.logical_key, "PENDENTE: chave lógica a confirmar"),
        ("granularidade", brief.grain, "PENDENTE: grão a confirmar"),
        ("populacao_elegivel", brief.eligible_population, "PENDENTE: população elegível a confirmar"),
        ("referencia_temporal", brief.reference_time, "PENDENTE: referência temporal a confirmar"),
    ):
        if value is not None:
            entity[key] = value
        elif previous_spec is None:
            entity[key] = pending
    if brief.intended_uses:
        spec["negocio"]["uso_pretendido"] = list(brief.intended_uses)
    elif previous_spec is None:
        spec["negocio"]["uso_pretendido"] = ["PENDENTE: uso pretendido a confirmar"]
    if brief.prohibited_uses:
        spec["negocio"]["nao_usar_para"] = list(brief.prohibited_uses)
    elif previous_spec is None:
        spec["negocio"]["nao_usar_para"] = ["Uso não aprovado ou não declarado"]
    if advance_to_discovery:
        state = spec["identidade"]["estado"]
        _require(state["fase_atual"] == "IDEIA", "INVALID_PHASE_ADVANCE")
        state["fase_anterior"], state["fase_atual"] = "IDEIA", "EM_DESCOBERTA"
    existing = {(source["schema"], source["objeto"]) for source in spec["fontes"]}
    next_id = 1
    for schema, obj in sorted(candidates):
        if (schema, obj) in existing:
            continue
        while any(source["id"] == f"fonte_{next_id:03d}" for source in spec["fontes"]):
            next_id += 1
        columns = details[f"{schema}.{obj}"]["columns"]
        spec["fontes"].append({
            "id": f"fonte_{next_id:03d}", "catalogo_ref": mm03.CATALOG_REF,
            "schema": schema, "objeto": obj,
            "tipo_objeto": objects[(schema, obj)]["object_type"],
            "campos": [item["name"] for item in columns["items"]]
                      if columns["status"] == "OBSERVED" else [],
            "papel": "APOIO",
            "proveniencia": {"status": "DESCOBERTO", "origem": "MM03 metadata sintética",
                            "referencia": envelope["snapshot_id"],
                            "observado_em_utc": None, "aprovacao": None, "medicao": None},
        })
        next_id += 1
    issues = mm01.validate_spec(spec, schema_contract, previous_spec=previous_spec)
    _require(not issues, "INVALID_MM01_SPEC")
    digest = mm02.calculate_spec_fingerprint(spec, schema_contract)
    return {"mode": "OBJETIVO_CONHECIDO", "metadata": envelope, "spec": spec,
            "fingerprint": {"algorithm": digest.algorithm,
                            "algorithm_version": digest.algorithm_version,
                            "sha256": digest.sha256},
            "uncertainty": ["fontes são candidatas, sem validação de registros",
                            "regras, score e uso dependem de estudo e aprovação humana",
                            "cobertura restrita ao escopo observado"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MM04/MM05 E0 offline sobre fixture sintética")
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", action="append", dest="schemas", required=True)
    parser.add_argument("--mode", choices=("known", "discover"), required=True)
    parser.add_argument("--candidate", action="append", default=[])
    parser.add_argument("--brief", help="JSON com campos de KnownObjective; só para known")
    parser.add_argument("--proposals", help="JSON de hipóteses explícitas; só para discover")
    parser.add_argument("--previous-spec", help="YAML/JSON MM01 anterior; só para known")
    parser.add_argument("--advance-to-discovery", action="store_true")
    args = parser.parse_args(argv)
    try:
        fixture, _ = mm03.load_fixture(args.fixture)
        if args.mode == "discover":
            _require(not args.brief and not args.candidate and not args.previous_spec
                     and not args.advance_to_discovery, "INVALID_MODE_ARGUMENTS")
            proposals = None
            if args.proposals:
                raw = Path(args.proposals).read_bytes()
                _require(len(raw) <= 65_536, "PROPOSALS_TOO_LARGE")
                payload = json.loads(raw.decode("utf-8"))
                _require(type(payload) is list, "INVALID_PROPOSAL_COLLECTION")
                expected = set(OpportunityProposal.__dataclass_fields__)
                _require(all(type(item) is dict and set(item) == expected for item in payload),
                         "INVALID_PROPOSAL_SHAPE")
                proposals = [OpportunityProposal(**item) for item in payload]
            report = discover_opportunities(fixture, args.catalog, args.schemas,
                                            proposals=proposals)
        else:
            _require(bool(args.brief) and not args.proposals, "BRIEF_REQUIRED")
            raw = Path(args.brief).read_bytes()
            _require(len(raw) <= 16_384, "BRIEF_TOO_LARGE")
            payload = json.loads(raw.decode("utf-8"))
            required = {"name", "title", "characteristic", "objective",
                        "operational_definition", "request_ref", "created_at_utc"}
            allowed = set(KnownObjective.__dataclass_fields__)
            _require(type(payload) is dict and required <= set(payload) <= allowed,
                     "INVALID_BRIEF_SHAPE")
            candidates = [tuple(x.split(".")) for x in args.candidate]
            previous_spec = mm01.load_document(args.previous_spec) if args.previous_spec else None
            report = known_objective(fixture, args.catalog, args.schemas, candidates,
                                     KnownObjective(**payload), previous_spec=previous_spec,
                                     advance_to_discovery=args.advance_to_discovery)
        print(json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
        return 0
    except (FlowError, mm03.MetadataError, ValueError, UnicodeError, OSError):
        print("REPROVADO_MM04_FLOW", file=sys.stderr)
        return 1
    except Exception:
        print("ERRO_MM04_FLOW", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
