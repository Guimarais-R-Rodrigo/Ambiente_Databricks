# Databricks notebook source
# MAGIC %md
# MAGIC # `drift_detector` — a distribuição mudou, ou só a média?
# MAGIC
# MAGIC **O problema.** A forma natural de checar se algo mudou entre dois períodos
# MAGIC é comparar as médias. Duas distribuições podem ter a mesma média e formas
# MAGIC completamente diferentes — uma concentrada, outra partida em dois grupos — e
# MAGIC a comparação de médias não vê nada. Num modelo em produção, é a forma que
# MAGIC decide se o score continua significando o que significava.
# MAGIC
# MAGIC **O que este script faz.** Calcula o PSI entre dois recortes da mesma
# MAGIC tabela, com bins derivados do período de referência.

# MAGIC
# MAGIC **Guia local completo:** [README deste script](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados aqui a partir de `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | uma view temporária de sessão |
# MAGIC | Diferença Free × trabalho | o script tem guarda de `cache()`; degrada sem ele no serverless |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_scripts.drift_detector import drift_detector
from hub_snippets.testing import fixtures

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparo — duas safras com a **mesma média** e formas diferentes
# MAGIC
# MAGIC A construção é deliberada: o período de comparação tem a distribuição
# MAGIC partida em dois grupos, com média praticamente igual à do período de
# MAGIC referência. É o caso que a comparação de médias não enxerga.

# COMMAND ----------

import random
from pyspark.sql import functions as F

rng = random.Random(42)
linhas = []
for i in range(4000):
    # referência: concentrada em torno de 600
    linhas.append((f"c{i:05d}", "2026-S1", round(rng.gauss(600, 40), 1)))
for i in range(4000):
    # comparação: metade em 520, metade em 680 — mesma média, forma outra
    centro = 520 if rng.random() < 0.5 else 680
    linhas.append((f"d{i:05d}", "2026-S2", round(rng.gauss(centro, 25), 1)))

populacao = spark.createDataFrame(linhas, "id string, safra string, score double")
populacao.createOrReplaceTempView("vw_exemplo_drift")

display(
    populacao.groupBy("safra").agg(
        F.round(F.avg("score"), 2).alias("media"),
        F.round(F.stddev("score"), 2).alias("desvio"),
        F.count("*").alias("linhas"),
    ).orderBy("safra")
)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Executado no laboratório:
# MAGIC
# MAGIC ```text
# MAGIC safra      media   desvio  linhas
# MAGIC 2026-S1   599.75    40.12    4000
# MAGIC 2026-S2   596.56    83.84    4000
# MAGIC ```
# MAGIC
# MAGIC As médias diferem em **0,53%**. Um relatório que compare só médias conclui
# MAGIC "sem mudança" e encerra o assunto. O desvio dobra e dá o primeiro sinal —
# MAGIC mas desvio também é um número só, e distribuições diferentes podem
# MAGIC compartilhá-lo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que o PSI vê

# COMMAND ----------

import json

resultado = drift_detector(
    "vw_exemplo_drift",
    date_col="safra",
    date_ref="2026-S1",
    date_comp="2026-S2",
    cols=["score"],
    num_bins=10,
)
print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O PSI sai em **2,94** — contra um limiar usual de 0,25 para
# MAGIC "mudança crítica". Ele compara a **forma**: cada bin do período de
# MAGIC referência recebe uma proporção diferente no período de comparação, e a soma
# MAGIC dessas diferenças é o índice.
# MAGIC
# MAGIC Os buckets mostram onde a mudança está. Na referência cada bin tem ~10% das
# MAGIC linhas, por construção dos quantis. Na comparação, o primeiro bin recebe
# MAGIC **44,8%** e o último **42,2%**, enquanto os do meio ficam com menos de 1%:
# MAGIC é a distribuição partida em dois grupos, exatamente como foi construída.
# MAGIC
# MAGIC Dois detalhes de implementação que mudam a interpretação:
# MAGIC
# MAGIC - **Os bins vêm da referência**, não de cada período. Se cada um definisse
# MAGIC   os seus próprios quantis, as duas distribuições ficariam parecidas por
# MAGIC   construção e o índice ficaria sistematicamente baixo.
# MAGIC - **Os limiares são heurística calibrável.** As faixas usuais (0,1 e 0,25)
# MAGIC   vêm da tradição de crédito e não são lei. Num score que muda de escala a
# MAGIC   cada retreino, elas disparam sem que nada esteja errado.
# MAGIC
# MAGIC O erro de interpretação mais provável: tratar PSI alto como "o modelo
# MAGIC piorou". **Drift de dados não implica queda de performance.** São coisas
# MAGIC distintas, e a única forma de saber a segunda é medir a performance.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este script
# MAGIC
# MAGIC - **Como prova de que o modelo degradou.** Ele mede mudança na entrada.
# MAGIC   Performance se mede com o alvo realizado, que costuma chegar depois.
# MAGIC - **Com bins demais em base pequena.** Bin quase vazio infla o índice por
# MAGIC   ruído. Com poucos milhares de linhas, dez bins já é bastante.
# MAGIC - **Em variável categórica.** O script seleciona colunas numéricas e faz
# MAGIC   `cast("double")`; passar uma coluna de texto explicitamente quebra em
# MAGIC   `approxQuantile`, não devolve um índice ruim. Para categórica, o caminho é
# MAGIC   `hub_snippets.ml.drift_detection`, que calcula CSI.
# MAGIC - **Comparando períodos de tamanhos muito diferentes** sem olhar a
# MAGIC   contagem: o índice não avisa que um dos lados tem pouca base.
