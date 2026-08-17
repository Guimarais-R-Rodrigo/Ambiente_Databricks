# Databricks notebook source
# MAGIC %md
# MAGIC # `train_lgbm` — o baseline que quase sempre ganha
# MAGIC
# MAGIC **O problema.** Começar um problema tabular por rede neural custa semanas e costuma perder para uma árvore ajustada em minutos. Sem baseline, não há como saber se o modelo complexo valeu.
# MAGIC
# MAGIC **O que este helper faz.** Treina LightGBM com parâmetros conservadores por tarefa, early stopping e métricas padronizadas.

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
# MAGIC | Diferença Free × trabalho | a instalação leva ~3 min no Free; no trabalho, confirme a política do workspace |

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
# MAGIC **Como ler.** Comece pelo `overfit_gap`, que é a diferença entre treino e
# MAGIC validação: **0,0460**. É pequeno, e pequeno é o que se quer. Um baseline com
# MAGIC AUC de treino 0,99 e validação 0,85 decorou, e o número que ele reporta não
# MAGIC vai se repetir em produção.
# MAGIC
# MAGIC O `early stopping` parou na iteração **57**, de 500 disponíveis. Isso
# MAGIC também é informação: o problema é fácil o bastante para não precisar do
# MAGIC orçamento inteiro. Se ele fosse até o limite, valeria aumentar.
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
# MAGIC **Como ler.** Nenhum destes valores é o padrão do LightGBM: são uma escolha
# MAGIC conservadora, e vale saber qual.
# MAGIC
# MAGIC `learning_rate` 0,05 em vez de 0,1 troca velocidade por estabilidade —
# MAGIC combinado com `n_estimators` 500 e early stopping, deixa o modelo parar
# MAGIC sozinho no ponto certo. `subsample` e `colsample_bytree` em 0,8 introduzem
# MAGIC aleatoriedade que reduz variância. `reg_alpha` e `reg_lambda` mantêm
# MAGIC regularização mínima ligada por padrão, o que é decisão de gosto defensável
# MAGIC — muita gente prefere começar em zero.
# MAGIC
# MAGIC O ponto de expor a constante é que **ela seja discutível**. Parâmetro
# MAGIC escondido dentro da função é parâmetro que ninguém revisa.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como modelo final, sem ajuste.** É baseline: serve de piso, não de entrega.
# MAGIC - **Em base pequena.** Com poucos milhares de linhas, regressão logística regularizada costuma empatar e é explicável.
# MAGIC - **Sem separar validação no tempo.** O early stopping usa a validação; se ela vier de sorteio, o corte é otimista.
# MAGIC - **Com `log_mlflow=False` em produção.** Aqui é contorno de laboratório; lá, o registro é o que torna o resultado auditável.
