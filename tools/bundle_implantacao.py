"""Gera um ZIP mínimo e sanitizado para implantação manual no Databricks.

O pacote contém somente a subárvore derivada do produto e um manifesto SHA-256.
Ele não transporta Git, documentação interna, referências congeladas ou paths da
máquina do autor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from project_policy import SAFE_SIMULATED_USERNAME
from publicar_free import conferir_fonte_espelho


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "Novo_Ambiente_Simulado" / "Users" / SAFE_SIMULATED_USERNAME


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="ZIP de saída")
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="gera pacote de revisão mesmo com fonte/derivado não commitados",
    )
    args = parser.parse_args()

    if not SOURCE.is_dir():
        print("FAIL simulado sanitizado ausente; rode tools/render_simulado.py --write")
        return 1
    divergencias = conferir_fonte_espelho(SOURCE)
    if divergencias:
        print("FAIL pacote recusado: fonte/espelho ou inventário inválido")
        for erro in divergencias:
            print(f"  {erro}")
        return 1
    files = sorted(path for path in SOURCE.rglob("*") if path.is_file())
    if not files:
        print("FAIL simulado sanitizado não contém arquivos")
        return 1

    commit_proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if commit_proc.returncode != 0:
        print(f"FAIL não foi possível resolver o commit: {commit_proc.stderr.strip()}")
        return 1
    commit = commit_proc.stdout.strip()

    status_proc = subprocess.run(
        ["git", "status", "--porcelain", "--", "ambiente_fonte", "Novo_Ambiente_Simulado"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if status_proc.returncode != 0:
        print(f"FAIL não foi possível conferir o worktree: {status_proc.stderr.strip()}")
        return 1
    dirty = bool(status_proc.stdout.strip())
    if dirty and not args.allow_dirty:
        print("FAIL fonte/derivado têm mudanças não commitadas; use --allow-dirty somente para revisão")
        return 1

    suffix = "-dirty" if dirty else ""
    output = args.output or REPO_ROOT / ".artifacts" / f"ambiente-databricks-{commit[:12]}{suffix}.zip"
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for path in files:
        relative = path.relative_to(SOURCE).as_posix()
        entries.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
        )
    manifest = {
        "schema_version": 1,
        "source_commit": commit,
        "worktree_dirty": dirty,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": "/Users/<username-trabalho>/",
        "files": entries,
    }

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(SOURCE).as_posix())
        archive.writestr("MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"OK {output}: {len(files)} arquivos + MANIFEST.json; commit {commit[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
