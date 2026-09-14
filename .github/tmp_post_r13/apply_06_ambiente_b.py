from pathlib import Path
p=Path('ambiente_fonte/README.md')
t=p.read_text(encoding='utf-8')
t=t.replace('esta mudança é documental e não publica automaticamente o workspace.','o README local é obrigatório para novos snippets, scripts e prompts; ele não homologa runtime nem publica o workspace.',1)
p.write_text(t,encoding='utf-8')
