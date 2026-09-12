"""Guarda datada R04-A: preservação funcional/documental contra a main integrada."""
from __future__ import annotations
import ast,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
BASE='1be947b0a62c3b0b85fa3cd5692f474b9066d85f'
PREFIX='ambiente_fonte/.assistant/'
OBJECTS=['spark/date_features','spark/join_diagnostics','spark/null_summary','spark/psi_calculator','spark/safe_display','spark/smart_sample']

def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
def before(path): return git('show',BASE+':'+path)
def unchanged(path): assert (ROOT/path).read_bytes()==before(path),path

def magics(text):
    result=[]
    for cell in text.split('# COMMAND ----------'):
        lines=[line for line in cell.splitlines() if line.startswith('# MAGIC')]
        if lines and not lines[0].startswith('# MAGIC %md'): result.append('\n'.join(lines))
    return result

def check():
    paths=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
    notebooks={PREFIX+'hub_snippets/'+obj+'/exemplo_'+obj.split('/')[-1]+'.py' for obj in OBJECTS}
    python=[p for p in paths if p.startswith(PREFIX) and p.endswith('.py') and p not in notebooks]
    for p in python: unchanged(p)
    for p in sorted(notebooks):
        a=before(p).decode(); b=(ROOT/p).read_text()
        assert ast.dump(ast.parse(a),include_attributes=False)==ast.dump(ast.parse(b),include_attributes=False),p+' AST'
        assert magics(a)==magics(b),p+' magic executable'
        pattern=r'(?ms)^# MAGIC ```text\n.*?^# MAGIC ```\s*$'
        assert re.findall(pattern,a)==re.findall(pattern,b),p+' output'
        assert [l for l in a.splitlines() if l.strip() and not l.startswith('# MAGIC')]==[l for l in b.splitlines() if l.strip() and not l.startswith('# MAGIC')],p+' executable/comment cells'
    readmes=[p for p in paths if p.startswith(PREFIX) and p.endswith('/README.md') and b'<!-- readme-objeto:' in before(p)]
    assert len(readmes)==22,len(readmes)
    for p in readmes: unchanged(p)
    protected=[p for p in paths if p.startswith((PREFIX+'skills/',PREFIX+'hub_padroes/',PREFIX+'hub_readmes_visual_assets/',
              'tools/','.github/workflows/','novas_funcionalidades/','docs/decisions/','docs/sprints/sistema_temas/'))]
    for p in protected: unchanged(p)
    forms=[p for p in paths if p.startswith(PREFIX+'hub_prompts/') and p.endswith('.md') and not p.endswith('/README.md')]
    for p in forms: unchanged(p)
    unchanged('ambiente_fonte/.assistant_instructions.md')
    ctrl='docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json'; a=json.loads(before(ctrl)); b=json.loads((ROOT/ctrl).read_text())
    removed={'hub_snippets/'+obj for obj in OBJECTS}
    assert set(a['pending'])-set(b['pending'])==removed
    assert not set(b['pending'])-set(a['pending']); assert len(b['pending'])==49
    assert all(v==a['pending'][p] for p,v in b['pending'].items())
    assert {k:v for k,v in a.items() if k!='pending'}=={k:v for k,v in b.items() if k!='pending'}
    original=before('CHANGELOG.md').decode(); current=(ROOT/'CHANGELOG.md').read_text()
    header=original[:original.index('## 2026-')]; history=original[original.index('## 2026-'):]
    assert current.startswith(header); assert current.endswith(history)
    source=ROOT/'ambiente_fonte'; target=ROOT/'Novo_Ambiente_Simulado/Users/usuario-free'; mirrored=[]
    for p in source.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p==source/'README.md': continue
        dest=target/p.relative_to(source); assert dest.is_file() and dest.read_bytes()==p.read_bytes(),str(p)+' mirror'; mirrored.append(str(p.relative_to(source)))
    derived=[str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()]
    assert set(derived)==set(mirrored),'extra/missing mirror'
    assert (ROOT/'MANUAL_TECNICO.md').read_bytes()==(source/'.assistant/MANUAL_TECNICO.md').read_bytes()
    print(json.dumps({'base':BASE,'status':'PASS','checks':{
      'product_python_unchanged':len(python),'six_notebooks_AST_magics_outputs_preserved':len(notebooks),
      'previous_object_readmes_unchanged':len(readmes),'protected_paths':len(protected),'prompt_forms_unchanged':len(forms),
      'migration_exemptions_removed':6,'pending':49,'source_files_mirrored':len(mirrored),
      'manual_three_copies_equal':True,'changelog_prior_entries_preserved':True}},ensure_ascii=False,indent=2))
if __name__=='__main__': check()
