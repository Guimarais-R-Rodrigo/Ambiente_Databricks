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
import re
import shutil
import sys
from pathlib import Path

DEFAULT_USERNAME = "guimarais.r.rodrigo@gmail.com"

# O username do trabalho é identificador corporativo e não pode virar nome de
# diretório versionado (ADR-0003). A replicação no trabalho copia o conteúdo da
# subárvore renderizada, sem exigir render com o username de lá.
CORPORATE_RE = re.compile(r"c\d{6}|corp\.|\.gov\.br", re.IGNORECASE)
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
    "(regra `.claude/rules/fonte-de-verdade.md`).\n"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="executa o render")
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    args = parser.parse_args()

    source = SOURCE.resolve()
    if not source.exists():
        print(f"FAIL fonte não encontrada: {source}")
        return 1

    if CORPORATE_RE.search(args.username):
        print(
            "FAIL username com aparência corporativa recusado (ADR-0003).\n"
            "     Para replicar no trabalho, copie o conteúdo da subárvore já\n"
            "     renderizada para /Users/<username-trabalho>/ — ver o runbook\n"
            "     em docs/playbooks/replicacao-trabalho.md."
        )
        return 1

    user_dir = TARGET_ROOT / "Users" / args.username
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

    if TARGET_ROOT.exists():
        shutil.rmtree(TARGET_ROOT)
    user_dir.mkdir(parents=True)

    for src, dst in plan:
        if src.is_dir():
            shutil.copytree(src, dst, ignore=IGNORAR)
        else:
            shutil.copy2(src, dst)

    (TARGET_ROOT / "README_GERADO.md").write_text(MARKER, encoding="utf-8")

    n_files = sum(1 for p in TARGET_ROOT.rglob("*") if p.is_file())
    print(f"\nOK: {n_files} arquivos renderizados em {TARGET_ROOT}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
