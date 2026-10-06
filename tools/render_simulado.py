"""Renderiza Novo_Ambiente_Simulado/ como espelho da árvore do workspace.

Copia ambiente_fonte/ (fonte canônica) para a árvore exata que o workspace
Databricks espera, de modo que a replicação seja uma cópia mecânica:

    Novo_Ambiente_Simulado/Users/<username>/.assistant_instructions.md
    Novo_Ambiente_Simulado/Users/<username>/.assistant/...

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

from project_policy import SAFE_SIMULATED_USERNAME, validate_username_component  # noqa: E402

DEFAULT_USERNAME = SAFE_SIMULATED_USERNAME

SOURCE = Path("ambiente_fonte")
TARGET_ROOT = Path("Novo_Ambiente_Simulado")

# Artefatos de execução local não são produto: rodar um helper dentro de
# ambiente_fonte/ cria __pycache__, e sem este filtro o lixo era copiado para o
# simulado e publicado no workspace.
IGNORAR = shutil.ignore_patterns(
    "__pycache__", "*.pyc", "*.pyo", ".pytest_cache", ".ruff_cache", ".DS_Store"
)

MARKER = (
    "# GERADO POR tools/render_simulado.py — NÃO EDITAR À MÃO\n\n"
    "Este diretório é derivado de `ambiente_fonte/`. Qualquer edição manual\n"
    "será perdida no próximo render. Fonte de verdade: o repositório git\n"
    "(regra `docs/ai/rules/fontes-e-derivados.md`).\n"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="executa o render")
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

    target_root = (repo_root / TARGET_ROOT).resolve()
    expected_target = (repo_root / "Novo_Ambiente_Simulado").resolve()
    if target_root != expected_target or target_root.parent != repo_root:
        print("FAIL raiz derivada não é o diretório fixo do workspace")
        return 1
    users_root = (target_root / "Users").resolve()
    user_dir = (users_root / username).resolve()
    if not user_dir.is_relative_to(users_root):
        print("FAIL destino do username escaparia de Novo_Ambiente_Simulado/Users")
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
    print(f"\nOK: {n_files} arquivos renderizados em {TARGET_ROOT}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
