from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_SHA = "a8f314a31106aceb52db2661544146cc2bddcc99"
OLD_BASE = "6085eabd4ca715ea2566336aaeb91e2778d76c77"
V03_SHA = "32a892a766037c4bb8c6e0f9ab78661c0583e5fb"
ALLOWED_CONFLICTS = {"CHANGELOG.md", "README.md"}
OVERLAP = {
    "CHANGELOG.md",
    "CLAUDE.md",
    "MANUAL_TECNICO.md",
    "Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md",
    "README.md",
    "ambiente_fonte/.assistant/MANUAL_TECNICO.md",
    "docs/sprints/README.md",
}


def git(*args: str, text: bool = True) -> str:
    out = subprocess.check_output(["git", *args], cwd=ROOT)
    return out.decode("utf-8") if text else out


def show(ref: str, path: str) -> str:
    return git("show", f"{ref}:{path}")


def changed(base: str, head: str) -> set[str]:
    return {line for line in git("diff", "--name-only", base, head).splitlines() if line}


def resolve_expected_conflicts() -> None:
    unresolved = {line for line in git("diff", "--name-only", "--diff-filter=U").splitlines() if line}
    unexpected = unresolved - ALLOWED_CONFLICTS
    if unexpected:
        raise SystemExit(f"Conflitos inesperados: {sorted(unexpected)}")

    if "CHANGELOG.md" in unresolved:
        v03 = Path("/tmp/v03_CHANGELOG.md").read_text(encoding="utf-8")
        main = show("origin/main", "CHANGELOG.md")
        match = re.search(
            r"(?ms)^## 2026-09-12 — V03: adaptador Plotly opt-in \(Codex\)\n.*?(?=^## 2026-09-12 — )",
            v03,
        )
        if not match:
            raise SystemExit("Seção V03 não encontrada no CHANGELOG da candidata")
        section = match.group(0).rstrip() + "\n\n"
        marker = "## 2026-09-12 — R04-A: seis guias de operações Spark (ChatGPT)"
        if marker not in main:
            raise SystemExit("Seção R04-A não encontrada no CHANGELOG da main")
        if "## 2026-09-12 — V03: adaptador Plotly opt-in (Codex)" in main:
            raise SystemExit("Main já contém seção V03 inesperadamente")
        Path("CHANGELOG.md").write_text(main.replace(marker, section + marker, 1), encoding="utf-8")
        subprocess.check_call(["git", "add", "CHANGELOG.md"], cwd=ROOT)

    if "README.md" in unresolved:
        main = show("origin/main", "README.md")
        old_identity = "repo (identidade)  : 1115 arquivos varridos no repositório editável/derivado"
        old_links = "repo (links)       : 1102 links fora da raiz analisada"
        if old_identity not in main or old_links not in main:
            raise SystemExit("Métricas R04-A esperadas ausentes do README da main")
        merged = main.replace(
            old_identity,
            "repo (identidade)  : 1119 arquivos varridos no repositório editável/derivado",
            1,
        ).replace(
            old_links,
            "repo (links)       : 1107 links fora da raiz analisada",
            1,
        )
        Path("README.md").write_text(merged, encoding="utf-8")
        subprocess.check_call(["git", "add", "README.md"], cwd=ROOT)

    leftover = git("diff", "--name-only", "--diff-filter=U").strip()
    if leftover:
        raise SystemExit(f"Conflitos não resolvidos: {leftover}")


def verify_cross_preservation() -> None:
    r04a = changed(OLD_BASE, MAIN_SHA)
    v03 = changed(OLD_BASE, V03_SHA)

    # Arquivos exclusivos da R04-A devem continuar exatamente como na main.
    for path in sorted(r04a - v03):
        current = ROOT / path
        expected = show("origin/main", path).encode("utf-8")
        if not current.is_file() or current.read_bytes() != expected:
            raise SystemExit(f"R04-A exclusiva alterada durante reconciliação: {path}")

    # Arquivos exclusivos da V03 devem continuar exatamente como na candidata aceita.
    for path in sorted(v03 - r04a):
        current = ROOT / path
        expected = show(V03_SHA, path).encode("utf-8")
        if not current.is_file() or current.read_bytes() != expected:
            raise SystemExit(f"V03 exclusiva alterada durante reconciliação: {path}")

    actual_overlap = r04a & v03
    if actual_overlap != OVERLAP:
        raise SystemExit(
            f"Sobreposição mudou: esperado={sorted(OVERLAP)} atual={sorted(actual_overlap)}"
        )

    # Documentos agregadores precisam conter evidências de ambos os lados.
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if "V03: adaptador Plotly opt-in (Codex)" not in changelog or "R04-A: seis guias de operações Spark" not in changelog:
        raise SystemExit("CHANGELOG não preservou V03 + R04-A")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    if "Sistema de Temas" not in claude or "R04-A" not in claude:
        raise SystemExit("CLAUDE.md não preservou contexto de ambas as iniciativas")
    manual = (ROOT / "ambiente_fonte/.assistant/MANUAL_TECNICO.md").read_text(encoding="utf-8")
    for needle in ("registrar_template_plotly_resolvido", "hub_snippets.spark.date_features", "hub_snippets.spark.smart_sample"):
        if needle not in manual:
            raise SystemExit(f"Manual reconciliado perdeu: {needle}")
    sprints = (ROOT / "docs/sprints/README.md").read_text(encoding="utf-8")
    if "V03" not in sprints or "R04-A" not in sprints:
        raise SystemExit("Índice de sprints não preservou V03 + R04-A")


if __name__ == "__main__":
    resolve_expected_conflicts()
    verify_cross_preservation()
    print("Reconciliação V03 + R04-A: preservação cruzada PASS")
