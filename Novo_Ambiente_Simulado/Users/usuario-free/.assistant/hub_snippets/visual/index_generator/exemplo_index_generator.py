# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.index_generator` — o índice do notebook, gerado do mesmo mapa
# MAGIC
# MAGIC **O problema.** Índice escrito à mão desatualiza na primeira seção que muda de lugar, e ninguém percebe — porque quem escreveu já sabe onde está tudo.
# MAGIC
# MAGIC **O que este objeto oferece.** Gera o índice das etapas da EDA a partir de `constants.emojis`, em HTML ou Markdown, com filtro das etapas ativas.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | nenhum — este objeto não recebe dados |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.visual.index_generator import gerar_indice_eda

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. O índice completo, e o filtrado

# COMMAND ----------

displayHTML(gerar_indice_eda())

# COMMAND ----------

# A analise real quase nunca usa as nove. Declarar quais estao ativas evita
# prometer secao que nao existe.
print(gerar_indice_eda(etapas_ativas=[1, 3, 4, 8], markdown=True))

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC ## 📋 Índice da EDA
# MAGIC
# MAGIC * 📐 Etapa 1 — Inventário Inicial
# MAGIC   Reconhece estrutura, volume, tipos e perfil geral dos dados.
# MAGIC * ✅ Etapa 3 — Qualidade de Dados
# MAGIC   Diagnostica nulos, duplicatas, outliers e inconsistências.
# MAGIC * 📊 Etapa 4 — Análise Univariada
# MAGIC   Distribuição individual de cada variável numérica, categórica e temporal.
# MAGIC * 📈 Etapa 8 — Relatório Executivo
# MAGIC   Síntese final com achados, impactos e próximos passos.
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Quatro etapas pedidas, quatro listadas — **e a numeração original
# MAGIC preservada**. O índice mostra 1, 3, 4 e 8, não 1, 2, 3 e 4.
# MAGIC
# MAGIC É a decisão de projeto que faz o objeto valer a pena. Renumerar
# MAGIC sequencialmente daria um índice mais bonito e destruiria a informação:
# MAGIC quem conhece o roteiro vê de imediato que a granularidade (2) não foi
# MAGIC analisada, que a bivariada (5) não foi feita e que não há visualizações
# MAGIC (6). **O que falta é tão informativo quanto o que está lá**, e só um
# MAGIC índice que respeita a numeração canônica consegue dizer isso.
# MAGIC
# MAGIC Um índice de 1 a 4 pareceria completo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem filtrar as etapas ativas.** Índice com nove itens num notebook que tem quatro promete o que não entrega.
# MAGIC - **Como âncora clicável.** O que ele gera é lista, não link — o Databricks não expõe âncora estável por célula.
# MAGIC - **Em notebook que não segue o roteiro.** O índice reflete o mapa das nove etapas; outro roteiro pede outro índice.
