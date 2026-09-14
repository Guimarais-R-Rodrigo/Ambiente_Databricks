from pathlib import Path
p=Path('ambiente_fonte/.assistant/hub_snippets/README.md')
t=p.read_text(encoding='utf-8')
t=t.replace('O objeto\nnovo inclui também `README.md`, a camada humana de conceito e escolha; a\nmigração das pastas legadas é gradual:','Cada objeto operacional inclui também `README.md`, a camada humana de conceito e escolha. A migração estrutural foi encerrada na R13:',1)
for old,new in {
'#### 📘 Guias locais R05 — modelos tabulares':'#### 📘 Modelos tabulares',
'#### 📘 Guias locais R06 — séries e validação temporal':'#### 📘 Séries e validação temporal',
'#### 📘 Guias locais R07 — score, safra e sobrevivência':'#### 📘 Score, safra e sobrevivência',
'#### 📘 Guias locais R08 — clusters, anomalias e explicabilidade':'#### 📘 Clusters, anomalias e explicabilidade',
'#### 📘 Guias locais R09 — avaliação, drift e MLOps':'#### 📘 Avaliação, drift e MLOps',
}.items():
    t=t.replace(old,new)
a=t.find('## Guias locais por objeto')
assert a>=0
new='''## Guias locais por objeto

A migração estrutural está concluída: os 52 snippets operacionais possuem README local. Para descobrir recursos, use os seis índices de categoria: [constants](constants/README.md), [display](display/README.md), [ml](ml/README.md), [spark](spark/README.md), [testing](testing/README.md) e [visual](visual/README.md). Cada índice enumera os filhos reais da categoria e aponta para o guia do objeto.

O [contrato editorial](../hub_padroes/readme/template_objeto.md) continua obrigatório para novos snippets. Leia o README local antes do notebook de exemplo; o exemplo pode ter efeitos próprios mesmo quando o helper apenas lê. O Manual permanece o inventário integrado e a presença do guia não significa homologação de runtime.
'''
p.write_text(t[:a]+new,encoding='utf-8')
