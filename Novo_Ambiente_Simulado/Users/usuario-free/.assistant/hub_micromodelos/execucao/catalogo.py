"""Catálogo e impacto E0 derivados exclusivamente de specs MM01 sintéticas."""
from __future__ import annotations

from typing import Any

from . import especificacao as mm01
from . import assinatura as mm02


class CatalogError(ValueError):
    """Recusa entrada ambígua sem ecoar conteúdo da especificação."""


def build_catalog(specs: list[dict[str, Any]], schema: dict[str, Any]) -> list[dict[str, Any]]:
    """Indexa somente YAMLs válidos; fingerprint não é execução ou aprovação."""
    if not isinstance(specs, list):
        raise CatalogError("INVALID_SPECS")
    seen: set[tuple[str, str]] = set()
    entries: list[dict[str, Any]] = []
    for spec in specs:
        if not isinstance(spec, dict) or mm01.validate_spec(spec, schema):
            raise CatalogError("INVALID_MM01_SPEC")
        identity = spec["identidade"]
        key = (identity["nome"], identity["micromodel_version"])
        if key in seen:
            raise CatalogError("DUPLICATE_IDENTITY_VERSION")
        seen.add(key)
        digest = mm02.calculate_spec_fingerprint(spec, schema)
        sources = sorted({
            (source["catalogo_ref"], source["schema"], source["objeto"])
            for source in spec["fontes"]
        })
        entries.append({
            "nome": key[0], "version": key[1],
            "fase": identity["estado"]["fase_atual"],
            "condicao": identity["estado"]["condicao"],
            "fingerprint": digest.sha256,
            "fingerprint_algorithm": digest.algorithm,
            "fontes": [{"catalogo_ref": c, "schema": s, "objeto": o}
                       for c, s, o in sources],
            "governanca_status": spec["publicacao"]["status"],
            "execution_status": "NOT_OBSERVED",
        })
    return sorted(entries, key=lambda item: (item["nome"], item["version"]))


def impact_by_source(catalog: list[dict[str, Any]], *, catalogo_ref: str,
                     schema: str, objeto: str) -> dict[str, Any]:
    """Identifica consumidores declarados, sem afirmar linhagem de runtime."""
    if not all(isinstance(x, str) and x for x in (catalogo_ref, schema, objeto)):
        raise CatalogError("INVALID_SOURCE")
    source = {"catalogo_ref": catalogo_ref, "schema": schema, "objeto": objeto}
    affected = [{"nome": item["nome"], "version": item["version"],
                 "fingerprint": item["fingerprint"]}
                for item in catalog if source in item["fontes"]]
    return {"source": source, "declared_consumers": affected,
            "coverage": "SPECS_PROVIDED_ONLY", "runtime_lineage_verified": False}
