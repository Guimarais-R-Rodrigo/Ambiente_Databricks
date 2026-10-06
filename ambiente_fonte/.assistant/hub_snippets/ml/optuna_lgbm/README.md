# `optuna_lgbm` — pesquisar hiperparâmetros do LightGBM sem confundir busca com teste final

<!-- readme-objeto: 1.0.0 -->

Otimização de hiperparâmetros escolhe configurações do modelo usando resultados de várias tentativas. Este helper combina Optuna e LightGBM: define um espaço de busca, treina modelos na mesma validação e devolve o `Study` completo e os melhores valores **dos parâmetros pesquisados**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Uma função de tuning com `TPESampler` do Optuna e estimadores LightGBM. |
| Para que serve? | Comparar configurações do LightGBM depois que dados, baseline e validação já estão definidos. |
| Use quando... | Houver orçamento de trials e uma validação apropriada para seleção de hiperparâmetros. |
| Evite quando... | Ainda estiver corrigindo leakage, features, target, partição ou baseline. |
| Precisa de... | Optuna, LightGBM, NumPy, scikit-learn e matrizes de treino/validação. |
| Entrega... | `best_params` pesquisados e o objeto `optuna.Study`; não devolve o melhor modelo treinado. |

Consulte a [implementação](optuna_lgbm.py), a [fachada](__init__.py) e o [notebook](exemplo_optuna_lgbm.py). O exemplo instala `lightgbm optuna`, reinicia o Python e executa uma busca curta; seus 15 trials são demonstração, não recomendação universal de orçamento.

## 1. O que é?

Hiperparâmetros são escolhas feitas antes do ajuste dos pesos/árvores: learning rate, número de folhas, profundidade, regularização e outros. Em vez de testar uma grade fixa, Optuna usa um *sampler* para sugerir configurações com base nos resultados observados.

Este helper usa `TPESampler(seed=42)`. TPE (*Tree-structured Parzen Estimator*) modela regiões associadas a resultados melhores e piores e sugere novos valores a partir dessa informação. Isso é uma busca sequencial orientada pelos trials anteriores; não torna o espaço de busca automaticamente adequado ao problema.

## 2. Que problema este recurso resolve?

A pergunta é: “Dentro deste espaço de hiperparâmetros e desta validação, qual configuração observada produziu o melhor valor da função objetivo?”. A resposta ajuda a escolher uma configuração para nova avaliação.

Ela não responde “qual é o melhor modelo verdadeiro” nem “qual configuração generaliza para qualquer período”. A própria validação foi usada repetidamente para escolher o vencedor.

## 3. Quando faz sentido usar?

Use depois que um baseline já roda corretamente, o target está definido, as features são plausíveis e a validação representa a decisão. Também é útil quando há vários parâmetros contínuos/discretos e uma grade completa seria cara.

A busca precisa de orçamento suficiente para o tamanho do espaço e para a variabilidade do problema. Este helper não impõe um número mínimo de trials porque não existe um limiar universal que transforme TPE em busca “confiável”.

## 4. Quando não usar?

Não use tuning para compensar leakage. Se a validação contém informação futura, o Optuna encontrará a configuração que explora melhor a validação contaminada.

Também não use o mesmo conjunto repetidamente para tuning e depois o apresente como “teste final”. O código pode executar sem erro e produzir um ótimo valor, mas a estimativa já participou da seleção. Reserve um conjunto/janela independente quando a decisão exigir avaliação final.

## 5. Como funciona, intuitivamente?

`optimize_lgbm` valida a tarefa e as classes, escolhe uma métrica interna do LightGBM e cria uma função `objective(trial)`. Cada trial sugere oito hiperparâmetros: `learning_rate`, `num_leaves`, `max_depth`, `min_child_samples`, `subsample`, `colsample_bytree`, `reg_alpha` e `reg_lambda`.

Alguns parâmetros ficam fixos: objetivo, métrica interna, seed e `n_estimators=500`; no multiclasse também `num_class`. O modelo usa early stopping de 50 rodadas na validação.

A **função objetivo do Optuna** é definida pelo código, não pelo nome genérico `metric`: binário retorna AUC; regressão retorna `-RMSE`; multiclasse retorna `-log_loss`. O estudo sempre usa `direction="maximize"`, por isso erros são negados nos dois últimos casos.

