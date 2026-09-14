from pathlib import Path
p=Path('docs/sprints/README.md')
t=p.read_text(encoding='utf-8').rstrip()
line='\n\n### Reconciliação documental pós-R13\nEscopo D01–D04: `docs/sprints/documentacao_pos_r13.md`.'
if '### Reconciliação documental pós-R13' not in t: t+=line
p.write_text(t+'\n',encoding='utf-8')
