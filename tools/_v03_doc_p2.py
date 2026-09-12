from pathlib import Path


def replace_once(path, old, new):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit("anchor mismatch in %s: count=%s" % (path, count))
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# 1) theme_plotly README: dependências exigidas pela revalidação V03.
path = "ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md"
old = """Tenha Plotly instalado e o caminho de importação preparado. `aplicar_tema` recebe uma `go.Figure`, não uma tabela de dados. Para a rota V03, tenha também um `ResolvedTheme` produzido pelo núcleo V02 para o contexto `notebook`; não passe dicionário cru ao adaptador. Fonte e subtítulo devem ser textos controlados e apropriados ao compartilhamento."""
new = """Tenha Plotly instalado e o caminho de importação preparado. `aplicar_tema` recebe uma `go.Figure`, não uma tabela de dados. Para a rota V03, tenha também um `ResolvedTheme` produzido pelo núcleo V02 para o contexto `notebook`; não passe dicionário cru ao adaptador. Como a V03 revalida esse resultado antes de consumi-lo, `jsonschema` e `referencing` também precisam estar disponíveis conforme `hub_snippets/requirements-temas.txt`. O helper não instala dependências automaticamente. Fonte e subtítulo devem ser textos controlados e apropriados ao compartilhamento."""
replace_once(path, old, new)

# 2) notebook executável: declarar as dependências de validação explicitamente.
path = "ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py"
old = "# MAGIC | Bibliotecas | Plotly disponível; NumPy para gerar os dados sintéticos desta demonstração |"
new = "# MAGIC | Bibliotecas | Plotly e NumPy disponíveis; para a seção V03, `jsonschema` e `referencing` preparados conforme `hub_snippets/requirements-temas.txt`; o notebook não instala pacotes |"
replace_once(path, old, new)

# 3) README do núcleo V02: registrar a integração opt-in V03 já existente.
path = "ambiente_fonte/.assistant/hub_snippets/visual/tema/README.md"
old = """> **CUSTOMIZADO PELO HUB · V02 CANDIDATA · NÃO APLICA CORES.** O núcleo valida
> uma proposta; não instala painel, não aprova a identidade e não publica arquivos."""
new = """> **CUSTOMIZADO PELO HUB · V02 INTEGRADA · O NÚCLEO NÃO APLICA CORES SOZINHO.** O núcleo valida
> uma proposta; a V03 permite consumo Plotly por opt-in, sem instalar painel, aprovar identidade ou publicar arquivos."""
replace_once(path, old, new)

old = """Na preparação de uma proposta e nos futuros adaptadores de gráficos, cabeçalhos
e materiais editoriais. Também permite testar uma configuração em Python sem
compute Spark ou acesso a dados de clientes. Os consumidores antigos continuam
usando suas rotas atuais até a migração específica de cada um."""
new = """Na preparação de uma proposta e nos adaptadores de gráficos, cabeçalhos
e materiais editoriais. A V03 já conecta explicitamente este núcleo ao `theme_plotly`
por uma rota opt-in; outros consumidores continuam em suas rotas atuais até a sprint
específica de cada um. Também permite testar uma configuração em Python sem
compute Spark ou acesso a dados de clientes."""
replace_once(path, old, new)

old = """Para aplicar o tema Plotly legado, a alternativa existente é
[`theme_plotly`](../theme_plotly/); ele não está integrado a este núcleo ainda."""
new = """Para Plotly, a V03 mantém a rota legada e acrescenta uma integração opt-in com
[`theme_plotly`](../theme_plotly/): somente um `ResolvedTheme` explícito é consumido
pela API nova. Isso não migra gráficos existentes nem transforma a validação em aprovação."""
replace_once(path, old, new)

# 4) Manual: expor o pré-requisito na referência operacional central.
path = "ambiente_fonte/.assistant/MANUAL_TECNICO.md"
old = """Mantém a rota legada de configuração/aplicação/registro e acrescenta, na V03, uma rota opt-in que consome `ResolvedTheme` de contexto notebook. `aplicar_tema_resolvido` afeta somente a figura passada; `registrar_template_plotly_resolvido` usa namespace `hub-*` e não muda o default da sessão sem `ativar=True`. A figura formatada continua exigindo exibição; tema não altera a lógica estatística dos dados plotados. Dados, eixos e cores explícitas de traces permanecem fora da responsabilidade do adaptador."""
new = """Mantém a rota legada de configuração/aplicação/registro e acrescenta, na V03, uma rota opt-in que consome `ResolvedTheme` de contexto notebook. `aplicar_tema_resolvido` afeta somente a figura passada; `registrar_template_plotly_resolvido` usa namespace `hub-*` e não muda o default da sessão sem `ativar=True`. Como a rota V03 revalida o tema antes do consumo, ela requer também as dependências declaradas em `hub_snippets/requirements-temas.txt` (`jsonschema` e `referencing`); nenhuma função instala pacotes. A figura formatada continua exigindo exibição; tema não altera a lógica estatística dos dados plotados. Dados, eixos e cores explícitas de traces permanecem fora da responsabilidade do adaptador."""
replace_once(path, old, new)

# 5) Changelog: preservar os dois novos achados documentais e sua correção.
path = "CHANGELOG.md"
old = """- (Codex) Code review P2: o adaptador Plotly passa a consumir layout e rodapé somente dos tokens extraídos do JSON canônico revalidado; adulterar apenas `_values` de um `ResolvedTheme` não contamina a figura.
- (Codex) Bloco copiável V03 no README importa `plotly.graph_objects as go` localmente, sem depender da execução de células anteriores."""
new = """- (Codex) Code review P2: o adaptador Plotly passa a consumir layout e rodapé somente dos tokens extraídos do JSON canônico revalidado; adulterar apenas `_values` de um `ResolvedTheme` não contamina a figura.
- (Codex) Bloco copiável V03 no README importa `plotly.graph_objects as go` localmente, sem depender da execução de células anteriores.
- (Codex) Code review P2 documental: README, notebook e Manual explicitam que a rota V03 revalida o tema e requer `jsonschema`/`referencing` conforme `hub_snippets/requirements-temas.txt`, sem instalação automática.
- (Codex) README do núcleo V02 deixa de afirmar que Plotly ainda não está integrado e passa a registrar a integração opt-in V03 sem sugerir migração automática ou aprovação."""
replace_once(path, old, new)

print("V03_DOC_REVIEW_P2_PATCH_OK")
