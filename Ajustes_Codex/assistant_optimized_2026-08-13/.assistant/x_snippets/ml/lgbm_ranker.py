"""
LightGBM Ranker (LambdaRank) com métricas NDCG.

Uso:
    from x_snippets.ml.lgbm_ranker import train_lgbm_ranker, evaluate_ranking
    model, metrics = train_lgbm_ranker(X_train, y_train, groups_train, X_val, y_val, groups_val)

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
import lightgbm as lgb
from typing import Dict, List, Tuple, Optional
import mlflow


SEED = 42


def train_lgbm_ranker(
    X_train: np.ndarray,
    y_train: np.ndarray,
    groups_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    groups_val: np.ndarray,
    params: Optional[Dict] = None,
    num_boost_round: int = 500,
    early_stopping_rounds: int = 50,
    log_mlflow: bool = True,
) -> Tuple[lgb.Booster, Dict[str, float]]:
    """Treina LightGBM ranker com LambdaRank.

    Args:
        X_train: Features de treino.
        y_train: Labels de relevância (0, 1, 2, 3...).
        groups_train: Array com tamanho de cada grupo no treino.
        X_val: Features de validação.
        y_val: Labels de validação.
        groups_val: Array com tamanho de cada grupo na validação.
        params: Parâmetros do LightGBM (opcional).
        num_boost_round: Número máximo de boosting rounds.
        early_stopping_rounds: Early stopping.
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Tuple (modelo, métricas).
    """
    _validate_groups(X_train, y_train, groups_train, "train")
    _validate_groups(X_val, y_val, groups_val, "validation")
    if params is None:
        params = {
            "objective": "lambdarank",
            "metric": "ndcg",
            "ndcg_eval_at": [5, 10, 20],
            "learning_rate": 0.05,
            "num_leaves": 63,
            "min_data_in_leaf": 50,
            "feature_fraction": 0.8,
            "bagging_fraction": 0.8,
            "bagging_freq": 5,
            "verbose": -1,
            "seed": SEED,
        }

    train_data = lgb.Dataset(X_train, label=y_train, group=groups_train)
    val_data = lgb.Dataset(X_val, label=y_val, group=groups_val, reference=train_data)

    model = lgb.train(
        params,
        train_data,
        num_boost_round=num_boost_round,
        valid_sets=[val_data],
        callbacks=[lgb.early_stopping(early_stopping_rounds), lgb.log_evaluation(50)],
    )

    # Avaliar
    metrics = evaluate_ranking(model, X_val, y_val, groups_val)

    if log_mlflow:
        mlflow.log_params({k: v for k, v in params.items() if k != "verbose"})
        mlflow.log_metrics(metrics)

    return model, metrics


def evaluate_ranking(
    model: lgb.Booster,
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    ks: Optional[List[int]] = None,
) -> Dict[str, float]:
    """Calcula NDCG@k e MAP@k por grupo.

    Args:
        model: Modelo LightGBM treinado.
        X: Features.
        y: Labels de relevância.
        groups: Tamanho dos grupos.
        ks: Valores de k para métricas.

    Returns:
        Dict com NDCG@k e MAP@k.
    """
    _validate_groups(X, y, groups, "evaluation")
    ks = [5, 10, 20] if ks is None else list(ks)
    if not ks or any(k <= 0 for k in ks):
        raise ValueError("ks must contain positive integers")
    scores = model.predict(X)

    metrics = {}
    offset = 0
    ndcgs = {k: [] for k in ks}

    for group_size in groups:
        group_scores = scores[offset:offset + group_size]
        group_labels = y[offset:offset + group_size]

        # Ordenar por score previsto
        ranked_idx = np.argsort(-group_scores)
        ranked_labels = group_labels[ranked_idx]

        for k in ks:
            ndcg = _ndcg_at_k(ranked_labels, k)
            ndcgs[k].append(ndcg)

        offset += group_size

    for k in ks:
        metrics[f"ndcg_at_{k}"] = np.mean(ndcgs[k])

    print("Ranking metrics: " + ", ".join(f"{name}={value:.4f}" for name, value in metrics.items()))
    return metrics


def _validate_groups(X: np.ndarray, y: np.ndarray, groups: np.ndarray, label: str) -> None:
    groups = np.asarray(groups)
    if len(X) != len(y) or len(y) == 0:
        raise ValueError(f"{label}: X and y must have the same non-zero row count")
    if groups.ndim != 1 or len(groups) == 0 or not np.issubdtype(groups.dtype, np.integer):
        raise ValueError(f"{label}: groups must be a non-empty integer vector of group sizes")
    if (groups <= 0).any() or int(groups.sum()) != len(y):
        raise ValueError(f"{label}: group sizes must be positive and sum to len(y)")
    if (np.asarray(y) < 0).any():
        raise ValueError(f"{label}: relevance labels must be non-negative")


def _ndcg_at_k(ranked_labels: np.ndarray, k: int) -> float:
    """Calcula NDCG@k para um grupo."""
    dcg = sum((2**ranked_labels[i] - 1) / np.log2(i + 2) for i in range(min(k, len(ranked_labels))))
    ideal = sorted(ranked_labels, reverse=True)
    idcg = sum((2**ideal[i] - 1) / np.log2(i + 2) for i in range(min(k, len(ideal))))
    return dcg / idcg if idcg > 0 else 0.0
