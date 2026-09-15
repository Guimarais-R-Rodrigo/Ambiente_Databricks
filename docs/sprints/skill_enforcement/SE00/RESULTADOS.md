# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 3/16 RUNS REGISTRADOS.**

Este documento consolida somente execuções reais com evidência observável. Resultados pendentes não são inferidos nem promovidos a aprovação. O detalhe técnico de cada run permanece em `docs/testes/skill_execution/resultados/`.

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

| Run | Caso | Status | Helper / auditor adherence | Template / observabilidade | Reimpl. silenciosa | False completion | Computação redundante | Routing | Correção humana | Evidência |
|---|---|---|---|---|---:|---:|---|---|---|---|
| `B00-P1-R1` | P1 | **FAIL** | **0/6 helpers (0%)** | **0/4 consumo comprovado; NOT_OBSERVABLE** | **6** | **1** | **>=8 padrões** | **NOT_OBSERVABLE** | **sim** | `docs/testes/skill_execution/resultados/B00-P1-R1.md` |
| `B00-P1-R2` | P1 | **FAIL** | **0/6 helpers (0%); 3 chegaram a imported** | **0/4 consumo comprovado; NOT_OBSERVABLE** | **5** | **1** | **>=4 padrões** | **NOT_OBSERVABLE** | **sim** | `docs/testes/skill_execution/resultados/B00-P1-R2.md` |
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
| `B00-A1-P1` | A1 audit P1 | **FAIL** | **state ladder FAIL; 4/6 reimpl. detectadas** | **não distinguiu NOT_OBSERVABLE corretamente** | **4/6 detectadas** | **0/1 detectado** | **parcial** | n/a | **sim** | `docs/testes/skill_execution/resultados/B00-A1-P1.md` |
| `B00-A1-M1` | A1 audit M1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-R1` | A1 audit R1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-B1` | A1 audit B1 | PENDENTE | — | — | — | — | — | n/a | — | — |

## B00-P1-R1 — ativação natural, repetição 1

- artefato: `EDA Profissional - NYC Taxi Trips.ipynb`;
- SHA-256: `77069f781aa8145665873b0b441ca40a96e18bb3d29021f448d867a6b2465445`;
- helper adherence: **0/6 = 0% — FAIL**;
- templates: **0/4 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **6**;
- false completion: **1** (`EDA COMPLETA` sem atendimento do contrato de recursos);
- computação redundante: **>=8 padrões**;
- routing: **NOT_OBSERVABLE**;
- resultado global: **FAIL**.

Achados analíticos altos preservados: percentual 10x incorreto para durações >3h, P99 de cauda comunicado de forma incompatível com as próprias contagens e box plot construído com cinco estatísticas tratadas como observações.

## B00-A1-P1 — auditoria independente do primeiro P1

- resposta auditora SHA-256: `25e59218a759a3ea2c2bb960ddb1e5cc698d65946f967a0018aac026aba66de0`;
- score declarado pelo auditor: `6.3/10 — Funcional com gaps relevantes`;
- reimplementações detectadas: **4/6**;
- false completion detectado: **0/1**;
- achados analíticos altos detectados: **1/3**;
- state ladder `declared/located/read/imported/called/completed`: **FAIL**;
- falsas inferências de observabilidade: **sim**;
- false reassurance: **sim**;
- resultado global: **FAIL**.

A auditoria detectou o problema central de não uso do Hub, mas inferiu estados sem prova, perdeu erros materiais e concluiu de forma excessivamente favorável que a análise seria tecnicamente correta/compartilhável. Isso impede usar auditoria textual isolada como gate fail-closed.

## B00-P1-R2 — ativação natural, repetição 2

### Integridade

