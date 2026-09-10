# Databricks notebook source
# MAGIC %md
# MAGIC # Hub Snippets
# MAGIC
# MAGIC > A biblioteca matemática e algorítmica central do ecossistema `.assistant`: funções e classes reutilizáveis, revisadas e testadas para fluxos de Machine Learning e Big Data no Databricks.
# MAGIC
# MAGIC > **CONTEÚDO CUSTOMIZADO PELO HUB.** `hub_snippets` não é uma biblioteca institucional da Databricks nem é carregada automaticamente pela Genie Code. O notebook precisa tornar o pacote visível ao Python e importar explicitamente a função desejada.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🧭 Neste Guia
# MAGIC
# MAGIC | Para entender... | Vá para... |
# MAGIC |---|---|
# MAGIC | o conceito e a estrutura de um snippet | [O que é um Snippet](#-o-que-é-um-snippet-neste-ecossistema) |
# MAGIC | as categorias da biblioteca | [Mapa de Categorias](#-mapa-de-categorias-do-hub-snippets) |
# MAGIC | quais objetos estão disponíveis | [Catálogo Detalhado](#-catálogo-detalhado-por-categoria) |
# MAGIC | como importar e executar | [Passo a Passo Operacional](#️-passo-a-passo-operacional-como-usar-um-snippet) |
# MAGIC | runtime, dependências e custo | [Onde o Código Executa](#️-onde-o-código-executa-e-quanto-pode-custar) |
# MAGIC | dúvidas e limitações | [Perguntas Frequentes](#-perguntas-frequentes-faq) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <a id="-o-que-é-um-snippet-neste-ecossistema"></a>
# MAGIC
# MAGIC ## 🧩 O que é um Snippet neste Ecossistema?
# MAGIC
# MAGIC No desenvolvimento de software tradicional, a palavra *snippet* costuma significar um pedaço solto de código copiado de fóruns da internet.
# MAGIC
# MAGIC **Neste ecossistema, um Snippet é algo diferente: é uma peça reutilizável de engenharia analítica.**
# MAGIC
# MAGIC Pense nos snippets como funções de uma biblioteca especializada:
# MAGIC
# MAGIC - Você não precisa reprogramar rotinas numéricas ou reimplementar fórmulas do zero toda vez que construir um modelo; pode reutilizar blocos com contrato, exemplo e testes conhecidos.
# MAGIC - Em Machine Learning, isso reduz retrabalho em cálculos como *Population Stability Index* (PSI), junções temporais, métricas e análise de safras (*Vintage Analysis*).
# MAGIC - A reutilização não elimina a validação: assinatura, dependências, volume, instante de decisão e significado de negócio continuam precisando ser conferidos.
# MAGIC
# MAGIC ```text
# MAGIC ┌─────────────────────────────────────────────────────────────────────────────┐
# MAGIC │                            O QUE DEFINE UM SNIPPET                          │
# MAGIC │                                                                             │
# MAGIC │   🛡️ Efeito Declarado: transformação, coleta ou estado precisam ser claros │
# MAGIC │   📐 Lógica Revisável: fórmula, premissas e limites ficam no código         │
# MAGIC │   ⚡ Execução Adequada: Pandas ou Spark conforme o tipo e o volume          │
# MAGIC │   🧪 Evidência Delimitada: testes e exemplos cobrem cenários conhecidos     │
# MAGIC └─────────────────────────────────────────────────────────────────────────────┘
# MAGIC ```
# MAGIC
# MAGIC Cada snippet resolve uma **dor analítica específica**, expondo uma API pública curta. A linha de `import` simplifica o uso, mas não substitui a leitura do contrato.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🏛️ Arquitetura e o Padrão "Pasta de Objeto"
# MAGIC
# MAGIC Para favorecer que o código seja limpo, fácil de encontrar e intuitivo tanto para pessoas quanto para a IA, os snippets seguem o padrão de organização chamado **Pasta de Objeto**.
# MAGIC
# MAGIC Na estrutura vigente, cada snippet fica em um diretório autossuficiente com três componentes centrais:
# MAGIC
# MAGIC ![Arquitetura da pasta de um snippet](./assets/diagramas/01_arquitetura_pasta.png)
# MAGIC
# MAGIC > **Leitura textual do diagrama:** cada objeto possui um `__init__.py` que
# MAGIC > expõe a API pública, um módulo com a implementação e um
# MAGIC > `exemplo_<nome>.py` que importa essa API e demonstra o contrato exercitado.
# MAGIC
# MAGIC ### O que cada arquivo faz
# MAGIC
# MAGIC 1. **`__init__.py` (A Fachada):** reexporta as funções e classes públicas. É ele que permite imports curtos sem expor a organização interna do módulo.
# MAGIC 2. **`nome_do_snippet.py` (O Motor):** contém implementação, validações, tipagem e docstring. O código é a fonte técnica para a assinatura real.
# MAGIC 3. **`exemplo_nome_do_snippet.py` (O Guia Didático):** demonstra o uso com dados sintéticos e registra uma saída observada. Ele ensina o contrato exercitado; não promete compatibilidade com qualquer runtime ou volume.
# MAGIC
# MAGIC O Catálogo de Helpers (`.assistant/CATALOGO_HELPERS.md`) relaciona demanda, caminho público e dependências. Ele é o índice canônico; este README preserva uma leitura narrativa por categoria.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <a id="-mapa-de-categorias-do-hub-snippets"></a>
# MAGIC
# MAGIC ## 🗺️ Mapa de Categorias do Hub Snippets
# MAGIC
# MAGIC A biblioteca é dividida em seis categorias funcionais que acompanham as principais etapas de um fluxo analítico:
# MAGIC
# MAGIC ![Mapa das categorias do Hub Snippets](./assets/diagramas/02_mapa_categorias.png)
# MAGIC
# MAGIC > **Leitura textual do diagrama:** a biblioteca se divide em seis categorias:
# MAGIC > `ml`, `spark`, `display`, `visual`, `constants` e `testing`.
# MAGIC > Cada ramo agrupa objetos com uma responsabilidade técnica distinta.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <a id="-catálogo-detalhado-por-categoria"></a>
# MAGIC
# MAGIC ## 📚 Catálogo Detalhado por Categoria
# MAGIC
# MAGIC Abaixo você encontra o papel de cada objeto e o momento em que ele pode ser útil. Consulte o módulo e o notebook correspondente antes de adotar a função em um pipeline.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 1. Categoria: `ml` (Machine Learning e Estatística Aplicada)
# MAGIC
# MAGIC *É o coração algorítmico do Hub, voltado a modelagem preditiva, risco de crédito, séries temporais e governança de modelos.*
# MAGIC
# MAGIC #### 🕒 Engenharia Temporal e Séries Temporais
# MAGIC
# MAGIC - **`lgbm_temporal`**: prepara atributos temporais e treina LightGBM com parâmetros declarados.
# MAGIC   - *Quando usar:* em problemas temporais nos quais a disponibilidade histórica de cada atributo foi validada. LightGBM é dependência opcional; ausência do pacote impede esse fluxo.
# MAGIC - **`split_temporal`**: divide um `pandas.DataFrame` em treino, validação e teste por períodos completos de calendário, com gaps opcionais.
# MAGIC   - *Quando usar:* quando a avaliação precisa preservar ordem temporal. O helper não recebe datas finais fixas; recebe proporções, unidade de período e quantidade de gaps.
# MAGIC - **`walk_forward`**: produz janelas sucessivas de validação temporal.
# MAGIC   - *Quando usar:* para avaliar estabilidade ao longo de múltiplos cortes históricos, depois de definir tamanho das janelas e política de reentreino.
# MAGIC - **`vintage_analysis`**: constrói curvas de safra e maturação por período de originação.
# MAGIC   - *Quando usar:* em risco, retenção ou eventos cujo denominador, janela e censura tenham sido definidos.
# MAGIC
# MAGIC #### 📊 Risco de Crédito e Scorecards
# MAGIC
# MAGIC - **`woe_iv_calculator`**: calcula *Weight of Evidence* (WOE) e *Information Value* (IV) para os tipos suportados.
# MAGIC   - *Quando usar:* como diagnóstico ou transformação em scorecards, com binning, target e tratamento de categorias explicitamente revisados.
# MAGIC - **`scorecard_builder`**: converte um modelo logístico compatível em uma escala de pontos configurável.
# MAGIC   - *Quando usar:* quando a escala, odds, PDO e coeficientes foram validados. Transparência do cálculo não equivale a aprovação regulatória.
# MAGIC - **`score_bands`**: organiza um score em faixas e resume evento e volumetria.
# MAGIC   - *Quando usar:* para estudar cortes operacionais; a política de decisão continua externa ao helper.
# MAGIC
# MAGIC #### 📈 Avaliação, Métricas e Visualização
# MAGIC
# MAGIC - **`metrics_report`**: consolida métricas de classificação, como AUC, Gini, KS, F1, LogLoss e Brier quando aplicáveis.
# MAGIC   - *Quando usar:* para comparar modelos sob a mesma população, target, unidade e estratégia de corte.
# MAGIC - **`curves_plotly`**: produz figuras interativas de ROC, Precision-Recall, ganho e KS.
# MAGIC   - *Quando usar:* na análise de thresholds e na comunicação visual, conferindo se a escala do KS é razão ou percentual.
# MAGIC - **`explainability_report`**: organiza importância e explicações locais ou globais para modelos suportados.
# MAGIC   - *Quando usar:* em revisão técnica. Explicabilidade descreve o comportamento do modelo; não demonstra causalidade.
# MAGIC
# MAGIC #### 🛡️ Monitoramento e MLOps
# MAGIC
# MAGIC - **`performance_monitor`**: compara métricas observadas com limiares e períodos configurados.
# MAGIC   - *Quando usar:* dentro de uma rotina de monitoramento. A classe calcula quando chamada; não agenda tarefas, não envia alertas e não retreina sozinha.
# MAGIC - **`drift_detection`**: reúne diagnósticos de mudança de distribuição.
# MAGIC   - *Quando usar:* para investigar alteração entre referência e período atual. Drift não prova, sozinho, degradação de performance.
# MAGIC - **`mlflow_run`**: wrapper para abertura e registro governado de runs no MLflow.
# MAGIC   - *Quando usar:* quando experimento, tags, parâmetros e artefatos foram definidos. O run é um efeito externo intencional.
# MAGIC
# MAGIC #### 🔍 Não Supervisionado e Anomalias
# MAGIC
# MAGIC - **`clustering_suite`**: compara configurações de clustering com as métricas implementadas.
# MAGIC   - *Quando usar:* para apoiar seleção de configuração; métricas internas não substituem utilidade de negócio.
# MAGIC - **`cluster_profiling`**: resume diferenças entre grupos encontrados.
# MAGIC   - *Quando usar:* para interpretar clusters, evitando converter automaticamente padrões estatísticos em personas definitivas.
# MAGIC - **`isolation_forest`**: aplica detecção de anomalias e organiza seu perfil.
# MAGIC   - *Quando usar:* como mecanismo de priorização investigativa. Uma anomalia não é sinônimo de fraude.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 2. Categoria: `spark` (Operações Distribuídas em Escala)
# MAGIC
# MAGIC *Voltada a operações sobre DataFrames PySpark, mantendo o processamento principal no cluster e declarando as coletas necessárias.*
# MAGIC
# MAGIC - **`pit_join` (Point-in-Time Join)**: relaciona eventos a registros históricos disponíveis até o instante de decisão.
# MAGIC   - *Quando usar:* na construção de bases analíticas em que cada entidade possui uma data de referência. Chaves, duplicidades e atraso de publicação precisam ser definidos.
# MAGIC - **`psi_calculator`**: calcula PSI numérico e CSI categórico com agregações Spark.
# MAGIC   - *Quando usar:* para comparar distribuições. O resultado final e distribuições agregadas são coletados no driver; linhas completas não são coletadas pelo cálculo numérico.
# MAGIC - **`null_summary`**: resume nulos e padrões configurados em DataFrames Spark.
# MAGIC   - *Quando usar:* no perfil inicial, considerando que agregações sobre tabela larga podem exigir leitura ampla.
# MAGIC - **`smart_sample`**: cria amostra simples ou estratificada segundo os parâmetros fornecidos.
# MAGIC   - *Quando usar:* para prototipação controlada. Amostra não garante representatividade sem validação do desenho.
# MAGIC - **`date_features`**: deriva atributos de calendário em PySpark.
# MAGIC   - *Quando usar:* depois de confirmar timezone, calendário e instante de disponibilidade das novas colunas.
# MAGIC - **`join_diagnostics`**: mede cobertura, duplicidade, perda e expansão de linhas em joins.
# MAGIC   - *Quando usar:* antes e depois de cruzamentos relevantes. A API pública é `diagnosticar_join`.
# MAGIC - **`safe_display`**: limita a quantidade exibida no notebook.
# MAGIC   - *Quando usar:* na inspeção visual. Limitar exibição protege a interface, mas não torna qualquer transformação anterior barata.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 3. Categoria: `display` (Exibição e Tabelas Formatadas)
# MAGIC
# MAGIC *Focada na apresentação didática de dados tabulares dentro dos notebooks.*
# MAGIC
# MAGIC - **`dataframe_styled`**: aplica formatação e recursos visuais a DataFrames pandas.
# MAGIC   - *Quando usar:* em relatórios e inspeções com volume compatível com o driver.
# MAGIC - **`distribution_grid`**: organiza múltiplas distribuições em uma grade compacta.
# MAGIC   - *Quando usar:* em EDA; limites e amostras devem ser definidos antes da conversão para estruturas locais.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 4. Categoria: `visual` (Identidade Visual e Design em Plotly)
# MAGIC
# MAGIC *Favorece consistência estética nos gráficos e capítulos de notebook.*
# MAGIC
# MAGIC - **`theme_plotly`**: aplica o tema visual do Hub a figuras ou à sessão, conforme a função chamada.
# MAGIC   - *Quando usar:* quando o notebook deve adotar a identidade visual do projeto. Alterações de template global são efeitos de sessão, não funções puras.
# MAGIC - **`section_header`**: renderiza cabeçalhos, subtítulos e badges em HTML.
# MAGIC   - *Quando usar:* para dividir notebooks longos em capítulos claros; confirme onde HTML é aceito.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 5. Categoria: `constants` (Padrões Brasileiros)
# MAGIC
# MAGIC *Funções e constantes de formatação cultural e identidade visual.*
# MAGIC
# MAGIC - **`format_br`**: converte números em strings no padrão brasileiro:
# MAGIC   - Moeda: `1250000.5` ➔ `R$ 1.250.000,50`
# MAGIC   - Porcentagem: `0.154` ➔ `15,4%`
# MAGIC   - Inteiro: `15000` ➔ `15.000`
# MAGIC   - *Quando usar:* ao apresentar resumos, métricas e KPIs. A função de inteiro não acrescenta unidade automaticamente.
# MAGIC - **`colors` e `styles`**: concentram paletas e convenções visuais do Hub.
# MAGIC   - *Quando usar:* para evitar cores e estilos divergentes entre notebooks.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 6. Categoria: `testing` (Dados Sintéticos e Fixtures)
# MAGIC
# MAGIC *Acelera desenvolvimento e testes ao reduzir a dependência de bases externas.*
# MAGIC
# MAGIC - **`fixtures`**: geradores de dados sintéticos para cenários tabulares, contratos, transações e séries temporais.
# MAGIC   - *Quando usar:* em exemplos, regressões e protótipos reproduzíveis. Dados sintéticos exercitam propriedades escolhidas; não representam automaticamente a distribuição real.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📋 Inventário Completo da Biblioteca
# MAGIC
# MAGIC O catálogo narrativo acima destaca os objetos mais recorrentes. O mapa abaixo completa a visão da biblioteca, incluindo os componentes especializados que podem ser necessários em séries temporais, survival, ranking, deep learning e apresentação visual.
# MAGIC
# MAGIC ```text
# MAGIC hub_snippets/
# MAGIC ├── constants
# MAGIC │   ├── colors             ├── emojis
# MAGIC │   ├── format_br          └── styles
# MAGIC ├── display
# MAGIC │   ├── correlation_matrix ├── dataframe_styled
# MAGIC │   └── distribution_grid
# MAGIC ├── ml
# MAGIC │   ├── arima_wrapper      ├── autoencoder_anomaly
# MAGIC │   ├── cluster_profiling  ├── clustering_suite
# MAGIC │   ├── curves_plotly      ├── drift_detection
# MAGIC │   ├── explainability_report
# MAGIC │   ├── isolation_forest   ├── kaplan_meier
# MAGIC │   ├── lgbm_ranker        ├── lgbm_temporal
# MAGIC │   ├── metrics_report     ├── mlflow_run
# MAGIC │   ├── mlp_embeddings     ├── optuna_lgbm
# MAGIC │   ├── performance_monitor
# MAGIC │   ├── prophet_wrapper    ├── score_bands
# MAGIC │   ├── scorecard_builder  ├── shap_explainer
# MAGIC │   ├── split_temporal     ├── survival_cox
# MAGIC │   ├── tabnet_wrapper     ├── train_catboost
# MAGIC │   ├── train_lgbm         ├── train_xgboost
# MAGIC │   ├── umap_viz           ├── vintage_analysis
# MAGIC │   ├── walk_forward       └── woe_iv_calculator
# MAGIC ├── spark
# MAGIC │   ├── date_features      ├── join_diagnostics
# MAGIC │   ├── null_summary       ├── pit_join
# MAGIC │   ├── psi_calculator     ├── safe_display
# MAGIC │   └── smart_sample
# MAGIC ├── testing
# MAGIC │   └── fixtures
# MAGIC └── visual
# MAGIC     ├── badge              ├── divider
# MAGIC     ├── index_generator    ├── kpi_card
# MAGIC     ├── section_header     └── theme_plotly
# MAGIC ```
# MAGIC
# MAGIC > **Como usar este inventário:** escolha o objeto pelo problema, abra seu `exemplo_<nome>.py` e confirme API, dependências e tipo de retorno no Catálogo de Helpers (`.assistant/CATALOGO_HELPERS.md`).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <a id="️-passo-a-passo-operacional-como-usar-um-snippet"></a>
# MAGIC
# MAGIC ## 🛠️ Passo a Passo Operacional: Como Usar um Snippet
# MAGIC
# MAGIC Usar um snippet envolve quatro decisões: localizar o exemplo, tornar o pacote importável, chamar a API real e validar o resultado.
# MAGIC
# MAGIC ![Fluxo operacional para utilizar um snippet](./assets/diagramas/03_fluxo_operacional.png)
# MAGIC
# MAGIC > **Leitura textual do diagrama:** escolha o objeto pelo problema, consulte o
# MAGIC > exemplo, confirme assinatura e dependências, configure o caminho Python,
# MAGIC > importe explicitamente e valide a saída antes de reutilizá-la.
# MAGIC
# MAGIC ### Passo 1: Inspecione o notebook modelo
# MAGIC
# MAGIC Abra o arquivo `exemplo_<snippet>.py`. Ele mostra a função chamada, os dados sintéticos usados e a forma da saída observada. Confirme se o seu cenário respeita as mesmas premissas.
# MAGIC
# MAGIC ### Passo 2: Torne a biblioteca visível ao Python
# MAGIC
# MAGIC A pasta `.assistant` não entra automaticamente no `sys.path` só por existir no workspace. Informe a raiz que contém `hub_snippets/`:
# MAGIC
# MAGIC ```python
# MAGIC from pathlib import Path
# MAGIC import sys
# MAGIC
# MAGIC assistant_root = Path("/Workspace/Users/<username>/.assistant")
# MAGIC if str(assistant_root) not in sys.path:
# MAGIC     sys.path.insert(0, str(assistant_root))
# MAGIC ```
# MAGIC
# MAGIC Troque `<username>` pelo diretório autorizado ou use a raiz equivalente do seu Git folder. Em compute serverless, outra opção é declarar dependências pelo **Environment** ou pelo ambiente do Git folder, conforme o fluxo adotado.
# MAGIC
# MAGIC ### Passo 3: Importe e execute com a assinatura real
# MAGIC
# MAGIC ```python
# MAGIC # Exemplo 1: engenharia temporal em pandas
# MAGIC from hub_snippets.ml.split_temporal import temporal_split
# MAGIC
# MAGIC df_treino, df_val, df_teste = temporal_split(
# MAGIC     df=meu_dataframe,
# MAGIC     date_col="data_safra",
# MAGIC     train_pct=0.70,
# MAGIC     val_pct=0.15,
# MAGIC     gap_periods=1,
# MAGIC     period_unit="M",
# MAGIC )
# MAGIC
# MAGIC # Exemplo 2: monitoramento numérico em Spark
# MAGIC from hub_snippets.spark.psi_calculator import calcular_psi
# MAGIC
# MAGIC resultado_psi = calcular_psi(
# MAGIC     df_base=dados_referencia_spark,
# MAGIC     df_atual=dados_atuais_spark,
# MAGIC     col="score_credito",
# MAGIC     n_bins=20,
# MAGIC )
# MAGIC ```
# MAGIC
# MAGIC Os parâmetros acima correspondem às APIs atuais: `temporal_split` não recebe `train_end`/`val_end`, e `calcular_psi` usa `df_base`, `df_atual`, `col` e `n_bins`.
# MAGIC
# MAGIC ### Passo 4: Interprete e apresente
# MAGIC
# MAGIC Os snippets retornam DataFrames pandas, DataFrames PySpark, dicionários, escalares, modelos ou figuras, conforme o objeto. Antes de encadear a saída:
# MAGIC
# MAGIC - confira tipo, unidade e schema retornados;
# MAGIC - diferencie resultado executado de exemplo ilustrativo;
# MAGIC - interprete thresholds como política analítica, não padrão universal;
# MAGIC - registre versão, parâmetros e população quando houver decisão de modelo.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <a id="️-onde-o-código-executa-e-quanto-pode-custar"></a>
# MAGIC
# MAGIC ## ⚙️ Onde o Código Executa e Quanto Pode Custar
# MAGIC
# MAGIC | Família | Execução predominante | Atenção principal |
# MAGIC |---|---|---|
# MAGIC | pandas / NumPy / scikit-learn | driver | memória local e conversões de Spark |
# MAGIC | PySpark | cluster, com resultados agregados no driver quando necessário | scans, shuffles, `collect()` agregado e cardinalidade |
# MAGIC | Plotly / HTML | driver e navegador | tamanho da figura e estado visual da sessão |
# MAGIC | MLflow | serviço + armazenamento configurado | criação de runs e artefatos persistentes |
# MAGIC | bibliotecas opcionais | depende do compute | versão, compatibilidade e política de instalação |
# MAGIC
# MAGIC Não existe um helper universalmente “rápido”. Volume, largura, particionamento, cardinalidade e plano físico precisam ser considerados no contexto da chamada.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC <a id="-perguntas-frequentes-faq"></a>
# MAGIC
# MAGIC ## ❓ Perguntas Frequentes (FAQ)
# MAGIC
# MAGIC ### 1. Os snippets alteram o meu DataFrame original (*in-place*)?
# MAGIC
# MAGIC **A maior parte retorna um novo objeto, mas “zero efeito colateral” não é uma regra universal.** Helpers visuais podem modificar tema de sessão, wrappers do MLflow criam runs e treinadores retornam objetos com estado. Leia a docstring e o exemplo do objeto antes de usá-lo.
# MAGIC
# MAGIC ### 2. Posso usar os snippets em compute Databricks Serverless?
# MAGIC
# MAGIC **Depende do snippet, das bibliotecas disponíveis e do runtime.** Os módulos Python puros tendem a ser portáveis; PySpark, MLflow, LightGBM, SHAP, Plotly e outras dependências devem ser confirmados no destino. Serverless não torna `.assistant` automaticamente importável.
# MAGIC
# MAGIC ### 3. O que acontece se faltar uma biblioteca opcional, como LightGBM ou Tabulate?
# MAGIC
# MAGIC O comportamento depende do módulo: alguns produzem `ImportError` orientado e outros falham no import da dependência. Consulte o catálogo, confirme o pacote exigido e instale-o somente pelo mecanismo permitido no ambiente.
# MAGIC
# MAGIC ### 4. Como os snippets Spark lidam com tabelas muito grandes?
# MAGIC
# MAGIC Eles priorizam operações distribuídas, mas algumas rotinas executam ações e coletam **resultados agregados**, categorias limitadas ou amostras no driver. Isso é diferente de coletar a tabela inteira, mas ainda exige controle de cardinalidade e inspeção do plano.
# MAGIC
# MAGIC ### 5. A Genie Code encontra e executa os snippets automaticamente?
# MAGIC
# MAGIC **Não.** Uma skill pode recomendar explicitamente um helper, mas o notebook ainda precisa configurar a importação e executar o código. `hub_snippets` é uma extensão customizada, não um mecanismo nativo de descoberta da Genie Code.
# MAGIC
# MAGIC ### 6. Posso propor um novo snippet para a biblioteca?
# MAGIC
# MAGIC **Sim.** Use o molde em `.assistant/hub_padroes/` e a skill `@hub-ml-criar-objeto`. Todo novo objeto deve declarar contrato, dependências, efeitos, limites, API pública, exemplo sintético e testes proporcionais ao risco.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔗 Continue Explorando
# MAGIC
# MAGIC - Catálogo completo de helpers: `.assistant/CATALOGO_HELPERS.md`
# MAGIC - <a href="$../README_scripts.md">Hub Scripts</a>
# MAGIC - <a href="$../README_skills.md">Agent Skills</a>
# MAGIC - <a href="$../README_prompts.md">Hub Prompts</a>
# MAGIC - [Dependências em compute serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies)
# MAGIC - [Arquivos no workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace)
