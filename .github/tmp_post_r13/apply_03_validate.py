from pathlib import Path
p=Path('.claude/skills/validar-assistant/SKILL.md')
t=p.read_text(encoding='utf-8')
t=t.replace('conjunto exato das 13 pastas','conjunto exato das 14 pastas',1)
a='| Links fora da raiz analisada | sim | idem, para `README.md`, `docs/` e `.claude/` |\n'
r='| READMEs de objeto | sim | contrato 1.0.0; 75/75 operacionais, 3/3 exemplares e `pending=0`; novos objetos sem README reprovam |\n'
assert a in t and r not in t
t=t.replace(a,a+r,1)
p.write_text(t,encoding='utf-8')
