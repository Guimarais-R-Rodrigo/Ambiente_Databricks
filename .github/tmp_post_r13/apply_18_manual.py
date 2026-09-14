from pathlib import Path
src=Path('ambiente_fonte/.assistant/MANUAL_TECNICO.md')
t=src.read_text(encoding='utf-8')
old='''**Base examinada:** código do commit `c5fdc61181c14124d653cf9e6222d9a402745949`, após a limpeza das pastas de rascunhos. As explicações sobre plataforma foram confrontadas com documentação oficial consultada em **11/09/2026**. Exemplos com dados são sintéticos. Uma saída esperada não é prova de execução em seu workspace; diferenças de versão, dependência e permissão precisam ser verificadas no destino.'''
new='''**Base documental e estrutural atual:** a iniciativa R00–R13 de READMEs foi encerrada no Git em `99e01012c26621539b4379ca301e4782765f68c0`, com 75/75 objetos operacionais, 3/3 exemplares e zero pendências. A R13 auditou coerência documental e regressões locais; não recertificou toda afirmação externa da plataforma. As explicações sobre Databricks continuam apoiadas na documentação oficial consultada em **11/09/2026** e devem ser verificadas novamente quando uma capacidade, interface ou versão puder ter mudado. Exemplos com dados são sintéticos; saída esperada não prova execução no workspace de destino.'''
assert t.count(old)==1, t.count(old)
t=t.replace(old,new,1)
src.write_text(t,encoding='utf-8')
Path('MANUAL_TECNICO.md').write_bytes(src.read_bytes())
