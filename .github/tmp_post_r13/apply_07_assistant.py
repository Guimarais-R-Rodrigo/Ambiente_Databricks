from pathlib import Path
p=Path('ambiente_fonte/.assistant/README.md')
t=p.read_text(encoding='utf-8')
a='Consulte o Hub Padrões em `.assistant/hub_padroes/README.md`.\n\n'
b=a+'### 📘 README local do recurso\n\nAo chegar a um snippet, script ou prompt concreto, leia primeiro o `README.md` da pasta. Ele orienta escolha, requisitos, efeitos, limites e interpretação; depois use o notebook de exemplo e a implementação ou briefing. O guia não equivale a homologação de runtime ou aprovação de negócio.\n\n'
assert t.count(a)==1
t=t.replace(a,b,1)
p.write_text(t,encoding='utf-8')
