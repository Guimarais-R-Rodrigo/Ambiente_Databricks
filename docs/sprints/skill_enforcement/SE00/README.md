# SE00 — Baseline reproduzível de execução de skills

## Estado

**ENCERRADA / HOMOLOGADA / INTEGRADA — 16/16 runs concluídos, PR #56 integrada na `main` e auditoria pós-merge concluída em 16/09/2026.**

A SE00 é a primeira sprint do Skill Enforcement Framework. Ela não implementa enforcement. Seu objetivo foi congelar e medir o comportamento da Genie Code antes de qualquer mudança de contrato, preflight, runner, receipt ou postflight.

A homologação aceita a baseline observada como evidência do estado pré-enforcement. Os resultados `FAIL` não foram convertidos em `PASS`; eles constituem a evidência empírica que justifica as sprints seguintes do SEF.

## Linhagem e fechamento

- plano mestre SEF integrado pela PR #55;
- base experimental congelada: `28669f99db27cf23df73549297bbf57eda033f58`;
- ambiente de coleta: Databricks pessoal/Free;
- coleta executada sem republicar ou alterar o Hub entre os 16 runs;
- branch de coleta: `sef/SE00-baseline`;
- última `main` reconciliada antes da integração: `62e9404851d6a7902371bd5b6531a113d521311c`;
- HEAD final da candidata integrada: `4379080a46781a543d8f7933d61c1d024076c096`;
- PR #56: integrada em `main` pelo merge commit `3341f58a8ebffac8b3f0f8837c7d0d6f8aa0b245`;
- auditoria pós-merge: **15/15 workflows de `push` concluídos em `success`**;
- snapshot final validado na `main`: **1480 arquivos / 1957 links / 0 extras**;
- `.assistant`, `.assistant_instructions.md` e helpers/snippets/scripts do produto: **sem alterações comportamentais pela SE00**;
- SE01: **não iniciada neste fechamento**.

## Objetivo experimental

A baseline mediu separadamente:

- ativação natural da skill;
- execução após seleção explícita;
- aderência sob pressão de velocidade;
- resistência a bypass adversarial;
- capacidade da skill auditora de detectar desvios;
- estados observáveis de helpers/templates;
- reimplementação, redundância, false completion e necessidade de correção humana.

## Artefatos canônicos

- [`../../../testes/skill_execution/README.md`](../../../testes/skill_execution/README.md)
- [`../../../testes/skill_execution/casos_eda.json`](../../../testes/skill_execution/casos_eda.json)
- [`../../../testes/skill_execution/template_resultado.md`](../../../testes/skill_execution/template_resultado.md)
- [`../../../testes/skill_execution/inventario_recursos.json`](../../../testes/skill_execution/inventario_recursos.json)
- [`TESTES.md`](TESTES.md)
- [`RESULTADOS.md`](RESULTADOS.md)
- [`CHECKPOINT.md`](CHECKPOINT.md)

`TESTES.md` e `RESULTADOS.md` preservam o registro técnico da candidata e dos 16 runs. Este README e `CHECKPOINT.md` registram o estado de governança pós-merge.

## Resultado final da baseline

Tabela congelada: `samples.nyctaxi.trips`.

| Família | Resultado | Helpers concluídos | Templates comprovados |
|---|---|---:|---:|
| `B00-P1` | **3/3 FAIL** | 0/18 | 0/12 |
| `B00-M1` | **3/3 FAIL** | 0/16 | 0/12 |
| `B00-R1` | **3/3 FAIL** | 0/17 | 0/12 |
| `B00-B1` | **3/3 FAIL; bypass resistance 0/3** | 0/18 | 0/12 |
| `B00-A1` | **4/4 FAIL; state ladder 0/4** | n/a | 0/16 com state ladder |

Consolidado:

- runs: **16/16**;
- executores EDA: **12/12**;
- auditorias A1: **4/4**;
- helper adherence dos executores: **0/69 (0%)**;
- template consumption comprovado: **0/48**;
- reimplementações manuais: **67**;
- computação redundante: **>=77 padrões**;
- false completion de recurso/workflow: **3 ocorrências observadas**;
- execução incompleta: **1/12**;
- correção humana: **12/12 executores + 4/4 auditorias**;
- auditorias com state ladder completo: **0/4**;
- bypass resistance: **0/3**.

## Conclusão de engenharia

A baseline demonstra que, no estado pré-enforcement:

1. seleção natural ou explícita de skill não garante execução dos recursos canônicos;
2. import não prova chamada nem conclusão;
3. helpers podem ser reimplementados silenciosamente;
4. templates podem permanecer sem prova de leitura/consumo;
5. pressão por velocidade não recupera aderência;
6. instruções conflitantes do usuário podem prevalecer sobre o contrato da skill;
7. auditoria textual por outra LLM pode melhorar recall, mas não substitui receipt/state ladder verificável;
8. qualidade analítica e enforcement são dimensões independentes.

A evidência justifica a arquitetura:

`Contract → Preflight → Execute → Receipt → Postflight`

com política explícita de precedência/conflito, execução determinística quando aplicável, estados machine-readable e gates fail-closed.

## Observabilidade

Helpers seguem a escada:

`declared → located → read → imported → called → completed`

Templates seguem:

`declared → located → read → consumed`

Quando a interface não permite decidir, o estado permanece `NOT_OBSERVABLE`; ausência de telemetria não é promovida a `PASS`.

## Gate final da SE00

- [x] 16/16 runs documentados;
- [x] métricas e limitações consolidadas;
- [x] evidências históricas preservadas;
- [x] diff da candidata revisado como documental/instrumental;
- [x] branch reconciliada com a `main` vigente antes do merge;
- [x] snapshot final validado: 1480/1957/0 extras;
- [x] 8/8 workflows de PR do HEAD final em `success`;
- [x] homologação explícita do usuário;
- [x] PR #56 integrada;
- [x] `main` pós-merge auditada;
- [x] 15/15 workflows de `push` pós-merge em `success`.

## Próxima etapa

A SE00 está formalmente encerrada na `main`.

A próxima sprint prevista é a SE01 — ADR do enforcement, contrato estruturado inicial, validador estático e prova controlada de execução — mas **não foi iniciada neste fechamento**.