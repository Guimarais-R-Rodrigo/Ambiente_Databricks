"""Handoff MM10 de laboratório: PREPARAR_PUBLICACAO sem submeter/publicar."""
from __future__ import annotations

import copy
import math
from typing import Any

import micromodelo_mm01_contract as mm01
import micromodelo_mm02_fingerprint as mm02


class HandoffError(ValueError):
    """Entrada estruturalmente inconsistente; não ecoa dados."""


def prepare_handoff(spec: dict[str, Any], schema: dict[str, Any],
                    aggregate: dict[str, Any] | None = None) -> dict[str, Any]:
    """Gera somente rascunho estruturado, com autoridades pendentes explícitas."""
    if not isinstance(spec, dict) or mm01.validate_spec(spec, schema):
        raise HandoffError("INVALID_MM01_SPEC")
    digest = mm02.calculate_spec_fingerprint(spec, schema)
    observed = None
    if aggregate is not None:
        if not isinstance(aggregate, dict) or set(aggregate) != {
            "populacao", "contagens", "scores_emitidos", "score_min", "score_max", "score_media"
        }:
            raise HandoffError("INVALID_AGGREGATE")
        counts = aggregate["contagens"]
        if not isinstance(counts, dict) or set(counts) != {
            "TRUE", "FALSE", "INDETERMINADO"
        } or any(type(value) is not int or value < 0 for value in counts.values()):
            raise HandoffError("INVALID_COUNTS")
        if type(aggregate["populacao"]) is not int or \
                sum(counts.values()) != aggregate["populacao"]:
            raise HandoffError("UNRECONCILED_COUNTS")
        score_count = aggregate["scores_emitidos"]
        if type(score_count) is not int or not 0 <= score_count <= aggregate["populacao"]:
            raise HandoffError("INVALID_SCORE_COUNT")
        stats = [aggregate[key] for key in ("score_min", "score_media", "score_max")]
        if score_count == 0:
            if any(value is not None for value in stats):
                raise HandoffError("INVALID_SCORE_STATS")
        elif any(type(value) not in (int, float) or not math.isfinite(value)
                 for value in stats) or not 0 <= stats[0] <= stats[1] <= stats[2] <= 100:
            raise HandoffError("INVALID_SCORE_STATS")
        observed = {"status": "SUPPLIED_UNVERIFIED", "population": aggregate["populacao"],
                    "counts": dict(counts), "score_count": score_count}
    sources = sorted({
        (item["catalogo_ref"], item["schema"], item["objeto"])
        for item in spec["fontes"]
    })
    return {
        "mode": "PREPARAR_PUBLICACAO",
        "status": "DRAFT_NOT_SUBMITTED",
        "environment": "E0_SYNTHETIC_LAB",
        "identity": {"name": spec["identidade"]["nome"],
                     "version": spec["identidade"]["micromodel_version"],
                     "phase": spec["identidade"]["estado"]["fase_atual"]},
        "spec_fingerprint": digest.sha256,
        "fingerprint_algorithm": digest.algorithm,
        "sources_declared": [{"catalogo_ref": c, "schema": s, "objeto": o}
                             for c, s, o in sources],
        "output_contract": copy.deepcopy(spec["saida"]),
        "aggregate": observed,
        "run_ref": None,
        "approval_status": "PENDENTE",
        "governance_authority": "GOVERNANCA_EXTERNA",
        "required_decisions": [
            "gestor_informacao", "lgpd", "populacao_e_granularidade",
            "limiares_e_indeterminado", "retencao_resultados_individuais",
            "permissoes_e_publicacao",
        ],
        "published": False,
    }
