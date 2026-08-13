"""
Wrapper para treino de CatBoost com integração MLflow.

Uso:
    from x_snippets.ml.train_catboost import train_catboost_baseline
    model, metrics = train_catboost_baseline(X_train, y_train, X_val, y_val)

Autor: Rodrigo via assistente
Versão: 1.0
"""

from __future__ import annotations

from catboost import CatBoostClassifier, CatBoostRegressor
import numpy as np
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score, mean_squared_error
from typing import Dict, Tuple, Optional, List, Any
try:
    import mlflow
except ImportError:
    mlflow = None

SEED = 42


def train_catboost_baseline(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    task: str = "binary",
    cat_features: Optional[List[int]] = None,
    params_override: Optional[Dict[str, Any]] = None,
    log_mlflow: bool = True,
) -> Tuple[Any, Dict[str, float]]:
    """Treina CatBoost com defaults sensatos.

    Args:
        X_train: Features de treino.
        y_train: Target de treino.
        X_val: Features de validação.
        y_val: Target de validação.
        task: 'binary', 'multiclass' ou 'regression'.
        cat_features: Índices de features categóricas (CatBoost trata nativamente).
        params_override: Parâmetros para sobrescrever.
        log_mlflow: Se True, loga no MLflow.

    Returns:
        Tuple (modelo, métricas).
    """
    if task not in {"binary", "multiclass", "regression"}:
        raise ValueError("task must be 'binary', 'multiclass', or 'regression'")
    y_train = np.asarray(y_train)
    y_val = np.asarray(y_val)
    classes = np.unique(y_train)
    if task in {"binary", "multiclass"} and (len(classes) < 2 or not np.isin(np.unique(y_val), classes).all()):
        raise ValueError("validation labels must be represented in training, with at least two classes")
    params = {
        "iterations": 500,
        "learning_rate": 0.05,
        "depth": 6,
        "l2_leaf_reg": 3.0,
        "random_seed": SEED,
        "verbose": 0,
        "early_stopping_rounds": 50,
    }

    if params_override:
        params.update(params_override)

    if task == "binary":
        params["loss_function"] = "Logloss"
        params["eval_metric"] = "AUC"
        model = CatBoostClassifier(**params)
    elif task == "multiclass":
        params["loss_function"] = "MultiClass"
        params["eval_metric"] = "MultiClass"
        model = CatBoostClassifier(**params)
    else:
        params["loss_function"] = "RMSE"
        model = CatBoostRegressor(**params)

    model.fit(
        X_train, y_train,
        eval_set=(X_val, y_val),
        cat_features=cat_features,
        verbose=0,
    )

    metrics = {}
    if task == "binary":
        y_prob_val = model.predict_proba(X_val)[:, 1]
        metrics["auc_val"] = roc_auc_score(y_val, y_prob_val)
        metrics["gini_val"] = 2 * metrics["auc_val"] - 1
    elif task == "multiclass":
        probabilities = model.predict_proba(X_val)
        metrics["log_loss_val"] = log_loss(y_val, probabilities, labels=classes)
        metrics["accuracy_val"] = accuracy_score(y_val, np.asarray(model.predict(X_val)).reshape(-1))
    else:
        metrics["rmse_val"] = float(np.sqrt(mean_squared_error(y_val, model.predict(X_val))))

    if log_mlflow:
        if mlflow is None:
            raise ImportError("mlflow is required when log_mlflow=True")
        mlflow.log_params({"algorithm": "catboost", **{k: v for k, v in params.items() if k != "verbose"}})
        mlflow.log_metrics(metrics)

    return model, metrics
