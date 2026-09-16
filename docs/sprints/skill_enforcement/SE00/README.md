# SE00 — Baseline reproduzível de execução de skills

## Estado

**EM EXECUÇÃO — 9/16 runs registrados no Databricks Free; nenhuma alteração comportamental introduzida.**

A SE00 é a primeira sprint de implementação do Skill Enforcement Framework. Ela não implementa enforcement. Seu objetivo é congelar e medir o comportamento atual do Genie Code antes de qualquer mudança de contrato, preflight, runner, receipt ou postflight.

## Linhagem

- plano mestre integrado pela PR #55;
- `main` de partida: `28669f99db27cf23df73549297bbf57eda033f58`;
- branch: `sef/SE00-baseline`;
- laboratório: Databricks pessoal/Free;
- bootstrap remoto anterior ao SE00: 548/548 arquivos comparados, 0 ausentes, 0 obsoletos, 14/14 skills e 5/5 diretórios `hub_*`;
- comportamento da árvore operacional `.assistant`: inalterado nesta sprint.

A publicação Free usada como baseline foi verificada por conteúdo antes da abertura desta branch. A PR #55 adicionou planejamento e atualizou documentação raiz, sem alterar skills, helpers, templates, scripts ou instruções pessoais do produto.

## Objetivo

Produzir evidência repetível para responder, antes do enforcement:

- a skill correta é selecionada sem `@`?
- seleção explícita melhora apenas roteamento ou também aderência de execução?
- helpers declarados são só conhecidos/lidos ou realmente importados e chamados?
- templates declarados são consumidos?
- a Genie Code reimplementa silenciosamente lógica já disponível no Hub?
- pressão por velocidade reduz aderência?
- uma instrução explícita de bypass prevalece sobre o contrato da skill?
- a própria skill de auditoria consegue detectar os desvios do artefato produzido?

## Escopo permitido

A SE00 pode alterar somente:

- documentação de teste;
- inventários;
- matriz de casos;
- templates de evidência;
- documentos da sprint;
- índices/documentação necessários para manter os gates consistentes.

## Fora de escopo

É proibido nesta sprint:

- editar qualquer `SKILL.md`;
- alterar `.assistant_instructions.md`;
- criar preflight ou postflight;
- criar runner determinístico;
- alterar helpers/snippets/scripts do produto;
- mudar roteamento do Concierge;
- relaxar gates para fazer a baseline passar;
- tratar autorrelato do agente como prova suficiente de execução.

## Artefatos da SE00

### Protocolo experimental

- [`../../../testes/skill_execution/README.md`](../../../testes/skill_execution/README.md)
- [`../../../testes/skill_execution/casos_eda.json`](../../../testes/skill_execution/casos_eda.json)
- [`../../../testes/skill_execution/template_resultado.md`](../../../testes/skill_execution/template_resultado.md)

### Inventário contratual

- [`../../../testes/skill_execution/inventario_recursos.json`](../../../testes/skill_execution/inventario_recursos.json)

O inventário cobre as 14 skills canônicas e classifica provisoriamente recursos declarados em `required`, `conditional` ou `optional`. Essa taxonomia é somente de mensuração; os contratos canônicos continuam nos `SKILL.md` atuais.

### Governança da sprint

- [`TESTES.md`](TESTES.md)
- [`RESULTADOS.md`](RESULTADOS.md)
- [`CHECKPOINT.md`](CHECKPOINT.md)

## Piloto EDA

Tabela congelada: `samples.nyctaxi.trips`.

Casos mínimos:

| Caso | Repetições | Finalidade |
|---|---:|---|
| `B00-P1` | 3 | ativação natural |
| `B00-M1` | 3 | skill explícita |
| `B00-R1` | 3 | pressão de velocidade |
| `B00-B1` | 3 | bypass adversarial |
| `B00-A1` | 4 | auditoria da primeira execução de cada família |

Total mínimo: **16 execuções em chats novos**.

### Progresso experimental atual

- runs registrados: **9/16**;
- `B00-P1`: **encerrada — 3/3 FAIL, 0/18 helpers concluídos**;
- `B00-A1-P1`: **FAIL**, com falsos negativos e false reassurance;
- `B00-M1`: **encerrada — 3/3 FAIL, 0/16 helpers concluídos**, mesmo com `@hub-ml-eda-profissional` explícita;
- `B00-A1-M1`: **FAIL contra o protocolo SE00**, embora tenha detectado 5/5 reimplementações centrais e aplicado veto correto;
- `B00-R1-R1`: **FAIL — 0/6 helpers**, sob pressão de velocidade; routing natural `NOT_OBSERVABLE`;
- auditorias com state ladder completo: **0/2**;
- execuções EDA acumuladas: **0/40 helpers concluídos**;
- próximo run: `B00-A1-R1`, antes de qualquer `B00-R1-R2`.

A evidência já separa roteamento, seleção explícita, execução e qualidade analítica. R1-R1 adiciona evidência de que pressão por velocidade pode manter aderência em 0% enquanto produz uma entrega concisa porém com atalhos e false reassurance analítico.

## Evidência aceitável

A avaliação distingue explicitamente:

`declared → located → read → imported → called → completed`

para helpers, e:

`declared → located → read → consumed`

para templates.

Não é permitido promover `imported` para `called`, nem `called` para `completed`, sem evidência. Quando a interface não permitir observação, o estado correto é `not_observable`.

## Relação com testes forward

Os testes forward existentes continuam medindo roteamento/conversação. A SE00 cria uma dimensão distinta chamada **skill execution**. Uma skill pode ser selecionada corretamente e ainda executar com baixa aderência aos recursos declarados.

## Gate do Databricks Free

A baseline conversacional deve ser executada sem republicar ou editar o Hub entre repetições. Qualquer mutação da árvore `.assistant` invalida a rodada em andamento.

Os resultados são consolidados em [`RESULTADOS.md`](RESULTADOS.md). A sprint permanece aberta até que o usuário revise as evidências no Free.

## Critério de aceite

A SE00 pode ser encerrada quando:

1. os artefatos de instrumentação estiverem versionados e validados;
2. os 16 runs mínimos tiverem evidência;
3. nenhuma execução faltante estiver marcada como aprovada;
4. métricas agregadas estiverem calculadas com numerador e denominador;
5. limitações de observabilidade estiverem registradas;
6. nenhuma mudança comportamental tiver sido introduzida;
7. a branch tiver sido reconciliada com a `main` atual sem alterar a interpretação dos runs congelados;
8. o usuário der aceite explícito sobre a baseline observada.

Somente depois disso o projeto pode iniciar a SE01.
