# Databricks notebook source
# MAGIC %md
# MAGIC # `display.distribution_grid` — a forma de cada variável, de uma vez
# MAGIC
# MAGIC **O problema.** Olhar variável por variável em base de vinte colunas ou custa vinte células ou não acontece. E o que se procura — cauda, pico em zero, bimodalidade — só aparece na forma, nunca na média.
# MAGIC
# MAGIC **O que este objeto oferece.** Desenha a distribuição de várias colunas numa grade única, com amostragem controlada.

# MAGIC
# MAGIC **Antes de executar:** consulte o [README deste objeto](README.md) para entender o conceito, os requisitos e os efeitos do exemplo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | confira as dependências e a compatibilidade descritas no README; não há equivalência universal entre runtimes |
# MAGIC | Bibliotecas | Plotly disponível; NumPy para gerar os dados sintéticos desta demonstração |
# MAGIC | Dados | sintéticos, com três formas diferentes de propósito |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.display.distribution_grid import plot_distributions

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Três variáveis com formas deliberadamente diferentes

# COMMAND ----------

import numpy as np

rng = np.random.default_rng(42)
n = 5000

simetrica = rng.normal(50, 10, n)
assimetrica = rng.exponential(2000, n)          # cauda longa a direita
bimodal = np.where(rng.random(n) < 0.5,
                   rng.normal(20, 4, n), rng.normal(70, 4, n))

base = spark.createDataFrame(
    [(float(simetrica[i]), float(assimetrica[i]), float(bimodal[i])) for i in range(n)],
    "simetrica double, assimetrica double, bimodal double",
)

# A media sozinha nao distingue nenhuma das tres formas — e por isso que a
# grade existe.
from pyspark.sql import functions as F

base.agg(*[F.round(F.avg(c), 1).alias(f"media_{c}") for c in base.columns]).show()

# COMMAND ----------

plot_distributions(base, ncols=3, sample_n=5000)

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC +---------------+-----------------+-------------+
# MAGIC |media_simetrica|media_assimetrica|media_bimodal|
# MAGIC +---------------+-----------------+-------------+
# MAGIC |           49.8|           1984.9|         45.5|
# MAGIC +---------------+-----------------+-------------+
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Três médias, três formas completamente diferentes — e a tabela
# MAGIC acima não distingue nenhuma delas.
# MAGIC
# MAGIC | Variável | Média | O que a forma mostra |
# MAGIC |---|---:|---|
# MAGIC | `simetrica` | 49,8 | distribuição aproximadamente simétrica; não há garantia de metade exata da amostra de cada lado da média |
# MAGIC | `assimetrica` | 1.984,9 | cauda longa à direita — **a maioria está bem abaixo da média** |
# MAGIC | `bimodal` | 45,5 | dois picos, em ~20 e ~70. **Quase ninguém vale 45** |
# MAGIC
# MAGIC O caso bimodal é o que justifica a grade. A média de 45,5 cai exatamente no
# MAGIC vale entre os dois grupos: é um valor que quase nenhum cliente tem, e que
# MAGIC descreve uma população que não existe. Uma segmentação construída sobre
# MAGIC essa média pode separar os dois grupos, mas resumir ambos pelo mesmo
# MAGIC valor esconde sua heterogeneidade. Aqui os grupos são sintéticos.
# MAGIC
# MAGIC Uma média isolada não mostra os dois picos. O histograma complementa
# MAGIC resumos e quantis; sua leitura depende dos intervalos escolhidos e dos
# MAGIC dados amostrados. O helper usa intervalos automáticos do Plotly, traz os
# MAGIC valores selecionados ao driver e os incorpora na figura. O N do rodapé
# MAGIC é a quantidade de linhas coletadas, não a contagem válida de cada coluna.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Com grade extensa sem ajuste.** O tema fixa altura em 450; confira legibilidade e ajuste a figura após a função, sem tratar um número de colunas como limite universal.
# MAGIC - **Sem olhar o `sample_n`.** A grade desenha a amostra; a cauda rara pode não estar nela, e é justamente a cauda que interessa.
# MAGIC - **Sobre códigos de categorias.** Os intervalos numéricos podem impor uma distância sem significado; prefira contagens por categoria.