## 6. Exemplo de situação

Imagine que um baseline LightGBM binário já foi validado em uma janela temporal. Você quer saber se combinações diferentes de learning rate, folhas e regularização melhoram AUC naquela janela antes de avaliar numa janela posterior.

Você roda 50 trials com `task="binary"`. O `Study` guarda valores, parâmetros e estados de cada tentativa; `best_params` devolve a melhor combinação **entre os parâmetros sugeridos**. Depois você deve reconstruir um modelo completo, juntar os parâmetros fixos pertinentes e avaliar fora da validação usada na busca.

## 7. O que você precisa antes de usar?

Para a rota binária com AUC, confirme **ambas as classes 0 e 1 no treino e na validação** antes de consumir compute. A checagem local não garante as duas classes na validação; uma única classe pode chegar ao fit e produzir erro ou AUC indefinida depois, conforme a versão. Essa é uma pré-condição de uso, não uma validação adicional já implementada.

Treino e validação precisam estar alinhados e prontos para LightGBM. O helper não valida dimensões de `X`, valores infinitos, leakage, schema ou transformações.

Para classificação, precisa haver ao menos duas classes no treino e toda classe da validação deve existir no treino. Para regressão não há validação específica do domínio do target.

`n_trials` deve ser positivo. `timeout` é encaminhado ao Optuna sem uma validação local adicional. O espaço de busca está fixado no código; não há argumento para alterá-lo sem modificar a implementação.

Optuna, LightGBM, NumPy e scikit-learn são dependências obrigatórias. O helper não usa MLflow.

## 8. O que este recurso entrega?

O retorno é `(best_params, study)`.

`best_params` contém somente os parâmetros que foram sugeridos pelo trial. **Não contém** `objective`, a métrica interna, `random_state`, `n_estimators` nem `num_class`. Portanto não é um dicionário completo para reproduzir sozinho o modelo avaliado.

`study.best_value` significa:

| Tarefa | Valor maximizado |
|---|---|
| `binary` | AUC da validação. |
| `regression` | `-RMSE`; valor menos negativo é melhor. |
| `multiclass` | `-log_loss`; valor menos negativo é melhor. |

O helper não devolve o modelo do melhor trial. Cada modelo existe apenas dentro da função objetivo durante a busca.

## 9. Como usar este recurso no Hub?

Reconstrução explícita após a busca binária com `metric="auc"`:

```python
import lightgbm as lgb
params_novo_fit = {"objective": "binary", "metric": "auc", "verbosity": -1,
                   "random_state": 42, "n_estimators": 500, **best_params}
modelo = lgb.LGBMClassifier(**params_novo_fit)
modelo.fit(X_train, y_train, eval_set=[(X_val, y_val)],
           callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)])
```

É um **novo fit**, não recuperação do modelo do trial: `best_iteration` e o modelo não foram preservados pelo retorno. Para regressão use `LGBMRegressor`, `objective="regression"`, `metric="rmse"`; para multiclasse use `LGBMClassifier`, `objective="multiclass"`, `metric="multi_logloss"` e `num_class` conforme as classes de treino. Preserve os demais parâmetros fixos/callbacks e avalie um teste independente depois, sem usá-lo no early stopping.

```python
from hub_snippets.ml.optuna_lgbm import optimize_lgbm

best_params, study = optimize_lgbm(
    X_train, y_train,
    X_val, y_val,
    task="binary",
    n_trials=50,
    metric="auc",
)
```

Veja o [notebook](exemplo_optuna_lgbm.py). Ele instala dependências sem versões fixadas e reinicia o Python. O exemplo usa 15 trials apenas para demonstrar o mecanismo e não deve ser convertido em política de produção.

Para treinar o modelo escolhido, combine conscientemente `best_params` com os parâmetros fixos/necessários do modelo e faça nova avaliação. Não assuma que `best_params` é drop-in completo para todo wrapper.

## 10. Decisões e configurações que mais importam

Espaço fixado no código (limites inclusivos):

| Parâmetro | Intervalo | Distribuição |
|---|---|---|
| `learning_rate` | 0,01–0,3 | float logarítmica |
| `num_leaves` | 15–127 | inteira |
| `max_depth` | 3–12 | inteira |
| `min_child_samples` | 5–100 | inteira |
| `subsample` | 0,5–1,0 | float uniforme |
| `colsample_bytree` | 0,5–1,0 | float uniforme |
| `reg_alpha` | 0,001–10 | float logarítmica |
| `reg_lambda` | 0,001–10 | float logarítmica |

