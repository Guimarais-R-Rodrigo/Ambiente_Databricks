# SE00 — Baseline reproduzível de execução de skills

## Estado

**HOMOLOGADA — 16/16 runs concluídos, branch reconciliada com `main`, gates técnicos aprovados e integração da PR #56 autorizada pelo usuário em 16/09/2026.**

A SE00 é a primeira sprint do Skill Enforcement Framework. Ela não implementa enforcement. Seu objetivo foi congelar e medir o comportamento da Genie Code antes de qualquer mudança de contrato, preflight, runner, receipt ou postflight.

A coleta, a consolidação, a reconciliação e a validação técnica foram concluídas. A homologação aceita a baseline observada — inclusive os resultados FAIL que justificam o SEF — e não os reclassifica como PASS. A SE01 permanece fora deste ato e só pode começar depois da auditoria pós-merge da `main`.

## Linhagem

- plano mestre integrado pela PR #55;
- base experimental: `28669f99db27cf23df73549297bbf57eda033f58`;
- branch: `sef/SE00-baseline`;
- laboratório: Databricks pessoal/Free;
- bootstrap anterior ao SE00: 548/548 arquivos comparados, 0 ausentes, 0 obsoletos, 14/14 skills e 5/5 diretórios `hub_*`;
- árvore operacional `.assistant`: inalterada durante os 16 runs;
- `main` reconciliada após o congelamento da coleta: `6dfb8707835921f2f48020f383cf571902080109`;
- snapshot reconciliado validado: **1476 arquivos / 1935 links / 0 extras**;
- homologação explícita do usuário: **concedida em 16/09/2026**;
- integração da PR #56: **autorizada**.

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

`TESTES.md` e `RESULTADOS.md` preservam o registro técnico da candidata imediatamente antes do aceite; o estado de governança final da sprint é registrado neste README e em `CHECKPOINT.md`.

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
- os oito workflows aplicáveis do HEAD técnico validado concluíram em **success**;
- o commit que registra a homologação é exclusivamente documental e deve ter seus próprios checks confirmados antes do merge.

## Homologação

O usuário **homologou explicitamente a SE00 em 16/09/2026** e autorizou a integração da PR #56.

A homologação encerra o gate humano da baseline e preserva todos os resultados individuais como evidência histórica congelada.

## Próxima etapa

A integração da PR #56 está autorizada. Depois do merge e da auditoria pós-merge da `main`, a iniciativa poderá avançar para SE01 em etapa separada.

**A homologação da SE00 não autoriza iniciar SE01 antes da confirmação pós-merge.**