# `metrics_report` — entender o que um modelo acerta, erra e ordena

<!-- readme-objeto: 1.0.0 -->

Este snippet do Hub calcula indicadores de classificação binária ou regressão a partir de respostas conhecidas e previsões. Não treina um modelo nem decide sua aprovação: oferece medidas diferentes para perguntas diferentes.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Calculadora padronizada de métricas de ML. |
| Para que serve? | Avaliar ordenação, decisões por corte e erro de previsão. |
| Use quando... | Você tem alvo realizado e previsões alinhadas da mesma população. |
| Evite quando... | O alvo ainda não maturou ou você precisa avaliar várias classes. |
| Precisa de... | NumPy, scikit-learn e SciPy; dados limitados à memória do driver. |
| Entrega... | Dicionário de números, não tabela pronta nem parecer de aprovação. |

Acesse a [implementação](metrics_report.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_metrics_report.py). O notebook usa dados sintéticos, sem escrita de tabelas.

## 1. O que é?

Uma métrica resume um aspecto de uma previsão. Classificação binária pergunta se um evento acontecerá, representando ausência por `0` e ocorrência por `1`. Regressão prevê uma quantidade, como valor ou prazo.

`calculate_binary_metrics` compara probabilidades com eventos observados; `calculate_regression_metrics` compara quantidades previstas com realizadas. Uma única nota não descreve todos os erros: um modelo pode ordenar bem os clientes e, ainda assim, atribuir probabilidades exageradas.

## 2. Que problema este recurso resolve?

Ajuda a responder “o modelo separa os eventos dos não eventos?”, “quantos casos alcançamos com este corte?” e “qual o tamanho dos erros?”. Padroniza nomes e arredondamentos para evitar relatórios incomparáveis.

Não responde quanto custa cada erro, se houve vazamento de informação ou se a amostra representa a operação. Essas perguntas precisam acompanhar os números.

## 3. Quando faz sentido usar?

Use na avaliação de um conjunto de teste separado do desenvolvimento ou em períodos de monitoramento com rótulos já realizados. Em uma classificação com evento raro, combine precisão e recall com a prevalência: a frequência do evento muda a dificuldade prática de encontrar casos.

Para uma previsão de valor, compare MAE e RMSE com uma referência simples medida nas mesmas linhas. Comparações exigem o mesmo horizonte, unidade, população e regra de avaliação, não apenas o mesmo nome da métrica.

## 4. Quando não usar?

Não passe rótulos incompletos como se fossem negativos. Um contrato ainda dentro do prazo de observação não é necessariamente um caso sem evento; o código pode calcular números, mas responder à pergunta errada.

O classificador exige as duas classes `0` e `1`: não é um avaliador multiclasse, de sobrevivência ou ranking. O helper também não aceita pesos amostrais; uma amostra artificialmente balanceada pode distorcer precisão, prevalência, Brier e lift em relação à operação.

## 5. Como funciona, intuitivamente?

Para decisões binárias, probabilidades maiores ou iguais a `threshold` viram `1`. Precisão mede quantos dos marcados realmente eram eventos; recall mede quantos dos eventos foram marcados. F1 combina essas duas proporções. Ao elevar o corte, recall não aumenta; precisão, porém, não é obrigada a subir em toda amostra.

AUC-ROC resume a ordenação dos scores. O KS do relatório é a maior diferença absoluta entre as distribuições acumuladas de scores de eventos e não eventos, multiplicada por 100. O Gini aqui é `2 × AUC − 1`, não uma medida de desigualdade de renda.

Na regressão, MAE é a média dos erros absolutos; RMSE dá mais peso a erros grandes. MAPE divide o erro absoluto pelo valor real e expressa a média em porcentagem; este código exclui alvos exatamente iguais a zero dessa conta.

## 6. Exemplo de situação

Em uma ilustração com 100 observações e 20 eventos, os dez maiores scores contêm seis eventos. A taxa no topo é 60%, contra 20% na base: o lift desse topo é três. Isso significa concentração de eventos observados, não “três vezes mais lucro” nem efeito causal de uma campanha.

Esse cálculo ilustra o significado do indicador; não é uma medição de modelo real. O [notebook](exemplo_metrics_report.py) traz outra população sintética e resultados históricos, que não são desempenho garantido para novos dados.

## 7. O que você precisa antes de usar?

Cada posição de `y_true` precisa corresponder à mesma observação de `y_prob` ou `y_pred`. Faça o alinhamento por chave antes de extrair arrays: índices pandas não são usados para juntar os vetores. Declare o grão, por exemplo cliente por mês, e impeça duplicações indevidas.

As funções exigem vetores unidimensionais, não vazios, de mesmo tamanho e valores finitos. Na classificação, ambas as classes precisam existir e as probabilidades devem estar em `[0, 1]`, orientadas para a classe `1`. O corte deve estar nesse intervalo. Na regressão não se exige positividade do alvo, mas valores próximos de zero tornam MAPE instável.

O processamento é local, sem amostragem ou coleta Spark automática. Bibliotecas presentes em um runtime não significam que estarão presentes em outro; confira NumPy, SciPy e scikit-learn na sessão de uso.

## 8. O que este recurso entrega?

