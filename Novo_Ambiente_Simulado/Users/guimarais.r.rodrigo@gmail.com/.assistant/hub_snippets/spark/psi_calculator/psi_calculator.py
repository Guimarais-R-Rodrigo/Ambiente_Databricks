"""PSI/CSI nativo em PySpark, com bins derivados somente da referência.

Os limites 0,10/0,25 são heurísticas comuns de monitoramento, não padrões da
Databricks nem gatilhos universais de retreino. Calibre-os ao volume e ao risco.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional

from pyspark.sql import Column, DataFrame, functions as F


def _validate(df_base: DataFrame, df_atual: DataFrame, col: str, n_bins: int) -> None:
    if not 2 <= n_bins <= 100:
        raise ValueError("n_bins deve estar entre 2 e 100")
    for label, frame in (("base", df_base), ("atual", df_atual)):
        if col not in frame.columns:
            raise ValueError(f"coluna {col!r} não existe no DataFrame {label}")


def _calcular_bins_referencia(df_base: DataFrame, col: str, n_bins: int = 20) -> List[float]:
    """Calcule breakpoints numéricos na população de referência não nula."""
    quantiles = [i / n_bins for i in range(1, n_bins)]
    values = df_base.filter(F.col(col).isNotNull()).stat.approxQuantile(col, quantiles, 0.01)
    return sorted({float(value) for value in values if value is not None and math.isfinite(float(value))})


def _bin_expression(col: str, breakpoints: List[float]) -> Column:
    """Use bin 0 para missing e bins 1..N para valores numéricos."""
    value = F.col(col).cast("double")
    expression = F.when(value.isNull() | F.isnan(value), F.lit(0))
    for index, boundary in enumerate(breakpoints, start=1):
        expression = expression.when(value <= F.lit(boundary), F.lit(index))
    return expression.otherwise(F.lit(len(breakpoints) + 1))


def _distribuicao(df: DataFrame, bucket: Column) -> tuple[Dict[int, int], int]:
    rows = df.select(bucket.alias("_bin")).groupBy("_bin").count().collect()
    counts = {int(row["_bin"]): int(row["count"]) for row in rows}
    return counts, sum(counts.values())


def _stability_index(base: Dict[object, int], current: Dict[object, int], n_base: int, n_current: int,
                     epsilon: float = 1e-6) -> float:
    if n_base == 0 or n_current == 0:
        raise ValueError(f"as populações devem ser não vazias (base={n_base}, atual={n_current})")
    value = 0.0
    for key in set(base) | set(current):
        p_base = max(base.get(key, 0) / n_base, epsilon)
        p_current = max(current.get(key, 0) / n_current, epsilon)
        value += (p_current - p_base) * math.log(p_current / p_base)
    return float(value)


def calcular_psi(df_base: DataFrame, df_atual: DataFrame, col: str, n_bins: int = 20) -> float:
    """Calcule PSI numérico incluindo mudança da proporção de valores ausentes."""
    _validate(df_base, df_atual, col, n_bins)
    breakpoints = _calcular_bins_referencia(df_base, col, n_bins)
    expression = _bin_expression(col, breakpoints)
    base, n_base = _distribuicao(df_base, expression)
    current, n_current = _distribuicao(df_atual, expression)
    return round(_stability_index(base, current, n_base, n_current), 6)


def _calcular_csi_categorico(df_base: DataFrame, df_atual: DataFrame, col: str) -> float:
    category = F.coalesce(F.col(col).cast("string"), F.lit("__MISSING__"))
    base_rows = df_base.select(category.alias("category")).groupBy("category").count().collect()
    current_rows = df_atual.select(category.alias("category")).groupBy("category").count().collect()
    base = {row["category"]: int(row["count"]) for row in base_rows}
    current = {row["category"]: int(row["count"]) for row in current_rows}
    return round(_stability_index(base, current, sum(base.values()), sum(current.values())), 6)


def calcular_csi(df_base: DataFrame, df_atual: DataFrame, feature_cols: List[str], n_bins: int = 20) -> Dict[str, float]:
    """Calcule estabilidade por feature; numéricas usam PSI, demais usam categorias."""
    if not feature_cols:
        raise ValueError("feature_cols não pode ser vazio")
    missing = set(feature_cols) - set(df_base.columns) | (set(feature_cols) - set(df_atual.columns))
    if missing:
        raise ValueError(f"colunas ausentes: {sorted(missing)}")
    numeric_tokens = ("tinyint", "smallint", "int", "bigint", "float", "double", "decimal")
    base_types = dict(df_base.dtypes)
    results: Dict[str, float] = {}
    for col in feature_cols:
        if any(token in base_types[col] for token in numeric_tokens):
            results[col] = calcular_psi(df_base, df_atual, col, n_bins)
        else:
            results[col] = _calcular_csi_categorico(df_base, df_atual, col)
    return dict(sorted(results.items(), key=lambda item: item[1], reverse=True))


def interpretar_psi(
    psi_value: float,
    *,
    warning_threshold: Optional[float] = None,
    critical_threshold: Optional[float] = None,
) -> str:
    """Interprete PSI somente com thresholds calibrados pelo consumidor."""
    if not math.isfinite(psi_value) or psi_value < 0:
        raise ValueError("psi_value deve ser finito e não negativo")
    if warning_threshold is None or critical_threshold is None:
        return f"PSI={psi_value:.4f} — compare com a política calibrada desta feature/modelo"
    if not 0 <= warning_threshold < critical_threshold:
        raise ValueError("esperado 0 <= warning_threshold < critical_threshold")
    if psi_value >= critical_threshold:
        return f"🔴 PSI={psi_value:.4f} — acima do crítico configurado; investigar"
    if psi_value >= warning_threshold:
        return f"🟡 PSI={psi_value:.4f} — acima do alerta configurado; investigar"
    return f"🟢 PSI={psi_value:.4f} — abaixo do alerta configurado"
