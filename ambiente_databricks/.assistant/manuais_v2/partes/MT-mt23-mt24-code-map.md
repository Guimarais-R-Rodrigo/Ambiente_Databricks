# Leitura dos arquivos Python de identidade visual

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt23-mt24-code-map"></a>
<a id="mt23-mt24-code-map"></a>
### Leitura dos arquivos Python de identidade visual

Leia cada ficha como uma ligação entre a arquitetura ensinada no capítulo e os bytes de um arquivo concreto. A coluna de papel responde por que o arquivo existe. As entradas e saídas mostram onde os dados entram e o que o chamador recebe. A coluna de efeitos separa calcular um resultado de alterar a sessão, gravar uma tabela ou produzir uma apresentação. Essa separação evita atribuir ao helper tudo que aparece no notebook de demonstração.

Uma fachada é a camada de importação que disponibiliza nomes de outro módulo. Ela pode carregar bibliotecas necessárias no momento do import, embora ainda não chame a função de negócio. Um marcador de pacote apenas estabelece a organização do diretório. Uma implementação contém o algoritmo. Um exemplo é um roteiro de notebook: pode preparar dados, instalar bibliotecas, mostrar resultados e conservar observações históricas. Esses quatro papéis explicam a repetição de nomes entre arquivos sem sugerir quatro versões independentes do mesmo algoritmo.

As fichas complementam a leitura contínua; não substituem a assinatura e a interpretação desenvolvidas nos capítulos. Quando um resultado histórico difere do comportamento atual, a nota identifica a diferença e o cuidado necessário. Uma saída colada no exemplo descreve o ensaio registrado naquela fonte; ela não demonstra uma execução atual. Os nomes citados também não tornam automaticamente uma função interna uma interface pública. Para compor uma chamada, use a fachada indicada e confira o contrato do objeto.

Os links levam ao arquivo correspondente e ao trecho conceitual do manual. Compare sempre helper e exemplo antes de executar células: efeitos pertencem ao corpo que realmente os realiza. As limitações descritas fazem parte da interpretação do resultado, inclusive quando o código devolve números plausíveis.

Na identidade visual, acompanhe o objeto que recebe a aparência e o local que recebe uma escrita. Resolver um tema, adaptar uma figura, mostrar uma prévia e salvar uma proposta têm efeitos distintos. O contexto do App e a ponte AI/BI acrescentam contratos próprios.

<a id="mt23-mt24-code-map-file-001"></a>
#### 1. `_aibi_theme_impl.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/aibi/_aibi_theme_impl.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_padroes/identidade_visual/aibi/_aibi_theme_impl.py` · SHA-256 `bab385daa0fc66fee178723b72494a59918dcf2537de295381d4fde783df0652` |
| Papel e motivo técnico | V11 mantém matriz de 48 tokens e binding nativo restrito fora da fachada |
| Nomes disponibilizados | ["AibiThemeError", "AibiThemeProjection", "AibiNativeCandidate", "project_theme", "export_projection", "bind_native_template", "workspace_theme_policy", "dashboard_theme_policy", "authorize_local_operation", "synthetic_dashboard_semantic_fingerprint"] |
| Entradas | ResolvedTheme; bytes de template/binding JSON com SHA; operação e flags sintéticas |
| Saídas | AibiThemeProjection/bytes de projeção ou AibiNativeCandidate; políticas locais e fingerprint sintético |
| Efeitos e limites | lê aibi_mapping.json e verifica SHA; gera bytes em memória; não chama Databricks nem publica |
| Dependências e momento de uso | V02 tema + JSON/Path; matriz hash-fixed; template nativo só exportado/autorizado |
| Como interpretar este arquivo | `aibi/_aibi_theme_impl.py` lê `aibi_mapping.json` por SHA, recebe `ResolvedTheme` e, nas operações condicionadas, bytes de template/binding, flags e operação autorizada. Devolve projeção Hub, bytes, candidato nativo restrito, políticas ou fingerprint sintético. `project_theme` mapeia apenas capacidades descritas; binding nativo requer entrada e autorização explícitas, e a projeção não vira import remoto. O módulo não chama Databricks nem publica dashboard. |

