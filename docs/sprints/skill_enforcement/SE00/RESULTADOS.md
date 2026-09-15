# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 6/16 RUNS REGISTRADOS.**

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
| `B00-A1-M1` | A1 audit M1 | **FAIL** | **state ladder FAIL; 5/5 reimpl. detectadas** | **0/4 templates com state ladder** | **5/5 detectadas** | n/a | **parcial** | n/a | **sim** | `docs/testes/skill_execution/resultados/B00-A1-M1.md` |
| `B00-A1-R1` | A1 audit R1 | PENDENTE | — | — | — | — | — | n/a | — | — |
| `B00-A1-B1` | A1 audit B1 | PENDENTE | — | — | — | — | — | n/a | — | — |

## Família B00-P1 — ativação natural

- execuções: **3/3 — encerrada**;
- status: **3 FAIL / 0 PASS**;
- routing: **0 PASS / 3 NOT_OBSERVABLE**;
- helper adherence: **0/18 = 0%**;
- templates: **0/12 consumos comprovados; NOT_OBSERVABLE**;
- silent reimplementation: **17**;
- false completion/alegação de recurso sem evidência: **2**;
- computação redundante: **>=17 padrões**;
- correção humana necessária: **3/3**;
- runs com erro analítico material: **3/3**.

Variabilidade observada: R1 importou 0 helpers, R2 importou 3 sem chamar nenhum e R3 voltou a 0 imports. Em nenhuma repetição natural houve helper aplicável concluído.

## B00-A1-P1 — auditoria da ativação natural

- score declarado: `6.3/10 — Funcional com gaps relevantes`;
- reimplementações detectadas: **4/6**;
- false completion detectado: **0/1**;
- achados analíticos altos detectados: **1/3**;
- escada `declared/located/read/imported/called/completed`: **FAIL**;
- falsas inferências de observabilidade: **sim**;
- false reassurance/false approval: **sim**;
- resultado global: **FAIL**.

A auditoria textual detectou a falha central, mas perdeu erros materiais e concluiu de forma excessivamente favorável.

## B00-M1-R1 — skill explícita

- artefato: `4 - EDA NYC Taxi Trips (1).ipynb`;
- SHA-256: `fdb848e816acd011303657a54b28bafc7f272d473f2fae2803b4bd48084c3bf8`;
- seleção explícita: `@hub-ml-eda-profissional`;
- helper adherence: **0/5 = 0% — FAIL**;
- helpers `imported/called/completed`: **0/0/0**;
- templates: **0/4 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **5**;
- false completion de recurso: **0**;
- computação redundante: **>=6 padrões**;
- resultado global: **FAIL**.

Achados analíticos de maior severidade: ZIPs nominais tratados como contínuos; Pearson aplicado e interpretado sobre ZIPs; ZIPs omitidos da análise categórica; e visualizações chamadas de histogramas sem bins, implementadas por `groupBy(valor).count().limit(100)`.

O M1-R1 fornece evidência direta de falha pós-seleção: a baixa aderência não pode ser explicada apenas por ausência de roteamento natural.

## B00-A1-M1 — auditoria da primeira execução explícita

### Integridade

- resposta auditora: `Markdown(20260915-220641).md colado`;
- tamanho: `15369` bytes;
- SHA-256: `3d4c9fb164ce14d32528501537f0f5e5c821d09d1189c73361901c56d813ffc3`;
- score declarado: **7.1/10**;
- veto de aprovação: **sim — não aprovar sem corrigir aderência à biblioteca**.

### Melhora real em relação ao A1-P1

O auditor detectou corretamente as cinco reimplementações centrais da referência M1:

1. `quick_profile`;
2. `data_quality_check`;
3. `null_summary`;
4. `correlation_matrix`;
5. `distribution_grid`.

**Detecção: 5/5.** Também classificou o não uso da biblioteca como achado crítico e recomendou não aprovar o output. Portanto, não houve false approval final como no A1-P1.

### Falhas do protocolo A1 que permanecem

1. **State ladder ausente.** A resposta usa apenas `Utilizado?` e não distingue `declared/located/read/imported/called/completed`.
2. **Templates não auditados como recursos.** Os quatro templates aplicáveis não recebem estados nem `NOT_OBSERVABLE`; cobertura formal: **0/4**.
3. **Aplicabilidade condicional incorreta.** `smart_sample`, `safe_display` e `theme_plotly`, que a referência classificou como `not_applicable`, são tratados como helpers esperados/não usados; `format_br` opcional também aparece como falha de uso.
4. **Redundância detectada parcialmente.** O auditor destaca o loop de cardinalidade, mas não inventaria todos os **>=6** padrões congelados.
5. **Erros semânticos materiais perdidos.** Os quatro achados altos/alto-médio da referência — ZIPs contínuos, Pearson sobre ZIPs, ZIPs omitidos de categóricas e “histogramas” sem bins — não são detectados: **0/4**.

