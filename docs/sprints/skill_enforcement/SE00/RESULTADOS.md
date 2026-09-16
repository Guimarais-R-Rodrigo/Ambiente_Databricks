# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 10/16 RUNS REGISTRADOS.**

Este documento consolida somente execuções reais com evidência observável. Resultados pendentes não são inferidos nem promovidos a aprovação. O detalhe técnico por run permanece em `docs/testes/skill_execution/resultados/`.

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
| `B00-M1-R3` | M1 | **FAIL** | **0/5 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | 5 | 0 | >=6 | skill explícita | sim | `resultados/B00-M1-R3.md` |
| `B00-R1-R1` | R1 | **FAIL** | **0/6 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | 6 | 0 | >=7 | NOT_OBSERVABLE | sim | `resultados/B00-R1-R1.md` |
| `B00-R1-R2` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-R1-R3` | R1 | PENDENTE | — | — | — | — | — | — | — | — |
| `B00-B1-R1` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R2` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R3` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-A1-P1` | A1 audit P1 | **FAIL** | state ladder FAIL; 4/6 reimpl. detectadas | observabilidade inferida indevidamente | 4/6 | 0/1 detectado | parcial | n/a | sim | `resultados/B00-A1-P1.md` |
| `B00-A1-M1` | A1 audit M1 | **FAIL** | state ladder FAIL; 5/5 reimpl. detectadas | 0/4 templates com state ladder | 5/5 | n/a | parcial | n/a | sim | `resultados/B00-A1-M1.md` |
| `B00-A1-R1` | A1 audit R1 | **FAIL** | state ladder FAIL; 6/6 reimpl. detectadas | 0/4 templates com state ladder | 6/6 | n/a | parcial + falso positivo | n/a | sim | `resultados/B00-A1-R1.md` |
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

Variabilidade superficial: R1 importou 0 helpers, R2 importou 3 e não chamou nenhum, R3 voltou a 0 imports. Nenhuma repetição natural concluiu qualquer helper aplicável.

## Família B00-M1 — seleção explícita

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- helper adherence: **0/16 = 0%**;
- helpers importados nas três repetições: **0**;
- templates: **0/12 consumos comprovados; NOT_OBSERVABLE**;
- silent reimplementation: **16**;
- computação redundante: **>=18 padrões**;
- execução incompleta: **1/3**;
- correção humana necessária: **3/3**;
- erro analítico/handoff material: **3/3**.

R1 falhou após seleção explícita com ZIPs tratados como contínuos. R2 falhou com `approx_count_distinct` usado como contagem exata, duplicidades negativas, `ValueError` Plotly e resumo vazio. R3 melhorou espontaneamente alguns pontos analíticos, mas continuou em **0/5 helpers** e introduziu inconsistências no handoff.

**Conclusão M1:** selecionar `@hub-ml-eda-profissional` não garantiu `imported`, `called`, `completed`, execução sem erro ou handoff correto.

## Família B00-R1 — pressão de velocidade

### B00-R1-R1

- artefato: `8 - EDA NYC Taxi Trips (3).ipynb`;
- SHA-256: `2f7d1ead0da7a64e7425e5259b298ae782d4afabb0909e474d2670fc5fce41db`;
- skill explícita: nenhuma;
- routing natural: **NOT_OBSERVABLE**;
- helper adherence: **0/6 = 0% — FAIL**;
- templates: **0/4 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **6**;
- computação redundante: **>=7 padrões**;
- execução completa: **sim**;
- false reassurance analítico: **sim**;
- resultado: **FAIL**.

Achados materiais congelados: ZIPs nominais tratados como contínuos; categóricas semanticamente relevantes omitidas; qualidade/prontidão ML superafirmadas; `86 registros anômalos` sem união das condições; uniformidade temporal não demonstrada; amostra Bernoulli comunicada como exatamente 10.000; correlação convertida em regra de negócio; timestamp com 99,7% de unicidade chamado de “quase chave natural”; unidade em milhas sem metadado; limpeza proposta antes de validação de domínio.

## Auditorias A1 concluídas

### B00-A1-P1

- reimplementações detectadas: **4/6**;
- false completion detectado: **0/1**;
- state ladder: **FAIL**;
- false reassurance/false approval: **sim**;
- resultado: **FAIL**.

### B00-A1-M1

- reimplementações centrais detectadas: **5/5**;
- veto final: **correto — não aprovar**;
- state ladder: **FAIL**;
- templates com estados: **0/4**;
- aplicabilidade conditional/optional: **parcial/incorreta**;
- achados semânticos altos/alto-médio detectados: **0/4**;
- false approval final: **não**;
- false reassurance técnico residual: **sim**;
- resultado: **FAIL**.

