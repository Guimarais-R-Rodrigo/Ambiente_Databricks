# `comparar_tabelas` — comparar duas tabelas sem confundir diferença com erro

<!-- readme-objeto: 1.0.0 -->

Este recurso é um briefing para orientar uma comparação controlada entre duas tabelas ou versões de uma mesma fonte. Ele ajuda a declarar objetivo, grão, chaves, período, colunas críticas, tolerâncias e restrições antes de pedir uma análise ao assistente. Não executa comparação por conta própria e não transforma qualquer diferença em defeito.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um prompt preenchível para comparar schema, conteúdo, reconciliação, migração, período ou drift entre dois recursos. |
| Para que serve? | Tornar a comparação reproduzível e separar diferenças materiais de variações esperadas. |
| Use quando... | Houver duas fontes comparáveis, com objetivo e população explicitados. |
| Evite quando... | O grão ou a chave ainda não forem compreendidos, ou quando só existir uma fonte. |
| Precisa de... | Duas fontes acessíveis, unidade de análise, chaves, período, filtros e tolerâncias. |
| Entrega... | Um pedido estruturado; a resposta e as métricas dependem da interação e das leituras realmente autorizadas. |

Comece pelo [briefing original](comparar_tabelas.md). O [notebook de exemplo](exemplo_comparar_tabelas.py) ilustra uma reconciliação com dados sintéticos, mas o preparo **sobrescreve duas tabelas persistentes** no schema `workspace.default`; leia a seção 9 antes de executar.

## 1. O que é?

`comparar_tabelas` é um prompt personalizado do Hub. Ele organiza uma solicitação para comparar dois recursos que podem representar versões, cargas, ambientes ou recortes distintos. O formulário força a pessoa a declarar o tipo de comparação e os elementos que dão significado às diferenças: granularidade, chaves, tempo, colunas críticas, filtros e tolerâncias.

O arquivo principal é texto. Ele não importa Python, não abre tabelas e não calcula métricas sozinho. A comparação só acontece quando o briefing preenchido é fornecido a um assistente com os recursos e permissões apropriados.

## 2. Que problema este recurso resolve?

A pergunta central é: “A e B diferem de uma forma que importa para o objetivo declarado?”. Uma comparação ingênua de schema pode ignorar duplicidade, perda de cobertura, divergência por chave ou mudança de distribuição; uma comparação linha a linha também pode ser inválida quando o grão ou a chave não coincidem.

O briefing reduz esse risco ao pedir explicitamente o que será considerado equivalente e qual tolerância deve ser usada. Ele apoia a decisão de investigar, aceitar com ressalvas ou rejeitar uma carga, mas não toma essa decisão automaticamente.

## 3. Quando faz sentido usar?

Use em reconciliação pós-migração, comparação de cargas sucessivas, validação entre origem e destino, análise de mudança de schema ou conteúdo e investigação de drift quando existirem duas referências comparáveis.

Faz mais sentido quando a população pode ser alinhada por filtros e período, a unidade de análise está clara e existe uma chave ou outra estratégia defensável de correspondência. Para números, também é importante declarar tolerância absoluta ou relativa; diferenças de centavos, arredondamento ou precisão temporal não devem ser tratadas como materialidade universal.

## 4. Quando não usar?

Não use como atalho para “provar que a carga está correta” quando você ainda não sabe o que uma linha representa ou quando as duas fontes têm populações diferentes por desenho. Nesse caso, primeiro diagnostique granularidade, filtros e cobertura.

Um contraexemplo é reconciliar duas tabelas de clientes apenas por `id_cliente` quando uma tem uma linha mensal e a outra uma linha diária. O código pode executar um join, mas a multiplicação resultante responde a uma pergunta diferente da pretendida.

## 5. Como funciona, intuitivamente?

Você descreve os dois lados da comparação e a pergunta que pretende responder. O prompt orienta o assistente a conferir schema, grão, cobertura temporal, chaves e duplicidade antes de reconciliar registros.

Depois, diferenças são organizadas por categorias como somente A, somente B, iguais e divergentes. Valores numéricos e timestamps precisam de tolerâncias e precisão declaradas. O resultado deve separar evidência observada, hipótese de causa e recomendação de ação.

## 6. Exemplo de situação

Uma equipe migrou uma tabela legada de clientes para uma nova camada `silver`. A expectativa é manter a mesma população e saldo, mas a nova carga contém regras de arredondamento e um processo diferente de atualização.

O briefing pode declarar A como a tabela legada, B como a nova tabela, grão cliente-mês, chave composta, período comum, filtros equivalentes e tolerância de R$ 0,01 para saldo. Uma resposta útil mostrará contagens, cobertura de chaves e divergências acima da tolerância. Ela não deve afirmar que a migração está correta apenas porque a maior parte das linhas coincidiu.

## 7. O que você precisa antes de usar?

Tenha acesso aos dois recursos e preencha os campos do [briefing](comparar_tabelas.md): recursos A e B, tipo de comparação, granularidade, chaves, coluna temporal/período, colunas críticas, tolerâncias, filtros e restrições.

