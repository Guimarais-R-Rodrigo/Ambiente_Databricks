"""Constrói features de recência, frequência e valor (RFV/RFM) por cliente."""

from __future__ import annotations

from collections.abc import Sequence

from pyspark.sql import DataFrame, SparkSession, functions as F


def rfv_calculator(
    table_name: str,
    col_cliente: str,
    col_data: str,
    col_valor: str,
    dt_referencia: str,
    periodos: Sequence[int] = (30, 60, 90),
) -> DataFrame:
    """Calculate leakage-safe RFV features up to an inclusive reference date.

    The function returns raw features; it deliberately does not invent quintile
    scores or business segments. Define those rules from the intended decision.
    """
    periods = sorted({int(period) for period in periodos})
    if not periods or any(period <= 0 for period in periods):
        raise ValueError("periodos must contain positive integers")

    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    source = spark.table(table_name)
    required = {col_cliente, col_data, col_valor}
    missing = required - set(source.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")

    ref_date = F.to_date(F.lit(dt_referencia))
    df = (
        source
        .withColumn(col_data, F.to_date(F.col(col_data)))
        .filter(F.col(col_data).isNotNull())
        .filter(F.col(col_data) <= ref_date)
    )

    base = (
        df.groupBy(col_cliente)
        .agg(
            F.max(col_data).alias("ultima_data"),
            F.sum(F.col(col_valor)).alias("valor_total"),
            F.count(F.lit(1)).alias("frequencia_total"),
        )
        .withColumn("recencia", F.datediff(ref_date, F.col("ultima_data")))
    )

    for period in periods:
        windowed = df.filter(F.col(col_data) >= F.date_sub(ref_date, period - 1))
        aggregate = windowed.groupBy(col_cliente).agg(
            F.count(F.lit(1)).alias(f"frequencia_{period}d"),
            F.sum(F.col(col_valor)).alias(f"valor_{period}d"),
        )
        base = base.join(aggregate, on=col_cliente, how="left")

    fill_columns = [
        column
        for period in periods
        for column in (f"frequencia_{period}d", f"valor_{period}d")
    ]
    return base.fillna(0, subset=fill_columns)
