
"""Renderização de headers visuais para seções de notebook."""

from __future__ import annotations

from html import escape
from typing import Optional

from x_snippets.constants.colors import AZUL_CAIXA, BG_SECTION, TEXTO_SECUNDARIO
from x_snippets.constants.emojis import SECOES_EDA


def section_header_html(etapa: Optional[int] = None, emoji: Optional[str] = None, titulo: Optional[str] = None, descricao: Optional[str] = None) -> str:
    """Build a standardized HTML header for notebook sections.

    Args:
        etapa: EDA stage number. If provided, values are auto-filled from `SECOES_EDA`.
        emoji: Emoji to display. Optional when `etapa` is known.
        titulo: Section title. Optional when `etapa` is known.
        descricao: One-line section description. Optional when `etapa` is known.

    Returns:
        HTML string ready for `displayHTML()`.
    """
    if etapa is not None and etapa in SECOES_EDA:
        default = SECOES_EDA[etapa]
        emoji = emoji or default["emoji"]
        titulo = titulo or f"Etapa {etapa} — {default['titulo']}"
        descricao = descricao or default["descricao"]

    emoji = escape(str(emoji or "📌"), quote=True)
    titulo = escape(str(titulo or "Seção"), quote=True)
    descricao = escape(str(descricao or "Descrição não informada."), quote=True)

    return f"""
    <div style="background:{BG_SECTION}; border-left:4px solid {AZUL_CAIXA}; padding:12px 16px; margin:8px 0 12px 0; border-radius:4px; font-family:Segoe UI, Roboto, sans-serif;">
        <h3 style="margin:0; color:{AZUL_CAIXA}; font-size:18px;">{emoji} {titulo}</h3>
        <p style="margin:6px 0 0 0; color:{TEXTO_SECUNDARIO}; font-size:13px;">{descricao}</p>
    </div>
    """
