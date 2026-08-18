"""
Curvas diagnósticas de ML em Plotly com tema institucional.

Uso:
    from hub_snippets.ml.curves_plotly import plot_roc_curve, plot_pr_curve, plot_lift_curve
    fig = plot_roc_curve(y_true, y_prob, title="ROC — Churn Previdência")

Autor: Rodrigo via assistente
Versão: 1.1 — Adequação visual (paleta Caixa + aplicar_tema)
"""

import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score
from typing import Optional

# Paleta institucional Caixa
# PENDENTE/DECISAO -- a unica linha do 12.2 que nao e higiene.
# Esta paleta tem **seis** cores; a oficial em `constants.colors` tem dez, e as
# seis primeiras sao identicas. Trocar por `colors.PALETA_CATEGORICA` nao mudaria
# nenhum grafico com ate seis series, e mudaria todos os que passam disso: hoje
# a setima serie recomeca no azul, e passaria a ser roxo. E decisao de produto.
PALETA_CATEGORICA = ["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E"]
from hub_snippets.constants import colors

AZUL_CAIXA = colors.AZUL_CAIXA
LARANJA = colors.LARANJA
CINZA_ESCURO = colors.CINZA_ESCURO

# Tema padrão
TEMA_BASE = dict(
    template="plotly_white",
    font=dict(family="Segoe UI, Roboto, sans-serif", size=12, color=CINZA_ESCURO),
    title=dict(font=dict(size=16, color=AZUL_CAIXA), x=0.01, xanchor="left"),
    colorway=PALETA_CATEGORICA,
    height=450,
    width=900,
    margin=dict(l=60, r=30, t=70, b=60),
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
)


def _aplicar_tema(fig: go.Figure, subtitulo: Optional[str] = None, n: Optional[int] = None) -> go.Figure:
    """Aplica tema institucional ao gráfico."""
    fig.update_layout(**TEMA_BASE)
    footer = []
    if n is not None:
        footer.append(f"N = {n:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
    if subtitulo:
        footer.append(subtitulo)
    if footer:
        fig.add_annotation(
            text=" | ".join(footer), xref="paper", yref="paper",
            x=0, y=-0.18, showarrow=False,
            font=dict(size=10, color=colors.TEXTO_SECUNDARIO), xanchor="left",
        )
    return fig


def plot_roc_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    title: str = "Curva ROC",
    show_auc: bool = True,
    n: Optional[int] = None,
) -> go.Figure:
    """Gera curva ROC com AUC anotado.

    Args:
        y_true: Labels verdadeiros.
        y_prob: Probabilidades preditas.
        title: Título do gráfico.
        show_auc: Se True, mostra AUC no gráfico.
        n: N amostral para rodapé.

    Returns:
        Plotly Figure.
    """
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc_val = roc_auc_score(y_true, y_prob)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines",
        name=f"Modelo (AUC = {auc_val:.3f})",
        line=dict(color=AZUL_CAIXA, width=2.5),
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines",
        name="Random (AUC = 0.500)",
        line=dict(color=CINZA_ESCURO, width=1, dash="dash"),
    ))

    if show_auc:
        fig.add_annotation(
            x=0.6, y=0.3, text=f"AUC = {auc_val:.4f}",
            showarrow=False, font=dict(size=14, color=AZUL_CAIXA, family="Segoe UI"),
            bgcolor="rgba(255,255,255,0.8)", bordercolor=AZUL_CAIXA, borderwidth=1,
        )

    fig.update_xaxes(title="Taxa de Falso Positivo (FPR)")
    fig.update_yaxes(title="Taxa de Verdadeiro Positivo (TPR)")

    _aplicar_tema(fig, subtitulo=f"AUC = {auc_val:.4f}", n=n or len(y_true))
    fig.update_layout(title=title)

    return fig


def plot_pr_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    title: str = "Curva Precision-Recall",
    n: Optional[int] = None,
) -> go.Figure:
    """Gera curva Precision-Recall.

    Args:
        y_true: Labels verdadeiros.
        y_prob: Probabilidades preditas.
        title: Título do gráfico.
        n: N amostral para rodapé.

    Returns:
        Plotly Figure.
    """
    precision, recall, _ = precision_recall_curve(y_true, y_prob)
    # Average Precision
    from sklearn.metrics import average_precision_score
    ap = average_precision_score(y_true, y_prob)

    # Baseline (proporção de positivos)
    baseline = y_true.mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=recall, y=precision, mode="lines",
        name=f"Modelo (AP = {ap:.3f})",
        line=dict(color=AZUL_CAIXA, width=2.5),
    ))
    fig.add_hline(
        y=baseline, line_dash="dash", line_color=CINZA_ESCURO,
        annotation_text=f"Baseline ({baseline:.1%})",
        annotation_position="top right",
    )

    fig.update_xaxes(title="Recall")
    fig.update_yaxes(title="Precision")

    _aplicar_tema(fig, subtitulo=f"AP = {ap:.4f} | Baseline = {baseline:.1%}", n=n or len(y_true))
    fig.update_layout(title=title)

    return fig


