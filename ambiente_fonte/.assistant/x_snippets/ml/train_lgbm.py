"""
Wrapper para treino de LightGBM com integração MLflow.

Uso:
    from x_snippets.ml.train_lgbm import train_lightgbm_baseline
    model, metrics = train_lightgbm_baseline(X_train, y_train, X_val, y_val, task='binary')

Autor: Rodrigo via assistente
Versão: 1.0
"""

from __future__ import annotations

import lightgbm as lgb
import numpy as np
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score, mean_squared_error
from typing import Dict, Tuple, Optional, Any
try:
    import mlflow
except ImportError:
    mlflow = None


SEED = 42

DEFAULT_PARAMS_BINARY = {
    "objective": "binary",
    "metric": "auc",
    "learning_rate": 0.05,
    "num_leaves": 31,
    "max_depth": -1,
    "min_child_samples": 20,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 0.1,
    "n_estimators": 500,
    "random_state": SEED,
    "verbose": -1,
}

DEFAULT_PARAMS_REGRESSION = {
    **DEFAULT_PARAMS_BINARY,
    "objective": "regression",
    "metric": "rmse",
}

DEFAULT_PARAMS_MULTICLASS = {
    **DEFAULT_PARAMS_BINARY,
    "objective": "multiclass",
    "metric": "multi_logloss",
}


def train_lightgbm_baseline(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    task: str = "binary",
    params_override: Optional[Dict[str, Any]] = None,
    early_stopping_rounds: int = 50,
    log_mlflow: bool = True,
) -> Tuple[lgb.LGBMModel, Dict[str, float]]:
    """Treina LightGBM com defaults sensatos e early stopping.

    Args:
        X_train: Features de treino.
        y_train: Target de treino.
        X_val: Features de validação.
        y_val: Target de validação.
        task: Tipo de tarefa ('binary', 'multiclass', 'regression').
        params_override: Parâmetros para sobrescrever os defaults.
        early_stopping_rounds: Paciência do early stopping.
        log_mlflow: Se True, loga parâmetros e métricas no MLflow.

    Returns:
        Tuple de (modelo treinado, dicionário de métricas).
    """
    if early_stopping_rounds < 0:
        raise ValueError("early_stopping_rounds must be non-negative")
    # Selecionar params base
    if task == "binary":
        params = DEFAULT_PARAMS_BINARY.copy()
    elif task == "regression":
        params = DEFAULT_PARAMS_REGRESSION.copy()
    elif task == "multiclass":
        params = DEFAULT_PARAMS_MULTICLASS.copy()
        params["num_class"] = len(np.unique(y_train))
    else:
        raise ValueError(f"Task desconhecido: {task}. Use 'binary', 'multiclass' ou 'regression'.")

    if params_override:
        params.update(params_override)

    y_train = np.asarray(y_train)
    y_val = np.asarray(y_val)
    if len(y_train) == 0 or len(y_val) == 0:
        raise ValueError("training and validation sets must be non-empty")
    train_classes = np.unique(y_train)
    if task in {"binary", "multiclass"}:
        if train_classes.size < 2 or not np.isin(np.unique(y_val), train_classes).all():
            raise ValueError("validation labels must be represented in training, with at least two classes")

    # Treinar
    if task in ("binary", "multiclass"):
        model = lgb.LGBMClassifier(**params)
    else:
        model = lgb.LGBMRegressor(**params)

    callbacks = [lgb.log_evaluation(0)]
    if early_stopping_rounds:
        callbacks.insert(0, lgb.early_stopping(early_stopping_rounds))
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=callbacks,
    )

    # Métricas
    metrics = _calculate_metrics(model, X_train, y_train, X_val, y_val, task)

    # MLflow
    if log_mlflow:
        if mlflow is None:
            raise ImportError("mlflow is required when log_mlflow=True")
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

    return model, metrics


def _calculate_metrics(
    model, X_train, y_train, X_val, y_val, task: str
) -> Dict[str, float]:
    """Calcula métricas por split."""
    metrics = {}

    if task == "binary":
        y_prob_train = model.predict_proba(X_train)[:, 1]
        y_prob_val = model.predict_proba(X_val)[:, 1]
        metrics["auc_train"] = roc_auc_score(y_train, y_prob_train)
        metrics["auc_val"] = roc_auc_score(y_val, y_prob_val)
        metrics["gini_val"] = 2 * metrics["auc_val"] - 1
        metrics["overfit_gap"] = metrics["auc_train"] - metrics["auc_val"]
    elif task == "regression":
        y_pred_train = model.predict(X_train)
        y_pred_val = model.predict(X_val)
        metrics["rmse_train"] = np.sqrt(mean_squared_error(y_train, y_pred_train))
        metrics["rmse_val"] = np.sqrt(mean_squared_error(y_val, y_pred_val))
        metrics["overfit_gap"] = ((metrics["rmse_val"] - metrics["rmse_train"]) / metrics["rmse_val"]
                                  if metrics["rmse_val"] else 0.0)
    elif task == "multiclass":
        train_prob = model.predict_proba(X_train)
        val_prob = model.predict_proba(X_val)
        labels = model.classes_
        metrics["log_loss_train"] = log_loss(y_train, train_prob, labels=labels)
        metrics["log_loss_val"] = log_loss(y_val, val_prob, labels=labels)
        metrics["accuracy_val"] = accuracy_score(y_val, model.predict(X_val))
        metrics["overfit_gap"] = metrics["log_loss_val"] - metrics["log_loss_train"]

    return metrics
