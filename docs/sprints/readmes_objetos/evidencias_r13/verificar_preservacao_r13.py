from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = "ec4b559d098c96dfececbb17e52fbc276cb485c0"

ALLOWED_EXACT = {
    "README.md",
    "CHANGELOG.md",
    "docs/sprints/README.md",
    "docs/sprints/readmes_objetos/README.md",
    "docs/sprints/readmes_objetos/RELATORIO_R13.md",
    "docs/sprints/readmes_objetos/ACHADOS_R13.md",
    "docs/sprints/readmes_objetos/MATRIZ_AUDITORIA_R13.md",
    "docs/sprints/readmes_objetos/RUBRICA_R13.json",
}
ALLOWED_PREFIX = "docs/sprints/readmes_objetos/evidencias_r13/"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8")


def main() -> None:
    protected = [
        "ambiente_fonte",
        "Novo_Ambiente_Simulado",
        "MANUAL_TECNICO.md",
        "tools",
    ]
    for path in protected:
        changed = git("diff", "--name-only", BASE, "--", path).splitlines()
        if changed:
            raise SystemExit(f"FAIL R13: produto/ferramenta protegida mudou em {path}: {changed[:10]}")

    changed_all = set(git("diff", "--name-only", BASE).splitlines())
    unexpected = sorted(
        p for p in changed_all
        if p not in ALLOWED_EXACT and not p.startswith(ALLOWED_PREFIX)
    )
    if unexpected:
        raise SystemExit(f"FAIL R13: caminho fora do escopo documental: {unexpected}")

    temp_workflows = sorted(p for p in changed_all if p.startswith(".github/workflows/readmes-r13"))
    if temp_workflows:
        raise SystemExit(f"FAIL R13: workflow temporário permaneceu na árvore: {temp_workflows}")

    subprocess.check_call(["git", "-C", str(ROOT), "diff", "--check"])
    print(f"PASS R13 preservação: {len(changed_all)} caminho(s) líquidos, todos documentais/evidência; produto, simulado, Manual e tools idênticos à base.")


if __name__ == "__main__":
    main()
