# Databricks notebook source
# MAGIC %md
# MAGIC # `vintage_analysis` — comparar safras sem comparar o incomparável
# MAGIC
# MAGIC **O problema.** Duas safras de crédito originadas em meses diferentes têm
# MAGIC idades diferentes hoje. Comparar a inadimplência delas no calendário é
# MAGIC comparar um contrato de três meses com um de doze — e o mais novo sempre
# MAGIC parece melhor, porque ainda não teve tempo de estragar.
# MAGIC
# MAGIC **O que este helper faz.** Organiza a carteira por **MOB** (meses desde a
# MAGIC originação), que é o eixo em que safras se tornam comparáveis.

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

from hub_snippets.ml.vintage_analysis import build_vintage_table

# O módulo trabalha em pandas: análise de safra opera sobre dados já agregados,
# não sobre volume bruto.
painel_pd = painel.toPandas()
print(f"convertido: {len(painel_pd)} linhas (volume controlado)")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Comparando safras no eixo do calendário.** É o erro que o helper
# MAGIC   existe para evitar; o MOB é o eixo, não o mês.
# MAGIC - **Somando ou promediando taxas de safras em MOBs diferentes.** O número
# MAGIC   resultante não corresponde a carteira nenhuma.
# MAGIC - **Com safra recente, para projetar o patamar final.** A curva ainda está
# MAGIC   subindo; extrapolar dela subestima sistematicamente.
# MAGIC - **Sem conferir o tamanho de cada safra.** Uma safra pequena produz curva
# MAGIC   errática que parece tendência.
# MAGIC
# MAGIC ### Nota de duplicação
# MAGIC
# MAGIC Este módulo **redeclara** `PALETA_CATEGORICA`, `AZUL_CAIXA`,
# MAGIC `PALETA_SEQUENCIAL` e `TEMA_BASE` em vez de importar de
# MAGIC `hub_snippets.constants.colors`. Os valores aqui são **idênticos** aos de
# MAGIC lá, mas são cópias: mudar a paleta exige editar os dois. A unificação é
# MAGIC mudança de comportamento e está registrada como trabalho futuro.
