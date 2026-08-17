# Databricks notebook source
# MAGIC %md
# MAGIC # `score_bands` — faixas de score com a direção explícita
# MAGIC
# MAGIC **O problema.** Agrupar score em faixas é o passo antes de qualquer política de aprovação. E a informação que decide tudo — se score alto é bom ou ruim — não está no número: é convenção do modelo, e trocá-la sem perceber inverte a decisão sem mudar a aparência do relatório.
# MAGIC
# MAGIC **O que este helper faz.** Gera bandas por quantil **exigindo** que a direção do score seja declarada.

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

from hub_snippets.ml.score_bands import generate_score_bands

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Bandas com a direção declarada

# COMMAND ----------

n = 4000
y = (rng.random(n) < 0.12).astype(int)
score = np.clip(0.06 + 0.40 * y + rng.normal(0, 0.12, n), 0.001, 0.999)

bandas = generate_score_bands(score, y, n_bands=5, higher_score_is_better=False)
print(bandas.to_string(index=False))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** `higher_score_is_better=False` diz que score alto significa
# MAGIC **mais risco** — é a convenção de um modelo de propensão a inadimplir. A
# MAGIC taxa de evento cresce da primeira banda para a última.
# MAGIC
# MAGIC O parâmetro não tem padrão silencioso de propósito. Um scorecard de crédito
# MAGIC tradicional usa a convenção oposta: score alto é bom cliente. Trocar as duas
# MAGIC sem perceber inverte a política de aprovação inteira, e o relatório continua
# MAGIC parecendo certo — as bandas existem, os números somam, e o banco aprova
# MAGIC exatamente quem deveria recusar.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A mesma base com a direção invertida

# COMMAND ----------

invertida = generate_score_bands(score, y, n_bands=5, higher_score_is_better=True)
print(invertida.to_string(index=False))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** É a mesma tabela de cabeça para baixo. Nada no formato avisa
# MAGIC qual das duas é a certa — só quem conhece o modelo sabe.
# MAGIC
# MAGIC Por isso a direção vale como informação a carregar junto do score, na
# MAGIC documentação da tabela e no nome da coluna. `score_risco` e
# MAGIC `score_qualidade` dizem sozinhos o que `score` não diz.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem saber a direção do score.** É o único parâmetro que, errado,
# MAGIC   produz resultado plausível e invertido.
# MAGIC - **Com bandas demais em base pequena.** Cada banda vira ruído; cinco a dez
# MAGIC   é o usual.
# MAGIC - **Comparando bandas entre modelos.** Os cortes vêm dos quantis de cada
# MAGIC   base; a banda 3 de um não é a banda 3 do outro.
# MAGIC - **Como política de aprovação pronta.** A banda organiza; o corte é
# MAGIC   decisão de negócio, com custo assimétrico.
