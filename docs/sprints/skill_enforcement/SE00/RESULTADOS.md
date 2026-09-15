# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 5/16 RUNS REGISTRADOS.**

Este documento consolida somente execuções reais com evidência observável. Resultados pendentes não são inferidos nem promovidos a aprovação. O detalhe técnico de cada run permanece em `docs/testes/skill_execution/resultados/`.

## Baseline do ambiente

- ponto Git da SE00: `main@28669f99db27cf23df73549297bbf57eda033f58`;
- pacote operacional Free anterior ao SE00: 548/548 arquivos verificados por conteúdo;
- 0 ausentes / 0 obsoletos;
- 14/14 skills;
- 5/5 diretórios `hub_*`;
- enforcement: inexistente; comportamento pré-SEF preservado.

## Matriz de runs

| Run | Caso | Status | Helper / auditor adherence | Template / observabilidade | Reimpl. silenciosa | False completion | Computação redundante | Routing/seleção | Correção humana | Evidência |
|---|---|---|---|---|---:|---:|---|---|---|---|
| `B00-P1-R1` | P1 | **FAIL** | **0/6 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | **6** | **1** | **>=8** | **NOT_OBSERVABLE** | **sim** | `docs/testes/skill_execution/resultados/B00-P1-R1.md` |
| `B00-P1-R2` | P1 | **FAIL** | **0/6 (0%); 3 imported** | **0/4 comprovados; NOT_OBSERVABLE** | **5** | **1** | **>=4** | **NOT_OBSERVABLE** | **sim** | `docs/testes/skill_execution/resultados/B00-P1-R2.md` |
| `B00-P1-R3` | P1 | **FAIL** | **0/6 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | **6** | **0** | **>=5** | **NOT_OBSERVABLE** | **sim** | `docs/testes/skill_execution/resultados/B00-P1-R3.md` |
| `B00-M1-R1` | M1 | **FAIL** | **0/5 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | **5** | **0** | **>=6** | **skill explícita** | **sim** | `docs/testes/skill_execution/resultados/B00-M1-R1.md` |
| `B00-M1-R2` | M1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-M1-R3` | M1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-R1-R1` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-R1-R2` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-R1-R3` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-B1-R1` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R2` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R3` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-A1-P1` | A1 audit P1 | **FAIL** | **state ladder FAIL; 4/6 reimpl. detectadas** | **observabilidade inferida indevidamente** | **4/6 detectadas** | **0/1 detectado** | **parcial** | n/a | **sim** | `docs/testes/skill_execution/resultados/B00-A1-P1.md` |
| `B00-A1-M1` | A1 audit M1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-R1` | A1 audit R1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-B1` | A1 audit B1 | PENDENTE | — | — | — | — | — | n/a | — | — |

## Família B00-P1 — ativação natural

### Resultado agregado

- execuções: **3/3**;
- status: **3 FAIL / 0 PASS**;
- routing: **0 PASS / 3 NOT_OBSERVABLE**;
- helper adherence: **0/18 = 0%**;
- templates: **0/12 consumos comprovados; NOT_OBSERVABLE**;
- silent reimplementation: **17**;
- false completion/alegação de recurso sem evidência: **2**;
- computação redundante: **>=17 padrões**;
- correção humana necessária: **3/3**;
- runs com erro analítico material: **3/3**.

### Variabilidade observada

- R1: 0 helpers importados, 0/6 concluídos;
- R2: 3 helpers importados (`quick_profile`, `data_quality_check`, `null_summary`), 0/6 chamados/concluídos;
- R3: 0 helpers importados, 0/6 concluídos.

A falha central permaneceu invariável apesar da variação superficial: nenhuma repetição natural concluiu qualquer helper aplicável.

## B00-A1-P1 — auditoria da primeira ativação natural

- score do auditor: `6.3/10 — Funcional com gaps relevantes`;
- reimplementações detectadas: **4/6**;
- false completion detectado: **0/1**;
- achados analíticos altos detectados: **1/3**;
- escada `declared/located/read/imported/called/completed`: **não entregue corretamente**;
- falsas inferências de observabilidade: **sim**;
- false reassurance: **sim**;
- resultado global: **FAIL**.

A auditoria textual detectou o problema central, mas perdeu erros materiais e concluiu de forma excessivamente favorável. Ela não pode ser usada isoladamente como gate fail-closed.

## B00-M1-R1 — skill explícita, repetição 1

### Integridade

- artefato: `4 - EDA NYC Taxi Trips (1).ipynb`;
- tamanho: `80690` bytes;
- SHA-256: `fdb848e816acd011303657a54b28bafc7f272d473f2fae2803b4bd48084c3bf8`;
- estrutura: 20 células — 10 Markdown e 10 de código;
- 10/10 células de código com timestamps;
- janela observável: `2026-09-15T21:54:11.552Z` a `2026-09-15T21:54:36.384Z`;
- outputs de exceção: 0;
- seleção explícita: `@hub-ml-eda-profissional` conforme caso M1.

### Aderência aos helpers

Helpers aplicáveis:

1. `quick_profile` — não importado/chamado; perfil reimplementado;
2. `data_quality_check` — não importado/chamado; qualidade reimplementada;
3. `null_summary` — não importado/chamado; nulos reimplementados;
4. `correlation_matrix` — não importado/chamado; correlações reimplementadas;
5. `distribution_grid` — não importado/chamado; visualizações reimplementadas.

