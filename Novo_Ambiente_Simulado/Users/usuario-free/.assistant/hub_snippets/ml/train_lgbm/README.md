# `train_lgbm` — baseline LightGBM para comparar modelos tabulares com um contrato explícito

<!-- readme-objeto: 1.0.0 -->

LightGBM combina árvores de decisão por *gradient boosting*: novas árvores são acrescentadas para reduzir o erro que permanece. Este helper organiza um baseline supervisionado para classificação binária, multiclasse ou regressão, mede treino e validação e pode registrar parâmetros e métricas no MLflow. Baseline aqui significa **referência de comparação**, não modelo automaticamente aprovado.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um wrapper da API scikit-learn do LightGBM. |
| Para que serve? | Criar uma referência tabular reproduzível para classificação ou regressão. |
| Use quando... | Dados e target já estiverem preparados e houver validação pertinente ao problema. |
| Evite quando... | Precisar de causalidade, pipeline completo, treino Spark distribuído ou decisão operacional pronta. |
| Precisa de... | LightGBM, NumPy, scikit-learn, matrizes alinhadas e MLflow se `log_mlflow=True`. |
| Entrega... | Modelo `LGBMClassifier`/`LGBMRegressor` e métricas por tarefa. |

Consulte a [implementação](train_lgbm.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_train_lgbm.py). O exemplo instala `lightgbm` sem fixar versão e reinicia o Python; leia esse efeito antes de executá-lo. As chamadas demonstradas usam `log_mlflow=False`.

## 1. O que é?

Uma árvore divide os exemplos por condições nas variáveis. No *gradient boosting*, várias árvores pequenas são combinadas sequencialmente para melhorar a função de perda. LightGBM é uma implementação eficiente desse método para dados estruturados.

`train_lightgbm_baseline` é um recorte dessa biblioteca. Ele escolhe defaults locais conforme `task`, permite sobrescritas, usa um conjunto de validação para parada antecipada e calcula um pequeno conjunto de métricas. Não faz preparação de features, separação temporal, tuning, calibração, explicabilidade nem publicação.

## 2. Que problema este recurso resolve?

A pergunta prática é: “Com estes dados preparados e esta validação, qual é uma referência competitiva de árvore para comparar com modelos mais simples ou mais complexos?”. Sem baseline, um modelo sofisticado pode parecer bom apenas porque nunca foi comparado sob as mesmas condições.

O helper ajuda a padronizar essa comparação. Ele não responde se uma variável causa o target, se o ganho é economicamente relevante ou se o modelo deve ser colocado em produção.

## 3. Quando faz sentido usar?

Use quando cada linha representa a unidade que será prevista, as features estavam disponíveis no instante da decisão e a validação reproduz o cenário que importa. O wrapper suporta `binary`, `multiclass` e `regression`.

Também faz sentido como referência antes de testar TabNet, MLP com embeddings ou uma busca Optuna. A comparação só é informativa quando população, features, target, partições e métrica permanecem compatíveis.

## 4. Quando não usar?

Não use uma validação aleatória quando o objetivo real é prever períodos futuros e existe mudança temporal importante. O código executará, mas a resposta poderá ser otimista porque treino e validação misturam regimes que em produção não coexistem.

Não use este wrapper como substituto de processamento distribuído Spark: ele recebe matrizes/arrays já materializados para a API Python do LightGBM. Para volumes que não cabem nesse desenho, o problema de execução precisa ser resolvido antes de escolher este helper.

## 5. Como funciona, intuitivamente?

A função seleciona um dicionário de parâmetros para a tarefa, aplica `params_override`, cria `LGBMClassifier` ou `LGBMRegressor` e chama `fit` com `eval_set=[(X_val, y_val)]`. Quando `early_stopping_rounds` é positivo, um callback interrompe o treinamento depois de um número de rodadas sem melhora da métrica monitorada.

