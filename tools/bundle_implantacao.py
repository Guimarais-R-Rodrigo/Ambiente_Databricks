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

from project_policy import SIMULATED_ROOT, simulated_root, SAFE_SIMULATED_USERNAME, EXPECTED_HUB_DIRS, EXPECTED_SKILL_NAMES, LEGACY_MANAGED_SKILL_NAMES
from notebook_marker import eh_notebook
from publicar_free import conferir_fonte_espelho
from temas_v09_transicao import validate_theme_inventory


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = simulated_root(REPO_ROOT) / "Users" / SAFE_SIMULATED_USERNAME

# A área de domínio precisa viajar no próprio Hub, com contratos e execução.
MICROMODELOS_REQUIRED = frozenset({
    ".assistant/hub_micromodelos/README.md",
    ".assistant/hub_micromodelos/__init__.py",
    ".assistant/hub_micromodelos/contratos/micromodelo.schema.json",
    ".assistant/hub_micromodelos/contratos/micromodelo.template.yaml",
    ".assistant/hub_micromodelos/execucao/__init__.py",
    ".assistant/hub_micromodelos/execucao/especificacao.py",
    ".assistant/hub_micromodelos/execucao/assinatura.py",
    ".assistant/hub_micromodelos/execucao/fluxo.py",
    ".assistant/hub_micromodelos/exemplos/README.md",
    ".assistant/hub_micromodelos/exemplos/recencia_contato/README.md",
    ".assistant/hub_micromodelos/exemplos/recencia_contato/micromodelo.yaml",
    ".assistant/hub_micromodelos/exemplos/recencia_contato/dados_sinteticos.json",
    ".assistant/hub_micromodelos/exemplos/recencia_contato/resultado_esperado.json",
    ".assistant/hub_micromodelos/exemplos/recencia_contato/executar_exemplo.py",
})


def main() -> int:
    global SOURCE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="ZIP de saída")
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="gera pacote de revisão mesmo com fonte/derivado não commitados",
    )
    parser.add_argument("--output-root", type=Path, default=SIMULATED_ROOT)
    args = parser.parse_args()
    try:
        SOURCE = simulated_root(REPO_ROOT, args.output_root) / "Users" / SAFE_SIMULATED_USERNAME
    except ValueError as exc:
        print(f"FAIL {exc}")
        return 1
    from simulado import parity_errors
    errors = parity_errors(REPO_ROOT, args.output_root)
    if errors:
        print("FAIL pacote recusado: " + "; ".join(errors))
        return 1

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
        ["git", "status", "--porcelain", "--", "ambiente_fonte"],
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

    if output.is_relative_to(SOURCE.resolve()) or output.is_relative_to((REPO_ROOT / "ambiente_fonte").resolve()):
        print("FAIL saída do pacote não pode ficar dentro do produto")
        return 1
    if output.exists():
        print("FAIL saída já existe; use outro nome para preservar o pacote anterior")
        return 1

    entries = []
    for path in files:
        if path.is_symlink():
            print("FAIL symlink recusado no pacote")
            return 1
        relative = path.relative_to(SOURCE).as_posix()
        entries.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
                "object_type": "NOTEBOOK" if path.suffix == ".ipynb" or (path.suffix == ".py" and eh_notebook(path)) else "FILE",
            }
        )
    packaged_paths = {entry["path"] for entry in entries}
    missing_mm = MICROMODELOS_REQUIRED - packaged_paths
    if missing_mm:
        print("FAIL pacote recusado: módulo Micromodelos incompleto: " + ", ".join(sorted(missing_mm)))
        return 1
    try:
        theme_contract = validate_theme_inventory(entries)
    except ValueError as exc:
        print(f"FAIL pacote recusado: {exc}")
        return 1
    manifest = {
        "schema_version": 2,
        "source_commit": commit,
        "worktree_dirty": dirty,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": "/Users/<username-trabalho>/",
        "files": entries,
        "theme_contract": theme_contract,
        "managed_hub_directories": sorted(EXPECTED_HUB_DIRS),
        "managed_skill_names": sorted(EXPECTED_SKILL_NAMES),
        "legacy_skill_names_for_review": sorted(LEGACY_MANAGED_SKILL_NAMES),
        "preserve": [".assistant/.mcp_servers.json", "skills e arquivos alheios ao Hub", "ACL e configuracoes administrativas"],
    }

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(SOURCE).as_posix())
        archive.writestr("MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"OK {output}: {len(files)} arquivos + MANIFEST.json; commit {commit[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
