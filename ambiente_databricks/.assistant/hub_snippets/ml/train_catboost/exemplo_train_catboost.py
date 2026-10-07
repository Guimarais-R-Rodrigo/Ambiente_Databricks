# Databricks notebook source
# MAGIC %md
# MAGIC # `train_catboost` — o baseline para quando há categórica de verdade
# MAGIC
# MAGIC **O problema.** One-hot pode tornar uma matriz de alta cardinalidade muito larga. Target encoding sem separação adequada pode vazar o alvo; ambos continuam sendo alternativas quando preparados e avaliados corretamente.
# MAGIC
# MAGIC **O que este helper faz.** Treina CatBoost com tratamento categórico declarado. As estatísticas ordenadas/permutadas reduzem fontes de viés, mas não garantem ausência de leakage temporal ou de entidade.

# MAGIC
# MAGIC **Guia local completo:** [README deste modelo](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `catboost` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma — o módulo desliga a escrita de log do CatBoost |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~1 min no Free; no trabalho, confirme a política do workspace |

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
# MAGIC Este exemplo passa log_mlflow=False para desativar apenas o registro explícito do helper. Antes de habilitar tracking, confirme dependência, experimento, permissões, configuração do runtime e autologging da sessão. Uma falha numa configuração de serverless não determina o suporte em outras configurações.

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
modelo, metricas = train_catboost_baseline(
    X_tr, y_tr, X_va, y_va, task="binary", cat_features=[2], log_mlflow=False,
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
# MAGIC O que importa é que ele **encontrou** esse sinal com uma coluna de 200 níveis, sem one-hot manual. O CatBoost usa mecanismos de estatísticas categóricas ordenadas/permutadas para reduzir o viés e o vazamento do target durante o treino. Essa “ordem” é parte do algoritmo e **não equivale ao tempo real de disponibilidade do dado**: point-in-time continua sendo responsabilidade da construção da base.
# MAGIC
# MAGIC **Duas armadilhas que este notebook mostra na prática**, ambas
# MAGIC encontradas ao executar e não ao ler:
# MAGIC
# MAGIC 1. `np.column_stack` promove tudo a float, e aí o CatBoost recusa a
# MAGIC    coluna. A mensagem é longa e não diz "converta para inteiro" — diz que
# MAGIC    o array é de ponto flutuante, "o que significa nenhuma feature
# MAGIC    categórica".
# MAGIC O wrapper usa allow_writing_files=False para evitar arquivos auxiliares como catboost_info no diretório de trabalho. params_override={"allow_writing_files": True} habilita essa escrita; só use essa opção com um destino de trabalho e efeito pretendidos.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem declarar corretamente as categóricas.** Em ndarray numérico, um código nominal pode ser tratado como número; em outros tipos, a biblioteca pode falhar. Confira `cat_features` e os tipos.
# MAGIC - **Quando não há razão específica para CatBoost.** Sem categóricas relevantes, compare custo e qualidade com outros baselines em vez de presumir vantagem ou desvantagem.
# MAGIC - **Em tuning caro sem orçamento definido.** O custo relativo depende de dados, hardware e parâmetros; escolha a estratégia de busca por evidência do seu ambiente.
