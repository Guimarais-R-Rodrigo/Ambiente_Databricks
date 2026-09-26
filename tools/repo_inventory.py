"""Inventário Git certificável, separado da higiene da árvore de trabalho."""
from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath


def git_paths(root: Path, *, untracked: bool = False) -> list[Path]:
    """Lista caminhos NUL-delimited; Git ausente/falho nunca vira aprovação vazia.

    Não usa --exclude-standard ao listar extras: ignorado ainda pode precisar
    de higiene. O chamador aplica o escopo documentado de caches/quarentena.
    """
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z", "--others" if untracked else "--cached"],
            cwd=root, capture_output=True,
        )
    except OSError as exc:
        raise ValueError("Git indisponível; use um checkout para certificar o inventário") from exc
    if proc.returncode:
        raise ValueError("git ls-files falhou; inventário não certificado")
    paths = []
    for raw in proc.stdout.split(b"\0"):
        if not raw:
            continue
        name = raw.decode("utf-8", errors="strict")
        rel = PurePosixPath(name)
        if rel.is_absolute() or ".." in rel.parts or "\\" in name:
            raise ValueError("Git retornou caminho não seguro")
        path = root.joinpath(*rel.parts)
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("caminho Git resolve fora do repositório")
        paths.append(path)
    if not untracked and not paths:
        raise ValueError("inventário Git vazio; não certificado")
    return sorted(set(paths))
