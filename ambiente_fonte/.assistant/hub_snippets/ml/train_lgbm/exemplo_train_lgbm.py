# Databricks notebook source
# MAGIC %md
# MAGIC # `train_lgbm` — um baseline de árvore para comparação tabular
# MAGIC
# MAGIC **O problema.** Sem uma referência tabular consistente, não há como saber se a complexidade de outro modelo acrescentou valor. Um baseline ajuda a comparar qualidade, custo e estabilidade sob o mesmo protocolo.
# MAGIC
# MAGIC **O que este helper faz.** Treina LightGBM com parâmetros conservadores por tarefa, early stopping e métricas padronizadas.

# MAGIC
# MAGIC **Guia local completo:** [README deste modelo](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `lightgbm` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~1 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install lightgbm

# COMMAND ----------
# MAGIC %restart_python

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparação
# MAGIC
# MAGIC `%restart_python` reinicia o interpretador, então tudo — inclusive o
# MAGIC `sys.path` — precisa vir **depois** dele.

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np

rng = np.random.default_rng(42)

from hub_snippets.ml.train_lgbm import DEFAULT_PARAMS_BINARY, train_lightgbm_baseline

# COMMAND ----------
# MAGIC %md
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Um problema binário com sinal moderado

# COMMAND ----------

n = 6000
X = rng.normal(0, 1, (n, 8))
# só as três primeiras colunas carregam sinal; as outras cinco são ruído
logito = 1.2 * X[:, 0] - 0.8 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0, 0.8, n)
y = (logito > 1.0).astype(int)

corte = 4500
X_tr, y_tr = X[:corte], y[:corte]
X_va, y_va = X[corte:], y[corte:]
print(f"treino {X_tr.shape} | validacao {X_va.shape} | prevalencia {y.mean():.3f}")

# COMMAND ----------

modelo, metricas = train_lightgbm_baseline(X_tr, y_tr, X_va, y_va, task="binary", log_mlflow=False)
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC auc_train                0.9728
# MAGIC auc_val                  0.9268
# MAGIC gini_val                 0.8536
# MAGIC overfit_gap              0.0460
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** `overfit_gap` é a diferença de AUC entre treino e validação: aqui foi **0,0460**. O helper não define limiar que transforme esse valor em “pequeno” ou “grande”. Interprete-o junto da partição, variabilidade e custo da decisão; gap baixo também pode coexistir com leakage compartilhado entre treino e validação.
# MAGIC
# MAGIC O `early stopping` parou na iteração **57**, de 500 disponíveis. Isso
# MAGIC também é informação: nesta execução a validação deixou de melhorar antes do
# MAGIC orçamento inteiro. Se o treino alcançar o limite, investigue curva, custo e validação antes de decidir se aumentar `n_estimators` faz sentido.
# MAGIC
# MAGIC O `gini_val` de 0,8536 é só o AUC reescalado (`2 × AUC − 1`) — aparece
# MAGIC porque a tradição de crédito reporta assim, não porque acrescente algo.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Os parâmetros padrão são uma decisão, não um acaso

# COMMAND ----------

for chave, valor in DEFAULT_PARAMS_BINARY.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC learning_rate            0.05
# MAGIC num_leaves               31
# MAGIC max_depth                -1
# MAGIC min_child_samples        20
# MAGIC subsample                0.8
# MAGIC colsample_bytree         0.8
# MAGIC reg_alpha                0.1
# MAGIC reg_lambda               0.1
# MAGIC n_estimators             500
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O bloco histórico acima é um extrato: a constante atual também contém `objective`, `metric`, `random_state` e `verbose`, que a célula Python imprime. Use `DEFAULT_PARAMS_BINARY` e `model.get_params()` como inventário técnico; não conte o bloco colado como lista completa. Alguns valores coincidem com defaults da biblioteca e outros são escolhas locais.
# MAGIC
# MAGIC `learning_rate` 0,05, `n_estimators` 500, regularização e `colsample_bytree=0,8` são escolhas locais a revisar. Um detalhe importante: `subsample=0,8` **não habilita sozinho bagging de linhas** porque o wrapper não define `subsample_freq` e o default LightGBM é 0 (desabilitado). A amostragem de colunas em 0,8, por outro lado, está ativa.
# MAGIC
# MAGIC O ponto de expor a constante é que **ela seja discutível**. Parâmetro
# MAGIC escondido dentro da função é parâmetro que ninguém revisa.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como modelo final, sem ajuste.** É baseline: serve de piso, não de entrega.
# MAGIC - **Sem comparar com referência simples.** Em problemas menores ou mais lineares, regressão regularizada pode ser competitiva e mais simples; meça em vez de presumir.
# MAGIC - **Sem separar validação no tempo.** O early stopping usa a validação; se ela vier de sorteio, o corte é otimista.
# MAGIC - **Quando sua governança exige rastreabilidade e o logging foi desligado.** O laboratório usa `False`; em produção, siga a política de experimentos do ambiente em vez de assumir um padrão universal.