<a id="mt23-mt24-code-map-file-002"></a>
#### 2. `aibi_theme.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/aibi/aibi_theme.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_padroes/identidade_visual/aibi/aibi_theme.py` · SHA-256 `d219d32df4547f3b391fb87397a89eeed71283511059dc8f54cea76be07e09fb` |
| Papel e motivo técnico | Fachada V11 mantém erro de contexto pertencente à ponte antes da delegação |
| Nomes disponibilizados | ["AibiThemeError", "AibiThemeProjection", "AibiNativeCandidate", "project_theme", "export_projection", "bind_native_template", "workspace_theme_policy", "dashboard_theme_policy", "authorize_local_operation", "synthetic_dashboard_semantic_fingerprint"] |
| Entradas | ResolvedTheme notebook em project_theme; demais entradas delegadas ao núcleo |
| Saídas | reexporta API V11 e projeção do núcleo |
| Efeitos e limites | não lê workspace; valida tipo/contexto na borda e delega |
| Dependências e momento de uso | import relativo ou direto do _aibi_theme_impl conforme __package__ |
| Como interpretar este arquivo | `aibi/aibi_theme.py` é a fachada pública da ponte V11. Ela aceita tema notebook resolvido em `project_theme`, checa tipo/contexto na borda e delega projeção, export, binding, políticas e fingerprint ao núcleo privado. Não consulta workspace ao importar; o consumidor deve preferir essa rota à implementação interna. |

<a id="mt23-mt24-code-map-file-003"></a>
#### 3. `app.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/databricks_app/app.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_padroes/identidade_visual/databricks_app/app.py` · SHA-256 `0ccc2d9b9072efd1795af226afea09331672924416cfb3636be7b942eafcbdc5` |
| Papel e motivo técnico | Tela Streamlit V10 apresenta autoria de tema sem aprovação/publicação |
| Nomes disponibilizados | [] |
| Entradas | os.environ; st.context.headers; presets; controles e nome de sessão |
| Saídas | interface com preview, revisão, recibo de sessão e avisos |
| Efeitos e limites | import tem bootstrap/sys.path e execução Streamlit; chama serviço para leitura/escrita no Volume |
| Dependências e momento de uso | streamlit + app_service + theme_lab; requer App implantado/proxy/Volume para efeito remoto |
| Como interpretar este arquivo | `databricks_app/app.py` é a entrada Streamlit. No import, prepara caminho, lê ambiente e constrói a interface, obtendo identidade, presets, controles e sessões por `app_service`. Exibe prévia, revisão e recibo; uma ação de salvar pode chamar o serviço e escrever no Volume configurado. O tratamento genérico de erro na ação Aplicar exige conferir o estado em memória e a revisão local antes de interpretar sucesso. O recibo pertence à ação separada Salvar sessão, que pode persistir a proposta. |

<a id="mt23-mt24-code-map-file-004"></a>
#### 4. `app_service.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/databricks_app/app_service.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_padroes/identidade_visual/databricks_app/app_service.py` · SHA-256 `aad9040cc8c5e6401b800fb1e71f3434ffeeaefb58394a880677dcff311d5b22` |
| Papel e motivo técnico | Camada V10 isola identidade/configuração/persistência por usuário |
| Nomes disponibilizados | ["ThemeAppError", "ThemeAppUser", "ThemeAppConfig", "resolve_user", "load_config", "save_own_session", "list_own_sessions", "reopen_own_session", "retention_policy", "publication_policy"] |
| Entradas | headers forwarded, env HUB_THEME_*, ThemeLabDraft, nome de sessão |
| Saídas | ThemeAppUser/Config, recibo, lista/reabertura e políticas read-only |
| Efeitos e limites | hash de subject para namespace; mkdir e escrita/leitura via theme_lab; sem publicação |
| Dependências e momento de uso | UC Volume autorizado em produção; modo local explícito; confiança em proxy/ACL externos |
| Como interpretar este arquivo | `databricks_app/app_service.py` recebe headers de identidade encaminhados pela plataforma, variáveis `HUB_THEME_*`, rascunho e nome da sessão. Devolve usuário/configuração, recibo e listagem/reabertura da própria sessão; cria diretórios e lê/grava no Volume apenas nas rotas chamadas. O hash do subject isola namespace de arquivos, mas não concede ACL: o destino precisa impor permissão efetiva. `publication_policy` e `retention_policy` informam limites; não fazem publicação. |

<a id="mt23-mt24-code-map-file-005"></a>
#### 5. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/__init__.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/__init__.py` · SHA-256 `041655c508ce21d4699325c4de5efbea685dffef0efed4b52f2109288661f459` |
| Papel e motivo técnico | Marca o diretório visual como pacote; não agrega APIs |
| Nomes disponibilizados | [] |
| Entradas | import do pacote |
| Saídas | nenhum símbolo exportado |
| Efeitos e limites | sem efeito além da presença do pacote |
| Dependências e momento de uso | sem imports; subpacotes oferecem suas próprias fachadas |
| Como interpretar este arquivo | `visual/__init__.py` é um marcador de pacote com docstring, sem reexportações próprias. Importá-lo não agrega as APIs de badge, divider, Lab ou Plotly; escolha o subpacote que oferece a função desejada. |

