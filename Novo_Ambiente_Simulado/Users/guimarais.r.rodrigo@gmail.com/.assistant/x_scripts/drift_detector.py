"""Detect numeric distribution drift with Population Stability Index (PSI)."""

from __future__ import annotations

from math import log
from typing import Any, Dict, Iterable, Optional

from pyspark.sql import Column, DataFrame, SparkSession, functions as F


def _cache_if_supported(df: DataFrame) -> DataFrame:
    """cache() é bloqueado em compute serverless; nesse caso, seguir sem cache."""
    try:
        return df.cache()
    except Exception:
        return df


def _unpersist_quietly(df: DataFrame) -> None:
    try:
        df.unpersist()
    except Exception:
        pass


def _classify_psi(
    value: float,
    warning_threshold: Optional[float],
    critical_threshold: Optional[float],
) -> str:
    """Classify only when the caller supplies a calibrated monitoring policy."""
    if warning_threshold is None or critical_threshold is None:
        return "not_classified"
    if not 0 <= warning_threshold < critical_threshold:
        raise ValueError("expected 0 <= warning_threshold < critical_threshold")
    return "critical" if value >= critical_threshold else "attention" if value >= warning_threshold else "stable"


def _bucket_expression(column_name: str, boundaries: list[float]) -> Column:
    """Build a bucket expression shared by reference and comparison datasets."""
    value = F.col(column_name).cast("double")
    bucket = F.when(value.isNull() | F.isnan(value), F.lit("missing"))
    for index, boundary in enumerate(boundaries):
        bucket = bucket.when(value <= F.lit(boundary), F.lit(f"bin_{index:02d}"))
    return bucket.otherwise(F.lit(f"bin_{len(boundaries):02d}"))


def _counts_by_bucket(df: DataFrame, bucket: Column) -> tuple[dict[str, int], int]:
    rows = df.select(bucket.alias("bucket")).groupBy("bucket").count().collect()
    counts = {str(row["bucket"]): int(row["count"]) for row in rows}
    return counts, sum(counts.values())


def drift_detector(
    table_name: str,
    date_col: str,
    date_ref: str,
    date_comp: str,
    cols: Optional[Iterable[str]] = None,
    method: str = "psi",
    *,
    num_bins: int = 10,
    relative_error: float = 0.001,
    epsilon: float = 1e-6,
    warning_threshold: Optional[float] = None,
    critical_threshold: Optional[float] = None,
) -> Dict[str, Any]:
    """Compare two cohorts using PSI with reference-derived quantile buckets.

    PSI thresholds are monitoring heuristics, not universal pass/fail rules. Calibrate
    them for the model, feature, sample size, and business risk before automation.

    Args:
        table_name: Unity Catalog table in ``catalog.schema.table`` form.
        date_col: Cohort/date column used to select the two populations.
        date_ref: Reference cohort value.
        date_comp: Comparison cohort value.
        cols: Numeric columns. When omitted, all numeric columns are selected.
        method: Currently only ``"psi"`` is supported.
        num_bins: Target number of reference quantile bins (2 to 100).
        relative_error: Spark ``approxQuantile`` relative error.
        epsilon: Smoothing applied to zero bucket proportions.

    Returns:
        Per-column PSI, interpretation, reference boundaries, and bucket details.
    """
    if method.lower() != "psi":
        raise ValueError("method must be 'psi'; no other drift method is implemented")
    if not 2 <= num_bins <= 100:
        raise ValueError("num_bins must be between 2 and 100")
    if not 0 <= relative_error <= 1:
        raise ValueError("relative_error must be between 0 and 1")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")

    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    df = spark.table(table_name)
    missing = {date_col, *(cols or [])} - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")

    selected_cols = list(cols) if cols else [
        name
        for name, dtype in df.dtypes
        if any(token in dtype for token in ("tinyint", "smallint", "int", "bigint", "float", "double", "decimal"))
    ]
    if not selected_cols:
        raise ValueError("no numeric columns selected")

    ref_df = _cache_if_supported(df.filter(F.col(date_col) == F.lit(date_ref)))
    comp_df = _cache_if_supported(df.filter(F.col(date_col) == F.lit(date_comp)))
    ref_size = ref_df.count()
    comp_size = comp_df.count()
    if ref_size == 0 or comp_size == 0:
        _unpersist_quietly(ref_df)
        _unpersist_quietly(comp_df)
        raise ValueError(f"both cohorts must be non-empty (reference={ref_size}, comparison={comp_size})")

    probabilities = [index / num_bins for index in range(1, num_bins)]
    results: Dict[str, Any] = {}
    try:
        for column_name in selected_cols:
            raw_boundaries = ref_df.stat.approxQuantile(column_name, probabilities, relative_error)
            boundaries = sorted({float(value) for value in raw_boundaries if value is not None})
            bucket = _bucket_expression(column_name, boundaries)
            ref_counts, _ = _counts_by_bucket(ref_df, bucket)
            comp_counts, _ = _counts_by_bucket(comp_df, bucket)
            labels = sorted(set(ref_counts) | set(comp_counts))

            details = []
            psi = 0.0
            for label in labels:
                ref_pct = max(ref_counts.get(label, 0) / ref_size, epsilon)
                comp_pct = max(comp_counts.get(label, 0) / comp_size, epsilon)
                contribution = (comp_pct - ref_pct) * log(comp_pct / ref_pct)
                psi += contribution
                details.append(
                    {
                        "bucket": label,
                        "reference_count": ref_counts.get(label, 0),
                        "comparison_count": comp_counts.get(label, 0),
                        "reference_pct": ref_pct,
                        "comparison_pct": comp_pct,
                        "psi_contribution": contribution,
                    }
                )

            results[column_name] = {
                "psi": float(psi),
                "classification": _classify_psi(float(psi), warning_threshold, critical_threshold),
                "boundaries": boundaries,
                "reference_size": ref_size,
                "comparison_size": comp_size,
                "buckets": details,
            }
    finally:
        _unpersist_quietly(ref_df)
        _unpersist_quietly(comp_df)
    return results
