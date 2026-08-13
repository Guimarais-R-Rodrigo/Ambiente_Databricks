"""
Cálculo de WOE (Weight of Evidence) e IV (Information Value) em PySpark.

Uso:
    from x_snippets.ml.woe_iv_calculator import calculate_woe_iv
    woe_df = calculate_woe_iv(sdf, feature_col='renda_faixa', target_col='flag_default')

Autor: Rodrigo via assistente
Versão: 1.0
Nota: Implementação PySpark nativa (sem toPandas).
"""

from pyspark.sql import DataFrame, functions as F, Window
from typing import Tuple


def calculate_woe_iv(
    df: DataFrame,
    feature_col: str,
    target_col: str,
    smoothing: float = 0.5,
) -> Tuple[DataFrame, float]:
    """Calcula WOE e IV para uma feature categórica/binned.

    Args:
        df: DataFrame PySpark com feature e target.
        feature_col: Coluna da feature (já discretizada em faixas).
        target_col: Coluna do target binário (0/1).

    Returns:
        Tuple de (DataFrame com WOE por faixa, IV total).
    """
    missing = {feature_col, target_col} - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if smoothing <= 0:
        raise ValueError("smoothing must be positive")
    totals = df.agg(
        F.sum(F.when(F.col(target_col) == 0, 1).otherwise(0)).alias("total_bom"),
        F.sum(F.when(F.col(target_col) == 1, 1).otherwise(0)).alias("total_mau"),
        F.sum(F.when(F.col(target_col).isNull() | ~F.col(target_col).isin(0, 1), 1).otherwise(0)).alias("invalid"),
    ).collect()[0]

    total_bom = totals["total_bom"]
    total_mau = totals["total_mau"]
    if totals["invalid"]:
        raise ValueError(f"target_col contains {totals['invalid']} null/non-binary rows")
    if not total_bom or not total_mau:
        raise ValueError("target_col must contain both classes 0 and 1")

    # Contagem por faixa
    grouped = (
        df.groupBy(feature_col)
        .agg(
            F.sum(F.when(F.col(target_col) == 0, 1).otherwise(0)).alias("n_bom"),
            F.sum(F.when(F.col(target_col) == 1, 1).otherwise(0)).alias("n_mau"),
            F.count("*").alias("n_total"),
        )
    )
    n_bins = grouped.count()
    woe_df = (
        grouped
        .withColumn("pct_bom", (F.col("n_bom") + F.lit(smoothing)) / F.lit(total_bom + smoothing * n_bins))
        .withColumn("pct_mau", (F.col("n_mau") + F.lit(smoothing)) / F.lit(total_mau + smoothing * n_bins))
        # WOE
        .withColumn("woe", F.log(F.col("pct_bom") / F.col("pct_mau")))
        # IV parcial
        .withColumn("iv_partial", (F.col("pct_bom") - F.col("pct_mau")) * F.col("woe"))
        .orderBy(feature_col)
    )

    # IV total
    iv_total = woe_df.agg(F.sum("iv_partial").alias("iv")).collect()[0]["iv"]

    return woe_df, iv_total


def classify_iv(iv: float) -> str:
    """Classifica o IV em faixas de poder preditivo.

    Args:
        iv: Information Value calculado.

    Returns:
        String com classificação.
    """
    if iv < 0 or not float(iv) < float("inf"):
        raise ValueError("iv must be finite and non-negative")
    if iv < 0.02:
        return "Inútil (< 0.02)"
    elif iv < 0.10:
        return "Fraca (0.02-0.10)"
    elif iv < 0.30:
        return "Média (0.10-0.30)"
    elif iv < 0.50:
        return "Forte (0.30-0.50)"
    else:
        return "Elevada (> 0.50) — investigar concentração, binning e possível leakage"