Depois, `_calculate_metrics` mede treino e validação. No binário calcula AUC de treino e validação, Gini de validação e a diferença de AUC. Na regressão usa RMSE e um gap relativo. No multiclasse usa log loss de treino/validação, accuracy de validação e diferença de log loss. Se solicitado, os parâmetros e métricas são enviados ao MLflow.

## 6. Exemplo de situação

Imagine um problema fictício de propensão com 40 mil observações históricas. O treinamento usa meses anteriores e a validação usa o mês seguinte. Antes de testar uma rede neural, você quer uma referência de árvore sob a mesma janela e as mesmas features.

`train_lightgbm_baseline(..., task="binary")` devolve um modelo e métricas de discriminação. A decisão útil não é “LightGBM ganhou porque a AUC é alta”, mas “esta é a referência obtida nesta partição; qualquer alternativa deve ser comparada com ela sob o mesmo protocolo”. Nenhum valor de AUC é prometido por este cenário.

## 7. O que você precisa antes de usar?

`X_train` e `X_val` precisam ter o mesmo significado e ordem de features; `y_train` e `y_val` precisam estar alinhados às linhas. O wrapper converte apenas os targets para NumPy e não valida formato, finitude ou número de colunas de `X`: erros desse tipo podem surgir depois dentro do LightGBM.

Em classificação, o treino precisa ter ao menos duas classes e a validação não pode introduzir classe ausente no treino. A função não exige explicitamente que o caso binário tenha exatamente duas classes; confirme a codificação antes da chamada. Em multiclasse, `num_class` é inicialmente derivado das classes de treino.

LightGBM e scikit-learn são dependências efetivas. MLflow é opcional apenas porque o módulo trata sua ausência: com `log_mlflow=True`, a falta de MLflow gera `ImportError` **depois do treinamento**. Verifique dependências antes de consumir compute.

## 8. O que este recurso entrega?

O retorno é `(model, metrics)`.

| Tarefa | Métricas produzidas | Interpretação |
|---|---|---|
| `binary` | `auc_train`, `auc_val`, `gini_val`, `overfit_gap` | AUC mede ordenação das duas classes; Gini é `2*AUC-1`; o gap é AUC de treino menos validação. |
| `regression` | `rmse_train`, `rmse_val`, `overfit_gap` | RMSE fica na unidade do target; o gap é `(rmse_val-rmse_train)/rmse_val` quando o denominador é não zero. |
| `multiclass` | `log_loss_train`, `log_loss_val`, `accuracy_val`, `overfit_gap` | Menor log loss é melhor; accuracy é proporção de classes previstas corretamente; gap é log loss de validação menos treino. |

`overfit_gap` não possui limiar universal neste helper. Um valor pequeno ou grande precisa ser interpretado com variabilidade, desenho da validação, tamanho amostral e custo da decisão.

## 9. Como usar este recurso no Hub?

Depois de tornar a raiz `.assistant` disponível ao Python:

```python
from hub_snippets.ml.train_lgbm import train_lightgbm_baseline

model, metrics = train_lightgbm_baseline(
    X_train, y_train, X_val, y_val,
    task="binary",
    log_mlflow=False,
)
```

O [notebook de exemplo](exemplo_train_lgbm.py) mostra um caso sintético. Ele executa `%pip install lightgbm` e `%restart_python`, portanto altera a sessão. Não copie a instalação sem revisar a política e as versões do ambiente.

Com `log_mlflow=True`, o wrapper chama `mlflow.log_params` e `mlflow.log_metrics`; ele não abre/fecha explicitamente um run nem registra o modelo por chamada própria. O contexto de experimento precisa ser definido pelo consumidor ou pelo ambiente.

## 10. Decisões e configurações que mais importam

`task` define modelo, objetivo e métricas. `params_override` é aplicado depois dos defaults e pode sobrescrever inclusive `objective`, `metric`, `num_class` e a semente. Isso dá flexibilidade, mas permite criar uma configuração incompatível com a avaliação que continua sendo escolhida por `task`.

