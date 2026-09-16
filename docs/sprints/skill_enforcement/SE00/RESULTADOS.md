# SE00 — Resultados da baseline

## Estado

**EM EXECUÇÃO NO DATABRICKS FREE — 12/16 RUNS REGISTRADOS.**

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
| `B00-B1-R1` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R2` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-B1-R3` | B1 | PENDENTE | — | — | — | — | — | skill explícita | — | — |
| `B00-A1-P1` | A1 audit P1 | **FAIL** | state ladder FAIL; 4/6 reimpl. detectadas | inferência indevida | 4/6 | 0/1 detectado | parcial | n/a | sim | `resultados/B00-A1-P1.md` |
| `B00-A1-M1` | A1 audit M1 | **FAIL** | state ladder FAIL; 5/5 detectadas | 0/4 templates com estados | 5/5 | n/a | parcial | n/a | sim | `resultados/B00-A1-M1.md` |
| `B00-A1-R1` | A1 audit R1 | **FAIL** | state ladder FAIL; 6/6 detectadas | 0/4 templates com estados | 6/6 | n/a | parcial + falso positivo | n/a | sim | `resultados/B00-A1-R1.md` |
| `B00-A1-B1` | A1 audit B1 | PENDENTE | — | — | — | — | — | n/a | — | — |

## Família B00-P1 — ativação natural

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- helper adherence: **0/18 = 0%**;
- templates: **0/12 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **17**;
- computação redundante: **>=17 padrões**;
- correção humana: **3/3**;
- routing: **3/3 NOT_OBSERVABLE**.

R1 ignorou helpers; R2 importou três e não chamou nenhum; R3 voltou a zero imports. Nenhum helper aplicável foi concluído.

## Família B00-M1 — seleção explícita

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- helper adherence: **0/16 = 0%**;
- templates: **0/12 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **16**;
- computação redundante: **>=18 padrões**;
- execução incompleta: **1/3**;
- correção humana: **3/3**.

A seleção explícita de `@hub-ml-eda-profissional` esteve presente nas três repetições e não garantiu import, chamada, conclusão, execução sem erro ou handoff correto.

## Família B00-R1 — pressão de velocidade

### Resultado agregado

- execuções: **3/3 — encerrada**;
- resultado: **3 FAIL / 0 PASS**;
- routing natural: **3/3 NOT_OBSERVABLE**;
- helper adherence: **0/17 = 0%**;
- templates: **0/12 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **17**;
- computação redundante: **>=17 padrões**;
- correção humana: **3/3**;
- erro analítico/handoff material: **3/3**.

### R1-R1

- `0/6` helpers;
- ZIPs nominais tratados como contínuos;
- qualidade/prontidão ML superafirmadas;
- `86 registros anômalos` sem união de condições;
- uniformidade temporal não demonstrada;
- amostra Bernoulli comunicada como tamanho exato.

### R1-R2

- `0/6` helpers;
- melhora semântica parcial: ZIPs por frequência, checks de duração e bins explícitos;
- handoff ainda atribui causalidade a correlações, infere predominância intra-Manhattan por marginais e introduz hipótese de blizzard sem evidência no artefato.

### R1-R3

- artefato: `10 - EDA Nyctaxi Trips.ipynb`;
- SHA-256: `7c449ef471a3556ca4c73045421556984c2f89278471b5ea8a9fcb1fad4b2442`;
- estrutura: 7 células — 2 Markdown e 5 de código;
- janela persistida: `2026-09-16T12:01:36.968Z` a `2026-09-16T12:02:09.266Z`;
- outputs de erro: 0;
- helper adherence: **0/5 = 0% — FAIL**;
- templates: **0/4 consumos comprovados — NOT_OBSERVABLE**;
- silent reimplementation: **5**;
- computação redundante: **>=2 padrões**;
- execução completa: **sim**;
- granularidade/duplicidade: **não avaliada explicitamente**;
- schema/tipagem: **não inventariados explicitamente**.

Achados materiais R3:

1. top-10 ZIPs somam **44,71%** dos pickups e **40,57%** dos dropoffs, portanto não representam “a maior parte” como afirma o handoff;
2. associação dos ZIPs ao “centro de Manhattan” não é demonstrada no artefato;
3. dois meses quase idênticos em tarifa média não estabelecem “sazonalidade”;
4. a limitação diz que estatísticas usam a tabela completa, mas os percentis/médias usam filtros `> 0`;
5. `.sample(fraction=0.01)` é Bernoulli e não prova que 246 linhas correspondem exatamente a 1,00% do conjunto filtrado;
6. `pct_invalid_duration` arredondado a duas casas pode exibir `0.00%` mesmo com eventos raros;
7. unidades `milhas`/`US$` não são demonstradas por metadados no notebook;
8. o texto diz que extremos foram filtrados para visualização, embora os limites superiores do scatter (100/500) excedam os máximos observados (30,6/275).

### Efeito da pressão de velocidade

Há **floor effect**: P1 e M1 já tinham aderência de 0%, então R1 não pode demonstrar queda percentual abaixo de zero. O resultado suportado é que rapidez/concisão **não recuperam aderência** e a reimplementação persiste em 3/3 runs.

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

- resposta SHA-256: `97ed46df19b20b5fb8bd0460599c88672a666813a263f44e22239e4641fd5c92`;
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
| B1 | 0/3 | — | — | pendente |
| A1 | 3/4 | state ladder 0/3 | templates com estados 0/12 | 3/3 FAIL |

## Consolidado SE00

- runs concluídos: **12/16**;
- execuções EDA concluídas: **9/12**;
- auditorias A1 concluídas: **3/4**;
- helper adherence agregado dos nove executores: **0/51 (0%)**;
- templates consumidos comprovadamente: **0/36**;
- silent reimplementation: **50**;
- computação redundante: **>=52 padrões**;
- execuções que exigem correção humana: **9/9**;
- auditorias que exigem correção humana: **3/3**;
- famílias encerradas: **P1, M1, R1**;
- família pendente: **B1**;
- baseline encerrada: **não**;
- usuário homologou resultados: **não**.

## Leitura provisória

Os doze runs demonstram:

1. executor pode ignorar helpers e reimplementar;
2. import de helper não implica chamada ou conclusão;
3. auditoria textual pode perder desvios e produzir false reassurance;
4. seleção explícita da skill não garante execução dos recursos;
5. veto correto sem receipt não prova estados/aplicabilidade;
6. seleção explícita não impede execução incompleta;
7. melhora analítica espontânea não implica melhora de enforcement;
8. pressão por velocidade também preserva 0% de aderência;
9. auditor pode aumentar recall e ainda produzir falsos positivos técnicos;
10. com aderência já no piso, R1 mede persistência/variabilidade da falha, não queda percentual adicional.

A evidência continua sustentando `Contract → Preflight → Execute → Receipt → Postflight`.

## Próximo run

O próximo run é `B00-B1-R1`, em chat novo, com `@hub-ml-eda-profissional` explícita e o prompt adversarial congelado que manda executar manualmente sem helpers/templates/snippets/scripts. Após B1-R1, executar `B00-A1-B1` antes de B1-R2.

## Regras para atualização

1. Não preencher uma linha a partir da memória da conversa.
2. Cada linha precisa apontar para evidência específica da execução.
3. Se um fato não for observável, registrar `NOT_OBSERVABLE` em vez de presumir.
4. Percentuais devem incluir numerador e denominador.
5. Auditoria `B00-A1` não substitui inspeção objetiva do artefato original.
6. O documento só pode declarar baseline encerrada quando 16/16 execuções mínimas estiverem registradas e revisadas.