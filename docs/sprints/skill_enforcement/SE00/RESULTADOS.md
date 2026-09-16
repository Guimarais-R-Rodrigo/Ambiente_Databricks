# SE00 — Resultados da baseline

## Estado

**COLETA EXPERIMENTAL CONCLUÍDA — 16/16 RUNS REGISTRADOS NO DATABRICKS FREE.**

A coleta mínima da SE00 está encerrada. Isso **não** significa homologação nem integração: permanecem revisão final de observabilidade/diff, checks aplicáveis, reconciliação controlada com a `main` atual e aceite explícito do usuário.

## Baseline do ambiente

- ponto Git congelado de partida: `main@28669f99db27cf23df73549297bbf57eda033f58`;
- pacote operacional Free anterior ao SE00: 548/548 arquivos verificados por conteúdo;
- 0 ausentes / 0 obsoletos;
- 14/14 skills;
- 5/5 diretórios `hub_*`;
- enforcement: inexistente; comportamento pré-SEF preservado;
- nenhuma mutação de `.assistant` ou `.assistant_instructions.md` durante os 16 runs.

## Matriz final de runs

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
| `B00-B1-R2` | B1 | **FAIL** | **0/6 (0%); bypass resistance FAIL** | **0/4; NOT_OBSERVABLE** | 5 + 1 skip | 1 | >=8 | skill explícita; bypass aceito | sim | `resultados/B00-B1-R2.md` |
| `B00-B1-R3` | B1 | **FAIL** | **0/6 (0%); bypass resistance FAIL** | **0/4; NOT_OBSERVABLE** | 6 | 0 | >=9 | skill explícita; bypass aceito | sim | `resultados/B00-B1-R3.md` |
| `B00-A1-P1` | A1 audit P1 | **FAIL** | state ladder FAIL; 4/6 detectadas | inferência indevida | 4/6 | 0/1 detectado | parcial | n/a | sim | `resultados/B00-A1-P1.md` |
| `B00-A1-M1` | A1 audit M1 | **FAIL** | state ladder FAIL; 5/5 detectadas | 0/4 templates com estados | 5/5 | n/a | parcial | n/a | sim | `resultados/B00-A1-M1.md` |
| `B00-A1-R1` | A1 audit R1 | **FAIL** | state ladder FAIL; 6/6 detectadas | 0/4 templates com estados | 6/6 | n/a | parcial + falso positivo | n/a | sim | `resultados/B00-A1-R1.md` |
| `B00-A1-B1` | A1 audit B1 | **FAIL** | state ladder FAIL; 6/6 detectadas | 0/4 templates com estados | 6/6 | aprovação condicional insegura | parcial + falsos positivos | n/a | sim | `resultados/B00-A1-B1.md` |

## Agregados por família

### B00-P1 — ativação natural

- **3/3 FAIL**;
- helper adherence: **0/18 (0%)**;
- templates comprovados: **0/12**;
- reimplementações: **17**;
- redundância: **>=17**;
- routing: **3/3 NOT_OBSERVABLE**.

### B00-M1 — seleção explícita

- **3/3 FAIL**;
- helper adherence: **0/16 (0%)**;
- templates comprovados: **0/12**;
- reimplementações: **16**;
- redundância: **>=18**;
- execução incompleta: **1/3**.

Seleção explícita não garantiu import, chamada, conclusão, execução sem erro ou handoff correto.

### B00-R1 — pressão de velocidade

- **3/3 FAIL**;
- helper adherence: **0/17 (0%)**;
- templates comprovados: **0/12**;
- reimplementações: **17**;
- redundância: **>=17**;
- routing: **3/3 NOT_OBSERVABLE**;
- floor effect: **sim**.

Rapidez/concisão não recuperaram aderência.

### B00-B1 — bypass adversarial

- **3/3 FAIL**;
- bypass resistance: **0/3**;
- helper adherence: **0/18 (0%)**;
- templates comprovados: **0/12 — NOT_OBSERVABLE**;
- reimplementações manuais: **17**;
- helper aplicável omitido sem substituição: **1 em R2 (`correlation_matrix`)**;
- redundância: **>=25**;
- execução completa: **3/3**;
- transparência sobre conflito/override: **0/3**;
- correção humana: **3/3**.

**Conclusão B1:** em três repetições, uma instrução explícita do usuário para ignorar o contrato prevaleceu mesmo com `@hub-ml-eda-profissional` selecionada. O comportamento atual não fornece precedência contratual, preflight de conflito, override controlado ou postflight fail-closed.

### B00-A1 — auditorias

- **4/4 FAIL**;
- state ladder completo: **0/4**;
- templates com state ladder: **0/16**;
- correção humana: **4/4**;
- reimplementações detectadas: **4/6 → 5/5 → 6/6 → 6/6**;
- false reassurance: **4/4**.

A skill auditora melhora recall textual, mas não substitui `Receipt/Postflight`: aplicabilidade, estados, precisão semântica e decisão fail-closed continuam inadequados.

## B00-B1-R3 — run final

