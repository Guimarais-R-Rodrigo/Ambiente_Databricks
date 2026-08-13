
"""Tema Plotly institucional para notebooks analíticos.

Example:
    registrar_template_plotly()
    fig = px.bar(df_pd, x="segmento", y="clientes", title="Clientes por segmento")
    fig = aplicar_tema(fig, subtitulo="Distribuição consolidada", fonte="catalog.schema.table", n=12500)
    fig.show()
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import plotly.io as pio
import plotly.graph_objects as go

from x_snippets.constants.colors import PALETA_CATEGORICA, TEXTO_SECUNDARIO, AZUL_CAIXA


def get_tema_eda() -> Dict[str, Any]:
    """Return the default Plotly theme configuration for the ecosystem."""
    return {
        "template": "plotly_white",
        "font": {"family": "Segoe UI, Roboto, sans-serif", "size": 12, "color": "#333333"},
        "title": {"font": {"size": 16, "color": AZUL_CAIXA}, "x": 0.01, "xanchor": "left"},
        "colorway": PALETA_CATEGORICA,
        "height": 450,
        "width": 900,
        "margin": {"l": 60, "r": 30, "t": 70, "b": 60},
        "legend": {"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5},
    }


def aplicar_tema(fig: go.Figure, subtitulo: Optional[str] = None, fonte: Optional[str] = None, n: Optional[int] = None) -> go.Figure:
    """Apply the institutional theme and optional footer annotations.

    Args:
        fig: Plotly figure to format.
        subtitulo: Optional subtitle rendered as footer annotation.
        fonte: Optional source label.
        n: Optional sample size label.

    Returns:
        The formatted Plotly figure.
    """
    fig.update_layout(**get_tema_eda())
    footer_parts = []
    if n is not None:
        footer_parts.append(f"N = {n:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
    if fonte:
        footer_parts.append(f"Fonte: {fonte}")
    if subtitulo:
        footer_parts.append(subtitulo)

    if footer_parts:
        fig.add_annotation(
            text=" | ".join(footer_parts),
            xref="paper",
            yref="paper",
            x=0,
            y=-0.18,
            showarrow=False,
            font={"size": 10, "color": TEXTO_SECUNDARIO},
            xanchor="left",
        )
    return fig


def registrar_template_plotly() -> None:
    """Register the 'caixa' Plotly template globally in the current session."""
    pio.templates["caixa"] = go.layout.Template(layout=get_tema_eda())
    pio.templates.default = "caixa"
