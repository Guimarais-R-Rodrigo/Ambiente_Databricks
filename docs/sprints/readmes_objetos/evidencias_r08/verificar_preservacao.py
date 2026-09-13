"""Preservação R08 contra a base integrada pós-R07."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OBJECTS = [
    "autoencoder_anomaly",
    "cluster_profiling",
    "clustering_suite",
    "explainability_report",
    "shap_explainer",
    "umap_viz",
]


def git_show(base: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{base}:{path}"], cwd=ROOT)


def executable_notebook_bytes(raw: bytes) -> bytes:
    lines = raw.decode("utf-8").splitlines()
    kept = [line for line in lines if not line.startswith("# MAGIC")]
    return ("\n".join(kept) + "\n").encode("utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="b73bbb91961f9ba5f9031d648c42ec0891b63347")
    args = ap.parse_args()
    base = args.base

    # Implementações e fachadas da R08: byte a byte.
    for obj in OBJECTS:
        for name in (f"{obj}.py", "__init__.py"):
            path = f"ambiente_fonte/.assistant/hub_snippets/ml/{obj}/{name}"
            current = (ROOT / path).read_bytes()
            assert current == git_show(base, path), path

    # Notebooks: nenhuma linha executável/magic não-Markdown pode mudar.
    for obj in OBJECTS:
        path = f"ambiente_fonte/.assistant/hub_snippets/ml/{obj}/exemplo_{obj}.py"
        current = executable_notebook_bytes((ROOT / path).read_bytes())
        old = executable_notebook_bytes(git_show(base, path))
        assert current == old, path

    # READMEs de objetos já entregues antes da R08 não podem derivar.
    prior = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", base, "ambiente_fonte/.assistant/hub_snippets"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    prior_readmes = [
        p for p in prior
        if p.endswith("/README.md") and p != "ambiente_fonte/.assistant/hub_snippets/README.md"
    ]
    for path in prior_readmes:
        assert (ROOT / path).read_bytes() == git_show(base, path), path

    # Exatamente as seis dispensas R08 saíram; as demais são idênticas.
    old_control = json.loads(git_show(base, "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"))
    new_control = json.loads((ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json").read_text(encoding="utf-8"))
    expected_removed = {f"hub_snippets/ml/{o}" for o in OBJECTS}
    removed = set(old_control["exemptions"]) - set(new_control["exemptions"])
    added = set(new_control["exemptions"]) - set(old_control["exemptions"])
    assert removed == expected_removed, (removed, expected_removed)
    assert not added, added
    for key in new_control["exemptions"]:
        assert new_control["exemptions"][key] == old_control["exemptions"][key], key

    # Manual: fonte canônica, cópia raiz e simulado idênticos.
    canonical = (ROOT / "ambiente_fonte/.assistant/MANUAL_TECNICO.md").read_bytes()
    assert canonical == (ROOT / "MANUAL_TECNICO.md").read_bytes()
    assert canonical == (ROOT / "Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md").read_bytes()

    # O simulado deve ser espelho do produto, nunca uma edição paralela.
    source = ROOT / "ambiente_fonte"
    target = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free"
    source_files = sorted(p.relative_to(source) for p in source.rglob("*") if p.is_file())
    target_files = sorted(p.relative_to(target) for p in target.rglob("*") if p.is_file())
    assert source_files == target_files, (len(source_files), len(target_files))
    for rel in source_files:
        assert (source / rel).read_bytes() == (target / rel).read_bytes(), str(rel)

    # Sistema de Temas V00–V04 é trabalho paralelo já integrado, não escopo R08.
    changed_temas = subprocess.check_output(
        ["git", "diff", "--name-only", base, "--", "docs/sprints/sistema_temas", ".github/workflows/temas-v00-ci.yml", ".github/workflows/temas-v01-ci.yml", ".github/workflows/temas-v02-ci.yml", ".github/workflows/temas-v03-ci.yml", ".github/workflows/temas-v04-ci.yml"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    assert not changed_temas, changed_temas

    print(f"PASS: 12 implementação/fachada preservadas; 6 notebooks executáveis preservados; {len(prior_readmes)} READMEs anteriores intactos; 6 dispensas removidas; {len(source_files)} arquivos fonte espelhados no simulado.")


if __name__ == "__main__":
    main()
