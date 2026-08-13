
"""Geração de KPI cards em HTML e Markdown."""

from __future__ import annotations

from html import escape
from typing import Dict, Any


def kpi_card_html(metricas: Dict[str, Any]) -> str:
    """Return inline KPI badges as HTML."""
    badges = []
    for label, value in metricas.items():
        safe_label = escape(str(label), quote=True)
        safe_value = escape(str(value), quote=True)
        badges.append(
            f'<span style="display:inline-block; background:#E8F4FD; padding:4px 10px; border-radius:12px; font-size:12px; margin-right:8px; color:#1A1A1A; font-family:Segoe UI, Roboto, sans-serif;"><b>{safe_value}</b> {safe_label}</span>'
        )
    return "".join(badges)


def kpi_card_markdown(metricas: Dict[str, Any]) -> str:
    """Return KPI line as blockquote markdown."""
    parts = [f"**{str(value).replace('|', '\\|')}** {str(label).replace('|', '\\|')}" for label, value in metricas.items()]
    return "> " + " | ".join(parts)
