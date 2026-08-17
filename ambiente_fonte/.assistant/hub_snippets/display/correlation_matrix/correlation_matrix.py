
"""Heatmap de correlação com Plotly para DataFrames PySpark."""

from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

import plotly.graph_objects as go
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
from pyspark.sql import DataFrame

from hub_snippets.visual.theme_plotly import aplicar_tema


def plot_correlation(df: DataFrame, cols: Optional[Iterable[str]] = None, method: str = "pearson", threshold_highlight: float = 0.8):
    """Compute correlation matrix in Spark and return a Plotly heatmap plus strong pairs."""
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

    fig = go.Figure(data=go.Heatmap(z=matrix, x=selected_cols, y=selected_cols, colorscale="Blues", zmin=-1, zmax=1))
    fig.update_layout(title="Matriz de correlação")
    fig = aplicar_tema(fig, subtitulo=f"Método: {method}")

    strong_pairs: List[Tuple[str, str, float]] = []
    for i, c1 in enumerate(selected_cols):
        for j, c2 in enumerate(selected_cols):
            if j > i and abs(matrix[i][j]) >= threshold_highlight:
                strong_pairs.append((c1, c2, float(matrix[i][j])))
    return fig, strong_pairs


plot_correlation_matrix = plot_correlation
