# `tabnet_wrapper` — TabNet tabular com classificação/regressão e importância global do modelo

<!-- readme-objeto: 1.0.0 -->

TabNet é uma arquitetura neural para dados tabulares que usa mecanismos de atenção/máscaras para selecionar features ao longo de passos de decisão. Este wrapper oferece um caminho controlado para classificação binária ou regressão e devolve, além do modelo e das métricas, `feature_importances_` calculada pela implementação `pytorch-tabnet`.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um wrapper de `TabNetClassifier`/`TabNetRegressor` da biblioteca `pytorch-tabnet`. |
| Para que serve? | Comparar uma arquitetura neural tabular com baselines sob o mesmo protocolo. |
| Use quando... | Houver dados tabulares preparados, orçamento de treino e hipótese real para testar TabNet. |
| Evite quando... | Ainda não houver baseline, pré-processamento estável ou necessidade/recursos para uma rede neural. |
| Precisa de... | `pytorch-tabnet`, PyTorch, NumPy, scikit-learn e MLflow se `log_mlflow=True`. |
| Entrega... | Modelo treinado, métricas de validação e vetor global `feature_importances_`. |

Consulte a [implementação](tabnet_wrapper.py), a [fachada](__init__.py) e o [notebook](exemplo_tabnet_wrapper.py). O exemplo instala `pytorch-tabnet` sem fixar versão, reinicia o Python e usa `log_mlflow=False`.

## 1. O que é?

TabNet processa dados tabulares em passos sucessivos e aprende máscaras que controlam quais features são usadas em cada etapa. A implementação `pytorch-tabnet` oferece estimadores para classificação e regressão e uma API semelhante à do scikit-learn.

`train_tabnet` encapsula um subconjunto: binário ou regressão, parâmetros arquiteturais básicos, categorias opcionais, early stopping e métricas. Ele não expõe toda a API da biblioteca, pretraining, multitask, grouped features ou callbacks customizados.

## 2. Que problema este recurso resolve?

A pergunta é: “Sob o mesmo treino/validação, uma arquitetura TabNet acrescenta valor em relação aos baselines tabulares já estabelecidos?”. O retorno facilita comparar desempenho e consultar uma importância global produzida pela própria biblioteca.

Essa importância não é causal e não é automaticamente uma explicação suficiente para decisões individuais. O helper não substitui governança, teste final ou análise de erro.

## 3. Quando faz sentido usar?

Use quando o pipeline tabular está estável e já existe uma referência mais simples. Pode fazer sentido em problemas com interações complexas, volume suficiente e orçamento de treino, especialmente quando se quer explorar as máscaras/explicações internas da arquitetura.

O wrapper suporta também features categóricas pela dupla `cat_idxs`/`cat_dims`, desde que os dados já estejam codificados de maneira compatível com `pytorch-tabnet`.

## 4. Quando não usar?

Não escolha TabNet apenas porque a métrica de um exemplo sintético foi alta. Sem comparação no mesmo dataset, o número não responde se a arquitetura vale o custo adicional.

Não trate `feature_importances_` como “quanto cada variável causou a previsão”. A biblioteca deriva a importância de suas explicações/máscaras globais; isso descreve uso do modelo, não efeito causal nem garantia de estabilidade fora da amostra.

## 5. Como funciona, intuitivamente?

A função valida `task`, shapes básicos, categorias e parâmetros de treino, fixa seeds e importa PyTorch. No binário cria `TabNetClassifier` com `n_d`, `n_a`, `n_steps`, `gamma=1.5`, `lambda_sparse=1e-4`, Adam, StepLR e máscara `sparsemax`. Na regressão cria `TabNetRegressor` com um conjunto menor de argumentos explícitos.

O `fit` usa a validação como `eval_set`, AUC para classificação ou RMSE para regressão, com `max_epochs`, `patience` e `batch_size`. Depois o helper recalcula AUC/Gini ou RMSE em scikit-learn e lê `model.feature_importances_`.

Na implementação atual de `pytorch-tabnet`, a importância global é calculada a partir da explicação agregada sobre `X_train` e normalizada. É uma propriedade do estimador treinado, não SHAP.

## 6. Exemplo de situação

Imagine um problema binário de propensão com oito features numéricas e um LightGBM já estabelecido como baseline. Você quer testar se TabNet encontra interações úteis e se o padrão de importância aprendido é coerente com o sinal conhecido.

Você usa a mesma separação e calcula AUC na validação. Se a diferença for material e estável, aprofunda custo, calibração e interpretação. Se empatar, a complexidade extra pode não se justificar. O helper não decide esse trade-off automaticamente.

