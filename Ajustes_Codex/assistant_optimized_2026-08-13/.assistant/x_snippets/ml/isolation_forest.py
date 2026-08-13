"""
Isolation Forest com profiling de anomalias e MLflow.

Uso:
    from x_snippets.ml.isolation_forest import train_isolation_forest, profile_anomalies
    results = train_isolation_forest(df, feature_cols, contamination=0.01)

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import mlflow


SEED = 42


# Inline intencional: snippet autônomo (copy-pasteable). Centralizado: constants/format_br.py
def _fmt_br(n) -> str:
    """Formata inteiro no padrão BR (3.375.674)."""
    return f"{int(n):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")



def train_isolation_forest(
    df: pd.DataFrame,
    feature_cols: List[str],
    contamination: float = 0.01,
    n_estimators: int = 200,
    max_samples: str = "auto",
    scaler: str = "standard",
    log_mlflow: bool = True,
) -> Dict[str, object]:
    """Treina Isolation Forest e retorna scores de anomalia.

    Args:
        df: DataFrame com features.
        feature_cols: Colunas de features.
        contamination: Taxa esperada de anomalias (0 a 0.5).
        n_estimators: Número de árvores.
        max_samples: Amostras por árvore.
        scaler: 'standard' ou 'none'.
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Dict com scores, labels, modelo e estatísticas.
    """
    X = df[feature_cols].values

    # Escalar
    scaler_obj = None
    if scaler == "standard":
        scaler_obj = StandardScaler()
        X_scaled = scaler_obj.fit_transform(X)
    else:
        X_scaled = X

    # Treinar
    model = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        max_samples=max_samples,
        random_state=SEED,
        n_jobs=-1,
    )
    model.fit(X_scaled)

    # Scores e labels
    scores = model.decision_function(X_scaled)  # mais negativo = mais anômalo
    labels = model.predict(X_scaled)  # -1 = anomalia, 1 = normal

    n_anomalies = int((labels == -1).sum())
    pct_anomalies = n_anomalies / len(df) * 100

    stats = {
        "n_total": len(df),
        "n_anomalies": n_anomalies,
        "pct_anomalies": round(pct_anomalies, 2),
        "score_min": round(float(scores.min()), 4),
        "score_p5": round(float(np.percentile(scores, 5)), 4),
        "score_median": round(float(np.median(scores)), 4),
        "score_threshold": round(float(np.percentile(scores, contamination * 100)), 4),
    }

    print(f"Isolation Forest: {_fmt_br(n_anomalies)} anomalias detectadas ({pct_anomalies:.2f}%)")
    print(f"  Score range: [{stats['score_min']:.4f}, {float(scores.max()):.4f}]")
    print(f"  Threshold (p{contamination*100:.0f}): {stats['score_threshold']:.4f}")

    if log_mlflow:
        mlflow.log_params({"algorithm": "isolation_forest", "contamination": contamination, "n_estimators": n_estimators})
        mlflow.log_metrics({"n_anomalies": n_anomalies, "pct_anomalies": pct_anomalies})

    return {"scores": scores, "labels": labels, "model": model, "stats": stats, "scaler": scaler_obj}


def profile_anomalies(
    df: pd.DataFrame,
    feature_cols: List[str],
    scores: np.ndarray,
    labels: np.ndarray,
    top_n: int = 50,
) -> pd.DataFrame:
    """Perfila as anomalias mais extremas.

    Args:
        df: DataFrame original.
        feature_cols: Colunas de features.
        scores: Array de scores de anomalia.
        labels: Array de labels (-1/1).
        top_n: Número de anomalias a perfilar.

    Returns:
        DataFrame com profiling das top anomalias.
    """
    df_analysis = df.copy()
    df_analysis["anomaly_score"] = scores
    df_analysis["is_anomaly"] = labels == -1

    # Global stats para comparação
    global_means = df[feature_cols].mean()
    global_stds = df[feature_cols].std()

    # Top anomalias
    anomalies = df_analysis[df_analysis["is_anomaly"]].nlargest(top_n, "anomaly_score", keep="first")
    # Na verdade, queremos as mais anômalas (score mais negativo)
    anomalies = df_analysis[df_analysis["is_anomaly"]].nsmallest(top_n, "anomaly_score")

    # Para cada anomalia, qual feature mais desvia
    profiles = []
    for idx, row in anomalies.iterrows():
        deviations = {}
        for feat in feature_cols:
            if global_stds[feat] > 0:
                z = (row[feat] - global_means[feat]) / global_stds[feat]
                deviations[feat] = abs(z)

        most_anomalous_feat = max(deviations, key=deviations.get) if deviations else "N/A"
        profiles.append({
            "index": idx,
            "anomaly_score": row["anomaly_score"],
            "most_anomalous_feature": most_anomalous_feat,
            "max_z_score": round(deviations.get(most_anomalous_feat, 0), 2),
        })

    return pd.DataFrame(profiles)
