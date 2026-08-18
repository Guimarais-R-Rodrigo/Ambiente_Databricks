"""Cria amostras reprodutíveis e limitadas de DataFrames Spark."""

from __future__ import annotations

from typing import Optional

from pyspark.sql import DataFrame, Window, functions as F


def smart_sample(
    df: DataFrame,
    n: int = 10000,
    stratify_col: Optional[str] = None,
    seed: int = 42,
) -> DataFrame:
    """Return at most ``n`` rows, preserving strata approximately when requested.

    Stratified sampling uses a distributed per-stratum row number and does not
    collect category values on the driver. If the number of strata exceeds ``n``,
    representing every stratum is impossible and the function raises.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if stratify_col and stratify_col not in df.columns:
        raise ValueError(f"column not found: {stratify_col}")

    bounded_count = df.limit(n + 1).count()
    if bounded_count <= n:
        return df

    if stratify_col:
        strata_count = df.select(stratify_col).distinct().limit(n + 1).count()
        if strata_count > n:
            raise ValueError(f"cannot represent more than {n} strata in a sample of {n} rows")

        total = df.count()
        partition = Window.partitionBy(stratify_col)
        random_order = Window.partitionBy(stratify_col).orderBy(F.rand(seed))
        allocated = (
            df.withColumn("__stratum_count", F.count(F.lit(1)).over(partition))
            .withColumn(
                "__stratum_target",
                F.greatest(F.lit(1), F.round(F.col("__stratum_count") * F.lit(n / total)).cast("long")),
            )
            .withColumn("__sample_rank", F.row_number().over(random_order))
            .filter(F.col("__sample_rank") <= F.col("__stratum_target"))
            .drop("__stratum_count", "__stratum_target", "__sample_rank")
        )
        return allocated.orderBy(F.rand(seed)).limit(n)

    fraction = min(1.0, n * 1.2 / df.count())
    return df.sample(withReplacement=False, fraction=fraction, seed=seed).limit(n)