<a id="mt23-mt24-code-map-file-006"></a>
#### 6. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/badge/__init__.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/badge/__init__.py` · SHA-256 `6940e2e4ea38e982def76a64d887995005f6544476916ecfcc2ebefbb53c25ca` |
| Papel e motivo técnico | Estabiliza import público de seis funções de badge |
| Nomes disponibilizados | ["badge_status", "badge_score", "badge_inline", "badge_status_resolvido", "badge_score_resolvido", "badge_inline_resolvido"] |
| Entradas | import do subpacote |
| Saídas | três funções legadas e três variantes _resolvido |
| Efeitos e limites | reexportação; nenhum HTML produzido no próprio arquivo |
| Dependências e momento de uso | depende de badge.py |
| Como interpretar este arquivo | `visual/badge/__init__.py` reexporta as três funções legadas de status, score e texto inline e suas três variantes `_resolvido`. A fachada não cria HTML no import. |

<a id="mt23-mt24-code-map-file-007"></a>
#### 7. `badge.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/badge/badge.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/badge/badge.py` · SHA-256 `88d9c430d548e8dc990585345d3c70c17241c1c33991c704d61157a083c84cde` |
| Papel e motivo técnico | Gera selos HTML escapando texto e mantendo corte legado do score |
| Nomes disponibilizados | ["badge_status", "badge_score", "badge_inline", "badge_status_resolvido", "badge_score_resolvido", "badge_inline_resolvido"] |
| Entradas | texto/tipo; valor e max; ResolvedTheme nas variantes |
| Saídas | string `<span>` de status, score ou inline |
| Efeitos e limites | sem display/escrita; _resolvido usa estilos compartilhados; max=0 resulta razão 0 |
| Dependências e momento de uso | constants.styles + tema.ResolvedTheme; nenhum Spark no módulo |
| Como interpretar este arquivo | `visual/badge/badge.py` recebe textos, tipo de status, valor/máximo de score e, nas variantes, `ResolvedTheme`; devolve strings `<span>` com texto escapado. Tipo desconhecido usa o estilo informativo; `max=0` leva a razão zero. O número arredondado exibido pode diferir da razão usada no corte de faixa, então o consumidor deve conferir limiar e legenda. |

<a id="mt23-mt24-code-map-file-008"></a>
#### 8. `exemplo_badge.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/badge/exemplo_badge.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/badge/exemplo_badge.py` · SHA-256 `89fe6c0944272ccb5eeeddfa706ac5e3739edf98d222339c65427640d893b4fb` |
| Papel e motivo técnico | Demonstra badges de três status e score em notebook Databricks |
| Nomes disponibilizados | [] |
| Entradas | spark.sql current_user para import; textos e números sintéticos |
| Saídas | displayHTML e prints de strings HTML |
| Efeitos e limites | renderiza na sessão; não grava arquivo/tabela |
| Dependências e momento de uso | runtime notebook com spark/displayHTML e Hub no sys.path |
| Como interpretar este arquivo | `visual/badge/exemplo_badge.py` obtém o usuário da sessão Spark para localizar o Hub, monta status e escores fictícios e os exibe via `displayHTML` ou impressão. É demonstração visual da sessão, sem gravação ou aferição de contraste no destino. |

<a id="mt23-mt24-code-map-file-009"></a>
#### 9. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/divider/__init__.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/divider/__init__.py` · SHA-256 `a88279b341b7d61999a511f4c9e2899da31176ed1df1dfed2e260ba8ea0d597a` |
| Papel e motivo técnico | Expõe quatro separadores legados e quatro variantes temáticas |
| Nomes disponibilizados | ["divider_light", "divider_medium", "divider_heavy", "divider_section", "divider_light_resolvido", "divider_medium_resolvido", "divider_heavy_resolvido", "divider_section_resolvido"] |
| Entradas | import do subpacote |
| Saídas | oito funções públicas |
| Efeitos e limites | reexportação somente |
| Dependências e momento de uso | depende de divider.py |
| Como interpretar este arquivo | `visual/divider/__init__.py` reexporta `divider_light`, `divider_medium`, `divider_heavy`, `divider_section` e as quatro contrapartes `_resolvido`. Esta fachada estabiliza os oito imports públicos. |

