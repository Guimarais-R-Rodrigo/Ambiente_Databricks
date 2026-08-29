# Databricks notebook source
# MAGIC %md
# MAGIC # `cluster_profiling` — descrever o cluster sem inventar a persona
# MAGIC
# MAGIC **O problema.** Depois de agrupar, vem o batismo: "cluster 2 é o cliente premium". O nome gruda, viaja para o slide, e ninguém volta para conferir se a diferença que o justificava era grande ou marginal. Perfilar é o passo entre agrupar e nomear, e é o que costuma ser pulado.
# MAGIC
# MAGIC **O que este helper faz.** Descreve cada cluster por variável e aponta quais features mais o diferenciam dos demais.

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

from hub_snippets.ml.cluster_profiling import profile_clusters, top_differentiators

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Um resultado de clusterização

# COMMAND ----------

n = 900
base = pd.DataFrame({
    "renda": np.concatenate([rng.normal(3000, 500, 300), rng.normal(9000, 900, 300),
                             rng.normal(3200, 600, 300)]),
    "idade": np.concatenate([rng.normal(30, 5, 300), rng.normal(48, 6, 300),
                             rng.normal(31, 5, 300)]),
    "produtos": np.concatenate([rng.normal(2, 0.6, 300), rng.normal(5, 1.0, 300),
                                rng.normal(2.1, 0.6, 300)]),
})
base["cluster"] = np.repeat([0, 1, 2], 300)

perfis = profile_clusters(base, feature_cols=["renda", "idade", "produtos"],
                          cluster_col="cluster")
print(perfis.to_string(index=False) if hasattr(perfis, "to_string") else perfis)

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC  cluster   n  pct_total  feature  cluster_mean  global_mean  index  z_score
# MAGIC        0 300       33.3    renda     2979.4605    5040.5970  0.591    -0.72
# MAGIC        0 300       33.3    idade       30.2131      36.1335  0.836    -0.59
# MAGIC        1 300       33.3    renda     8989.8733    5040.5970  1.783     1.37
# MAGIC        1 300       33.3    idade       47.9166      36.1335  1.326     1.18
# MAGIC        2 300       33.3    renda     3152.4571    5040.5970  0.625    -0.66
# MAGIC        2 300       33.3    idade       30.2707      36.1335  0.838    -0.59
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Os clusters 0 e 2 foram construídos **quase idênticos** — de
# MAGIC propósito. O perfil mostra isso: renda, idade e número de produtos ficam
# MAGIC próximos entre os dois, e distantes do cluster 1.
# MAGIC
# MAGIC É a situação que mais produz persona falsa. Nomear 0 e 2 de forma diferente
# MAGIC — "jovem digital" e "jovem tradicional" — inventa uma distinção que os
# MAGIC dados não sustentam, e a partir daí a área trata dois grupos iguais com
# MAGIC estratégias diferentes.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O que de fato diferencia

# COMMAND ----------

for c in (0, 1, 2):
    top = top_differentiators(perfis, cluster_id=c, top_n=2)
    print(f"cluster {c}: {top.to_string(index=False) if hasattr(top, 'to_string') else top}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Para o cluster 1 as diferenças devem ser grandes em todas as
# MAGIC três variáveis. Para 0 e 2, o "top diferenciador" existe — a função sempre
# MAGIC devolve um — mas a magnitude é pequena.
# MAGIC
# MAGIC O erro de interpretação mais provável está aí: **a função devolve um
# MAGIC ranking mesmo quando não há diferença relevante**. Ranking não é evidência
# MAGIC de separação; olhe o tamanho da diferença antes de dar nome ao grupo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Para nomear cluster sem olhar a magnitude.** O ranking existe sempre; a diferença relevante, não.
# MAGIC - **Sobre clusters de tamanhos muito desiguais.** A média de um grupo de vinte é instável.
# MAGIC - **Sem checar sobreposição.** Médias distantes com distribuições sobrepostas não separam ninguém na prática.
# MAGIC - **Como validação da clusterização.** Perfilar descreve o resultado; não diz se k estava certo.
