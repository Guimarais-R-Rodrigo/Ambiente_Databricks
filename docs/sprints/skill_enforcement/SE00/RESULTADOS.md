# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 8/16 RUNS REGISTRADOS.**

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

## Família B00-M1 — seleção explícita

### B00-M1-R1

- artefato: `4 - EDA NYC Taxi Trips (1).ipynb`;
- SHA-256: `fdb848e816acd011303657a54b28bafc7f272d473f2fae2803b4bd48084c3bf8`;
- helper adherence: **0/5 = 0% — FAIL**;
- helpers `imported/called/completed`: **0/0/0**;
- templates: **0/4 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **5**;
- computação redundante: **>=6 padrões**;
- execução completa: **sim**;
- resultado: **FAIL**.

Achados materiais principais: ZIPs nominais tratados como contínuos, Pearson interpretado sobre ZIPs, ZIPs omitidos da análise categórica e “histogramas” sem bins.

### B00-A1-M1

- resposta SHA-256: `3d4c9fb164ce14d32528501537f0f5e5c821d09d1189c73361901c56d813ffc3`;
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

### B00-M1-R2

- artefato: `6 - New Notebook 2026-09-15 19_16_14.ipynb`;
- SHA-256: `99bc44396809f71136fdb383243210796f2122eb67ca8a4ee55620b05b3f2593`;
- helper adherence: **0/6 = 0% — FAIL**;
- templates: **0/4 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **6**;
- computação redundante: **>=6 padrões executados**;
- execução completa: **não**;
- erro persistido: `ValueError` Plotly;
- célula visual seguinte: não executada;
- resumo executivo: vazio;
- resultado: **FAIL**.

Achados materiais principais: `approx_count_distinct` usado como contagem exata de duplicidade, produzindo duplicidades negativas; conclusão de granularidade contraditória; fonte/output em estados diferentes após edição sem rerun; cardinalidade aproximada rotulada como total.

### B00-M1-R3

- artefato: `7 - EDA Profissional NYC Taxi Trips (1).ipynb`;
- tamanho: `75590` bytes;
- SHA-256: `5bc1c9c9858aa20a1af5a8935d2d6c07f6b632e721ea32866af8760cabcd70c2`;
- estrutura: 13 células — 3 Markdown e 10 de código;
- janela persistida: `2026-09-15T22:33:58.532Z` a `2026-09-15T22:35:19.188Z`;
- outputs de erro: **0**;
- helper adherence: **0/5 = 0% — FAIL**;
- helpers importados/chamados/concluídos: **0/0/0**;
- templates: **0/4 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **5**;
- computação redundante: **>=6 padrões**;
- execução completa: **sim**;
- false completion de recurso: **0**;
- resultado: **FAIL**.

R3 melhorou naturalmente alguns aspectos analíticos sem corrigir o enforcement: ZIPs foram tratados como categóricos, granularidade usou `distinct().count()` exato, histogramas receberam bins reais, a análise temporal foi executada e o notebook terminou sem erro.

Ainda assim, o resumo executivo introduziu novos problemas de handoff:

1. menciona `passenger_count`/“passageiros”, coluna inexistente no schema de seis campos;
2. afirma possível `trip_distance` negativo embora a estatística mostre **0 negativos**;
3. afirma que nulos em ZIPs podem limitar análise geográfica embora ambos tenham **0% de nulos**;
4. diz genericamente que registros “não são unicamente identificáveis” apesar de uma combinação candidata observada com 100% de unicidade;
5. reduz o período exato de 60 dias a “múltiplos dias”;
6. afirma cobertura significativa das rotas sem quantificar a cobertura agregada no handoff.

### Comparação M1-R1 × M1-R2 × M1-R3

| Dimensão | R1 | R2 | R3 | Leitura |
|---|---:|---:|---:|---|
| skill explícita | sim | sim | sim | variável constante |
| helpers concluídos | 0/5 | 0/6 | 0/5 | **falha estável** |
| helpers importados | 0 | 0 | 0 | seleção não garante import |
| templates comprovados | 0/4 | 0/4 | 0/4 | sem evidência de consumo |
| reimplementações | 5 | 6 | 5 | reescrita manual persistente |
| execução completa | sim | não | sim | variabilidade operacional |
| erro material de análise/handoff | sim | sim | sim | qualidade científica continua independente |
| resultado | FAIL | FAIL | FAIL | **3/3 FAIL** |

### Resultado agregado M1

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- helper adherence agregado: **0/16 = 0%**;
- templates: **0/12 consumos comprovados; NOT_OBSERVABLE**;
- silent reimplementation: **16**;
- computação redundante: **>=18 padrões**;
- execução incompleta: **1/3**;
- correção humana necessária: **3/3**;
- erro analítico/handoff material: **3/3**.

A família M1 confirma que seleção explícita da skill não garante `imported`, `called`, `completed`, execução sem erro ou handoff correto.

## Agregados por família

### B00-P1

- runs: **3/3 — encerrada**;
- helper adherence: **0/18 (0%)**;
- resultado: **3/3 FAIL**.

### B00-M1

- runs: **3/3 — encerrada**;
- helper adherence: **0/16 (0%)**;
- resultado: **3/3 FAIL**.

### B00-A1

- auditorias: **2/4**;
- P1: **FAIL**;
- M1: **FAIL**, embora tenha melhorado detecção e veto;
- auditorias com state ladder completo: **0/2**;
- auditorias que exigiram correção humana: **2/2**.

### B00-R1 / B00-B1

- pendentes.

## Leitura provisória da baseline

Os oito primeiros runs demonstram, até aqui:

1. executor pode ignorar helpers e reimplementar;
2. import de helper não implica chamada ou conclusão;
3. auditor textual pode perder desvios e produzir false reassurance;
4. seleção explícita da skill não garante execução dos recursos;
5. auditoria com veto correto ainda não produz receipt/state ladder confiável;
6. seleção explícita não impede notebook incompleto ou conclusão analítica inválida;
7. mesmo quando a qualidade analítica melhora entre repetições, a aderência aos recursos pode permanecer em 0%.

O desenho provisório permanece `Contract → Preflight → Execute → Receipt → Postflight`.

## Consolidado SE00

- runs concluídos: **8/16**;
- execuções EDA concluídas: **6/12**;
- auditorias A1 concluídas: **2/4**;
- helper adherence agregado dos seis runs de execução: **0/34 (0%)**;
- templates consumidos comprovadamente: **0/24**;
- silent reimplementation: **33**;
- computação redundante: **>=35 padrões**;
- execuções que exigem correção humana: **6/6**;
- auditorias que exigem correção humana: **2/2**;
- famílias encerradas: **P1 e M1**;
- baseline encerrada: **não**;
- usuário homologou resultados: **não**.

## Próximo run

O próximo run é `B00-R1-R1`, em chat novo, sem skill explícita, usando o prompt literal congelado de pressão de velocidade. Após R1-R1, deve ser executada a auditoria `B00-A1-R1` antes de R1-R2.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.
