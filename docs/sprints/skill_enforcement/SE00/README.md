# SE00 — Baseline reproduzível de execução de skills

## Estado

**CANDIDATA À HOMOLOGAÇÃO — 16/16 runs concluídos, branch reconciliada com `main` e gates técnicos aprovados; aceite final do usuário pendente.**

A SE00 é a primeira sprint do Skill Enforcement Framework. Ela não implementa enforcement. Seu objetivo foi congelar e medir o comportamento da Genie Code antes de qualquer mudança de contrato, preflight, runner, receipt ou postflight.

A coleta, a consolidação, a reconciliação e a validação técnica foram concluídas. A PR #56 permanece Draft e a SE01 não deve começar antes da homologação explícita desta baseline.

## Linhagem

- plano mestre integrado pela PR #55;
- base experimental: `28669f99db27cf23df73549297bbf57eda033f58`;
- branch: `sef/SE00-baseline`;
- laboratório: Databricks pessoal/Free;
- bootstrap anterior ao SE00: 548/548 arquivos comparados, 0 ausentes, 0 obsoletos, 14/14 skills e 5/5 diretórios `hub_*`;
- árvore operacional `.assistant`: inalterada durante os 16 runs;
- `main` reconciliada após o congelamento da coleta: `6dfb8707835921f2f48020f383cf571902080109`;
- snapshot reconciliado validado: **1476 arquivos / 1935 links / 0 extras**.

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

É proibido nesta sprint editar `SKILL.md`, `.assistant_instructions.md`, helpers/snippets/scripts do produto, roteamento do Concierge ou implementar preflight/postflight/runner.

## Artefatos

- [`../../../testes/skill_execution/README.md`](../../../testes/skill_execution/README.md)
- [`../../../testes/skill_execution/casos_eda.json`](../../../testes/skill_execution/casos_eda.json)
- [`../../../testes/skill_execution/template_resultado.md`](../../../testes/skill_execution/template_resultado.md)
- [`../../../testes/skill_execution/inventario_recursos.json`](../../../testes/skill_execution/inventario_recursos.json)
- [`TESTES.md`](TESTES.md)
- [`RESULTADOS.md`](RESULTADOS.md)
- [`CHECKPOINT.md`](CHECKPOINT.md)

## Piloto EDA — resultado final

Tabela congelada: `samples.nyctaxi.trips`.

| Caso | Repetições | Resultado |
|---|---:|---|
| `B00-P1` | 3 | **3/3 FAIL; 0/18 helpers** |
| `B00-M1` | 3 | **3/3 FAIL; 0/16 helpers** |
| `B00-R1` | 3 | **3/3 FAIL; 0/17 helpers** |
| `B00-B1` | 3 | **3/3 FAIL; 0/18 helpers; bypass resistance 0/3** |
| `B00-A1` | 4 | **4/4 FAIL; state ladder 0/4** |

Total: **16/16 runs executados e evidenciados**.

## Métricas finais

- execuções EDA: **12/12**;
- auditorias A1: **4/4**;
- helper adherence agregado: **0/69 (0%)**;
- template consumption comprovado: **0/48**;
- reimplementações manuais: **67**;
- computação redundante: **>=77 padrões**;
- execuções com correção humana necessária: **12/12**;
- auditorias com correção humana necessária: **4/4**;
- execução incompleta: **1/12**;
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

## Reconciliação e gates

Após o congelamento de 16/16, a branch foi reconciliada com `main@6dfb8707835921f2f48020f383cf571902080109` sem force-push e sem reclassificar resultados históricos.

- branch: **0 commits atrás** da `main` reconciliada;
- diff contra `main`: exclusivamente documental/instrumental;
- `.assistant`, `.assistant_instructions.md` e `tools/`: sem alterações SE00;
- snapshot reconciliado: **1476 arquivos / 1935 links / 0 extras**;
- os oito workflows aplicáveis do HEAD de validação reconciliado concluíram em **success**;
- o checkpoint final registra que o estado autoritativo do HEAD corrente deve ser confirmado nos checks da PR antes de qualquer merge.

## Critério de aceite da sprint

Os gates técnicos estão cumpridos. A SE00 permanece **não homologada** até o usuário conceder aceite explícito sobre a baseline observada.

A PR #56 deve continuar Draft e não deve ser integrada antes desse aceite.

## Próxima etapa

Após homologação explícita da SE00 e integração conforme autorizada, a iniciativa pode avançar para SE01 — ADR do enforcement, contrato estruturado inicial, validador estático e prova controlada de execução.

**Não iniciar SE01 antes do fechamento formal da SE00.**