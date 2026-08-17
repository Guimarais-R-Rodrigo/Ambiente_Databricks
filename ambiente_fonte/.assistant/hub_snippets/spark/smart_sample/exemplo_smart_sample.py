# Databricks notebook source
# MAGIC %md
# MAGIC # `smart_sample` — amostra que se reproduz e que preserva o raro
# MAGIC
# MAGIC **O problema.** Amostrar parece trivial: `df.limit(1000)` resolve. Só que
# MAGIC `limit` não amostra — devolve as primeiras linhas que o Spark encontrar, e
# MAGIC a ordem depende da partição. Se os dados chegaram ordenados por data ou por
# MAGIC região, a "amostra" é um recorte enviesado com cara de aleatório.
# MAGIC
# MAGIC **O que este helper faz.** Amostra com semente declarada e, quando pedido,
# MAGIC estratifica — de modo que a categoria rara não desapareça.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from pyspark.sql import functions as F

from hub_snippets.spark.smart_sample import smart_sample
from hub_snippets.testing import fixtures

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparo — uma base com categoria rara
# MAGIC
# MAGIC Acrescentamos um segmento minúsculo à fixture. É o caso que a amostragem
# MAGIC simples costuma engolir.

# COMMAND ----------

base = fixtures.base_tabular(n=5000, seed=42)
# 20 linhas de um segmento raro, contra 5.000 do resto
raros = base.limit(20).withColumn("uf", F.lit("XX"))
populacao = base.unionByName(raros)

display(
    populacao.groupBy("uf").count().orderBy("count")
)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** `XX` tem 20 linhas em 5.020 — 0,4% da base. É o tipo de
# MAGIC categoria que existe em toda base real e some em toda amostra descuidada.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Amostra reprodutível

# COMMAND ----------

a = smart_sample(populacao, n=500, seed=42)
b = smart_sample(populacao, n=500, seed=42)
c = smart_sample(populacao, n=500, seed=7)

print(f"mesma semente : {a.count()} e {b.count()} linhas, conjuntos iguais? "
      f"{a.exceptAll(b).count() == 0}")
print(f"outra semente : {c.count()} linhas, difere de a? {c.exceptAll(a).count() > 0}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Mesma semente, mesma amostra — é o que permite alguém
# MAGIC reproduzir o seu número amanhã. Sem semente declarada, duas execuções dão
# MAGIC resultados diferentes e ninguém sabe se a diferença é do dado ou do sorteio.
# MAGIC
# MAGIC A contagem sai próxima de 500, não exata: amostragem por fração sorteia
# MAGIC linha a linha. Se o seu caso exige exatamente N linhas, o caminho é ordenar
# MAGIC por algo declarado e limitar — assumindo o viés que isso introduz.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Onde a amostra simples falha

# COMMAND ----------

simples = smart_sample(populacao, n=200, seed=42)
estratificada = smart_sample(populacao, n=200, stratify_col="uf", seed=42)

for rotulo, df in [("simples", simples), ("estratificada", estratificada)]:
    raras = df.filter(F.col("uf") == "XX").count()
    print(f"{rotulo:14} {df.count():4} linhas | categoria rara XX: {raras}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Numa amostra de 200 sobre uma categoria que é 0,4% da base, o
# MAGIC esperado é **menos de uma linha** de `XX`. A amostra simples costuma sair
# MAGIC com zero — e uma análise por UF feita sobre ela conclui que `XX` não existe.
# MAGIC
# MAGIC A estratificada preserva a presença de cada categoria. O preço é que ela
# MAGIC **deixa de representar as proporções**: `XX` fica superrepresentada em
# MAGIC relação à base. Isso é adequado para inspecionar todas as categorias, e
# MAGIC errado para estimar uma média global.
# MAGIC
# MAGIC O erro de interpretação mais provável está exatamente aí: usar amostra
# MAGIC estratificada para estimar prevalência. O número sai enviesado na direção da
# MAGIC categoria rara, e nada no resultado avisa.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Estratificada, para estimar média ou prevalência global.** Ela quebra
# MAGIC   as proporções de propósito; a estimativa sai enviesada.
# MAGIC - **Esperando exatamente N linhas.** É fração, não cota.
# MAGIC - **Como substituto de agregação.** Se a pergunta cabe num `groupBy`, faça
# MAGIC   o `groupBy`: amostrar para depois agregar troca exatidão por nada.
# MAGIC - **Em base com partição enviesada, sem conferir.** Amostragem uniforme
# MAGIC   sobre dado mal distribuído continua devolvendo o viés da distribuição.
