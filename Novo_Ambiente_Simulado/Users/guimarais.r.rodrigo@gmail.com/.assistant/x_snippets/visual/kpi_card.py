
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
    # Backslash fora da expressão da f-string: PEP 701 só vale em Python >= 3.12
    # e o runtime Databricks pode ser anterior.
    pipe_escaped = {str(label).replace("|", "\\|"): str(value).replace("|", "\\|") for label, value in metricas.items()}
    parts = [f"**{value}** {label}" for label, value in pipe_escaped.items()]
    return "> " + " | ".join(parts)
