"""Diagnóstico de distribuição no driver, com políticas de monitoramento configuráveis."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


MISSING_CATEGORY = "__MISSING__"


def _finite_1d(values: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=float).reshape(-1)
    array = array[np.isfinite(array)]
    if len(array) == 0:
        raise ValueError(f"{name} has no finite values")
    return array


def calculate_psi(reference: np.ndarray, current: np.ndarray, n_bins: int = 10, eps: float = 1e-6) -> float:
    """Calculate PSI with reference edges and an explicit missing-value bucket."""
    if n_bins < 2 or eps <= 0:
        raise ValueError("n_bins must be at least 2 and eps must be positive")
    raw_ref = np.asarray(reference, dtype=float).reshape(-1)
    raw_cur = np.asarray(current, dtype=float).reshape(-1)
    if np.isinf(raw_ref).any() or np.isinf(raw_cur).any():
        raise ValueError("infinite values are not supported")
    ref = _finite_1d(raw_ref, "reference")
    cur = _finite_1d(raw_cur, "current")
    internal = np.unique(np.quantile(ref, np.linspace(0, 1, n_bins + 1)[1:-1]))
    bins = np.concatenate(([-np.inf], internal, [np.inf]))
    ref_counts = np.append(np.histogram(ref, bins=bins)[0], np.isnan(raw_ref).sum())
    cur_counts = np.append(np.histogram(cur, bins=bins)[0], np.isnan(raw_cur).sum())
    ref_pct = np.maximum(ref_counts / len(raw_ref), eps)
    cur_pct = np.maximum(cur_counts / len(raw_cur), eps)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def calculate_ks(reference: np.ndarray, current: np.ndarray) -> Tuple[float, float]:
    """Return two-sample KS statistic and p-value for finite observations."""
    result = ks_2samp(_finite_1d(reference, "reference"), _finite_1d(current, "current"))
    return float(result.statistic), float(result.pvalue)


def calculate_csi(reference: pd.Series, current: pd.Series, eps: float = 1e-6) -> float:
    """Calculate a categorical stability index, treating missingness as a category."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    ref = reference.astype("object").where(reference.notna(), MISSING_CATEGORY)
    cur = current.astype("object").where(current.notna(), MISSING_CATEGORY)
    if ref.empty or cur.empty:
        raise ValueError("reference and current must be non-empty")
    ref_dist = ref.value_counts(normalize=True)
    cur_dist = cur.value_counts(normalize=True)
    value = 0.0
    for category in set(ref_dist.index) | set(cur_dist.index):
        ref_pct = max(float(ref_dist.get(category, 0)), eps)
        cur_pct = max(float(cur_dist.get(category, 0)), eps)
        value += (cur_pct - ref_pct) * np.log(cur_pct / ref_pct)
    return float(value)


def detect_drift_all_features(
    df_reference: pd.DataFrame,
    df_current: pd.DataFrame,
    feature_cols: List[str],
    numeric_cols: Optional[List[str]] = None,
    categorical_cols: Optional[List[str]] = None,
    psi_threshold: Optional[float] = None,
    ks_threshold: Optional[float] = None,
    *,
    severe_psi_threshold: Optional[float] = None,
    severe_ks_threshold: Optional[float] = None,
    min_non_null: int = 10,
) -> pd.DataFrame:
    """Report drift evidence; classify only with consumer-supplied thresholds.

    KS p-values depend strongly on sample size and observations must satisfy the
    test's assumptions. PSI/CSI thresholds are policy, not universal constants.
    """
    missing = set(feature_cols) - set(df_reference.columns) | set(feature_cols) - set(df_current.columns)
    if missing:
        raise ValueError(f"features missing from one or both DataFrames: {sorted(missing)}")
    if min_non_null <= 0:
        raise ValueError("min_non_null must be positive")
    if (psi_threshold is None) != (ks_threshold is None):
        raise ValueError("supply both psi_threshold and ks_threshold, or neither")
    if severe_psi_threshold is not None and psi_threshold is None:
        raise ValueError("severe thresholds require warning thresholds")

    numeric = numeric_cols or df_reference[feature_cols].select_dtypes(include=[np.number]).columns.tolist()
    categorical = categorical_cols or [column for column in feature_cols if column not in numeric]
    results = []

    for column in numeric:
        ref_missing = float(df_reference[column].isna().mean())
        cur_missing = float(df_current[column].isna().mean())
        ref_all = pd.to_numeric(df_reference[column], errors="coerce").to_numpy()
        cur_all = pd.to_numeric(df_current[column], errors="coerce").to_numpy()
        ref = ref_all[np.isfinite(ref_all)]
        cur = cur_all[np.isfinite(cur_all)]
        if len(ref) < min_non_null or len(cur) < min_non_null:
            results.append({"feature": column, "type": "numeric", "status": "INSUFFICIENT_DATA", "reference_n": len(ref), "current_n": len(cur)})
            continue
        psi = calculate_psi(ref_all, cur_all)
        ks_stat, ks_pvalue = calculate_ks(ref, cur)
        status = "NOT_CLASSIFIED"
        if psi_threshold is not None:
            severe = (severe_psi_threshold is not None and psi >= severe_psi_threshold) or (severe_ks_threshold is not None and ks_stat >= severe_ks_threshold)
            status = "SEVERE" if severe else "ALERT" if psi >= psi_threshold or ks_stat >= ks_threshold else "OK"
        results.append(
            {
                "feature": column,
                "type": "numeric",
                "psi": psi,
                "ks_statistic": ks_stat,
                "ks_pvalue": ks_pvalue,
                "reference_n": len(ref),
                "current_n": len(cur),
                "reference_missing_pct": ref_missing * 100,
                "current_missing_pct": cur_missing * 100,
                "status": status,
            }
        )

    for column in categorical:
        if len(df_reference[column]) < min_non_null or len(df_current[column]) < min_non_null:
            results.append({"feature": column, "type": "categorical", "status": "INSUFFICIENT_DATA"})
            continue
        csi = calculate_csi(df_reference[column], df_current[column])
        status = "NOT_CLASSIFIED"
        if psi_threshold is not None:
            status = "SEVERE" if severe_psi_threshold is not None and csi >= severe_psi_threshold else "ALERT" if csi >= psi_threshold else "OK"
        results.append({"feature": column, "type": "categorical", "psi": csi, "status": status})

    columns = ["feature", "type", "psi", "ks_statistic", "ks_pvalue", "reference_n", "current_n", "reference_missing_pct", "current_missing_pct", "status"]
    return pd.DataFrame(results).reindex(columns=columns).sort_values("psi", ascending=False, na_position="last").reset_index(drop=True)
