"""Badges de status e score para notebooks executivos.

A API legada mantém a aparência existente. A V04 acrescenta funções opt-in
que recebem um ``ResolvedTheme`` e materializam o CSS pelo módulo compartilhado
de estilos, sem estado global nem mudança das regras de classificação.
"""

from __future__ import annotations

from html import escape

from hub_snippets.constants.styles import (
    STYLE_BADGE_FAIL,
    STYLE_BADGE_INFO,
    STYLE_BADGE_OK,
    STYLE_BADGE_WARN,
    get_styles_resolvidos,
)
from hub_snippets.visual.tema import ResolvedTheme


def _badge_html(texto: str, style: str) -> str:
    safe_text = escape(str(texto), quote=True)
    return f'<span style="{style}">{safe_text}</span>'


def badge_status(texto: str, tipo: str = "ok") -> str:
    styles = {
        "ok": STYLE_BADGE_OK,
        "warn": STYLE_BADGE_WARN,
        "fail": STYLE_BADGE_FAIL,
        "info": STYLE_BADGE_INFO,
    }
    return _badge_html(texto, styles.get(tipo, styles["info"]))


def badge_score(valor: float, max: float = 100) -> str:
    ratio = 0 if max == 0 else valor / max
    if ratio >= 0.8:
        return badge_status(f"Score: {valor:.0f}/{max:.0f}", "ok")
    if ratio >= 0.5:
        return badge_status(f"Score: {valor:.0f}/{max:.0f}", "warn")
    return badge_status(f"Score: {valor:.0f}/{max:.0f}", "fail")


def badge_inline(texto: str) -> str:
    return badge_status(texto, "info")


def badge_status_resolvido(texto: str, theme: ResolvedTheme, tipo: str = "ok") -> str:
    """Renderiza o mesmo badge com estilo vindo explicitamente do tema V02."""
    styles = get_styles_resolvidos(theme)
    key = tipo if tipo in {"ok", "warn", "fail", "info"} else "info"
    return _badge_html(texto, styles[f"badge.{key}"])


def badge_score_resolvido(valor: float, theme: ResolvedTheme, max: float = 100) -> str:
    """Mantém os cortes legados e troca somente a apresentação visual."""
    ratio = 0 if max == 0 else valor / max
    if ratio >= 0.8:
        return badge_status_resolvido(f"Score: {valor:.0f}/{max:.0f}", theme, "ok")
    if ratio >= 0.5:
        return badge_status_resolvido(f"Score: {valor:.0f}/{max:.0f}", theme, "warn")
    return badge_status_resolvido(f"Score: {valor:.0f}/{max:.0f}", theme, "fail")


def badge_inline_resolvido(texto: str, theme: ResolvedTheme) -> str:
    return badge_status_resolvido(texto, theme, "info")
