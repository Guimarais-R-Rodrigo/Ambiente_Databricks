"""
Análise de safras (vintage/cohort): curvas de maturação, heatmap e métricas.

Uso:
    from x_snippets.ml.vintage_analysis import build_vintage_table, plot_vintage_curves, plot_vintage_heatmap

Autor: Rodrigo via assistente
Versão: 1.0
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Tuple

# Paleta institucional Caixa
PALETA_CATEGORICA = ["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E",
                     "#7B2D8B", "#00A79D", "#F15A29", "#A7A9AC"]
AZUL_CAIXA = "#005CA9"
PALETA_SEQUENCIAL = ["#E6F0FA", "#99C2E8", "#4D94D6", "#005CA9", "#003D73"]
TEMA_BASE = dict(
    template="plotly_white",
    font=dict(family="Segoe UI, Roboto, sans-serif", size=12, color="#333333"),
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
    """Constrói tabela de safras agregada.

    Args:
        df: DataFrame com dados de contratos ao longo do tempo.
        contract_id: Coluna de ID do contrato.
        dt_originacao: Coluna de data de originação.
        dt_referencia: Coluna de data de referência (foto).
        target: Coluna do evento (0/1).
        safra_grain: 'month' ou 'quarter'.
        mob_col: Coluna de MOB (se já existir; senão calcula).

    Returns:
        DataFrame agregado: safra × MOB com taxa.
    """
    required = {contract_id, dt_originacao, dt_referencia, target}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if safra_grain not in {"month", "quarter"}:
        raise ValueError("safra_grain must be 'month' or 'quarter'")
    df = df.copy()
    df[dt_originacao] = pd.to_datetime(df[dt_originacao])
    df[dt_referencia] = pd.to_datetime(df[dt_referencia])

    # Calcular MOB se não fornecido
    if mob_col is None:
        df["mob"] = (
            (df[dt_referencia].dt.year - df[dt_originacao].dt.year) * 12
            + (df[dt_referencia].dt.month - df[dt_originacao].dt.month)
        )
    else:
        df["mob"] = df[mob_col]

    # Safra
    if safra_grain == "month":
        df["safra"] = df[dt_originacao].dt.to_period("M").astype(str)
    elif safra_grain == "quarter":
        df["safra"] = df[dt_originacao].dt.to_period("Q").astype(str)

    df = df[df["mob"].notna() & (df["mob"] >= 0)].copy()
    df[target] = pd.to_numeric(df[target], errors="raise")
    if not df[target].dropna().isin([0, 1]).all():
        raise ValueError("target must be binary (0/1)")

    # Collapse duplicate snapshots and expand each contract only through its last
    # observed MOB. This preserves earlier events while leaving immature cells out.
    contract_mob = (
        df.groupby(["safra", contract_id, "mob"], as_index=False)
        .agg(event_at_mob=(target, "max"))
        .sort_values(["safra", contract_id, "mob"])
    )
    expanded_rows = []
    for (cohort, contract), group in contract_mob.groupby(["safra", contract_id], sort=False):
        group = group.set_index("mob").sort_index()
        max_mob = int(group.index.max())
        timeline = group.reindex(range(0, max_mob + 1))
        timeline["event_at_mob"] = timeline["event_at_mob"].fillna(0)
        timeline["event_by_mob"] = (
            timeline["event_at_mob"] if target_is_cumulative else timeline["event_at_mob"].cummax()
        )
        timeline["safra"] = cohort
        timeline[contract_id] = contract
        timeline["mob"] = timeline.index
        expanded_rows.append(timeline.reset_index(drop=True))
    contract_mob = pd.concat(expanded_rows, ignore_index=True)

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
    # Publish a cohort/MOB rate only when every cohort contract is mature/observed
    # through that MOB. Partial cells remain NaN instead of treating immature
    # contracts as non-events or changing the denominator silently.
    complete_cell = agg["n_contratos_observados"] == agg["n_contratos_safra"]
    agg["taxa_acumulada"] = np.where(
        complete_cell,
        agg["n_eventos_acumulados"] / agg["n_contratos_safra"],
        np.nan,
    )
    agg["cobertura_observada"] = agg["n_contratos_observados"] / agg["n_contratos_safra"]
    # Backward-compatible alias: 'taxa' now has the same cumulative-incidence meaning.
    agg["taxa"] = agg["taxa_acumulada"]

    print(f"Vintage table: {agg['safra'].nunique()} safras, MOB range [{agg['mob'].min()}-{agg['mob'].max()}]")
    return agg


def plot_vintage_curves(
    vintage_df: pd.DataFrame,
    title: str = "Curvas de Maturação por Safra",
    max_mob: int = 24,
    top_n_safras: Optional[int] = None,
) -> Any:
    """Plota curvas de maturação (vintage curves).

    Args:
        vintage_df: DataFrame de build_vintage_table().
        title: Título do gráfico.
        max_mob: MOB máximo a exibir.
        top_n_safras: Se definido, mostra apenas as N safras mais recentes.

    Returns:
        Plotly Figure.
    """
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
    fig.update_layout(
        yaxis_tickformat=".1%",
        legend_title_text="Safra",
    )

    return fig


def plot_vintage_heatmap(
    vintage_df: pd.DataFrame,
    title: str = "Heatmap de Safras",
    max_mob: int = 24,
    metric: str = "taxa_acumulada",
) -> Any:
    """Plota heatmap de safras × MOB.

    Args:
        vintage_df: DataFrame de build_vintage_table().
        title: Título.
        max_mob: MOB máximo.
        metric: Coluna para colorir ('taxa', 'taxa_acumulada').

    Returns:
        Plotly Figure.
    """
    import plotly.graph_objects as go

    plot_df = vintage_df[vintage_df["mob"] <= max_mob].copy()

    # Pivot: safra × MOB
    pivot = plot_df.pivot_table(index="safra", columns="mob", values=metric)
    pivot = pivot.sort_index(ascending=False)

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values * 100,
        x=[f"MOB {c}" for c in pivot.columns],
        y=pivot.index,
        colorscale=[[0, "#E6F0FA"], [0.25, "#99C2E8"], [0.5, "#4D94D6"], [0.75, "#005CA9"], [1, "#003D73"]],
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


def compare_safras(
    vintage_df: pd.DataFrame,
    mob_checkpoints: Optional[List[int]] = None,
) -> pd.DataFrame:
    """Compara performance das safras em MOBs fixos.

    Args:
        vintage_df: DataFrame de build_vintage_table().
        mob_checkpoints: MOBs para comparação.

    Returns:
        DataFrame comparativo.
    """
    mob_checkpoints = [3, 6, 12, 24] if mob_checkpoints is None else list(mob_checkpoints)
    results = []
    for safra in sorted(vintage_df["safra"].unique()):
        safra_data = vintage_df[vintage_df["safra"] == safra]
        row = {"safra": safra, "n_contratos": safra_data["n_contratos_safra"].iloc[0]}

        for mob in mob_checkpoints:
            mob_data = safra_data[safra_data["mob"] == mob]
            if len(mob_data) > 0:
                row[f"taxa_mob_{mob}"] = mob_data["taxa_acumulada"].iloc[0]
            else:
                row[f"taxa_mob_{mob}"] = None

        results.append(row)

    result_df = pd.DataFrame(results)

    # Calcular média e desvio
    for mob in mob_checkpoints:
        col = f"taxa_mob_{mob}"
        if col in result_df.columns:
            mean_val = result_df[col].mean()
            result_df[f"vs_media_mob_{mob}"] = result_df[col] - mean_val

    return result_df
