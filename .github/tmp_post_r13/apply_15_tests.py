from pathlib import Path
p=Path('docs/testes/README.md')
t=p.read_text(encoding='utf-8')
a='## Transição ao trabalho — preparação em 11/09/2026\n'
b='''## Estado local/documental pós-R13 — 14/09/2026

A iniciativa de READMEs R00–R13 foi encerrada localmente com 75/75 objetos operacionais, 3/3 exemplares e zero pendências. Esse fechamento não altera retroativamente as rodadas Databricks abaixo: publicação, smoke e testes conversacionais continuam valendo apenas para o ambiente e a data em que foram observados.

'''+a
assert a in t and 'Estado local/documental pós-R13' not in t
t=t.replace(a,b,1)
p.write_text(t,encoding='utf-8')