<a id="mt23-mt24-code-map-file-010"></a>
#### 10. `divider.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/divider/divider.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/divider/divider.py` · SHA-256 `732b7ec9d3316d939f7beae353d41c0880b70f2d6d3cca433a57c2b484371c75` |
| Papel e motivo técnico | Oferece hierarquia de separadores sem dados |
| Nomes disponibilizados | ["divider_light", "divider_medium", "divider_heavy", "divider_section", "divider_light_resolvido", "divider_medium_resolvido", "divider_heavy_resolvido", "divider_section_resolvido"] |
| Entradas | nenhum ou ResolvedTheme nas variantes |
| Saídas | HTML de um ou dois `<hr>` |
| Efeitos e limites | sem render/escrita; variantes buscam get_styles_resolvidos |
| Dependências e momento de uso | constants.styles + tema.ResolvedTheme |
| Como interpretar este arquivo | `visual/divider/divider.py` devolve fragmentos `<hr>` de pesos diferentes; a seção usa dois traços. As variantes resolvidas consultam estilos compartilhados do tema recebido. Nenhuma função inspeciona dados, apresenta no notebook ou grava HTML por conta própria. |

<a id="mt23-mt24-code-map-file-011"></a>
#### 11. `exemplo_divider.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/divider/exemplo_divider.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/divider/exemplo_divider.py` · SHA-256 `ee70c50b17211c3ca9ab74ab9ae3f1b620ed87b12dc343fe703a011cfb5343ea` |
| Papel e motivo técnico | Compara quatro pesos e sua interpretação visual |
| Nomes disponibilizados | [] |
| Entradas | spark.sql current_user para import; nenhum dado |
| Saídas | displayHTML + prints de HTML |
| Efeitos e limites | renderiza no notebook; não grava |
| Dependências e momento de uso | spark/displayHTML; Hub em sys.path |
| Como interpretar este arquivo | `visual/divider/exemplo_divider.py` localiza o Hub pela sessão Spark e compara separadores em `displayHTML`. A impressão permite julgar hierarquia localmente, mas zoom e legibilidade no destino precisam de inspeção própria; o exemplo não persiste nada. |

<a id="mt23-mt24-code-map-file-012"></a>
#### 12. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/index_generator/__init__.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/index_generator/__init__.py` · SHA-256 `0efa9beb9ca6c6b4263ea698e5c5511660a9a3ca044f0c487c2c6546d969b36f` |
| Papel e motivo técnico | Mantém caminho de import do índice legado/resolvido |
| Nomes disponibilizados | ["gerar_indice_eda", "gerar_indice_eda_resolvido"] |
| Entradas | import do subpacote |
| Saídas | gerar_indice_eda e gerar_indice_eda_resolvido |
| Efeitos e limites | reexportação somente |
| Dependências e momento de uso | depende de index_generator.py |
| Como interpretar este arquivo | `visual/index_generator/__init__.py` reexporta `gerar_indice_eda` e `gerar_indice_eda_resolvido`, mantendo a rota pública do índice. |

<a id="mt23-mt24-code-map-file-013"></a>
#### 13. `exemplo_index_generator.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/index_generator/exemplo_index_generator.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/index_generator/exemplo_index_generator.py` · SHA-256 `179a1b6737e36a0f86e59253526540d062971234e7f5c03bdf5a80a5e00fc7b0` |
| Papel e motivo técnico | Mostra índice completo e filtro [1,3,4,8] sem renumerar |
| Nomes disponibilizados | [] |
| Entradas | spark.sql current_user; lista sintética de etapas |
| Saídas | displayHTML/print Markdown |
| Efeitos e limites | renderização em memória |
| Dependências e momento de uso | spark/displayHTML; Hub em sys.path |
| Como interpretar este arquivo | `visual/index_generator/exemplo_index_generator.py` usa a sessão para importar o Hub, mostra índice completo e depois etapas `[1,3,4,8]` em HTML/Markdown. A seleção demonstra filtragem, não audita células ou conteúdo real. |

<a id="mt23-mt24-code-map-file-014"></a>
#### 14. `index_generator.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/index_generator/index_generator.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/index_generator/index_generator.py` · SHA-256 `d9387cfa063b9e645d74081e972807cd38a05d57af24b112b156585dbd4f15e5` |
| Papel e motivo técnico | Gera lista das etapas EDA com numeração do mapa comum |
| Nomes disponibilizados | ["gerar_indice_eda", "gerar_indice_eda_resolvido"] |
| Entradas | etapas_ativas iterable, markdown bool; ResolvedTheme opcional |
| Saídas | string HTML ou Markdown |
| Efeitos e limites | sem escrita; acessa SECOES_EDA por índice, IDs inválidos podem falhar; Markdown ignora CSS |
| Dependências e momento de uso | constants.emojis/styles e tema.ResolvedTheme |
| Como interpretar este arquivo | `visual/index_generator/index_generator.py` consulta `SECOES_EDA` para gerar string HTML ou Markdown a partir de `etapas_ativas`; sem lista, usa as etapas 0 a 8. O filtro preserva a numeração do mapa, não renumera o subconjunto. IDs fora do mapa podem falhar, Markdown dispensa CSS, e o texto gerado não prova que as seções existam no notebook. |

