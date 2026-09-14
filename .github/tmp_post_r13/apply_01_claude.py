from pathlib import Path
p=Path('CLAUDE.md')
t=p.read_text(encoding='utf-8')
old="""- README didático por pasta de objeto: `ADR-0012`, ratificado em 2026-09-12;
  contrato 1.0.0 estabilizado após aceite do piloto. R03-A/R03-B foram integradas
  pelo PR nº 13, R04-A pelo PR nº 17 e R04-B pelo PR nº 18. As duas levas R04
  foram reconciliadas com o Sistema de Temas antes do merge. Estado e retomada:
  `docs/sprints/readmes_objetos/README.md`."""
new="""- README didático por pasta de objeto: `ADR-0012`, ratificado em 2026-09-12;
  contrato **1.0.0** vigente. A iniciativa própria R00–R13 foi aceita e encerrada
  no Git após PR #33 (`b0e953cc`) e fechamento documental PR #34 (`99e01012`):
  **75/75 operacionais, 3/3 exemplares e 0 pendências**. A auditoria final é
  `A0_light`; não equivale a publicação nem homologação Databricks/Genie Code.
  Estado vigente: `docs/sprints/readmes_objetos/README.md`."""
assert t.count(old)==1, t.count(old)
t=t.replace(old,new,1)
start='### Estado da migração de READMEs — R04-B'
pos=t.find(start); assert pos>=0
newtail="""### Estado vigente dos READMEs de objeto
A migração estrutural terminou na R11 e a iniciativa R00–R13 foi encerrada após a
auditoria final R13 e o fechamento documental pós-merge. O contrato vigente é
`readme-objeto: 1.0.0`; todos os 75 objetos operacionais possuem README, os três
exemplares permanecem separados e `CONTROLE_MIGRACAO.json` está em
`phase=complete` com `pending={}`.

Para manutenção futura, todo novo snippet, script ou prompt precisa entrar já com
README no mesmo contrato; reintroduzir dispensa é regressão. Use o
[estado vigente](docs/sprints/readmes_objetos/README.md), o
[relatório final R13](docs/sprints/readmes_objetos/RELATORIO_R13.md) e o
[contrato editorial](ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md).
Cobertura estrutural não é homologação de runtime, publicação no workspace nem
auditoria independente.
"""
p.write_text(t[:pos]+newtail,encoding='utf-8')
