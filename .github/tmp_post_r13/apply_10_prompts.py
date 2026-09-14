from pathlib import Path
p=Path('ambiente_fonte/.assistant/hub_prompts/README.md')
t=p.read_text(encoding='utf-8')
# Atualiza a anatomia da pasta para incluir o README local.
old='''hub_prompts/
└── eda_rapida/
    ├── eda_rapida.md             <- briefing técnico preenchível
    └── exemplo_eda_rapida.py     <- notebook didático de acompanhamento'''
new='''hub_prompts/
└── eda_rapida/
    ├── README.md                 <- guia local para escolher e interpretar
    ├── eda_rapida.md             <- briefing técnico preenchível
    └── exemplo_eda_rapida.py     <- notebook didático de acompanhamento'''
assert t.count(old)==1
t=t.replace(old,new,1)
intro='''A pasta de prompt tem três camadas complementares: **README local para decidir se o recurso é adequado**, **briefing para preencher** e **notebook para preparar o cenário e registrar evidência**. O README não substitui o briefing, e o notebook não transforma uma resposta esperada em execução real.\n\n'''
marker='### 1. O Arquivo Markdown (`<nome>.md`)\n'
if intro not in t:
    assert marker in t
    t=t.replace(marker,intro+marker,1)
root=Path('ambiente_fonte/.assistant/hub_prompts')
names=sorted(x.name for x in root.iterdir() if x.is_dir() and (x/'README.md').is_file())
for name in names:
    needle=f'hub_prompts/{name}/{name}.md'
    pos=t.find(needle); assert pos>=0, name
    line_start=t.rfind('\n',0,pos)+1
    line_end=t.find('\n',pos)
    line=t[line_start:line_end]
    link=f'[README local]({name}/README.md)'
    if link not in line:
        line=line.rstrip()+f' · {link}'
        t=t[:line_start]+line+t[line_end:]
p.write_text(t,encoding='utf-8')
