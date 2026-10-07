"""Geração do índice visual de notebooks EDA.

Markdown permanece textual. A V04 acrescenta uma rota HTML opt-in que recebe
``ResolvedTheme`` e usa os estilos compartilhados do Sistema de Temas.
"""

from __future__ import annotations

from typing import Iterable, Optional

from hub_snippets.constants.emojis import SECOES_EDA
from hub_snippets.constants.styles import (
    STYLE_INDEX_CONTAINER,
    STYLE_INDEX_DESCRIPTION,
    STYLE_INDEX_HEADING,
    STYLE_INDEX_ITEM,
    get_styles_resolvidos,
)
from hub_snippets.visual.tema import ResolvedTheme


def _gerar_indice(etapas_ativas: Optional[Iterable[int]], markdown: bool, *, container: str, heading: str, item_style: str, description: str) -> str:
    etapas = list(etapas_ativas) if etapas_ativas is not None else list(range(9))

    if markdown:
        lines = ["## 📋 Índice da EDA", ""]
        for etapa in etapas:
            sec = SECOES_EDA[etapa]
            lines.append(f"* {sec['emoji']} Etapa {etapa} — {sec['titulo']}  ")
            lines.append(f"  {sec['descricao']}")
        return "\n".join(lines)

    items = []
    for etapa in etapas:
        sec = SECOES_EDA[etapa]
        items.append(
            f'<div style="{item_style}">'
            f'<strong>{sec["emoji"]} Etapa {etapa}</strong> — {sec["titulo"]}<br/>'
            f'<span style="{description}">{sec["descricao"]}</span>'
            f'</div>'
        )
    return (f'<div style="{container}">'
            f'<h3 style="{heading}">📋 Índice da EDA</h3>'
            + ''.join(items) + '</div>')


def gerar_indice_eda(etapas_ativas: Optional[Iterable[int]] = None, markdown: bool = False) -> str:
    """Generate a formatted EDA index in HTML or Markdown."""
    return _gerar_indice(
        etapas_ativas,
        markdown,
        container=STYLE_INDEX_CONTAINER,
        heading=STYLE_INDEX_HEADING,
        item_style=STYLE_INDEX_ITEM,
        description=STYLE_INDEX_DESCRIPTION,
    )


def gerar_indice_eda_resolvido(theme: ResolvedTheme, etapas_ativas: Optional[Iterable[int]] = None, markdown: bool = False) -> str:
    """Gera o índice com tema explícito; Markdown continua sem decoração visual."""
    styles = get_styles_resolvidos(theme)
    return _gerar_indice(
        etapas_ativas,
        markdown,
        container=styles["index.container"],
        heading=styles["index.heading"],
        item_style=styles["index.item"],
        description=styles["index.description"],
    )