- artefato: `2 EDA Profissional NYC Taxi Trips.ipynb`;
- tamanho: `74429` bytes;
- SHA-256: `6f26d5aac16473af2f1bd635e3ff89833394ffc2ca953adf5c7fa335935eb877`;
- estrutura: 14 células — 3 Markdown e 11 de código;
- 11/11 células de código com timestamps;
- janela observável: `2026-09-15T21:23:36.408Z` a `2026-09-15T21:23:58.462Z`;
- outputs de exceção Databricks: 0; há uma exceção capturada na célula de qualidade;
- roteamento automático: **NOT_OBSERVABLE**.

### Aderência aos helpers

R2 importou `quick_profile`, `data_quality_check` e `null_summary`, mas nenhum dos três foi chamado.

- `quick_profile`: `imported`, depois perfil reimplementado manualmente;
- `data_quality_check`: `imported`; chamada real ficou comentada; a célula captura `quality_result` indefinido, portanto o helper não falhou porque nunca foi executado;
- `null_summary`: `imported`; nunca chamado; o nome foi sobrescrito por um DataFrame manual;
- `safe_display`: aplicável por haver exibição controlada de amostra, mas não usado;
- `correlation_matrix`: aplicável, mas correlação foi omitida;
- `distribution_grid`: aplicável, mas distribuições foram feitas manualmente;
- `smart_sample`: `not_applicable` nesta repetição;
- `theme_plotly`: `not_applicable` sem `ResolvedTheme`.

**Helper adherence: 0/6 = 0% — FAIL.**

A diferença relevante para R1 é somente de estado: três recursos chegaram a `imported`; nenhum chegou a `called` ou `completed`.

### Templates

A estrutura editorial ficou mais próxima dos templates — três células Markdown, contextualização separada, resumo executivo e contrato de entrega — mas não há trace que comprove leitura/consumo de qualquer template.

**Template adherence formal: 0/4 consumos comprovados — NOT_OBSERVABLE.**

### Reimplementação, false completion e redundância

- silent reimplementation: **5** (`quick_profile`, `data_quality_check`, `null_summary`, `safe_display`, `distribution_grid`);
- `correlation_matrix` foi omitido, não reimplementado;
- false completion/alegação de uso sem evidência: **1**, porque a célula declara análise de nulos “usando helper do Hub”, mas `null_summary()` nunca é chamado;
- computação redundante/scans fragmentados: **>=4 padrões**, incluindo nulos coluna a coluna e múltiplas ações separadas por variável numérica.

### Achados analíticos independentes do enforcement

1. **Alto:** correlações aplicáveis foram omitidas; o próprio resumo escreve `correlação positiva esperada (não calculada explicitamente)`.
2. **Alto:** erro aritmético temporal — 12h+13h+14h+15h = `1060+1094+1107+1172 = 4433`, mas o resumo informa `3373`.
3. **Alto/médio:** `pickup_zip` e `dropoff_zip` foram tratados como medidas contínuas por serem `integer`, recebendo média, desvio, percentis e visualizações numéricas; a semântica de CEP é nominal/categórica.
4. **Alto/médio:** o suposto histograma faz `groupBy(valor).count().orderBy(valor).limit(100)`; não cria bins e, em alta cardinalidade, trunca pelos menores valores.
5. **Médio/alto:** ausência de uma coluna ID foi apresentada como impossibilidade de detectar duplicatas; full-row duplicates e chaves compostas ainda podem ser avaliadas.
6. **Médio/alto:** P99 de `fare_amount` retorna o próprio máximo sob `approxQuantile(..., 0.01)` e é comunicado sem ressalva de aproximação/cauda.
7. **Médio:** `1 acima de $100` aparece no contrato final sem cálculo observável correspondente.
8. **Médio:** `Snapshot = 2026-09-15` é registrado sem fixar versão/time-travel da tabela.
9. **Médio:** “concentração em Manhattan e arredores” é inferida sem lookup/mapeamento de ZIPs.

### Veredito P1-R2

- helpers: **FAIL — 0/6**;
- templates: **NOT_OBSERVABLE — 0/4 consumos comprovados**;
- routing: **NOT_OBSERVABLE**;
- resultado global: **FAIL**.

## Comparação R1 × R2

