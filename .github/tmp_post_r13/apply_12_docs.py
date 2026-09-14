from pathlib import Path
p=Path('docs/README.md')
t=p.read_text(encoding='utf-8')
t=t.replace('“Como está a migração dos READMEs de objeto?”','“Qual é o estado final dos READMEs de objeto?”',1)
t=t.replace('## Estado vigente\n\nEm 29/08/2026,','## Estado documental/local atual\n\nA iniciativa R00–R13 de READMEs por objeto foi encerrada em 14/09/2026 com 75/75 objetos operacionais, 3/3 exemplares, zero pendências e auditoria final local `A0_light`. Esse fechamento não publica nem homologa Databricks/Genie Code.\n\n## Última evidência Databricks real registrada\n\nEm 29/08/2026,',1)
p.write_text(t,encoding='utf-8')