## 7. O que você precisa antes de usar?

`X` deve chegar numérico, normalmente `float32`; o wrapper chama `np.asarray` sem converter o dtype. Para categorias, valide integralidade antes de chamar: `int(...)` na implementação pode truncar valores fracionários de `cat_idxs`/`cat_dims` silenciosamente.

```python
import numpy as np

assert len(cat_idxs) == len(cat_dims) and len(set(cat_idxs)) == len(cat_idxs)
assert all(isinstance(i, (int, np.integer)) and not isinstance(i, bool) for i in cat_idxs)
assert all(isinstance(d, (int, np.integer)) and not isinstance(d, bool) for d in cat_dims)
for i, d in zip(cat_idxs, cat_dims):
    assert 0 <= i < X_train.shape[1] and d > 0
    for X_part in [X_train, X_val]:
        coluna = X_part[:, i]
        assert np.isfinite(coluna).all() and (coluna == np.floor(coluna)).all()
        assert ((0 <= coluna) & (coluna < d)).all()
```

Use o mesmo encoder ajustado no treino e uma política explícita para categorias desconhecidas; não recalcule os códigos na validação.

Para a rota binária com AUC, confirme **ambas as classes 0 e 1 no treino e na validação** antes de consumir compute. A checagem local não garante as duas classes na validação; uma única classe pode chegar ao fit e produzir erro ou AUC indefinida depois, conforme a versão. Essa é uma pré-condição de uso, não uma validação adicional já implementada.

`X_train` e `X_val` precisam ser matrizes 2-D com o mesmo número de features; targets devem estar alinhados e splits não podem ser vazios. Para binário, labels precisam ser 0/1 e ambas as classes devem existir no treino; a validação é checada como 0/1, mas não há exigência local de ambas as classes nela antes do cálculo de AUC.

`cat_idxs` e `cat_dims` devem ter o mesmo comprimento. Índices precisam cair dentro das colunas e cardinalidades devem ser positivas. O wrapper não valida cada valor categórico contra `cat_dims`; a biblioteca pode falhar posteriormente.

`max_epochs` e `patience` precisam ser positivos e `batch_size > 1`. Não há validação local de positividade/coerência de `n_d`, `n_a`, `n_steps`, `gamma`, `virtual_batch_size` ou tipos/finitude dos dados.

PyTorch, `pytorch-tabnet`, NumPy e scikit-learn são obrigatórios. MLflow é opcional quando logging está desligado.

## 8. O que este recurso entrega?

O retorno é `(model, metrics, importance)`.

| Tarefa | `metrics` | Observação |
|---|---|---|
| `binary` | `auc_val`, `gini_val` | AUC calculada com `predict_proba[:,1]`; Gini é `2*AUC-1`. |
| `regression` | `rmse_val` | RMSE calculado sobre `model.predict(X_val)`. |

`importance` é `model.feature_importances_`, um array por feature. Na biblioteca atual ele é normalizado a partir da soma da explicação global do treino quando `compute_importance` está habilitado no fit.

O helper não devolve as máscaras locais por linha nem chama `model.explain`. Se a pergunta exige explicação individual, use a API apropriada e valide seu significado separadamente.

## 9. Como usar este recurso no Hub?

Regressão usa target numérico 1-D, embora o wrapper o remodele internamente para o fit:

```python
import numpy as np
from hub_snippets.ml.tabnet_wrapper import train_tabnet

y_train_reg = np.asarray(y_train_reg, dtype=np.float32).reshape(-1)
y_val_reg = np.asarray(y_val_reg, dtype=np.float32).reshape(-1)
assert np.isfinite(y_train_reg).all() and np.isfinite(y_val_reg).all()
modelo_reg, metricas_reg, importancia_reg = train_tabnet(
    X_train, y_train_reg, X_val, y_val_reg,
    task="regression", log_mlflow=False,
)
# metricas_reg contém rmse_val, na unidade do target.
```

As matrizes seguem `float32`, mesma largura e alinhamento com os respectivos targets.

`log_mlflow=False` desliga apenas as chamadas explícitas de registro deste wrapper. Não desativa autologging já configurado na sessão nem garante ausência de logs/caches da biblioteca. Confira o estado da sessão e o destino antes de treinar.

