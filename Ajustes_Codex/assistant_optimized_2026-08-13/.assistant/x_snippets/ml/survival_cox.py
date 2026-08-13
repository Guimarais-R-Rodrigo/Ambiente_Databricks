"""
Cox Proportional Hazards com lifelines e MLflow.

Uso:
    from x_snippets.ml.survival_cox import train_cox_ph, validate_proportionality
    model, metrics = train_cox_ph(df, duration_col='duration', event_col='event', feature_cols=features)

Autor: Rodrigo via assistente
Versão: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
try:
    import mlflow
except ImportError:
    mlflow = None


SEED = 42


def train_cox_ph(
    df: pd.DataFrame,
    duration_col: str,
    event_col: str,
    feature_cols: List[str],
    penalizer: float = 0.01,
    l1_ratio: float = 0.0,
    log_mlflow: bool = True,
) -> Tuple[object, Dict[str, float]]:
    """Treina modelo Cox Proportional Hazards.

    Args:
        df: DataFrame com duration, event e features.
        duration_col: Coluna de tempo até evento/censura.
        event_col: Coluna de evento (1=ocorreu, 0=censurado).
        feature_cols: Colunas de features.
        penalizer: Penalização L2 (regularização).
        l1_ratio: Proporção L1 vs L2 (0=puro L2, 1=puro L1).
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Tuple (modelo CoxPH, métricas).
    """
    from lifelines import CoxPHFitter

    if not feature_cols or len(feature_cols) != len(set(feature_cols)):
        raise ValueError("feature_cols must be a non-empty list without duplicates")
    required = {duration_col, event_col, *feature_cols}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if penalizer < 0 or not 0 <= l1_ratio <= 1:
        raise ValueError("penalizer must be non-negative and l1_ratio must be in [0, 1]")
    df_model = df[[duration_col, event_col] + feature_cols].dropna().copy()
    if df_model.empty or (df_model[duration_col] <= 0).any():
        raise ValueError("complete-case data must be non-empty with positive durations")
    if not df_model[event_col].isin([0, 1]).all() or df_model[event_col].sum() == 0:
        raise ValueError("event_col must be binary and contain at least one event")

    model = CoxPHFitter(penalizer=penalizer, l1_ratio=l1_ratio)
    model.fit(df_model, duration_col=duration_col, event_col=event_col)

    # Métricas
    metrics = {
        "c_index": model.concordance_index_,
        "log_likelihood": model.log_likelihood_,
        "aic": model.AIC_partial_,
        "n_observations": len(df_model),
        "n_events": int(df_model[event_col].sum()),
    }

    # Hazard ratios
    summary = model.summary
    print(f"\nCox PH treinado: C-index = {metrics['c_index']:.4f}")
    print(f"  N = {metrics['n_observations']}, Eventos = {metrics['n_events']}")
    print(f"\nHazard Ratios (top-10 significativos):")
    sig = summary[summary["p"] < 0.05].sort_values("exp(coef)", ascending=False).head(10)
    if len(sig) > 0:
        print(sig[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].to_string())
    else:
        print("  Nenhuma feature significativa (p < 0.05)")

    if log_mlflow:
        if mlflow is None:
            raise ImportError("mlflow is required when log_mlflow=True")
        mlflow.log_params({"algorithm": "cox_ph", "penalizer": penalizer, "l1_ratio": l1_ratio})
        mlflow.log_metrics(metrics)

    return model, metrics


def validate_proportionality(model, df, duration_col, event_col) -> pd.DataFrame:
    """Testa pressuposto de proporcionalidade (Schoenfeld).

    Args:
        model: CoxPHFitter treinado.
        df: DataFrame original.
        duration_col: Coluna de tempo.
        event_col: Coluna de evento.

    Returns:
        DataFrame com resultados do teste por feature.
    """
    from lifelines.statistics import proportional_hazard_test

    feature_cols = list(model.params_.index)
    required = {duration_col, event_col, *feature_cols}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    frame = df[[duration_col, event_col] + feature_cols].dropna().copy()
    if frame.empty:
        raise ValueError("no complete rows available for proportional-hazards test")
    result = proportional_hazard_test(model, frame, time_transform="rank")
    summary = result.summary.reset_index().rename(columns={"index": "feature"})
    summary["violates_at_0_05"] = summary["p"] < 0.05
    return summary
