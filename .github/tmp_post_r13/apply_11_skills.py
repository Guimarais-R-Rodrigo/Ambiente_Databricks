from pathlib import Path
p=Path('ambiente_fonte/.assistant/skills/README.md')
t=p.read_text(encoding='utf-8')
a='- **Templates:** `checklist-objeto-novo.md` e os moldes em `hub_padroes/`.\n'
b=a+'- **Documentação:** snippet, script ou prompt novo deve incluir README local no contrato 1.0.0.\n'
assert a in t
t=t.replace(a,b,1)
p.write_text(t,encoding='utf-8')
