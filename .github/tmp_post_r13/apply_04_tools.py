from pathlib import Path
p=Path('tools/README.md')
t=p.read_text(encoding='utf-8')
t=t.replace('## READMEs de objeto — R01','## READMEs de objeto — contrato vigente 1.0.0',1)
old='''[CONTROLE_MIGRACAO.json](../docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json)
identifica legados pendentes. Um README entregue precisa sair da dispensa no
mesmo commit. Novos objetos sem README reprovam. A versão anterior diferente do
controle, na história first-parent, delimita o conjunto máximo de dispensas;
na introdução inicial, só objetos existentes na base anterior são elegíveis.
Histórico raso reprova com orientação para usar `fetch-depth: 0`.'''
new='''[CONTROLE_MIGRACAO.json](../docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json)
registra o fechamento da transição: `phase=complete`, `pending={}`, 75/75 READMEs
operacionais e 3/3 exemplares. Ele permanece como evidência e guarda de ratchet,
não como fila ativa de legados. Novos objetos sem README reprovam e reintroduzir
uma dispensa também deve reprovar. Histórico raso continua incompatível com a
verificação monotônica e exige `fetch-depth: 0`.'''
assert t.count(old)==1, t.count(old)
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8')
