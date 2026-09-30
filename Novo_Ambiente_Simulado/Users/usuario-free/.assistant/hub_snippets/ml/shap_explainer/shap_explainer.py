"""
SHAP explainer unificado: TreeSHAP, cálculo e geração de plots padrão.

Uso:
    from hub_snippets.ml.shap_explainer import compute_shap, plot_shap_global, plot_shap_local

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple


SEED = 42


def compute_shap(
    model,
    X: np.ndarray,
    feature_names: List[str],
    model_type: str = "tree",
    max_samples: int = 5000,
    *,
    task: str = "classification",
    output_index: Optional[int] = None,
    background: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, float]:
    """Calcula SHAP values para o modelo.

    Args:
        model: Modelo treinado (LightGBM, XGBoost, sklearn, etc.).
        X: Features para explicar (array ou DataFrame).
        feature_names: Nomes das features.
        model_type: 'tree' (TreeSHAP), 'linear', 'kernel' (model-agnostic).
        max_samples: Máximo de amostras para KernelSHAP.
        background: Referência explícita para model_type='linear'; None preserva X.

    Returns:
        Tuple (shap_values array, base_value float).
    """
    import shap

    if background is not None:
        if model_type != "linear":
            raise ValueError("background is supported only for linear models")
        reference = np.asarray(background)
        features = np.asarray(X)
        if (reference.ndim != 2 or features.ndim != 2 or not reference.shape[0]
                or reference.shape[1] != features.shape[1]):
            raise ValueError("background must be a nonempty 2D array with X column count")
        try:
            if not np.isfinite(reference.astype(float)).all():
                raise ValueError("background must contain only finite numeric values")
        except (TypeError, OverflowError) as exc:
            raise ValueError("background must contain only finite numeric values") from exc
    if task not in {"classification", "regression"}:
        raise ValueError("task must be 'classification' or 'regression'")
    if len(feature_names) != np.asarray(X).shape[1]:
        raise ValueError("feature_names length must match X columns")
    if max_samples <= 0:
        raise ValueError("max_samples must be positive")

    def select_output(values: Any, base: Any, n_rows: int, n_features: int) -> tuple[np.ndarray, float]:
        if hasattr(values, "values"):
            explanation = values
            base = explanation.base_values
            values = explanation.values
        if isinstance(values, list):
            if output_index is None:
                raise ValueError("multi-output SHAP result requires output_index (for example, the positive class index)")
            if not 0 <= output_index < len(values):
                raise ValueError("output_index is outside the available outputs")
            selected = np.asarray(values[output_index])
            base_array = np.asarray(base)
            selected_base = base_array[output_index] if base_array.ndim else base_array
        else:
            array = np.asarray(values)
            if array.ndim == 2:
                selected = array
                selected_base = base
            elif array.ndim == 3:
                if output_index is None:
                    raise ValueError("3D/multi-output SHAP result requires output_index")
                if array.shape[:2] == (n_rows, n_features):
                    if not 0 <= output_index < array.shape[2]:
                        raise ValueError("output_index is outside the available outputs")
                    selected = array[:, :, output_index]
                elif array.shape[1:] == (n_rows, n_features):
                    if not 0 <= output_index < array.shape[0]:
                        raise ValueError("output_index is outside the available outputs")
                    selected = array[output_index]
                else:
                    raise ValueError(f"unrecognized SHAP tensor shape: {array.shape}")
                base_array = np.asarray(base)
                if base_array.ndim == 0:
                    selected_base = base_array
                elif base_array.ndim == 1:
                    selected_base = base_array[output_index]
                elif base_array.shape[-1] > output_index:
                    selected_base = base_array[..., output_index]
                else:
                    raise ValueError(f"unrecognized SHAP base-value shape: {base_array.shape}")
            else:
                raise ValueError(f"SHAP values must be 2D or multi-output 3D, received {array.shape}")
        if selected.shape != (n_rows, n_features):
            raise ValueError(f"selected SHAP output has shape {selected.shape}; expected {(n_rows, n_features)}")
        base_array = np.asarray(selected_base, dtype=float)
        if base_array.size == 0 or not np.isfinite(base_array).all():
            raise ValueError("SHAP base value must be finite")
        if base_array.size > 1 and not np.allclose(base_array, base_array.flat[0]):
            raise ValueError("per-row SHAP base values vary; this API requires a constant base value")
        return selected.astype(float), float(base_array.flat[0])

    if model_type == "tree":
        explainer = shap.TreeExplainer(model)
        raw_values = explainer.shap_values(X)
        shap_values, base_value = select_output(raw_values, explainer.expected_value, len(X), len(feature_names))
    elif model_type == "linear":
        explainer = shap.LinearExplainer(model, X if background is None else background)
        raw_values = explainer.shap_values(X)
        shap_values, base_value = select_output(raw_values, explainer.expected_value, len(X), len(feature_names))
    elif model_type == "kernel":
        # Subsample para performance
        if len(X) > max_samples:
            idx = np.random.RandomState(SEED).choice(len(X), max_samples, replace=False)
            X_sample = X.iloc[idx] if hasattr(X, "iloc") else X[idx]
        else:
            X_sample = X
        predictor = model.predict_proba if task == "classification" else model.predict
        background = X_sample.iloc[:100] if hasattr(X_sample, "iloc") else X_sample[:100]
        explainer = shap.KernelExplainer(predictor, background)
        raw_values = explainer.shap_values(X_sample)
        shap_values, base_value = select_output(raw_values, explainer.expected_value, len(X_sample), len(feature_names))
    else:
        raise ValueError(f"model_type deve ser 'tree', 'linear' ou 'kernel'. Recebido: {model_type}")

    print(f"SHAP calculado: {shap_values.shape[0]} observações × {shap_values.shape[1]} features")
    print(f"  Base value (E[f(x)]): {base_value:.4f}")
    print(f"  Mean |SHAP| top-5: {pd.Series(np.abs(shap_values).mean(0), index=feature_names).nlargest(5).to_dict()}")

    return shap_values, base_value


def get_feature_importance_shap(
    shap_values: np.ndarray,
    feature_names: List[str],
    top_n: int = 20,
) -> pd.DataFrame:
    """Retorna ranking de importância baseado em mean |SHAP|.

    Args:
        shap_values: Array de SHAP values.
        feature_names: Nomes das features.
        top_n: Número de features a retornar.

    Returns:
        DataFrame com ranking de importância.
    """
    shap_values = np.asarray(shap_values)
    if shap_values.ndim != 2 or shap_values.shape[1] != len(feature_names):
        raise ValueError("select one output/class so shap_values has shape (rows, features)")
    importance = np.abs(shap_values).mean(axis=0)
    total = importance.sum()
    if not np.isfinite(total) or total <= 0:
        raise ValueError("SHAP importance total must be positive and finite")

    df = pd.DataFrame({
        "feature": feature_names,
        "mean_abs_shap": importance,
        "pct_importance": importance / total * 100,
    }).sort_values("mean_abs_shap", ascending=False).head(top_n).reset_index(drop=True)

    df["rank"] = range(1, len(df) + 1)
    df["cumulative_pct"] = df["pct_importance"].cumsum()

    return df[["rank", "feature", "mean_abs_shap", "pct_importance", "cumulative_pct"]]


def plot_shap_global(
    shap_values: np.ndarray,
    X: np.ndarray,
    feature_names: List[str],
    plot_type: str = "beeswarm",
    max_display: int = 20,
    save_path: Optional[str] = None,
):
    """Gera plot SHAP global (summary ou bar).

    Args:
        shap_values: Array de SHAP values.
        X: Features originais.
        feature_names: Nomes das features.
        plot_type: 'beeswarm' ou 'bar'.
        max_display: Máximo de features a mostrar.
        save_path: Path para salvar (opcional).
    """
    import shap
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 8))
    if plot_type == "beeswarm":
        shap.summary_plot(shap_values, X, feature_names=feature_names,
                          max_display=max_display, show=False)
    elif plot_type == "bar":
        shap.summary_plot(shap_values, X, feature_names=feature_names,
                          plot_type="bar", max_display=max_display, show=False)

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
        print(f"  Plot salvo: {save_path}")
    plt.close()


def plot_shap_local(
    shap_values: np.ndarray,
    base_value: float,
    X: np.ndarray,
    feature_names: List[str],
    idx: int,
    save_path: Optional[str] = None,
):
    """Gera waterfall plot para uma observação.

    Args:
        shap_values: Array de SHAP values.
        base_value: Base value do explainer.
        X: Features originais.
        feature_names: Nomes das features.
        idx: Índice da observação a explicar.
        save_path: Path para salvar (opcional).
    """
    import shap
    import matplotlib.pyplot as plt

    explanation = shap.Explanation(
        values=shap_values[idx],
        base_values=base_value,
        data=X[idx],
        feature_names=feature_names,
    )

    plt.figure(figsize=(10, 6))
    shap.waterfall_plot(explanation, show=False)

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.close()
