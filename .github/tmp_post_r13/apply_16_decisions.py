from pathlib import Path
p=Path('docs/decisions/README.md')
t=p.read_text(encoding='utf-8')
a='| [0012](ADR-0012-readmes-de-objeto.md) | README didático por objeto; transição controlada | aceito em 2026-09-12; ratificação anexada |'
b='| [0012](ADR-0012-readmes-de-objeto.md) | README didático por objeto; transição controlada | aceito e implementado; R00–R13 encerrada em 2026-09-14 |'
assert a in t
t=t.replace(a,b,1)
p.write_text(t,encoding='utf-8')
