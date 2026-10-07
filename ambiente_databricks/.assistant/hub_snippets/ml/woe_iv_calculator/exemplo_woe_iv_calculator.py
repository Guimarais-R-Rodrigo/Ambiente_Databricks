# Databricks notebook source
# MAGIC %md
# MAGIC # `woe_iv_calculator` — e por que IV alto é motivo de desconfiança
# MAGIC
# MAGIC **O problema.** WOE e Information Value vêm da tradição de crédito e são
# MAGIC usados para escolher variáveis: quanto maior o IV, mais a variável separa
# MAGIC bom de mau. A leitura natural — "IV alto, variável ótima" — é a que mais
# MAGIC coloca vazamento dentro de um modelo.
# MAGIC
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC faixa_renda  n_bom  n_mau  n_total     woe   iv_partial
# MAGIC alta          1016    296     1312  -0.1133      0.00580
# MAGIC baixa          446     89      535   0.2618      0.01130
# MAGIC media          919    234     1153   0.0210      0.00017
# MAGIC
# MAGIC IV da faixa de renda    :  0.0173   (Inútil (< 0.02))
# MAGIC IV do status de cobrança: 15.5748   (Elevada — investigar leakage)
# MAGIC ```
# MAGIC
# MAGIC **O que este helper faz.** Calcula WOE por faixa e o IV total, e classifica
# MAGIC a força — inclusive a faixa que deveria acender alerta em vez de comemoração.

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
# MAGIC ## 1. WOE e Information Value
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
# MAGIC Um IV altíssimo merece investigação, não comemoração automática. Ele pode
# MAGIC refletir leakage ou proxy do target, mas também concentração, bins muito
# MAGIC específicos, seleção de amostra ou uma associação realmente forte no recorte.
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
# MAGIC não funcionará — é o mesmo vazamento que `hub_snippets.ml.split_temporal`
# MAGIC trata pelo lado do tempo, chegando aqui por outra porta: não pela ordem
# MAGIC das linhas, mas pelo conteúdo da coluna.
# MAGIC
# MAGIC **A regra prática:** IV muito acima do esperado para o domínio é sinal
# MAGIC para investigar a origem da variável, não para promovê-la. Pergunte
# MAGIC sempre: *esse dado existia, com esse valor, no instante da decisão?*
# MAGIC
# MAGIC ## Resumo para levar
# MAGIC
# MAGIC | Armadilha | Sintoma | Conta certa |
# MAGIC |---|---|---|
# MAGIC | Celebrar IV alto | variável "perfeita", IV muito acima do domínio | verificar se ela existia na hora da decisão |
# MAGIC | Ler faixa de IV como norma | "0,3 é forte" repetido sem fonte | tratar como referência, e calibrar no próprio domínio |
# MAGIC | Aplicar WOE calculado no treino inteiro | otimismo que não reaparece em produção | calcular as faixas só no treino e aplicá-las ao resto |
# MAGIC
# MAGIC As armadilhas de **safra** — somar taxas por vintage, comparar safras pelo
# MAGIC calendário — são de outro helper: `hub_snippets.ml.vintage_analysis`, que
# MAGIC tem notebook próprio.
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
# MAGIC - **Com IV acima de 0,5, sem investigar.** A faixa é uma heurística local,
# MAGIC   não diagnóstico universal. Verifique leakage, origem, concentração, binning e
# MAGIC   estabilidade antes de interpretar o valor como poder preditivo útil.
# MAGIC - **Em variável contínua sem binning declarado.** Este helper não cria bins;
# MAGIC   valores distintos viram grupos. O IV depende da discretização, e comparar
# MAGIC   resultados de regras de binning diferentes exige muito cuidado.
# MAGIC - **Como substituto de validação temporal.** Uma variável com IV alto na
# MAGIC   base inteira pode ter IV zero na safra mais recente.
