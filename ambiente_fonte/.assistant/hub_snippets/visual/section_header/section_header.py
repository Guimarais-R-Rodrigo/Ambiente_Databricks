"""Renderização de headers visuais para seções de notebook.

A API legada continua produzindo a aparência histórica. A V04 acrescenta uma
rota explícita que recebe ``ResolvedTheme`` e usa estilos compartilhados, sem
estado global nem alteração dos textos ou da lógica de preenchimento por etapa.
"""

from __future__ import annotations

from html import escape
from typing import Optional

from hub_snippets.constants.emojis import SECOES_EDA
from hub_snippets.constants.styles import (
    STYLE_SECTION_DESCRIPTION,
    STYLE_SECTION_HEADER,
    STYLE_SECTION_TITLE,
    get_styles_resolvidos,
)
from hub_snippets.visual.tema import ResolvedTheme


def _conteudo(etapa: Optional[int], emoji: Optional[str], titulo: Optional[str], descricao: Optional[str]) -> tuple[str, str, str]:
    if etapa is not None and etapa in SECOES_EDA:
        default = SECOES_EDA[etapa]
        emoji = emoji or default["emoji"]
        titulo = titulo or f"Etapa {etapa} — {default['titulo']}"
        descricao = descricao or default["descricao"]

    return (
        escape(str(emoji or "📌"), quote=True),
        escape(str(titulo or "Seção"), quote=True),
        escape(str(descricao or "Descrição não informada."), quote=True),
    )


def _render_header(etapa: Optional[int], emoji: Optional[str], titulo: Optional[str], descricao: Optional[str], *, container: str, title: str, description: str) -> str:
    emoji_seguro, titulo_seguro, descricao_segura = _conteudo(etapa, emoji, titulo, descricao)
    return f"""
    <div style="{container}">
        <h3 style="{title}">{emoji_seguro} {titulo_seguro}</h3>
        <p style="{description}">{descricao_segura}</p>
    </div>
    """


def section_header_html(etapa: Optional[int] = None, emoji: Optional[str] = None, titulo: Optional[str] = None, descricao: Optional[str] = None) -> str:
    """Build a standardized HTML header for notebook sections."""
    return _render_header(
        etapa,
        emoji,
        titulo,
        descricao,
        container=STYLE_SECTION_HEADER,
        title=STYLE_SECTION_TITLE,
        description=STYLE_SECTION_DESCRIPTION,
    )


def section_header_html_resolvido(theme: ResolvedTheme, etapa: Optional[int] = None, emoji: Optional[str] = None, titulo: Optional[str] = None, descricao: Optional[str] = None) -> str:
    """Renderiza o cabeçalho com tokens do tema notebook explicitamente recebido."""
    styles = get_styles_resolvidos(theme)
    return _render_header(
        etapa,
        emoji,
        titulo,
        descricao,
        container=styles["section.container"],
        title=styles["section.title"],
        description=styles["section.description"],
    )
