from pathlib import Path
p=Path('ambiente_fonte/.assistant/hub_scripts/README.md')
t=p.read_text(encoding='utf-8')
root=Path('ambiente_fonte/.assistant/hub_scripts')
names=sorted(x.name for x in root.iterdir() if x.is_dir() and (x/'README.md').is_file())
for name in names:
    link=f'- **Guia local:** [{name}: guia local]({name}/README.md)\n'
    if link in t:
        continue
    marker=f'#### `{name}`'
    i=t.find(marker); assert i>=0, name
    j=t.find('\n\n',i); assert j>=0
    t=t[:j+2]+link+'\n'+t[j+2:]
old='''**Equivalente textual da figura:** a pasta contém `__init__.py`, que expõe a interface pública; `<nome>.py`, que contém a implementação; e `exemplo_<nome>.py`, que demonstra a chamada em formato de notebook. A saída não é universal: conforme o utilitário, pode ser dicionário, DataFrame Spark, texto YAML/JSON ou lista de violações.'''
new='''**Equivalente textual da figura:** o núcleo executável contém `__init__.py`, implementação e `exemplo_<nome>.py`; cada objeto operacional possui também `README.md`, que explica adequação, requisitos, efeitos, limites e interpretação antes da execução. A saída não é universal: conforme o utilitário, pode ser dicionário, DataFrame Spark, texto YAML/JSON ou lista de violações.'''
assert t.count(old)==1
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8')
