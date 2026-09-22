# SE08 — complemento de I/O após reconciliação concorrente

**Estado: IMPLEMENTACAO_PARCIAL_EM_REVIEW. Não é aceite, RC, certificação da SE08 ou promoção.**

## Origem e fronteira da execução

Autor deste complemento: ChatGPT. Fonte primária: GitHub, sem memória de outros chats.
A reconciliação inicial confirmou `main@73cacdd44fbccc80da835d96388ca23b6a6fcefc`,
PRs #80/#81 merged, candidatas com 12/12 e 7/7 workflows e ambos os pós-merges
com 18/18 success. A branch `sef/SE08-operacao` inicialmente era idêntica à main.
O P2 original da PR #80 estava resolvido. Dois threads tardios da PR #81 foram
observados: UTF-8 inválido e autoria do changelog; não foi reatribuída autoria
histórica sem prova.

Durante esta execução, escritas externas a ela avançaram a main para
`c70f5af9b4108f2d99c79ba678719347e91fc910` (merge da PR #82, hotfix UTF-8)
e a SE08 para `aa83e5cc2e31da9dbd04ca888fe8d5b2ac2f9d53`, tree
`14f5849bfc121153c764b0dcda680318215d3e42`. A comparação a c70f5af9 observou
sete commits à frente e zero atrás. Esses commits adicionam integração SE08
em validator, certifier, CI e testes; não foram escritos nem certificados por
esta execução. A declaração do autor da PR #82 sobre os labels ChatGPT foi
observada no thread; esta execução não resolveu threads em nome de terceiros.

Para preservar as alterações concorrentes, a review
`sef/review-SE08-policy-io-20260921` nasce do snapshot aa83e5cc. Não houve
force-push, alteração da canônica, merge, PR ou publicação Databricks nesta
execução. Qualquer HEAD posterior deve ser reconciliado, nunca sobrescrito.

## Escopo canônico e critério de parada

O Plano Mestre define SE08 como CI, operação, documentação e gate de promoção
ao trabalho. A revisão `REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md` prevalece:
desenvolvimento sem PR, certificação local antes da candidata, Free/Genie e
promoção como gates separados. Este complemento trata apenas a consistência
de leitura do validator usado nessa integração. Não redefine o DoD nem cria
outro perfil de certificação.

Faltam execução em clone completo, certificação do SHA final, Windows/NTFS e
reconciliação com a outra linha de implementação. A próxima ação é local;
não usar Actions como executor de desenvolvimento nem declarar SE08 concluída.

## Achado reproduzido e correção

Blob de partida conferido por hash Git:
`12729da088e87f4d79559da213f56a2429525b0b` em aa83e5cc.

A correção UTF-8 já estava presente. Entretanto, `summarize()` fazia duas
leituras: validava a primeira e contava entradas da segunda. Uma injeção
explícita retornando primeiro uma policy sintética válida de 14 entradas e
depois `{"skills": []}` produziu `status=PASS` com `policy_entries=0`.
Erro na segunda leitura também era silenciosamente substituído por objeto vazio.
Isso é teste de fronteira sintético; não é observação de corrida nativa.

O complemento lê/parseia uma única vez e valida o mesmo objeto resumido.
O handler continua cobrindo OSError, UnicodeDecodeError e JSONDecodeError.
Preserva as assinaturas públicas, `assistant_root` e seu suporte no CLI,
`discover_skills`, os níveis e todas as regras de validação da versão aa83e5cc.
A igualdade do corpo das regras e das interfaces foi conferida por AST.
Não altera policy.json, contratos, runtime, writer, certifier, renderer ou CI.

## Evidência e limites

Ambiente: Linux x86_64, Python 3.13.5. Componentes reconstruídos por hash,
com fixtures sintéticas temporárias; não há checkout completo nem história Git local.
Comando: `python -B tools/tests/test_skill_enforcement_policy_io.py -v`.

| Rodada | Alvo | Resultado |
|---|---|---|
| 09 | Código aa83e5cc, 12 métodos | exit 1, uma falha, zero skips |
| 11 | Mesmo código, suíte ampliada para 15 métodos | exit 1, três falhas, zero skips |
| 12 | Código corrigido, mesmos 15 métodos | exit 0, 15/15, zero skips |

A ampliação acrescenta teste da contradição observável, ausência de releitura
após erro e CLI positivo com raiz explícita. As tentativas vermelhas permanecem
no bundle externo, não foram substituídas por repetição da mesma candidata.
Resultado verde observado em `2026-09-22T01:41:17.553091+00:00`.

Código corrigido: blob `c09f1b088083a30b0e325f4bc998f8d65fdd5842`, SHA-256
`a84ab7aba727e85af4cf089993354c289cb80645ae858ab080a45548a62ad314`.
Teste: blob `e3699d3107d3b4d400359a063579942f9955c617`.
O SHA do commit publicado e o manifesto do bundle devem ser conferidos no
handoff externo; não se atribui evidência de componente a uma tree inteira.

Uma proposta anterior desta execução, `baa0db58695415c8476106303693f9bcc9d234ac`,
foi criada como objeto Git a partir de 73cacdd4, mas não anexada a ref nem
integrada: foi superada pela reconciliação. Seus 12 testes focalizados e os dez
testes de uma proposta alternativa de CI ficam apenas como histórico de bancada.
A alternativa de CI não foi publicada nem substitui o perfil se08 concorrente.
Não aplicar aquela proposta antiga sobre esta review.

## Gate local de continuação

Em clone completo, limpo e de SHA congelado, executar serialmente:

1. `python -B tools/tests/test_skill_enforcement_policy_io.py -v`;
2. `python -B tools/tests/test_skill_enforcement_se08.py -v`;
3. `python -B tools/tests/test_certify_storage_cleanup.py -v`;
4. `python -B tools/tests/test_certify_local.py -v`;
5. `python -B tools/tests/test_validate_create_readme.py -v`;
6. `python -B tools/tests/test_skill_enforcement_se07_create_l3.py -v`;
7. `python -B tools/tests/test_skill_enforcement_se07.py -v`;
8. `python -B tools/tests/test_render_simulado.py -v`;
9. `python -B tools/validate_assistant.py --conferir-readme`;
10. `python -B tools/skill_enforcement/certify_local.py --profile se08 --evidence-dir <novo-diretorio-externo>`;
11. `python -B tools/ci_local.py --verbose`, com dependências canônicas preparadas.

Estes comandos são requisitos da próxima rodada, NÃO resultados executados.
O perfil se08 e o CI devem ser lidos antes para confirmar a cobertura vigente,
sem confundir o FULL SE07 histórico de 16 gates com suítes fora dele.
Não usar allow-dirty, skip-render ou no-evidence na certificação completa.
O CI parcial utiliza flags próprias e não substitui esse FULL.

Registrar externamente comandos, SHA/tree, plataforma, Python, filesystem,
stdout/stderr, exit observado, testes/falhas/skips, início/fim, hashes e todas
as tentativas. Não resolver falha por retry, skip novo ou mudança de threshold.
Um novo commit exige recertificação correspondente. Não executar Free/Genie,
PR ou promoção só porque testes focalizados passaram.

## Dívidas e bloqueios preservados

- SE06: 24/25; S06-A1-R4=NOT_RUN; SE06_DOD=INCOMPLETE; FULLY_CERTIFIED=false.
- SE07: CLOSED_BY_HUMAN_DECISION_WITH_KNOWN_RESIDUAL; SE07_FULLY_CERTIFIED=false.
- Storage cleanup histórico FAIL 8/9 permanece; resíduo desaparecido entre
  observações, causa não estabelecida. FULL PASS não o reclassifica.
- NATIVE_WINERROR32_NOT_REPRODUCED_IN_THIS_RECERTIFICATION não é WINERROR32_FIXED.
- hub-ml-criar-objeto: current_level L2 global; piloto L3 stage-specific não promove a skill.
- Sem dados reais, credenciais, identificadores corporativos ou alterações em outras frentes.

A entrada atribuída desta execução está preservada em
[fragmento de changelog](../sprints/skill_enforcement/SE08/ENTRADA_CHANGELOG_POLICY_IO.md).
O conteúdo pertinente foi incorporado ao `CHANGELOG.md` raiz pela consolidação
repo-side, preservando as entradas históricas e sem reatribuir autoria de
terceiros. A candidata ainda não é pronta: rematerialização do derivado,
snapshot, certificação local/Windows e gates de ambiente permanecem pendentes.
