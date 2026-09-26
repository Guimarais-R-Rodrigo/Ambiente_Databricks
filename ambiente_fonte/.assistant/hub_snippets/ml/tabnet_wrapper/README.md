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

```python
from hub_snippets.ml.tabnet_wrapper import train_tabnet

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

O [notebook](exemplo_tabnet_wrapper.py) instala `pytorch-tabnet` e reinicia o Python. Nesta R05, a prosa é ajustada para não apresentar máscaras como explicação causal ou afirmar que TabNet é universalmente “último recurso”.

Com MLflow habilitado, o wrapper registra apenas `algorithm`, `n_d`, `n_a`, `n_steps` e as métricas retornadas; não registra automaticamente toda a configuração nem o modelo por chamada própria.

## 10. Decisões e configurações que mais importam

`n_d` controla largura do caminho de decisão e `n_a` a largura da atenção; `n_steps` define quantidade de passos. Mais capacidade pode aumentar custo e risco de overfitting; não há melhor valor universal.

No binário, o wrapper fixa `gamma=1.5`, `lambda_sparse=1e-4`, learning rate 0,02 e scheduler StepLR. Na regressão esses argumentos não são todos explicitados, então defaults da biblioteca podem diferir. Comparar os dois modos exige ler os parâmetros efetivos do modelo.

`batch_size` é passado ao fit, enquanto a biblioteca também possui `virtual_batch_size` próprio que o wrapper não expõe. A documentação do `pytorch-tabnet` recomenda que o virtual batch seja coerente com o batch; confirme a configuração efetiva ao mudar tamanhos.

## 11. Limitações, riscos e armadilhas

O wrapper não escolhe device explicitamente; a biblioteca decide conforme sua configuração/default. Ambiente e versão podem alterar CPU/GPU disponíveis e tempo de treino.

`feature_importances_` não garante valor zero para ruído, não identifica direção do efeito e não substitui validação local. A frase histórica do notebook “como no SHAP, nada recebe zero” não é uma propriedade garantida nem do SHAP nem desta implementação e não deve orientar interpretação.

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

Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. O [repositório oficial `pytorch-tabnet`](https://github.com/dreamquark-ai/tabnet) documenta parâmetros, tarefas e instalação. A implementação oficial de [`_compute_feature_importances`](https://github.com/dreamquark-ai/tabnet/blob/develop/pytorch_tabnet/abstract_model.py) mostra a agregação/normalização da explicação global usada em `feature_importances_`.

A evidência de runtime desta R05 será registrada no relatório. Sem publicação Databricks, homologação de workspace ou auditoria independente presumida.