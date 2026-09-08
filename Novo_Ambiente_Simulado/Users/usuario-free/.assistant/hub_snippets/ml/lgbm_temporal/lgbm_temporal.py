"""
LightGBM para séries temporais com lag/rolling features automáticas.

Uso:
    from hub_snippets.ml.lgbm_temporal import create_temporal_features, train_lgbm_temporal
    df_feat = create_temporal_features(df, target_col='saldo', date_col='dt_ref')

Autor: Rodrigo via assistente
Versão: 1.0
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Sequence


SEED = 42


def create_temporal_features(
    df: pd.DataFrame,
    target_col: str,
    date_col: str,
    lags: Optional[List[int]] = None,
    rolling_windows: Optional[List[int]] = None,
    calendar_features: bool = True,
    entity_cols: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """Gera features temporais (lags, rolling, calendar) automaticamente.

    Args:
        df: DataFrame com coluna de data e target.
        target_col: Coluna do target.
        date_col: Coluna de data.
        lags: Lista de lags a criar (default: [1,2,3,6,12]).
        rolling_windows: Janelas de rolling stats (default: [3,6,12]).
        calendar_features: Se True, adiciona mês, trimestre, dia da semana.

    Returns:
        DataFrame com features adicionadas.
    """
    required = {target_col, date_col, *(entity_cols or [])}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    sort_cols = [*(entity_cols or []), date_col]
    df = df.sort_values(sort_cols).copy()

    if lags is None:
        lags = [1, 2, 3, 6, 12]
    if rolling_windows is None:
        rolling_windows = [3, 6, 12]

    groups = df.groupby(list(entity_cols), sort=False)[target_col] if entity_cols else None
    generated_required: list[str] = []

    # Lag features, always isolated by entity when entity columns are provided.
    for lag in lags:
        if lag <= 0:
            raise ValueError("lags must contain positive integers")
        name = f"lag_{lag}"
        df[name] = groups.shift(lag) if groups is not None else df[target_col].shift(lag)
        generated_required.append(name)

    # Rolling features
    for w in rolling_windows:
        if isinstance(w, bool) or not isinstance(w, int) or w < 2:
            raise ValueError("rolling_windows must contain integers >= 2 for sample std")
        names = [f"rolling_{stat}_{w}" for stat in ("mean", "std", "min", "max")]
        generated_required.extend(names)
        if groups is None:
            shifted = df[target_col].shift(1)
            df[f"rolling_mean_{w}"] = shifted.rolling(w).mean()
            df[f"rolling_std_{w}"] = shifted.rolling(w).std()
            df[f"rolling_min_{w}"] = shifted.rolling(w).min()
            df[f"rolling_max_{w}"] = shifted.rolling(w).max()
        else:
            shifted = groups.shift(1)
            regrouped = shifted.groupby([df[column] for column in entity_cols], sort=False)
            df[f"rolling_mean_{w}"] = regrouped.transform(lambda series: series.rolling(w).mean())
            df[f"rolling_std_{w}"] = regrouped.transform(lambda series: series.rolling(w).std())
            df[f"rolling_min_{w}"] = regrouped.transform(lambda series: series.rolling(w).min())
            df[f"rolling_max_{w}"] = regrouped.transform(lambda series: series.rolling(w).max())

    # Calendar features
    if calendar_features:
        dt = pd.to_datetime(df[date_col])
        df["month"] = dt.dt.month
        df["quarter"] = dt.dt.quarter
        df["day_of_week"] = dt.dt.dayofweek
        df["day_of_year"] = dt.dt.dayofyear
        df["is_month_start"] = dt.dt.is_month_start.astype(int)
        df["is_month_end"] = dt.dt.is_month_end.astype(int)

    # Trend
    df["trend"] = df.groupby(list(entity_cols), sort=False).cumcount() if entity_cols else range(len(df))

    # Remova somente warm-up criado por este helper. Missing preexistente em
    # coluna alheia pertence à política de imputação do pipeline consumidor.
    n_before = len(df)
    if generated_required:
        df = df.dropna(subset=generated_required).reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)
    print(f"Features temporais: {n_before - len(df)} linhas removidas por warm-up das features geradas")

    return df