def plot_lift_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    title: str = "Curva de Lift",
    n_bins: int = 10,
    n: Optional[int] = None,
) -> go.Figure:
    """Gera curva de Lift (ganho acumulado).

    Args:
        y_true: Labels verdadeiros.
        y_prob: Probabilidades preditas.
        title: Título do gráfico.
        n_bins: Número de decis para cálculo.
        n: N amostral para rodapé.

    Returns:
        Plotly Figure.
    """
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob, dtype=float)
    if y_true.ndim != 1 or y_prob.ndim != 1 or len(y_true) != len(y_prob) or len(y_true) == 0:
        raise ValueError("y_true and y_prob must be non-empty one-dimensional arrays of equal length")
    if not np.isfinite(y_prob).all() or not np.isin(y_true, [0, 1]).all():
        raise ValueError("y_prob must be finite and y_true must contain only 0/1")
    if not 2 <= n_bins <= len(y_true):
        raise ValueError("n_bins must be between 2 and the sample size")

    # Ordenar por probabilidade decrescente
    order = np.argsort(-y_prob)
    y_sorted = y_true[order]

    # Calcular lift cumulativo
    n_total = len(y_true)
    n_positive = y_true.sum()
    baseline_rate = n_positive / n_total

    percentiles = np.linspace(0, 1, n_bins + 1)[1:]
    lifts = []
    for p in percentiles:
        k = max(1, int(np.ceil(p * n_total)))
        captured = y_sorted[:k].sum()
        expected = k * baseline_rate
        lifts.append(captured / expected if expected > 0 else 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=percentiles * 100, y=lifts, mode="lines+markers",
        name="Lift",
        line=dict(color=AZUL_CAIXA, width=2.5),
        marker=dict(size=8, color=AZUL_CAIXA),
    ))
    fig.add_hline(y=1, line_dash="dash", line_color=CINZA_ESCURO,
                  annotation_text="Sem modelo (lift = 1)")

    first_share = float(percentiles[0] * 100)
    share_label = f"{first_share:g}%"
    # Destacar o primeiro segmento, que equivale a 1/n_bins da base.
    fig.add_annotation(
        x=first_share, y=lifts[0], text=f"Lift top-{share_label} = {lifts[0]:.2f}x",
        showarrow=True, arrowhead=2, ax=40, ay=-30,
        font=dict(size=11, color=AZUL_CAIXA),
    )

    fig.update_xaxes(title="% da base (ordenada por score)")
    fig.update_yaxes(title="Lift")

    _aplicar_tema(fig, subtitulo=f"Top-{share_label} lift = {lifts[0]:.2f}x", n=n or n_total)
    fig.update_layout(title=title)

    return fig


def plot_ks_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    title: str = "Curva KS",
    n: Optional[int] = None,
) -> go.Figure:
    """Gera curva KS (Kolmogorov-Smirnov) com ponto de máxima separação.

    Args:
        y_true: Labels verdadeiros (0/1).
        y_prob: Probabilidades preditas.
        title: Título do gráfico.
        n: N amostral para rodapé.

    Returns:
        Plotly Figure.
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    ks_values = tpr - fpr
    ks_max_idx = np.argmax(ks_values)
    ks_stat = ks_values[ks_max_idx]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="TPR (sensibilidade)",
                             line=dict(color=AZUL_CAIXA, width=2)))
    fig.add_trace(go.Scatter(x=fpr, y=fpr, mode="lines", name="FPR (diagonal)",
                             line=dict(color=CINZA_ESCURO, width=1, dash="dash")))

    # Linha vertical no ponto KS máximo
    fig.add_shape(type="line",
                  x0=fpr[ks_max_idx], x1=fpr[ks_max_idx],
                  y0=fpr[ks_max_idx], y1=tpr[ks_max_idx],
                  line=dict(color=LARANJA, width=2.5, dash="dot"))

    fig.add_annotation(
        x=fpr[ks_max_idx], y=(tpr[ks_max_idx] + fpr[ks_max_idx]) / 2,
        text=f"KS = {ks_stat:.4f}", showarrow=True, arrowhead=2,
        ax=50, ay=-20, font=dict(size=12, color=LARANJA),
    )

    fig.update_xaxes(title="FPR")
    fig.update_yaxes(title="TPR / FPR")

    _aplicar_tema(fig, subtitulo=f"KS = {ks_stat:.4f}", n=n or len(y_true))
    fig.update_layout(title=title)

    return fig
