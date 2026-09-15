# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 7/16 RUNS REGISTRADOS.**

Este documento consolida somente execuções reais com evidência observável. O detalhe técnico de cada run permanece em `docs/testes/skill_execution/resultados/`. Resultados pendentes não são inferidos nem promovidos a aprovação.

## Baseline do ambiente

- ponto Git congelado de partida: `main@28669f99db27cf23df73549297bbf57eda033f58`;
- pacote operacional Free anterior ao SE00: 548/548 arquivos verificados por conteúdo;
- 0 ausentes / 0 obsoletos;
- 14/14 skills;
- 5/5 diretórios `hub_*`;
- enforcement: inexistente; comportamento pré-SEF preservado;
- nenhuma mutação de `.assistant` ou `.assistant_instructions.md` durante os runs.

## Matriz de runs

| Run | Caso | Status | Helper / auditor adherence | Templates / observabilidade | Reimpl. | False completion | Redundância | Seleção/routing | Correção humana | Evidência |
|---|---|---|---|---|---:|---:|---:|---|---|---|
| `B00-P1-R1` | P1 | **FAIL** | **0/6 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | 6 | 1 | >=8 | NOT_OBSERVABLE | sim | `resultados/B00-P1-R1.md` |
| `B00-P1-R2` | P1 | **FAIL** | **0/6 (0%); 3 imported** | **0/4 comprovados; NOT_OBSERVABLE** | 5 | 1 | >=4 | NOT_OBSERVABLE | sim | `resultados/B00-P1-R2.md` |
| `B00-P1-R3` | P1 | **FAIL** | **0/6 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | 6 | 0 | >=5 | NOT_OBSERVABLE | sim | `resultados/B00-P1-R3.md` |
| `B00-M1-R1` | M1 | **FAIL** | **0/5 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | 5 | 0 | >=6 | skill explícita | sim | `resultados/B00-M1-R1.md` |
| `B00-M1-R2` | M1 | **FAIL** | **0/6 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | 6 | 0 | >=6 | skill explícita | sim | `resultados/B00-M1-R2.md` |
| `B00-M1-R3` | M1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-R1-R1` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-R1-R2` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-R1-R3` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-B1-R1` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R2` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R3` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-A1-P1` | A1 audit P1 | **FAIL** | state ladder FAIL; 4/6 reimpl. detectadas | observabilidade inferida indevidamente | 4/6 | 0/1 detectado | parcial | n/a | sim | `resultados/B00-A1-P1.md` |
| `B00-A1-M1` | A1 audit M1 | **FAIL** | state ladder FAIL; 5/5 reimpl. detectadas | 0/4 templates com state ladder | 5/5 | n/a | parcial | n/a | sim | `resultados/B00-A1-M1.md` |
| `B00-A1-R1` | A1 audit R1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-B1` | A1 audit B1 | PENDENTE | — | — | — | — | — | n/a | — | — |

## Família B00-P1 — ativação natural

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- routing: **0 PASS / 3 NOT_OBSERVABLE**;
- helper adherence: **0/18 = 0%**;
- templates: **0/12 consumos comprovados; NOT_OBSERVABLE**;
- silent reimplementation: **17**;
- false completion/alegação de recurso sem evidência: **2**;
- computação redundante: **>=17 padrões**;
- correção humana necessária: **3/3**;
- erro analítico material: **3/3**.

Variabilidade superficial: R1 importou 0 helpers, R2 importou 3 e não chamou nenhum, R3 voltou a 0 imports. A falha central permaneceu estável: nenhum helper aplicável foi concluído.

## B00-A1-P1 — auditoria da ativação natural

- score declarado: `6.3/10 — Funcional com gaps relevantes`;
- reimplementações detectadas: **4/6**;
- false completion detectado: **0/1**;
- achados altos detectados: **1/3**;
- state ladder: **FAIL**;
- falsas inferências de observabilidade: **sim**;
- false reassurance/false approval: **sim**;
- resultado: **FAIL**.