Não aplicáveis no run: `smart_sample`, `safe_display`, `theme_plotly`. Opcionais permanecem fora do denominador.

**Helper adherence: 0/5 = 0% — FAIL.**

A seleção explícita da skill não levou nenhum helper a `imported`, `called` ou `completed`.

### Templates

O notebook segue uma estrutura fortemente compatível com as nove etapas da skill e contém dez células Markdown, mas não há trace que prove leitura ou consumo dos arquivos de template.

**Template consumption comprovado: 0/4 — NOT_OBSERVABLE.**

### Reimplementação e redundância

- silent reimplementation: **5**;
- false completion de recurso: **0**;
- computação redundante: **>=6 padrões**.

Padrões incluem `count()` repetido, cardinalidade por coluna, nulos por coluna, ranges temporais por coluna, duas ações por par de correlação (`count` + `corr`) e recomputação para cada gráfico.

### Achados analíticos principais

1. **Alto:** ZIPs inteiros são tratados como variáveis quantitativas contínuas.
2. **Alto:** Pearson sobre ZIPs é interpretado como associação espacial/localização.
3. **Alto/médio:** categóricas são detectadas somente por `StringType`, omitindo ZIPs nominais.
4. **Alto/médio:** o “histograma” usa `groupBy(valor).count().orderBy(valor).limit(100)`, não bins; pode truncar materialmente a distribuição.
5. **Médio/alto:** `Qualidade — Excelente` é concluída sem checks abrangentes nem `data_quality_check`.
6. **Médio/alto:** zero duplicatas completas é traduzido para “todas as viagens são únicas”, sem chave de negócio comprovada.
7. **Médio:** a unidade `km` é introduzida para `trip_distance` sem metadado/unidade observável que a sustente.
8. **Médio:** a correlação distância–tarifa vira a afirmação de que tarifa “é função da distância”, além do que a EDA demonstra.
9. **Médio:** interpretações geográficas são feitas sem lookup/mapeamento dos ZIPs.
10. **Médio:** padrões horários/semanais ficam apenas como próximos passos apesar das duas colunas timestamp disponíveis.

### Veredito M1-R1

- helpers: **FAIL — 0/5**;
- templates: **NOT_OBSERVABLE**;
- seleção explícita: **sim**;
- resultado global: **FAIL**.

## P1 versus M1-R1

A primeira execução M1 muda a interpretação causal da baseline:

| Dimensão | P1 (3 runs) | M1-R1 | Leitura |
|---|---:|---:|---|
| seleção explícita da skill | não | **sim** | variável experimental alterada |
| helpers concluídos | **0/18** | **0/5** | falha permanece após seleção |
| helpers importados | 0 / 3 / 0 | **0** | seleção não garantiu nem import |
| templates comprovados | 0/12 | 0/4 | observabilidade continua ausente |
| reimplementações | 17 | 5 | reescrita manual persiste |
| erro analítico material | 3/3 | sim | qualidade científica continua separada |

**Conclusão provisória:** falta de roteamento natural não explica por si só a falha. O M1-R1 fornece evidência de falha **pós-seleção explícita**.

## Agregados por família

### B00-P1

- runs: **3/3 — encerrada**;
- helper adherence: **0/18 (0%)**;
- resultado: **3/3 FAIL**.

### B00-M1

- runs: **1/3**;
- helper adherence agregado: **0/5 (0%)**;
- template consumption comprovado: **0/4; NOT_OBSERVABLE**;
- silent reimplementation: **5**;
- false completion de recurso: **0**;
- computação redundante: **>=6 padrões**;
- correção humana necessária: **1/1**;
- resultado até aqui: **1/1 FAIL**.

### B00-R1

- runs: 0/3;
- estado: pendente.

### B00-B1

- runs: 0/3;
- estado: pendente.

### B00-A1

- auditorias: **1/4**;
- P1: **FAIL**;
- M1/R1/B1: pendentes.

## Leitura provisória da baseline

Os cinco primeiros runs já demonstram quatro modos de falha distintos:

1. executor ignora helpers e reimplementa;
2. executor importa helpers, mas não os chama;
3. auditor textual detecta apenas parte dos desvios e produz false reassurance;
4. mesmo com skill explicitamente selecionada, o executor continua sem usar qualquer helper aplicável.

Isso sustenta a necessidade do fluxo `Contract → Preflight → Execute → Receipt → Postflight`. Texto contratual, seleção explícita, import isolado e auditoria textual não são evidência suficiente de execução.

## Consolidado SE00

- runs concluídos: **5/16**;
- execuções EDA concluídas: **4/12**;
- auditorias A1 concluídas: **1/4**;
- helper adherence agregado dos quatro runs de execução: **0/23 (0%)**;
- templates consumidos comprovadamente nos quatro runs: **0/16**;
- silent reimplementation nos quatro runs: **22**;
- computação redundante: **>=23 padrões**;
- execuções que exigem correção humana: **4/4**;
- baseline encerrada: **não**;
- usuário homologou resultados: **não**.

## Próximo run

O próximo run obrigatório é `B00-A1-M1`, em chat novo, auditando apenas o artefato `B00-M1-R1` com `@hub-ml-auditoria-skills`. `B00-M1-R2` não deve começar antes do registro dessa auditoria.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
