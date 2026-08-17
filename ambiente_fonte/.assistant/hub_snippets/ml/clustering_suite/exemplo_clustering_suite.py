# Databricks notebook source
# MAGIC %md
# MAGIC # `clustering_suite` — escolher k sem fingir que o dado escolheu
# MAGIC
# MAGIC **O problema.** A pergunta "quantos clusters?" não tem resposta no dado. Cotovelo e silhueta são heurísticas que discordam entre si com frequência, e o gráfico do cotovelo quase sempre tem mais de um joelho plausível. Apresentar o k como descoberta esconde que foi escolha.
# MAGIC
# MAGIC **O que este helper faz.** Roda a seleção de k por método declarado e o pipeline completo com padronização, devolvendo o que sustentou a escolha.

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

from hub_snippets.ml.clustering_suite import run_clustering_pipeline, select_k

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Três grupos plantados

# COMMAND ----------

centros = [(0, 0), (6, 6), (0, 7)]
pontos = np.vstack([
    rng.normal(c, 1.0, size=(300, 2)) for c in centros
])
base = pd.DataFrame(pontos, columns=["f1", "f2"])
print(f"{len(base)} pontos, 3 grupos plantados")

# COMMAND ----------

resultado_k = select_k(pontos, k_range=range(2, 8), method="silhouette")
print(resultado_k.to_string(index=False) if hasattr(resultado_k, "to_string") else resultado_k)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A silhueta deve apontar 3, que é o número plantado. Vale
# MAGIC olhar a **distância** entre o melhor e o segundo colocado: quando os dois
# MAGIC estão próximos, a escolha é arbitrária e dizer "o dado indicou 3" é falso.
# MAGIC
# MAGIC Aqui os grupos foram construídos bem separados. Em dado real a curva é
# MAGIC quase sempre mais chata, e é aí que o método vira decisão de negócio: em
# MAGIC quantos segmentos a área consegue operar?

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O pipeline com padronização

# COMMAND ----------

saida = run_clustering_pipeline(
    base, feature_cols=["f1", "f2"], k=3, scaler="standard", log_mlflow=False,
)
print(type(saida))
if isinstance(saida, dict):
    for k in list(saida)[:6]:
        print(f"  {k}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A padronização não é detalhe: k-means mede distância
# MAGIC euclidiana, e uma variável em reais domina outra em anos por três ordens de
# MAGIC grandeza. Sem escalonar, o "cluster" acaba sendo a variável de maior
# MAGIC amplitude, e nada no resultado avisa.
# MAGIC
# MAGIC `log_mlflow=False` está explícito porque este notebook declara não escrever
# MAGIC nada. Em trabalho real, registrar o k escolhido e o método é o que permite
# MAGIC alguém questionar a segmentação depois.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Apresentando k como descoberta.** É escolha, apoiada em heurística que discorda de si mesma.
# MAGIC - **Sem padronizar.** A variável de maior amplitude vira o cluster.
# MAGIC - **Em dado com categórica sem tratamento.** Distância euclidiana sobre código de categoria não significa nada.
# MAGIC - **Como segmentação de negócio pronta.** Cluster é ponto de partida; segmento é decisão com nome, dono e ação.
