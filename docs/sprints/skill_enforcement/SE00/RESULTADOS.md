# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 9/16 RUNS REGISTRADOS.**

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
| `B00-M1-R3` | M1 | **FAIL** | **0/5 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | 5 | 0 | >=6 | skill explícita | sim | `resultados/B00-M1-R3.md` |
| `B00-R1-R1` | R1 | **FAIL** | **0/6 (0%)** | **0/4 comprovados; NOT_OBSERVABLE** | 6 | 0 | >=7 | NOT_OBSERVABLE | sim | `resultados/B00-R1-R1.md` |
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

## Família B00-M1 — seleção explícita

### Resultado agregado

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

R1 falhou após seleção explícita com ZIPs tratados como contínuos e visualização sem bins. R2 falhou com `approx_count_distinct` interpretado como contagem exata, duplicidades negativas, `ValueError` Plotly e resumo vazio. R3 melhorou espontaneamente a semântica dos ZIPs, granularidade, bins e execução, mas manteve **0/5 helpers** e introduziu inconsistências no handoff (`passenger_count` inexistente, distância negativa inexistente e nulos em ZIP inexistentes).

**Conclusão da família M1:** seleção explícita de `@hub-ml-eda-profissional` não garantiu `imported`, `called`, `completed`, execução sem erro ou handoff correto.

## Auditorias A1 concluídas

### B00-A1-P1

- score declarado: `6.3/10 — Funcional com gaps relevantes`;
- reimplementações detectadas: **4/6**;
- false completion detectado: **0/1**;
- achados altos detectados: **1/3**;
- state ladder: **FAIL**;
- false reassurance/false approval: **sim**;
- resultado: **FAIL**.

### B00-A1-M1

- score declarado: **7.1/10**;
- reimplementações centrais detectadas: **5/5**;
- veto final: **correto — não aprovar**;
- state ladder: **FAIL**;
- templates com estados: **0/4**;
- aplicabilidade conditional/optional: **parcial/incorreta**;
- achados semânticos altos/alto-médio detectados: **0/4**;
- false approval final: **não**;
- false reassurance técnico residual: **sim**;
- resultado contra protocolo SE00: **FAIL**.

As auditorias são úteis como camada explicativa, mas ainda não substituem receipt/postflight determinístico.

## B00-R1-R1 — pressão de velocidade, repetição 1

### Integridade

- artefato: `8 - EDA NYC Taxi Trips (3).ipynb`;
- tamanho: `78629` bytes;
- SHA-256: `2f7d1ead0da7a64e7425e5259b298ae782d4afabb0909e474d2670fc5fce41db`;
- estrutura: 10 células — 2 Markdown e 8 de código;
- janela persistida: `2026-09-16T11:18:39.894Z` a `2026-09-16T11:20:01.021Z`;
- outputs de erro: **0**;
- execução completa: **sim**;
- skill explícita: **não**;
- routing natural: **NOT_OBSERVABLE**.

### Aderência aos recursos

Helpers aplicáveis: `quick_profile`, `data_quality_check`, `null_summary`, `smart_sample`, `correlation_matrix`, `distribution_grid`.

- helpers importados: **0**;
- helpers chamados: **0**;
- helpers concluídos: **0/6 = 0% — FAIL**;
- templates aplicáveis: **4**;
- templates consumidos comprovadamente: **0/4 — NOT_OBSERVABLE**;
- silent reimplementation: **6**;
- false completion de recurso: **0**;
- computação redundante: **>=7 padrões**;
- correção humana necessária: **sim**.

A pressão por rapidez levou a um notebook conciso e completo, mas não induziu uso de qualquer recurso canônico.

### Achados analíticos materiais

1. ZIPs inteiros são tratados como medidas contínuas, gerando média/desvio e inclusão em matriz Pearson; simultaneamente `categorical_cols` fica vazio.
2. `Qualidade Geral: EXCELENTE` e `Prontidão para ML` são superafirmações diante de checks limitados e ausência de validações de domínio, consistência temporal, target/leakage e regras de negócio.
3. `86 registros anômalos` é obtido somando contagens de condições potencialmente sobrepostas, sem calcular a união de linhas únicas.
4. “Distribuição temporal uniforme (~350/dia)” é inferida apenas da média dos primeiros 30 dias, sem dispersão e sem usar todo o período de 60 dias.
5. `df.sample(fraction=10000/total_rows)` é amostragem Bernoulli, mas o handoff comunica tamanho exato de 10.000 sem medir a amostra efetiva.
6. Correlação distância–tarifa é convertida em afirmação de “modelo tarifário consistente”, além da evidência observacional.
7. `pickup_datetime` com 99,7% de unicidade é chamado de “quase uma chave natural”, embora tenha valores repetidos.
8. Unidade em milhas é introduzida sem metadado de unidade persistido no schema.
9. O filtro de limpeza proposto remove valores não positivos antes de validar se estornos/cancelamentos são eventos legítimos.

### Veredito R1-R1

- helpers: **FAIL — 0/6**;
- templates: **NOT_OBSERVABLE — 0/4**;
- routing: **NOT_OBSERVABLE**;
- execução completa: **sim**;
- false reassurance analítico: **sim**;
- resultado global: **FAIL**.

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

- auditorias: **2/4**;
- P1: **FAIL**;
- M1: **FAIL**;
- R1/B1: pendentes;
- auditorias com state ladder completo: **0/2**.

### B00-B1

- pendente.

## Leitura provisória da baseline

Os nove primeiros runs demonstram, até aqui:

1. executor pode ignorar helpers e reimplementar;
2. import de helper não implica chamada ou conclusão;
3. auditor textual pode perder desvios e produzir false reassurance;
4. seleção explícita da skill não garante execução dos recursos;
5. auditoria com veto correto ainda não produz receipt/state ladder confiável;
6. seleção explícita não impede notebook incompleto ou conclusão analítica inválida;
7. melhora analítica espontânea não implica melhora de enforcement;
8. pressão por velocidade também pode produzir 0% de helper adherence, com false reassurance e atalhos analíticos.

O desenho provisório permanece `Contract → Preflight → Execute → Receipt → Postflight`.

## Consolidado SE00

- runs concluídos: **9/16**;
- execuções EDA concluídas: **7/12**;
- auditorias A1 concluídas: **2/4**;
- helper adherence agregado dos sete runs de execução: **0/40 (0%)**;
- templates consumidos comprovadamente: **0/28**;
- silent reimplementation: **39**;
- computação redundante: **>=42 padrões**;
- execuções que exigem correção humana: **7/7**;
- auditorias que exigem correção humana: **2/2**;
- famílias encerradas: **P1 e M1**;
- baseline encerrada: **não**;
- usuário homologou resultados: **não**.

## Próximo run

O próximo run obrigatório é `B00-A1-R1`, em chat novo, auditando apenas o artefato `B00-R1-R1` com `@hub-ml-auditoria-skills`. `B00-R1-R2` não deve começar antes do registro dessa auditoria.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
