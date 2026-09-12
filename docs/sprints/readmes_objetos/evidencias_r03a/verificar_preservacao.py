"""Conferência datada de preservação R03-A contra a main integrada.
Não interpreta aprovação do usuário como auditoria independente.
"""
from pathlib import Path
import ast,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[4]
BASE='5493f7db68f397ad7040485cb09bad53eb79be74'
PARALLEL_BASE='b88a9ccdde6e61892bc25eb7cf4f4b2577badb23'
PREFIX='ambiente_fonte/.assistant/'
OBJECTS=['constants/colors','constants/emojis','constants/styles','testing/fixtures','visual/badge','visual/divider','visual/kpi_card']

def old(path):
 return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def listed():
 return subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
def same(path):
 assert (ROOT/path).read_bytes()==old(path),path

def outputs(text):
 return re.findall(r'(?ms)^# MAGIC ```text\n.*?^# MAGIC ```\s*$',text)
def magics(text):
 # Everything executable in MAGIC cells, including multiline SQL/python directives;
 # markdown cells alone may change. Databricks cells start at COMMAND markers.
 result=[]
 for cell in text.split('# COMMAND ----------'):
  magic=[l for l in cell.splitlines() if l.startswith('# MAGIC')]
  if magic and not magic[0].startswith('# MAGIC %md'): result.append('\n'.join(magic))
 return result

checks={};paths=listed()
# All helper Python files unchanged except seven documentation examples.
nb={PREFIX+'hub_snippets/'+o+'/exemplo_'+o.split('/')[-1]+'.py' for o in OBJECTS}
helper_py=[p for p in paths if p.startswith(PREFIX+('hub_snippets/')) or p.startswith(PREFIX+'hub_scripts/')]
helper_py=[p for p in helper_py if p.endswith('.py') and p not in nb]
for p in helper_py:same(p)
checks['python_helpers_and_other_examples_unchanged']=len(helper_py)
for p in sorted(nb):
 a=old(p).decode();b=(ROOT/p).read_text()
 assert ast.dump(ast.parse(a),include_attributes=False)==ast.dump(ast.parse(b),include_attributes=False),p+' AST'
 assert outputs(a)==outputs(b),p+' historical output'
 assert magics(a)==magics(b),p+' executable magic'
 assert b.startswith('# Databricks notebook source\n'),p+' marker'
checks['seven_notebooks_AST_magic_outputs_preserved']=len(nb)
# Previously documented objects change only version marker.
accepted=[]
for p in paths:
 if p.startswith(PREFIX) and p.endswith('/README.md'):
  a=old(p).decode()
  if '<!-- readme-objeto: 0.1.0-candidata -->' in a:
   b=(ROOT/p).read_text()
   assert b==a.replace('<!-- readme-objeto: 0.1.0-candidata -->','<!-- readme-objeto: 1.0.0 -->'),p
   accepted.append(p)
assert len(accepted)==9,accepted
checks['previous_readmes_only_version_changed']=len(accepted)
protected=[p for p in paths if p.startswith((PREFIX+'skills/',PREFIX+'hub_readmes_visual_assets/','novas_funcionalidades/','tools/','.github/workflows/'))]
for p in protected:
 if p=='tools/README.md':
  assert (ROOT/p).read_bytes()==subprocess.check_output(['git','show',PARALLEL_BASE+':'+p],cwd=ROOT),p
 else:same(p)
# Every V00 addition/change other than the two shared conflict resolutions stays byte-identical.
parallel_paths=subprocess.check_output(['git','diff','--name-only',BASE,PARALLEL_BASE],cwd=ROOT,text=True).splitlines()
parallel_paths=[p for p in parallel_paths if p not in ('CHANGELOG.md','README.md')]
for p in parallel_paths:
 assert (ROOT/p).read_bytes()==subprocess.check_output(['git','show',PARALLEL_BASE+':'+p],cwd=ROOT),p
checks['v00_files_preserved']=len(parallel_paths)
checks['v00_base']=PARALLEL_BASE
checks['protected_skills_assets_tools_workflows_experiments']=len(protected)
forms=[p for p in paths if p.startswith(PREFIX+'hub_prompts/') and p.endswith('.md') and not p.endswith('/README.md')]
for p in forms:same(p)
checks['prompt_forms_unchanged']=len(forms)
ctrl='docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json'
a=json.loads(old(ctrl));b=json.loads((ROOT/ctrl).read_text())
assert set(a['pending'])-set(b['pending'])=={'hub_snippets/'+o for o in OBJECTS}
assert not set(b['pending'])-set(a['pending'])
assert all(a['pending'][p]==v for p,v in b['pending'].items())
assert a['base_commit']==b['base_commit'] and b['template_version']=='1.0.0'
assert len(b['pending'])==61
checks['migration_exemptions_removed']=7
# same teaching contract numbered section content, stable intro separately recorded.
p=PREFIX+'hub_padroes/readme/template_objeto.md'
a=old(p).decode();b=(ROOT/p).read_text()
assert a[a.index('## 1. O que é?'):]==b[b.index('## 1. O que é?'):]
checks['fifteen_section_contract_unchanged']=True
p='docs/decisions/ADR-0012-readmes-de-objeto.md';assert (ROOT/p).read_bytes().startswith(old(p))
same('docs/decisions/ADR-0011-concierge-hub.md')
checks['adr_history_preserved']=True
# Mirror checks after renderer: all source bytes, not handwritten deriveds.
source=ROOT/'ambiente_fonte';target=ROOT/'Novo_Ambiente_Simulado/Users/usuario-free'
count=0
for p in source.rglob('*'):
 if not p.is_file() or '__pycache__' in p.parts or p == source/'README.md':continue
 dest=target/p.relative_to(source)
 assert dest.exists() and p.read_bytes()==dest.read_bytes(),str(p.relative_to(ROOT))+' mirror'
 count+=1
assert (ROOT/'MANUAL_TECNICO.md').read_bytes()==(source/'.assistant/MANUAL_TECNICO.md').read_bytes()
checks['source_files_mirrored']=count
print(json.dumps({'base':BASE,'status':'PASS','checks':checks},ensure_ascii=False,indent=2))
