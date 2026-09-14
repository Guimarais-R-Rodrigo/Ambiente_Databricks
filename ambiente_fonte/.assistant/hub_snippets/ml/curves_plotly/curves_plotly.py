"""
Curvas diagnósticas de ML em Plotly com tema institucional.

Uso legado:
    from hub_snippets.ml.curves_plotly import plot_roc_curve
    fig = plot_roc_curve(y_true, y_prob)

Uso V07 opt-in:
    from hub_snippets.ml.curves_plotly import plot_roc_curve_resolvido
    fig = plot_roc_curve_resolvido(y_true, y_prob, theme)

A rota legada preserva a paleta histórica de seis cores. A rota resolvida usa o
token dedicado ``palette.curves_legacy`` e nunca altera o cálculo das métricas.
"""

import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score
from typing import Optional

from hub_snippets.constants import colors
from hub_snippets.visual.tema import ResolvedTheme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido, get_tokens_plotly

# Paleta histórica deliberadamente distinta da paleta geral de dez cores.
PALETA_CATEGORICA = ["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E"]
AZUL_CAIXA = colors.AZUL_CAIXA
LARANJA = colors.LARANJA
CINZA_ESCURO = colors.CINZA_ESCURO

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


def _validate_binary_inputs(y_true: np.ndarray, y_prob: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob, dtype=float)
    if y_true.ndim != 1 or y_prob.ndim != 1 or len(y_true) != len(y_prob) or len(y_true) == 0:
        raise ValueError("y_true and y_prob must be non-empty one-dimensional arrays of equal length")
    if not np.isin(y_true, [0, 1]).all() or np.unique(y_true).size != 2:
        raise ValueError("binary curves require both classes 0 and 1")
    if not np.isfinite(y_prob).all() or ((y_prob < 0) | (y_prob > 1)).any():
        raise ValueError("y_prob must contain finite probabilities in [0, 1]")
    return y_true, y_prob


def _visuais(theme: Optional[ResolvedTheme]):
    if theme is None:
        return {
            "palette": list(PALETA_CATEGORICA),
            "primary": AZUL_CAIXA,
            "accent": LARANJA,
            "neutral": CINZA_ESCURO,
            "card": "rgba(255,255,255,0.8)",
        }
    tokens = get_tokens_plotly(theme)
    palette = list(tokens["palette.curves_legacy"])
    return {
        "palette": palette,
        "primary": palette[0],
        "accent": palette[1],
        "neutral": tokens["text.plot"],
        "card": tokens["surface.card"],
    }


def _aplicar_tema(fig: go.Figure, subtitulo: Optional[str] = None, n: Optional[int] = None) -> go.Figure:
    """Aplica o tema histórico exatamente como antes da V07."""
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


def _finalizar(fig: go.Figure, theme: Optional[ResolvedTheme], *, subtitulo: str, n: int) -> go.Figure:
    if theme is None:
        return _aplicar_tema(fig, subtitulo=subtitulo, n=n)
    aplicar_tema_resolvido(fig, theme, subtitulo=subtitulo, n=n)
    # A família de curvas possui paleta própria no contrato e não deve ser
    # expandida silenciosamente para ``palette.categorical``.
    fig.update_layout(colorway=_visuais(theme)["palette"])
    return fig


def _plot_roc_curve(y_true, y_prob, title, show_auc, n, *, theme):
    vis = _visuais(theme)
    y_true, y_prob = _validate_binary_inputs(y_true, y_prob)
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc_val = roc_auc_score(y_true, y_prob)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines",
        name=f"Modelo (AUC = {auc_val:.3f})",
        line=dict(color=vis["primary"], width=2.5),
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines",
        name="Random (AUC = 0.500)",
        line=dict(color=vis["neutral"], width=1, dash="dash"),
    ))
    if show_auc:
        font = dict(size=14, color=vis["primary"])
        if theme is None:
            font["family"] = "Segoe UI"
        fig.add_annotation(
            x=0.6, y=0.3, text=f"AUC = {auc_val:.4f}",
            showarrow=False, font=font,
            bgcolor=vis["card"], bordercolor=vis["primary"], borderwidth=1,
        )
    fig.update_xaxes(title="Taxa de Falso Positivo (FPR)")
    fig.update_yaxes(title="Taxa de Verdadeiro Positivo (TPR)")
    _finalizar(fig, theme, subtitulo=f"AUC = {auc_val:.4f}", n=n or len(y_true))
    fig.update_layout(title=title)
    return fig


def plot_roc_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str = "Curva ROC", show_auc: bool = True, n: Optional[int] = None) -> go.Figure:
    """Gera a curva ROC legada."""
    return _plot_roc_curve(y_true, y_prob, title, show_auc, n, theme=None)


def plot_roc_curve_resolvido(y_true: np.ndarray, y_prob: np.ndarray, theme: ResolvedTheme, title: str = "Curva ROC", show_auc: bool = True, n: Optional[int] = None) -> go.Figure:
    """Gera a mesma curva ROC com aparência derivada do tema V02."""
    return _plot_roc_curve(y_true, y_prob, title, show_auc, n, theme=theme)


