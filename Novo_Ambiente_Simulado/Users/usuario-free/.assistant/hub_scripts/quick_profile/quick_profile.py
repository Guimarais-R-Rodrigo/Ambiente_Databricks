"""Gera um perfil inicial e limitado de uma tabela do Unity Catalog."""

from __future__ import annotations

from typing import Any, Dict

from pyspark.sql import DataFrame, SparkSession, functions as F


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


def quick_profile(
    table_name: str,
    sample_fraction: float = 0.1,
    max_categories: int = 20,
    *,
    seed: int = 42,
) -> Dict[str, Any]:
    """Profile schema and selected statistics using a declared sample.

    Row count and null counts are computed on the complete table in one aggregate.
    Cardinality, top values, numeric summaries, and date ranges use the sample to
    bound cost. Returned metadata makes that distinction explicit.
    """
    if not 0 < sample_fraction <= 1:
        raise ValueError("sample_fraction must be in (0, 1]")
    if max_categories <= 0:
        raise ValueError("max_categories must be positive")

    # Resolver a sessão explicitamente: o global de notebook `spark` não existe
    # quando o módulo é importado (NameError em runtime serverless).
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    df = spark.table(table_name)
    dtypes = dict(df.dtypes)
    numeric_cols = [
        column
        for column, dtype in df.dtypes
        if any(token in dtype for token in ("tinyint", "smallint", "int", "bigint", "float", "double", "decimal"))
    ]
    date_cols = [column for column, dtype in df.dtypes if "date" in dtype or "timestamp" in dtype]
    string_cols = [column for column, dtype in df.dtypes if dtype == "string"]

    aggregate_expressions = [F.count(F.lit(1)).alias("__total")]
    aggregate_expressions.extend(
        F.sum(F.when(F.col(column).isNull(), 1).otherwise(0)).alias(column)
        for column in df.columns
    )
    aggregate = df.agg(*aggregate_expressions).collect()[0].asDict()
    total_rows = int(aggregate.pop("__total") or 0)
    null_summary = sorted(
        (
            {
                "column": column,
                "null_count": int(aggregate[column] or 0),
                "null_pct": (int(aggregate[column] or 0) / total_rows * 100) if total_rows else 0.0,
            }
            for column in df.columns
        ),
        key=lambda item: item["null_pct"],
        reverse=True,
    )

    sample = _cache_if_supported(df if sample_fraction == 1 else df.sample(False, sample_fraction, seed))
    sample_rows = sample.count()
    try:
        cardinality = {}
        if string_cols:
            expressions = [F.approx_count_distinct(F.col(column)).alias(column) for column in string_cols[:10]]
            cardinality = sample.agg(*expressions).collect()[0].asDict()

        top_values = {
            column: [row.asDict() for row in sample.groupBy(column).count().orderBy(F.desc("count")).limit(max_categories).collect()]
            for column in string_cols[:5]
        }

        numeric_summary: Dict[str, Any] = {}
        selected_numeric = numeric_cols[:10]
        if selected_numeric:
            expressions = []
            for column in selected_numeric:
                expressions.extend(
                    [
                        F.min(column).alias(f"{column}__min"),
                        F.max(column).alias(f"{column}__max"),
                        F.avg(column).alias(f"{column}__mean"),
                    ]
                )
            row = sample.agg(*expressions).collect()[0].asDict()
            numeric_summary = {
                column: {metric: row[f"{column}__{metric}"] for metric in ("min", "max", "mean")}
                for column in selected_numeric
            }

        date_range: Dict[str, Any] = {}
        selected_dates = date_cols[:5]
        if selected_dates:
            expressions = []
            for column in selected_dates:
                expressions.extend([F.min(column).alias(f"{column}__min"), F.max(column).alias(f"{column}__max")])
            row = sample.agg(*expressions).collect()[0].asDict()
            date_range = {
                column: {metric: row[f"{column}__{metric}"] for metric in ("min", "max")}
                for column in selected_dates
            }
    finally:
        _unpersist_quietly(sample)

    return {
        "table": table_name,
        "total_rows": total_rows,
        "total_columns": len(df.columns),
        "sample_fraction": sample_fraction,
        "sample_seed": seed,
        "sample_rows": sample_rows,
        "dtypes": dtypes,
        "null_summary_full_table": null_summary,
        "cardinality_sample": cardinality,
        "top_values_sample": top_values,
        "numeric_summary_sample": numeric_summary,
        "date_range_sample": date_range,
    }
