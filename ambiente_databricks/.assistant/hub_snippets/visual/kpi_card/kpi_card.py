"""Geração de KPI cards em HTML e Markdown.

O caminho legado permanece estável. A V04 acrescenta uma variante HTML opt-in
com estilo materializado a partir de ``ResolvedTheme``; Markdown continua sem
aparência de tema por ser uma representação textual.
"""

from __future__ import annotations

from html import escape
from typing import Any, Dict

from hub_snippets.constants.styles import STYLE_KPI_CARD, get_styles_resolvidos
from hub_snippets.visual.tema import ResolvedTheme


def _kpi_card_html(metricas: Dict[str, Any], style: str) -> str:
    badges = []
    for label, value in metricas.items():
        safe_label = escape(str(label), quote=True)
        safe_value = escape(str(value), quote=True)
        badges.append(f'<span style="{style}"><b>{safe_value}</b> {safe_label}</span>')
    return "".join(badges)


def kpi_card_html(metricas: Dict[str, Any]) -> str:
    """Return inline KPI badges as HTML."""
    return _kpi_card_html(metricas, STYLE_KPI_CARD)


def kpi_card_markdown(metricas: Dict[str, Any]) -> str:
    """Return KPI line as blockquote markdown."""
    # Backslash fora da expressão da f-string: PEP 701 só vale em Python >= 3.12
    # e o runtime Databricks pode ser anterior.
    pipe_escaped = {str(label).replace("|", "\\|"): str(value).replace("|", "\\|") for label, value in metricas.items()}
    parts = [f"**{value}** {label}" for label, value in pipe_escaped.items()]
    return "> " + " | ".join(parts)


def kpi_card_html_resolvido(metricas: Dict[str, Any], theme: ResolvedTheme) -> str:
    """Renderiza os mesmos valores com o estilo explícito do tema V02."""
    return _kpi_card_html(metricas, get_styles_resolvidos(theme)["card.kpi"])
