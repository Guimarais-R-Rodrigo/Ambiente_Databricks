from pathlib import Path

PATH = Path('ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md')
text = PATH.read_text(encoding='utf-8')

replacements = [
    (
        'Tenha Plotly instalado e o caminho de importação preparado. `aplicar_tema` recebe uma `go.Figure`, não uma tabela de dados. Fonte e subtítulo devem ser textos controlados e apropriados ao compartilhamento.\n',
        'Tenha Plotly instalado e o caminho de importação preparado. `aplicar_tema` recebe uma `go.Figure`, não uma tabela de dados. Para a rota V03, tenha também um `ResolvedTheme` produzido pelo núcleo V02 para o contexto `notebook`; não passe dicionário cru ao adaptador. Fonte e subtítulo devem ser textos controlados e apropriados ao compartilhamento.\n',
    ),
    (
        '`get_tema_eda()` retorna um dicionário. `aplicar_tema(...)` retorna a própria figura modificada, preservando os dados dos traces. `registrar_template_plotly()` retorna `None` e deixa um efeito na sessão.\n',
        '`get_tema_eda()` retorna o dicionário legado. `aplicar_tema(...)` retorna a própria figura modificada, preservando os dados dos traces. `registrar_template_plotly()` retorna `None` e deixa o template legado ativo na sessão. Na rota V03, `get_tema_plotly(theme)` retorna um novo dicionário de layout derivado do `ResolvedTheme`; `aplicar_tema_resolvido(...)` retorna a mesma figura modificada sem trocar o template default; e `registrar_template_plotly_resolvido(...)` retorna `None`, registra um nome `hub-*` e só altera o default quando `ativar=True`.\n',
    ),
    (
        'O [notebook](exemplo_theme_plotly.py) demonstra legado e opt-in configurado.',
        'O [notebook](exemplo_theme_plotly.py) demonstra o legado e a rota opt-in usando uma referência resolvida sem customização inline.',
    ),
    (
        'As decisões particulares do Hub são verificáveis em [theme_plotly.py](theme_plotly.py), base `c60f1e5`.\n',
        'As decisões particulares vigentes do Hub são verificáveis em [theme_plotly.py](theme_plotly.py). O estado desta sprint está em `docs/sprints/sistema_temas/V03/CHECKPOINT_V03.md`; a base `c60f1e5` permanece apenas como referência histórica da R03-B.\n',
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'âncora editorial inesperada ({count}): {old[:90]!r}')
    text = text.replace(old, new, 1)

PATH.write_text(text, encoding='utf-8')
print('V03_README_POLISH_OK')
