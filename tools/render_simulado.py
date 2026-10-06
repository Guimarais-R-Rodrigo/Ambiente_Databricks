"""Renderiza .artifacts/simulado/ como espelho da árvore do workspace.

Copia ambiente_fonte/ (fonte canônica) para a árvore exata que o workspace
Databricks espera, de modo que a replicação seja uma cópia mecânica:

    .artifacts/simulado/Users/<username>/.assistant_instructions.md
    .artifacts/simulado/Users/<username>/.assistant/...

Uso:

    python tools/render_simulado.py                 # dry-run (mostra o plano)
    python tools/render_simulado.py --write         # apaga e regenera
    python tools/render_simulado.py --username foo  # sobrepõe o username

Cópia fiel byte a byte: nenhum header é injetado, para que o diff entre o
simulado e o workspace publicado seja vazio.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_policy import SAFE_SIMULATED_USERNAME, SIMULATED_ROOT, simulated_root, validate_username_component  # noqa: E402

DEFAULT_USERNAME = SAFE_SIMULATED_USERNAME

SOURCE = Path("ambiente_fonte")
TARGET_ROOT = SIMULATED_ROOT
from simulado import MARKER, inventory, parity_errors

# Artefatos de execução local não são produto: rodar um helper dentro de
# ambiente_fonte/ cria __pycache__, e sem este filtro o lixo era copiado para o
# simulado e publicado no workspace.
IGNORAR = shutil.ignore_patterns(
    "__pycache__", "*.pyc", "*.pyo", ".pytest_cache", ".ruff_cache", ".DS_Store"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="executa o render")
    mode.add_argument("--check", action="store_true", help="confere inventário, bytes e tipos sem escrever")
    parser.add_argument("--output-root", type=Path, default=TARGET_ROOT,
                        help="subdiretório gerado dentro de .artifacts/ (padrão: .artifacts/simulado)")
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    source = (repo_root / SOURCE).resolve()
    if not source.exists():
        print(f"FAIL fonte não encontrada: {source}")
        return 1

    try:
        username = validate_username_component(args.username)
    except ValueError as exc:
        print(f"FAIL {exc}")
        return 1

    try:
        target_root = simulated_root(repo_root, args.output_root)
        inventory(source, source=True)  # Fail closed on missing input or source symlinks.
        if target_root.exists():
            for path in target_root.rglob("*"):
                if path.is_symlink():
                    raise ValueError("destino contém link simbólico; reconcilie antes de renderizar")
    except (OSError, ValueError) as exc:
        print(f"FAIL {exc}")
        return 1
    if args.check:
        errors = parity_errors(repo_root, args.output_root, username)
        for error in errors:
            print(f"DERIVED_STALE: {error}")
        if not errors:
            print("OK: fonte/saída equivalentes por paths, bytes, hashes e tipos")
        return int(bool(errors))

    users_root = (target_root / "Users").resolve()
    user_dir = (users_root / username).resolve()
    if not user_dir.is_relative_to(users_root):
        print("FAIL destino do username escaparia de .artifacts/simulado/Users")
        return 1
    plan = [
        (source / ".assistant_instructions.md", user_dir / ".assistant_instructions.md"),
        (source / ".assistant", user_dir / ".assistant"),
    ]

    print(f"fonte  : {source}")
    print(f"destino: {user_dir.resolve()}")
    for src, dst in plan:
        kind = "dir " if src.is_dir() else "file"
        print(f"  copy {kind} {src.name} -> {dst}")

    if not args.write:
        print("\nDRY-RUN: nada foi escrito. Use --write para executar.")
        return 0

    if target_root.exists():
        shutil.rmtree(target_root)
    user_dir.mkdir(parents=True)

    for src, dst in plan:
        if src.is_dir():
            shutil.copytree(src, dst, ignore=IGNORAR)
        else:
            shutil.copy2(src, dst)

    (target_root / "README_GERADO.md").write_text(
        MARKER, encoding="utf-8", newline="\n"
    )

    n_files = sum(1 for p in target_root.rglob("*") if p.is_file())
    print(f"\nOK: {n_files} arquivos renderizados em {target_root.relative_to(repo_root)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