| Chave | Leitura e unidade |
|---|---|
| `auc_roc`, `gini` | Ordenação; maior costuma ser melhor. Gini pode ser negativo. |
| `ks_pct` | KS bilateral em pontos percentuais, de 0 a 100; uma ordenação invertida também pode ter KS alto. |
| `auc_pr` | **Average Precision (AP)** do scikit-learn, não área trapezoidal sob a curva PR. |
| `brier_score` | Erro quadrático das probabilidades; menor é melhor, mas não mede somente calibração. |
| `precision`, `recall`, `f1` | Proporções no corte declarado, de 0 a 1. |
| `lift_10pct`, `prevalence` | Razão de concentração no topo e proporção de eventos na base. |
| `rmse`, `mae`, `mape`, `r2` | Retorno exclusivo da função de regressão: unidade do alvo, unidade do alvo, porcentagem e coeficiente sem unidade. |

O dicionário binário contém dez chaves, sem acurácia. Arredonda `ks_pct` a uma casa, lift a duas e as demais a quatro. Regressão arredonda MAPE a duas casas e as demais a quatro. Se todos os alvos forem zero, MAPE é `NaN`; R² tem limitações em amostras unitárias ou alvos constantes, conforme o scikit-learn.

## 9. Como usar este recurso no Hub?

Com `.assistant` disponível no caminho de importação, este exemplo trabalha apenas em memória:

```python
from hub_snippets.ml.metrics_report import calculate_binary_metrics

y = [0, 1, 0, 1]
p = [0.1, 0.8, 0.3, 0.6]
relatorio = calculate_binary_metrics(y, p, threshold=0.5)
print(relatorio["auc_roc"], relatorio["ks_pct"])
```

O [notebook](exemplo_metrics_report.py) explica a preparação do import no workspace. A docstring antiga cita `format_metrics_table`, mas **essa função não existe na implementação nem na fachada atual**. Para apresentar uma tabela, converta o dicionário explicitamente ou use uma ferramenta de apresentação já disponível.

## 10. Decisões e configurações que mais importam

`threshold=0.5` é um padrão, não uma recomendação. Escolha o corte na validação segundo custo dos erros, capacidade de atendimento ou restrições do processo; reserve o teste para avaliar essa escolha. Modelos podem ser comparados com cortes diferentes quando a regra operacional é comum e os cortes foram escolhidos sem consultar o teste.

O topo do lift contém `ceil(0.10 × N)` observações, no mínimo uma. Em base pequena, isso pode exceder 10% da amostra. Empates na fronteira não têm regra de negócio explícita; o código usa a ordenação do NumPy.

## 11. Limitações, riscos e armadilhas

Arredondamento pode esconder pequenas diferenças. Não há intervalo de confiança, teste de significância, análise por segmento ou proteção contra vazamento. Uma AUC alta não valida calibração, estabilidade, equidade nem viabilidade econômica.

`ks_pct=40` significa 40 pontos percentuais. Não envie esse valor a um limiar definido na escala 0–1. A curva de [`curves_plotly`](../curves_plotly/README.md) usa `max(TPR − FPR)`, sem valor absoluto, na escala 0–1: a diferença não é apenas de unidade quando a ordenação está invertida.

A função de regressão pode devolver MAPE indefinido ou R² negativo; não substitua automaticamente esses resultados por zero. Verifique primeiro o significado e a população efetivamente avaliada.

## 12. Quais são as alternativas?

Use diretamente as funções do scikit-learn para pesos, outras classes, métricas adicionais ou controle dos valores sem arredondamento. Para visualizar compromissos entre cortes, use [`curves_plotly`](../curves_plotly/README.md).

Para acompanhar deterioração ao longo de períodos, use [`performance_monitor`](../performance_monitor/README.md) após selecionar e traduzir os nomes das métricas. Para apenas apresentar o resultado, uma tabela pandas pode ser suficiente.

## 13. Como saber se o resultado faz sentido?

Confira a proporção de eventos, a quantidade de linhas e o alinhamento por chave. Na fixture perfeita acima, AUC é 1 e KS é 100; ao inverter os scores, AUC deve cair, mesmo que o KS bilateral permaneça alto.

Recalcule precisão e recall pela contagem de verdadeiros/falsos positivos em um corte conhecido. Registre quantos zeros foram excluídos de MAPE e compare o modelo com uma referência simples na mesma população. Resultado sem erro de execução não é evidência de adequação à decisão.

## 14. Arquivos relacionados e próximos passos

A [implementação](metrics_report.py) define cálculos e validações; a [fachada](__init__.py) define os dois imports públicos; o [notebook](exemplo_metrics_report.py) apresenta classificação desbalanceada. Consulte o [catálogo da coleção](../../README.md) e o [Manual Técnico](../../../MANUAL_TECNICO.md) para compor o fluxo completo.

O próximo passo é decidir quais métricas respondem à pergunta do estudo e registrar os dados, o corte e a população junto dos valores.

## 15. Referências

Comportamento conferido na implementação e na fachada locais. A documentação primária de [Average Precision](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html) distingue AP de integração trapezoidal; [KS bilateral](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html) define a estatística e as premissas; [calibração](https://scikit-learn.org/stable/modules/calibration.html) explica por que Brier não isola calibração. Consultadas em 13/09/2026.

A revisão R09 é documental e autorrevisada. A execução dos casos sintéticos é registrada no relatório da sprint; não implica homologação Databricks ou validação do seu modelo.