```python
import numpy as np
from hub_snippets.ml.tabnet_wrapper import train_tabnet

X_train = np.asarray(X_train, dtype=np.float32)
X_val = np.asarray(X_val, dtype=np.float32)
assert np.isfinite(X_train).all() and np.isfinite(X_val).all()
assert set(np.asarray(y_train).reshape(-1)) == {0, 1}
assert set(np.asarray(y_val).reshape(-1)) == {0, 1}
model, metrics, importance = train_tabnet(
    X_train, y_train,
    X_val, y_val,
    task="binary",
    n_d=16,
    n_a=16,
    n_steps=4,
    log_mlflow=False,
)
```

O notebook instala pytorch-tabnet e reinicia o Python. A importância global resulta das máscaras/explicações do modelo; não é causalidade nem substitui explicação individual.

Com MLflow habilitado, o wrapper registra apenas `algorithm`, `n_d`, `n_a`, `n_steps` e as métricas retornadas; não registra automaticamente toda a configuração nem o modelo por chamada própria.

## 10. Decisões e configurações que mais importam

`n_d` controla largura do caminho de decisão e `n_a` a largura da atenção; `n_steps` define quantidade de passos. Mais capacidade pode aumentar custo e risco de overfitting; não há melhor valor universal.

No binário, o wrapper fixa `gamma=1.5`, `lambda_sparse=1e-4`, learning rate 0,02 e scheduler StepLR. Na regressão esses argumentos não são todos explicitados, então defaults da biblioteca podem diferir. Comparar os dois modos exige ler os parâmetros efetivos do modelo.

`batch_size` é passado ao fit, enquanto a biblioteca também possui `virtual_batch_size` próprio que o wrapper não expõe. A documentação do `pytorch-tabnet` recomenda que o virtual batch seja coerente com o batch; confirme a configuração efetiva ao mudar tamanhos.

## 11. Limitações, riscos e armadilhas

O wrapper não escolhe device explicitamente; a biblioteca decide conforme sua configuração/default. Ambiente e versão podem alterar CPU/GPU disponíveis e tempo de treino.

`feature_importances_` não garante valor zero para ruído, não identifica direção do efeito e não substitui validação local. Também não há garantia de que toda feature receba importância não nula.

O suporte categórico depende de codificação correta e do comportamento da versão instalada. O notebook instala a dependência sem pin, enquanto a biblioteca `pytorch-tabnet` pode evoluir. Registre versões em experimentos reproduzíveis.

## 12. Quais são as alternativas?

[train_lgbm](../train_lgbm/README.md), [train_catboost](../train_catboost/README.md) e [train_xgboost](../train_xgboost/README.md) são baselines de árvores para comparar sob o mesmo protocolo. [mlp_embeddings](../mlp_embeddings/README.md) oferece outra arquitetura neural quando embeddings categóricas são o foco.

Se uma referência linear resolve o problema com qualidade suficiente e menor custo, complexidade adicional pode não ser necessária. A decisão deve considerar ganho, estabilidade, latência, manutenção e explicabilidade.

## 13. Como saber se o resultado faz sentido?

Recalcule a métrica de validação a partir das previsões. Compare o vetor de importância com features-sinal conhecidas em dados sintéticos ou com análises independentes, sem concluir causalidade.

Repita o treino sob sementes/janelas relevantes quando estabilidade importar. Verifique se o early stopping realmente ocorreu, quais parâmetros efetivos ficaram no modelo e se a validação contém as classes necessárias.

## 14. Arquivos relacionados e próximos passos

A [implementação](tabnet_wrapper.py) define o wrapper; a [fachada](__init__.py) exporta `SEED` e `train_tabnet`; o [notebook](exemplo_tabnet_wrapper.py) demonstra classificação binária e importância. O [guia da coleção](../../README.md) e o [Manual Técnico](../../../MANUAL_TECNICO.md#catalogo-helpers) mantêm a visão integrada.

Se o candidato continuar competitivo, avalie predição fora da amostra, custo e explicações locais separadamente antes de produção.

## 15. Referências

O [registro histórico de testes](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/docs/sprints/readmes_objetos/RELATORIO_R05.md) identifica execução local em 12/09/2026. O arquivo de versões citado ali não está no pacote operacional; não infira uma versão homologada a partir de instalação sem pin. Confira a versão efetiva e execute os dois modos no destino antes de considerá-los validados.

Consulte pytorch-tabnet e a implementação de feature_importances_ na versão testada. Compare custo e qualidade com um baseline sob a mesma partição e valide a arquitetura no runtime de destino.

Referências primárias de conceito/API: [repositório oficial `pytorch-tabnet`](https://github.com/dreamquark-ai/tabnet), [`_compute_feature_importances`](https://github.com/dreamquark-ai/tabnet/blob/develop/pytorch_tabnet/abstract_model.py).
