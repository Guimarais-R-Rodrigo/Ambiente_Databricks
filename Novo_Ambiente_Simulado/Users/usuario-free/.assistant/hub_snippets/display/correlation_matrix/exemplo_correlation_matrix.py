# Databricks notebook source
# MAGIC %md
# MAGIC # `display.correlation_matrix` — correlação sem ler cem números
# MAGIC
# MAGIC **O problema.** Uma matriz de correlação com 15 variáveis tem 105 pares. Impressa como tabela, ninguém encontra o par que importa — e o par que importa costuma ser o que denuncia redundância ou vazamento.
# MAGIC
# MAGIC **O que este objeto oferece.** Desenha a matriz como mapa de calor, destacando o que passa de um limiar declarado.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | `plotly`, já presente no runtime |
# MAGIC | Dados | sintéticos, com correlação plantada |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | **sim** — `pyspark.ml` clássico não roda no serverless; ver a seção 2 |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.display.correlation_matrix import plot_correlation

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base com redundância plantada

# COMMAND ----------

import numpy as np
from pyspark.sql import functions as F

rng = np.random.default_rng(42)
n = 3000
renda = rng.normal(5000, 1500, n)
base = spark.createDataFrame(
    [
        (float(renda[i]),
         # limite_credito e quase uma copia de renda: correlacao ~0,97
         float(renda[i] * 3 + rng.normal(0, 400)),
         float(rng.normal(40, 12)),
         float(rng.normal(0, 1)))
        for i in range(n)
    ],
    "renda double, limite_credito double, idade double, ruido double",
)
print(f"linhas: {base.count()} | colunas: {len(base.columns)}")

# COMMAND ----------

try:
    plot_correlation(base, threshold_highlight=0.8)
except Exception as erro:
    print("não executou neste runtime:")
    print(f"  {type(erro).__name__}: {str(erro).splitlines()[0][:150]}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC linhas: 3000 | colunas: 4
# MAGIC não executou neste runtime:
# MAGIC   Py4JError: An error occurred while calling
# MAGIC   None.org.apache.spark.ml.feature.VectorAssembler
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A base foi construída com `limite_credito` valendo três vezes a
# MAGIC `renda` mais um ruído pequeno — correlação de cerca de 0,97 por construção.
# MAGIC Em compute clássico o mapa mostraria esse par destacado, e as outras duas
# MAGIC colunas próximas de zero.
# MAGIC
# MAGIC O par redundante é o achado que este helper existe para produzir: duas
# MAGIC variáveis quase idênticas num modelo dividem a importância entre si, e cada
# MAGIC uma parece menos relevante do que é. Em modelo linear, a instabilidade é
# MAGIC pior — os coeficientes podem até trocar de sinal.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Para concluir causalidade.** Correlação alta entre renda e limite não diz qual determina qual — neste caso, sabemos, porque plantamos.
# MAGIC - **Com variável categórica codificada como número.** A correlação de Pearson sobre código de agência mede a ordem do código, que não significa nada.
# MAGIC - **Como único critério de seleção de feature.** Correlação com o alvo ignora interação; variável fraca sozinha pode ser forte em par.
# MAGIC - **Amostrando por medo do driver.** Não precisa: o cálculo é distribuído (`Correlation.corr` do MLlib) e o que volta é a matriz k×k, não as linhas. Amostrar aqui perde precisão de graça. O custo cresce com o número de **colunas**, não de linhas — e acima de umas trinta o mapa deixa de ser legível antes de o cálculo pesar.
