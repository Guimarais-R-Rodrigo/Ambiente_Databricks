"""Avalia a qualidade de uma tabela do Unity Catalog com varredura compacta."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pyspark.sql import SparkSession, functions as F


DEFAULT_THRESHOLDS = {"null_warn": 5.0, "null_fail": 20.0, "freshness_days": 2.0}


def data_quality_check(
    table_name: str,
    pk_columns: List[str],
    date_column: Optional[str] = None,
    thresholds: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Assess PK uniqueness, null rates, and optional freshness.

    Thresholds are local monitoring policy, not Databricks defaults. For production
    pipelines, encode enforceable rules as Lakeflow expectations and monitor the
    pipeline event log; use this helper for ad-hoc diagnosis.
    """
    limits = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    if not pk_columns:
        raise ValueError("pk_columns must contain at least one column")
    if not 0 <= limits["null_warn"] <= limits["null_fail"] <= 100:
        raise ValueError("expected 0 <= null_warn <= null_fail <= 100")
    if limits["freshness_days"] < 0:
        raise ValueError("freshness_days must be non-negative")

    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    df = spark.table(table_name)
    required = set(pk_columns) | ({date_column} if date_column else set())
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")

    aggregate_expressions = [F.count(F.lit(1)).alias("__total")]
    aggregate_expressions.extend(
        F.sum(F.when(F.col(column).isNull(), 1).otherwise(0)).alias(column)
        for column in df.columns
    )
    if date_column:
        aggregate_expressions.append(F.max(F.col(date_column)).alias("__max_date"))
    aggregate = df.agg(*aggregate_expressions).collect()[0].asDict()
    total = int(aggregate.pop("__total") or 0)
    max_date = aggregate.pop("__max_date", None)

    distinct_pk = df.select(*pk_columns).dropDuplicates().count()
    duplicates = total - distinct_pk
    alerts: list[dict[str, Any]] = []

    null_checks: Dict[str, Any] = {}
    for column in df.columns:
        count = int(aggregate[column] or 0)
        pct = count / total * 100 if total else 0.0
        status = "fail" if pct >= limits["null_fail"] else "warn" if pct >= limits["null_warn"] else "pass"
        null_checks[column] = {"count": count, "pct": pct, "status": status}
        if status != "pass":
            alerts.append(
                {
                    "check": "null_rate",
                    "column": column,
                    "severity": status,
                    "message": f"Null rate {pct:.2f}% ({count}/{total}).",
                }
            )

    checks: Dict[str, Any] = {
        "row_count": total,
        "pk_uniqueness": {
            "columns": list(pk_columns),
            "duplicate_rows": duplicates,
            "status": "pass" if duplicates == 0 else "fail",
        },
        "nulls": null_checks,
    }
    if duplicates:
        alerts.append(
            {
                "check": "pk_uniqueness",
                "severity": "fail",
                "message": f"Primary-key candidate has {duplicates} duplicate rows.",
            }
        )

    if date_column:
        max_as_date = max_date.date() if isinstance(max_date, datetime) else max_date
        days_old = (date.today() - max_as_date).days if isinstance(max_as_date, date) else None
        freshness_status = (
            "fail" if days_old is None or days_old > limits["freshness_days"] else "pass"
        )
        checks["freshness"] = {
            "column": date_column,
            "max_value": str(max_date) if max_date is not None else None,
            "days_old": days_old,
            "status": freshness_status,
        }
        if freshness_status == "fail":
            alerts.append(
                {
                    "check": "freshness",
                    "severity": "fail",
                    "message": f"Latest {date_column} is {days_old!r} days old; limit is {limits['freshness_days']}.",
                }
            )

    failures = sum(alert["severity"] == "fail" for alert in alerts)
    warnings = sum(alert["severity"] == "warn" for alert in alerts)
    status = "fail" if failures else "warn" if warnings else "pass"
    score = max(0, 100 - 25 * failures - 5 * warnings)
    return {
        "status": status,
        "score": score,
        "thresholds": limits,
        "checks": checks,
        "alerts": alerts,
    }