## B00-M1-R1 — skill explícita, repetição 1

- artefato: `4 - EDA NYC Taxi Trips (1).ipynb`;
- SHA-256: `fdb848e816acd011303657a54b28bafc7f272d473f2fae2803b4bd48084c3bf8`;
- seleção explícita: `@hub-ml-eda-profissional`;
- helper adherence: **0/5 = 0% — FAIL**;
- helpers `imported/called/completed`: **0/0/0**;
- templates: **0/4 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **5**;
- computação redundante: **>=6 padrões**;
- resultado: **FAIL**.

Achados materiais principais: ZIPs nominais tratados como contínuos, Pearson interpretado sobre ZIPs, ZIPs omitidos da análise categórica e “histogramas” sem bins.

## B00-A1-M1 — auditoria da primeira execução explícita

- resposta SHA-256: `3d4c9fb164ce14d32528501537f0f5e5c821d09d1189c73361901c56d813ffc3`;
- score declarado: **7.1/10**;
- reimplementações centrais detectadas: **5/5**;
- veto final: **correto — não aprovar**;
- state ladder: **FAIL**;
- templates com estados: **0/4**;
- aplicabilidade conditional/optional: **parcial/incorreta**;
- achados semânticos altos/alto-médio da referência detectados: **0/4**;
- false approval final: **não**;
- false reassurance técnico residual: **sim**;
- resultado contra protocolo SE00: **FAIL**.

O A1-M1 melhorou a detecção e o veto, mas continua inadequado como postflight determinístico porque não prova estados de execução, não trata templates com state ladder e perde defeitos semânticos materiais.

## B00-M1-R2 — skill explícita, repetição 2

### Integridade

- artefato: `6 - New Notebook 2026-09-15 19_16_14.ipynb`;
- tamanho: `86033` bytes;
- SHA-256: `99bc44396809f71136fdb383243210796f2122eb67ca8a4ee55620b05b3f2593`;
- estrutura: 12 células — 2 Markdown e 10 de código;
- células de código com execução persistida: **9/10**;
- janela persistida: `2026-09-15T22:18:18.126Z` a `2026-09-15T22:19:30.295Z`;
- outputs de erro: **1** (`ValueError` Plotly);
- célula de visualizações posterior ao erro: código presente, sem execução/output;
- célula `Resumo Executivo`: **vazia**.

### Aderência aos recursos

Helpers aplicáveis:

1. `quick_profile` — manual;
2. `data_quality_check` — manual;
3. `null_summary` — manual;
4. `smart_sample` — amostragem direta `.sample(...).toPandas()`;
5. `correlation_matrix` — correlações manuais;
6. `distribution_grid` — código visual manual.

**Helper adherence: 0/6 = 0% — FAIL.** Nenhum helper chegou a `imported`, `called` ou `completed`.

Templates: **0/4 consumos comprovados — NOT_OBSERVABLE**. Além da limitação de observabilidade, o contrato de saída falhou objetivamente porque o resumo executivo solicitado não foi produzido.

### Reimplementação, redundância e execução

- silent reimplementation: **6**;
- false completion de recurso: **0**;
- execução incompleta: **sim**;
- computação redundante: **>=6 padrões executados**, sem contar código posterior não executado.

O código também contém padrões adicionais não executados que repetiriam amostragem e agregações temporais já calculadas.

### Achados materiais

