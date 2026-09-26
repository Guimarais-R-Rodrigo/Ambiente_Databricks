
"""Resumo de nulos por coluna com semáforos."""

from __future__ import annotations

from pyspark.sql import DataFrame, functions as F


def null_summary(df: DataFrame, threshold_warn: float = 5, threshold_fail: float = 20) -> DataFrame:
    """Return null counts and percentages by column with traffic-light status."""
    total = df.count()
    exprs = []
    for c in df.columns:
        exprs.append(F.sum(F.col(c).isNull().cast("int")).alias(c))
    counts = df.select(exprs).collect()[0].asDict()
    rows = []
    for col_name, count_null in counts.items():
        pct = (count_null / total * 100) if total else 0.0
        if pct >= threshold_fail:
            status = "🔴"
        elif pct >= threshold_warn:
            status = "🟡"
        else:
            status = "🟢"
        rows.append((col_name, int(count_null), float(pct), status))
    result = df.sparkSession.createDataFrame(rows, ["coluna", "count_null", "pct_null", "status"]).orderBy(F.desc("pct_null"))
    print("Resumo de nulos calculado com sucesso.")
    return result
