from pathlib import Path
p=Path('docs/decisions/ADR-0012-readmes-de-objeto.md')
t=p.read_text(encoding='utf-8').rstrip()
marker='## Registro de conclusão — 2026-09-14'
if marker not in t:
    t+='''\n\n## Registro de conclusão — 2026-09-14\n\nA implementação da decisão foi concluída pela iniciativa R00–R13. O estado integrado confirma contrato 1.0.0, 75/75 READMEs operacionais, 3/3 exemplares, zero pendências e seis índices funcionais de snippets. A auditoria final R13 foi `A0_light`, aceita e integrada pelo PR #33; o fechamento documental pós-merge foi integrado pelo PR #34.\n\nEsta nota registra implementação e encerramento sem alterar o corpo decisório original. Não equivale a auditoria independente, publicação no workspace ou homologação Databricks/Genie Code.'''
p.write_text(t+'\n',encoding='utf-8')
