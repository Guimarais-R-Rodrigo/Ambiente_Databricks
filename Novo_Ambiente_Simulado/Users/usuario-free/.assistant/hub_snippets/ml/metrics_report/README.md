# `metrics_report` — métricas padronizadas para classificação binária e regressão

<!-- readme-objeto: 1.0.0 -->

Este objeto calcula um conjunto padronizado de métricas **driver-side**. Ele ajuda a comparar resultados sob um contrato comum, mas não escolhe população, target, split, threshold de negócio nem aprova um modelo para produção.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Helper NumPy/scikit-learn para métricas binárias e de regressão. |
| Para que serve? | Padronizar nomes, escalas e cálculo de métricas recorrentes. |
| Use quando... | A população de avaliação, o target e a unidade das previsões já foram definidos. |
| Evite quando... | Você precisa de multiclasses, métricas distribuídas em Spark ou validação temporal por si só. |
| Precisa de... | NumPy, SciPy e scikit-learn; arrays 1-D finitos. |
| Entrega... | Dicionário de métricas arredondadas. |

Consulte a [implementação](metrics_report.py), a [fachada pública](__init__.py) e o [notebook](exemplo_metrics_report.py).

## 1. O que é?

`calculate_binary_metrics` recebe rótulos 0/1 e probabilidades em `[0,1]`. `calculate_regression_metrics` recebe valores reais e previsões. O módulo centraliza fórmulas e nomes para reduzir comparações com unidades diferentes.

## 2. Que problema este recurso resolve?

Ele evita que cada notebook implemente AUC, KS, Gini, lift, RMSE ou MAPE de maneira diferente. O ganho principal é **consistência de contrato**, não descobrir qual métrica é correta para qualquer problema.

## 3. Quando faz sentido usar?

Use depois de congelar população de avaliação, target, horizonte e split. Em classificação, declare o threshold usado para F1, precision e recall. Para comparar modelos, mantenha essas condições iguais.

## 4. Quando não usar?

Não use sobre um Spark DataFrame esperando execução distribuída. Não use AUC/F1 como substitutos de validação de negócio, calibração ou ausência de leakage. O helper binário exige as duas classes.

## 5. Como funciona, intuitivamente?

No binário, métricas de ranking (`auc_roc`, `ks_pct`, `gini`, `auc_pr`, `lift_10pct`) convivem com calibração (`brier_score`) e métricas dependentes de threshold (`f1`, `precision`, `recall`). `prevalence` registra a taxa observada de positivos.

Na regressão, calcula RMSE, MAE, MAPE e R². O MAPE exclui observações cujo `y_true` é zero; se todos os valores reais forem zero, devolve `NaN`.

## 6. Exemplo de situação

Um modelo de propensão produz probabilidades numa base com 5% de eventos. AUC pode permanecer alta enquanto recall no threshold 0,5 é baixo. O relatório torna essa diferença visível e permite repetir o cálculo em outros thresholds.

## 7. O que você precisa antes de usar?

Arrays devem ser 1-D, não vazios e de mesmo comprimento. `y_prob` precisa ser finito e estar em `[0,1]`; classificação exige rótulos 0/1 e presença das duas classes. `threshold` precisa estar entre 0 e 1.

Regressão exige valores finitos. Defina previamente a unidade do target: RMSE/MAE herdam essa unidade.

## 8. O que este recurso entrega?

Classificação: `auc_roc`, `ks_pct`, `gini`, `auc_pr`, `brier_score`, `f1`, `precision`, `recall`, `lift_10pct` e `prevalence`.

**Atenção à unidade:** `ks_pct` está em pontos percentuais, escala 0–100. Não divida por 100 ao passar para consumidores que também esperam `ks_pct`.

Regressão: `rmse`, `mae`, `mape` e `r2`.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.metrics_report import calculate_binary_metrics

metricas = calculate_binary_metrics(y_true, y_prob, threshold=0.30)
```

Para regressão, importe `calculate_regression_metrics`.

## 10. Decisões e configurações que mais importam

O `threshold` só afeta F1, precision e recall. AUC, KS, Gini, AP, Brier e lift usam as probabilidades diretamente.

`lift_10pct` usa `ceil(10% * N)`: em bases pequenas, o grupo superior pode não ter exatamente 10% em termos fracionários.

## 11. Limitações, riscos e armadilhas

A função não calcula intervalos de confiança nem incerteza amostral. Não há suporte multiclasse. O arredondamento ocorre antes do retorno.

O MAPE exclui targets iguais a zero e pode ficar instável perto de zero. R² pode ser pouco informativo em amostras ou desenhos inadequados.

Uma métrica excelente em teste contaminado continua sendo evidência inválida.

## 12. Quais são as alternativas?

Use APIs do scikit-learn diretamente quando precisar de métricas não incluídas, curvas completas, pesos amostrais ou configurações específicas. Para visualização, veja [`curves_plotly`](../curves_plotly/README.md). Para acompanhamento temporal, veja [`performance_monitor`](../performance_monitor/README.md).

## 13. Como saber se o resultado faz sentido?

Cheque prevalência, número de classes, unidade do KS, threshold e tamanho da amostra. Recalcule casos simples manualmente e compare com funções oficiais do scikit-learn. Valide métricas em população realmente out-of-sample.

## 14. Arquivos relacionados e próximos passos

A [implementação](metrics_report.py) contém as fórmulas; a [fachada](__init__.py) expõe somente as duas funções públicas; o [notebook](exemplo_metrics_report.py) demonstra classificação desbalanceada.

A saída pode ser traduzida para a política de [`performance_monitor`](../performance_monitor/README.md) por `selecionar_metricas_do_relatorio`.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base R09. Referências primárias: documentação de métricas do scikit-learn (`sklearn.metrics`) e SciPy (`scipy.stats.ks_2samp`).

Os valores retornados são evidência estatística; sua adequação depende do desenho de avaliação e da decisão de negócio.