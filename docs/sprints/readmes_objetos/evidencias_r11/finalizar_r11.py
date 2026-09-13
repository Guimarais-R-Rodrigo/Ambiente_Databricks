from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[4]
BASE='7ba5d386c30374c429114572ff5bc8e889d3ea7b'
P=ROOT/'ambiente_fonte/.assistant/hub_prompts'; D=ROOT/'docs/sprints/readmes_objetos'
A=['baseline_orchestration','explainability','monitoramento_modelo','pipeline','safra']
B=['auditoria_skills','comentar_notebook','novo_projeto','tutor_explicar']; N=A+B

def write(p,t): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(t,encoding='utf-8')
def finish():
 c=D/'CONTROLE_MIGRACAO.json'; data=json.loads(c.read_text(encoding='utf-8')); exp={f'hub_prompts/{n}' for n in N}
 if set(data['pending']) not in (exp,set()): raise RuntimeError(set(data['pending']))
 data['pending']={}; data['phase']='complete'; write(c,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 cat=P/'README.md'; text=cat.read_text(encoding='utf-8')
 for n in N:
  old=f'- **Arquivos:** `hub_prompts/{n}/{n}.md` · `hub_prompts/{n}/exemplo_{n}.py`'; new=old+f' · [README local]({n}/README.md)'
  if new not in text:
   if text.count(old)!=1: raise RuntimeError(('catalogo',n))
   text=text.replace(old,new,1)
 write(cat,text)
 idx=D/'README.md'; s=idx.read_text(encoding='utf-8'); p=s.find('O contrato vigente é **1.0.0**.'); e=s.find('\n\nOs relatórios anteriores',p)
 if p<0 or e<0: raise RuntimeError('estado iniciativa')
 new=('O contrato vigente é **1.0.0**. A R10 foi aceita e integrada pelo PR nº 30 no commit `7ba5d386`. '
      'A R11 documenta os nove Hub Prompts restantes em lotes A/B. A candidata busca fechar a migração estrutural em **75/75 operacionais e 3/3 exemplares, com 0 pendências**, sujeita ao validador real.\n\n'
      'Consulte o [relatório R11](RELATORIO_R11.md), a [matriz nominal](MATRIZ_ALTERACOES_R11.md) e os [achados](ACHADOS_R11.md). '
      'Fechar `pending` encerra a migração estrutural de READMEs, não homologação Databricks nem etapas posteriores da iniciativa.')
 write(idx,s[:p]+new+s[e:])
 sr=ROOT/'docs/sprints/README.md'; st=sr.read_text(encoding='utf-8')
 if '### READMEs R11' not in st: write(sr,st.rstrip()+"\n\n### READMEs R11\nA R10 foi integrada pelo PR #30 (`7ba5d386`). A R11 cobre os nove Hub Prompts restantes e busca fechar a migração estrutural em 75/75, sem antecipar homologação ou etapas posteriores.\n")
 rr=ROOT/'README.md'; rt=rr.read_text(encoding='utf-8'); old='> **READMEs R10 — candidata:** seis guias de Hub Prompts; cobertura alvo 66/75, sujeita ao freeze e aceite editorial.'
 newr='> **READMEs R10 — integrada:** seis guias de Hub Prompts foram aceitos e integrados pelo PR #30 (`7ba5d386`).\n>\n> **READMEs R11 — candidata:** nove guias finais de Hub Prompts; cobertura alvo 75/75 e zero pendências estruturais, sujeita ao freeze e aceite editorial.'
 if old in rt: write(rr,rt.replace(old,newr,1))
 report=f'''# Relatório R11 — fechamento da migração de READMEs\n\n## Escopo\nR11-A: {', '.join('`'+x+'`' for x in A)}.\n\nR11-B: {', '.join('`'+x+'`' for x in B)}.\n\n## Base e meta\nBase: `{BASE}` após merge da R10. Estado inicial: 66/75 operacionais e 9 pendências. Meta candidata: **75/75 operacionais, 3/3 exemplares e 0 pendências**, com `phase=complete`, subordinada ao validador.\n\n## Preservação\nOs nove briefings `.md` permanecem byte a byte iguais à base. Os notebooks recebem backlink e somente erratas Markdown declaradas; código executável e outputs existentes ficam preservados.\n\n## Limites\nFechar a migração estrutural não equivale a publicação no workspace, homologação Databricks/Genie Code, auditoria independente ou encerramento automático das etapas posteriores.\n'''; write(D/'RELATORIO_R11.md',report)
 mat='# Matriz de alterações R11\n\n| Lote | Objeto | README | Briefing | Notebook |\n|---|---|---|---|---|\n'+ '\n'.join(f"| {'A' if n in A else 'B'} | `{n}` | novo 1.0.0 | preservado | backlink"+(' + errata Markdown' if n in {'monitoramento_modelo','auditoria_skills','comentar_notebook','tutor_explicar'} else '')+' |' for n in N)+'\n'; write(D/'MATRIZ_ALTERACOES_R11.md',mat)
 ach='''# Achados R11\n\n1. Os nove objetos restantes são prompts; resposta real continua dependente de interação humana.\n2. `monitoramento_modelo` citava nomes de tabela incorretos na prosa; o código já gravava duas tabelas `monitor_*`.\n3. `comentar_notebook` preservava uma dívida histórica de onze notebooks sem saída colada, incompatível com o gate atual de zero.\n4. Exemplos de leitura usavam a frase genérica `cria nenhuma`; a R11 passa a descrevê-los como leitura sem tabela.\n5. `tutor_explicar` fixava Spark 4.1 no exemplo; a versão passa a ser confirmada no ambiente real.\n'''; write(D/'ACHADOS_R11.md',ach)
 write(D/'RUBRICA_R11.json','{\n  "sprint": "R11",\n  "contrato": "1.0.0",\n  "objetos": 9,\n  "meta": "75/75",\n  "gates": ["estrutura", "preservacao", "ci_local", "renderer"],\n  "nao_coberto": ["genie_code_real", "runtime_databricks", "publicacao_workspace", "auditoria_independente", "aceite_editorial"]\n}\n')
 ev=D/'evidencias_r11/FREEZE_R11.txt'
 if not ev.exists(): write(ev,f'R11 freeze placeholder\nbase={BASE}\n')
 ch=ROOT/'CHANGELOG.md'; ct=ch.read_text(encoding='utf-8'); h='## 2026-09-13 — R11: fechamento da migração de READMEs (ChatGPT)'
 if h not in ct:
  anchor='Template: `.claude/templates/changelog-entry.md`.\n\n'; entry=h+'\n\n- Documenta os nove Hub Prompts restantes no contrato 1.0.0.\n- Preserva os nove briefings e limita notebooks a backlinks/erratas Markdown declaradas.\n- Fecha `pending` e muda o controle para `phase=complete`; meta estrutural 75/75 sujeita ao validador.\n- Sem publicação, homologação Databricks/Genie Code, auditoria independente, merge antecipado ou encerramento das etapas posteriores.\n\n'; write(ch,ct.replace(anchor,anchor+entry,1))
def snap(out):
 output=out.read_text(encoding='utf-8').strip()
 if 'APROVADO: 0 falha(s), 0 aviso(s)' not in output: raise RuntimeError('validator')
 p=ROOT/'README.md'; t=p.read_text(encoding='utf-8'); s=t.find('### Estado verificável do gate local'); f=t.find('```text\n',s); e=t.find('\n```',f)
 if min(s,f,e)<0: raise RuntimeError('snapshot')
 write(p,t[:f+8]+output+t[e:])
if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('--snapshot',type=Path); a=ap.parse_args(); snap(a.snapshot) if a.snapshot else finish()
