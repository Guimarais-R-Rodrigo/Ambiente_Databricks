# R03-A — conciliação com a V00 integrada em paralelo

Data: 2026-09-12. Autor/revisor: ChatGPT, A0_light.

## Bases e motivo

O lote R03-A foi escrito e testado sobre main `5493f7db68f397ad7040485cb09bad53eb79be74`, resultando em `7bb2db65718d6350e4ad753c1744fa48a7fb55ea`. A conferência remota 34705928058 passou nas oito etapas e em 26/26 testes suplementares, incluindo Spark real. O artefato 10301489767 foi lido; essa evidência refere-se à árvore inicial, não à composição seguinte.

Durante a rodada, outra frente integrou o PR nº 8 (instrumentação visual V00), e a main passou a `b88a9ccdde6e61892bc25eb7cf4f4b2577badb23`. A simulação com git merge-tree encontrou somente dois conflitos textuais: CHANGELOG.md e README.md. Não houve conflito de algoritmo, API, paleta, template ou ADR.

## Resolução e preservação

As inserções da R03-A foram acrescidas ao changelog completo da main V00 sem remover ou editar suas entradas. O README manteve as orientações da R03-A; os números de validação foram recalculados na árvore combinada. Todos os demais arquivos adicionados/alterados pela V00 foram preservados integralmente, incluindo tools/README.md, docs/README.md, instrumentos, relatórios e workflow permanente. O verificador datado passou a conferir esse documento compartilhado contra a V00 em vez da base anterior, sem ignorá-lo.

Os sete novos guias e o conteúdo das quinze seções do contrato não foram reescritos. Continuam 13/74 objetos operacionais e 61 pendentes. O ADR do Concierge e o aceite anterior permanecem intactos. A composição ocorre somente na branch de trabalho; não autoriza novo merge na main nem início de R03-B.

## Evidências e limites

Os logs iniciais continuam datados e vinculados à primeira base. Os resultados da nova composição serão registrados no comentário de fechamento do PR nº 9 e no pacote da conversa após execução real. Não usar a aprovação anterior para atestar automaticamente a composição. Reexecutar as oito etapas e as três suítes específicas da V00; verificar bytes das duas frentes e a árvore exata. O aceite dos sete novos textos, auditoria independente e homologação Databricks continuam fora da execução desta rodada.

### Execução local da composição

As oito etapas passaram novamente, com 195 testes aprovados e sete opcionais Spark pulados. As suítes V00 executaram 27 testes de inventário, 12 de contratos legados e nove de confiabilidade do relatório: 48 aprovados. A preservação passou, incluindo os 20 arquivos da V00 não envolvidos nos dois conflitos textuais. Grupos de preservação se sobrepõem; não somar como arquivos únicos. Estes resultados são locais, não o resultado futuro da CI do PR.
