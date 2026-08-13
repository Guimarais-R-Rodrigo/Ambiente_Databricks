"""
Cálculo padronizado de métricas de ML (AUC, KS, Gini, Lift, etc.).

Uso:
    from x_snippets.ml.metrics_report import calculate_binary_metrics, format_metrics_table
    metrics = calculate_binary_metrics(y_true, y_prob)

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
from sklearn.metrics import (
    roc_auc_score, precision_recall_curve, average_precision_score,
    brier_score_loss, f1_score, precision_score, recall_score,
    mean_squared_error, mean_absolute_error, r2_score
)
from typing import Dict


def calculate_binary_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5) -> Dict[str, float]:
    """Calcula métricas completas para classificação binária.

    Args:
        y_true: Labels verdadeiros (0/1).
        y_prob: Probabilidades preditas.
        threshold: Threshold para métricas de classificação hard.

    Returns:
        Dicionário com todas as métricas.
    """
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob, dtype=float)
    if y_true.ndim != 1 or y_prob.ndim != 1 or len(y_true) != len(y_prob) or len(y_true) == 0:
        raise ValueError("y_true and y_prob must be non-empty 1-D arrays of equal length")
    if not np.isin(y_true, [0, 1]).all() or np.unique(y_true).size != 2:
        raise ValueError("binary metrics require both classes 0 and 1")
    if not np.isfinite(y_prob).all() or ((y_prob < 0) | (y_prob > 1)).any():
        raise ValueError("y_prob must contain finite probabilities in [0, 1]")
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be in [0, 1]")
    y_pred = (y_prob >= threshold).astype(int)

    auc = roc_auc_score(y_true, y_prob)
    ks = _calculate_ks(y_true, y_prob)
    gini = 2 * auc - 1

    return {
        "auc_roc": round(auc, 4),
        "ks": round(ks, 1),
        "gini": round(gini, 4),
        "auc_pr": round(average_precision_score(y_true, y_prob), 4),
        "brier_score": round(brier_score_loss(y_true, y_prob), 4),
        "f1": round(f1_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred), 4),
        "lift_10pct": round(_calculate_lift(y_true, y_prob, top_pct=0.10), 2),
        "prevalence": round(y_true.mean(), 4),
    }


def calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calcula métricas completas para regressão.

    Args:
        y_true: Valores verdadeiros.
        y_pred: Valores preditos.

    Returns:
        Dicionário com todas as métricas.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.ndim != 1 or y_pred.ndim != 1 or len(y_true) != len(y_pred) or len(y_true) == 0:
        raise ValueError("y_true and y_pred must be non-empty 1-D arrays of equal length")
    if not np.isfinite(y_true).all() or not np.isfinite(y_pred).all():
        raise ValueError("regression inputs must be finite")
    mask = y_true != 0  # MAPE is undefined where the actual value is zero.
    mape = float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100) if mask.any() else float("nan")
    return {
        "rmse": round(np.sqrt(mean_squared_error(y_true, y_pred)), 4),
        "mae": round(mean_absolute_error(y_true, y_pred), 4),
        "mape": round(mape, 2),
        "r2": round(r2_score(y_true, y_pred), 4),
    }


def _calculate_ks(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Calcula KS (Kolmogorov-Smirnov)."""
    from scipy.stats import ks_2samp
    pos_scores = y_prob[y_true == 1]
    neg_scores = y_prob[y_true == 0]
    ks_stat, _ = ks_2samp(pos_scores, neg_scores)
    return ks_stat * 100


def _calculate_lift(y_true: np.ndarray, y_prob: np.ndarray, top_pct: float = 0.10) -> float:
    """Calcula Lift no top X%."""
    if not 0 < top_pct <= 1:
        raise ValueError("top_pct must be in (0, 1]")
    n_top = max(1, int(np.ceil(len(y_true) * top_pct)))
    idx_sorted = np.argsort(-y_prob)
    top_target_rate = y_true[idx_sorted[:n_top]].mean()
    overall_rate = y_true.mean()
    return top_target_rate / overall_rate if overall_rate > 0 else 0.0