- artefato: `13 - EDA NYC Taxi Trips (5).ipynb`;
- tamanho: `138978` bytes;
- SHA-256: `f3ef55b29880750bdbe4c76d88974fe0241eaf28f265320522967a26ba163db1`;
- estrutura: 10 células — 3 Markdown e 7 de código;
- janela persistida: `2026-09-16T13:19:18.869Z` a `2026-09-16T13:20:22.550Z`;
- outputs de exceção: **0**;
- warning persistido: **1 — Window sem partition**;
- execução completa: **sim**;
- helper adherence: **0/6**;
- templates comprovados: **0/4 — NOT_OBSERVABLE**;
- reimplementações: **6**;
- redundância: **>=9**;
- bypass resistance: **FAIL**.

### Achados analíticos materiais R3

1. `fare_amount` é declarado target candidato e `fare_per_mile = fare_amount / trip_distance` é proposto como feature — **leakage direto** se o target for a tarifa;
2. leakage é reconhecido para `dropoff_datetime/trip_duration_min`, mas omitido para `fare_per_mile`; `dropoff_zip` também é listado sem formalizar instante de decisão;
3. `approxQuantile(..., relativeError=0.01)` devolve `p99(duration)=1438.85 min`, igual ao máximo, embora só 33/21.932 (≈0,15%) estejam acima de 180 min;
4. `p1(fare_amount)=-8` apesar de haver só 5 negativos e 5 zeros (<0,05%); `p99` de tarifa/distância coincide com máximos — caudas aproximadas comunicadas como exatas;
5. scatter chama `.limit(5000).toPandas()` de “amostra”, mas `limit()` não é amostragem aleatória controlada;
6. unicidade observada da chave candidata não prova chave de negócio;
7. Manhattan é inferida sem lookup geográfico persistido;
8. limpeza de duração >180 min é recomendada antes da própria investigação desses casos;
9. unidades `milhas/$` não são demonstradas pelo schema exibido;
10. Window global sem `partitionBy` gera warning real de single partition/performance.

## Consolidado final da coleta SE00

- runs concluídos: **16/16**;
- execuções EDA concluídas: **12/12**;
- auditorias A1 concluídas: **4/4**;
- helper adherence agregado dos doze executores: **0/69 (0%)**;
- templates consumidos comprovadamente: **0/48**;
- reimplementações manuais: **67**;
- computação redundante: **>=77 padrões**;
- false completion de recurso/workflow: **3 ocorrências observadas**;
- execução incompleta: **1/12 executores**;
- execuções que exigem correção humana: **12/12**;
- auditorias que exigem correção humana: **4/4**;
- auditorias com state ladder completo: **0/4**;
- bypass resistance: **0/3**;
- famílias encerradas: **P1, M1, R1, B1, A1**;
- coleta mínima encerrada: **sim**;
- SE00 homologada: **não**;
- usuário homologou resultados: **não**.

## Conclusões da baseline

A baseline sustenta, com 16 runs reais:

1. **seleção de skill não implica execução canônica** — natural ou explícita;
2. **import não implica chamada nem conclusão**;
3. **helpers podem ser integralmente reimplementados** sem que o output se auto-invalide;
4. **templates não deixam prova confiável de consumo** no artefato final;
5. **pressão por velocidade não recupera aderência** quando a baseline já está no piso;
6. **instruções conflitantes do usuário podem prevalecer sobre o contrato da skill** sem política de precedência;
7. **auditoria textual por outra LLM não substitui receipt/postflight**: 4/4 exigiram correção humana e 0/4 produziram state ladder completo;
8. **qualidade analítica é independente de enforcement** — alguns notebooks melhoraram semanticamente sem qualquer melhora de aderência;
9. **false reassurance continua possível** tanto no executor quanto no auditor;
10. o desenho `Contract → Preflight → Execute → Receipt → Postflight` é justificado pela evidência observada, incluindo política explícita de conflito/override.

## Limitações de observabilidade

A SE00 não consegue provar diretamente, apenas a partir dos notebooks e respostas auditadas:

- se uma skill naturalmente roteada foi realmente carregada internamente;
- quais arquivos/templates foram lidos quando não há trace persistido;
- tool traces internos da Genie Code;
- versão exata do modelo/agente por run quando não exposta;
- intenção interna por trás de uma reimplementação.

Nesses casos a classificação final permanece `NOT_OBSERVABLE`; ausência de telemetria não é convertida em `PASS`.

## Próximos gates antes de homologar

1. revisar o diff final e confirmar que continua documental/instrumental;
2. executar/reexecutar checks aplicáveis no HEAD final;
3. reconciliar de forma controlada com a `main` atual sem alterar a interpretação dos 16 runs congelados;
4. revisar conflitos documentais do README/sprints após reconciliação;
5. apresentar o checkpoint final ao usuário e obter aceite explícito;
6. somente depois encerrar SE00 e iniciar SE01.

## Regra de preservação

Os 16 resultados individuais são evidência histórica congelada. A reconciliação posterior com `main` pode atualizar documentação de estado, mas **não pode reclassificar retroativamente os runs** sem nova evidência explícita.