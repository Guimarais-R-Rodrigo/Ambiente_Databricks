"""
Visualização 2D com UMAP para clusters.

Uso:
    from x_snippets.ml.umap_viz import plot_umap_clusters
    fig = plot_umap_clusters(X_scaled, labels, title="Segmentação de clientes")

Autor: Rodrigo via assistente
Versão: 1.1 — Adequação visual (paleta Caixa + tema institucional)
"""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, List


SEED = 42

# Paleta institucional Caixa
PALETA_CATEGORICA = ["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E",
                     "#7B2D8B", "#00A79D", "#F15A29", "#A7A9AC"]
AZUL_CAIXA = "#005CA9"

TEMA_BASE = dict(
    template="plotly_white",
    font=dict(family="Segoe UI, Roboto, sans-serif", size=12, color="#333333"),
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
    """Calcula embedding UMAP 2D.

    Args:
        X: Dados escalados (N x features).
        n_components: Dimensões do embedding (2 ou 3).
        n_neighbors: Vizinhos para UMAP.
        min_dist: Distância mínima entre pontos.

    Returns:
        Array (N x n_components) com coordenadas UMAP.
    """
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
    """Gera scatter plot UMAP 2D colorido por cluster com tema institucional.

    Args:
        X_scaled: Dados escalados.
        labels: Array de labels de cluster.
        title: Título do gráfico.
        cluster_names: Nomes opcionais para clusters.
        point_size: Tamanho dos pontos.
        n: N amostral para rodapé.

    Returns:
        Plotly Figure.
    """
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

    # Rodapé
    n_display = n or len(X_scaled)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    footer = f"N = {n_display:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    footer += f" | {n_clusters} clusters"
    fig.add_annotation(
        text=footer, xref="paper", yref="paper",
        x=0, y=-0.15, showarrow=False,
        font=dict(size=10, color="#6C757D"), xanchor="left",
    )

    return fig
