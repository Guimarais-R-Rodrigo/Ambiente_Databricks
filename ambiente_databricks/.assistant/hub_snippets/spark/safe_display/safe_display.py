"""Limita as ações de display de DataFrames Spark grandes no notebook."""

from __future__ import annotations

from typing import Callable, Optional

from pyspark.sql import DataFrame


def safe_display(
    df: DataFrame,
    limit: int = 1000,
    msg: bool = True,
    *,
    display_fn: Optional[Callable[[DataFrame], None]] = None,
) -> None:
    """Display at most ``limit`` rows without issuing a full-table count."""
    if limit <= 0:
        raise ValueError("limit must be positive")
    # Sem cache(): PERSIST não é suportado em compute serverless e o prefixo
    # limit+1 já limita o custo das duas ações.
    preview = df.limit(limit + 1)
    observed = preview.count()
    truncated = observed > limit
    if msg:
        suffix = "+" if truncated else ""
        print(f"Displaying {min(observed, limit):,}{suffix} rows (limit={limit:,}).".replace(",", "."))
    renderer = display_fn or globals().get("display")
    if renderer is None:
        raise RuntimeError("Databricks display() is unavailable; pass display_fn explicitly")
    renderer(preview.limit(limit))