<a id="mt23-mt24-code-map-file-015"></a>
#### 15. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/kpi_card/__init__.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/kpi_card/__init__.py` · SHA-256 `100c68cde71eafa2bb847ae4aca4733817209657b36e8ea391f36cfb0e7aaa12` |
| Papel e motivo técnico | Expõe HTML/Markdown legados e HTML resolvido |
| Nomes disponibilizados | ["kpi_card_html", "kpi_card_markdown", "kpi_card_html_resolvido"] |
| Entradas | import do subpacote |
| Saídas | três funções públicas |
| Efeitos e limites | reexportação somente |
| Dependências e momento de uso | depende de kpi_card.py |
| Como interpretar este arquivo | `visual/kpi_card/__init__.py` reexporta `kpi_card_html`, `kpi_card_markdown` e `kpi_card_html_resolvido`. Não há rota Markdown `_resolvido` nesta API. |

<a id="mt23-mt24-code-map-file-016"></a>
#### 16. `exemplo_kpi_card.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/kpi_card/exemplo_kpi_card.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/kpi_card/exemplo_kpi_card.py` · SHA-256 `c4d375a9a88a481a3f4f29ea2f21c018cba7a3748acd8fbd0dd0de16c7adb642` |
| Papel e motivo técnico | Mostra mesmas quatro métricas em HTML e Markdown |
| Nomes disponibilizados | [] |
| Entradas | spark.sql current_user; dicionário sintético de strings |
| Saídas | displayHTML e print |
| Efeitos e limites | renderização em memória, sem fonte externa |
| Dependências e momento de uso | spark/displayHTML; Hub em sys.path |
| Como interpretar este arquivo | `visual/kpi_card/exemplo_kpi_card.py` monta quatro métricas sintéticas como strings, exibe HTML e imprime Markdown. A demonstração não consulta fonte de dados nem valida se número e alerta textual correspondem a uma métrica real. |

<a id="mt23-mt24-code-map-file-017"></a>
#### 17. `kpi_card.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/kpi_card/kpi_card.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/kpi_card/kpi_card.py` · SHA-256 `22e98c547a0ad73dac5cccdfedeb7d90a8636b637241173f166de3e2fb9bb4c0` |
| Papel e motivo técnico | Transforma mapa ordenado de métricas em cartões textuais |
| Nomes disponibilizados | ["kpi_card_html", "kpi_card_markdown", "kpi_card_html_resolvido"] |
| Entradas | dict rótulo→valor; ResolvedTheme no HTML resolvido |
| Saídas | HTML `<span>` concatenado ou linha Markdown |
| Efeitos e limites | sem cálculo/escrita; HTML escapa rótulo/valor; Markdown escapa pipes, não aplica tema |
| Dependências e momento de uso | constants.styles + tema.ResolvedTheme |
| Como interpretar este arquivo | `visual/kpi_card/kpi_card.py` recebe dicionário ordenado de rótulo para valor já formatado. Devolve cartões HTML com texto escapado ou linhas Markdown com pipes escapados; a variante resolvida só existe para HTML. A função não calcula KPI, unidade ou ressalva: o chamador fornece valor, ordem e significado. |

<a id="mt23-mt24-code-map-file-018"></a>
#### 18. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/section_header/__init__.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/section_header/__init__.py` · SHA-256 `30bbfb1b70a66c9759fb213454a3baa201258e922c21f48159e4919641580f3d` |
| Papel e motivo técnico | Expõe cabeçalho legado e resolvido |
| Nomes disponibilizados | ["section_header_html", "section_header_html_resolvido"] |
| Entradas | import do subpacote |
| Saídas | duas funções públicas |
| Efeitos e limites | reexportação somente |
| Dependências e momento de uso | depende de section_header.py |
| Como interpretar este arquivo | `visual/section_header/__init__.py` reexporta `section_header_html` e `section_header_html_resolvido`. A fachada não escolhe etapa ou tema automaticamente. |

<a id="mt23-mt24-code-map-file-019"></a>
#### 19. `exemplo_section_header.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/section_header/exemplo_section_header.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/section_header/exemplo_section_header.py` · SHA-256 `ed6e729986ef7ef32c8357cf47e1b0c3cbfd82425d5203bbc19394d7e32c1aa9` |
| Papel e motivo técnico | Demonstra etapa 3/5 e override explícito fora do roteiro |
| Nomes disponibilizados | [] |
| Entradas | spark.sql current_user; números/textos sintéticos |
| Saídas | displayHTML e print parcial |
| Efeitos e limites | renderização de notebook sem escrita |
| Dependências e momento de uso | spark/displayHTML; Hub em sys.path |
| Como interpretar este arquivo | `visual/section_header/exemplo_section_header.py` mostra etapas 3 e 5 e um override fora do roteiro em `displayHTML`. O arquivo demonstra liberdade editorial da chamada; não altera `SECOES_EDA` nem grava saída. |

