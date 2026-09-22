# SER00 — dependências, concorrência e ordem

Base auditada: `11851e137dd7793b351ac08fc211c0be90005dee`. Nenhuma branch concorrente foi incorporada.

## Estado Git observado

| Frente | Estado e identidade | Interação com SER |
|---|---|---|
| main / PSEF00 | PR #98 integrada em 11851e137dd7793b351ac08fc211c0be90005dee | baseline de autoria |
| PSEF01 / PR #99 | draft; b733bf3fa226bef964e640c0728c8dfecc9e992d; branch psef/PSEF01-contrato-editorial-policy-aware | toca hub_prompts/README e cinco documentos PSEF; derivado stale declarado; não incorporar candidata acumulada |
| MM01 / PR #51 | aberta; 94ba596ca4385223248a102b9ff02c0252491c88; 181 commits, 39 arquivos; R5 PASS mecânico com bundle não aceito e R6 aguardada | não incorporar; compartilha README/CHANGELOG e gates; qualquer avanço main exige nova reconciliação |
| antiga SE08 / PR #91 | draft, não mergeável; 65d75dca58860e7e19c8dceb5f70ce4ddb568fcd | toca skills/README, Manual, tools/skill_enforcement, CI e derivado; preservar e não integrar por efeito colateral |
| antiga V05 / PR #26 | aberta na listagem; 22 arquivos de theme_lab, testes, README, índices e workflow | superfície visual/derivado; não misturar com rollout |
| antigas PR #4, #5, #6 | abertas na listagem inicial, frentes anteriores de READMEs | não fechadas/alteradas; reexaminar delta completo antes de qualquer integração concorrente |
| SER00 | ser/SER00-rollout-baseline, criada diretamente na main auditada | documentação SER + ADR-0022/índice de ADR; zero produto/policy/runtime |

A MM01 continuou avançando durante a SER00: depois de 3e3e105f.../R5, a PR passou a 94ba596c...; R5 ficou como PASS mecânico, mas o bundle foi recusado como certificação final por sanitização insuficiente de paths escapados, e R6 tornou-se o próximo gate. Não reutilizar PASS ou identidade anterior como evidência da nova HEAD.

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
