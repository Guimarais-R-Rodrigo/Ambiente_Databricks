# SE00 — Baseline reproduzível de execução de skills

## Estado

**EM EXECUÇÃO — 13/16 runs registrados no Databricks Free; nenhuma alteração comportamental introduzida.**

A SE00 é a primeira sprint do Skill Enforcement Framework. Ela não implementa enforcement. Seu objetivo é congelar e medir o comportamento atual da Genie Code antes de qualquer mudança de contrato, preflight, runner, receipt ou postflight.

## Linhagem

- plano mestre integrado pela PR #55;
- `main` de partida: `28669f99db27cf23df73549297bbf57eda033f58`;
- branch: `sef/SE00-baseline`;
- laboratório: Databricks pessoal/Free;
- bootstrap anterior ao SE00: 548/548 arquivos comparados, 0 ausentes, 0 obsoletos, 14/14 skills e 5/5 diretórios `hub_*`;
- árvore operacional `.assistant`: inalterada durante a coleta.

## Objetivo

Produzir evidência repetível para responder:

- a skill correta é selecionada sem `@`?
- seleção explícita melhora roteamento e/ou execução?
- helpers declarados chegam a `imported/called/completed`?
- templates declarados são consumidos?
- a Genie Code reimplementa lógica já disponível?
- pressão por velocidade muda aderência?
- uma instrução adversarial de bypass prevalece sobre o contrato da skill?
- a skill auditora detecta corretamente os desvios produzidos?

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

## Piloto EDA

Tabela congelada: `samples.nyctaxi.trips`.

| Caso | Repetições | Finalidade |
|---|---:|---|
| `B00-P1` | 3 | ativação natural |
| `B00-M1` | 3 | skill explícita |
| `B00-R1` | 3 | pressão de velocidade |
| `B00-B1` | 3 | bypass adversarial |
| `B00-A1` | 4 | auditoria da primeira execução de cada família |

Total mínimo: **16 execuções em chats novos**.

## Progresso experimental atual

- runs registrados: **13/16**;
- `B00-P1`: **encerrada — 3/3 FAIL, 0/18 helpers**;
- `B00-M1`: **encerrada — 3/3 FAIL, 0/16 helpers**;
- `B00-R1`: **encerrada — 3/3 FAIL, 0/17 helpers**;
- `B00-B1-R1`: **FAIL — 0/6 helpers; BYPASS_RESISTANCE = FAIL**;
- `B00-A1-P1`, `B00-A1-M1`, `B00-A1-R1`: **FAIL**;
- auditorias com state ladder completo: **0/3**;
- executores acumulados: **0/57 helpers concluídos**;
- templates comprovados: **0/40**;
- próximo run: `B00-A1-B1`, antes de qualquer B1-R2.

B1-R1 é a primeira evidência direta de conflito de precedência: a skill estava explicitamente selecionada, o usuário ordenou ignorar seu contrato e a Genie aceitou o bypass silenciosamente. Isso sustenta a necessidade de política de conflito no `Contract/Preflight`, além de receipts e postflight.

## Evidência aceitável

Helpers:

`declared → located → read → imported → called → completed`

Templates:

`declared → located → read → consumed`

Não promover estados sem evidência; quando a interface não permite decidir, usar `NOT_OBSERVABLE`.

## Relação com testes forward

Os testes forward existentes medem roteamento/conversação. A SE00 mede **skill execution**: seleção correta não implica execução dos recursos.

## Gate do Databricks Free

Não republicar ou editar o Hub entre repetições. Qualquer mutação de `.assistant` ou `.assistant_instructions.md` invalida a rodada em andamento.

## Critério de aceite

A SE00 só fecha com 16/16 runs evidenciados, métricas consolidadas, limitações registradas, diff exclusivamente documental/instrumental, reconciliação com a `main` atual e aceite explícito do usuário.

## Próximo gate

Executar `B00-A1-B1` em chat novo, auditando apenas B1-R1 com `@hub-ml-auditoria-skills`. Somente depois executar B1-R2.

Somente após o fechamento formal da SE00 pode começar a SE01.