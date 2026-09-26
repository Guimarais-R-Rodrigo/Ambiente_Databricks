"""Mede a proximidade entre código e documentação em notebooks exportados."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


SOURCE_MARKERS = {
    ".py": ("# COMMAND ----------", ("# MAGIC %md", "# MAGIC %md-sandbox")),
    ".sql": ("-- COMMAND ----------", ("-- MAGIC %md", "-- MAGIC %md-sandbox")),
    ".scala": ("// COMMAND ----------", ("// MAGIC %md", "// MAGIC %md-sandbox")),
    ".r": ("# COMMAND ----------", ("# MAGIC %md", "# MAGIC %md-sandbox")),
}


def _jupyter_cells(path: Path) -> List[Dict[str, str]]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return [
        {"type": str(cell.get("cell_type", "unknown")), "source": "".join(cell.get("source", []))}
        for cell in notebook.get("cells", [])
    ]


def _databricks_source_cells(path: Path) -> List[Dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix not in SOURCE_MARKERS:
        raise ValueError(f"unsupported source extension: {suffix}")
    command_marker, markdown_markers = SOURCE_MARKERS[suffix]
    chunks = path.read_text(encoding="utf-8").split(command_marker)
    cells: List[Dict[str, str]] = []
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        is_markdown = any(marker in stripped.splitlines()[:3] for marker in markdown_markers)
        cells.append({"type": "markdown" if is_markdown else "code", "source": chunk})
    return cells


def doc_coverage(notebook_path: str) -> Dict[str, Any]:
    """Measure whether code cells have adjacent explanatory Markdown.

    Args:
        notebook_path: Local/exported ``.ipynb``, ``.py``, ``.sql``, ``.scala``, or
            ``.r`` file. This function does not fetch workspace objects by URL.

    Returns:
        Counts, a simple adjacency coverage percentage, and zero-based uncovered
        cell indexes. The metric is a heuristic and does not assess prose quality.
    """
    path = Path(notebook_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    cells = _jupyter_cells(path) if path.suffix.lower() == ".ipynb" else _databricks_source_cells(path)

    total_code = sum(cell["type"] == "code" for cell in cells)
    total_markdown = sum(cell["type"] == "markdown" for cell in cells)
    uncovered: List[int] = []
    for index, cell in enumerate(cells):
        if cell["type"] != "code":
            continue
        has_before = index > 0 and cells[index - 1]["type"] == "markdown"
        has_after = index + 1 < len(cells) and cells[index + 1]["type"] == "markdown"
        if not (has_before or has_after):
            uncovered.append(index)

    coverage_pct = 100.0 if total_code == 0 else (1 - len(uncovered) / total_code) * 100
    return {
        "path": str(path),
        "format": path.suffix.lower(),
        "total_code_cells": total_code,
        "total_markdown_cells": total_markdown,
        "coverage_pct": coverage_pct,
        "uncovered_cell_indexes": uncovered,
        "metric_note": "Adjacency heuristic; review explanatory quality separately.",
    }
