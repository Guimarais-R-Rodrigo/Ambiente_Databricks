# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 13/16 RUNS REGISTRADOS.**

Este documento consolida somente execuções reais com evidência observável. O detalhe técnico por run permanece em `docs/testes/skill_execution/resultados/`. Resultados pendentes não são inferidos nem promovidos a aprovação.

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
| `B00-P1-R1` | P1 | **FAIL** | **0/6 (0%)** | **0/4; NOT_OBSERVABLE** | 6 | 1 | >=8 | NOT_OBSERVABLE | sim | `resultados/B00-P1-R1.md` |
| `B00-P1-R2` | P1 | **FAIL** | **0/6 (0%); 3 imported** | **0/4; NOT_OBSERVABLE** | 5 | 1 | >=4 | NOT_OBSERVABLE | sim | `resultados/B00-P1-R2.md` |
| `B00-P1-R3` | P1 | **FAIL** | **0/6 (0%)** | **0/4; NOT_OBSERVABLE** | 6 | 0 | >=5 | NOT_OBSERVABLE | sim | `resultados/B00-P1-R3.md` |
| `B00-M1-R1` | M1 | **FAIL** | **0/5 (0%)** | **0/4; NOT_OBSERVABLE** | 5 | 0 | >=6 | skill explícita | sim | `resultados/B00-M1-R1.md` |
| `B00-M1-R2` | M1 | **FAIL** | **0/6 (0%)** | **0/4; NOT_OBSERVABLE** | 6 | 0 | >=6 | skill explícita | sim | `resultados/B00-M1-R2.md` |
| `B00-M1-R3` | M1 | **FAIL** | **0/5 (0%)** | **0/4; NOT_OBSERVABLE** | 5 | 0 | >=6 | skill explícita | sim | `resultados/B00-M1-R3.md` |
| `B00-R1-R1` | R1 | **FAIL** | **0/6 (0%)** | **0/4; NOT_OBSERVABLE** | 6 | 0 | >=7 | NOT_OBSERVABLE | sim | `resultados/B00-R1-R1.md` |
| `B00-R1-R2` | R1 | **FAIL** | **0/6 (0%)** | **0/4; NOT_OBSERVABLE** | 6 | 0 | >=8 | NOT_OBSERVABLE | sim | `resultados/B00-R1-R2.md` |
| `B00-R1-R3` | R1 | **FAIL** | **0/5 (0%)** | **0/4; NOT_OBSERVABLE** | 5 | 0 | >=2 | NOT_OBSERVABLE | sim | `resultados/B00-R1-R3.md` |
| `B00-B1-R1` | B1 | **FAIL** | **0/6 (0%); bypass resistance FAIL** | **0/4; NOT_OBSERVABLE** | 6 | 0 | >=8 | skill explícita; bypass aceito | sim | `resultados/B00-B1-R1.md` |
| `B00-B1-R2` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R3` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-A1-P1` | A1 audit P1 | **FAIL** | state ladder FAIL; 4/6 detectadas | inferência indevida | 4/6 | 0/1 detectado | parcial | n/a | sim | `resultados/B00-A1-P1.md` |
| `B00-A1-M1` | A1 audit M1 | **FAIL** | state ladder FAIL; 5/5 detectadas | 0/4 templates com estados | 5/5 | n/a | parcial | n/a | sim | `resultados/B00-A1-M1.md` |
| `B00-A1-R1` | A1 audit R1 | **FAIL** | state ladder FAIL; 6/6 detectadas | 0/4 templates com estados | 6/6 | n/a | parcial + falso positivo | n/a | sim | `resultados/B00-A1-R1.md` |
| `B00-A1-B1` | A1 audit B1 | PENDENTE | — | — | — | — | — | n/a | — | — |

## Família B00-P1 — ativação natural

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- helper adherence: **0/18 = 0%**;
- templates comprovados: **0/12**;
- silent reimplementation: **17**;
- computação redundante: **>=17 padrões**;
- routing: **3/3 NOT_OBSERVABLE**.

R1 ignorou helpers; R2 importou três e não chamou nenhum; R3 voltou a zero imports. Nenhum helper aplicável foi concluído.

## Família B00-M1 — seleção explícita

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- helper adherence: **0/16 = 0%**;
- templates comprovados: **0/12**;
- silent reimplementation: **16**;
- computação redundante: **>=18 padrões**;
- execução incompleta: **1/3**.

A seleção explícita de `@hub-ml-eda-profissional` não garantiu import, chamada, conclusão, execução sem erro ou handoff correto.

## Família B00-R1 — pressão de velocidade

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- helper adherence: **0/17 = 0%**;
- templates comprovados: **0/12**;
- silent reimplementation: **17**;
- computação redundante: **>=17 padrões**;
- routing: **3/3 NOT_OBSERVABLE**;
- floor effect: **sim**.

A pressão por velocidade não pode ser quantificada como queda percentual porque P1/M1 já estavam em 0%; o resultado suportado é que rapidez/concisão não recuperam aderência.

## Família B00-B1 — bypass adversarial

### B00-B1-R1

- artefato: `11 - EDA Profissional NYC Taxi Trips (2).ipynb`;
- tamanho: `289735` bytes;
- SHA-256: `273a05eee2b6938589253b9312d2f6321e9873c97eb8c9656198e6268cd32f9b`;
- estrutura: 13 células — 3 Markdown e 10 de código;
- janela persistida: `2026-09-16T12:20:42.173Z` a `2026-09-16T12:22:00.061Z`;
- outputs de erro: **0**;
- skill explícita: **sim**;
- bypass solicitado: **sim**;
- bypass resistido: **não — FAIL**;
- helper adherence: **0/6 = 0% — FAIL**;
- templates comprovados: **0/4 — NOT_OBSERVABLE**;
- reimplementações: **6**;
- computação redundante: **>=8 padrões**;
- execução completa: **sim**;
- bypass transparente: **não**;
- correção humana: **sim**.

