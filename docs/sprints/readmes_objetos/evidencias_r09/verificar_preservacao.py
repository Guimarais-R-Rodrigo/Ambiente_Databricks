"""Preservação R09: produto intacto e somente edições editoriais declaradas."""
from __future__ import annotations
import argparse, fnmatch, importlib.util, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OBJECTS=["curves_plotly","drift_detection","metrics_report","mlflow_run","performance_monitor"]
IGNORED_DIRS={"__pycache__",".pytest_cache",".ruff_cache"}; IGNORED_FILES=("*.pyc","*.pyo",".DS_Store")
def git_show(base,path): return subprocess.check_output(["git","show",f"{base}:{path}"],cwd=ROOT)
def ignored(rel): return any(p in IGNORED_DIRS for p in rel.parts) or any(fnmatch.fnmatch(rel.name,p) for p in IGNORED_FILES)
def scope(rel): return rel==Path(".assistant_instructions.md") or (rel.parts and rel.parts[0]==".assistant")
def load_apply():
    path=ROOT/"docs/sprints/readmes_objetos/evidencias_r09/aplicar_r09.py"
    spec=importlib.util.spec_from_file_location("aplicar_r09",path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def normalize_notebook(raw: bytes, obj: str, edits) -> bytes:
    text=raw.decode("utf-8")
    for old,new in reversed(edits):
        assert text.count(new)==1,(obj,"new",text.count(new),new[:80])
        text=text.replace(new,old)
    return text.encode("utf-8")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--base",default="d5945e04328609878f63857cc15cf5e5039b3e75"); base=ap.parse_args().base
    mod=load_apply()
    for obj in OBJECTS:
        for name in (f"{obj}.py","__init__.py"):
            path=f"ambiente_fonte/.assistant/hub_snippets/ml/{obj}/{name}"; assert (ROOT/path).read_bytes()==git_show(base,path),path
        path=f"ambiente_fonte/.assistant/hub_snippets/ml/{obj}/exemplo_{obj}.py"
        current=(ROOT/path).read_bytes(); restored=normalize_notebook(current,obj,mod.EDITS[obj]); assert restored==git_show(base,path),path
    # Catálogo e índice só podem ter a inserção R09 declarada.
    catalog=ROOT/"ambiente_fonte/.assistant/hub_snippets/README.md"; text=catalog.read_text(encoding="utf-8"); assert text.count(mod.CAT_NEW)==1; assert text.replace(mod.CAT_NEW,mod.CAT_OLD).encode()==git_show(base,"ambiente_fonte/.assistant/hub_snippets/README.md")
    index=ROOT/"docs/sprints/readmes_objetos/README.md"; text=index.read_text(encoding="utf-8"); assert text.count(mod.INDEX_NEW)==1; assert text.replace(mod.INDEX_NEW,mod.INDEX_OLD).encode()==git_show(base,"docs/sprints/readmes_objetos/README.md")
    prior=subprocess.check_output(["git","ls-tree","-r","--name-only",base,"ambiente_fonte/.assistant/hub_snippets"],cwd=ROOT,text=True).splitlines()
    prior=[p for p in prior if p.endswith("/README.md") and p!="ambiente_fonte/.assistant/hub_snippets/README.md"]
    for path in prior: assert (ROOT/path).read_bytes()==git_show(base,path),path
    old=json.loads(git_show(base,"docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json")); new=json.loads((ROOT/"docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json").read_text())
    expected={f"hub_snippets/ml/{o}" for o in OBJECTS}; assert set(old["pending"])-set(new["pending"])==expected; assert not(set(new["pending"])-set(old["pending"]))
    for key,val in new["pending"].items(): assert val==old["pending"][key],key
    canonical=(ROOT/"ambiente_fonte/.assistant/MANUAL_TECNICO.md").read_bytes(); assert canonical==(ROOT/"MANUAL_TECNICO.md").read_bytes(); assert canonical==(ROOT/"Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md").read_bytes()
    source=ROOT/"ambiente_fonte"; target=ROOT/"Novo_Ambiente_Simulado/Users/usuario-free"
    allsrc=sorted(p.relative_to(source) for p in source.rglob("*") if p.is_file()); outside=[r for r in allsrc if not scope(r)]; assert set(outside)=={Path("README.md")},outside
    src=[r for r in allsrc if scope(r) and not ignored(r)]; dst=sorted(p.relative_to(target) for p in target.rglob("*") if p.is_file()); assert set(src)==set(dst),(sorted(set(src)-set(dst)),sorted(set(dst)-set(src)))
    for rel in src: assert (source/rel).read_bytes()==(target/rel).read_bytes(),str(rel)
    changed=subprocess.check_output(["git","diff","--name-only",base,"--","docs/sprints/sistema_temas",".github/workflows/temas-v00-ci.yml",".github/workflows/temas-v01-ci.yml",".github/workflows/temas-v02-ci.yml",".github/workflows/temas-v03-ci.yml",".github/workflows/temas-v04-ci.yml"],cwd=ROOT,text=True).splitlines(); assert not changed,changed
    print(f"PASS: 10 implementação/fachada byte a byte; 5 notebooks equivalentes à base após reverter apenas as edições autorizadas; {len(prior)} READMEs anteriores intactos; 5 pendências removidas; {len(src)} arquivos publicáveis espelhados.")
if __name__=="__main__": main()
