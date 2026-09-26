from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[4]
BASE='7ba5d386c30374c429114572ff5bc8e889d3ea7b'
N='baseline_orchestration explainability monitoramento_modelo pipeline safra auditoria_skills comentar_notebook novo_projeto tutor_explicar'.split()

def out(*a): return subprocess.check_output(a,cwd=ROOT,text=True)
def main():
 expected={'ambiente_fonte/.assistant/hub_prompts/README.md'}
 expected|={f'ambiente_fonte/.assistant/hub_prompts/{n}/README.md' for n in N}
 expected|={f'ambiente_fonte/.assistant/hub_prompts/{n}/exemplo_{n}.py' for n in N}
 got=set(out('git','diff','--cached','--name-only',BASE,'--','ambiente_fonte/.assistant').splitlines())
 assert got==expected,(sorted(got-expected),sorted(expected-got))
 for n in N:
  prompt=f'ambiente_fonte/.assistant/hub_prompts/{n}/{n}.md'
  assert not out('git','diff','--name-only',BASE,'--',prompt).strip(),prompt
  p=ROOT/f'ambiente_fonte/.assistant/hub_prompts/{n}/exemplo_{n}.py'
  assert 'Guia local: [`README.md`](./README.md)' in p.read_text(encoding='utf-8'),p
  old=out('git','show',f'{BASE}:{p.relative_to(ROOT).as_posix()}')
  new=p.read_text(encoding='utf-8')
  exe=lambda s:'\n'.join(x for x in s.splitlines() if not x.startswith('# MAGIC'))
  assert exe(old)==exe(new),p
 ctl=json.loads((ROOT/'docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json').read_text())
 assert ctl['phase']=='complete',ctl
 assert ctl['pending']=={},ctl
 subprocess.check_call(['diff','-qr','ambiente_fonte/.assistant','Novo_Ambiente_Simulado/Users/usuario-free/.assistant'],cwd=ROOT)
 subprocess.check_call(['cmp','ambiente_fonte/.assistant_instructions.md','Novo_Ambiente_Simulado/Users/usuario-free/.assistant_instructions.md'],cwd=ROOT)
 subprocess.check_call(['git','diff','--cached','--check'],cwd=ROOT)
 subprocess.check_call(['git','diff','--check'],cwd=ROOT)
 print('PASS R11: 9 briefings preservados; 9 notebooks com codigo nao-Markdown preservado; source diff fechado; phase=complete; pending=0; espelho equivalente.')
if __name__=='__main__': main()
