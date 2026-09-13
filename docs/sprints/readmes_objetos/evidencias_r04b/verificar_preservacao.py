"""Guarda R04-B: preserva produto, notebooks e controles contra a main pós-R04-A."""
from __future__ import annotations

import ast
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = "a8f314a31106aceb52db2661544146cc2bddcc99"
PREFIX = "ambiente_fonte/.assistant/"
OBJECTS = [
    "data_quality_check",
    "doc_coverage",
    "drift_detector",
    "naming_checker",
    "rfv_calculator",
    "schema_to_yaml",
]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def before(path):
    return git("show", BASE + ":" + path)


def unchanged(path):
    assert (ROOT / path).read_bytes() == before(path), path


def executable_magics(text):
    result = []
    for cell in text.split("# COMMAND ----------"):
        lines = [line for line in cell.splitlines() if line.startswith("# MAGIC")]
        if lines and not lines[0].startswith("# MAGIC %md"):
            result.append("\n".join(lines))
    return result


def check():
    paths = git("ls-tree", "-r", "--name-only", BASE).decode().splitlines()
    notebooks = {
        PREFIX + f"hub_scripts/{obj}/exemplo_{obj}.py"
        for obj in OBJECTS
    }
    implementations = {
        PREFIX + f"hub_scripts/{obj}/{obj}.py"
        for obj in OBJECTS
    }
    facades = {
        PREFIX + f"hub_scripts/{obj}/__init__.py"
        for obj in OBJECTS
    }
    for path in sorted(implementations | facades):
        unchanged(path)

    for path in sorted(notebooks):
        old = before(path).decode()
        new = (ROOT / path).read_text(encoding="utf-8")
        assert ast.dump(ast.parse(old), include_attributes=False) == ast.dump(ast.parse(new), include_attributes=False), path + " AST"
        assert executable_magics(old) == executable_magics(new), path + " magic executable"
        output_pattern = r"(?ms)^# MAGIC ```text\n.*?^# MAGIC ```\s*$"
        assert re.findall(output_pattern, old) == re.findall(output_pattern, new), path + " output"
        assert [x for x in old.splitlines() if x.strip() and not x.startswith("# MAGIC")] == [
            x for x in new.splitlines() if x.strip() and not x.startswith("# MAGIC")
        ], path + " executable/comment cells"

    previous_readmes = [
        p for p in paths
        if p.startswith(PREFIX)
        and p.endswith("/README.md")
        and b"<!-- readme-objeto:" in before(p)
    ]
    assert len(previous_readmes) == 29, len(previous_readmes)
    for path in previous_readmes:
        unchanged(path)

    protected = [
        p for p in paths
        if p.startswith((
            PREFIX + "skills/",
            PREFIX + "hub_padroes/",
            PREFIX + "hub_readmes_visual_assets/",
            "tools/",
            ".github/workflows/",
            "novas_funcionalidades/",
            "docs/decisions/",
            "docs/sprints/sistema_temas/",
        ))
    ]
    for path in protected:
        unchanged(path)

    forms = [
        p for p in paths
        if p.startswith(PREFIX + "hub_prompts/") and p.endswith(".md") and not p.endswith("/README.md")
    ]
    for path in forms:
        unchanged(path)
    unchanged("ambiente_fonte/.assistant_instructions.md")

    control = "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"
    old_control = json.loads(before(control))
    new_control = json.loads((ROOT / control).read_text(encoding="utf-8"))
    removed = {f"hub_scripts/{obj}" for obj in OBJECTS}
    assert set(old_control["pending"]) - set(new_control["pending"]) == removed
    assert not set(new_control["pending"]) - set(old_control["pending"])
    assert len(new_control["pending"]) == 43
    assert all(v == old_control["pending"][p] for p, v in new_control["pending"].items())
    assert {k: v for k, v in old_control.items() if k != "pending"} == {
        k: v for k, v in new_control.items() if k != "pending"
    }

    old_changelog = before("CHANGELOG.md").decode()
    new_changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    header = old_changelog[: old_changelog.index("## 2026-")]
    history = old_changelog[old_changelog.index("## 2026-") :]
    assert new_changelog.startswith(header)
    assert new_changelog.endswith(history)

    source = ROOT / "ambiente_fonte"
    target = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free"
    mirrored = []
    for path in source.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path == source / "README.md":
            continue
        dest = target / path.relative_to(source)
        assert dest.is_file() and dest.read_bytes() == path.read_bytes(), str(path) + " mirror"
        mirrored.append(str(path.relative_to(source)))
    derived = [str(path.relative_to(target)) for path in target.rglob("*") if path.is_file()]
    assert set(derived) == set(mirrored), "extra/missing mirror"
    assert (ROOT / "MANUAL_TECNICO.md").read_bytes() == (source / ".assistant/MANUAL_TECNICO.md").read_bytes()

    print(json.dumps({
        "base": BASE,
        "status": "PASS",
        "checks": {
            "six_implementations_unchanged": len(implementations),
            "six_facades_unchanged": len(facades),
            "six_notebooks_AST_magics_outputs_preserved": len(notebooks),
            "previous_object_readmes_unchanged": len(previous_readmes),
            "protected_paths": len(protected),
            "prompt_forms_unchanged": len(forms),
            "migration_exemptions_removed": 6,
            "pending": 43,
            "source_files_mirrored": len(mirrored),
            "manual_three_copies_equal": True,
            "changelog_prior_entries_preserved": True,
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    check()
