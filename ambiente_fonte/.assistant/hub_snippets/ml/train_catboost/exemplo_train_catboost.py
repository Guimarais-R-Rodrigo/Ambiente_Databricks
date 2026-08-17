# Databricks notebook source
# MAGIC %md
# MAGIC # `train_catboost` — o baseline para quando há categórica de verdade
# MAGIC
# MAGIC **O problema.** Codificar categórica de alta cardinalidade com one-hot explode a dimensão; com *target encoding* feito à mão, vaza o alvo. As duas saídas usuais são ruins.
# MAGIC
# MAGIC **O que este helper faz.** Treina CatBoost, que trata categórica nativamente com codificação ordenada — construída para não vazar.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `catboost` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma — mas exige `allow_writing_files=False`; ver a célula de treino |
# MAGIC | Diferença Free × trabalho | a instalação leva ~3 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install catboost

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

from hub_snippets.ml.train_catboost import train_catboost_baseline

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
# MAGIC ## 1. Uma base com categórica de alta cardinalidade

# COMMAND ----------

n = 6000
# 200 categorias: one-hot criaria 200 colunas para uma variavel so
categoria = rng.integers(0, 200, n)
efeito = (categoria % 7) * 0.25  # o sinal esta no resto, nao na ordem
# ARMADILHA: `np.column_stack` promove tudo a float, e o CatBoost recusa
# `cat_features` sobre coluna de ponto flutuante:
#   CatBoostError: 'data' is numpy array of floating point numerical type, it
#   means no categorical features, but 'cat_features' specifies nonzero number
# A coluna categorica precisa chegar como inteiro ou texto. Um array de
# `dtype=object` preserva os dois tipos lado a lado.
num_1 = rng.normal(0, 1, n)
num_2 = rng.normal(0, 1, n)
X = np.empty((n, 3), dtype=object)
X[:, 0] = num_1
X[:, 1] = num_2
X[:, 2] = categoria  # inteiro, nao float
y = ((0.9 * num_1 + efeito + rng.normal(0, 0.8, n)) > 1.2).astype(int)

corte = 4500
X_tr, y_tr = X[:corte], y[:corte]
X_va, y_va = X[corte:], y[corte:]
print(f"categorias distintas: {len(np.unique(categoria))} | prevalencia {y.mean():.3f}")

# COMMAND ----------

# `cat_features` recebe o INDICE da coluna, nao o nome: a entrada e ndarray.
# `allow_writing_files=False` NAO e detalhe: sem ele o CatBoost cria uma pasta
# `catboost_info/` no diretorio de trabalho — que no Databricks e a pasta do
# proprio notebook, dentro de `.assistant`. Foram 10 arquivos publicados por
# engano no workspace na primeira execucao deste notebook.
modelo, metricas = train_catboost_baseline(
    X_tr, y_tr, X_va, y_va, task="binary", cat_features=[2], log_mlflow=False,
    params_override={"allow_writing_files": False},
)
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC categorias distintas: 200 | prevalencia 0.368
# MAGIC auc_val                  0.8645
# MAGIC gini_val                 0.7289
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O AUC de 0,8645 não se compara com os 0,93 dos notebooks
# MAGIC anteriores: a base é outra, com o sinal escondido num agrupamento latente
# MAGIC (`categoria % 7`) que nenhuma ordem numérica revela.
# MAGIC
# MAGIC O que importa é que ele **encontrou** esse sinal, com uma coluna de 200
# MAGIC níveis, sem one-hot e sem codificação manual. O CatBoost usa codificação
# MAGIC ordenada: para cada linha, a estatística da categoria é calculada só com
# MAGIC as linhas **anteriores** dela. É a mesma ideia do ponto no tempo que o
# MAGIC `pit_join` aplica ao dado, aqui aplicada à codificação — e é o que impede
# MAGIC o *target encoding* de vazar o alvo.
# MAGIC
# MAGIC **Duas armadilhas que este notebook mostra na prática**, ambas
# MAGIC encontradas ao executar e não ao ler:
# MAGIC
# MAGIC 1. `np.column_stack` promove tudo a float, e aí o CatBoost recusa a
# MAGIC    coluna. A mensagem é longa e não diz "converta para inteiro" — diz que
# MAGIC    o array é de ponto flutuante, "o que significa nenhuma feature
# MAGIC    categórica".
# MAGIC 2. Sem `allow_writing_files=False`, o CatBoost cria `catboost_info/` no
# MAGIC    diretório de trabalho. No Databricks isso é a **pasta do notebook**, e
# MAGIC    a primeira execução deixou dez arquivos de log publicados dentro de
# MAGIC    `.assistant/hub_snippets/ml/train_catboost/`. Foi o `--verify` da
# MAGIC    publicação que apanhou, listando-os como obsoletos no remoto.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem declarar `cat_features`.** Sem isso ele trata a categórica como número, e a ordem inventada vira sinal falso.
# MAGIC - **Quando não há categórica.** O ganho dele está exatamente aí; sem categórica, é mais lento sem contrapartida.
# MAGIC - **Em busca de hiperparâmetro larga.** É o mais lento dos três; use LightGBM para explorar e CatBoost para confirmar.
