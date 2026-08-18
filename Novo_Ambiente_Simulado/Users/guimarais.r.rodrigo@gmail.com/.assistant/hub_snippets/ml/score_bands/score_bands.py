"""Cria faixas de score auditáveis, com a direção do score declarada."""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np
import pandas as pd


def generate_score_bands(
    scores: np.ndarray,
    y_true: np.ndarray,
    n_bands: int = 10,
    labels: Optional[Sequence[str]] = None,
    *,
    higher_score_is_better: bool = True,
) -> pd.DataFrame:
    """Summarize event rates from the best band to the worst band.

    Quantile edges can collapse when scores are tied; the returned number of bands
    may therefore be smaller than ``n_bands``. Approval accumulation follows the
    declared score direction and assumes ``y_true=1`` is the adverse event.
    """
    scores = np.asarray(scores, dtype=float)
    y_true = np.asarray(y_true)
    if scores.ndim != 1 or y_true.ndim != 1 or len(scores) != len(y_true) or len(scores) == 0:
        raise ValueError("scores and y_true must be non-empty one-dimensional arrays of equal length")
    if not np.isfinite(scores).all():
        raise ValueError("scores must be finite")
    if not np.isin(y_true, [0, 1]).all():
        raise ValueError("y_true must contain only 0 and 1")
    if n_bands < 2:
        raise ValueError("n_bands must be at least 2")

    frame = pd.DataFrame({"score": scores, "event": y_true})
    raw_band = pd.qcut(frame["score"], q=min(n_bands, len(frame)), duplicates="drop")
    frame["__interval"] = raw_band
    intervals = sorted(frame["__interval"].dropna().unique(), key=lambda interval: interval.mid, reverse=higher_score_is_better)
    actual_bands = len(intervals)
    if labels is None:
        labels = [f"B{index:02d}" for index in range(1, actual_bands + 1)]
    if len(labels) != actual_bands:
        raise ValueError(f"labels must contain {actual_bands} values after duplicate quantile edges were removed")
    label_map = dict(zip(intervals, labels))
    frame["faixa"] = frame["__interval"].map(label_map)

    total = len(frame)
    cumulative = 0.0
    rows = []
    for interval in intervals:
        subset = frame[frame["__interval"] == interval]
        count = len(subset)
        share = count / total
        cumulative += share
        events = int(subset["event"].sum())
        rows.append(
            {
                "faixa": label_map[interval],
                "score_min": float(subset["score"].min()),
                "score_max": float(subset["score"].max()),
                "n": count,
                "pct_base": share * 100,
                "n_bom": count - events,
                "n_mau": events,
                "taxa_default": events / count * 100,
                "aprovacao_acum": cumulative * 100,
                "higher_score_is_better": higher_score_is_better,
            }
        )
    return pd.DataFrame(rows)
