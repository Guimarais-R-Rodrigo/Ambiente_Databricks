"""Guarda R12: índices completos, navegação coerente e produto preservado."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = "d51ca5dddb76e960f44f5b106b918f3415cc25d4"
ASSIST = ROOT / "ambiente_fonte/.assistant"
SNIPPETS = ASSIST / "hub_snippets"
SIM = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free"
CATEGORIES = ("constants", "display", "ml", "spark", "testing", "visual")


def git(*args: str, text: bool = True):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=text)


def main() -> None:
    control = ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"
    current_control = json.loads(control.read_text(encoding="utf-8"))
    base_control = git("show", f"{BASE}:docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json")
    assert control.read_text(encoding="utf-8") == base_control, "CONTROLE_MIGRACAO mudou na R12"
    assert current_control["phase"] == "complete" and current_control["pending"] == {}, current_control

    expected_source = {
        "ambiente_fonte/.assistant/README.md",
        "ambiente_fonte/.assistant/MANUAL_TECNICO.md",
        "ambiente_fonte/.assistant/hub_snippets/README.md",
        *{f"ambiente_fonte/.assistant/hub_snippets/{c}/README.md" for c in CATEGORIES},
    }
    changed = set(git("diff", "--name-only", BASE, "--", "ambiente_fonte/.assistant").splitlines())
    assert changed == expected_source, ("diff de produto inesperado", sorted(changed ^ expected_source))

    counts = {}
    for category in CATEGORIES:
        root = SNIPPETS / category
        index = root / "README.md"
        assert index.is_file(), index
        text = index.read_text(encoding="utf-8")
        assert "<!-- readme-categoria: 1.0.0 -->" in text, index
        children = {
            p.name for p in root.iterdir()
            if p.is_dir() and not p.name.startswith("_")
        }
        assert children, category
        for name in children:
            assert (root / name / "README.md").is_file(), f"objeto sem README: {category}/{name}"
        linked = set(re.findall(r"\]\(([A-Za-z0-9_]+)/README\.md\)", text))
        assert linked == children, (category, sorted(children - linked), sorted(linked - children))
        counts[category] = len(children)

    assert not (SNIPPETS / "tests/README.md").exists(), "tests/ virou categoria funcional por engano"

    for nav in (ASSIST / "README.md", SNIPPETS / "README.md", ASSIST / "MANUAL_TECNICO.md"):
        text = nav.read_text(encoding="utf-8")
        for category in CATEGORIES:
            needle = f"hub_snippets/{category}/README.md" if nav != SNIPPETS / "README.md" else f"{category}/README.md"
            assert needle in text, (nav, category)

    manual = (ASSIST / "MANUAL_TECNICO.md").read_bytes()
    assert manual == (ROOT / "MANUAL_TECNICO.md").read_bytes(), "Manual fonte != cópia raiz"
    assert "Na migração em andamento" not in manual.decode("utf-8"), "Manual mantém estado histórico obsoleto"

    for src in sorted((ASSIST).rglob("*")):
        if not src.is_file() or "__pycache__" in src.parts or src.suffix in {".pyc", ".pyo"}:
            continue
        rel = src.relative_to(ASSIST)
        dst = SIM / ".assistant" / rel
        assert dst.is_file() and src.read_bytes() == dst.read_bytes(), f"espelho divergente: {rel}"
    assert (ROOT / "ambiente_fonte/.assistant_instructions.md").read_bytes() == (SIM / ".assistant_instructions.md").read_bytes()

    subprocess.check_call(["git", "-C", str(ROOT), "diff", "--check"])
    resumo = ", ".join(f"{k}={v}" for k, v in counts.items())
    print(f"PASS R12: seis índices completos ({resumo}); diff fonte fechado; objetos preservados; controle complete; espelho equivalente.")


if __name__ == "__main__":
    main()