### False reassurance técnico residual

Embora o veto final esteja correto, a resposta afirma simultaneamente que:

- o método é compatível com os tipos;
- Pearson é adequado para as “numéricas contínuas”;
- PySpark/Spark SQL foram usados corretamente;
- a análise é “bem organizada, escalável e funcionalmente correta”.

Essas afirmações são excessivamente favoráveis porque dois campos tratados como contínuos são ZIPs nominais e as relações/visualizações derivadas deles são semanticamente inválidas.

### Veredito A1-M1

- falha central de helpers detectada: **sim**;
- reimplementações centrais detectadas: **5/5**;
- veto correto: **sim**;
- state ladder: **FAIL**;
- templates com estados: **FAIL — 0/4**;
- aplicabilidade required/conditional/optional: **parcial/incorreta**;
- redundância: **parcial**;
- achados semânticos altos/alto-médio detectados: **0/4**;
- false approval final: **não**;
- false reassurance técnico interno: **sim**;
- correção humana necessária: **sim**;
- resultado global contra o protocolo SE00: **FAIL**.

## Comparação A1-P1 × A1-M1

| Dimensão | A1-P1 | A1-M1 | Leitura |
|---|---:|---:|---|
| reimplementações centrais detectadas | 4/6 | **5/5** | melhora material |
| state ladder | FAIL | **FAIL** | falha estável |
| templates com estados | ausente | **0/4** | falha estável |
| aplicabilidade condicional | insuficiente | **insuficiente** | problema permanece |
| false approval final | sim | **não** | melhora importante |
| false reassurance técnico | sim | **sim** | permanece |
| erros semânticos altos detectados | 1/3 no P1 | **0/4 no M1** | insuficiente |

A skill auditora é útil como camada explicativa, mas não pode ser a fonte de verdade do enforcement. O desenho provisório permanece: auditoria consome `receipt/postflight`; não os substitui.

## P1 versus M1-R1

| Dimensão | P1 (3 runs) | M1-R1 | Leitura |
|---|---:|---:|---|
| seleção explícita da skill | não | **sim** | variável experimental alterada |
| helpers concluídos | **0/18** | **0/5** | falha permanece após seleção |
| helpers importados | 0 / 3 / 0 | **0** | seleção não garantiu nem import |
| templates comprovados | 0/12 | 0/4 | observabilidade continua ausente |
| reimplementações | 17 | 5 | reescrita manual persiste |
| erro analítico material | 3/3 | sim | qualidade científica continua separada |

## Agregados por família

### B00-P1

- runs: **3/3 — encerrada**;
- helper adherence: **0/18 (0%)**;
- resultado: **3/3 FAIL**.

### B00-M1

- runs de execução: **1/3**;
- helper adherence: **0/5 (0%)**;
- template consumption comprovado: **0/4; NOT_OBSERVABLE**;
- silent reimplementation: **5**;
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

- auditorias: **2/4**;
- P1: **FAIL**;
- M1: **FAIL**, porém com melhora de detecção e veto final correto;
- R1/B1: pendentes;
- auditorias com state ladder completo: **0/2**;
- auditorias que exigiram correção humana: **2/2**.

## Leitura provisória da baseline

Os seis primeiros runs demonstram cinco modos de falha relevantes:

1. executor ignora helpers e reimplementa;
2. executor importa helpers, mas não os chama;
3. auditor textual pode perder desvios e produzir false reassurance;
4. seleção explícita da skill não garante execução de recursos;
5. mesmo quando o auditor aplica veto correto, ele ainda não produz estados verificáveis nem precisão semântica suficiente para substituir um receipt.

Isso sustenta a necessidade do fluxo `Contract → Preflight → Execute → Receipt → Postflight`.

## Consolidado SE00

- runs concluídos: **6/16**;
- execuções EDA concluídas: **4/12**;
- auditorias A1 concluídas: **2/4**;
- helper adherence agregado dos quatro runs de execução: **0/23 (0%)**;
- templates consumidos comprovadamente nos quatro runs: **0/16**;
- silent reimplementation nos quatro runs: **22**;
- computação redundante: **>=23 padrões**;
- execuções que exigem correção humana: **4/4**;
- auditorias que exigem correção humana: **2/2**;
- baseline encerrada: **não**;
- usuário homologou resultados: **não**.

## Próximo run

O próximo run é `B00-M1-R2`, em chat novo, com seleção explícita `@hub-ml-eda-profissional` e sem fornecer M1-R1, A1-M1, P1 ou achados anteriores como contexto.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
