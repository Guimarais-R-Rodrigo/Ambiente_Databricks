"""Export a Unity Catalog table schema as safe YAML 1.2."""

from __future__ import annotations

import json
from typing import Any, Dict

from pyspark.sql import SparkSession, functions as F


def schema_to_dict(
    table_name: str,
    *,
    include_comments: bool = True,
    include_stats: bool = False,
) -> Dict[str, Any]:
    """Return a serializable schema dictionary with optional bounded scan stats."""
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    df = spark.table(table_name)
    payload: Dict[str, Any] = {"table": table_name, "columns": []}

    stats: Dict[str, Any] = {}
    total_rows = 0
    if include_stats:
        expressions = [F.count(F.lit(1)).alias("__total")]
        for index, field in enumerate(df.schema.fields):
            expressions.extend(
                [
                    F.approx_count_distinct(F.col(field.name)).alias(f"c{index}__distinct"),
                    F.sum(F.when(F.col(field.name).isNull(), 1).otherwise(0)).alias(f"c{index}__null"),
                ]
            )
        stats = df.agg(*expressions).collect()[0].asDict()
        total_rows = int(stats.pop("__total") or 0)
        payload["row_count"] = total_rows

    for index, field in enumerate(df.schema.fields):
        column: Dict[str, Any] = {
            "name": field.name,
            "type": field.dataType.simpleString(),
            "nullable": bool(field.nullable),
        }
        if include_comments and field.metadata and field.metadata.get("comment") is not None:
            column["comment"] = str(field.metadata["comment"])
        if include_stats:
            null_count = int(stats[f"c{index}__null"] or 0)
            column["stats"] = {
                "approx_distinct": int(stats[f"c{index}__distinct"] or 0),
                "null_count": null_count,
                "null_pct": null_count / total_rows * 100 if total_rows else 0.0,
            }
        payload["columns"].append(column)
    return payload


def schema_to_yaml(
    table_name: str,
    include_comments: bool = True,
    include_stats: bool = False,
) -> str:
    """Return a safely escaped YAML representation.

    PyYAML is used when installed. The JSON fallback is intentional: JSON is a
    valid YAML 1.2 document and preserves escaping without a hidden dependency.
    """
    payload = schema_to_dict(
        table_name,
        include_comments=include_comments,
        include_stats=include_stats,
    )
    try:
        import yaml
    except ImportError:
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)
