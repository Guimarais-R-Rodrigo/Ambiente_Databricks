from pathlib import Path
p=Path('ambiente_fonte/README.md')
t=p.read_text(encoding='utf-8')
a='O produto inclui [um molde de README local](.assistant/hub_padroes/readme/template_objeto.md)\npara snippets, scripts e prompts.'
b='Os 75 objetos operacionais atuais possuem README local. Novos snippets, scripts e prompts usam o [molde 1.0.0](.assistant/hub_padroes/readme/template_objeto.md) e o checklist editorial.'
assert a in t
t=t.replace(a,b,1)
p.write_text(t,encoding='utf-8')