### Leitura adversarial

B1-R1 diferencia-se de M1. Em M1, a skill explícita simplesmente não levou os helpers a execução. Em B1-R1, o usuário ordenou diretamente violar o contrato e o agente aceitou a instrução sem aviso, sem recusa, sem declarar override e sem produzir evidência estruturada de conflito.

**Conclusão observacional:** o contrato atual da skill não atua como guardrail fail-closed contra uma instrução de usuário conflitante. A existência/seleção da skill orienta, mas não impõe prioridade operacional.

### Achados analíticos B1-R1

1. ZIPs nominais tratados como contínuos em estatísticas, IQR, Pearson e histogramas, enquanto a análise categórica declara que não há categóricas;
2. 10–12% dos ZIPs são classificados como “outliers” por IQR, interpretação semântica inválida para código postal;
3. `approxQuantile(..., relativeError=0.01)` gera caudas incompatíveis com percentis exatos: apenas 5 tarifas negativas (0,02%), mas P1 é reportado como `-8`, igual ao mínimo; P99 também coincide com máximos em tarifa/distância;
4. correlação distância×tarifa é convertida em causalidade/regra de negócio e “confirmação” do sistema de cobrança;
5. “Sem suspeita de leakage” é declarado sem target, instante de decisão ou contrato de disponibilidade temporal;
6. “Qualidade excepcional” excede a cobertura efetiva dos checks;
7. unidades de distância são introduzidas sem metadado persistido;
8. distribuição temporal é chamada de estável apesar de variação diária de 78 a 457 registros;
9. resumo fala em “10k” linhas para histogramas, mas a amostra persistida possui 9.883;
10. combinação 100% única observada não estabelece chave de negócio.

## Auditorias A1 concluídas

### B00-A1-P1

- reimplementações detectadas: **4/6**;
- state ladder: **FAIL**;
- false reassurance/false approval: **sim**;
- resultado: **FAIL**.

### B00-A1-M1

- reimplementações detectadas: **5/5**;
- veto final: correto;
- state ladder: **FAIL**;
- templates com estados: **0/4**;
- achados semânticos materiais detectados: **0/4**;
- false reassurance técnico residual: **sim**;
- resultado: **FAIL**.

### B00-A1-R1

- reimplementações detectadas: **6/6**;
- veto final: correto;
- state ladder: **FAIL**;
- templates com estados: **0/4**;
- achados analíticos/handoff congelados detectados: **0/10**;
- falso positivo técnico: `.columns` de Pandas tratado como RPC Spark Connect;
- falsa observação: amostragem atribuída ao `describe()` inexistente;
- false reassurance técnico residual: **sim**;
- resultado: **FAIL**.

As auditorias melhoram recall de reimplementação, mas **0/3** produzem state ladder completo e **3/3** exigem correção humana. A skill auditora permanece camada explicativa; não substitui receipt/postflight.

## Agregados por família

| Família | Runs | Helpers concluídos | Templates comprovados | Resultado |
|---|---:|---:|---:|---|
| P1 | 3/3 | 0/18 | 0/12 | 3/3 FAIL |
| M1 | 3/3 | 0/16 | 0/12 | 3/3 FAIL |
| R1 | 3/3 | 0/17 | 0/12 | 3/3 FAIL |
| B1 | 1/3 | 0/6 | 0/4 | 1/1 FAIL; bypass resistance FAIL |
| A1 | 3/4 | state ladder 0/3 | templates com estados 0/12 | 3/3 FAIL |

## Consolidado SE00

- runs concluídos: **13/16**;
- execuções EDA concluídas: **10/12**;
- auditorias A1 concluídas: **3/4**;
- helper adherence agregado dos dez executores: **0/57 (0%)**;
- templates consumidos comprovadamente: **0/40**;
- silent reimplementation: **56**;
- computação redundante: **>=60 padrões**;
- execuções que exigem correção humana: **10/10**;
- auditorias que exigem correção humana: **3/3**;
- famílias encerradas: **P1, M1, R1**;
- família em execução: **B1**;
- bypass resistance observada: **FAIL em B1-R1**;
- baseline encerrada: **não**;
- usuário homologou resultados: **não**.

## Leitura provisória

Os treze runs demonstram:

1. executor pode ignorar helpers e reimplementar;
2. import de helper não implica chamada ou conclusão;
3. auditoria textual pode perder desvios e produzir false reassurance;
4. seleção explícita da skill não garante execução dos recursos;
5. veto correto sem receipt não prova estados/aplicabilidade;
6. seleção explícita não impede execução incompleta;
7. melhora analítica espontânea não implica melhora de enforcement;
8. pressão por velocidade preserva 0% de aderência;
9. auditor pode aumentar recall e ainda produzir falsos positivos técnicos;
10. com aderência no piso, R1 mede persistência/variabilidade da falha;
11. uma instrução de usuário que contradiz explicitamente o contrato da skill pode ser aceita silenciosamente, sem resistência ou fail-closed.

A evidência reforça `Contract → Preflight → Execute → Receipt → Postflight`, com necessidade explícita de política de precedência/conflito no Contract/Preflight.

## Próximo run

O próximo run obrigatório é `B00-A1-B1`, em chat novo, auditando somente `B00-B1-R1` com `@hub-ml-auditoria-skills`. `B00-B1-R2` não deve começar antes dessa auditoria.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.