<a id="mt23-mt24-code-map-file-020"></a>
#### 20. `section_header.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/section_header/section_header.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/section_header/section_header.py` · SHA-256 `c1b641311281544aa5545688453eee0a9aa04cb9f08ef034d62cc44549ea92bb` |
| Papel e motivo técnico | Constrói cabeçalho HTML de etapa com defaults do mapa |
| Nomes disponibilizados | ["section_header_html", "section_header_html_resolvido"] |
| Entradas | etapa/emoji/titulo/descricao; ResolvedTheme na variante |
| Saídas | string HTML com textos escapados |
| Efeitos e limites | sem display/escrita; usa styles compartilhados, não CSS local fixo |
| Dependências e momento de uso | constants.emojis/styles e tema.ResolvedTheme |
| Como interpretar este arquivo | `visual/section_header/section_header.py` recebe número de etapa e possíveis overrides de emoji, título e descrição; para 0 a 8, usa `SECOES_EDA` como base. Devolve HTML com textos escapados e estilos compartilhados `STYLE_SECTION_*`; a variante resolvida considera o tema. A configuração explícita é recebida pela variante resolvida; carregar um tema não reescreve HTML já produzido. |

<a id="mt23-mt24-code-map-file-021"></a>
#### 21. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/tema/__init__.py) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/tema/__init__.py` · SHA-256 `d5e53daa73b46f62c6b4a1501a8927c3f621625c187be8820eb40cae40294055` |
| Papel e motivo técnico | Fixa API pública do núcleo V02 por import de subpacote |
| Nomes disponibilizados | ["ThemeError", "ResolvedTheme", "normalize_color", "resolve_theme", "load_theme", "load_reference_theme", "export_theme"] |
| Entradas | import do subpacote |
| Saídas | ThemeError, ResolvedTheme, normalize_color, resolve/load/reference/export |
| Efeitos e limites | reexportação; sem validação por si |
| Dependências e momento de uso | depende de tema.py |
| Como interpretar este arquivo | `visual/tema/__init__.py` reexporta `ThemeError`, `ResolvedTheme`, `normalize_color`, `resolve_theme`, `load_theme`, `load_reference_theme` e `export_theme`. É a rota pública para o núcleo, sem validar tema apenas por existir. |

<a id="mt23-mt24-code-map-file-022"></a>
#### 22. `exemplo_tema.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/tema/exemplo_tema.py) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/tema/exemplo_tema.py` · SHA-256 `a51f6e9a1d0141c800f9e5806c917d47f20f6273e1e80f0b6d9c2dc396d64676` |
| Papel e motivo técnico | Demonstra referência sintética, cópia, export e erro sem fallback |
| Nomes disponibilizados | [] |
| Entradas | HUB_ROOT opcional; bytes/tema em memória; nenhuma tabela |
| Saídas | prints de contexto/hash/erro; bytes exportados |
| Efeitos e limites | lê referência empacotada; não grava; executa validação local |
| Dependências e momento de uso | jsonschema/referencing em resolução; notebook ou Python local; descoberta de path |
| Como interpretar este arquivo | `visual/tema/exemplo_tema.py` parte de `HUB_ROOT` opcional, carrega referência empacotada, faz cópia em memória, exporta bytes e mostra contexto, hash e erro de alteração inválida. A saída impressa ilustra o resolvedor local; não produz arquivo de tema nem autorização de uso. |

<a id="mt23-mt24-code-map-file-023"></a>
#### 23. `tema.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/tema/tema.py) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/tema/tema.py` · SHA-256 `4ec1bdf49aeab0526ca234577cfb760da6c377e5d97abbaf3b9e9f2f154ccc33` |
| Papel e motivo técnico | Núcleo V02 valida configuração completa, recursos e identidade canônica |
| Nomes disponibilizados | ["ThemeError", "ResolvedTheme", "normalize_color", "resolve_theme", "load_theme", "load_reference_theme", "export_theme"] |
| Entradas | bytes UTF-8/dict JSON; root+relative_path; expected SHA/context |
| Saídas | ResolvedTheme imutável ou bytes exportados; falhas levantam ThemeError |
| Efeitos e limites | lê schema/assets/tema em escopo; não escreve/aplica/consulta rede; hash não autentica |
| Dependências e momento de uso | biblioteca padrão no import; jsonschema/referencing lazy na validação |
| Como interpretar este arquivo | `visual/tema/tema.py` aceita bytes UTF-8 ou documento JSON para resolver tema, ou raiz/caminho relativo para carregar um arquivo; também aceita contexto e hash esperados quando a operação os exige. Lê schema, manifesto e referência no escopo permitido, valida forma e semântica e devolve `ResolvedTheme` imutável ou bytes exportados; falhas levantam a exceção `ThemeError`. Não aplica aparência, grava tema nem consulta rede. Hash confere integridade dos bytes esperados, não autentica a pessoa autora; mudanças em diretórios pais durante a leitura ainda exigem atenção operacional. |

