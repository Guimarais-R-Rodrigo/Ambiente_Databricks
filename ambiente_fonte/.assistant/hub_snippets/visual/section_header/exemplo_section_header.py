# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.section_header` — cabeçalho que carrega a etapa da EDA
# MAGIC
# MAGIC **O problema.** Notebook de EDA longo vira um rolo indistinto: quem abre no meio não sabe se está na qualidade dos dados ou já na modelagem. E a numeração feita à mão sai de ordem na primeira reorganização.
# MAGIC
# MAGIC **O que este objeto oferece.** Um cabeçalho em HTML que puxa emoji, título e descrição do mapa de `constants.emojis` a partir do número da etapa.

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

from hub_snippets.visual.section_header import section_header_html

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Pelo número da etapa, sem digitar título

# COMMAND ----------

displayHTML(
    section_header_html(etapa=3)
    + section_header_html(etapa=5)
)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Passar `etapa=3` bastou: emoji, título e descrição vieram do mapa
# MAGIC de `constants.emojis`, e não foram digitados aqui. É a diferença entre
# MAGIC cabeçalho e cabeçalho **consistente** — dois notebooks que declaram a etapa
# MAGIC 3 exibem exatamente o mesmo texto, sem que ninguém precise combinar.
# MAGIC
# MAGIC O acoplamento é intencional e vale registrar: este módulo **importa** de
# MAGIC `constants.emojis` e de `constants.colors`. Se `SECOES_EDA` mudar, os
# MAGIC cabeçalhos mudam junto — que é exatamente o que `constants.styles` **não**
# MAGIC faz com as cores, conforme registrado no notebook daquele objeto.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Sobrescrevendo, quando a seção não é uma das nove

# COMMAND ----------

displayHTML(section_header_html(
    emoji="🧪",
    titulo="Backtest da política de corte",
    descricao="Fora do roteiro padrão: compara o corte vigente com dois alternativos.",
))

print(section_header_html(etapa=3)[:180], "...")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC <div style="background:#F8F9FA; border-left:4px solid #005CA9; padding:12px 16px;
# MAGIC      margin:8px 0 12px 0; border-radius:4px; font-family:Segoe UI, Roboto, sans-serif;">
# MAGIC   ...
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Quando a seção não é uma das nove, passe `emoji`, `titulo` e
# MAGIC `descricao` à mão. Forçar um número que não corresponde é pior que não
# MAGIC numerar: quem lê procura a etapa 3 no índice e encontra outra coisa.
# MAGIC
# MAGIC A saída é HTML puro, e o estilo vem de `constants.styles`. Trocar a
# MAGIC aparência de todos os cabeçalhos do ecossistema é uma edição num arquivo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Fora do roteiro das nove etapas.** Se a seção não é uma delas, passe `titulo` e `emoji` à mão em vez de forçar um número.
# MAGIC - **Repetido na mesma etapa.** Dois cabeçalhos com o número 3 desfazem a orientação que eles existem para dar.
# MAGIC - **Em notebook curto.** Três células não precisam de navegação.
