# SER00 — dependências, concorrência e ordem

Baseline auditada: `11851e137dd7793b351ac08fc211c0be90005dee`. Main atual: `4bc7c9aada96468505e51f279cf32c107d0b6dbb`. As únicas branches concorrentes incorporadas foram as manutenções A07/PR #102 e #105, por merges explícitos após certificação local.

## Estado Git observado

| Frente | Estado e identidade | Interação com SER |
|---|---|---|
| main | `4bc7c9aada96468505e51f279cf32c107d0b6dbb`, após merges das PRs #102 e #105 sobre a baseline PSEF00 | base atual da certificação final SER00 |
| PSEF01 / PR #99 | draft; b733bf3fa226bef964e640c0728c8dfecc9e992d; branch psef/PSEF01-contrato-editorial-policy-aware | toca hub_prompts/README e cinco documentos PSEF; derivado stale declarado; não incorporar candidata acumulada |
| MM01 / PR #51 | aberta; HEAD observada `a5bb60a27ad8b0ab5cb8953642efbcdb14211328` em 2026-09-23 | não incorporar; compartilha README/CHANGELOG e gates; reconfirmar antes da certificação final |
| antiga SE08 / PR #91 | draft, não mergeável; 65d75dca58860e7e19c8dceb5f70ce4ddb568fcd | toca skills/README, Manual, tools/skill_enforcement, CI e derivado; preservar e não integrar por efeito colateral |
| antiga V05 / PR #26 | aberta na listagem; 22 arquivos de theme_lab, testes, README, índices e workflow | superfície visual/derivado; não misturar com rollout |
| antigas PR #4, #5, #6 | abertas na listagem inicial, frentes anteriores de READMEs | não fechadas/alteradas; reexaminar delta completo antes de qualquer integração concorrente |
| manutenção A07 / PR #102 | certificada localmente em `4a70834d...`, integrada em `515e673b...` | corrigiu oráculo test-only e snapshot raiz |
| manutenção A07 / PR #105 | certificada localmente em `7af65df5...`, integrada em `4bc7c9aa...` | adicionou delete sharing Win32; teste causal PASS, stress 30/30, CI/FULL verdes |
| SER00 | `ser/SER00-rollout-baseline`, a reconciliar por merge normal com `main@4bc7c9aa...` | documentação SER + ADR-0022 + changelog/snapshot; zero produto/policy/runtime da SER00 |

A MM01 continuou avançando independentemente e foi observada em `c43273fb...`; não transportar estados intermediários para a SER. As PRs #102 e #105 foram explicitamente autorizadas e integradas porque eram pré-requisitos técnicos da certificação SER00.

A busca paginada de branches psef/ retornou PSEF00 e PSEF01, sem PSEF04. A listagem inicial tinha sete PRs abertas: #4, #5, #6, #26, #51, #91 e #99. Esse conjunto é uma observação, não trava de concorrência; reconfirmar imediatamente antes de certificar/integrar. Não se declara auditoria exaustiva dos deltas das três PRs antigas de README nesta rodada.

## Grafo de execução candidato

```text
SER00 A01–A03 aceitas + complemento local A07 + aceite de integração
  -> SER01 somente após autorização separada
  -> SER02
  -> SER03
  -> SER04
  -> SER05 -> SER06
  -> SER07 -> SER08
  -> SER09 -> SER10
  -> SER11 -> SER12
  -> SER13 -> SER14
  -> SER15
  -> SER16
  -> SER-ACTIONS-RECERTIFICATION (futuro, não bloqueante)
```

Essa linha é a ordem de integração, não uma alegação de que toda sprint depende funcionalmente de todas as anteriores.

## Dependências técnicas e ausência de ciclos

| Consumidor | Dependência real | Como evitar dependência artificial |
|---|---|---|
| SER01–SER14 | identidade de certificação SER e semântica de condições aprovadas | não duplicar engine; não alterar perfis históricos silenciosamente |
| SER02 explainability | modelo/dataset sintéticos ligados à fixture, dependência SHAP compatível | não exigir conclusão SER10; fixture pré-treinada/versionada é suficiente para testar binding/cálculo |
| SER03 safra | calendário/MOB/denominadores e núcleo vintage | não depender de modelo de crédito real |
| SER04 estatística | catálogo efetivo de métodos e plano aprovado | não exigir bibliotecas/causalidade que não integram a superfície |
| SER06 cross-EDA | SER05 aceita e contrato PIT/diagnóstico | helpers existentes não são prova de L4 da skill |
| SER08 features | SER07 aceita; primitives temporais e contrato de materialização | reutilizar PIT compartilhado sem copiar runner da cross-EDA |
| SER10 baseline | SER09 aceita; splits/features consistentes; adapters de treino/tracking | respeitar algoritmo/tarefa; não tornar todos os helpers obrigatórios |
| SER12 monitoramento | SER11 aceita; identidade de modelo e referência; métricas validadas | fixtures sintéticas; integração final com produtoras após promoção |
| SER14 pipeline | SER13 aceita; operação de efeito suportada no Free/pessoal | spec/diagnóstico não substitui deploy; falta de capacidade mantém bloqueio |
| SER15 | promoções realmente aceitas e seus verifiers | não declarar nove concluídas se alguma ficou parcial |
| SER16 | árvore integrada reconciliada e provas por skill | campanha final não é a primeira observação comportamental |

## Coordenação externa

PSEF01 pode prosseguir em sua própria frente; briefings não recebem policy ou Receipt próprios. PSEF02/PSEF03 se apoiam principalmente em skills já implementadas. Recomenda-se executar as partes pertinentes de PSEF04 após as respectivas promoções SER; se forem integradas antes, registrar reconciliação na sprint produtora e na SER15. Nunca hardcodar níveis futuros nos prompts.

MM01 não é alterada pela SER. MM04 é dependência prospectiva: criar hub-ml-micromodelos exigirá reconciliar explicitamente a cardinalidade atualmente fixa em 14 no validator. Não adicionar a 15ª skill nesta frente por conveniência nem editar a candidata MM01. A arquitetura de evidências das produtoras deve informar essa frente, não substituí-la.

Antes de cada sprint: main/PRs/branches/arquivos, PSEF e MM reconfirmados. Se a main avançar durante certificação, preservar bundle, declarar stale e abrir nova rodada sobre estado reconciliado; nunca transportar PASS entre SHAs. Uma sprint parte da main vigente depois da integração da anterior, não de outra candidata não aceita.

O README Micromodelos da main ainda registra o fechamento MM00 e MM01 como próximo passo; a PR #51 mostra trabalho em andamento fora da main. Preservar essa diferença entre estado integrado e candidata. A exceção documental D1-B/Q-01 da MM00 foi encerrada e não autoriza adiar o changelog de novas sprints.
