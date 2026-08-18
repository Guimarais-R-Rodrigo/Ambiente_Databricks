
"""Badges de status e score para notebooks executivos."""

from __future__ import annotations

from html import escape

from hub_snippets.constants.colors import AZUL_CAIXA, BG_HEADER


def badge_status(texto: str, tipo: str = "ok") -> str:
    styles = {
        "ok": "background:#EAF7EC; color:#2E7D32;",
        "warn": "background:#FFF8E1; color:#B26A00;",
        "fail": "background:#FDECEC; color:#B71C1C;",
        "info": f"background:{BG_HEADER}; color:{AZUL_CAIXA};",
    }
    style = styles.get(tipo, styles["info"])
    safe_text = escape(str(texto), quote=True)
    return f'<span style="display:inline-block; {style} padding:2px 8px; border-radius:10px; font-size:11px;">{safe_text}</span>'


def badge_score(valor: float, max: float = 100) -> str:
    ratio = 0 if max == 0 else valor / max
    if ratio >= 0.8:
        return badge_status(f"Score: {valor:.0f}/{max:.0f}", "ok")
    if ratio >= 0.5:
        return badge_status(f"Score: {valor:.0f}/{max:.0f}", "warn")
    return badge_status(f"Score: {valor:.0f}/{max:.0f}", "fail")


def badge_inline(texto: str) -> str:
    return badge_status(texto, "info")
