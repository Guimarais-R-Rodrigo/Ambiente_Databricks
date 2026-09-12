"""Guarda datada R03-B: compara com a base real, sem editar arquivos."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[4]
BASE='c60f1e54743dc23ed60b32ad2260b9aa6a77af0a'
PREFIX='ambiente_fonte/.assistant/'
OBJECTS=['display/correlation_matrix','display/dataframe_styled','display/distribution_grid',
         'visual/index_generator','visual/section_header','visual/theme_plotly']


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def before(path):
    return git('show',BASE+':'+path)


def unchanged(path):
    assert (ROOT/path).read_bytes()==before(path),path


def magics(text):
    result=[]
    for cell in text.split('# COMMAND ----------'):
        lines=[line for line in cell.splitlines() if line.startswith('# MAGIC')]
        if lines and not lines[0].startswith('# MAGIC %md'):
            result.append('\n'.join(lines))
    return result


def check():
    paths=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
    notebooks={PREFIX+'hub_snippets/'+obj+'/exemplo_'+obj.split('/')[-1]+'.py' for obj in OBJECTS}
    python=[p for p in paths if p.startswith(PREFIX) and p.endswith('.py') and p not in notebooks]
    for p in python:
        unchanged(p)
    for p in sorted(notebooks):
        a=before(p).decode();b=(ROOT/p).read_text()
        assert ast.dump(ast.parse(a),include_attributes=False)==ast.dump(ast.parse(b),include_attributes=False),p+' AST'
        assert magics(a)==magics(b),p+' magic'
        pattern=r'(?ms)^# MAGIC ```text\n.*?^# MAGIC ```\s*$'
        assert re.findall(pattern,a)==re.findall(pattern,b),p+' output'
        # Além de AST: nenhum comentário de célula Python foi alterado.
        assert [l for l in a.splitlines() if l.strip() and not l.startswith('# MAGIC')]==[l for l in b.splitlines() if l.strip() and not l.startswith('# MAGIC')],p+' executable cells'
    readmes=[p for p in paths if p.startswith(PREFIX) and p.endswith('/README.md') and b'<!-- readme-objeto:' in before(p)]
    assert len(readmes)==16,readmes
    for p in readmes:
        unchanged(p)
    protected=[p for p in paths if p.startswith((PREFIX+'skills/',PREFIX+'hub_padroes/',PREFIX+'hub_readmes_visual_assets/',
          'tools/','.github/workflows/','novas_funcionalidades/','docs/decisions/','docs/sprints/sistema_temas/'))]
    for p in protected:
        unchanged(p)
    forms=[p for p in paths if p.startswith(PREFIX+'hub_prompts/') and p.endswith('.md') and not p.endswith('/README.md')]
    for p in forms:
        unchanged(p)
    unchanged('ambiente_fonte/.assistant_instructions.md')
    ctrl='docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json'
    a=json.loads(before(ctrl));b=json.loads((ROOT/ctrl).read_text())
    assert set(a['pending'])-set(b['pending'])=={'hub_snippets/'+obj for obj in OBJECTS}
    assert not set(b['pending'])-set(a['pending'])
    assert len(b['pending'])==55
    assert all(v==a['pending'][p] for p,v in b['pending'].items())
    assert {k:v for k,v in a.items() if k!='pending'}=={k:v for k,v in b.items() if k!='pending'}
    assert b['template_version']=='1.0.0'
    original=before('CHANGELOG.md').decode()
    current=(ROOT/'CHANGELOG.md').read_text()
    assert current.startswith(original[:original.index('## 2026-')])
    assert current.endswith(original[original.index('## 2026-'):])
    source=ROOT/'ambiente_fonte';target=ROOT/'Novo_Ambiente_Simulado/Users/usuario-free'
    mirrored=[]
    for p in source.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p==source/'README.md':
            continue
        dest=target/p.relative_to(source)
        assert dest.is_file() and dest.read_bytes()==p.read_bytes(),str(p)+' mirror'
        mirrored.append(str(p.relative_to(source)))
    derived=[str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()]
    assert set(derived)==set(mirrored),'extra/missing mirror'
    assert (ROOT/'MANUAL_TECNICO.md').read_bytes()==(source/'.assistant/MANUAL_TECNICO.md').read_bytes()
    result={'base':BASE,'status':'PASS','checks':{
       'product_python_unchanged':len(python),'six_notebooks_AST_magics_outputs_preserved':len(notebooks),
       'previous_object_readmes_unchanged':len(readmes),'protected_patterns_skills_assets_tools_ADRs_V00':len(protected),
       'prompt_forms_unchanged':len(forms),'migration_exemptions_removed':6,'pending':55,
       'source_files_mirrored':len(mirrored),'manual_three_copies_equal':True,'changelog_prior_entries_preserved':True}}
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    check()
