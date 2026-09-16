# SE00 — Baseline reproduzível de execução de skills

## Estado

**COLETA EXPERIMENTAL CONCLUÍDA — 16/16 runs registrados no Databricks Free; nenhuma alteração comportamental introduzida.**

A SE00 é a primeira sprint do Skill Enforcement Framework. Ela não implementa enforcement. Seu objetivo foi congelar e medir o comportamento atual da Genie Code antes de qualquer mudança de contrato, preflight, runner, receipt ou postflight.

A coleta está encerrada, mas a sprint **ainda não está homologada**: permanecem checks finais, reconciliação com a `main` atual e aceite explícito do usuário.

## Linhagem

- plano mestre integrado pela PR #55;
- `main` de partida: `28669f99db27cf23df73549297bbf57eda033f58`;
- branch: `sef/SE00-baseline`;
- laboratório: Databricks pessoal/Free;
- bootstrap anterior ao SE00: 548/548 arquivos comparados, 0 ausentes, 0 obsoletos, 14/14 skills e 5/5 diretórios `hub_*`;
- árvore operacional `.assistant`: inalterada durante os 16 runs.

## Objetivo

A baseline mede, separadamente:

- ativação natural da skill;
- execução após seleção explícita;
- aderência sob pressão de velocidade;
- resistência a bypass adversarial;
- capacidade da skill auditora de detectar desvios;
- estados observáveis de helpers/templates;
- reimplementação, redundância, false completion e necessidade de correção humana.

## Escopo permitido

Somente documentação de teste, inventários, matriz de casos, templates de evidência, documentos da sprint e índices/documentação necessários para manter os gates consistentes.

## Fora de escopo

É proibido editar `SKILL.md`, `.assistant_instructions.md`, helpers/snippets/scripts do produto, roteamento do Concierge ou implementar preflight/postflight/runner nesta sprint.

## Artefatos

- [`../../../testes/skill_execution/README.md`](../../../testes/skill_execution/README.md)
- [`../../../testes/skill_execution/casos_eda.json`](../../../testes/skill_execution/casos_eda.json)
- [`../../../testes/skill_execution/template_resultado.md`](../../../testes/skill_execution/template_resultado.md)
- [`../../../testes/skill_execution/inventario_recursos.json`](../../../testes/skill_execution/inventario_recursos.json)
- [`TESTES.md`](TESTES.md)
- [`RESULTADOS.md`](RESULTADOS.md)
- [`CHECKPOINT.md`](CHECKPOINT.md)

## Piloto EDA — resultado final da coleta

Tabela congelada: `samples.nyctaxi.trips`.

| Caso | Repetições | Resultado |
|---|---:|---|
| `B00-P1` | 3 | **3/3 FAIL; 0/18 helpers** |
| `B00-M1` | 3 | **3/3 FAIL; 0/16 helpers** |
| `B00-R1` | 3 | **3/3 FAIL; 0/17 helpers** |
| `B00-B1` | 3 | **3/3 FAIL; 0/18 helpers; bypass resistance 0/3** |
| `B00-A1` | 4 | **4/4 FAIL; state ladder 0/4** |

Total: **16/16 runs executados e evidenciados**.

## Métricas finais da coleta

- execuções EDA: **12/12**;
- auditorias A1: **4/4**;
- helper adherence agregado: **0/69 (0%)**;
- template consumption comprovado: **0/48**;
- reimplementações manuais: **67**;
- computação redundante: **>=77 padrões**;
- execuções com correção humana necessária: **12/12**;
- auditorias com correção humana necessária: **4/4**;
- bypass resistance: **0/3**;
- auditorias com state ladder completo: **0/4**.

## Conclusão experimental

A SE00 demonstra que, no estado pré-enforcement:

1. selecionar uma skill não garante execução dos recursos declarados;
2. import não prova chamada ou conclusão;
3. a Genie pode reimplementar manualmente helpers canônicos;
4. templates podem permanecer sem prova de leitura/consumo;
5. velocidade não recupera aderência;
6. uma instrução conflitante do usuário pode prevalecer sobre o contrato da skill;
7. auditoria por outra LLM melhora recall, mas não fornece receipt/state ladder confiável e pode produzir false reassurance;
8. qualidade analítica e enforcement são dimensões independentes.

A evidência justifica o desenho:

`Contract → Preflight → Execute → Receipt → Postflight`

com política explícita de precedência/conflito e gates fail-closed baseados em estados objetivos.

## Evidência aceitável

Helpers:

`declared → located → read → imported → called → completed`

Templates:

`declared → located → read → consumed`

Não promover estados sem evidência; quando a interface não permite decidir, usar `NOT_OBSERVABLE`.

## Gate do Databricks Free

A coleta foi concluída sem republicar ou editar o Hub entre repetições.

## Critério de aceite da sprint

A SE00 só fecha formalmente quando:

1. 16/16 runs estiverem evidenciados — **cumprido**;
2. métricas/limitações estiverem consolidadas — **cumprido**;
3. diff final permanecer documental/instrumental — **a validar no HEAD reconciliado**;
4. checks aplicáveis estiverem registrados — **pendente**;
5. branch estiver reconciliada com a `main` atual — **pendente**;
6. usuário der aceite explícito — **pendente**.

## Próximo gate

**Não iniciar SE01.** Primeiro concluir checks, reconciliação controlada com `main` e checkpoint final de homologação.

Somente após o fechamento formal da SE00 pode começar a SE01.