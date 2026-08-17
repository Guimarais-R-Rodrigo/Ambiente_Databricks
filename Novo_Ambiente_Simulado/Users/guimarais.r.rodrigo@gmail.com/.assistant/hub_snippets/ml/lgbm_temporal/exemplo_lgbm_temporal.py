# Databricks notebook source
# MAGIC %md
# MAGIC # `lgbm_temporal` — lags e janelas, com a entidade no lugar certo
# MAGIC
# MAGIC **O problema.** Criar lag e média móvel é trivial num painel de uma série. Num painel de muitas entidades — clientes, contratos, agências — a mesma operação sem particionar por entidade puxa o valor do **cliente anterior** para dentro da feature. O resultado é plausível, e o modelo aprende ruído.
# MAGIC
# MAGIC **O que este helper faz.** Cria features temporais exigindo a coluna de entidade, e derruba a ambiguidade em vez de assumir uma.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side** |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

from hub_snippets.ml.lgbm_temporal import create_temporal_features

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Um painel de várias entidades

# COMMAND ----------

meses = pd.date_range("2025-01-01", periods=12, freq="MS")
linhas = []
for ent in ("A", "B", "C"):
    nivel = {"A": 100, "B": 500, "C": 900}[ent]
    for m in meses:
        linhas.append({"id": ent, "dt": m, "valor": nivel + float(rng.normal(0, 5))})
painel = pd.DataFrame(linhas).sort_values(["id", "dt"]).reset_index(drop=True)

print(painel.groupby("id")["valor"].mean().round(1).to_string())

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** As três entidades vivem em patamares muito diferentes — 100,
# MAGIC 500 e 900. É de propósito: se o lag vazar entre entidades, a diferença
# MAGIC aparece de forma gritante em vez de se esconder no ruído.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Com a entidade declarada

# COMMAND ----------

com_ent = create_temporal_features(
    painel, target_col="valor", date_col="dt", lags=[1], entity_cols=["id"],
)
col_lag = [c for c in com_ent.columns if "lag" in c.lower()][0]

# A primeira linha de CADA entidade tem lag nulo: não há mês anterior dela.
nulos_por_entidade = com_ent.groupby("id")[col_lag].apply(lambda s: int(s.isna().sum()))
print(f"coluna de lag: {col_lag}")
print(nulos_por_entidade.to_string())

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Cada entidade tem exatamente **um** lag nulo — o primeiro mês
# MAGIC dela. É essa a assinatura de um lag corretamente particionado.
# MAGIC
# MAGIC Se a coluna de entidade fosse esquecida, só a primeira linha do painel
# MAGIC inteiro teria nulo, e a primeira linha de B receberia o último valor de A —
# MAGIC 100 onde deveria haver 500. O número sai, o modelo treina, e ninguém vê.
# MAGIC
# MAGIC A verificação vale como hábito: **conte os nulos por entidade**. Um nulo por
# MAGIC entidade por lag é o esperado; nulos de menos significam vazamento lateral.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem `entity_cols`, em painel de várias entidades.** É o erro que este notebook existe para mostrar.
# MAGIC - **Com o painel desordenado.** Lag pressupõe ordem; ordene por entidade e data antes.
# MAGIC - **Em série com buracos.** Lag de 1 é a linha anterior, não o mês anterior — se faltam meses, os dois deixam de coincidir.
# MAGIC - **Sobre DataFrame do Spark.** É pandas: colete antes, com limite.
