"""
Wrapper Prophet com MLflow e feriados BR.

Uso:
    from x_snippets.ml.prophet_wrapper import train_prophet
    model, forecast, metrics = train_prophet(df, ds_col='dt_ref', y_col='saldo')

Autor: Rodrigo via assistente
Versão: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import mlflow


SEED = 42


def train_prophet(
    df: pd.DataFrame,
    ds_col: str = "ds",
    y_col: str = "y",
    periods: int = 12,
    freq: str = "MS",
    yearly: bool = True,
    weekly: bool = False,
    country_holidays: str = "BR",
    changepoint_prior: float = 0.05,
    log_mlflow: bool = True,
) -> Tuple:
    """Treina Prophet com configuração padrão para séries Caixa.

    Args:
        df: DataFrame com colunas ds (data) e y (valor).
        ds_col: Nome da coluna de data.
        y_col: Nome da coluna de valor.
        periods: Número de períodos a prever.
        freq: Frequência ('MS'=mensal, 'W'=semanal, 'D'=diário).
        yearly: Sazonalidade anual.
        weekly: Sazonalidade semanal.
        country_holidays: País para feriados.
        changepoint_prior: Sensibilidade a mudanças de tendência.
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Tuple (modelo, forecast DataFrame, métricas).
    """
    from prophet import Prophet

    # Preparar input
    df_prophet = df.rename(columns={ds_col: "ds", y_col: "y"})[["ds", "y"]].copy()
    df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])

    # Modelo
    model = Prophet(
        yearly_seasonality=yearly,
        weekly_seasonality=weekly,
        daily_seasonality=False,
        changepoint_prior_scale=changepoint_prior,
    )
    if country_holidays:
        model.add_country_holidays(country_name=country_holidays)

    model.fit(df_prophet)

    # Forecast
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)

    # Métricas in-sample
    merged = df_prophet.merge(forecast[["ds", "yhat"]], on="ds")
    residuals = merged["y"] - merged["yhat"]
    metrics = {
        "mape_insample": np.mean(np.abs(residuals / merged["y"])) * 100,
        "rmse_insample": np.sqrt(np.mean(residuals**2)),
        "mae_insample": np.mean(np.abs(residuals)),
    }

    if log_mlflow:
        mlflow.log_params({
            "algorithm": "prophet",
            "periods": periods,
            "freq": freq,
            "yearly": yearly,
            "changepoint_prior": changepoint_prior,
        })
        mlflow.log_metrics(metrics)

    return model, forecast, metrics
