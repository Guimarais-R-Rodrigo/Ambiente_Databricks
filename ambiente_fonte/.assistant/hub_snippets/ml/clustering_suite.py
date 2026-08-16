"""
Suite completa de clustering: escalonamento, seleção de k, treino e métricas.

Uso:
    from hub_snippets.ml.clustering_suite import run_clustering_pipeline
    results = run_clustering_pipeline(df, features_cols, k_range=range(2,11))

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import mlflow


SEED = 42


# Inline intencional: snippet autônomo (copy-pasteable). Centralizado: constants/format_br.py
def _fmt_br(n) -> str:
    """Formata inteiro no padrão BR (3.375.674)."""
    return f"{int(n):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")



def select_k(
    X_scaled: np.ndarray,
    k_range: range = range(2, 11),
    method: str = "both",
) -> Dict[str, object]:
    """Avalia múltiplos k e retorna métricas para seleção.

    Args:
        X_scaled: Dados já escalados.
        k_range: Range de k a avaliar.
        method: 'elbow', 'silhouette' ou 'both'.

    Returns:
        Dict com scores por k e k recomendado.
    """
    if method not in {"elbow", "silhouette", "both"}:
        raise ValueError("method must be 'elbow', 'silhouette', or 'both'")
    candidates = list(k_range)
    if not candidates or any(k < 2 or k >= len(X_scaled) for k in candidates):
        raise ValueError("k_range must contain values from 2 through n_samples - 1")
    results = {"k": [], "inertia": [], "silhouette": [], "calinski": [], "davies_bouldin": []}

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=SEED, n_init=10)
        labels = km.fit_predict(X_scaled)

        results["k"].append(k)
        results["inertia"].append(km.inertia_)
        results["silhouette"].append(silhouette_score(X_scaled, labels))
        results["calinski"].append(calinski_harabasz_score(X_scaled, labels))
        results["davies_bouldin"].append(davies_bouldin_score(X_scaled, labels))

    # Recomendação: k com maior silhouette
    if method == "elbow" and len(candidates) >= 3:
        best_idx = int(np.argmax(np.diff(results["inertia"], n=2))) + 1
    else:
        best_idx = int(np.argmax(results["silhouette"]))
    best_k = results["k"][best_idx]

    print(f"Seleção de k:")
    print(f"  Melhor silhouette: k={best_k} (score={results['silhouette'][best_idx]:.4f})")
    print(f"  Melhor Calinski-Harabasz: k={results['k'][np.argmax(results['calinski'])]}")
    print(f"  Melhor Davies-Bouldin: k={results['k'][np.argmin(results['davies_bouldin'])]}")

    return {"scores": pd.DataFrame(results), "best_k": best_k}


def run_clustering_pipeline(
    df: pd.DataFrame,
    feature_cols: List[str],
    k: Optional[int] = None,
    k_range: range = range(2, 11),
    algorithm: str = "kmeans",
    scaler: str = "standard",
    log_mlflow: bool = True,
) -> Dict[str, object]:
    """Pipeline completo de clustering.

    Args:
        df: DataFrame com features.
        feature_cols: Colunas de features.
        k: Número de clusters (se None, seleciona automaticamente).
        k_range: Range para seleção automática de k.
        algorithm: 'kmeans', 'gmm' ou 'dbscan'.
        scaler: 'standard' ou 'robust'.
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Dict com labels, métricas, modelo e scaler.
    """
    if algorithm not in {"kmeans", "gmm", "dbscan"}:
        raise ValueError("algorithm must be 'kmeans', 'gmm', or 'dbscan'")
    if scaler not in {"standard", "robust"}:
        raise ValueError("scaler must be 'standard' or 'robust'")
    missing = set(feature_cols) - set(df.columns)
    if not feature_cols or missing:
        raise ValueError(f"feature_cols is empty or missing columns: {sorted(missing)}")
    X = df[feature_cols].values
    if len(X) < 3 or not np.isfinite(X).all():
        raise ValueError("clustering requires at least 3 rows with finite feature values")

    # Escalar
    scaler_obj = StandardScaler() if scaler == "standard" else RobustScaler()
    X_scaled = scaler_obj.fit_transform(X)

    # Selecionar k se necessário
    if k is None and algorithm != "dbscan":
        selection = select_k(X_scaled, k_range)
        k = selection["best_k"]

    # Treinar
    if algorithm == "kmeans":
        model = KMeans(n_clusters=k, random_state=SEED, n_init=10)
        labels = model.fit_predict(X_scaled)
    elif algorithm == "gmm":
        model = GaussianMixture(n_components=k, random_state=SEED)
        labels = model.fit_predict(X_scaled)
    elif algorithm == "dbscan":
        model = DBSCAN(eps=0.5, min_samples=5)
        labels = model.fit_predict(X_scaled)
        k = len(set(labels)) - (1 if -1 in labels else 0)

    # Métricas
    mask = labels >= 0  # excluir noise do DBSCAN
    metrics = {}
    if mask.sum() > 1 and len(set(labels[mask])) > 1:
        metrics["silhouette"] = silhouette_score(X_scaled[mask], labels[mask])
        metrics["calinski_harabasz"] = calinski_harabasz_score(X_scaled[mask], labels[mask])
        metrics["davies_bouldin"] = davies_bouldin_score(X_scaled[mask], labels[mask])

    metrics["n_clusters"] = k
    metrics["n_noise"] = int((labels == -1).sum())

    if log_mlflow:
        mlflow.log_params({"algorithm": algorithm, "n_clusters": k, "scaler": scaler})
        mlflow.log_metrics(metrics)

    silhouette = metrics.get("silhouette")
    silhouette_text = f"{silhouette:.4f}" if silhouette is not None else "N/A"
    print(f"Clustering concluído: {k} clusters, silhouette={silhouette_text}")

    return {"labels": labels, "metrics": metrics, "model": model, "scaler": scaler_obj, "X_scaled": X_scaled}
