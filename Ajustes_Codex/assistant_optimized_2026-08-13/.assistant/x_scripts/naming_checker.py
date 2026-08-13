"""Check configurable table and column naming conventions."""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Dict, List


def naming_checker(
    table_name: str,
    *,
    enforce_prefix: bool = False,
    allowed_table_prefixes: Sequence[str] = (),
    max_col_length: int = 255,
) -> List[Dict[str, str]]:
    """Return naming-policy violations without presenting local policy as Databricks law.

    Unity Catalog does not require dimensional prefixes such as ``dim_`` or
    ``fato_``. Supply your organization's prefixes only when that policy exists.
    """
    if max_col_length <= 0:
        raise ValueError("max_col_length must be positive")
    if enforce_prefix and not allowed_table_prefixes:
        raise ValueError("allowed_table_prefixes is required when enforce_prefix=True")

    df = spark.table(table_name)
    violations: List[Dict[str, str]] = []
    table_short = table_name.split(".")[-1]

    if len(table_name.split(".")) != 3:
        violations.append(
            {
                "object": table_name,
                "severity": "warning",
                "message": "Prefer a fully qualified Unity Catalog name: catalog.schema.table.",
                "policy": "databricks-recommended-context",
            }
        )
    if enforce_prefix and not any(table_short.startswith(prefix) for prefix in allowed_table_prefixes):
        violations.append(
            {
                "object": table_name,
                "severity": "warning",
                "message": f"Table does not start with one of {tuple(allowed_table_prefixes)}.",
                "policy": "organization-custom",
            }
        )

    for column_name in df.columns:
        if not re.fullmatch(r"[a-z][a-z0-9_]*", column_name):
            violations.append(
                {
                    "object": column_name,
                    "severity": "warning",
                    "message": "Column is outside the configured lowercase snake_case convention.",
                    "policy": "project-custom",
                }
            )
        if len(column_name) > max_col_length:
            violations.append(
                {
                    "object": column_name,
                    "severity": "warning",
                    "message": f"Column exceeds the configured limit of {max_col_length} characters.",
                    "policy": "project-custom",
                }
            )
    return violations
