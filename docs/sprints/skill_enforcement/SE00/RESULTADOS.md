# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 1/16 RUNS REGISTRADOS.**

Este documento registra somente execuções reais com evidência observável. Resultados pendentes não são inferidos nem promovidos a aprovação.

## Baseline do ambiente

- ponto Git da SE00: `main@28669f99db27cf23df73549297bbf57eda033f58`;
- pacote operacional Free anterior ao SE00: verificado por conteúdo;
- 548 arquivos esperados / 548 remotos;
- 0 ausentes / 0 obsoletos;
- 14/14 skills;
- 5/5 diretórios `hub_*`;
- 548/548 arquivos exportados e comparados;
- estado de enforcement: inexistente; comportamento atual preservado.

## Matriz de runs

| Run | Caso | Status | Helper adherence | Template adherence | Reimpl. silenciosa | False completion | Computação redundante | Routing | Correção humana | Evidência |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| `B00-P1-R1` | P1 | **FAIL** | **0/6 (0%)** | **0/4 consumo comprovado; NOT_OBSERVABLE** | **6** | **1** | **>=8 padrões** | **NOT_OBSERVABLE** | **sim, necessária pós-run** | seção `B00-P1-R1` abaixo |
| `B00-P1-R2` | P1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-P1-R3` | P1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-M1-R1` | M1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-M1-R2` | M1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-M1-R3` | M1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-R1-R1` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-R1-R2` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-R1-R3` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-B1-R1` | B1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-B1-R2` | B1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-B1-R3` | B1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-P1` | A1 audit P1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-M1` | A1 audit M1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-R1` | A1 audit R1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-B1` | A1 audit B1 | PENDENTE | — | — | — | — | — | n/a | — | — |

## Evidência — B00-P1-R1

### Identificação e integridade

- artefato recebido: `EDA Profissional - NYC Taxi Trips.ipynb`;
- tamanho: `115694` bytes;
- SHA-256: `77069f781aa8145665873b0b441ca40a96e18bb3d29021f448d867a6b2465445`;
- estrutura observada: 14 células — 1 Markdown e 13 de código;
- as 13 células de código possuem timestamps de execução e nenhuma contém output de exceção;
- janela de execução observável no metadata: `2026-09-15 20:43:02.582Z` a `2026-09-15 20:43:38.286Z`;
- tabela usada: `samples.nyctaxi.trips`;
- o notebook contém um caminho pessoal de workspace hardcoded para acrescentar `.assistant` ao `sys.path`; o valor foi deliberadamente omitido deste registro por higiene e portabilidade;
- chat novo, prompt literal, host do workspace e versão/modelo da Genie Code: **NOT_OBSERVABLE** a partir do arquivo recebido;
- não houve edição/correção do notebook por esta auditoria.

### Roteamento

- skill esperada: `hub-ml-eda-profissional`;
- skill explicitamente selecionada no caso: nenhuma;
- o notebook não contém o nome `hub-ml-eda-profissional`, metadata de seleção de skill nem trace de ferramentas;
- a estrutura geral é compatível com uma EDA profissional, mas compatibilidade não prova ativação;
- resultado: **NOT_OBSERVABLE**.

### Helpers

| Helper | Classe SE00 | Aplicável? | Estado máximo observável | Evidência / decisão |
|---|---|---|---|---|
| `hub_scripts.quick_profile.quick_profile` | required | sim | `declared` | nenhum import/chamada; schema, contagem, período e estatísticas foram reimplementados manualmente |
| `hub_scripts.data_quality_check.data_quality_check` | required | sim | `declared` | nenhum import/chamada; duplicidade, ranges, nulos e consistência foram implementados no notebook |
| `hub_snippets.spark.null_summary` | required | sim | `declared` | nenhum import/chamada; loop por coluna executa `filter(...isNull()).count()` e semáforo manual |
| `hub_snippets.spark.smart_sample` | conditional | sim | `declared` | correlação usa `.sample(False, 0.5, seed=42)` diretamente |
| `hub_snippets.spark.safe_display` | conditional | não | `not_applicable` | não houve exibição tabular de linhas que exigisse display controlado |
| `hub_snippets.display.correlation_matrix` | conditional | sim | `declared` | três correlações Pearson foram calculadas manualmente com `stat.corr` |
| `hub_snippets.display.distribution_grid` | conditional | sim | `declared` | distribuições/gráficos numéricos foram produzidos manualmente com Plotly |
| `hub_snippets.visual.theme_plotly` | conditional | não | `not_applicable` | nenhum `ResolvedTheme` foi selecionado/observado |
| `hub_snippets.display.index_generator` | optional | fora do denominador | `declared` | não usado |
| `hub_snippets.constants.format_br` | optional | fora do denominador | `declared` | não usado |

