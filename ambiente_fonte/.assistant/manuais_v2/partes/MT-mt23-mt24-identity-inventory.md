# Leitura dos arquivos estruturados de identidade visual

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt23-mt24-identity-inventory"></a>
<a id="mt23-mt24-identity-inventory"></a>
### Leitura dos arquivos estruturados de identidade visual

Os arquivos desta seção explicam como a identidade visual passa de uma ideia para uma forma que o software consegue ler. Cada ficha apresenta uma responsabilidade concreta: definir o formato de um tema, fornecer uma instância completa, relacionar nomes a recursos, organizar decisões de tradução ou configurar um aplicativo. Ao ler o caminho, identifique primeiro esse papel. Arquivos com extensão JSON podem ter formatos e autoridades muito diferentes.

Um schema é a norma que descreve a estrutura aceita. Uma instância é um documento que precisa obedecer a essa norma. Uma fixture é uma instância preparada para demonstração ou teste. Um manifesto associa nomes a recursos e versões verificáveis. O tema de exemplo fornece valores; ele não modifica as regras do schema. O manifesto permite conferir bytes de imagens; ele não renderiza imagens. Essa distinção ajuda a localizar a origem de um erro e o arquivo que precisa de uma alteração coordenada.

As fichas indicam o produtor e o consumidor porque um campo só produz efeito quando alguma operação o lê. Os metadados de proveniência preservam a história de construção. O hash permite comparar o conteúdo com os bytes esperados. Nenhum desses registros, isoladamente, demonstra implantação, aplicação visual no destino ou aprovação humana de marca. Para avaliar uma proposta, combine validação de estrutura, interpretação dos valores e inspeção do resultado na superfície correspondente.

Os exemplos notebook e editoriais usam grupos distintos de tokens, que são os valores de cor, tamanho e geometria consumidos pelos adaptadores. A ponte AI/BI acrescenta uma matriz de capacidades do produto de destino. O arquivo YAML do App descreve inicialização e variáveis do ambiente. Compare essas responsabilidades antes de copiar uma configuração entre contextos. Os mapas de campos dos capítulos explicam as regras internas; estas fichas mostram por que cada arquivo particular participa do conjunto.

<a id="mt23-mt24-identity-inventory-file-001"></a>
#### 1. `theme.schema.json`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/theme.schema.json) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/theme.schema.json` · SHA-256 `4fa814190590f28e88ec03ad1459b96aa2eb01be0762773a1b27e329ae8fc81e` |
| Por que existe | Única norma de forma do tema Hub V01/V02: distingue metadados de tema, 48 tokens notebook e 32 editoriais, sem depender de uma fixture. |
| Produtor | Frente de contrato V01, transportada ao padrão de produto V02; mudanças exigem revisão de consumidores e regeneração de TOKENS.md. |
| Consumidor e operação de leitura | tema.py lê bytes com SHA fixo, valida Draft 2020-12 e semântica; tools/temas_v02_check.py e mapas MT23 auditam o mesmo contrato. |
| Formato e campos | JSON Schema Draft 2020-12; raiz fechada e 11 required; $defs.notebookTokens (48) e editorialTokens (32), ambos fechados; allOf escolhe tokens/asset_set_id por context. x-hub-policy inclui candidate, limites, font allowlist e app/aibi reservados; x-hub em tokens descreve defaults declarativos e consumidores. |
| Autoridade e interpretação | Norma de campos do tema Hub; x-hub-policy.candidate é rótulo do arquivo, não estado vivo V14; defaults declarativos não são injetados pelo resolvedor. |
| Efeitos | Leitura/validação local; não grava tema, não aplica visual, não aprova marca. |
| Exemplo e limites | context=notebook exige asset_set_id=sem-assets e tokens notebook; readme/presentation exigem editorial-v2-congelado e 32 tokens. |

<a id="mt23-mt24-identity-inventory-file-002"></a>
#### 2. `assets.json`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/assets.json) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/assets.json` · SHA-256 `8a57ddea7a2bc5407726d02d75786d4611e464c99f8ab3a6ecfe89c10bff4905` |
| Por que existe | Amarra nomes fechados de conjuntos a bytes de recursos editoriais; impede que um tema escolha caminho livre ou substituição silenciosa. |
| Produtor | Registro de contrato V01 transportado ao produto; source_commit e verified_against_commit são metadados históricos do manifesto. |
| Consumidor e operação de leitura | tema.py lê com _ASSETS_SHA e _asset_manifest; tools/readme_visuals/theme_assets.mjs e verificadores de temas usam o registro. |
| Formato e campos | purpose, source_commit, sets, verified_against_commit. sets.sem-assets=[]; sets.editorial-v2-congelado contém 12 objetos {path,sha256}: 2 headers PNG e 5 pares PNG/SVG de README. |
| Autoridade e interpretação | Registro normativo local de asset_set_id e hashes, não registro de novas aprovações visuais; os 12 recursos permanecem fora desta lista de nove arquivos. |
| Efeitos | A leitura valida hashes e pode recusar recurso divergente; o JSON não renderiza ou escreve PNG/SVG. |
| Exemplo e limites | Tema notebook escolhe sem-assets; tema editorial escolhe editorial-v2-congelado; SHA errado interrompe resolução. |

