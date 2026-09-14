"""
Visualização 2D com UMAP para clusters.

Uso legado:
    from hub_snippets.ml.umap_viz import plot_umap_clusters
    fig = plot_umap_clusters(X_scaled, labels)

A V07 acrescenta ``plot_umap_clusters_resolvido``. A função reaproveita a rota
legada para calcular exatamente o mesmo embedding e altera somente aparência.
"""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, List

from hub_snippets.constants import colors
from hub_snippets.visual.tema import ResolvedTheme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido, get_tokens_plotly

SEED = 42
PALETA_CATEGORICA = colors.PALETA_CATEGORICA
AZUL_CAIXA = colors.AZUL_CAIXA

TEMA_BASE = dict(
    template="plotly_white",
    font=dict(family="Segoe UI, Roboto, sans-serif", size=12, color=colors.CINZA_ESCURO),
    title=dict(font=dict(size=16, color=AZUL_CAIXA), x=0.01, xanchor="left"),
    colorway=PALETA_CATEGORICA,
    height=600,
    width=900,
    margin=dict(l=60, r=30, t=70, b=60),
    legend=dict(orientation="h", yanchor="bottom", y=-0.20, xanchor="center", x=0.5),
)


def compute_umap(
    X: np.ndarray,
    n_components: int = 2,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
) -> np.ndarray:
    """Calcula embedding UMAP 2D."""
    from umap import UMAP

    reducer = UMAP(
        n_components=n_components,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        random_state=SEED,
    )
    return reducer.fit_transform(X)


def plot_umap_clusters(
    X_scaled: np.ndarray,
    labels: np.ndarray,
    title: str = "Clusters (UMAP 2D)",
    cluster_names: Optional[List[str]] = None,
    point_size: int = 3,
    n: Optional[int] = None,
) -> go.Figure:
    """Gera scatter plot UMAP 2D colorido por cluster com tema institucional legado."""
    embedding = compute_umap(X_scaled)

    import pandas as pd
    plot_df = pd.DataFrame({
        "UMAP_1": embedding[:, 0],
        "UMAP_2": embedding[:, 1],
        "Cluster": labels.astype(str),
    })

    if cluster_names:
        name_map = {str(i): name for i, name in enumerate(cluster_names)}
        plot_df["Cluster"] = plot_df["Cluster"].map(name_map)

    fig = px.scatter(
        plot_df,
        x="UMAP_1", y="UMAP_2",
        color="Cluster",
        title=title,
        opacity=0.6,
        color_discrete_sequence=PALETA_CATEGORICA,
    )
    fig.update_traces(marker=dict(size=point_size))
    fig.update_layout(**TEMA_BASE)
    fig.update_layout(title=title)

    n_display = n or len(X_scaled)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    footer = f"N = {n_display:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    footer += f" | {n_clusters} clusters"
    fig.add_annotation(
        text=footer, xref="paper", yref="paper",
        x=0, y=-0.15, showarrow=False,
        font=dict(size=10, color=colors.TEXTO_SECUNDARIO), xanchor="left",
    )
    return fig


def plot_umap_clusters_resolvido(
    X_scaled: np.ndarray,
    labels: np.ndarray,
    theme: ResolvedTheme,
    title: str = "Clusters (UMAP 2D)",
    cluster_names: Optional[List[str]] = None,
    point_size: int = 3,
    n: Optional[int] = None,
) -> go.Figure:
    """Calcula o mesmo UMAP e aplica explicitamente um tema V02 notebook/light."""
    tokens = get_tokens_plotly(theme)  # valida antes do cálculo potencialmente caro
    fig = plot_umap_clusters(X_scaled, labels, title, cluster_names, point_size, n)
    palette = list(tokens["palette.categorical"])
    for idx, trace in enumerate(fig.data):
        trace.marker.color = palette[idx % len(palette)]
    aplicar_tema_resolvido(fig, theme)
    fig.update_layout(title=title)
    if fig.layout.annotations:
        footer = fig.layout.annotations[-1]
        footer.font.color = tokens["text.secondary"]
        footer.font.size = tokens["chart.footer_px"]
    return fig
