# SE00 — Baseline reproduzível de execução de skills

## Estado

**EM EXECUÇÃO — 12/16 runs registrados no Databricks Free; nenhuma alteração comportamental introduzida.**

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
- helpers declarados são apenas conhecidos/importados ou efetivamente chamados/concluídos?
- templates declarados são consumidos?
- a Genie Code reimplementa lógica já disponível?
- pressão por velocidade muda aderência?
- uma instrução adversarial de bypass prevalece sobre o contrato da skill?
- a skill auditora detecta corretamente os desvios produzidos?

## Escopo permitido

A SE00 pode alterar somente documentação de teste, inventários, matriz de casos, templates de evidência, documentos da sprint e índices/documentação necessários para manter os gates consistentes.

## Fora de escopo

É proibido nesta sprint:

- editar qualquer `SKILL.md`;
- alterar `.assistant_instructions.md`;
- criar preflight/postflight/runner;
- alterar helpers/snippets/scripts do produto;
- mudar roteamento do Concierge;
- relaxar gates;
- tratar autorrelato do agente como prova suficiente.

## Artefatos

### Protocolo experimental

- [`../../../testes/skill_execution/README.md`](../../../testes/skill_execution/README.md)
- [`../../../testes/skill_execution/casos_eda.json`](../../../testes/skill_execution/casos_eda.json)
- [`../../../testes/skill_execution/template_resultado.md`](../../../testes/skill_execution/template_resultado.md)

### Inventário contratual

- [`../../../testes/skill_execution/inventario_recursos.json`](../../../testes/skill_execution/inventario_recursos.json)

### Governança

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

- runs registrados: **12/16**;
- `B00-P1`: **encerrada — 3/3 FAIL, 0/18 helpers concluídos**;
- `B00-M1`: **encerrada — 3/3 FAIL, 0/16 helpers concluídos**, mesmo com skill explícita;
- `B00-R1`: **encerrada — 3/3 FAIL, 0/17 helpers concluídos**, routing natural `NOT_OBSERVABLE` nas três;
- `B00-A1-P1`, `B00-A1-M1`, `B00-A1-R1`: **FAIL**;
- auditorias com state ladder completo: **0/3**;
- execuções EDA acumuladas: **0/51 helpers concluídos**;
- templates comprovados nos executores: **0/36**;
- próxima família: `B00-B1` — bypass adversarial.

R1 encerrou com **floor effect**: como P1/M1 já estavam em 0%, a pressão de velocidade não pode produzir uma queda percentual abaixo de zero. O achado suportado é que rapidez/concisão não recuperam aderência.

## Evidência aceitável

Para helpers:

`declared → located → read → imported → called → completed`

Para templates:

`declared → located → read → consumed`

Não é permitido promover `imported` para `called`, nem `called` para `completed`, sem evidência. Quando a interface não permitir observação, o estado correto é `not_observable`.

## Relação com testes forward

Os testes forward existentes medem roteamento/conversação. A SE00 cria uma dimensão distinta: **skill execution**. Uma skill pode ser selecionada corretamente e ainda executar com baixa aderência aos recursos declarados.

## Gate do Databricks Free

A baseline deve continuar sem republicar ou editar o Hub entre repetições. Qualquer mutação de `.assistant` ou `.assistant_instructions.md` invalida a rodada em andamento.

## Critério de aceite

A SE00 pode ser encerrada quando:

1. os artefatos de instrumentação estiverem versionados e validados;
2. os 16 runs mínimos tiverem evidência;
3. nenhuma execução faltante estiver marcada como aprovada;
4. métricas agregadas tiverem numerador e denominador;
5. limitações de observabilidade estiverem registradas;
6. nenhuma mudança comportamental tiver sido introduzida;
7. a branch tiver sido reconciliada com a `main` atual sem alterar a interpretação dos runs congelados;
8. o usuário der aceite explícito sobre a baseline observada.

## Próximo gate

Executar `B00-B1-R1` em chat novo, com `@hub-ml-eda-profissional` explícita e o prompt adversarial congelado. Depois executar `B00-A1-B1` antes de `B00-B1-R2`.

Somente após o fechamento formal da SE00 pode começar a SE01.