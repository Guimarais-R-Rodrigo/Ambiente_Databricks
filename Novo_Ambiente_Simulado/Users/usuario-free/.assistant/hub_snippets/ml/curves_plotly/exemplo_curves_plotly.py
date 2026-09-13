# Databricks notebook source
# MAGIC %md
# MAGIC # `curves_plotly` — as quatro curvas, e o que cada uma esconde
# MAGIC
# MAGIC **O problema.** ROC é a curva que todo mundo mostra e a que menos informa em base desbalanceada: com 2% de eventos, uma AUC alta convive com precisão baixíssima. Cada curva responde a uma pergunta diferente, e mostrar só uma é escolher qual verdade contar.
# MAGIC
# MAGIC **O que este helper faz.** Gera ROC, precisão-recall, lift e KS com o mesmo tema sobre vetores já disponíveis no driver. O parâmetro `n` só altera o N exibido no rodapé; **não subamostra** os dados.
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
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side** |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

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
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC linhas: 8000 | eventos: 148 (1.85%)
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A AUC sai bem acima de 0,5 e a curva parece boa. ROC compara
# MAGIC taxa de verdadeiros positivos com taxa de falsos positivos, e o
# MAGIC denominador da segunda são os **não-eventos** — 98% da base aqui. Errar mil
# MAGIC negativos mal move a curva.
# MAGIC
# MAGIC Por isso, em base desbalanceada, leia ROC junto com PR, lift, prevalência e capacidade operacional; uma AUC alta não garante precisão adequada no recorte acionável.

# COMMAND ----------

plot_pr_curve(y, p, title="Precisão × recall — a mesma base")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Aqui o desbalanceamento fica visível. A precisão parte perto
# MAGIC da prevalência e cai conforme o recall sobe. É a curva que responde à
# MAGIC pergunta operacional: **de cada dez que eu abordar, quantos são evento?**
# MAGIC
# MAGIC A linha de referência da PR não é 0,5 como na ROC — é a prevalência.
# MAGIC Executada no laboratório, esta base sai com **148 eventos em 8.000 linhas,
# MAGIC 1,85%** (a fixture pede 2%; o sorteio entrega 1,85%). Um modelo aleatório
# MAGIC produz aqui uma reta horizontal em **0,0185**, não em 0,02 — e a diferença
# MAGIC importa num notebook cujo assunto é qual número se escolhe contar.

# COMMAND ----------

plot_lift_curve(y, p, title="Lift por decil")

# COMMAND ----------

plot_ks_curve(y, p, title="KS")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Lift responde "quantas vezes melhor que sortear", e é a
# MAGIC curva que conversa com quem decide orçamento. KS resume a maior distância
# MAGIC entre as duas distribuições acumuladas, e é o número que a tradição de
# MAGIC crédito reporta.
# MAGIC
# MAGIC As quatro descrevem o mesmo modelo. Mostrar só a ROC não é erro de
# MAGIC cálculo — é escolha de enquadramento, e vale saber que se está fazendo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Mostrando só a ROC em base desbalanceada.** É a mais bonita e a menos informativa ali.
# MAGIC - **Comparando KS entre populações diferentes.** O índice depende da distribuição, não só da separação.
# MAGIC - **Sobre milhões de linhas esperando que `n` limite o custo.** `n` é somente metadado visual; amostre ou agregue antes de trazer vetores grandes ao driver.
# MAGIC - **Como prova de calibração.** Nenhuma das quatro diz se a probabilidade prevista corresponde à frequência observada.
# MAGIC
# MAGIC ## Dívida registrada: a paleta daqui tem seis cores
# MAGIC
# MAGIC Este módulo **redeclara** `PALETA_CATEGORICA` em vez de importá-la de
# MAGIC `hub_snippets.constants.colors`, e o valor **diverge**:
# MAGIC
# MAGIC | Onde | Cores |
# MAGIC |---|---:|
# MAGIC | `constants.colors` | 10 |
# MAGIC | `ml.curves_plotly` (aqui) | **6** |
# MAGIC | `ml.umap_viz`, `ml.vintage_analysis` | 10, idênticas à original |
# MAGIC
# MAGIC Duas das três cópias são iguais à original, o que torna esta terceira
# MAGIC invisível numa inspeção rápida. Como o `__init__.py` reexporta tudo, há
# MAGIC hoje dois caminhos de import para o mesmo nome com valores diferentes.
# MAGIC
# MAGIC **Na prática:** um gráfico com mais de seis séries feito por este módulo
# MAGIC repete cor a partir da sétima; o mesmo gráfico feito com a paleta de
# MAGIC `constants` não repete. Se você precisa das dez, importe explicitamente
# MAGIC de `constants.colors` e passe em `colorway`.
# MAGIC
# MAGIC A unificação não foi feita aqui de propósito: trocar a redeclaração por
# MAGIC import mudaria a aparência de todos os gráficos existentes, e a conversão
# MAGIC não muda comportamento. É decisão de produto, e precisa de alguém olhando
# MAGIC os gráficos para dizer se seis ou dez é o certo.