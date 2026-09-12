from pathlib import Path


def text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, value: str) -> None:
    Path(path).write_text(value, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    value = text(path)
    if value.count(old) != 1:
        raise SystemExit(f"âncora inesperada em {path}: {old[:80]!r} count={value.count(old)}")
    write(path, value.replace(old, new, 1))


# README do objeto: preserva as quinze seções e acrescenta a operação V03 dentro delas.
path = "ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/README.md"
replace_once(path, "| O que é? | Conjunto de funções de tema para Plotly. |",
             "| O que é? | Funções legadas de tema Plotly mais um adaptador V03 opt-in para `ResolvedTheme`. |")
replace_once(
    path,
    "Este objeto oferece três operações: `get_tema_eda` consulta a configuração, `aplicar_tema` modifica uma figura e `registrar_template_plotly` registra um padrão para novas figuras na sessão. Essas operações não são equivalentes e não centralizam o estilo de todo componente HTML do projeto.",
    "As três operações legadas continuam iguais: `get_tema_eda` consulta a configuração histórica, `aplicar_tema` modifica uma figura e `registrar_template_plotly` registra o padrão `caixa` na sessão. A V03 acrescenta, sem substituir essas chamadas, `get_tema_plotly`, `aplicar_tema_resolvido` e `registrar_template_plotly_resolvido` para consumir explicitamente um `ResolvedTheme` validado pela V02. Plotly continua sendo apenas um consumidor; HTML e outros componentes têm sprints próprias."
)
replace_once(
    path,
    "`registrar_template_plotly` insere a configuração no registro `plotly.io.templates` com o nome `caixa` e altera `pio.templates.default`. Esse efeito vale para o processo Python atual. Importar o módulo, por si só, não chama essa função.",
    "`registrar_template_plotly` insere a configuração legada no registro `plotly.io.templates` com o nome `caixa` e altera `pio.templates.default`. Esse efeito vale para o processo Python atual. Importar o módulo, por si só, não chama essa função.\n\nNa rota V03, `get_tema_plotly(theme)` traduz somente os tokens notebook atribuídos ao Plotly e não altera a sessão. `aplicar_tema_resolvido` aplica essa tradução explicitamente a uma figura. `registrar_template_plotly_resolvido` usa um nome `hub-*`, não ativa o template por padrão e só muda `pio.templates.default` com `ativar=True`. A configuração é revalidada pelo núcleo antes de ser consumida."
)
anchor = "Use `fig.show()` no notebook para visualizar. O [exemplo completo](exemplo_theme_plotly.py) gera uma série local e mostra figuras; não grava tabelas."
insert = '''### V03: aplicar uma proposta resolvida sem mudar o legado

A referência empacotada abaixo é **fixture de teste**, não tema operacional aprovado. Ela serve para demonstrar o fluxo; uma proposta real deve seguir o processo de governança do Sistema de Temas.

```python
from hub_snippets.visual.tema import load_reference_theme, resolve_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido

base = load_reference_theme("notebook")
proposta = base.to_dict()
proposta["theme_id"] = "hub-exemplo-proposta"
proposta["display_name"] = "Exemplo de proposta"
proposta["description"] = "Exemplo sintético para demonstrar a aplicação Plotly opt-in."
proposta["tokens"]["brand.primary"] = "#112233"

tema_resolvido = resolve_theme(proposta, expected_context="notebook")
fig = go.Figure(go.Bar(x=["A", "B"], y=[10, 12]))
aplicar_tema_resolvido(fig, tema_resolvido, fonte="dados sintéticos", n=2)
fig.show()
```

O fluxo não grava o tema, não o aprova e não altera outros gráficos da sessão. A fixture `legado_notebook` produz exatamente o mesmo layout de `get_tema_eda()`, o que é testado como regressão da migração.

'''
replace_once(path, anchor, insert + anchor)
replace_once(
    path,
    "Escolha conscientemente entre aplicação explícita e registro global. Para recuperar o padrão da sessão depois de uma experiência de registro, guarde o valor anterior de `pio.templates.default` e restaure-o; não suponha que uma nova célula comece uma sessão vazia.",
    "Escolha conscientemente entre aplicação explícita e registro global. Para propostas V03, prefira `aplicar_tema_resolvido`; `registrar_template_plotly_resolvido` exige namespace `hub-*`, recusa colisão por padrão e só ativa o template com `ativar=True`. Para recuperar o padrão da sessão depois de uma experiência de registro, guarde o valor anterior de `pio.templates.default` e restaure-o; não suponha que uma nova célula comece uma sessão vazia."
)
replace_once(
    path,
    "A paleta categórica não substitui escalas explicitamente definidas em heatmaps nem cores já fixadas nos traces. O registro global afeta outras figuras que usem o padrão da mesma sessão, e não outras sessões independentes.",
    "A paleta categórica não substitui escalas explicitamente definidas em heatmaps nem cores já fixadas nos traces. O registro global afeta outras figuras que usem o padrão da mesma sessão, e não outras sessões independentes. A V03 aplica somente `mode=light`: `dark` e `high_contrast` são válidos no contrato, mas falham fechados no adaptador Plotly até existirem tokens de superfície suficientes para não inventar backgrounds implícitos."
)
replace_once(
    path,
    "A [implementação](theme_plotly.py) define as três operações; a [fachada](__init__.py) exporta seus nomes. O [notebook](exemplo_theme_plotly.py) demonstra a aplicação explícita. [Correlation matrix](../../display/correlation_matrix/README.md) e [distribution grid](../../display/distribution_grid/README.md) são consumidores reais do tema.",
    "A [implementação](theme_plotly.py) mantém as três operações legadas e acrescenta as três operações V03; a [fachada](__init__.py) exporta os seis nomes. O [notebook](exemplo_theme_plotly.py) demonstra legado e opt-in configurado. [Correlation matrix](../../display/correlation_matrix/README.md) e [distribution grid](../../display/distribution_grid/README.md) continuam consumidores do caminho legado nesta sprint: não foram migrados implicitamente. O estado da V03 está em `docs/sprints/sistema_temas/V03/`."
)
value = text(path)
last = "Os testes R03-B conferem identidade do objeto, dados preservados, precedência, anotações e registro com restauração do estado. Não homologam o aspecto no Databricks nem verificam a origem declarada pelo usuário. Revisão própria de ChatGPT; auditoria independente não realizada."
addition = last + "\n\nA V03 acrescenta testes de equivalência do layout legado, tradução de tokens, integridade do `ResolvedTheme`, ausência de efeitos globais na aplicação por figura, namespace/colisão de templates e falha fechada de contextos/modos ainda não suportados. Esses testes também não substituem inspeção visual no Databricks."
if value.count(last) != 1:
    raise SystemExit("âncora final do README theme_plotly não encontrada")
write(path, value.replace(last, addition, 1))

# Notebook de exemplo: acrescenta uma seção opt-in sem remover a demonstração histórica.
path = "ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py"
marker = "## 3. V03 — proposta resolvida, aplicação explícita"
value = text(path)
if marker not in value:
    value += '''\n\n# COMMAND ----------\n# MAGIC %md\n# MAGIC ## 3. V03 — proposta resolvida, aplicação explícita\n# MAGIC\n# MAGIC Esta seção usa uma **fixture sintética** como ponto de partida. Ela não é um\n# MAGIC tema operacional aprovado. A proposta existe só em memória e afeta somente a\n# MAGIC figura passada à função nova.\n\n# COMMAND ----------\n\nimport plotly.io as pio\nfrom hub_snippets.visual.tema import load_reference_theme, resolve_theme\nfrom hub_snippets.visual.theme_plotly import aplicar_tema_resolvido, get_tema_plotly\n\nreferencia = load_reference_theme("notebook")\nproposta = referencia.to_dict()\nproposta["theme_id"] = "hub-v03-exemplo"\nproposta["display_name"] = "V03 exemplo sintético"\nproposta["description"] = "Proposta sintética usada somente para demonstrar o adaptador Plotly V03."\nproposta["tokens"]["brand.primary"] = "#112233"\nproposta["tokens"]["palette.categorical"] = ["#112233", "#445566", "#778899"]\n\ntema_resolvido = resolve_theme(proposta, expected_context="notebook")\ndefault_antes = pio.templates.default\n\nfigura3 = go.Figure(go.Bar(x=["A", "B", "C"], y=[10, 12, 9]))\nfigura3.update_layout(title="Proposta V03 — exemplo sintético")\naplicar_tema_resolvido(figura3, tema_resolvido, fonte="dados sintéticos", n=3)\n\nassert pio.templates.default == default_antes\nassert figura3.layout.title.font.color == "#112233"\nassert list(get_tema_plotly(referencia)["colorway"]) == list(get_tema_eda()["colorway"])\nfigura3.show()\n\n# COMMAND ----------\n# MAGIC %md\n# MAGIC **Como ler.** A cor alterada prova somente que o adaptador consumiu a proposta\n# MAGIC validada. `pio.templates.default` permanece igual porque aplicação por figura\n# MAGIC não é registro global. O teste de equivalência da referência legada evita que\n# MAGIC a V03 mude silenciosamente o visual atual. `dark` e `high_contrast` continuam\n# MAGIC fora do adaptador Plotly desta sprint; usar esses modos gera erro explícito.\n'''
    write(path, value)

# Manual canônico: documenta as APIs novas no mesmo verbete.
path = "ambiente_fonte/.assistant/MANUAL_TECNICO.md"
replace_once(
    path,
    "Obtém configuração, aplica tema a uma figura ou registra um template na sessão. `registrar_template_plotly` tem efeito no estado de apresentação da sessão. A figura formatada continua exigindo exibição; tema não altera a lógica estatística dos dados plotados. A aplicação modifica a própria figura; anotações podem se acumular em chamadas repetidas, e customizações de layout devem vir depois do tema.",
    "Mantém a rota legada de configuração/aplicação/registro e acrescenta, na V03, uma rota opt-in que consome `ResolvedTheme` de contexto notebook. `aplicar_tema_resolvido` afeta somente a figura passada; `registrar_template_plotly_resolvido` usa namespace `hub-*` e não muda o default da sessão sem `ativar=True`. A figura formatada continua exigindo exibição; tema não altera a lógica estatística dos dados plotados. Dados, eixos e cores explícitas de traces permanecem fora da responsabilidade do adaptador."
)
replace_once(
    path,
    "get_tema_eda() -> Dict[str, Any]\naplicar_tema(fig: go.Figure, subtitulo: Optional[str]=None, fonte: Optional[str]=None, n: Optional[int]=None) -> go.Figure\nregistrar_template_plotly() -> None",
    "get_tema_eda() -> Dict[str, Any]\naplicar_tema(fig: go.Figure, subtitulo: Optional[str]=None, fonte: Optional[str]=None, n: Optional[int]=None) -> go.Figure\nregistrar_template_plotly() -> None\nget_tema_plotly(theme: ResolvedTheme) -> Dict[str, Any]\naplicar_tema_resolvido(fig: go.Figure, theme: ResolvedTheme, subtitulo: Optional[str]=None, fonte: Optional[str]=None, n: Optional[int]=None) -> go.Figure\nregistrar_template_plotly_resolvido(theme: ResolvedTheme, *, nome: str, ativar: bool=False, substituir: bool=False) -> None"
)
manual_anchor = "</details>\n\n[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py)"
manual_add = "</details>\n\nPara usuários novos, mantenha `aplicar_tema` se o objetivo é preservar o hábito atual. Use `aplicar_tema_resolvido` somente quando houver uma configuração notebook explicitamente resolvida pelo núcleo V02. A V03 suporta `mode=light`; `dark`/`high_contrast` falham fechados até uma sprint futura definir superfícies Plotly sem defaults ocultos. Fixtures empacotadas servem a testes/demonstrações e não são temas operacionais aprovados.\n\n[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py)"
replace_once(path, manual_anchor, manual_add)

# Gate local: a etapa temas já descobre test_temas_v03.py; atualiza apenas a descrição.
path = "tools/ci_local.py"
value = text(path)
value = value.replace("1. Temas — núcleo V02 e contrato V01 compartilhado, com regressões adversariais;\n1. Temas — núcleo V02 e contrato V01 compartilhado, com regressões adversariais;",
                      "1. Temas — adaptador Plotly V03, núcleo V02 e contrato V01, com regressões adversariais;")
old = '"núcleo V02 e contrato V01 compartilhado (sem publicação)",'
new = '"adaptador Plotly V03 + núcleo V02 + contrato V01 (sem publicação)",'
if value.count(old) != 1:
    raise SystemExit("descrição da etapa temas não encontrada")
write(path, value.replace(old, new, 1))

# Índice da iniciativa: V03 vira etapa corrente candidata, sem afirmar aceite/merge.
path = "docs/sprints/sistema_temas/README.md"
replace_once(
    path,
    "## Etapa atual — V02 aceita e integrada pelo PR #14",
    "## Etapa atual — V03 em desenvolvimento na branch `codex/temas-v03`"
)
replace_once(
    path,
    "Os quatro checks pós-merge na `main` passaram. A V03 ainda não foi iniciada.",
    "Os quatro checks pós-merge da V02 na `main` passaram. A V03 foi iniciada a partir dessa base verde e acrescenta somente uma rota Plotly opt-in; ainda não foi aceita nem integrada."
)
replace_once(
    path,
    "## Continuidade — após V02\n\nA V02 está aceita e integrada no Git. A próxima sprint planejada é V03, que fará a\nintegração explícita do núcleo com Plotly preservando o comportamento legado por\npadrão. A V03 ainda não foi iniciada e não há publicação Databricks nesta etapa.",
    "## Continuidade — V03\n\nA V02 está aceita e integrada no Git. A [V03](V03/README.md) está em desenvolvimento\nna branch `codex/temas-v03`: integra explicitamente o núcleo com Plotly preservando\no comportamento legado por padrão. Ainda não há aceite, merge ou publicação\nDatabricks; V04 e V05 não foram iniciadas."
)

# Índice geral de sprints.
path = "docs/sprints/README.md"
replace_once(
    path,
    "A homologação operacional, a auditoria independente e a avaliação com usuário\niniciante permanecem pendentes. A V03 ainda não foi iniciada.",
    "A [V03](sistema_temas/V03/README.md) está em desenvolvimento em branch separada e acrescenta apenas um adaptador Plotly opt-in; não migra consumidores existentes. A homologação operacional, a auditoria independente e a avaliação com usuário iniciante permanecem pendentes."
)

# Contexto canônico para outras IAs.
path = "CLAUDE.md"
replace_once(
    path,
    "A V03 ainda não foi iniciada.",
    "A V03 está em desenvolvimento na branch `codex/temas-v03`, com adaptador Plotly opt-in; ainda não há aceite, merge ou migração de consumidores legados. Estado: `docs/sprints/sistema_temas/V03/CHECKPOINT_V03.md`."
)

# Changelog da sessão.
path = "CHANGELOG.md"
value = text(path)
marker = "## 2026-09-12 — V03: adaptador Plotly opt-in (Codex)"
anchor = "## 2026-09-12 — V02: aceite e integração Git concluídos (Codex)"
if marker not in value:
    if anchor not in value:
        raise SystemExit("âncora do changelog não encontrada")
    entry = '''## 2026-09-12 — V03: adaptador Plotly opt-in (Codex)\n\n### Adicionado\n\n- (Codex) `get_tema_plotly`, `aplicar_tema_resolvido` e `registrar_template_plotly_resolvido` sobre a API pública V02, sem alterar as três assinaturas legadas.\n- (Codex) Suíte V03, workflow somente leitura e documentação de sprint para equivalência legada, mapeamento de tokens, integridade, efeitos de sessão e falhas adversariais.\n\n### Atualizado\n\n- (Codex) README/notebook de `theme_plotly`, Manual e índices passam a documentar a rota configurada como opt-in; consumidores atuais continuam no caminho legado.\n- (Codex) Gate `temas` já descobre a suíte V03 pelo padrão `test_temas*.py`; descrição atualizada sem criar etapa paralela.\n\n### Notas\n\n- (Codex) Primeiro run remoto V03 `34721929275`: 22 V03 + 12 V00 + 105 V02 + 138 V01 aprovados. Não somar reexecuções como novos casos.\n- (Codex) `mode=dark` e `high_contrast` permanecem válidos no contrato, mas o adaptador Plotly V03 os recusa até existirem tokens de superfície suficientes.\n- (Codex) Sem aceite/merge V03, publicação Databricks, migração de consumidores, V04/V05 ou homologação operacional.\n\n'''
    write(path, value.replace(anchor, entry + anchor, 1))

print("V03_DOC_PATCH_OK")
