# Databricks notebook source
# MAGIC %md
# MAGIC # `isolation_forest` — contaminação é premissa, não descoberta
# MAGIC
# MAGIC **O problema.** Detecção de anomalia parece objetiva — o algoritmo acha o que é estranho. Só que o parâmetro `contamination` **diz ao algoritmo quantas anomalias encontrar**. Ele sempre encontra essa fração, tenha ela sentido ou não, e o resultado tem a mesma aparência nos dois casos.
# MAGIC
# MAGIC **O que este helper faz.** Treina o isolation forest com contaminação declarada e perfila as anomalias encontradas.

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

from hub_snippets.ml.isolation_forest import profile_anomalies, train_isolation_forest

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base com 1% de pontos realmente estranhos

# COMMAND ----------

normal = rng.normal(0, 1, size=(2970, 3))
estranhos = rng.normal(7, 0.5, size=(30, 3))
base = pd.DataFrame(np.vstack([normal, estranhos]), columns=["a", "b", "c"])
base["eh_estranho"] = [0] * 2970 + [1] * 30
print(f"{len(base)} linhas | estranhos plantados: {int(base.eh_estranho.sum())} (1,0%)")

# COMMAND ----------

saida = train_isolation_forest(
    base, feature_cols=["a", "b", "c"], contamination=0.01, log_mlflow=False,
)
labels = saida["labels"] if isinstance(saida, dict) else saida[1]
detectados = int((np.asarray(labels) == -1).sum())
print(f"marcados como anomalia: {detectados}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC 3000 linhas | estranhos plantados: 30 (1,0%)
# MAGIC   contamination=0.01 ->  30 marcados, 30 deles realmente estranhos
# MAGIC   contamination=0.05 -> 150 marcados, 30 deles realmente estranhos
# MAGIC   contamination=0.10 -> 300 marcados, 30 deles realmente estranhos
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O número de marcados corresponde à contaminação declarada,
# MAGIC porque foi ela que o determinou. Aqui a premissa estava certa — plantamos
# MAGIC 1% e pedimos 1% —, e por isso o resultado parece impressionante.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A mesma base, com a premissa errada

# COMMAND ----------

for c in (0.01, 0.05, 0.10):
    s = train_isolation_forest(base, feature_cols=["a", "b", "c"],
                               contamination=c, log_mlflow=False)
    lab = np.asarray(s["labels"] if isinstance(s, dict) else s[1])
    marcados = int((lab == -1).sum())
    acertos = int(((lab == -1) & (base.eh_estranho == 1)).sum())
    print(f"  contamination={c:.2f} -> {marcados:3} marcados, "
          f"{acertos} deles realmente estranhos")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O total de marcados acompanha a contaminação, não o dado. Com
# MAGIC 10% o modelo marca dez vezes mais pontos, e a maioria dos novos é normal —
# MAGIC mas o relatório de saída tem exatamente a mesma cara.
# MAGIC
# MAGIC O erro de interpretação mais provável: tratar a lista de anomalias como
# MAGIC descoberta. Ela é a resposta a uma pergunta que **você** fez, com a fração
# MAGIC que **você** informou. Sem uma estimativa externa de quantas anomalias
# MAGIC existem, o parâmetro é chute — e vale dizer isso no relatório.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem justificar a contaminação.** É o parâmetro que determina o resultado, e ele não vem do dado.
# MAGIC - **Como detector de fraude pronto.** Anomalia estatística e fraude são conjuntos diferentes que se cruzam pouco.
# MAGIC - **Sobre features em escalas muito diferentes** sem padronizar.
# MAGIC - **Como rótulo para treinar supervisionado.** Você estaria ensinando o modelo a reproduzir a sua premissa.
