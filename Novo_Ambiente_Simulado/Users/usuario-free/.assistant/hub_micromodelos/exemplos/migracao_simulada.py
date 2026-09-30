"""Ensaio MM12 conservador com legado FICTÍCIO; não é skill roteável.

A API compara saídas em memória e nunca lê, altera ou publica objetos legados.
O marcador synthetic é declaração da fixture, não verificação da origem real.
"""
from __future__ import annotations

from typing import Any


class MigrationLabError(ValueError):
    """Entrada inválida ou fora do namespace fictício fechado."""


def _index(rows: list[dict[str, Any]]) -> dict[str, tuple[str, int | None]]:
    if not isinstance(rows, list):
        raise MigrationLabError("INVALID_ROWS")
    indexed = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "fixture_namespace", "synthetic", "id_entidade", "classificacao", "score"
        }:
            raise MigrationLabError("INVALID_ROW_SHAPE")
        if row["fixture_namespace"] != "MM12_FICTICIO" or row["synthetic"] is not True:
            raise MigrationLabError("NON_SYNTHETIC_INPUT")
        key = row["id_entidade"]
        classification = row["classificacao"]
        score = row["score"]
        if not isinstance(key, str) or not key or key in indexed:
            raise MigrationLabError("INVALID_OR_DUPLICATE_KEY")
        if type(classification) is not str or classification not in {
            "TRUE", "FALSE", "INDETERMINADO"
        }:
            raise MigrationLabError("INVALID_CLASSIFICATION")
        if score is not None and (type(score) is not int or not 0 <= score <= 100):
            raise MigrationLabError("INVALID_SCORE")
        indexed[key] = (classification, score)
    return indexed


def rehearse_equivalence(legacy_rows: list[dict[str, Any]],
                         candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Exige mesmas chaves, classificação e score antes/depois; não moderniza regra."""
    legacy = _index(legacy_rows)
    candidate = _index(candidate_rows)
    if not legacy or not candidate:
        raise MigrationLabError("EMPTY_COMPARISON")
    missing = sorted(legacy.keys() - candidate.keys())
    extra = sorted(candidate.keys() - legacy.keys())
    changed = sorted(key for key in legacy.keys() & candidate.keys()
                     if legacy[key] != candidate[key])
    equivalent = not (missing or extra or changed)
    return {
        "status": "EQUIVALENT_LAB" if equivalent else "DIVERGENT_LAB",
        "fixture_namespace": "MM12_FICTICIO",
        "compared": len(legacy.keys() & candidate.keys()),
        "missing_keys": missing,
        "extra_keys": extra,
        "changed_keys": changed,
        "corporate_v1_verified": False,
        "migration_skill_routable": False,
        "publication_authorized": False,
    }
