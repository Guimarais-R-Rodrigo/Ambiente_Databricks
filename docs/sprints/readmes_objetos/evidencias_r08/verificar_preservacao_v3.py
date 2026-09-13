"""Preservação R08 alinhada ao escopo publicado por tools/render_simulado.py."""
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OBJECTS = [
    "autoencoder_anomaly", "cluster_profiling", "clustering_suite",
    "explainability_report", "shap_explainer", "umap_viz",
]
IGNORED_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache"}
IGNORED_FILES = ("*.pyc", "*.pyo", ".DS_Store")


def git_show(base: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{base}:{path}"], cwd=ROOT)


def executable_notebook_bytes(raw: bytes) -> bytes:
    lines = raw.decode("utf-8").splitlines()
    kept = [line for line in lines if not line.startswith("# MAGIC")]
    return ("\n".join(kept) + "\n").encode("utf-8")


def ignored(rel: Path) -> bool:
    if any(part in IGNORED_DIRS for part in rel.parts):
        return True
    return any(fnmatch.fnmatch(rel.name, pat) for pat in IGNORED_FILES)


def renderer_scope(rel: Path) -> bool:
    """Espelha o contrato atual do renderer: instruções + árvore .assistant/."""
    return rel == Path(".assistant_instructions.md") or (rel.parts and rel.parts[0] == ".assistant")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="b73bbb91961f9ba5f9031d648c42ec0891b63347")
    base = ap.parse_args().base

    for obj in OBJECTS:
        for name in (f"{obj}.py", "__init__.py"):
            path = f"ambiente_fonte/.assistant/hub_snippets/ml/{obj}/{name}"
            assert (ROOT / path).read_bytes() == git_show(base, path), path

    for obj in OBJECTS:
        path = f"ambiente_fonte/.assistant/hub_snippets/ml/{obj}/exemplo_{obj}.py"
        assert executable_notebook_bytes((ROOT / path).read_bytes()) == executable_notebook_bytes(git_show(base, path)), path

    prior = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", base, "ambiente_fonte/.assistant/hub_snippets"],
        cwd=ROOT, text=True,
    ).splitlines()
    prior_readmes = [p for p in prior if p.endswith("/README.md") and p != "ambiente_fonte/.assistant/hub_snippets/README.md"]
    for path in prior_readmes:
        assert (ROOT / path).read_bytes() == git_show(base, path), path

    old_control = json.loads(git_show(base, "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"))
    new_control = json.loads((ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json").read_text(encoding="utf-8"))
    expected_removed = {f"hub_snippets/ml/{o}" for o in OBJECTS}
    removed = set(old_control["pending"]) - set(new_control["pending"])
    added = set(new_control["pending"]) - set(old_control["pending"])
    assert removed == expected_removed, (removed, expected_removed)
    assert not added, added
    for key in new_control["pending"]:
        assert new_control["pending"][key] == old_control["pending"][key], key

    canonical = (ROOT / "ambiente_fonte/.assistant/MANUAL_TECNICO.md").read_bytes()
    assert canonical == (ROOT / "MANUAL_TECNICO.md").read_bytes()
    assert canonical == (ROOT / "Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md").read_bytes()

    source = ROOT / "ambiente_fonte"
    target = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free"
    source_all = sorted(p.relative_to(source) for p in source.rglob("*") if p.is_file())
    outside_scope = [rel for rel in source_all if not renderer_scope(rel)]
    assert set(outside_scope) == {Path("README.md")}, outside_scope

    scoped = [rel for rel in source_all if renderer_scope(rel)]
    excluded = [rel for rel in scoped if ignored(rel)]
    source_files = [rel for rel in scoped if not ignored(rel)]
    target_files = sorted(p.relative_to(target) for p in target.rglob("*") if p.is_file())
    missing = sorted(set(source_files) - set(target_files))
    extra = sorted(set(target_files) - set(source_files))
    print("FORA_DO_ESCOPO_RENDERER:", [str(x) for x in outside_scope])
    print("IGNORADOS_PELO_RENDERER:", [str(x) for x in excluded])
    print("AUSENTES_NO_SIMULADO:", [str(x) for x in missing])
    print("EXTRAS_NO_SIMULADO:", [str(x) for x in extra])
    assert not missing and not extra, (missing, extra)
    for rel in source_files:
        assert (source / rel).read_bytes() == (target / rel).read_bytes(), str(rel)

    changed_temas = subprocess.check_output(
        ["git", "diff", "--name-only", base, "--", "docs/sprints/sistema_temas",
         ".github/workflows/temas-v00-ci.yml", ".github/workflows/temas-v01-ci.yml",
         ".github/workflows/temas-v02-ci.yml", ".github/workflows/temas-v03-ci.yml",
         ".github/workflows/temas-v04-ci.yml"], cwd=ROOT, text=True,
    ).splitlines()
    assert not changed_temas, changed_temas

    print(
        f"PASS: 12 implementação/fachada preservadas; 6 notebooks executáveis preservados; "
        f"{len(prior_readmes)} READMEs anteriores intactos; 6 pendências removidas; "
        f"{len(source_files)} arquivos publicáveis espelhados; {len(excluded)} artefato(s) local(is) ignorado(s); "
        f"{len(outside_scope)} arquivo(s) de fonte fora do escopo do renderer."
    )


if __name__ == "__main__":
    main()
