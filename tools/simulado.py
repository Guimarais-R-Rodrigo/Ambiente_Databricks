"""Inventário exato do derivado: paths, bytes, hashes e tipos, sem git diff."""
from __future__ import annotations

import hashlib
from pathlib import Path

from notebook_marker import eh_notebook
from project_policy import SAFE_SIMULATED_USERNAME, simulated_root, validate_username_component

PUBLISHABLE = (".assistant_instructions.md", ".assistant")
IGNORE_NAMES = {"__pycache__", ".pytest_cache", ".ruff_cache", ".DS_Store"}
MARKER = (
    "# GERADO POR tools/render_simulado.py — NÃO EDITAR À MÃO\n\n"
    "Este diretório é derivado de `ambiente_fonte/`. Qualquer edição manual\n"
    "será perdida no próximo render. Fonte de verdade: o repositório git\n"
    "(regra `docs/ai/rules/fontes-e-derivados.md`).\n"
)


def ignored(path: Path) -> bool:
    return bool(IGNORE_NAMES.intersection(path.parts)) or path.suffix in {".pyc", ".pyo"}


def inventory(base: Path, *, source: bool = False) -> dict[str, dict]:
    if base.is_symlink() or not base.is_dir():
        raise ValueError(f"raiz ausente ou link simbólico: {base}")
    result = {}
    candidates = []
    if source:
        if not (base / ".assistant_instructions.md").is_file() or not (base / ".assistant").is_dir():
            raise ValueError("fonte deve conter instrução FILE e diretório .assistant")
        if not any(p.is_file() and not ignored(p.relative_to(base))
                   for p in (base / ".assistant").rglob("*")):
            raise ValueError("inventário .assistant vazio")
        for item in PUBLISHABLE:
            path = base / item
            if not path.exists():
                raise ValueError(f"fonte publicável ausente: {item}")
            candidates.extend([path, *path.rglob("*")] if path.is_dir() else [path])
    else:
        candidates = list(base.rglob("*"))
    for path in sorted(candidates):
        relative = path.relative_to(base)
        if path.is_symlink():
            raise ValueError(f"link simbólico recusado: {relative.as_posix()}")
        if source and ignored(relative):
            continue
        if path.is_dir():
            result[relative.as_posix()] = {"object_type": "DIRECTORY"}
        elif path.is_file():
            raw = path.read_bytes()
            result[relative.as_posix()] = {
                "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                "object_type": "NOTEBOOK" if path.suffix == ".ipynb" or
                    (path.suffix == ".py" and eh_notebook(path)) else "FILE",
            }
        else:
            raise ValueError(f"objeto não regular: {relative.as_posix()}")
    if not any(entry["object_type"] != "DIRECTORY" for entry in result.values()):
        raise ValueError("inventário publicável vazio")
    return result


def parity_errors(repo: Path, output_root: Path | str | None = None,
                  username: str = SAFE_SIMULATED_USERNAME) -> list[str]:
    try:
        target = simulated_root(repo, output_root)
        user = validate_username_component(username)
        expected = inventory(repo / "ambiente_fonte", source=True)
        for path in target.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"link simbólico recusado: {path.relative_to(target)}")
        actual = inventory(target / "Users" / user)
        expected_outer = {"README_GERADO.md", "Users", f"Users/{user}"}
        actual_outer = {p.relative_to(target).as_posix() for p in target.rglob("*")
                        if not p.is_relative_to(target / "Users" / user) or p == target / "Users" / user}
        errors = []
        # Reject links anywhere, including ancestors which pathlib.rglob does not follow.
        for p in target.rglob("*"):
            if p.is_symlink():
                errors.append(f"link simbólico recusado: {p.relative_to(target)}")
        if actual_outer != expected_outer:
            errors.append(f"inventário externo divergente: {sorted(actual_outer ^ expected_outer)}")
        marker = target / "README_GERADO.md"
        if not marker.is_file() or marker.read_bytes() != MARKER.encode("utf-8"):
            errors.append("marcador gerado ausente ou divergente")
        for name in sorted(expected.keys() - actual.keys()):
            errors.append(f"ausente: {name}")
        for name in sorted(actual.keys() - expected.keys()):
            errors.append(f"extra: {name}")
        for name in sorted(expected.keys() & actual.keys()):
            if expected[name] != actual[name]:
                errors.append(f"bytes/hash/tipo divergente: {name}")
        return errors
    except (OSError, ValueError) as exc:
        return [str(exc)]