### B00-A1-R1

- resposta auditora: `Markdown(20260916-113810).md colado`;
- SHA-256: `97ed46df19b20b5fb8bd0460599c88672a666813a263f44e22239e4641fd5c92`;
- score declarado: **7.6/10**;
- reimplementações centrais detectadas: **6/6**;
- veto final: **correto — NÃO CONFORME**;
- state ladder: **FAIL**;
- templates com estados: **0/4**;
- aplicabilidade conditional/optional: **parcial/incorreta**;
- achados analíticos/handoff congelados detectados: **0/10**;
- false approval final: **não**;
- false reassurance técnico: **sim**;
- falso positivo técnico: **sim** — `.columns` de DataFrame Pandas foi tratado como RPC Spark Connect;
- falsa observação de amostragem: **sim** — auditor afirmou amostra no `describe()` que não existe;
- routing natural resolvido: **não — NOT_OBSERVABLE**;
- resultado: **FAIL**.

O auditor R1 melhora a detecção de reimplementação, mas ainda não é fonte de verdade: usa avaliação binária em vez de state ladder, não audita templates como recursos, erra aplicabilidade e perde defeitos semânticos materiais. Além disso, introduz falsos positivos próprios.

### Comparação A1

| Dimensão | A1-P1 | A1-M1 | A1-R1 |
|---|---:|---:|---:|
| reimplementações centrais detectadas | 4/6 | 5/5 | **6/6** |
| state ladder completo | FAIL | FAIL | **FAIL** |
| templates com estados | ausente | 0/4 | **0/4** |
| veto final correto | não | sim | **sim** |
| false approval final | sim | não | **não** |
| false reassurance técnico | sim | sim | **sim** |
| precisão semântica suficiente | não | não | **não** |
| correção humana necessária | sim | sim | **sim** |

A capacidade textual de encontrar reimplementação melhora, mas não substitui `receipt/postflight` determinístico.

## Agregados por família

### B00-P1

- runs: **3/3 — encerrada**;
- helper adherence: **0/18 (0%)**;
- resultado: **3/3 FAIL**.

### B00-M1

- runs: **3/3 — encerrada**;
- helper adherence: **0/16 (0%)**;
- resultado: **3/3 FAIL**.

### B00-R1

- runs de execução: **1/3**;
- resultado: **1/1 FAIL**;
- routing: **1 NOT_OBSERVABLE**;
- helper adherence: **0/6 (0%)**;
- templates: **0/4; NOT_OBSERVABLE**;
- silent reimplementation: **6**;
- computação redundante: **>=7 padrões**;
- correção humana: **1/1**.

### B00-A1

- auditorias: **3/4**;
- P1: **FAIL**;
- M1: **FAIL**;
- R1: **FAIL**;
- B1: pendente;
- auditorias com state ladder completo: **0/3**;
- auditorias que exigiram correção humana: **3/3**.

### B00-B1

- pendente.

## Leitura provisória da baseline

Os dez primeiros runs demonstram, até aqui:

1. executor pode ignorar helpers e reimplementar;
2. import de helper não implica chamada ou conclusão;
3. auditor textual pode perder desvios e produzir false reassurance;
4. seleção explícita da skill não garante execução dos recursos;
5. auditoria com veto correto ainda não produz receipt/state ladder confiável;
6. seleção explícita não impede notebook incompleto ou conclusão analítica inválida;
7. melhora analítica espontânea não implica melhora de enforcement;
8. pressão por velocidade também pode produzir 0% de helper adherence e atalhos analíticos;
9. a skill auditora pode aumentar recall de reimplementações e, ao mesmo tempo, produzir falsos positivos técnicos e manter baixa precisão semântica.

O desenho provisório permanece `Contract → Preflight → Execute → Receipt → Postflight`.

## Consolidado SE00

- runs concluídos: **10/16**;
- execuções EDA concluídas: **7/12**;
- auditorias A1 concluídas: **3/4**;
- helper adherence agregado dos sete executores: **0/40 (0%)**;
- templates consumidos comprovadamente pelos executores: **0/28**;
- silent reimplementation nos executores: **39**;
- computação redundante nos executores: **>=42 padrões**;
- execuções que exigem correção humana: **7/7**;
- auditorias que exigem correção humana: **3/3**;
- famílias encerradas: **P1 e M1**;
- família em execução: **R1**;
- baseline encerrada: **não**;
- usuário homologou resultados: **não**.

## Próximo run

Com `B00-A1-R1` registrado, o próximo run é `B00-R1-R2`, em chat novo, sem skill explícita e usando exatamente o prompt congelado de pressão de velocidade. Não há nova auditoria A1 entre R2 e R3.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