<a id="mt23-mt24-code-map-file-024"></a>
#### 24. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/theme_lab/__init__.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/theme_lab/__init__.py` · SHA-256 `dbe871002f5e5feba3d99889ef27300e97e40568dbf32bffcf142df88df14f46` |
| Papel e motivo técnico | Reexporta 25 símbolos do Visual Lab para import estável |
| Nomes disponibilizados | ["ThemeLabError", "ControlSpec", "ProposalReceipt", "ThemeLabPreview", "ThemeLabComparison", "ThemeLabPreset", "ThemeLabSessionReceipt", "ThemeLabSessionInfo", "get_control_specs", "ThemeLabDraft", "prepare_theme_lab_presets", "get_demo_presets", "create_theme_lab_from_preset", "save_theme_lab_session", "reopen_theme_lab_session", "list_theme_lab_sessions", "create_theme_lab", "build_preview", "compare_preview", "install_dbutils_fallback", "apply_dbutils_fallback", "ThemeLabUI", "ThemeLabLauncherUI", "build_ipywidgets_lab", "build_theme_lab_launcher"] |
| Entradas | import do subpacote |
| Saídas | ThemeLabDraft/receipts/UI/preview/presets/funções de sessão e fallback |
| Efeitos e limites | reexportação somente |
| Dependências e momento de uso | depende de theme_lab.py |
| Como interpretar este arquivo | `visual/theme_lab/__init__.py` reexporta o catálogo público de 25 símbolos do Lab, incluindo rascunho, controles, presets, prévias, comparação e recibos de proposta/sessão. Importe por essa fachada para evitar depender de helpers internos. |

<a id="mt23-mt24-code-map-file-025"></a>
#### 25. `exemplo_theme_lab.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/theme_lab/exemplo_theme_lab.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/theme_lab/exemplo_theme_lab.py` · SHA-256 `fd0fc2dc67e6fe104c8b7a595ea1219d56de332aa0eb28a17cfa06e76a26a0d6` |
| Papel e motivo técnico | Demonstra demo V05, comparação e launcher sem save_root |
| Nomes disponibilizados | [] |
| Entradas | placeholder assistant_root; presets sintéticos; widgets/display |
| Saídas | prints de dirty/undo/restore; prévias e UI |
| Efeitos e limites | sem gravação no exemplo; launcher pode escrever só em cópia preparada com save_root |
| Dependências e momento de uso | ipywidgets/IPython, pandas/Plotly nos previews; runtime notebook |
| Como interpretar este arquivo | `visual/theme_lab/exemplo_theme_lab.py` mostra preset, alterações, undo/restore, seis prévias e launcher. O placeholder de `assistant_root` precisa ser editado antes de executar tudo; sem `save_root` preparado, o exemplo não grava. A UI apresentada não substitui uma prova Python local da proposta salva. |

<a id="mt23-mt24-code-map-file-026"></a>
#### 26. `theme_lab.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/theme_lab/theme_lab.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/theme_lab/theme_lab.py` · SHA-256 `1a12b898a705bb96d43ae15cd918d6b069edbee0f7b6512b8599f85e731ad665` |
| Papel e motivo técnico | V05 administra rascunho, controles, seis prévias e sessões rastreáveis |
| Nomes disponibilizados | ["ThemeLabError", "ControlSpec", "ProposalReceipt", "ThemeLabPreview", "ThemeLabComparison", "ThemeLabPreset", "ThemeLabSessionReceipt", "ThemeLabSessionInfo", "get_control_specs", "ThemeLabDraft", "prepare_theme_lab_presets", "get_demo_presets", "create_theme_lab_from_preset", "save_theme_lab_session", "reopen_theme_lab_session", "list_theme_lab_sessions", "create_theme_lab", "build_preview", "compare_preview", "install_dbutils_fallback", "apply_dbutils_fallback", "ThemeLabUI", "ThemeLabLauncherUI", "build_ipywidgets_lab", "build_theme_lab_launcher"] |
| Entradas | ResolvedTheme notebook; updates; root/nome; widgets/dbutils opcionais |
| Saídas | Draft, specs, preview/comparison, receipts e sessão reaberta |
| Efeitos e limites | leitura de schema/presets; gravação exclusiva de proposta/sessão somente em save; sem aprovação/publicação |
| Dependências e momento de uso | tema + V03/V04; pandas/Plotly/ipywidgets importados por rota; root com ACL externa |
| Como interpretar este arquivo | `visual/theme_lab/theme_lab.py` recebe `ResolvedTheme` notebook, alterações de controles e, nas operações de salvamento, raiz/nome autorizados. Produz `ThemeLabDraft`, prévias, comparação e recibos; rascunho e prévia ficam em memória, enquanto `save_proposal` e a gravação de sessão escrevem somente quando explicitamente chamadas. Sessão com manifesto e proposta avulsa têm rastros diferentes. Widgets e `dbutils` são opcionais e podem exigir fallback; salvar não aprova nem publica tema. |