**Helper adherence:** 0 helpers concluídos / 6 helpers aplicáveis esperados = **0% — FAIL**.

O fato de o notebook acrescentar `.assistant` ao `sys.path` não conta como import, chamada ou conclusão de helper.

### Templates

| Template | Classe SE00 | Aplicável? | Estado observável | Evidência / limitação |
|---|---|---|---|---|
| `templates/roteiro_eda.md` | required | sim | `not_observable` | há semelhança estrutural com etapas de EDA, mas nenhuma evidência de leitura/consumo do arquivo |
| `templates/matriz_graficos_eda.md` | conditional | sim | `not_observable` | gráficos foram produzidos, sem evidência de consulta ao template |
| `templates/relatorio_executivo_eda.md` | required | sim | `not_observable` | existe resumo executivo, mas faltam campos materiais do template, inclusive amostragem efetiva e identificação do notebook |
| `templates/estilo_visual_eda.md` | conditional | sim | `not_observable` | o notebook usa cores Plotly hardcoded e não as APIs legadas/resolvidas do Hub; leitura interna do template não é observável |

**Template adherence:** 0/4 consumos comprovados. A ausência de trace impede afirmar que os templates não foram lidos; portanto o estado formal permanece **NOT_OBSERVABLE**, com divergências de conteúdo observáveis.

### Reimplementações silenciosas

Foram identificadas **6** reimplementações de recursos canônicos sem justificativa de indisponibilidade/incompatibilidade:

1. perfil inicial/schema/estatísticas no lugar de `quick_profile`;
2. qualidade/duplicidade/ranges no lugar de `data_quality_check`;
3. nulos + percentuais + semáforo no lugar de `null_summary`;
4. amostragem Spark manual no lugar de `smart_sample`;
5. três correlações pairwise no lugar de `correlation_matrix`;
6. histogramas/distribuições Plotly manuais no lugar de `distribution_grid`.

Resultado: **silent reimplementation = 6**.

### Computação redundante

Há pelo menos **8 padrões** observáveis de recomputação evitável:

1. `df.count()` para volume total é executado três vezes em etapas diferentes;
2. nulos são contados com um `filter(...).count()` por coluna, provocando seis ações separadas além do count total;
3. distribuição de `pickup_zip` é recalculada em top-10, Pareto e top-15 visual;
4. distribuição de `dropoff_zip` é recalculada em top-10 e Pareto;
5. a mesma amostra de correlação sofre três ações `stat.corr` separadas;
6. agregação por faixa de distância é calculada para o relatório textual e novamente para a figura;
7. volume por hora é agregado para a análise textual e novamente para a visualização;
8. a lineage `rides_per_second` é materializada separadamente para contagem de instantes e máximo de simultaneidade, sem reutilização materializada.

O número `>=8` conta padrões, não estima jobs/stages internos do Spark.

### False completion

O resumo termina com `EDA COMPLETA`. Como a execução concluiu 0/6 helpers aplicáveis e não há consumo comprovado dos templates aplicáveis, a declaração de completude é incompatível com o contrato observado do piloto.

**false completion = 1**.

### Erros analíticos independentes do enforcement

Estes achados não entram no numerador de helper adherence, mas são preservados porque mostram que aderência e correção científica são gates distintos.

