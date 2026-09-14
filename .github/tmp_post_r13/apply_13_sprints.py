from pathlib import Path
p=Path('docs/sprints/README.md')
t=p.read_text(encoding='utf-8')
old='''A [migração R00–R13](readmes_objetos/README.md) usa numeração própria. Os
relatórios históricos acima permanecem intactos; não são substituídos pelos
checkpoints desta iniciativa.

O [checkpoint R02-I](readmes_objetos/CHECKPOINT_INTEGRACAO_R02.md) registra a
composição candidata com o Concierge. O [piloto R02](readmes_objetos/CHECKPOINT_R02.md)
e os relatos R00/R01 permanecem históricos; não houve início da R03.'''
new='''A [iniciativa R00–R13](readmes_objetos/README.md) usa numeração própria e está
encerrada no Git desde 14/09/2026: 75/75 READMEs operacionais, 3/3 exemplares,
zero pendências e auditoria final local `A0_light`. Homologação Databricks/Genie
Code e auditoria independente permanecem gates separados.

As subseções cronológicas abaixo preservam o estado observado em cada etapa. O
[checkpoint R02-I](readmes_objetos/CHECKPOINT_INTEGRACAO_R02.md), o
[piloto R02](readmes_objetos/CHECKPOINT_R02.md) e os relatos R00/R01 continuam
históricos; frases como “R03 não iniciada” descrevem aquele checkpoint, não o
estado vigente.'''
assert t.count(old)==1
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8')