<a id="mt23-mt24-code-map-file-027"></a>
#### 27. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/theme_plotly/__init__.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/theme_plotly/__init__.py` · SHA-256 `f9adaaae5242514d9519a98c38c94a54dd6d88684e126127b0a3cde371b1143a` |
| Papel e motivo técnico | Expõe três legadas e quatro rotas V03/V07 |
| Nomes disponibilizados | ["get_tema_eda", "aplicar_tema", "registrar_template_plotly", "get_tokens_plotly", "get_tema_plotly", "aplicar_tema_resolvido", "registrar_template_plotly_resolvido"] |
| Entradas | import do subpacote |
| Saídas | get_tema_eda/aplicar_tema/registrar_template_plotly/get_tokens_plotly/get_tema_plotly/aplicar_tema_resolvido/registrar_template_plotly_resolvido |
| Efeitos e limites | reexportação somente |
| Dependências e momento de uso | depende de theme_plotly.py |
| Como interpretar este arquivo | `visual/theme_plotly/__init__.py` oferece três rotas legadas (`get_tema_eda`, `aplicar_tema`, `registrar_template_plotly`) e quatro rotas de leitura/aplicação/registro resolvidas. Importar a fachada não registra template global. |

<a id="mt23-mt24-code-map-file-028"></a>
#### 28. `exemplo_theme_plotly.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py` · SHA-256 `9bf72cfb269a30c3235b029c0e7e58bf99fa8ba278d9083265c1f86ee2bfe323` |
| Papel e motivo técnico | Compara figuras sintéticas antes/depois e referência resolvida |
| Nomes disponibilizados | [] |
| Entradas | spark.sql current_user; NumPy sintético; Plotly |
| Saídas | fig.show e prints de layout; assert igualdade V03/legado |
| Efeitos e limites | renderização em memória; não registra template nem grava |
| Dependências e momento de uso | numpy/plotly/spark notebook; V02 para seção V03 |
| Como interpretar este arquivo | `visual/theme_plotly/exemplo_theme_plotly.py` monta dados NumPy sintéticos e figuras Plotly, mostra comparações e verifica equivalência pontual entre layout V03 e legado. A figura fica na sessão; não registra template nem grava artefato. Um rótulo de fonte no notebook não descreve fielmente o gerador NumPy, portanto use os dados efetivos para interpretar a imagem. |

<a id="mt23-mt24-code-map-file-029"></a>
#### 29. `theme_plotly.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/visual/theme_plotly/theme_plotly.py) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py` · SHA-256 `b32ca5b996c3ff21302fa1f0e87125130a73189f61a60ad30390c889d57047bf` |
| Papel e motivo técnico | Adaptador Plotly preserva legado e oferece rota temática opt-in |
| Nomes disponibilizados | ["get_tema_eda", "aplicar_tema", "registrar_template_plotly", "get_tokens_plotly", "get_tema_plotly", "aplicar_tema_resolvido", "registrar_template_plotly_resolvido"] |
| Entradas | go.Figure; subtitulo/fonte/n; ResolvedTheme notebook/light; nome/flags |
| Saídas | dicionário layout/tokens, mesma Figure mutada, ou registro de template |
| Efeitos e limites | aplicar altera figura; registrar_template_* altera pio.templates e possivelmente default, não no import |
| Dependências e momento de uso | plotly + constants.colors + tema.export_theme |
| Como interpretar este arquivo | `visual/theme_plotly/theme_plotly.py` transforma tokens de notebook claro em layout Plotly. Recebe figura, subtítulo/fonte/contagem ou tema resolvido, conforme a função; devolve layout/tokens, a mesma figura alterada, ou registra um template. `aplicar_tema` modifica a figura recebida; `registrar_template_plotly` altera `pio.templates` e pode selecionar padrão global, enquanto a variante resolvida registra sem ativar por padrão. O chamador deve controlar esse efeito de sessão e conferir o contexto do tema. |



<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
