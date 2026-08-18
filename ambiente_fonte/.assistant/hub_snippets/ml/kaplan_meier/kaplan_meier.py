"""
Kaplan-Meier com visualização Plotly e log-rank test.

Uso:
    from hub_snippets.ml.kaplan_meier import plot_kaplan_meier, log_rank_test
    fig = plot_kaplan_meier(df, duration_col='duration', event_col='event', group_col='segmento')

Autor: Rodrigo via assistente
Versão: 1.0
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go

from hub_snippets.constants.colors import (
    AZUL_CAIXA,
    AZUL_CLARO,
    CINZA_ESCURO,
    LARANJA,
    ROXO,
    TEAL,
    VERDE,
    VERMELHO,
)
from typing import Any, Optional, List, Dict


def plot_kaplan_meier(
    df: pd.DataFrame,
    duration_col: str,
    event_col: str,
    group_col: Optional[str] = None,
    title: str = "Curva de Sobrevivência (Kaplan-Meier)",
    ci: bool = True,
) -> go.Figure:
    """Plota curvas Kaplan-Meier com Plotly.

    Args:
        df: DataFrame com duration e event.
        duration_col: Coluna de tempo.
        event_col: Coluna de evento.
        group_col: Coluna de grupo (opcional, para comparar curvas).
        title: Título do gráfico.
        ci: Se True, mostra intervalo de confiança 95%.

    Returns:
        Plotly Figure.
    """
    from lifelines import KaplanMeierFitter

    fig = go.Figure()
    kmf = KaplanMeierFitter()

    if group_col is None:
        groups = {"Global": df}
    else:
        groups = {name: group for name, group in df.groupby(group_col)}

    # Ordem propria, e nao `PALETA_CATEGORICA[:8]`: aqui CINZA_ESCURO vem por
    # ultimo. Nomear preserva a atribuicao de cor por curva; fatiar a paleta
    # mudaria quatro delas.
    colors = [AZUL_CAIXA, LARANJA, AZUL_CLARO, VERDE, VERMELHO, ROXO, TEAL, CINZA_ESCURO]

    for i, (name, group_df) in enumerate(groups.items()):
        kmf.fit(group_df[duration_col], event_observed=group_df[event_col], label=str(name))
        color = colors[i % len(colors)]

        # Curva principal
        fig.add_trace(go.Scatter(
            x=kmf.survival_function_.index,
            y=kmf.survival_function_.iloc[:, 0],
            mode="lines",
            name=f"{name} (n={len(group_df)}, mediana={kmf.median_survival_time_:.1f})",
            line=dict(color=color, width=2),
        ))

        # IC 95%
        if ci:
            ci_df = kmf.confidence_interval_survival_function_
            fig.add_trace(go.Scatter(
                x=list(ci_df.index) + list(ci_df.index[::-1]),
                y=list(ci_df.iloc[:, 0]) + list(ci_df.iloc[:, 1][::-1]),
                fill="toself",
                fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.1)",
                line=dict(color="rgba(0,0,0,0)"),
                showlegend=False,
            ))

    fig.update_layout(
        template="plotly_white",
        font=dict(family="Segoe UI, Roboto, sans-serif", size=12, color=CINZA_ESCURO),
        title=dict(text=title, font=dict(size=16, color=AZUL_CAIXA), x=0.01, xanchor="left"),
        xaxis_title="Tempo",
        yaxis_title="S(t) — Probabilidade de sobrevivência",
        width=900, height=550,
        margin=dict(l=60, r=30, t=70, b=60),
        yaxis=dict(range=[0, 1.05]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    )

    return fig


def log_rank_test(
    df: pd.DataFrame,
    duration_col: str,
    event_col: str,
    group_col: str,
) -> Dict[str, Any]:
    """Executa log-rank test entre grupos.

    Args:
        df: DataFrame.
        duration_col: Coluna de tempo.
        event_col: Coluna de evento.
        group_col: Coluna de grupo.

    Returns:
        Dict com estatística e p-value.
    """
    from lifelines.statistics import logrank_test, multivariate_logrank_test

    groups = df[group_col].unique()
    if len(groups) != 2:
        # Teste global primeiro; pairwise com correção Holm para multiplicidade.
        from itertools import combinations
        global_result = multivariate_logrank_test(df[duration_col], df[group_col], df[event_col])
        raw_pairs = []
        for g1, g2 in combinations(groups, 2):
            d1 = df[df[group_col] == g1]
            d2 = df[df[group_col] == g2]
            lr = logrank_test(d1[duration_col], d2[duration_col], d1[event_col], d2[event_col])
            raw_pairs.append((f"{g1}_vs_{g2}", float(lr.test_statistic), float(lr.p_value)))

        # Holm step-down adjustment without adding a statsmodels dependency.
        ordered = sorted(enumerate(raw_pairs), key=lambda item: item[1][2])
        adjusted = [0.0] * len(raw_pairs)
        running = 0.0
        m = len(raw_pairs)
        for rank, (original_index, (_, _, p_value)) in enumerate(ordered):
            running = max(running, min(1.0, (m - rank) * p_value))
            adjusted[original_index] = running
        pairwise = {
            name: {
                "statistic": statistic,
                "p_value_raw": p_value,
                "p_value_holm": adjusted[index],
                "significant_holm_0_05": adjusted[index] < 0.05,
            }
            for index, (name, statistic, p_value) in enumerate(raw_pairs)
        }
        return {
            "global": {
                "statistic": float(global_result.test_statistic),
                "p_value": float(global_result.p_value),
                "significant_0_05": float(global_result.p_value) < 0.05,
            },
            "pairwise_holm": pairwise,
        }
    else:
        d1 = df[df[group_col] == groups[0]]
        d2 = df[df[group_col] == groups[1]]
        lr = logrank_test(d1[duration_col], d2[duration_col], d1[event_col], d2[event_col])
        sig = "✅ significativo" if lr.p_value < 0.05 else "❌ não significativo"
        print(f"  Log-rank: χ²={lr.test_statistic:.2f}, p={lr.p_value:.4f} ({sig})")
        return {"statistic": lr.test_statistic, "p_value": lr.p_value}
