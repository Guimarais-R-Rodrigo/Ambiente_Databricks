"""
Integração Optuna + LightGBM para otimização de hiperparâmetros.

Uso:
    from x_snippets.ml.optuna_lgbm import optimize_lgbm
    best_params, study = optimize_lgbm(X_train, y_train, X_val, y_val, n_trials=50)

Autor: Rodrigo via assistente
Versão: 1.0
"""

import optuna
import lightgbm as lgb
import numpy as np
from sklearn.metrics import log_loss, roc_auc_score, mean_squared_error
from typing import Dict, Tuple, Optional

SEED = 42


def optimize_lgbm(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    task: str = "binary",
    n_trials: int = 50,
    metric: str = "auc",
    timeout: Optional[int] = None,
) -> Tuple[Dict, optuna.Study]:
    """Otimiza hiperparâmetros do LightGBM via Optuna.

    Args:
        X_train: Features de treino.
        y_train: Target de treino.
        X_val: Features de validação.
        y_val: Target de validação.
        task: 'binary', 'multiclass' ou 'regression'.
        n_trials: Número de trials Optuna.
        metric: Métrica a otimizar ('auc', 'rmse').
        timeout: Timeout em segundos (None = sem limite).

    Returns:
        Tuple de (melhores parâmetros, study Optuna).
    """
    if task not in {"binary", "multiclass", "regression"}:
        raise ValueError("task must be 'binary', 'multiclass', or 'regression'")
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")
    train_classes = np.unique(y_train)
    if task in {"binary", "multiclass"} and (len(train_classes) < 2 or not np.isin(np.unique(y_val), train_classes).all()):
        raise ValueError("validation labels must be represented in training, with at least two classes")
    effective_metric = ("multi_logloss" if task == "multiclass" else "rmse" if task == "regression" else metric)
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    def objective(trial: 'optuna.trial.Trial') -> float:
        params = {
            "objective": _get_objective(task),
            "metric": effective_metric,
            "verbosity": -1,
            "random_state": SEED,
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 15, 127),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
            "n_estimators": 500,
        }
        if task == "multiclass":
            params["num_class"] = len(train_classes)

        if task in ("binary", "multiclass"):
            model = lgb.LGBMClassifier(**params)
        else:
            model = lgb.LGBMRegressor(**params)

        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)],
        )

        if task == "binary":
            y_prob = model.predict_proba(X_val)[:, 1]
            return roc_auc_score(y_val, y_prob)
        elif task == "regression":
            y_pred = model.predict(X_val)
            return -np.sqrt(mean_squared_error(y_val, y_pred))  # Negativo porque Optuna maximiza
        probabilities = model.predict_proba(X_val)
        return -log_loss(y_val, probabilities, labels=model.classes_)

    direction = "maximize" if task != "regression" else "maximize"
    study = optuna.create_study(direction=direction, sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=n_trials, timeout=timeout)

    return study.best_params, study


def _get_objective(task: str) -> str:
    if task == "binary":
        return "binary"
    elif task == "multiclass":
        return "multiclass"
    if task == "regression":
        return "regression"
    raise ValueError("task must be 'binary', 'multiclass', or 'regression'")