<a id="mt23-mt24-identity-inventory-file-003"></a>
#### 3. `legado_notebook.json`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/exemplos/legado_notebook.json) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/exemplos/legado_notebook.json` · SHA-256 `c820c56416af38cbf1faf29d924ae199dc2ece8570026394325c93567d4bc207` |
| Por que existe | Retém baseline visual notebook legado para comparação e leitura retrocompatível. |
| Produtor | Fixture derivada da referência V00 no pacote V01; não produzida por resolução runtime. |
| Consumidor e operação de leitura | tema.py load_reference_theme('notebook'); theme_lab preset legado_notebook; testes V02/V13 usam o arquivo. |
| Formato e campos | 11 campos obrigatórios de tema, context=notebook, mode=light, asset_set_id=sem-assets, 48 tokens explícitos. Ex.: brand.primary=#005CA9, status.warn_text=#B26A00, palette.curves_legacy com 6 cores, chart.footer_px=10. |
| Autoridade e interpretação | Instância/fixture completa sob o schema; seus valores não alteram o schema nem são identidade aprovada. |
| Efeitos | Pode ser lida e resolvida; arquivo isolado não altera notebook nem aplica tema. |
| Exemplo e limites | Uma cópia em memória sem brand.primary deve falhar SCHEMA_REQUIRED; referência íntegra expõe warnings de validação sem aprovação. |

<a id="mt23-mt24-identity-inventory-file-004"></a>
#### 4. `executivo_claro_exemplo.json`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/exemplos/executivo_claro_exemplo.json) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/exemplos/executivo_claro_exemplo.json` · SHA-256 `53429a210fd024c35e6b99c3917b04ec437787379ea50227a7fa37cdb5dc5438` |
| Por que existe | Mostra uma proposta notebook clara que modifica valores sem criar novo contexto ou herança implícita. |
| Produtor | Fixture sintética V01; autora da proposta fornece documento completo. |
| Consumidor e operação de leitura | theme_lab preset executivo_claro; tools/temas_v01_contract.py e temas_v02_check.py conferem fixture; tema.py pode resolver por load_theme explícito, mas load_reference_theme não a seleciona. |
| Formato e campos | 11 campos, context=notebook, mode=light, sem-assets, 48 tokens. Difere do legado em 7 valores: text.secondary, status.warn_text, semantic.positive, semantic.warning, chart.footer_px, section.description_px, badge.font_px. |
| Autoridade e interpretação | Instância candidata sintética, não padrão de tema/quarta referência pública. |
| Efeitos | Leitura e prévia se consumidor chamar rota temática; arquivo não instala, aprova ou grava. |
| Exemplo e limites | status.warn_text muda #B26A00→#805000 e chart.footer_px 10→12, mas nenhum contraste é certificado apenas por esse delta. |

<a id="mt23-mt24-identity-inventory-file-005"></a>
#### 5. `legado_editorial.json`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/exemplos/legado_editorial.json) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/exemplos/legado_editorial.json` · SHA-256 `0ac57489a92a1e8006a09797e326890e44f3f24de81df0ae0afe6df0e7f371df` |
| Por que existe | Preserva escolhas de tokens.yaml v2 e canvas readme_standard como referência de conteúdo editorial. |
| Produtor | Fixture V01 derivada dos tokens editoriais históricos; não substitui arquivos de imagem congelados. |
| Consumidor e operação de leitura | tema.py load_reference_theme('readme'); tools/readme_visuals/theme_assets.mjs seleciona o tema editorial por `--theme-id`; a ponte resolve esse ID no diretório canônico de exemplos e entrega um derivado validado; verificadores V02 conferem fixture. |
| Formato e campos | 11 campos, context=readme, mode=dark, asset_set_id=editorial-v2-congelado, 32 tokens; font.family=editorial_inter, geometry.glow_opacity=0.16, canvas=1400×900. |
| Autoridade e interpretação | Instância editorial completa sob schema; valores históricos não definem aprovação de novas imagens nem renderização universal. |
| Efeitos | Resolução confere manifesto de 12 recursos; JSON sozinho não recolore assinaturas congeladas. |
| Exemplo e limites | canvas.width_px=1400 é metadado da proposta e não substitui dimensões do contrato de cada figura V06. |

<a id="mt23-mt24-identity-inventory-file-006"></a>
#### 6. `apresentacao_exemplo.json`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/exemplos/apresentacao_exemplo.json) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/exemplos/apresentacao_exemplo.json` · SHA-256 `e2724bcc31f7b4f5398c51db1f671aec1f2ba022bb1ae006c8b56fdceaed79d0` |
| Por que existe | Fornece documento completo de presentation_hero para comparar contexto presentation com readme. |
| Produtor | Fixture sintética V01 do perfil presentation_hero; não é exportador ou apresentação homologada. |
| Consumidor e operação de leitura | tema.py load_reference_theme('presentation'); verificadores V02 leem a fixture; compositor editorial só usa tema quando receber candidato explicitamente. |
| Formato e campos | 11 campos, context=presentation, mode=dark, editorial-v2-congelado, 32 tokens. Valores editoriais iguais a legado_editorial exceto canvas.width_px=1600 contra 1400; height_px=900. |
| Autoridade e interpretação | Instância editorial, não novo schema; trocar context sozinho sem tokens/asset set coerentes falha. |
| Efeitos | Pode ser lida/resolvida; não gera slide nem publica apresentação. |
| Exemplo e limites | canvas 1600×900 ilustra perfil hero, não obriga cada export ou figura a adotar esse tamanho. |

