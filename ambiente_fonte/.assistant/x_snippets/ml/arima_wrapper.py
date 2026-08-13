"""
Wrapper auto-ARIMA com diagnóstico e MLflow.

Uso:
    from x_snippets.ml.arima_wrapper import train_arima
    model, forecast, metrics = train_arima(series, m=12, forecast_periods=6)

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
import mlflow


SEED = 42


def train_arima(
    series: np.ndarray,
    m: int = 12,
    forecast_periods: int = 6,
    seasonal: bool = True,
    log_mlflow: bool = True,
) -> Tuple:
    """Treina auto-ARIMA com seleção automática de ordem.

    Args:
        series: Array da série temporal (ordenada cronologicamente).
        m: Período sazonal (12=mensal, 4=trimestral, 7=diário-semanal).
        forecast_periods: Períodos a prever.
        seasonal: Se True, inclui componente sazonal (SARIMA).
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Tuple (modelo pmdarima, forecast array, métricas).
    """
    import pmdarima as pm

    model = pm.auto_arima(
        series,
        seasonal=seasonal,
        m=m,
        stepwise=True,
        suppress_warnings=True,
        error_action="ignore",
        random_state=SEED,
        n_fits=50,
    )

    # Forecast
    forecast, conf_int = model.predict(n_periods=forecast_periods, return_conf_int=True)

    # Métricas in-sample (residuais)
    residuals = model.resid()
    fitted = series - residuals

    mask = series != 0
    metrics = {
        "aic": model.aic(),
        "bic": model.bic(),
        "order": str(model.order),
        "seasonal_order": str(model.seasonal_order),
        "rmse_insample": np.sqrt(np.mean(residuals**2)),
        "mape_insample": np.mean(np.abs(residuals[mask] / series[mask])) * 100,
    }

    if log_mlflow:
        mlflow.log_params({
            "algorithm": "arima",
            "order": str(model.order),
            "seasonal_order": str(model.seasonal_order),
            "m": m,
        })
        mlflow.log_metrics({k: v for k, v in metrics.items() if isinstance(v, (int, float))})

    return model, forecast, metrics
