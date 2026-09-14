"""Contrato V09 do Sistema de Temas para o kit de transição.

Este módulo é deliberadamente offline: valida inventários e manifesta o conjunto
mínimo que precisa viajar no pacote. Não publica, ativa ou promove temas.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping

THEME_CONTRACT_VERSION = 1
THEME_REQUIRED_PATHS = (
    ".assistant/hub_padroes/identidade_visual/theme.schema.json",
    ".assistant/hub_padroes/identidade_visual/TOKENS.md",
    ".assistant/hub_padroes/identidade_visual/assets.json",
    ".assistant/hub_padroes/identidade_visual/README.md",
    ".assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md",
    ".assistant/hub_snippets/visual/tema/__init__.py",
    ".assistant/hub_snippets/visual/tema/tema.py",
    ".assistant/hub_snippets/visual/theme_plotly/__init__.py",
    ".assistant/hub_snippets/visual/theme_plotly/theme_plotly.py",
)


def _paths(entries: Iterable[Mapping[str, object]]) -> set[str]:
    result: set[str] = set()
    for entry in entries:
        path = entry.get("path")
        if isinstance(path, str):
            result.add(path)
    return result


def validate_theme_inventory(entries: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Falha se o bundle perder qualquer peça mínima do contrato temático V09."""
    present = _paths(entries)
    missing = [path for path in THEME_REQUIRED_PATHS if path not in present]
    if missing:
        raise ValueError("Sistema de Temas incompleto no bundle: " + ", ".join(missing))
    return {
        "contract_version": THEME_CONTRACT_VERSION,
        "required_paths": list(THEME_REQUIRED_PATHS),
        "transport": "required_and_hashed",
        "activation": "manual_opt_in",
        "publication": "not_performed",
    }


def validate_theme_contract(manifest: Mapping[str, object]) -> dict[str, object]:
    """Confere que manifesto e inventário contam a mesma história sobre temas."""
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ValueError("Manifesto sem lista de arquivos para validar temas.")
    expected = validate_theme_inventory(files)
    contract = manifest.get("theme_contract")
    if contract != expected:
        raise ValueError("Contrato de temas ausente ou divergente no manifesto.")
    return expected