Confirme que os filtros produzem populações comparáveis e que as chaves não geram muitos-para-muitos inesperado. O prompt não valida permissões previamente nem transforma “somente leitura” em bloqueio técnico; permissões e ações disponíveis dependem do ambiente.

## 8. O que este recurso entrega?

O artefato desta pasta entrega uma solicitação estruturada. Seu contrato pede veredito resumido, matriz de diferenças de schema, scorecard de conteúdo, métricas de reconciliação, diferenças priorizadas, código reproduzível quando aplicável e limitações.

Esses itens são solicitados, não garantidos. A pessoa deve conferir que numeradores, denominadores, período, filtros e tolerâncias usados na resposta correspondem ao briefing. “Compatível” também não significa “correto para o negócio” sem critérios de aceite apropriados.

## 9. Como usar este recurso no Hub?

Abra [comparar_tabelas.md](comparar_tabelas.md), preencha todos os campos e anexe ou selecione os dois recursos reais no Genie Code. O briefing sugere a skill conforme o foco: perfil/qualidade, Cross-EDA ou monitoramento; não existe uma skill única para qualquer comparação.

O [notebook de exemplo](exemplo_comparar_tabelas.py) prepara duas bases sintéticas e depois mostra o prompt preenchido. O preparo chama `saveAsTable(..., mode="overwrite")` para **duas** tabelas: `workspace.default.hub_exemplo_clientes_v1` e `workspace.default.hub_exemplo_clientes_v2`. Portanto, estudar o texto é seguro, mas executar a Parte 1 pode substituir objetos existentes com esses nomes.

A Parte 3 do notebook permanece marcada como não executada porque depende de uma conversa real com Genie Code. Não preencha essa seção com uma resposta inventada para “completar” o exemplo.

## 10. Decisões e configurações que mais importam

O `TIPO_COMPARACAO` define o que deve ser medido. `GRANULARIDADE` e `CHAVES` determinam se uma reconciliação linha a linha é válida. `COL_DATA_E_PERIODO` e `FILTROS` delimitam a população. `COLUNAS_CRITICAS_OU_TODAS` controla materialidade e custo.

`TOLERANCIAS_OU_PROPOR` merece atenção especial: pedir que o assistente proponha um limite não transforma esse limite em política aprovada. Registre sua origem e valide se faz sentido para unidade, precisão e decisão em questão.

## 11. Limitações, riscos e armadilhas

Duas tabelas podem ter o mesmo schema e ainda representar populações diferentes. Um join pode multiplicar linhas e produzir taxas falsas. Strings podem divergir por normalização, números por arredondamento e timestamps por timezone ou precisão.

A resposta de um assistente pode sugerir causas para diferenças; trate essas causas como hipóteses até verificá-las. Também não confunda um prompt que pede “somente leitura” com uma garantia de que nenhuma ferramenta ou notebook preparatório possa escrever.

## 12. Quais são as alternativas?

Para um diagnóstico inicial de uma única fonte, use [eda_rapida](../eda_rapida/README.md) ou o briefing [eda_completa](../eda_completa/eda_completa.md). Para regras explícitas de qualidade, use [data_quality](../data_quality/data_quality.md). Para avaliar compatibilidade de múltiplas fontes com objetivo de modelagem, use [cross_eda](../cross_eda/cross_eda.md).

Se a necessidade for apenas uma checagem determinística simples, um teste SQL/PySpark específico pode ser mais direto e auditável que uma conversa ampla.

## 13. Como saber se o resultado faz sentido?

Confirme contagens de A e B antes e depois dos filtros, unicidade das chaves e cardinalidade do join. Recalcule pelo menos uma taxa de divergência material a partir de numerador e denominador apresentados.

Verifique se nulos participaram das comparações, se a tolerância foi aplicada na unidade correta e se o período/timezone coincide entre os lados. Uma divergência explicada sem evidência deve permanecer hipótese.

## 14. Arquivos relacionados e próximos passos

O [briefing principal](comparar_tabelas.md) contém os placeholders e o contrato de saída. O [notebook](exemplo_comparar_tabelas.py) mostra uma situação sintética e os riscos do preparo persistente. O [catálogo de Hub Prompts](../README.md) ajuda a escolher briefings vizinhos.

Depois da comparação, transforme divergências materiais em testes reproduzíveis ou critérios formais de aceite. Quando o problema for de modelagem e múltiplas fontes, o próximo passo pode ser Cross-EDA em vez de ampliar indefinidamente a reconciliação.

## 15. Referências

O comportamento local descrito aqui foi confrontado com [comparar_tabelas.md](comparar_tabelas.md) e [exemplo_comparar_tabelas.py](exemplo_comparar_tabelas.py) na base R10 iniciada a partir do merge R09. O prompt e o notebook não foram executados no Databricks nesta revisão.

Para a seleção de contexto no Genie Code, consulte a documentação oficial [Navigate Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code), consultada em 13/09/2026. Ela documenta anexos e seleção de recursos com `@`; não homologa este prompt customizado.
