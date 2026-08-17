"""Geração do índice visual de notebooks EDA."""

from __future__ import annotations

from typing import Iterable, Optional

from hub_snippets.constants.emojis import SECOES_EDA


def gerar_indice_eda(etapas_ativas: Optional[Iterable[int]] = None, markdown: bool = False) -> str:
    """Generate a formatted EDA index in HTML or Markdown.

    Args:
        etapas_ativas: Which EDA stages to include. None means all (0-8).
        markdown: If True, return plain Markdown; otherwise return HTML.

    Returns:
        Formatted index string.
    """
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
            f'<div style="margin:6px 0; padding:6px 10px; background:#F8F9FA; border-radius:6px;">'
            f'<strong>{sec["emoji"]} Etapa {etapa}</strong> — {sec["titulo"]}<br/>'
            f'<span style="color:#6C757D; font-size:12px;">{sec["descricao"]}</span>'
            f'</div>'
        )
    return '<div style="font-family:Segoe UI, Roboto, sans-serif;"><h3 style="color:#005CA9; margin-bottom:10px;">📋 Índice da EDA</h3>' + ''.join(items) + '</div>'