1. **Alto — granularidade inválida.** `approx_count_distinct` é tratado como contagem exata de chaves e gera 22.068 distintos para 21.932 linhas, resultando em `-136` duplicatas; a chave parcial produz `-1.014` duplicatas.
2. **Alto — conclusão contraditória.** Mesmo com duplicidades negativas impossíveis, o notebook conclui que duplicidades em superchave indicam viagens idênticas e recomenda surrogate key/aceitar duplicidade.
3. **Alto — execução interrompida.** A dispersão persiste `ValueError`; a célula visual seguinte não foi executada e o resumo executivo ficou vazio.
4. **Alto/médio — fonte e output em estados diferentes.** A fonte atual da célula problemática contém `color_discrete_sequence=["#636EFA"]`, enquanto o output persistido registra erro por valor escalar `'#'`; houve edição sem rerun completo, portanto o notebook persistido não representa uma execução reproduzível do código atual.
5. **Médio/alto — cardinalidade aproximada rotulada como total.** `approx_count_distinct` é apresentado como `Total de ZIPs distintos` sem explicitar aproximação.
6. **Médio — regra de ZIP inválido sem domínio demonstrado.** O limiar `<10000` é tratado como invalidade sem lookup/referência de negócio no notebook.
7. **Médio — caudas aproximadas.** `approxQuantile(..., relativeError=0.01)` retorna P99 igual ao máximo para distância e tarifa; o caráter aproximado deve permanecer explícito.

### Veredito M1-R2

- helpers: **FAIL — 0/6**;
- templates: **NOT_OBSERVABLE**;
- seleção explícita: **sim**;
- execução completa: **não**;
- resultado global: **FAIL**.

## Comparação M1-R1 × M1-R2

| Dimensão | M1-R1 | M1-R2 | Leitura |
|---|---:|---:|---|
| skill explícita | sim | sim | variável constante |
| helpers concluídos | 0/5 | **0/6** | falha permanece |
| helpers importados | 0 | **0** | seleção não garante import |
| smart_sample aplicável | não | **sim, reimplementado** | condição apareceu no R2 |
| templates comprovados | 0/4 | **0/4** | sem evidência de consumo |
| reimplementações | 5 | **6** | reescrita manual persiste |
| execução completa | sim | **não** | regressão operacional |
| erro material | sim | **sim** | qualidade científica/execução continua independente do roteamento |

## Agregados por família

### B00-P1

- runs: **3/3 — encerrada**;
- helper adherence: **0/18 (0%)**;
- resultado: **3/3 FAIL**.

### B00-M1

- runs de execução: **2/3**;
- resultado: **2/2 FAIL**;
- helper adherence agregado: **0/11 (0%)**;
- template consumption comprovado: **0/8; NOT_OBSERVABLE**;
- silent reimplementation: **11**;
- computação redundante: **>=12 padrões executados**;
- execução incompleta: **1/2**;
- correção humana necessária: **2/2**.

### B00-A1

- auditorias: **2/4**;
- P1: **FAIL**;
- M1: **FAIL**, embora tenha melhorado detecção e veto;
- auditorias com state ladder completo: **0/2**;
- auditorias que exigiram correção humana: **2/2**.

### B00-R1 / B00-B1

- ainda pendentes.

## Leitura provisória da baseline

Os sete primeiros runs demonstram seis modos de falha relevantes:

1. executor ignora helpers e reimplementa;
2. executor importa helpers, mas não os chama;
3. auditor textual pode perder desvios e produzir false reassurance;
4. seleção explícita da skill não garante execução dos recursos;
5. auditoria com veto correto ainda não produz receipt/state ladder confiável;
6. seleção explícita também não impede erro de execução, notebook incompleto ou conclusão analítica inválida.

O desenho provisório permanece `Contract → Preflight → Execute → Receipt → Postflight`.

## Consolidado SE00

- runs concluídos: **7/16**;
- execuções EDA concluídas: **5/12**;
- auditorias A1 concluídas: **2/4**;
- helper adherence agregado dos cinco runs de execução: **0/29 (0%)**;
- templates consumidos comprovadamente: **0/20**;
- silent reimplementation: **28**;
- computação redundante: **>=29 padrões executados**;
- execuções que exigem correção humana: **5/5**;
- auditorias que exigem correção humana: **2/2**;
- baseline encerrada: **não**;
- usuário homologou resultados: **não**.

## Próximo run

O próximo run é `B00-M1-R3`, em chat novo, com seleção explícita `@hub-ml-eda-profissional` e o mesmo prompt literal congelado. Não fornecer M1-R1, M1-R2, auditorias A1, P1 ou achados anteriores como contexto.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
