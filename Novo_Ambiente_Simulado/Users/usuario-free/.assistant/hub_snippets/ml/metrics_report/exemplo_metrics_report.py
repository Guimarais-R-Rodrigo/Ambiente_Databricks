# Databricks notebook source
# MAGIC %md
# MAGIC # `metrics_report` — métricas sob população e threshold declarados
# MAGIC
# MAGIC **O problema.** Acurácia é a primeira métrica que todo mundo olha e a mais enganosa em risco: com 5% de eventos, responder "não" para todo mundo acerta 95%. E o limiar de 0,5, que vem por padrão em toda biblioteca, é uma escolha de negócio disfarçada de neutro.
# MAGIC
# MAGIC **O que este helper faz.** Devolve métricas binárias e de regressão. As métricas hard usam o threshold declarado; `ks_pct` está na escala 0–100.
# MAGIC
# MAGIC **Guia local completo:** [README deste objeto](README.md).

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side**, sobre numpy/pandas |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np

rng = np.random.default_rng(42)

from hub_snippets.ml.metrics_report import calculate_binary_metrics

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base desbalanceada, como quase toda base de risco

# COMMAND ----------

# 5% de eventos: prevalência típica de inadimplência, churn ou fraude.
n = 5000
y = (rng.random(n) < 0.05).astype(int)
# Score correlacionado com o alvo, mas longe de perfeito.
p = np.clip(0.03 + 0.35 * y + rng.normal(0, 0.10, n), 0.001, 0.999)

m = calculate_binary_metrics(y, p)
for k, v in m.items():
    print(f"  {k:24} {v}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC auc_roc      0.9925     f1           0.2263
# MAGIC ks_pct      92.1        precision    1.0
# MAGIC gini         0.985      recall       0.1276
# MAGIC auc_pr       0.9252     lift_10pct   9.71
# MAGIC brier_score  0.0269     prevalence   0.0486
# MAGIC
# MAGIC limiar 0.10 -> precisão 0.173 | recall 0.996 | f1 0.295
# MAGIC limiar 0.30 -> precisão 0.910 | recall 0.794 | f1 0.848
# MAGIC limiar 0.50 -> precisão 1.000 | recall 0.128 | f1 0.226
# MAGIC limiar 0.70 -> precisão 0.000 | recall 0.000 | f1 0.000
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Comece por `prevalence`, que sai em **0,0486**: menos de
# MAGIC cinco eventos em cada cem. Um modelo que responda "não" para todo mundo
# MAGIC acerta 95,1% dos casos nesta base — e é por isso que **acurácia não está
# MAGIC entre as dez chaves devolvidas**. A omissão é deliberada: a métrica que
# MAGIC todo mundo pede primeiro é a que menos informa aqui, e oferecê-la seria
# MAGIC convidar a comparação errada.
# MAGIC
# MAGIC Precisão e recall descrevem consequências diferentes do corte e mudam com o threshold. AUC resume ordenação, mas não escolhe política operacional nem substitui calibração, custo ou capacidade.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O limiar padrão é uma escolha, não um neutro

# COMMAND ----------

for corte in (0.10, 0.30, 0.50, 0.70):
    r = calculate_binary_metrics(y, p, threshold=corte)
    print(f"  limiar {corte:.2f} -> precisão {r['precision']:.3f} | "
          f"recall {r['recall']:.3f} | f1 {r['f1']:.3f}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O mesmo modelo, os mesmos scores, quatro pares de números
# MAGIC completamente diferentes. O limiar de 0,5 não tem nada de natural — ele é
# MAGIC o padrão da biblioteca, e em base desbalanceada costuma ser péssimo: com
# MAGIC 5% de prevalência, quase nenhum score passa de 0,5, e o recall despenca.
# MAGIC
# MAGIC Para comparar F1, precisão e recall, mantenha a mesma regra de corte e população; para AUC/AP e outras métricas sem corte, mantenha população, target e protocolo de avaliação comparáveis.
# MAGIC
# MAGIC Quem escolhe o limiar é o negócio: quanto custa um falso positivo contra
# MAGIC um falso negativo. Nenhuma métrica responde isso.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sobre DataFrame do Spark.** É driver-side: colete antes, com limite.
# MAGIC - **Aceitando o limiar padrão em base desbalanceada.** Ele é convenção de
# MAGIC   biblioteca, não decisão de negócio.
# MAGIC - **Comparando f1 entre modelos com limiares diferentes.** Não é
# MAGIC   comparação.
# MAGIC - **Como prova de que o modelo serve.** Estas métricas medem separação na
# MAGIC   base de teste; se o teste vazou, todas ficam ótimas.
