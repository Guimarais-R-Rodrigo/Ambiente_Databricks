"""
Análise de safras (vintage/cohort): curvas de maturação, heatmap e métricas.

Uso:
    from hub_snippets.ml.vintage_analysis import build_vintage_table, plot_vintage_curves, plot_vintage_heatmap

A V07 acrescenta rotas ``*_resolvido`` que reutilizam as figuras legadas e
alteram somente aparência. Agregação, maturidade, denominadores e comparação de
safras permanecem em uma única implementação.
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Tuple

from hub_snippets.constants import colors
from hub_snippets.visual.tema import ResolvedTheme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido, get_tokens_plotly

PALETA_CATEGORICA = colors.PALETA_CATEGORICA
AZUL_CAIXA = colors.AZUL_CAIXA
PALETA_SEQUENCIAL = colors.PALETA_SEQUENCIAL
TEMA_BASE = dict(
    template="plotly_white",
    font=dict(family="Segoe UI, Roboto, sans-serif", size=12, color=colors.CINZA_ESCURO),
    title=dict(font=dict(size=16, color=AZUL_CAIXA), x=0.01, xanchor="left"),
    height=600, width=1000,
    margin=dict(l=60, r=30, t=70, b=60),
    legend=dict(orientation="h", yanchor="bottom", y=-0.20, xanchor="center", x=0.5),
)


def build_vintage_table(
    df: pd.DataFrame,
    contract_id: str,
    dt_originacao: str,
    dt_referencia: str,
    target: str,
    safra_grain: str = "month",
    mob_col: Optional[str] = None,
    target_is_cumulative: bool = False,
) -> pd.DataFrame:
    """Constrói tabela de safras agregada."""
    required = {contract_id, dt_originacao, dt_referencia, target}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if safra_grain not in {"month", "quarter"}:
        raise ValueError("safra_grain must be 'month' or 'quarter'")
    df = df.copy()
    df[dt_originacao] = pd.to_datetime(df[dt_originacao])
    df[dt_referencia] = pd.to_datetime(df[dt_referencia])

    if mob_col is None:
        df["mob"] = (
            (df[dt_referencia].dt.year - df[dt_originacao].dt.year) * 12
            + (df[dt_referencia].dt.month - df[dt_originacao].dt.month)
        )
    else:
        df["mob"] = df[mob_col]

    if safra_grain == "month":
        df["safra"] = df[dt_originacao].dt.to_period("M").astype(str)
    elif safra_grain == "quarter":
        df["safra"] = df[dt_originacao].dt.to_period("Q").astype(str)

    df = df[df["mob"].notna() & (df["mob"] >= 0)].copy()
    if df.empty:
        raise ValueError("no valid observations remain after filtering non-negative MOB")
    if not np.isfinite(pd.to_numeric(df["mob"], errors="coerce")).all():
        raise ValueError("mob must contain finite numeric values")
    if not np.equal(df["mob"], np.floor(df["mob"])).all():
        raise ValueError("mob must contain integer values")
    df["mob"] = df["mob"].astype(int)
    df[target] = pd.to_numeric(df[target], errors="raise")
    if df[target].isna().any():
        raise ValueError("target cannot contain null values without an explicit policy")
    if not df[target].isin([0, 1]).all():
        raise ValueError("target must be binary (0/1)")

    contract_mob = (
        df.groupby(["safra", contract_id, "mob"], as_index=False)
        .agg(event_at_mob=(target, "max"))
        .sort_values(["safra", contract_id, "mob"])
    )
    if target_is_cumulative:
        decreases = (
            contract_mob.groupby(["safra", contract_id], sort=False)["event_at_mob"]
            .diff()
            .lt(0)
        )
        if decreases.any():
            raise ValueError("cumulative target cannot decrease for a contract")
        contract_mob["event_by_mob"] = contract_mob["event_at_mob"]
    else:
        contract_mob["event_by_mob"] = contract_mob.groupby(
            ["safra", contract_id], sort=False
        )["event_at_mob"].cummax()

    cohort_size = (
        contract_mob.groupby("safra")[contract_id]
        .nunique()
        .rename("n_contratos_safra")
        .reset_index()
    )
    agg = (
        contract_mob.groupby(["safra", "mob"], as_index=False)
        .agg(
            n_contratos_observados=(contract_id, "nunique"),
            n_eventos_acumulados=("event_by_mob", "sum"),
        )
        .merge(cohort_size, on="safra", how="left")
        .sort_values(["safra", "mob"])
    )
    complete_cell = agg["n_contratos_observados"] == agg["n_contratos_safra"]
    agg["taxa_acumulada"] = np.where(
        complete_cell,
        agg["n_eventos_acumulados"] / agg["n_contratos_safra"],
        np.nan,
    )
    agg["cobertura_observada"] = agg["n_contratos_observados"] / agg["n_contratos_safra"]
    agg["taxa"] = agg["taxa_acumulada"]

    print(f"Vintage table: {agg['safra'].nunique()} safras, MOB range [{agg['mob'].min()}-{agg['mob'].max()}]")
    return agg


def plot_vintage_curves(
    vintage_df: pd.DataFrame,
    title: str = "Curvas de Maturação por Safra",
    max_mob: int = 24,
    top_n_safras: Optional[int] = None,
) -> Any:
    """Plota curvas de maturação com a aparência legada."""
    import plotly.express as px

    plot_df = vintage_df[vintage_df["mob"] <= max_mob].copy()
    if top_n_safras:
        safras = sorted(plot_df["safra"].unique())[-top_n_safras:]
        plot_df = plot_df[plot_df["safra"].isin(safras)]

    fig = px.line(
        plot_df,
        x="mob", y="taxa_acumulada",
        color="safra",
        title=title,
        labels={"mob": "MOB (Months on Books)", "taxa_acumulada": "Taxa acumulada", "safra": "Safra"},
        color_discrete_sequence=PALETA_CATEGORICA,
    )
    fig.update_layout(**TEMA_BASE)
    fig.update_layout(yaxis_tickformat=".1%", legend_title_text="Safra")
    return fig


def plot_vintage_curves_resolvido(
    vintage_df: pd.DataFrame,
    theme: ResolvedTheme,
    title: str = "Curvas de Maturação por Safra",
    max_mob: int = 24,
    top_n_safras: Optional[int] = None,
) -> Any:
    """Reusa os mesmos pontos da curva e aplica paleta/layout do tema explícito."""
    tokens = get_tokens_plotly(theme)
    fig = plot_vintage_curves(vintage_df, title, max_mob, top_n_safras)
    palette = list(tokens["palette.categorical"])
    for idx, trace in enumerate(fig.data):
        trace.line.color = palette[idx % len(palette)]
    aplicar_tema_resolvido(fig, theme)
    fig.update_layout(title=title, yaxis_tickformat=".1%", legend_title_text="Safra")
    return fig


def plot_vintage_heatmap(
    vintage_df: pd.DataFrame,
    title: str = "Heatmap de Safras",
    max_mob: int = 24,
    metric: str = "taxa_acumulada",
) -> Any:
    """Plota heatmap de safras × MOB com a aparência legada."""
    import plotly.graph_objects as go

    plot_df = vintage_df[vintage_df["mob"] <= max_mob].copy()
    pivot = plot_df.pivot_table(index="safra", columns="mob", values=metric)
    pivot = pivot.sort_index(ascending=False)

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values * 100,
        x=[f"MOB {c}" for c in pivot.columns],
        y=pivot.index,
        colorscale=[[p, cor] for p, cor in zip((0, 0.25, 0.5, 0.75, 1), PALETA_SEQUENCIAL)],
        text=np.round(pivot.values * 100, 1),
        texttemplate="%{text:.1f}%",
        textfont={"size": 9},
        colorbar_title="Taxa (%)",
    ))
    fig.update_layout(**TEMA_BASE)
    fig.update_layout(
        title=title,
        width=1200, height=max(400, len(pivot) * 25),
        xaxis_title="MOB",
        yaxis_title="Safra",
    )
    return fig


def plot_vintage_heatmap_resolvido(
    vintage_df: pd.DataFrame,
    theme: ResolvedTheme,
    title: str = "Heatmap de Safras",
    max_mob: int = 24,
    metric: str = "taxa_acumulada",
) -> Any:
    """Reusa a mesma matriz e aplica ``palette.sequential`` do tema explícito."""
    tokens = get_tokens_plotly(theme)
    fig = plot_vintage_heatmap(vintage_df, title, max_mob, metric)
    cores = list(tokens["palette.sequential"])
    fig.data[0].colorscale = [[i / (len(cores) - 1), cor] for i, cor in enumerate(cores)]
    n_safras = len(fig.data[0].y)
    aplicar_tema_resolvido(fig, theme)
    fig.update_layout(
        title=title,
        height=max(tokens["chart.height_px"], n_safras * 25),
        xaxis_title="MOB",
        yaxis_title="Safra",
    )
    return fig


def compare_safras(
    vintage_df: pd.DataFrame,
    mob_checkpoints: Optional[List[int]] = None,
) -> pd.DataFrame:
    """Compara performance das safras em MOBs fixos."""
    mob_checkpoints = [3, 6, 12, 24] if mob_checkpoints is None else list(mob_checkpoints)
    results = []
    for safra in sorted(vintage_df["safra"].unique()):
        safra_data = vintage_df[vintage_df["safra"] == safra]
        row = {"safra": safra, "n_contratos": safra_data["n_contratos_safra"].iloc[0]}
        for mob in mob_checkpoints:
            mob_data = safra_data[safra_data["mob"] == mob]
            row[f"taxa_mob_{mob}"] = mob_data["taxa_acumulada"].iloc[0] if len(mob_data) > 0 else None
        results.append(row)

    result_df = pd.DataFrame(results)
    for mob in mob_checkpoints:
        col = f"taxa_mob_{mob}"
        if col in result_df.columns:
            mean_val = result_df[col].mean()
            result_df[f"vs_media_mob_{mob}"] = result_df[col] - mean_val
    return result_df
