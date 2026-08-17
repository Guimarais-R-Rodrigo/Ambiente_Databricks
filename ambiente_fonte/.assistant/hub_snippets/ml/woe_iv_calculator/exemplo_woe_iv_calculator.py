# Databricks notebook source
# MAGIC %md
# MAGIC # `woe_iv_calculator` — e por que IV alto é motivo de desconfiança
# MAGIC
# MAGIC **O problema.** WOE e Information Value vêm da tradição de crédito e são
# MAGIC usados para escolher variáveis: quanto maior o IV, mais a variável separa
# MAGIC bom de mau. A leitura natural — "IV alto, variável ótima" — é a que mais
# MAGIC coloca vazamento dentro de um modelo.
# MAGIC
# MAGIC **O que este helper faz.** Calcula WOE por faixa e o IV total, e classifica
# MAGIC a força — inclusive a faixa que deveria acender alerta em vez de comemoração.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime (Plotly já vem no Databricks) |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

current_user = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{current_user}/.assistant")

from pyspark.sql import functions as F
from hub_snippets.testing import fixtures

print("biblioteca acessível")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 2 — Information Value
# MAGIC
# MAGIC WOE (*weight of evidence*) transforma uma variável em log da razão entre
# MAGIC bons e maus de cada faixa. IV (*information value*) resume, num número, o
# MAGIC quanto a variável separa as duas classes.
# MAGIC
# MAGIC Circula uma régua de bolso: abaixo de 0,02 é inútil, acima de 0,5 é
# MAGIC suspeito. Ela é útil como referência inicial — e vira armadilha quando
# MAGIC tratada como norma.

# COMMAND ----------

from hub_snippets.ml.woe_iv_calculator import calculate_woe_iv, classify_iv

base = fixtures.base_tabular(n=3000, seed=13, prevalencia_alvo=0.2, pct_nulos_renda=0.0)

# Variável com relação real com o alvo.
base = base.withColumn(
    "faixa_renda",
    F.when(F.col("renda") < 5000, "baixa")
     .when(F.col("renda") < 12000, "media")
     .otherwise("alta"),
)

tabela_woe, iv = calculate_woe_iv(base, feature_col="faixa_renda", target_col="alvo")

print(f"IV = {iv:.4f}  ->  {classify_iv(iv)}")
print()
tabela_woe.show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Por que IV muito alto é motivo de desconfiança
# MAGIC
# MAGIC O reflexo natural diante de um IV altíssimo é comemorar. Quase sempre é o
# MAGIC contrário: significa que a variável **quase determina** o alvo, e isso
# MAGIC costuma indicar vazamento.
# MAGIC
# MAGIC Vamos provar criando uma variável construída a partir do próprio alvo —
# MAGIC o vazamento em sua forma mais crua:

# COMMAND ----------

vazada = base.withColumn(
    "status_cobranca",
    F.when(F.col("alvo") == 1, "em_cobranca").otherwise("regular"),
)

_, iv_vazado = calculate_woe_iv(vazada, "status_cobranca", "alvo")

print(f"IV da faixa de renda   : {iv:.4f}   ({classify_iv(iv)})")
print(f"IV do status de cobrança: {iv_vazado:.4f}   ({classify_iv(iv_vazado)})")
print()
print("O segundo parece a melhor variável do modelo. É a pior:")
print("o status de cobrança só existe DEPOIS que o cliente ficou inadimplente.")

# COMMAND ----------

# MAGIC %md
# MAGIC Em produção, no momento de decidir o crédito, `status_cobranca` ainda não
# MAGIC existe. O modelo treinado com ela terá desempenho excelente no teste e
# MAGIC não funcionará — é o mesmo vazamento do notebook 01, chegando por outra
# MAGIC porta.
# MAGIC
# MAGIC **A regra prática:** IV muito acima do esperado para o domínio é sinal
# MAGIC para investigar a origem da variável, não para promovê-la. Pergunte
# MAGIC sempre: *esse dado existia, com esse valor, no instante da decisão?*
# MAGIC
# MAGIC ## Resumo para levar
# MAGIC
# MAGIC | Armadilha | Sintoma | Conta certa |
# MAGIC |---|---|---|
# MAGIC | Somar taxas por safra | acumulado exagerado, às vezes acima de 100% | contar contratos distintos afetados |
# MAGIC | Comparar safras pelo calendário | safra antiga sempre parece pior | comparar em MOB equivalente |
# MAGIC | Celebrar IV alto | variável "perfeita" | verificar se ela existia na hora da decisão |
# MAGIC
# MAGIC As faixas de IV e os limites de PSI têm a mesma natureza: referências
# MAGIC úteis, não normas. Nenhuma delas vem de regulação — e apresentá-las como
# MAGIC exigência regulatória sem citar a fonte é algo que as instruções deste
# MAGIC ecossistema proíbem explicitamente.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como seletor automático de variável.** IV mede separação na base que
# MAGIC   você tem; não sabe se a variável existirá na hora da decisão.
# MAGIC - **Com IV acima de 0,5, sem investigar.** Nessa faixa a hipótese mais
# MAGIC   provável não é "variável excelente": é vazamento, ou variável derivada do
# MAGIC   próprio alvo.
# MAGIC - **Em variável contínua sem binning declarado.** O IV muda com o número de
# MAGIC   faixas, e comparar IVs calculados com binnings diferentes não significa
# MAGIC   nada.
# MAGIC - **Como substituto de validação temporal.** Uma variável com IV alto na
# MAGIC   base inteira pode ter IV zero na safra mais recente.