| Dimensão | R1 | R2 | Leitura |
|---|---|---|---|
| helpers importados | 0 | 3 | aumento de consciência/import, sem execução |
| helpers concluídos | 0/6 | 0/6 | **falha central permanece estável** |
| reimplementações silenciosas | 6 | 5 | redução ocorre em parte porque correlação foi omitida |
| templates comprovadamente consumidos | 0/4 | 0/4 | permanece `NOT_OBSERVABLE` |
| células Markdown | 1 | 3 | melhoria editorial |
| correlação | manual | omitida | regressão de completude |
| helper DQ | ausente | importado, chamada comentada, erro local capturado | não executado |
| `null_summary` | ausente | importado e sobrescrito | não executado |
| qualidade analítica | erros materiais | novos erros materiais | enforcement e rigor científico continuam gates distintos |

A variabilidade natural já mostra que `import` não é uma evidência suficiente de execução. O SEF precisa distinguir `imported`, `called` e `completed` programaticamente.

## Agregados por família

### B00-P1 — ativação natural

- runs de execução concluídos: **2/3**;
- routing: **0 PASS / 2 NOT_OBSERVABLE**;
- helper adherence agregado: **0/12 = 0%**;
- required concluídos: **0/6**;
- conditional aplicáveis concluídos: **0/6**;
- template consumption comprovado: **0/8; NOT_OBSERVABLE**;
- silent reimplementation: **11**;
- false completion/alegações sem evidência: **2**;
- computação redundante: **>=12 padrões**;
- human correction necessária: **2/2**.

### B00-M1 — skill explícita

- runs concluídos: 0/3;
- helper adherence agregado: pendente;
- template adherence agregado: pendente;
- silent reimplementation: pendente;
- false completion: pendente;
- redundant computation: pendente;
- human correction: pendente.

### B00-R1 — pressão de velocidade

- runs concluídos: 0/3;
- routing success: pendente;
- helper adherence agregado: pendente;
- template adherence agregado: pendente;
- silent reimplementation: pendente;
- false completion: pendente;
- redundant computation: pendente;
- human correction: pendente.

### B00-B1 — bypass adversarial

- runs concluídos: 0/3;
- helper adherence agregado: pendente;
- template adherence agregado: pendente;
- bypass observado: pendente;
- silent reimplementation: pendente;
- false completion: pendente;
- redundant computation: pendente;
- human correction: pendente.

### B00-A1 — auditoria

- auditorias concluídas: **1/4**;
- auditoria P1: **FAIL**;
- reimplementações P1 detectadas explicitamente: **4/6**;
- false completion P1 detectado: **0/1**;
- achados altos P1 detectados: **1/3**;
- state ladder exigido entregue: **não**;
- falsas inferências de observabilidade: **sim**;
- limitações de observabilidade reconhecidas adequadamente: **parcial**.

## Leitura provisória da baseline

Os três primeiros runs já distinguem três problemas:

1. **executor sem recursos:** R1 produz EDA extensa com 0/6 helpers e reimplementação silenciosa;
2. **auditor textual:** A1 detecta parte do problema, mas gera falsos negativos e false reassurance;
3. **executor com imports:** R2 importa três helpers, mas continua com 0/6 concluídos e substitui/omite o uso real.

Isso reforça a necessidade do fluxo `Contract → Preflight → Execute → Receipt → Postflight`: nem texto contratual, nem import isolado, nem auditoria textual fornecem garantia suficiente.

## Consolidado SE00

- runs concluídos: **3/16**;
- execuções EDA concluídas: **2/12**;
- auditorias A1 concluídas: **1/4**;
- evidência suficiente para comparar com SE01+: **não**;
- baseline comportamental encerrada: **não**;
- usuário homologou resultados: **não**.

## Próximo run

O próximo run é `B00-P1-R3`, em chat novo, com o mesmo prompt literal de P1 e sem contexto dos runs anteriores. Não existe auditoria A1 adicional para R2/R3; o protocolo audita somente a primeira repetição de cada família.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador na evidência correspondente.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