<a id="mt23-mt24-identity-inventory-file-007"></a>
#### 7. `aibi_mapping.json`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/aibi/aibi_mapping.json) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/aibi_mapping.json` · SHA-256 `98dba3149203a174c7ef76f5aac5636e9c3ab34fcd37ae120200347da831996f` |
| Por que existe | Classifica, token a token, o que pode ser traduzido diretamente, aproximado manualmente ou não tem equivalente seguro no dashboard. |
| Produtor | Frente V11 revisou matriz de capacidade documentada e datas das fontes; mudança exige atualização coordenada de SHA embutido no loader. |
| Consumidor e operação de leitura | _aibi_theme_impl.py _load_mapping/project_theme/export_projection; MT24_BRIDGE_FIELD_MAP.md documenta campos e 48 linhas. |
| Formato e campos | contract_version=1, source_context=notebook, target_product, native_theme_json_schema_status, native_import_ready_by_default=false, classifications, binding_strategies, 13 capabilities, 48 mappings {hub_token,classification,target_capability,binding_strategy,note}, 3 official_sources. Contagem: 3 translated/direct, 23 approximated/manual, 22 unsupported/none. |
| Autoridade e interpretação | Norma local da ponte Hub, não schema JSON nativo Databricks; fontes oficiais verificadas em 2026-09-14 e estado de formato nativo limitado ao conhecimento registrado. |
| Efeitos | Loader confere SHA e unicidade/shape; projeção gera formato Hub em memória, nunca Import theme nem API remota. |
| Exemplo e limites | surface.card→widget.background é direct; semantic.positive→dashboard.color_mappings requer revisão manual; status.warn_bg é unsupported. |

<a id="mt23-mt24-identity-inventory-file-008"></a>
#### 8. `dashboard_sintetico.json`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/aibi/dashboard_sintetico.json) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/dashboard_sintetico.json` · SHA-256 `d0ab3bdaa977c2284ac86c0456277c9ffa64fe1e834950a4de8b3ea9cc9c01ee` |
| Por que existe | Fornece oráculo semântico local para detectar quando uma mudança de tema alterou consultas, filtros ou widgets. |
| Produtor | Fixture V11 do Hub, com dados declaradamente sintéticos e sem dataset remoto. |
| Consumidor e operação de leitura | tools/tests/test_temas_v11.py, tools/tests/test_temas_v12.py e tools/temas_v13_ensaios.py leem JSON para fingerprint/asserções semânticas. |
| Formato e campos | fixture_version=1, kind=hub_v11_synthetic_dashboard_draft, databricks_importable=false, data_classification=synthetic_only, purpose; 1 dataset grain mes_segmento, 2 queries, 2 filters, 5 widgets (KPI/line/bar/table/text), 7 theme_test_cases. |
| Autoridade e interpretação | Fixture de teste, não export nativo nem contrato de dashboard Databricks. |
| Efeitos | Leitura local e cálculo de fingerprint/asserções; não cria, importa ou publica dashboard. |
| Exemplo e limites | q_evolucao usa campos mes/clientes_ativos; filtro f_mes aplica between; mudança de cor não pode mudar semantic_signature da query. |

<a id="mt23-mt24-identity-inventory-file-009"></a>
#### 9. `app.yaml`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/databricks_app/app.yaml) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app.yaml` · SHA-256 `2dbfd83c852cb0812d972de29281dd309e5958569162837ae15bbd99c5b3ac67` |
| Por que existe | Declara comando de inicialização e injeção de recurso de persistência do Databricks App sem embutir caminho ou segredo. |
| Produtor | Bundle V10 de App; operador autorizado precisa vincular theme_storage a Volume no destino. |
| Consumidor e operação de leitura | Plataforma Databricks App resolve env no deploy; app_service.load_config lê HUB_THEME_VOLUME/HUB_THEME_APP_MODE; tools/temas_v10_app.py confere texto do bundle. |
| Formato e campos | YAML command=['streamlit','run','app.py']; env: HUB_THEME_VOLUME valueFrom=theme_storage; HUB_THEME_APP_MODE=authoring_only; STREAMLIT_GATHER_USAGE_STATS='false'. |
| Autoridade e interpretação | Configuração declarativa do bundle, não schema de tema nem prova de deploy/ACL. |
| Efeitos | Quando implantado, inicia Streamlit e injeta variável do recurso; arquivo no Git não executa processo, não cria Volume e não concede permissão. |
| Exemplo e limites | Sem binding do recurso theme_storage, load_config deve parar fora de modo local explícito; path de Volume não deve ser hardcoded neste YAML. |



<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
