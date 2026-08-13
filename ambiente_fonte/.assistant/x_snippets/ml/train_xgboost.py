"""
Wrapper para treino de XGBoost com integração MLflow.

Uso:
    from x_snippets.ml.train_xgboost import train_xgboost_baseline
    model, metrics = train_xgboost_baseline(X_train, y_train, X_val, y_val)

Autor: Rodrigo via assistente
Versão: 1.0
"""

from __future__ import annotations

import xgboost as xgb
import numpy as np
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score, mean_squared_error
from typing import Dict, Tuple, Optional, Any
try:
    import mlflow
except ImportError:  # Optional unless logging is requested.
    mlflow = None

SEED = 42

DEFAULT_PARAMS = {
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "learning_rate": 0.05,
    "max_depth": 6,
    "min_child_weight": 5,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "n_estimators": 500,
    "random_state": SEED,
    "verbosity": 0,
    "use_label_encoder": False,
}


def train_xgboost_baseline(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    task: str = "binary",
    params_override: Optional[Dict[str, Any]] = None,
    early_stopping_rounds: int = 50,
    log_mlflow: bool = True,
) -> Tuple[xgb.XGBModel, Dict[str, float]]:
    """Treina XGBoost com defaults sensatos e early stopping.

    Args:
        X_train: Features de treino.
        y_train: Target de treino.
        X_val: Features de validação.
        y_val: Target de validação.
        task: 'binary', 'multiclass' ou 'regression'.
        params_override: Parâmetros para sobrescrever.
        early_stopping_rounds: Paciência.
        log_mlflow: Se True, loga no MLflow.

    Returns:
        Tuple (modelo, métricas).
    """
    if task not in {"binary", "multiclass", "regression"}:
        raise ValueError("task must be 'binary', 'multiclass', or 'regression'")
    if early_stopping_rounds < 0:
        raise ValueError("early_stopping_rounds must be non-negative")
    y_train = np.asarray(y_train)
    y_val = np.asarray(y_val)
    if len(y_train) == 0 or len(y_val) == 0:
        raise ValueError("training and validation sets must be non-empty")
    params = DEFAULT_PARAMS.copy()
    if task == "regression":
        params["objective"] = "reg:squarederror"
        params["eval_metric"] = "rmse"
    elif task == "multiclass":
        params["objective"] = "multi:softprob"
        params["eval_metric"] = "mlogloss"
        classes = np.unique(y_train)
        if len(classes) < 2 or not np.isin(np.unique(y_val), classes).all():
            raise ValueError("multiclass validation labels must be represented in training")
        params["num_class"] = len(classes)
    elif np.unique(y_train).size < 2 or np.unique(y_val).size < 2:
        raise ValueError("binary training and validation sets must contain both classes")

    if params_override:
        params.update(params_override)
    if early_stopping_rounds:
        params["early_stopping_rounds"] = early_stopping_rounds

    if task in ("binary", "multiclass"):
        model = xgb.XGBClassifier(**params)
    else:
        model = xgb.XGBRegressor(**params)

    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False,
    )

    # Métricas
    metrics = {}
    if task == "binary":
        y_prob_val = model.predict_proba(X_val)[:, 1]
        metrics["auc_val"] = roc_auc_score(y_val, y_prob_val)
        metrics["gini_val"] = 2 * metrics["auc_val"] - 1
    elif task == "multiclass":
        probabilities = model.predict_proba(X_val)
        metrics["log_loss_val"] = log_loss(y_val, probabilities, labels=model.classes_)
        metrics["accuracy_val"] = accuracy_score(y_val, model.predict(X_val))
    else:
        metrics["rmse_val"] = float(np.sqrt(mean_squared_error(y_val, model.predict(X_val))))

    if log_mlflow:
        if mlflow is None:
            raise ImportError("mlflow is required when log_mlflow=True")
        mlflow.log_params({"algorithm": "xgboost", **params})
        mlflow.log_metrics(metrics)

    return model, metrics
