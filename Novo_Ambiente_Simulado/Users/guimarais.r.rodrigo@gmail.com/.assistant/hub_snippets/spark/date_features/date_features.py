"""Add transparent calendar features to Spark DataFrames."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Optional

from pyspark.sql import DataFrame, functions as F


FIXED_NATIONAL_HOLIDAYS_BR = {
    "01-01",
    "04-21",
    "05-01",
    "09-07",
    "10-12",
    "11-02",
    "11-15",
    "11-20",
    "12-25",
}


def extrair_features_data(
    df: DataFrame,
    col_data: str,
    prefixo: Optional[str] = None,
    *,
    holiday_dates: Optional[Sequence[str]] = None,
) -> DataFrame:
    """Add deterministic date features.

    ``is_feriado_nacional_fixo`` covers only fixed-date Brazilian national
    holidays. Pass explicit ISO dates through ``holiday_dates`` to build the
    project calendar, including movable, state, municipal, or banking holidays.
    """
    if col_data not in df.columns:
        raise ValueError(f"column not found: {col_data}")
    prefix = f"{prefixo}_" if prefixo else ""
    date_value = F.to_date(F.col(col_data))
    fixed_holiday = F.date_format(date_value, "MM-dd").isin(sorted(FIXED_NATIONAL_HOLIDAYS_BR))
    explicit_dates = sorted(set(holiday_dates or ()))
    project_holiday = date_value.isin(explicit_dates) if explicit_dates else F.lit(False)
    iso_weekday = ((F.dayofweek(date_value) + F.lit(5)) % F.lit(7)) + F.lit(1)

    return (
        df.withColumn(f"{prefix}dia_semana_iso", iso_weekday)
        .withColumn(f"{prefix}is_fim_semana", iso_weekday.isin([6, 7]))
        .withColumn(f"{prefix}dia_mes", F.dayofmonth(date_value))
        .withColumn(f"{prefix}semana_ano", F.weekofyear(date_value))
        .withColumn(f"{prefix}mes", F.month(date_value))
        .withColumn(f"{prefix}trimestre", F.quarter(date_value))
        .withColumn(f"{prefix}ano", F.year(date_value))
        .withColumn(f"{prefix}is_feriado_nacional_fixo", fixed_holiday)
        .withColumn(f"{prefix}is_feriado_calendario", project_holiday)
    )


add_date_features = extrair_features_data
