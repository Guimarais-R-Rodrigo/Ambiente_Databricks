# Databricks notebook source
# MAGIC %md
# MAGIC # Crédito: duas contas que quase todo mundo erra
# MAGIC
# MAGIC > **Material didático (`x_docs`) — não é auto-descoberto pela Genie Code.**
# MAGIC > Dados sintéticos apenas. Inventário completo da biblioteca no
# MAGIC > [catálogo de helpers](../catalogo_helpers.md).
# MAGIC
# MAGIC Duas operações do vocabulário de crédito produzem resultado **plausível e
# MAGIC errado** quando feitas do jeito intuitivo. Plausível é a parte perigosa:
# MAGIC o número entra no relatório, ninguém questiona, e a decisão sai enviesada.
# MAGIC
# MAGIC 1. somar taxas de inadimplência por safra
# MAGIC 2. interpretar Information Value como se fosse régua universal

# COMMAND ----------

import sys

current_user = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{current_user}/.assistant")

from pyspark.sql import functions as F
from x_snippets.testing import fixtures

print("biblioteca acessível")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 1 — safras e MOB
# MAGIC
# MAGIC Uma **safra** é o conjunto de contratos originados no mesmo período. O
# MAGIC **MOB** (*months on book*) é quantos meses se passaram desde a
# MAGIC originação.
# MAGIC
# MAGIC A razão de existir dos dois conceitos é uma só: **safras diferentes
# MAGIC estão em momentos de vida diferentes**. Comparar a safra de janeiro com a
# MAGIC de maio pelo calendário compara um contrato de 8 meses com um de 4 — e o
# MAGIC mais velho parece pior simplesmente porque teve mais tempo para dar
# MAGIC problema. Comparar em MOB equivalente corrige isso.

# COMMAND ----------

painel = fixtures.safras(n_contratos=600, seed=7)
print("PAINEL (uma linha por contrato e MOB):")
painel.show(6, truncate=False)

print("\nA incidência cresce com o tempo de vida do contrato:")
(painel.groupBy("mob")
       .agg(F.avg("inadimplente").alias("incidencia"))
       .orderBy("mob")
       .show(12, truncate=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ### O erro: somar as taxas
# MAGIC
# MAGIC A conta intuitiva para "inadimplência acumulada até o MOB 12" é somar as
# MAGIC taxas de cada MOB. Vamos fazer e comparar com o valor correto.

# COMMAND ----------

por_mob = (painel.groupBy("mob")
                 .agg(F.avg("inadimplente").alias("taxa"))
                 .orderBy("mob")
                 .collect())

soma_das_taxas = sum(linha["taxa"] for linha in por_mob)

# O correto: fração de CONTRATOS que ficaram inadimplentes em algum momento
# até o MOB 12. Conta contratos distintos, não soma percentuais.
contratos_totais = painel.select("id_contrato").distinct().count()
contratos_ruins = (painel.filter(F.col("inadimplente") == 1)
                         .select("id_contrato").distinct().count())
incidencia_correta = contratos_ruins / contratos_totais

print(f"somando as taxas por MOB  : {soma_das_taxas:.1%}   <- errado")
print(f"contratos afetados        : {incidencia_correta:.1%}   <- correto")
print()
print(f"a soma exagera em {soma_das_taxas / incidencia_correta:.1f}x")

# COMMAND ----------

# MAGIC %md
# MAGIC A soma pode até passar de 100%, o que denuncia o erro. Mas quando fica
# MAGIC abaixo disso — e frequentemente fica — o número parece razoável e vira
# MAGIC decisão.
# MAGIC
# MAGIC **Por que a soma está errada:** um contrato que ficou inadimplente no MOB
# MAGIC 3 continua inadimplente no 4, no 5, no 6. Somar as taxas conta o mesmo
# MAGIC contrato várias vezes. A pergunta certa é *"que fração dos contratos foi
# MAGIC afetada?"*, e ela se responde contando contratos distintos.
# MAGIC
# MAGIC É exatamente isso que `build_vintage_table` faz — no nível contrato × MOB:

# COMMAND ----------

from x_snippets.ml.vintage_analysis import build_vintage_table

# O módulo trabalha em pandas: análise de safra opera sobre dados já agregados,
# não sobre volume bruto.
painel_pd = painel.toPandas()
print(f"convertido: {len(painel_pd)} linhas (volume controlado)")

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

from x_snippets.ml.woe_iv_calculator import calculate_woe_iv, classify_iv

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
