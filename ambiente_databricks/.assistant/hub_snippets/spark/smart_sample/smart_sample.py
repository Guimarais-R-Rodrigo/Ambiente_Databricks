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
    """Return at most ``n`` rows; stratified mode preserves every stratum exactly once or more.

    Stratified sampling allocates exactly ``n`` rows with largest remainders,
    uses a distributed per-stratum row number and does not collect category
    values on the driver. If the number of strata exceeds ``n``, representing
    every stratum is impossible and the function raises.
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

        remaining = n - strata_count
        global_window = Window.partitionBy()
        remainder_order = Window.orderBy(
            F.col("__fractional").desc(),
            F.xxhash64(F.col(stratify_col)).asc(),
        )
        counts = (
            df.groupBy(stratify_col)
            .count()
            .withColumnRenamed("count", "__stratum_count")
            .withColumn("__weight", F.col("__stratum_count") - F.lit(1))
            .withColumn("__weight_total", F.sum("__weight").over(global_window))
            .withColumn(
                "__raw_extra",
                F.when(
                    F.col("__weight_total") > 0,
                    F.lit(remaining) * F.col("__weight") / F.col("__weight_total"),
                ).otherwise(F.lit(0.0)),
            )
            .withColumn("__base_extra", F.floor("__raw_extra").cast("long"))
            .withColumn("__fractional", F.col("__raw_extra") - F.col("__base_extra"))
            .withColumn("__base_sum", F.sum("__base_extra").over(global_window))
            .withColumn("__bonus_rank", F.row_number().over(remainder_order))
            .withColumn(
                "__stratum_target",
                F.lit(1)
                + F.col("__base_extra")
                + F.when(
                    F.col("__bonus_rank") <= F.lit(remaining) - F.col("__base_sum"),
                    F.lit(1),
                ).otherwise(F.lit(0)),
            )
            .select(stratify_col, "__stratum_target")
        )
        random_order = Window.partitionBy(stratify_col).orderBy(F.rand(seed))
        left = df.alias("source")
        right = counts.alias("allocation")
        allocated = (
            left.join(
                right,
                F.col(f"source.`{stratify_col}`").eqNullSafe(
                    F.col(f"allocation.`{stratify_col}`")
                ),
                "inner",
            )
            .select(
                *[F.col(f"source.`{column}`").alias(column) for column in df.columns],
                F.col("allocation.__stratum_target"),
            )
            .withColumn("__sample_rank", F.row_number().over(random_order))
            .filter(F.col("__sample_rank") <= F.col("__stratum_target"))
            .drop("__stratum_target", "__sample_rank")
        )
        return allocated

    fraction = min(1.0, n * 1.2 / df.count())
    return df.sample(withReplacement=False, fraction=fraction, seed=seed).limit(n)