Os defaults locais incluem `learning_rate=0.05`, `n_estimators=500`, `num_leaves=31`, `colsample_bytree=0.8`, `subsample=0.8` e regularização L1/L2 igual a 0.1. Um detalhe importante: o wrapper **não define `subsample_freq`**. Na API atual do LightGBM, `subsample_freq=0` desabilita a amostragem periódica de linhas; portanto `subsample=0.8` isoladamente não deve ser descrito como bagging efetivo. `colsample_bytree=0.8`, por outro lado, controla a fração de features por árvore.

`early_stopping_rounds=50` usa a validação como parte da seleção do número de árvores. Zero desliga o callback criado pelo wrapper. A validação, portanto, não é um teste final intocado.

## 11. Limitações, riscos e armadilhas

O helper não valida leakage, grão, disponibilidade temporal, pesos, desbalanceamento, calibração, fairness ou estabilidade. Uma ótima métrica pode continuar sendo produto de uma partição inadequada.

Os `params_override` podem separar a configuração de treino do contrato de métricas. Por exemplo, alterar `objective` sem alterar `task` não muda a rotina de avaliação. O mesmo vale para sobrescrever `num_class` no multiclasse.

O notebook histórico exibe um bloco abreviado dos defaults e uma interpretação de `subsample=0.8` como aleatoriedade de linhas. A fonte de verdade atual é `DEFAULT_PARAMS_*` na implementação; como `subsample_freq` não é definido, não trate aquela frase histórica como descrição do comportamento atual.

## 12. Quais são as alternativas?

[train_xgboost](../train_xgboost/README.md) fornece outra referência de árvores impulsionadas. [train_catboost](../train_catboost/train_catboost.py) é especialmente relevante quando há variáveis categóricas que se pretende tratar nativamente. [optuna_lgbm](../optuna_lgbm/optuna_lgbm.py) pesquisa hiperparâmetros depois que um baseline e um protocolo de validação já existem.

Modelos lineares podem ser uma referência mais simples e interpretável em muitos problemas. O objetivo desta função não é declarar LightGBM vencedor universal, e sim tornar uma comparação explícita.

## 13. Como saber se o resultado faz sentido?

Confira número de linhas, classes, feature order e partição. Recalcule a métrica principal fora do helper usando as previsões do modelo. No binário, confira `gini_val == 2*auc_val-1`. Na regressão, verifique a unidade do RMSE.

Inspecione `model.best_iteration_` quando houve early stopping e `model.get_params()` para saber quais parâmetros foram efetivamente enviados. Não conclua que o modelo “generaliza” apenas porque o gap é pequeno; reserve um teste ou janela realmente independente quando o desenho exigir.

## 14. Arquivos relacionados e próximos passos

A [implementação](train_lgbm.py) define defaults, treino e métricas; a [fachada](__init__.py) exporta `SEED`, os três dicionários de defaults e `train_lightgbm_baseline`; o [notebook](exemplo_train_lgbm.py) demonstra classificação binária. O [guia da coleção](../../README.md) e o [Manual Técnico](../../../MANUAL_TECNICO.md#catalogo-helpers) mantêm as rotas integradas.

Depois do baseline, fixe o protocolo de comparação antes de ajustar hiperparâmetros ou trocar de família de modelo.

## 15. Referências

O contrato específico foi conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. Fontes primárias consultadas em 12/09/2026: [API `LGBMClassifier`](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html), incluindo `subsample_freq=0`, e [callback de early stopping](https://lightgbm.readthedocs.io/en/v4.6.0/pythonapi/lightgbm.early_stopping.html). O comportamento local dos defaults vem do código do Hub, não dessas páginas.

A evidência de runtime desta R05 será registrada no relatório da sprint; este README não presume publicação no Databricks, homologação em qualquer workspace nem revisão independente.