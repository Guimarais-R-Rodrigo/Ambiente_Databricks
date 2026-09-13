# Databricks notebook source
# MAGIC %md
# MAGIC # `curves_plotly` — as quatro curvas, e o que cada uma esconde
# MAGIC
# MAGIC **Guia local completo:** [README.md](README.md)
# MAGIC
# MAGIC **O problema.** ROC é uma curva comum de discriminação, mas em base muito desbalanceada ela não deve ser lida sozinha. Cada curva responde a uma pergunta diferente; PR e lift ajudam a enxergar seleção de eventos, enquanto ROC e KS resumem separação sob outras escalas.
# MAGIC
# MAGIC **O que este helper faz.** Gera ROC, precisão-recall, lift cumulativo e KS com o mesmo tema. Ele recebe vetores já no driver; o parâmetro `n` só altera o N mostrado no rodapé e **não subamostra** os dados.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente para o cálculo local |
# MAGIC | Bibliotecas | NumPy, scikit-learn e Plotly disponíveis no runtime |
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side** |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | revalide versões do runtime; não há escrita no workspace |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np

rng = np.random.default_rng(42)

from hub_snippets.ml.curves_plotly import (
    plot_ks_curve, plot_lift_curve, plot_pr_curve, plot_roc_curve,
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base com 2% de eventos

# COMMAND ----------

n = 8000
y = (rng.random(n) < 0.02).astype(int)
p = np.clip(0.015 + 0.30 * y + rng.normal(0, 0.06, n), 0.0005, 0.999)
print(f"linhas: {n} | eventos: {int(y.sum())} ({100 * y.mean():.2f}%)")

# COMMAND ----------

plot_roc_curve(y, p, title="ROC — base com 2% de eventos")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado histórico é:
# MAGIC
# MAGIC ```text
# MAGIC linhas: 8000 | eventos: 148 (1.85%)
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** ROC compara TPR e FPR ao variar o threshold. Em prevalência baixa, examine também PR, lift e capacidade operacional; AUC alta não informa sozinha quantos casos selecionados serão eventos.

# COMMAND ----------

plot_pr_curve(y, p, title="Precisão × recall — a mesma base")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A referência horizontal da PR é a prevalência observada. Nesta fixture histórica foram 148 eventos em 8.000 linhas, 1,85%. Average Precision resume a ordenação sob essa curva, mas não escolhe threshold de negócio.

# COMMAND ----------

plot_lift_curve(y, p, title="Lift por decil")

# COMMAND ----------

plot_ks_curve(y, p, title="KS")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O lift implementado é cumulativo: em cada fração da base ordenada por score, compara eventos capturados com o esperado sob a prevalência. KS usa `TPR - FPR` e destaca a maior separação. Nenhum dos dois prova causalidade ou calibração.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como única evidência em base desbalanceada.** Combine métricas e curvas conforme a decisão.
# MAGIC - **Como prova de calibração.** Nenhuma das quatro verifica frequência observada contra probabilidade prevista.
# MAGIC - **Passando milhões de linhas esperando que `n` limite o custo.** `n` é só metadado visual; amostre antes.
# MAGIC - **Comparando populações incompatíveis.** Mudança de população altera as métricas e precisa ser contextualizada.
# MAGIC
# MAGIC ## Dívida registrada: a paleta daqui tem seis cores
# MAGIC
# MAGIC Este módulo mantém uma `PALETA_CATEGORICA` local de seis cores. A paleta compartilhada em `constants.colors` possui dez. Alterar isso mudaria aparência de gráficos com mais de seis séries e continua sendo decisão visual de produto, fora desta sprint documental.
