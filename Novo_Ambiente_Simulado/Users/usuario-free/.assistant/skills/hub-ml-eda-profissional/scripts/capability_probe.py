#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capability probe SE01 para scripts relativos de Agent Skill.

O probe é deliberadamente pequeno, read-only e não executa EDA. Ele comprova
somente que um script relativo à skill consegue localizar a raiz ``.assistant``,
importar uma API pública existente e devolver um marcador estruturado.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Iterable

MARKER = "SEF_CAPABILITY_PROBE_V0_1"
IMPORT_TARGET = "hub_snippets.constants.format_br.fmt_int"


def _candidate_roots(explicit: str | None = None) -> Iterable[Path]:
    if explicit:
        yield Path(explicit)

    env_root = os.environ.get("ASSISTANT_ROOT")
    if env_root:
        yield Path(env_root)

    here = Path(__file__).resolve()
    for parent in here.parents:
        if parent.name == ".assistant":
            yield parent
            break

    cwd = Path.cwd().resolve()
    if cwd.name == ".assistant":
        yield cwd
    for parent in cwd.parents:
        if parent.name == ".assistant":
            yield parent
            break


def _looks_like_assistant_root(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "hub_snippets").is_dir()
        and (path / "skills").is_dir()
    )


def resolve_assistant_root(explicit: str | None = None) -> Path:
    seen: set[Path] = set()
    for candidate in _candidate_roots(explicit):
        resolved = candidate.expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if _looks_like_assistant_root(resolved):
            return resolved
    raise RuntimeError(
        "ASSISTANT_ROOT_NOT_FOUND: informe --assistant-root ou execute a partir de uma árvore .assistant válida"
    )


def run_probe(assistant_root: str | None = None) -> dict[str, object]:
    root = resolve_assistant_root(assistant_root)
    inserted = False
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
        inserted = True

    try:
        from hub_snippets.constants.format_br import fmt_int

        sample_result = fmt_int(1234)
        if sample_result != "1.234":
            raise RuntimeError(
                f"PUBLIC_API_RESULT_UNEXPECTED: fmt_int(1234)={sample_result!r}"
            )
    finally:
        if inserted and sys.path and sys.path[0] == root_text:
            sys.path.pop(0)

    return {
        "marker": MARKER,
        "status": "PASS",
        "assistant_root_resolved": True,
        "import_target": IMPORT_TARGET,
        "sample_result": sample_result,
        "writes_performed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Executa o capability probe read-only da SE01.")
    parser.add_argument("--assistant-root", help="Raiz .assistant explícita, quando necessário.")
    args = parser.parse_args(argv)

    try:
        payload = run_probe(args.assistant_root)
        code = 0
    except Exception as exc:  # saída estruturada é parte do probe
        payload = {
            "marker": MARKER,
            "status": "FAIL",
            "assistant_root_resolved": False,
            "import_target": IMPORT_TARGET,
            "writes_performed": False,
            "error_code": exc.__class__.__name__,
            "error": str(exc),
        }
        code = 1

    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
