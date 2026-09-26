# `stat_check` — definir a pergunta estatística antes de escolher o teste

<!-- readme-objeto: 1.0.0 -->

Este recurso é um briefing para organizar uma validação estatística antes de modelagem ou inferência. Ele força a declarar unidade amostral, target, finalidade, método, população, tempo, hipóteses, critérios e modo de trabalho. O prompt não executa testes nem transforma significância estatística em causalidade.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um prompt preenchível para diagnóstico estatístico pré-modelagem. |
| Para que serve? | Relacionar pergunta, estimando, método, pressupostos, efeito e incerteza. |
| Use quando... | Houver hipótese ou método a avaliar com desenho e população explicitados. |
| Evite quando... | A intenção for justificar uma conclusão já tomada ou quando a finalidade estiver indefinida. |
| Precisa de... | Dataset, unidade, target, objetivo, população, tempo, hipóteses, critérios e volume. |
| Entrega... | Uma solicitação estruturada de diagnóstico, método, evidência, código opcional e limitações. |

Comece pelo [briefing original](stat_check.md). O [notebook de exemplo](exemplo_stat_check.py) prepara uma tabela sintética com escrita persistente; confira a seção 9 antes de executar.

## 1. O que é?

`stat_check` é um prompt personalizado para separar três perguntas que costumam ser misturadas: previsão, inferência e experimento. O briefing pede que a finalidade seja declarada antes da escolha do método e que pressupostos sejam vinculados ao desenho real dos dados.

## 2. Que problema este recurso resolve?

O mesmo dataset pode exigir análises diferentes conforme a pergunta. Um teste escolhido apenas porque é familiar pode violar independência, ignorar repetição por entidade ou produzir um p-valor pouco relevante para a decisão. O briefing ajuda a explicitar essas escolhas.

## 3. Quando faz sentido usar?

Use para avaliar um método pretendido, desenhar uma análise inferencial, revisar comparações entre grupos ou preparar diagnósticos antes de modelagem. É especialmente útil quando há múltiplas hipóteses, medidas repetidas ou dependência temporal.

## 4. Quando não usar?

Não use para confirmar uma conclusão escolhendo o teste depois de observar o resultado. Um contraexemplo é comparar muitos segmentos até encontrar um p-valor baixo e tratá-lo como hipótese confirmatória sem considerar multiplicidade.

## 5. Como funciona, intuitivamente?

Você declara unidade, target, objetivo, população e hipóteses. O prompt pede que cada pergunta seja mapeada a estimando, método e pressupostos; depois orienta diagnóstico, tamanho de efeito e incerteza, mantendo significância estatística separada de relevância prática e poder preditivo.

## 6. Exemplo de situação

Uma equipe quer saber se a taxa de resposta difere entre grupos. O briefing informa unidade cliente, target binário, amostra de conveniência, hipóteses e volume. A resposta deve discutir método e limitações de seleção; não deve concluir causalidade apenas por diferença estatisticamente significativa.

## 7. O que você precisa antes de usar?

Preencha [stat_check.md](stat_check.md) com dataset, granularidade/chave/grupos, target, finalidade, método desejado ou seleção, população/amostra, tempo/split, hipóteses, critérios, volume, restrições e modo. Se algo essencial estiver ausente, a resposta deve delimitar a lacuna.

## 8. O que este recurso entrega?

O contrato solicita matriz de pergunta, estimando, método e pressupostos; diagnósticos; tamanho de efeito e incerteza; interpretação; código no nível solicitado; limitações e ameaças à validade. Esses elementos dependem da interação e dos dados efetivamente analisados.

## 9. Como usar este recurso no Hub?

Abra [stat_check.md](stat_check.md), preencha o briefing e selecione dataset e contexto. O prompt recomenda `@hub-ml-validacao-estatistica`.

O [notebook](exemplo_stat_check.py) cria `workspace.default.hub_exemplo_clientes` com `mode("overwrite")` usando dados sintéticos. Executar a Parte 1 pode substituir uma tabela existente com esse nome. A Parte 2 é texto; a Parte 3 depende de uma resposta real do Genie Code.

## 10. Decisões e configurações que mais importam

A finalidade `PREDICAO_INFERENCIA_EXPERIMENTO` vem antes do método. Unidade amostral e repetição determinam independência. População e mecanismo de seleção afetam validade externa. Hipóteses e critérios definem como interpretar multiplicidade, efeito e incerteza.

## 11. Limitações, riscos e armadilhas

Amostra grande pode tornar efeitos pequenos estatisticamente detectáveis sem importância prática. Amostra de conveniência limita generalização. Dependência temporal ou medidas repetidas invalidam métodos que assumem observações independentes. Um teste significativo não estabelece causalidade sozinho.

## 12. Quais são as alternativas?

Para exploração dos dados, use [eda_completa](../eda_completa/README.md). Para especificar atributos, use [feature_engineering](../feature_engineering/README.md). Quando a pergunta for apenas uma checagem determinística, um cálculo direto pode ser mais simples que um diagnóstico estatístico amplo.

## 13. Como saber se o resultado faz sentido?

Confirme unidade, direção do target, população, exclusões e tratamento de nulos. Verifique se o método responde à pergunta declarada e se tamanho de efeito e intervalo de incerteza acompanham o p-valor. Compare interpretação com os pressupostos realmente avaliados.

## 14. Arquivos relacionados e próximos passos

O [briefing](stat_check.md) contém o formulário; o [notebook](exemplo_stat_check.py) demonstra o cenário; o [catálogo](../README.md) reúne prompts vizinhos. Um diagnóstico aprovado pode seguir para código reproduzível, desenho experimental ou modelagem em etapa separada.

## 15. Referências

A descrição local foi confrontada com [stat_check.md](stat_check.md) e [exemplo_stat_check.py](exemplo_stat_check.py). Esta revisão foi estática e não executou o notebook nem a interação do Genie Code.

Para seleção de recursos no Genie Code, consulte [Navigate Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code), consultada em 13/09/2026.
