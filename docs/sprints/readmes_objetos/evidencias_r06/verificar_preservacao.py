"""Guarda R06: prova que a migração documental preserva os cinco objetos temporais."""
from __future__ import annotations

import ast
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = "cae94988cda66a8c61ecebbe6ceed487120a76f2"
PREFIX = "ambiente_fonte/.assistant/"
OBJECTS = [
    "arima_wrapper",
    "lgbm_temporal",
    "prophet_wrapper",
    "split_temporal",
    "walk_forward",
]


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def before(path: str) -> bytes:
    return git("show", f"{BASE}:{path}")


def unchanged(path: str) -> None:
    assert (ROOT / path).read_bytes() == before(path), path


def executable_magics(text: str) -> list[str]:
    result: list[str] = []
    for cell in text.split("# COMMAND ----------"):
        lines = [line for line in cell.splitlines() if line.startswith("# MAGIC")]
        if lines and not lines[0].startswith("# MAGIC %md"):
            result.append("\n".join(lines))
    return result


def check() -> None:
    base_paths = git("ls-tree", "-r", "--name-only", BASE).decode().splitlines()
    notebooks = {
        f"{PREFIX}hub_snippets/ml/{obj}/exemplo_{obj}.py" for obj in OBJECTS
    }

    # Nenhum Python do produto muda, salvo os cinco notebooks em comentários Markdown.
    product_python = [
        path for path in base_paths
        if path.startswith(PREFIX) and path.endswith(".py") and path not in notebooks
    ]
    for path in product_python:
        unchanged(path)

    output_pattern = r"(?ms)^# MAGIC ```text\n.*?^# MAGIC ```\s*$"
    for path in sorted(notebooks):
        old = before(path).decode("utf-8")
        new = (ROOT / path).read_text(encoding="utf-8")
        assert ast.dump(ast.parse(old), include_attributes=False) == ast.dump(
            ast.parse(new), include_attributes=False
        ), path + " AST"
        assert executable_magics(old) == executable_magics(new), path + " magic executável"
        assert re.findall(output_pattern, old) == re.findall(output_pattern, new), path + " outputs históricos"
        old_non_magic = [line for line in old.splitlines() if line.strip() and not line.startswith("# MAGIC")]
        new_non_magic = [line for line in new.splitlines() if line.strip() and not line.startswith("# MAGIC")]
        assert old_non_magic == new_non_magic, path + " linhas não-Markdown"

    previous_readmes = [
        path for path in base_paths
        if path.startswith(PREFIX)
        and path.endswith("/README.md")
        and b"<!-- readme-objeto:" in before(path)
    ]
    assert len(previous_readmes) == 41, len(previous_readmes)
    for path in previous_readmes:
        unchanged(path)

    for obj in OBJECTS:
        base = f"{PREFIX}hub_snippets/ml/{obj}"
        unchanged(f"{base}/{obj}.py")
        unchanged(f"{base}/__init__.py")
        readme = ROOT / base / "README.md"
        assert readme.is_file(), str(readme)
        assert "<!-- readme-objeto: 1.0.0 -->" in readme.read_text(encoding="utf-8")

    # Infraestrutura já integrada e superfícies concorrentes ficam congeladas.
    protected = [
        path for path in base_paths
        if path.startswith((
            "tools/",
            ".github/workflows/",
            "docs/decisions/",
            "docs/sprints/sistema_temas/",
            PREFIX + "skills/",
            PREFIX + "hub_padroes/",
            PREFIX + "hub_readmes_visual_assets/",
        ))
    ]
    for path in protected:
        unchanged(path)

    prompt_forms = [
        path for path in base_paths
        if path.startswith(PREFIX + "hub_prompts/")
        and path.endswith(".md")
        and not path.endswith("/README.md")
    ]
    for path in prompt_forms:
        unchanged(path)
    unchanged("ambiente_fonte/.assistant_instructions.md")

    control_path = "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"
    old_control = json.loads(before(control_path))
    new_control = json.loads((ROOT / control_path).read_text(encoding="utf-8"))
    removed = {f"hub_snippets/ml/{obj}" for obj in OBJECTS}
    assert set(old_control["pending"]) - set(new_control["pending"]) == removed
    assert not (set(new_control["pending"]) - set(old_control["pending"]))
    assert len(new_control["pending"]) == 32, len(new_control["pending"])
    for path, value in new_control["pending"].items():
        assert value == old_control["pending"][path], path
    assert {k: v for k, v in old_control.items() if k != "pending"} == {
        k: v for k, v in new_control.items() if k != "pending"
    }

    old_changelog = before("CHANGELOG.md").decode("utf-8")
    new_changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    old_history = old_changelog[old_changelog.index("## 2026-") :]
    assert new_changelog.endswith(old_history), "histórico anterior do CHANGELOG"

    source = ROOT / "ambiente_fonte"
    target = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free"
    mirrored: list[str] = []
    for path in source.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path == source / "README.md":
            continue
        dest = target / path.relative_to(source)
        assert dest.is_file() and dest.read_bytes() == path.read_bytes(), str(path) + " mirror"
        mirrored.append(str(path.relative_to(source)))
    derived = [str(path.relative_to(target)) for path in target.rglob("*") if path.is_file()]
    assert set(derived) == set(mirrored), "simulado com arquivos extras/ausentes"

    canonical_manual = source / ".assistant/MANUAL_TECNICO.md"
    assert (ROOT / "MANUAL_TECNICO.md").read_bytes() == canonical_manual.read_bytes()
    assert (target / ".assistant/MANUAL_TECNICO.md").read_bytes() == canonical_manual.read_bytes()

    print(json.dumps({
        "base": BASE,
        "status": "PASS",
        "checks": {
            "product_python_unchanged": len(product_python),
            "five_notebooks_AST_magics_outputs_preserved": len(notebooks),
            "previous_object_readmes_unchanged": len(previous_readmes),
            "five_implementations_unchanged": 5,
            "five_facades_unchanged": 5,
            "protected_paths": len(protected),
            "prompt_forms_unchanged": len(prompt_forms),
            "migration_exemptions_removed": 5,
            "pending": len(new_control["pending"]),
            "source_files_mirrored": len(mirrored),
            "manual_three_copies_equal": True,
            "changelog_prior_entries_preserved": True,
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    check()