`task` determina tanto o estimador quanto a função objetivo efetiva. O argumento `metric` tem alcance menor do que o nome sugere: no binário ele é colocado em `params["metric"]`, mas o valor que o Optuna maximiza continua sendo AUC calculada por `roc_auc_score`. Em regressão e multiclasse, `metric` é substituído por `rmse` e `multi_logloss` respectivamente.

`n_trials` e `timeout` definem orçamento, mas a quantidade efetiva concluída pode depender do timeout e do custo dos trials. O `TPESampler` tem seed 42; isso ajuda a repetir a sequência sob condições semelhantes, não garante igualdade entre versões/bibliotecas.

Um ponto técnico importante: o espaço sugere `subsample` entre 0,5 e 1,0, mas não configura `subsample_freq`. Na API LightGBM, frequência zero desabilita bagging periódico. Assim, esse eixo pode ser inerte na configuração padrão do estimador. Trate essa limitação como parte do espaço efetivamente pesquisado.

## 11. Limitações, riscos e armadilhas

A chamada altera a verbosidade global de `optuna.logging` para `WARNING`. O helper não restaura o estado anterior. Não faz chamadas MLflow próprias, mas autologging externo configurado na sessão continua sendo um efeito separado.

A função usa uma única validação em todos os trials. Quanto mais decisões são tomadas olhando a mesma validação, maior o risco de adaptar o processo àquela amostra. Cross-validation, nested validation ou janelas múltiplas não são implementadas aqui.

Parâmetros podem interagir. O notebook mostra `num_leaves` alto com `max_depth` baixo; isso não significa que a busca “errou”, apenas que um limite pode deixar o outro sem efeito. O mesmo vale para `subsample` sem frequência de bagging.

A função não persiste estudo em storage, não suporta retomada explícita, pruning configurado, callbacks customizados, distribuição entre workers ou constraints. Esses recursos existem no ecossistema Optuna, mas não neste wrapper.

## 12. Quais são as alternativas?

Uma busca manual pequena pode ser mais transparente quando há uma ou duas decisões de configuração. [train_lgbm](../train_lgbm/README.md) é o baseline que deve existir antes do tuning. Para comparar algoritmos, [train_catboost](../train_catboost/README.md) ou [train_xgboost](../train_xgboost/README.md) respondem a uma pergunta diferente de “qual hiperparâmetro do LightGBM?”.

Otimizar features, target e protocolo de validação pode ser mais importante do que aumentar o número de trials. Isso é prioridade de desenho, não uma regra de magnitude de ganho.

## 13. Como saber se o resultado faz sentido?

Inspecione `study.trials`, distribuição dos valores, parâmetros repetidamente escolhidos e duração. Compare o melhor trial com o baseline sob a mesma validação e depois avalie uma partição independente.

Confirme quais parâmetros realmente influenciaram o estimador. Para LightGBM, examine `study.best_params` junto dos parâmetros fixos do código e das relações como `num_leaves` versus `max_depth`. Não interprete uma terceira casa decimal como ganho robusto sem avaliar variabilidade.

## 14. Arquivos relacionados e próximos passos

A [implementação](optuna_lgbm.py) define espaço, objetivo e retorno; a [fachada](__init__.py) exporta `SEED` e `optimize_lgbm`; o [notebook](exemplo_optuna_lgbm.py) mostra um estudo binário curto. O [guia da coleção](../../README.md) e o [Manual Técnico](../../../MANUAL_TECNICO.md#catalogo-helpers) mantêm a navegação integrada.

Depois da busca, reconstrua o candidato de forma explícita, registre toda a configuração e use avaliação independente.

## 15. Referências

Consulte TPESampler do Optuna e a API LightGBM da versão instalada. O helper usa uma única validação e não devolve modelo treinado; registre parâmetros fixos e pesquisados, refaça o fit e avalie um teste independente.

Referências primárias de conceito/API: [documentação do `TPESampler`](https://optuna.readthedocs.io/en/latest/reference/samplers/generated/optuna.samplers.TPESampler.html), [API `LGBMClassifier`](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html).
