# Databricks notebook source
# MAGIC %md
# MAGIC # `drift_detection` — PSI, KS e CSI — três medidas, três perguntas
# MAGIC
# MAGIC **Guia local completo:** [README.md](README.md)
# MAGIC
# MAGIC **O problema.** Quando alguém pergunta se os dados mudaram, a resposta depende de qual mudança importa. PSI compara distribuição numérica por bins da referência, KS mede a maior distância entre distribuições acumuladas e CSI aplica aritmética semelhante a categorias. Nenhum deles, isoladamente, prova que a performance do modelo piorou.
# MAGIC
# MAGIC **O que este helper faz.** Calcula os três e varre várias features no driver. Sem thresholds fornecidos pelo consumidor, retorna evidência com `status=NOT_CLASSIFIED`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico; cálculo local no driver |
# MAGIC | Bibliotecas | NumPy, pandas e SciPy disponíveis no runtime |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | revalide versões; o helper não usa API de workspace |

# COMMAND ----------

import sys
usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")
import numpy as np
import pandas as pd
rng = np.random.default_rng(42)
from hub_snippets.ml.drift_detection import calculate_csi, calculate_ks, calculate_psi, detect_drift_all_features

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Duas populações que diferem em forma, não em média

# COMMAND ----------
ref = rng.normal(600, 40, 4000)
atual = np.where(rng.random(4000) < 0.5, rng.normal(520, 25, 4000), rng.normal(680, 25, 4000))
print(f"média  ref {ref.mean():7.2f} | atual {atual.mean():7.2f}")
print(f"desvio ref {ref.std():7.2f} | atual {atual.std():7.2f}")
print(f"PSI    {calculate_psi(ref, atual):.4f}")
ks_stat, ks_p = calculate_ks(ref, atual)
print(f"KS     {ks_stat:.4f}  (p-valor {ks_p:.2e})")

# COMMAND ----------
# MAGIC %md
# MAGIC O resultado histórico mostra médias próximas e formas muito diferentes. Em amostras grandes, p-valores podem ficar muito pequenos para diferenças de pequena magnitude; interprete estatística, tamanho amostral e impacto operacional em conjunto.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Categórica pede CSI

# COMMAND ----------
cat_ref = pd.Series(rng.choice(["SP", "RJ", "MG", "BA"], 3000, p=[.4, .3, .2, .1]))
cat_atual = pd.Series(rng.choice(["SP", "RJ", "MG", "BA"], 3000, p=[.25, .25, .25, .25]))
print(f"CSI entre as duas distribuições de UF: {calculate_csi(cat_ref, cat_atual):.4f}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Varrer muitas features sem classificar por padrão

# COMMAND ----------
base_ref = pd.DataFrame({"score": ref, "renda": rng.normal(5000, 1200, 4000), "uf": cat_ref.sample(4000, replace=True).values})
base_atual = pd.DataFrame({"score": atual, "renda": rng.normal(5100, 1250, 4000), "uf": cat_atual.sample(4000, replace=True).values})
relatorio = detect_drift_all_features(base_ref, base_atual, feature_cols=["score", "renda", "uf"], numeric_cols=["score", "renda"], categorical_cols=["uf"])
print(relatorio.to_string(index=False) if hasattr(relatorio, "to_string") else relatorio)

# COMMAND ----------
# MAGIC %md
# MAGIC Sem política, `status` permanece `NOT_CLASSIFIED`. Isso separa medida de distribuição de decisão de monitoramento.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. A mesma varredura com política explícita

# COMMAND ----------
com_politica = detect_drift_all_features(base_ref, base_atual, feature_cols=["score", "renda", "uf"], numeric_cols=["score", "renda"], categorical_cols=["uf"], psi_threshold=0.25, ks_threshold=0.10)
print(com_politica[["feature", "psi", "status"]].to_string(index=False))

# COMMAND ----------
# MAGIC %md
# MAGIC `0.25` e `0.10` são apenas valores da demonstração. Calibre thresholds com histórico, tamanho amostral, custo de falso alerta e risco. No contrato atual, warning PSI e KS precisam ser fornecidos juntos.
# MAGIC
# MAGIC **Armadilha adicional:** `min_non_null` descreve corretamente o requisito no ramo numérico; no ramo categórico atual, a implementação compara o comprimento total da série. Se sua categórica tiver muitas ausências, faça uma validação externa da contagem não nula.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - como prova de queda de performance;
# MAGIC - sobre uma base Spark enorme sem amostragem/limite consciente;
# MAGIC - com thresholds copiados como lei universal;
# MAGIC - em categóricas de cardinalidade extrema sem revisar agrupamento e categorias raras.
