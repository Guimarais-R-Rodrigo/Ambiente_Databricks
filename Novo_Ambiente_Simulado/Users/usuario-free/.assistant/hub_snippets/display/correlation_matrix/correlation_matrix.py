"""Heatmap de correlação com Plotly para DataFrames PySpark.

A API legada continua usando a escala ``Blues`` e o tema institucional histórico.
A V07 acrescenta uma rota opt-in que recebe ``ResolvedTheme``; cálculo, seleção
de colunas e pares fortes são compartilhados pelas duas rotas.
"""

from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

import plotly.graph_objects as go
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
from pyspark.sql import DataFrame

from hub_snippets.visual.tema import ResolvedTheme
from hub_snippets.visual.theme_plotly import aplicar_tema, aplicar_tema_resolvido, get_tokens_plotly


def _escala_divergente(theme: ResolvedTheme):
    """Mapeia a paleta divergente ao domínio simétrico [-1, 1] da correlação."""
    tokens = get_tokens_plotly(theme)
    cores = list(tokens["palette.diverging"])
    return [[i / (len(cores) - 1), cor] for i, cor in enumerate(cores)]


def _plot_correlation(
    df: DataFrame,
    cols: Optional[Iterable[str]],
    method: str,
    threshold_highlight: float,
    *,
    theme: Optional[ResolvedTheme],
):
    colorscale = "Blues" if theme is None else _escala_divergente(theme)
    selected_cols = list(cols) if cols else [
        c for c, t in df.dtypes
        if any(token in t for token in ("tinyint", "smallint", "int", "bigint", "float", "double", "decimal"))
    ]
    missing = set(selected_cols) - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if len(selected_cols) < 2:
        raise ValueError("select at least two numeric columns")
    if method not in {"pearson", "spearman"}:
        raise ValueError("method must be 'pearson' or 'spearman'")
    assembler = VectorAssembler(inputCols=selected_cols, outputCol="features")
    vector_df = assembler.transform(df.select(*selected_cols).na.drop())
    matrix = Correlation.corr(vector_df, "features", method).collect()[0][0].toArray().tolist()

    fig = go.Figure(data=go.Heatmap(z=matrix, x=selected_cols, y=selected_cols, colorscale=colorscale, zmin=-1, zmax=1))
    fig.update_layout(title="Matriz de correlação")
    if theme is None:
        aplicar_tema(fig, subtitulo=f"Método: {method}")
    else:
        aplicar_tema_resolvido(fig, theme, subtitulo=f"Método: {method}")

    strong_pairs: List[Tuple[str, str, float]] = []
    for i, c1 in enumerate(selected_cols):
        for j, c2 in enumerate(selected_cols):
            if j > i and abs(matrix[i][j]) >= threshold_highlight:
                strong_pairs.append((c1, c2, float(matrix[i][j])))
    return fig, strong_pairs


def plot_correlation(df: DataFrame, cols: Optional[Iterable[str]] = None, method: str = "pearson", threshold_highlight: float = 0.8):
    """Compute correlation matrix in Spark and return the legacy Plotly heatmap plus strong pairs."""
    return _plot_correlation(df, cols, method, threshold_highlight, theme=None)


def plot_correlation_resolvido(
    df: DataFrame,
    theme: ResolvedTheme,
    cols: Optional[Iterable[str]] = None,
    method: str = "pearson",
    threshold_highlight: float = 0.8,
):
    """Compute a mesma correlação e aplica explicitamente um tema V02 notebook/light."""
    return _plot_correlation(df, cols, method, threshold_highlight, theme=theme)


plot_correlation_matrix = plot_correlation
plot_correlation_matrix_resolvido = plot_correlation_resolvido