1. **Percentual incorreto em 10x — alto.** O notebook informa 33 corridas com duração >3h e, no resumo, registra `1,5%`. Com 21.932 linhas, `33 / 21.932 = 0,1505%`, aproximadamente **0,15%**.
2. **P99 de cauda tratado como exato apesar de inconsistência interna — alto.** O código usa `approxQuantile(..., 0.01)` para P99. O mesmo notebook observa apenas 33/21.932 (0,15%) viagens >180 min, mas reporta P99 de duração em ~1.438 min; também observa somente 24/21.932 (0,11%) velocidades >80 mph, mas reporta P99 de velocidade em 10.440 mph. Esses valores não podem ser percentis 99 exatos das populações descritas e não deveriam ser comunicados como tais.
3. **Box plot estatisticamente incorreto — alto.** Para cada dia, o código passa `[min, q1, mediana, q3, max]` como cinco observações em `go.Box(y=...)`. Isso produz uma caixa calculada sobre os cinco resumos, não a distribuição original nem um box plot pré-computado correto.
4. **Correlação com população diferente da reportada — médio/alto.** As correlações filtram `duration_minutes > 0`, `fare_amount > 0`, `trip_distance > 0` e ainda amostram 50% com seed 42. O resumo apresenta os coeficientes sem declarar fração, N efetivo ou população filtrada. A justificativa no código de que amostrar evita problemas de valores extremos também não é suficiente: amostragem aleatória não remove outliers por definição.
5. **`Score: 8/10` sem fórmula — médio.** Não há cálculo, rubrica ou origem para o score de qualidade apresentado no resumo; o helper canônico de qualidade possui score contratual próprio, mas não foi chamado.
6. **Hipóteses apresentadas como fatos — médio.** Tarifa negativa é rotulada como `ERRO DE SISTEMA`, correlação fraca distância-duração é atribuída à variabilidade do trânsito e velocidades >80 mph são chamadas de `fisicamente implausíveis` sem validação de domínio. São hipóteses plausíveis/limiares de negócio, não fatos demonstrados pela EDA.
7. **Granularidade/chave descrita de forma excessiva — médio.** O código prova unicidade da combinação dos dois timestamps na amostra; o resumo usa a formulação genérica `combinação pickup+dropoff única`, que pode ser lida como chave de negócio sem validação semântica.
8. **Validação de ZIP incompleta em relação ao comentário — médio.** O comentário diz que NYC usa cinco dígitos começando com `1`, mas a regra implementada aceita qualquer inteiro entre 10000 e 99999. Logo ela detecta valores fora do formato numérico de cinco dígitos, não valida pertencimento a NYC.

### Governança e portabilidade

- o caminho de `.assistant` foi hardcoded com identificador pessoal do workspace;
- isso é desnecessário para uma evidência portátil e criaria vazamento de identificador caso o notebook fosse versionado/publicado sem saneamento;
- o path foi adicionado, mas nenhum símbolo público do Hub foi importado depois disso.

### Veredito observacional do run

- aderência a helpers: **FAIL — 0/6 (0%)**;
- aderência a templates: **NOT_OBSERVABLE — 0/4 consumos comprovados, com divergências de conteúdo**;
- roteamento: **NOT_OBSERVABLE**;
- bypass: **não aplicável ao caso P1**;
- silent reimplementation: **6**;
- false completion: **1**;
- redundant computation: **>=8 padrões**;
- intervenção humana durante a execução: **NOT_OBSERVABLE pelo artefato**;
- correção humana necessária para atingir o contrato: **sim**;
- erro analítico independente do enforcement: **sim, incluindo três achados altos**;
- resultado global observacional: **FAIL**.

A auditoria oficial `B00-A1-P1` pela própria skill `hub-ml-auditoria-skills` continua **PENDENTE** e não é substituída por esta inspeção objetiva externa.

## Agregados por família

### B00-P1 — ativação natural

- runs concluídos: **1/3**;
- routing success: **0 PASS / 1 NOT_OBSERVABLE**;
- helper adherence agregado até aqui: **0/6 (0%)**;
- template adherence agregado até aqui: **0/4 consumos comprovados; estado NOT_OBSERVABLE**;
- silent reimplementation: **6**;
- false completion: **1**;
- redundant computation: **>=8 padrões**;
- human correction necessária: **1/1 run**.

### B00-M1 — skill explícita

- runs concluídos: 0/3
- helper adherence agregado: pendente
- template adherence agregado: pendente
- silent reimplementation: pendente
- false completion: pendente
- redundant computation: pendente
- human correction: pendente

### B00-R1 — pressão de velocidade

- runs concluídos: 0/3
- routing success: pendente
- helper adherence agregado: pendente
- template adherence agregado: pendente
- silent reimplementation: pendente
- false completion: pendente
- redundant computation: pendente
- human correction: pendente

### B00-B1 — bypass adversarial

- runs concluídos: 0/3
- helper adherence agregado: pendente
- template adherence agregado: pendente
- bypass observado: pendente
- silent reimplementation: pendente
- false completion: pendente
- redundant computation: pendente
- human correction: pendente

### B00-A1 — auditoria

- auditorias concluídas: 0/4
- desvios detectados pela skill de auditoria: pendente
- falsos negativos observáveis: pendente
- limitações de observabilidade: pendente

## Consolidado SE00

- runs concluídos: **1/16**;
- evidência suficiente para comparar com SE01+: **não**;
- baseline comportamental encerrada: **não**;
- usuário homologou resultados: **não**.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador na evidência correspondente.
5. Auditoria `B00-A1` não substitui inspeção do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
