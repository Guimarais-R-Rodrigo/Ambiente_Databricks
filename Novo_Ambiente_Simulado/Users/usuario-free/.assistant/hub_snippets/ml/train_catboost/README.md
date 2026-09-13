# `train_catboost` — baseline de boosting com tratamento explícito de variáveis categóricas

<!-- readme-objeto: 1.0.0 -->

CatBoost é uma biblioteca de *gradient boosting* que oferece mecanismos próprios para trabalhar com variáveis categóricas, além de numéricas. Este helper prepara um baseline para classificação binária, multiclasse ou regressão, permite indicar quais colunas são categóricas, calcula métricas de validação e pode registrar parâmetros e métricas no MLflow.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um wrapper de `CatBoostClassifier` e `CatBoostRegressor`. |
| Para que serve? | Criar uma referência tabular, inclusive quando categorias devem ser tratadas nativamente pelo CatBoost. |
| Use quando... | Houver dados preparados, validação pertinente e categóricas cuja representação foi definida conscientemente. |
| Evite quando... | Esperar que o helper descubra sozinho tipos, causalidade, leakage ou política de produção. |
| Precisa de... | CatBoost, NumPy, scikit-learn e MLflow se `log_mlflow=True`. |
| Entrega... | Modelo CatBoost treinado e dicionário de métricas por tarefa. |

Consulte a [implementação](train_catboost.py), a [fachada](__init__.py) e o [notebook de exemplo](exemplo_train_catboost.py). O exemplo instala `catboost` e reinicia o Python. Ele usa `log_mlflow=False` e cria somente dados locais sintéticos.

## 1. O que é?

CatBoost é uma implementação de boosting baseada em árvores. Seu diferencial relevante aqui é o suporte explícito a features categóricas: em vez de exigir que todas sejam convertidas manualmente em dezenas ou centenas de colunas, a biblioteca pode construir representações internas apropriadas quando essas features são declaradas.

`train_catboost_baseline` expõe apenas uma parte dessa capacidade. A função escolhe defaults locais, aplica parâmetros opcionais, cria classificador ou regressor, usa validação para early stopping e calcula métricas. Ela não prepara um `Pool`, não descobre categorias automaticamente, não faz tuning nem publica o modelo.

## 2. Que problema este recurso resolve?

A pergunta típica é: “Qual baseline de árvore obtenho se eu permitir que o CatBoost trate explicitamente as colunas categóricas desta matriz?”. Isso é especialmente útil para comparar com um modelo que recebeu one-hot ou outra codificação.

O helper padroniza o treino e a avaliação. Ele não garante que a categórica foi corretamente definida, que a codificação interna é adequada ao negócio ou que o resultado será superior a LightGBM/XGBoost.

## 3. Quando faz sentido usar?

Use quando há uma partição de treino/validação confiável e uma ou mais features categóricas realmente identificadas. Na entrada NumPy do exemplo, `cat_features` recebe **índices de colunas**, começando em zero.

Também é uma boa comparação quando one-hot tornaria a matriz muito larga ou quando target encoding manual criaria risco de vazamento. Isso não elimina a obrigação de controlar separação temporal e disponibilidade das features.

## 4. Quando não usar?

Não passe uma coluna codificada por números inteiros como se a ordem desses números tivesse significado quando, na realidade, ela é categoria nominal. Se você omitir `cat_features`, o wrapper não sabe sua intenção: números podem ser interpretados como valores numéricos.

Também não use uma boa AUC como evidência de que o mecanismo categórico evitou todo leakage. A partição pode continuar vazando tempo, entidade ou informação posterior à decisão. O algoritmo não corrige desenho de dados.

## 5. Como funciona, intuitivamente?

A função valida `task`, verifica algumas condições dos rótulos e cria um dicionário de parâmetros com 500 iterações, learning rate 0,05, profundidade 6, regularização e early stopping de 50 rodadas. `allow_writing_files=False` é colocado no default para evitar que o CatBoost crie `catboost_info/` no diretório de trabalho.

Depois, `params_override` é aplicado. Em seguida, porém, o código define `loss_function` e, nos classificadores, `eval_metric` conforme `task`. Portanto um `loss_function`/`eval_metric` enviado em `params_override` pode ser sobrescrito por essa etapa posterior. O modelo é treinado com `eval_set=(X_val, y_val)` e `cat_features` repassado diretamente à biblioteca.

Por fim, o helper mede AUC/Gini, log loss/accuracy ou RMSE e opcionalmente envia parâmetros e métricas ao MLflow.

## 6. Exemplo de situação

Imagine uma base fictícia de clientes com renda, tempo de relacionamento e um código de agência com centenas de níveis. Você quer comparar um baseline CatBoost com o LightGBM sob a mesma separação temporal.

Você prepara `X_train` e `X_val` preservando a coluna de agência em um tipo aceito pela biblioteca, informa seu índice em `cat_features` e chama o helper. O resultado permite comparar as métricas na mesma janela. Não transforma o código da agência em geografia nem descobre automaticamente relações causais entre agências.

## 7. O que você precisa antes de usar?

As matrizes de treino e validação precisam ter as mesmas colunas na mesma ordem e os targets precisam estar alinhados. O wrapper não valida explicitamente dimensionalidade ou quantidade de linhas antes de entregar os dados ao CatBoost.

Para classificação, o treino precisa conter ao menos duas classes e a validação não pode trazer classe ausente do treino. A função não impõe uma codificação binária específica além do que o CatBoost e as métricas aceitam.

