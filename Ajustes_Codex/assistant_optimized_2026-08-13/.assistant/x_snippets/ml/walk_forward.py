"""Calendar-aware expanding-window validation for temporal models."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Dict, List

import numpy as np
import pandas as pd


def walk_forward_cv(
    df: pd.DataFrame,
    date_col: str,
    target_col: str,
    model_fn: Callable[[pd.DataFrame, pd.DataFrame], Dict[str, Any]],
    min_train_periods: int = 12,
    test_periods: int = 1,
    step: int = 1,
    gap: int = 0,
    *,
    period_unit: str = "M",
) -> List[Dict[str, Any]]:
    """Run expanding-window folds on normalized calendar periods.

    ``model_fn`` must fit only on its first argument and evaluate ``target_col``
    only on its second. Preprocessing must be fitted inside each call.
    """
    missing = {date_col, target_col} - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if min_train_periods <= 0 or test_periods <= 0 or step <= 0 or gap < 0:
        raise ValueError("min_train_periods, test_periods, and step must be positive; gap cannot be negative")

    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col], errors="raise")
    data["__period"] = data[date_col].dt.to_period(period_unit)
    periods = sorted(data["__period"].dropna().unique())
    results: List[Dict[str, Any]] = []

    stop = len(periods) - gap - test_periods + 1
    for end in range(min_train_periods, stop, step):
        train_periods = periods[:end]
        evaluation_periods = periods[end + gap : end + gap + test_periods]
        train_df = data[data["__period"].isin(train_periods)].drop(columns="__period").copy()
        test_df = data[data["__period"].isin(evaluation_periods)].drop(columns="__period").copy()
        if train_df.empty or test_df.empty:
            continue

        returned = model_fn(train_df, test_df)
        if not isinstance(returned, dict):
            raise TypeError("model_fn must return a metrics dictionary")
        fold_metrics = dict(returned)
        fold_metrics.update(
            {
                "fold": len(results) + 1,
                "train_end": str(train_periods[-1]),
                "test_start": str(evaluation_periods[0]),
                "n_train": len(train_df),
                "n_test": len(test_df),
            }
        )
        results.append(fold_metrics)

    if results:
        metadata = {"fold", "train_end", "test_start", "n_train", "n_test"}
        for key in (candidate for candidate in results[0] if candidate not in metadata):
            values = [item[key] for item in results if isinstance(item.get(key), (int, float))]
            if values:
                print(f"{key}: {np.mean(values):.4f} ± {np.std(values):.4f}")
    return results
