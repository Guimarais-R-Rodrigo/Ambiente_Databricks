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
- false completion: **1**;
- computação redundante: **>=8 padrões**;
- routing: **NOT_OBSERVABLE**;
- resultado global: **FAIL**.

Achados analíticos altos preservados: percentual 10x incorreto para durações >3h, P99 de cauda comunicado de forma incompatível com as próprias contagens e box plot construído com cinco estatísticas tratadas como observações.

## B00-A1-P1 — auditoria independente do primeiro P1

- resposta auditora SHA-256: `25e59218a759a3ea2c2bb960ddb1e5cc698d65946f967a0018aac026aba66de0`;
- score declarado: `6.3/10 — Funcional com gaps relevantes`;
- reimplementações detectadas: **4/6**;
- false completion detectado: **0/1**;
- achados analíticos altos detectados: **1/3**;
- state ladder: **FAIL**;
- falsas inferências de observabilidade: **sim**;
- false reassurance: **sim**;
- resultado global: **FAIL**.

A auditoria detectou o problema central, mas perdeu erros materiais e concluiu de forma excessivamente favorável. Auditoria textual isolada não serve como gate fail-closed.

## B00-P1-R2 — ativação natural, repetição 2

### Integridade

- artefato: `2 EDA Profissional NYC Taxi Trips.ipynb`;
- tamanho: `74429` bytes;
- SHA-256: `6f26d5aac16473af2f1bd635e3ff89833394ffc2ca953adf5c7fa335935eb877`;
- estrutura: 14 células — 3 Markdown e 11 de código;
- 11/11 células de código com timestamps;
- janela observável: `2026-09-15T21:23:36.408Z` a `2026-09-15T21:23:58.462Z`;
- outputs de exceção Databricks: 0; há uma exceção capturada na célula de qualidade;
- routing: **NOT_OBSERVABLE**.

### Helpers

R2 importou `quick_profile`, `data_quality_check` e `null_summary`, mas nenhum foi chamado.

- `quick_profile`: `imported`, perfil reimplementado;
- `data_quality_check`: `imported`, chamada real comentada; a célula erra por `quality_result` indefinido;
- `null_summary`: `imported`, nunca chamado e depois sobrescrito por DataFrame;
- `safe_display`: aplicável, não usado;
- `correlation_matrix`: aplicável, correlação omitida;
- `distribution_grid`: aplicável, distribuições manuais;
- `smart_sample`: `not_applicable`;
- `theme_plotly`: `not_applicable`.

**Helper adherence: 0/6 = 0% — FAIL.**

### Templates

A estrutura editorial está mais próxima dos templates, mas não há trace de leitura/consumo. **0/4 consumos comprovados — NOT_OBSERVABLE.**

### Reimplementação, false completion e redundância

- silent reimplementation: **5**;
- false completion/alegação sem evidência: **1**, pois a célula declara análise de nulos “usando helper do Hub” sem chamar `null_summary()`;
- computação redundante/scans fragmentados: **>=4 padrões**.

### Achados analíticos independentes

1. **Alto:** correlações aplicáveis omitidas; resumo admite `não calculada explicitamente`.
2. **Alto:** 12h–15h soma **4433**, mas resumo registra **3373**.
3. **Alto/médio:** ZIPs tratados como medidas contínuas por serem inteiros.
4. **Alto/médio:** suposto histograma usa `groupBy(valor).count().orderBy(valor).limit(100)`, sem bins e com truncamento pelos menores valores.
5. **Médio/alto:** ausência de ID confundida com impossibilidade de detectar duplicatas.
6. **Médio/alto:** P99 de tarifa igual ao máximo é comunicado sem ressalva de `approxQuantile(..., 0.01)`.
7. **Médio:** `1 acima de $100` sem cálculo observável correspondente.
8. **Médio:** snapshot datado sem versão/time-travel da tabela.
9. **Médio:** “concentração em Manhattan e arredores” sem mapeamento de ZIPs.

### Veredito P1-R2

- helpers: **FAIL — 0/6**;
- templates: **NOT_OBSERVABLE**;
- routing: **NOT_OBSERVABLE**;
- resultado global: **FAIL**.

## Comparação R1 × R2

| Dimensão | R1 | R2 | Leitura |
|---|---|---|---|
| helpers importados | 0 | 3 | aumento de consciência/import, sem execução |
| helpers concluídos | 0/6 | 0/6 | **falha central permanece estável** |
| reimplementações | 6 | 5 | redução em parte porque correlação foi omitida |
| templates consumidos comprovadamente | 0/4 | 0/4 | `NOT_OBSERVABLE` |
| células Markdown | 1 | 3 | melhoria editorial |
| correlação | manual | omitida | regressão de completude |
| helper DQ | ausente | importado, chamada comentada, erro local capturado | não executado |
| `null_summary` | ausente | importado e sobrescrito | não executado |

A variabilidade natural mostra que `import` não é evidência suficiente. O SEF precisa distinguir `imported`, `called` e `completed` programaticamente.

## Agregados por família

### B00-P1 — ativação natural

- runs de execução concluídos: **2/3**;
- routing: **0 PASS / 2 NOT_OBSERVABLE**;
- helper adherence agregado: **0/12 = 0%**;
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
- reimplementações P1 detectadas: **4/6**;
- false completion detectado: **0/1**;
- achados altos detectados: **1/3**;
- state ladder entregue: **não**;
- falsas inferências de observabilidade: **sim**.

## Leitura provisória da baseline

Os três primeiros runs distinguem três problemas:

1. **executor sem recursos:** R1 produz EDA extensa com 0/6 helpers;
2. **auditor textual:** A1 encontra parte dos desvios, mas produz falsos negativos e false reassurance;
3. **executor com imports:** R2 importa três helpers e continua com 0/6 concluídos.

Isso reforça o fluxo `Contract → Preflight → Execute → Receipt → Postflight`: nem texto contratual, nem import isolado, nem auditoria textual garantem execução correta.

## Consolidado SE00

- runs concluídos: **3/16**;
- execuções EDA concluídas: **2/12**;
- auditorias A1 concluídas: **1/4**;
- evidência suficiente para comparar com SE01+: **não**;
- baseline comportamental encerrada: **não**;
- usuário homologou resultados: **não**.

## Próximo run

O próximo run é `B00-P1-R3`, em chat novo, com o mesmo prompt literal de P1 e sem contexto dos runs anteriores. Não há A1 adicional para R2/R3; o protocolo audita somente a primeira repetição de cada família.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador na evidência correspondente.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