`cat_features` deve identificar corretamente as features categóricas. Com NumPy misturando numéricas e categóricas, tipos podem ser promovidos de forma inesperada. O notebook mostra por que um `dtype=object` pode ser necessário para preservar a natureza da coluna; confirme o tipo efetivamente recebido.

CatBoost e scikit-learn são dependências efetivas. MLflow é opcional apenas com `log_mlflow=False`; se o logging estiver habilitado e MLflow estiver ausente, o erro ocorre depois do treinamento.

## 8. O que este recurso entrega?

O retorno é `(model, metrics)`.

| Tarefa | Métricas | Leitura |
|---|---|---|
| `binary` | `auc_val`, `gini_val` | Discriminação na validação; Gini é reescala de AUC. |
| `multiclass` | `log_loss_val`, `accuracy_val` | Probabilidades/classes na validação. |
| `regression` | `rmse_val` | Erro quadrático médio na unidade do target, após raiz. |

O modelo mantém toda a interface do objeto CatBoost retornado. O helper não devolve feature importance, SHAP, calibração, intervalo de confiança nem modelo registrado no MLflow.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.train_catboost import train_catboost_baseline

model, metrics = train_catboost_baseline(
    X_train, y_train, X_val, y_val,
    task="binary",
    cat_features=[2, 5],
    log_mlflow=False,
)
```

Veja o [notebook](exemplo_train_catboost.py) para o cenário sintético. Ele instala `catboost` sem versão fixada e reinicia a sessão Python.

O helper deixa `allow_writing_files=False` no default para não criar arquivos auxiliares no diretório da sessão. Isso é uma proteção local, não uma propriedade obrigatória do CatBoost: `params_override={"allow_writing_files": True}` pode reabilitar a escrita deliberadamente.

## 10. Decisões e configurações que mais importam

`cat_features` muda a forma como certas colunas são tratadas. Não decida pelo tipo “parece inteiro”; decida pela semântica. ID de agência, por exemplo, pode ser categórico mesmo sendo armazenado como número.

`params_override` permite alterar `iterations`, learning rate, profundidade, regularização, seed e `allow_writing_files`. Mas `loss_function` e `eval_metric` são redefinidos depois conforme `task`; não suponha que todo override sobreviverá. Confira `model.get_params()`.

O early stopping vem no dicionário como `early_stopping_rounds=50` e usa o conjunto de validação. Isso torna a validação parte da seleção do modelo, não um teste final preservado.

## 11. Limitações, riscos e armadilhas

O notebook histórico explicava a codificação categórica como se cada linha usasse literalmente as “linhas anteriores” em ordem temporal e fazia analogia com point-in-time join. Essa leitura é imprecisa. CatBoost usa técnicas ordenadas/permutadas para reduzir o viés e o vazamento de target das estatísticas categóricas; isso **não** certifica disponibilidade temporal das features e não substitui `pit_join`.

O wrapper não valida índices repetidos em `cat_features`, tipos permitidos, nulos, cardinalidade, memória ou correspondência de schema entre treino e validação. Esses erros podem surgir na biblioteca.

`allow_writing_files=False` evita uma classe de efeito colateral, mas não transforma o treino em operação sem efeitos: CPU/GPU, memória, logs do ambiente, MLflow e caches continuam dependendo da execução.

## 12. Quais são as alternativas?

[train_lgbm](../train_lgbm/README.md) oferece um baseline LightGBM. [train_xgboost](../train_xgboost/README.md) é outra referência de boosting. Uma codificação explícita + modelo linear pode ser preferível quando interpretabilidade e simplicidade dominam a decisão.

Não escolha CatBoost apenas porque existe categórica. Compare custo, qualidade, estabilidade, facilidade de inferência e exigências de governança sob o mesmo protocolo.

## 13. Como saber se o resultado faz sentido?

Confira tipos e índices de `cat_features` antes do treino. Use `model.get_cat_feature_indices()` depois para confirmar quais features o modelo registrou como categóricas. Recalcule a métrica de validação a partir de `predict_proba` ou `predict`.

Verifique que a mesma transformação e ordem de colunas chegam à inferência. Se uma categórica tem significado nominal, confirme que não foi convertida silenciosamente em float. Compare com um baseline sob exatamente a mesma partição.

## 14. Arquivos relacionados e próximos passos

A [implementação](train_catboost.py) contém defaults e métricas; a [fachada](__init__.py) exporta `SEED` e `train_catboost_baseline`; o [notebook](exemplo_train_catboost.py) demonstra uma categórica de alta cardinalidade. O [guia da coleção](../../README.md) e o [Manual Técnico](../../../MANUAL_TECNICO.md#catalogo-helpers) mantêm o catálogo integrado.

Se o baseline justificar aprofundamento, trate separadamente tuning, teste final, explicabilidade e empacotamento para inferência.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. Fontes primárias consultadas em 12/09/2026: [features categóricas no CatBoost](https://catboost.ai/docs/en/features/categorical-features), [parâmetro `has_time` e ordem/permutação](https://catboost.ai/docs/en/references/training-parameters/common) e [FAQ com referências ao ordered boosting/ordered categorical statistics](https://catboost.ai/docs/en/concepts/faq).

A evidência de runtime desta R05 será registrada no relatório da sprint. Este README não afirma homologação Databricks, publicação em workspace nem revisão independente.