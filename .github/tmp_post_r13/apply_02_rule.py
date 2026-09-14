from pathlib import Path
p=Path('.claude/rules/docs-e-readmes.md')
t=p.read_text(encoding='utf-8')
start='## README de objeto — R01'
pos=t.find(start); assert pos>=0
new="""## README de objeto — contrato vigente 1.0.0

A escala Objeto segue `ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md`
e o respectivo checklist editorial, conforme ADR-0012. A iniciativa R00–R13
encerrou a transição: existem **75/75 READMEs operacionais, 3/3 exemplares e zero
pendências estruturais**. `CONTROLE_MIGRACAO.json` permanece como evidência e
guarda de ratchet; não é backlog ativo.

A partir desse estado, todo novo snippet, script ou prompt precisa incluir seu
README na mesma mudança. Não crie dispensa automática nem reabra `pending`; uma
reintrodução é regressão e deve falhar no gate. O contrato 1.0.0 mantém quinze
seções para READMEs de objeto; índices, skills e outros documentos agregadores não
herdam mecanicamente esse formato.

O gate automático comprova estrutura, links, cobertura e invariantes; não certifica
qualidade didática, correção estatística, execução no Databricks ou aceite humano.
Relatórios e freezes R00–R13 são evidência histórica e não devem ser reescritos para
acompanhar o estado atual. Mudanças vivas pertencem aos índices, regras, Manual e
READMEs agregadores donos da informação.
"""
p.write_text(t[:pos]+new,encoding='utf-8')
