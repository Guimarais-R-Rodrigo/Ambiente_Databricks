"""
Wrapper TabNet com MLflow e atenção exportável.

Uso:
    from hub_snippets.ml.tabnet_wrapper import train_tabnet
    model, metrics, importance = train_tabnet(X_train, y_train, X_val, y_val)

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
try:
    import mlflow
except ImportError:
    mlflow = None


SEED = 42


def train_tabnet(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    task: str = "binary",
    cat_idxs: Optional[List[int]] = None,
    cat_dims: Optional[List[int]] = None,
    n_d: int = 32,
    n_a: int = 32,
    n_steps: int = 5,
    max_epochs: int = 100,
    patience: int = 15,
    batch_size: int = 1024,
    log_mlflow: bool = True,
) -> Tuple[object, Dict[str, float], np.ndarray]:
    """Treina TabNet com configuração padrão.

    Args:
        X_train: Features de treino.
        y_train: Target de treino.
        X_val: Features de validação.
        y_val: Target de validação.
        task: 'binary' ou 'regression'.
        cat_idxs: Índices de features categóricas.
        cat_dims: Cardinalidade de cada feature categórica.
        n_d: Dimensão do decision step.
        n_a: Dimensão do attention step.
        n_steps: Número de steps.
        max_epochs: Máximo de epochs.
        patience: Paciência do early stopping.
        batch_size: Tamanho do batch.
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Tuple (modelo, métricas, feature_importances).
    """
    if task not in {"binary", "regression"}:
        raise ValueError("task must be 'binary' or 'regression'")
    X_train = np.asarray(X_train)
    X_val = np.asarray(X_val)
    y_train = np.asarray(y_train).reshape(-1)
    y_val = np.asarray(y_val).reshape(-1)
    if X_train.ndim != 2 or X_val.ndim != 2 or X_train.shape[1] != X_val.shape[1]:
        raise ValueError("X_train and X_val must be 2-D with matching feature counts")
    if len(X_train) != len(y_train) or len(X_val) != len(y_val) or len(y_train) == 0 or len(y_val) == 0:
        raise ValueError("features and labels must be aligned and non-empty")
    categorical_indexes = [] if cat_idxs is None else [int(value) for value in cat_idxs]
    categorical_dimensions = [] if cat_dims is None else [int(value) for value in cat_dims]
    if len(categorical_indexes) != len(categorical_dimensions):
        raise ValueError("cat_idxs and cat_dims must have the same length")
    if any(index < 0 or index >= X_train.shape[1] for index in categorical_indexes) or any(value <= 0 for value in categorical_dimensions):
        raise ValueError("categorical indexes/dimensions are invalid")
    if task == "binary" and (not np.isin(y_train, [0, 1]).all() or np.unique(y_train).size != 2 or not np.isin(y_val, [0, 1]).all()):
        raise ValueError("binary TabNet requires 0/1 labels and both classes in training")
    if max_epochs <= 0 or patience <= 0 or batch_size <= 1:
        raise ValueError("max_epochs/patience must be positive and batch_size > 1")
    import torch
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    if task == "binary":
        from pytorch_tabnet.tab_model import TabNetClassifier
        model = TabNetClassifier(
            n_d=n_d, n_a=n_a, n_steps=n_steps,
            gamma=1.5, lambda_sparse=1e-4,
            cat_idxs=categorical_indexes,
            cat_dims=categorical_dimensions,
            optimizer_fn=torch.optim.Adam,
            optimizer_params=dict(lr=2e-2),
            scheduler_params={"step_size": 10, "gamma": 0.9},
            scheduler_fn=torch.optim.lr_scheduler.StepLR,
            mask_type="sparsemax",
            seed=SEED,
            verbose=0,
        )
        eval_metric = ["auc"]
    else:
        from pytorch_tabnet.tab_model import TabNetRegressor
        model = TabNetRegressor(
            n_d=n_d, n_a=n_a, n_steps=n_steps,
            cat_idxs=categorical_indexes,
            cat_dims=categorical_dimensions,
            seed=SEED, verbose=0,
        )
        eval_metric = ["rmse"]

    model.fit(
        X_train, y_train.reshape(-1, 1) if task == "regression" else y_train,
        eval_set=[(X_val, y_val.reshape(-1, 1) if task == "regression" else y_val)],
        eval_metric=eval_metric,
        max_epochs=max_epochs,
        patience=patience,
        batch_size=batch_size,
    )

    # Métricas
    from sklearn.metrics import roc_auc_score, mean_squared_error
    metrics = {}
    if task == "binary":
        y_prob = model.predict_proba(X_val)[:, 1]
        metrics["auc_val"] = roc_auc_score(y_val, y_prob)
        metrics["gini_val"] = 2 * metrics["auc_val"] - 1
    else:
        y_pred = model.predict(X_val).flatten()
        metrics["rmse_val"] = np.sqrt(mean_squared_error(y_val, y_pred))

    # Feature importance (attention-based)
    importance = model.feature_importances_

    if log_mlflow:
        if mlflow is None:
            raise ImportError("mlflow is required when log_mlflow=True")
        mlflow.log_params({"algorithm": "tabnet", "n_d": n_d, "n_a": n_a, "n_steps": n_steps})
        mlflow.log_metrics(metrics)

    return model, metrics, importance
