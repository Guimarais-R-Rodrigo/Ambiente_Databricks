"""Split temporal por período de calendário, e não por posição de linha, contra vazamento."""

from __future__ import annotations

from typing import Optional, Tuple

import pandas as pd


def temporal_split(
    df: pd.DataFrame,
    date_col: str,
    train_pct: float = 0.70,
    val_pct: float = 0.15,
    gap_periods: int = 1,
    period_unit: str = "M",
    *,
    group_col: Optional[str] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split complete calendar periods and leave explicit gaps between partitions.

    ``group_col`` enables a conservative entity-disjoint split: validation rows
    whose entity appeared in training and test rows whose entity appeared earlier
    are removed. Omit it for genuine panel/time-series forecasting where history
    from the same entity is intentional.
    """
    required = {date_col} | ({group_col} if group_col else set())
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if not 0 < train_pct < 1 or not 0 < val_pct < 1 or train_pct + val_pct >= 1:
        raise ValueError("train_pct and val_pct must be positive and sum to less than 1")
    if gap_periods < 0:
        raise ValueError("gap_periods must be non-negative")

    result = df.copy()
    result[date_col] = pd.to_datetime(result[date_col], errors="raise")
    result["__period"] = result[date_col].dt.to_period(period_unit)
    periods = sorted(result["__period"].dropna().unique())
    required_periods = 3 + 2 * gap_periods
    if len(periods) < required_periods:
        raise ValueError(f"at least {required_periods} periods are required")

    train_count = max(1, int(len(periods) * train_pct))
    val_count = max(1, int(len(periods) * val_pct))
    val_start = train_count + gap_periods
    val_end = val_start + val_count
    test_start = val_end + gap_periods
    if test_start >= len(periods):
        raise ValueError("split percentages plus gaps leave no test period")

    train = result[result["__period"].isin(periods[:train_count])].copy()
    val = result[result["__period"].isin(periods[val_start:val_end])].copy()
    test = result[result["__period"].isin(periods[test_start:])].copy()

    if group_col:
        train_groups = set(train[group_col].dropna())
        val = val[~val[group_col].isin(train_groups)].copy()
        earlier_groups = train_groups | set(val[group_col].dropna())
        test = test[~test[group_col].isin(earlier_groups)].copy()
        if val.empty or test.empty:
            raise ValueError("entity-disjoint filtering produced an empty validation or test set")

    return tuple(frame.drop(columns="__period").sort_values(date_col).reset_index(drop=True) for frame in (train, val, test))