def _plot_pr_curve(y_true, y_prob, title, n, *, theme):
    from sklearn.metrics import average_precision_score

    vis = _visuais(theme)
    y_true, y_prob = _validate_binary_inputs(y_true, y_prob)
    precision, recall, _ = precision_recall_curve(y_true, y_prob)
    ap = average_precision_score(y_true, y_prob)
    baseline = y_true.mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=recall, y=precision, mode="lines",
        name=f"Modelo (AP = {ap:.3f})",
        line=dict(color=vis["primary"], width=2.5),
    ))
    fig.add_hline(
        y=baseline, line_dash="dash", line_color=vis["neutral"],
        annotation_text=f"Baseline ({baseline:.1%})", annotation_position="top right",
    )
    fig.update_xaxes(title="Recall")
    fig.update_yaxes(title="Precision")
    _finalizar(fig, theme, subtitulo=f"AP = {ap:.4f} | Baseline = {baseline:.1%}", n=n or len(y_true))
    fig.update_layout(title=title)
    return fig


def plot_pr_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str = "Curva Precision-Recall", n: Optional[int] = None) -> go.Figure:
    """Gera a curva Precision-Recall legada."""
    return _plot_pr_curve(y_true, y_prob, title, n, theme=None)


def plot_pr_curve_resolvido(y_true: np.ndarray, y_prob: np.ndarray, theme: ResolvedTheme, title: str = "Curva Precision-Recall", n: Optional[int] = None) -> go.Figure:
    """Gera a mesma curva Precision-Recall com tema explícito."""
    return _plot_pr_curve(y_true, y_prob, title, n, theme=theme)


def _plot_lift_curve(y_true, y_prob, title, n_bins, n, *, theme):
    vis = _visuais(theme)
    y_true, y_prob = _validate_binary_inputs(y_true, y_prob)
    if not 2 <= n_bins <= len(y_true):
        raise ValueError("n_bins must be between 2 and the sample size")
    order = np.argsort(-y_prob)
    y_sorted = y_true[order]
    n_total = len(y_true)
    n_positive = y_true.sum()
    baseline_rate = n_positive / n_total
    percentiles = np.linspace(0, 1, n_bins + 1)[1:]
    lifts = []
    for p in percentiles:
        k = max(1, int(np.ceil(p * n_total)))
        captured = y_sorted[:k].sum()
        expected = k * baseline_rate
        lifts.append(captured / expected)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=percentiles * 100, y=lifts, mode="lines+markers", name="Lift",
        line=dict(color=vis["primary"], width=2.5), marker=dict(size=8, color=vis["primary"]),
    ))
    fig.add_hline(y=1, line_dash="dash", line_color=vis["neutral"], annotation_text="Sem modelo (lift = 1)")
    first_share = float(percentiles[0] * 100)
    share_label = f"{first_share:g}%"
    fig.add_annotation(
        x=first_share, y=lifts[0], text=f"Lift top-{share_label} = {lifts[0]:.2f}x",
        showarrow=True, arrowhead=2, ax=40, ay=-30,
        font=dict(size=11, color=vis["primary"]),
    )
    fig.update_xaxes(title="% da base (ordenada por score)")
    fig.update_yaxes(title="Lift")
    _finalizar(fig, theme, subtitulo=f"Top-{share_label} lift = {lifts[0]:.2f}x", n=n or n_total)
    fig.update_layout(title=title)
    return fig


def plot_lift_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str = "Curva de Lift", n_bins: int = 10, n: Optional[int] = None) -> go.Figure:
    """Gera a curva de Lift legada."""
    return _plot_lift_curve(y_true, y_prob, title, n_bins, n, theme=None)


def plot_lift_curve_resolvido(y_true: np.ndarray, y_prob: np.ndarray, theme: ResolvedTheme, title: str = "Curva de Lift", n_bins: int = 10, n: Optional[int] = None) -> go.Figure:
    """Gera a mesma curva de Lift com tema explícito."""
    return _plot_lift_curve(y_true, y_prob, title, n_bins, n, theme=theme)


def _plot_ks_curve(y_true, y_prob, title, n, *, theme):
    vis = _visuais(theme)
    y_true, y_prob = _validate_binary_inputs(y_true, y_prob)
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    ks_values = tpr - fpr
    ks_max_idx = np.argmax(ks_values)
    ks_stat = ks_values[ks_max_idx]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="TPR (sensibilidade)", line=dict(color=vis["primary"], width=2)))
    fig.add_trace(go.Scatter(x=fpr, y=fpr, mode="lines", name="FPR (diagonal)", line=dict(color=vis["neutral"], width=1, dash="dash")))
    fig.add_shape(type="line", x0=fpr[ks_max_idx], x1=fpr[ks_max_idx], y0=fpr[ks_max_idx], y1=tpr[ks_max_idx], line=dict(color=vis["accent"], width=2.5, dash="dot"))
    fig.add_annotation(
        x=fpr[ks_max_idx], y=(tpr[ks_max_idx] + fpr[ks_max_idx]) / 2,
        text=f"KS = {ks_stat:.4f}", showarrow=True, arrowhead=2,
        ax=50, ay=-20, font=dict(size=12, color=vis["accent"]),
    )
    fig.update_xaxes(title="FPR")
    fig.update_yaxes(title="TPR / FPR")
    _finalizar(fig, theme, subtitulo=f"KS = {ks_stat:.4f}", n=n or len(y_true))
    fig.update_layout(title=title)
    return fig


def plot_ks_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str = "Curva KS", n: Optional[int] = None) -> go.Figure:
    """Gera a curva KS legada."""
    return _plot_ks_curve(y_true, y_prob, title, n, theme=None)


def plot_ks_curve_resolvido(y_true: np.ndarray, y_prob: np.ndarray, theme: ResolvedTheme, title: str = "Curva KS", n: Optional[int] = None) -> go.Figure:
    """Gera a mesma curva KS com tema explícito."""
    return _plot_ks_curve(y_true, y_prob, title, n, theme=theme)
