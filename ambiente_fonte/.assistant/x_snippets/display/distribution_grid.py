
"""Grid de distribuições numéricas com Plotly subplots."""

from __future__ import annotations

from math import ceil
from typing import Iterable, Optional

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pyspark.sql import DataFrame

from x_snippets.spark.smart_sample import smart_sample
from x_snippets.visual.theme_plotly import aplicar_tema


def plot_distributions(df: DataFrame, cols: Optional[Iterable[str]] = None, ncols: int = 3, sample_n: int = 10000):
    """Return a Plotly subplot grid with histograms for numeric columns."""
    if ncols <= 0 or sample_n <= 0:
        raise ValueError("ncols and sample_n must be positive")
    selected_cols = list(cols) if cols else [
        c for c, t in df.dtypes
        if any(token in t for token in ("tinyint", "smallint", "int", "bigint", "float", "double", "decimal"))
    ]
    missing = set(selected_cols) - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if not selected_cols:
        raise ValueError("no numeric columns selected")
    sampled = smart_sample(df.select(*selected_cols), n=sample_n)
    pdf = sampled.toPandas()

    nrows = ceil(len(selected_cols) / ncols)
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=selected_cols)

    for idx, col_name in enumerate(selected_cols, start=1):
        row = ceil(idx / ncols)
        col = ((idx - 1) % ncols) + 1
        fig.add_trace(go.Histogram(x=pdf[col_name], name=col_name, showlegend=False), row=row, col=col)

    fig.update_layout(title="Distribuições numéricas")
    fig = aplicar_tema(fig, subtitulo="Grade de histogramas", n=len(pdf))
    return fig


plot_distribution_grid = plot_distributions
