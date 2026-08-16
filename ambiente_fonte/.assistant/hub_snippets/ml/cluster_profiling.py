"""
Profiling automático de clusters: estatísticas, índices e resumo.

Uso:
    from hub_snippets.ml.cluster_profiling import profile_clusters
    profiles = profile_clusters(df, feature_cols, cluster_col='cluster_id')

Autor: Rodrigo via assistente
Versão: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def profile_clusters(
    df: pd.DataFrame,
    feature_cols: List[str],
    cluster_col: str = "cluster_id",
) -> pd.DataFrame:
    """Gera profiling detalhado por cluster.

    Args:
        df: DataFrame com features e cluster_id.
        feature_cols: Colunas de features para perfilar.
        cluster_col: Nome da coluna de cluster.

    Returns:
        DataFrame com perfil por cluster (índice relativo, média, etc.).
    """
    global_means = df[feature_cols].mean()
    global_stds = df[feature_cols].std()

    profiles = []
    for cluster_id in sorted(df[cluster_col].unique()):
        cluster_df = df[df[cluster_col] == cluster_id]
        n = len(cluster_df)
        pct = n / len(df) * 100

        cluster_means = cluster_df[feature_cols].mean()
        # Índice relativo: cluster_mean / global_mean
        indices = cluster_means / global_means.replace(0, np.nan)

        for feat in feature_cols:
            profiles.append({
                "cluster": cluster_id,
                "n": n,
                "pct_total": round(pct, 1),
                "feature": feat,
                "cluster_mean": round(cluster_means[feat], 4),
                "global_mean": round(global_means[feat], 4),
                "index": round(indices[feat], 3) if pd.notna(indices[feat]) else None,
                "z_score": round((cluster_means[feat] - global_means[feat]) / global_stds[feat], 2)
                if global_stds[feat] > 0 else 0,
            })

    result = pd.DataFrame(profiles)

    # Resumo por cluster
    summary = df.groupby(cluster_col).size().reset_index(name="n")
    summary["pct"] = (summary["n"] / summary["n"].sum() * 100).round(1)
    print("\nDistribuição de clusters:")
    print(summary.to_string(index=False))

    return result


def top_differentiators(
    profiles_df: pd.DataFrame,
    cluster_id: int,
    top_n: int = 5,
) -> pd.DataFrame:
    """Retorna as features que mais diferenciam um cluster do global.

    Args:
        profiles_df: Output de profile_clusters.
        cluster_id: Cluster para analisar.
        top_n: Quantidade de features.

    Returns:
        DataFrame com top features ordenadas por abs(z_score).
    """
    cluster_data = profiles_df[profiles_df["cluster"] == cluster_id].copy()
    cluster_data["abs_z"] = cluster_data["z_score"].abs()
    return cluster_data.nlargest(top_n, "abs_z")[["feature", "cluster_mean", "global_mean", "index", "z_score"]]
