# Databricks notebook source
# MAGIC %md
# MAGIC # `train_xgboost` — o segundo baseline, para conferir o primeiro
# MAGIC
# MAGIC **O problema.** Um baseline só não diz se o resultado é do dado ou da biblioteca. Duas implementações diferentes chegando ao mesmo número é evidência; uma só é anedota.
# MAGIC
# MAGIC **O que este helper faz.** Treina XGBoost com a mesma interface e as mesmas métricas do baseline LightGBM, para comparação direta.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `xgboost` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~1 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install xgboost

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

from hub_snippets.ml.train_xgboost import DEFAULT_PARAMS, train_xgboost_baseline

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
# MAGIC ## 1. A mesma base do baseline LightGBM

# COMMAND ----------

n = 6000
X = rng.normal(0, 1, (n, 8))
logito = 1.2 * X[:, 0] - 0.8 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0, 0.8, n)
y = (logito > 1.0).astype(int)

corte = 4500
X_tr, y_tr = X[:corte], y[:corte]
X_va, y_va = X[corte:], y[corte:]
print(f"treino {X_tr.shape} | validacao {X_va.shape} | prevalencia {y.mean():.3f}")

# COMMAND ----------

modelo, metricas = train_xgboost_baseline(X_tr, y_tr, X_va, y_va, task="binary", log_mlflow=False)
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC auc_val                  0.9302
# MAGIC gini_val                 0.8603
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O baseline LightGBM, sobre **a mesma base e a mesma partição**,
# MAGIC deu `auc_val` **0,9268**. O XGBoost dá **0,9302**. A diferença é de
# MAGIC **0,0034** — três milésimos e meio.
# MAGIC
# MAGIC É esse o resultado que interessa, e ele não é sobre qual biblioteca ganhou.
# MAGIC Duas implementações independentes, com hiperparâmetros diferentes,
# MAGIC chegando ao mesmo lugar dizem que **o número veio do dado**, não de uma
# MAGIC particularidade do algoritmo. Se elas divergissem muito, a suspeita
# MAGIC recairia sobre a configuração, não sobre o problema.
# MAGIC
# MAGIC Escolher o XGBoost por esses três milésimos seria ruído travestido de
# MAGIC decisão. Uma feature nova mexe na segunda casa; a troca de biblioteca, na
# MAGIC terceira.


# COMMAND ----------

print("parametros padrao do XGBoost neste helper:")
for chave, valor in DEFAULT_PARAMS.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** `max_depth` 6 é a diferença conceitual: o XGBoost cresce por
# MAGIC nível e limita profundidade, enquanto o LightGBM cresce por folha e limita
# MAGIC `num_leaves` (31), deixando `max_depth` em −1. São duas estratégias
# MAGIC diferentes de controlar a mesma coisa, e é por isso que copiar
# MAGIC hiperparâmetro de um para o outro não faz sentido.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Para decidir "qual biblioteca é melhor".** A diferença entre elas quase sempre é menor que a de uma feature nova.
# MAGIC - **Com categórica de alta cardinalidade sem tratamento.** Aí o CatBoost costuma levar vantagem real.
# MAGIC - **Sem fixar a semente.** Comparar duas bibliotecas com sementes diferentes compara ruído.
