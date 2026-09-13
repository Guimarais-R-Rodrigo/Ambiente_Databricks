# Databricks notebook source
# MAGIC %md
# MAGIC # `score_bands` — faixas de score com a direção explícita
# MAGIC
# MAGIC **O problema.** Agrupar score em faixas é o passo antes de qualquer política de aprovação. E a informação que decide tudo — se score alto é bom ou ruim — não está no número: é convenção do modelo, e trocá-la sem perceber inverte a decisão sem mudar a aparência do relatório.
# MAGIC
# MAGIC **O que este helper faz.** Gera bandas por quantil e ordena segundo `higher_score_is_better`. A API possui default `True`, mas em uso real a direção deve ser passada explicitamente para não depender de convenção implícita.

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

from hub_snippets.ml.score_bands import generate_score_bands

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Bandas com a direção declarada

# COMMAND ----------

n = 4000
y = (rng.random(n) < 0.12).astype(int)
score = np.clip(0.06 + 0.40 * y + rng.normal(0, 0.12, n), 0.001, 0.999)

bandas = generate_score_bands(score, y, n_bands=5, higher_score_is_better=False)
print(f"bandas pedidas: 5 | bandas devolvidas: {len(bandas)}")
print(f"fração da base no piso do score (0,001): {100 * (score <= 0.0011).mean():.1f}%")
print(bandas.to_string(index=False))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC bandas pedidas: 5 | bandas devolvidas: 4
# MAGIC fração da base no piso do score (0,001): 26.8%
# MAGIC faixa  score_min  score_max    n  pct_base  n_bom  n_mau  taxa_default
# MAGIC   B01   0.001000   0.046265 1600      40.0   1600      0         0.000
# MAGIC   B02   0.046435   0.116641  800      20.0    799      1         0.125
# MAGIC   B03   0.116694   0.224791  800      20.0    787     13         1.625
# MAGIC   B04   0.224937   0.756304  800      20.0    323    477        59.625
# MAGIC ```
# MAGIC
# MAGIC **Pedimos cinco bandas e vieram quatro** — e a primeira ficou com 40% da
# MAGIC base em vez de 20%. Não é defeito: 26,8% dos scores estão empatados
# MAGIC exatamente no piso de 0,001, porque a fixture faz `clip` ali. Quantis não
# MAGIC conseguem cortar dentro de um empate, então dois cortes coincidem e as
# MAGIC duas primeiras bandas colapsam numa só. O módulo avisa disso na docstring
# MAGIC (*"quantile edges can collapse when scores are tied"*), e aqui a
# MAGIC advertência deixou de ser teórica.
# MAGIC
# MAGIC **A consequência prática:** quem escrever `labels=["A","B","C","D","E"]`
# MAGIC contando com cinco posições recebe um erro de tamanho, ou pior, um
# MAGIC alinhamento silencioso errado. Confira `len(bandas)` antes de assumir
# MAGIC `n_bands`. Score com piso, teto ou muito arredondado — coisa comum em
# MAGIC modelo já em produção — é onde isso acontece.
# MAGIC
# MAGIC Fora isso, `higher_score_is_better=False` diz que score alto significa
# MAGIC **mais risco** — é a convenção de um modelo de propensão a inadimplir. A
# MAGIC taxa de evento cresce da primeira banda para a última: 0,000 → 0,125 →
# MAGIC 1,625 → **59,625**. A concentração na última banda é o que torna o
# MAGIC scorecard útil.
# MAGIC
# MAGIC A implementação **tem** `higher_score_is_better=True` como default. Por isso,
# MAGIC passe a direção explicitamente. Um scorecard de crédito tradicional pode usar
# MAGIC a convenção de score alto = bom cliente, enquanto um score de risco pode inverter isso. Trocar as duas
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
# MAGIC `score_qualidade` ajudam a reduzir ambiguidade. A coluna `aprovacao_acum` do
# MAGIC helper é cobertura cumulativa da base ordenada; só vira aprovação real quando
# MAGIC uma política/cutoff é efetivamente aplicada.

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
