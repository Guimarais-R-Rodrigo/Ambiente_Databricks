# Databricks notebook source
# MAGIC %md
# MAGIC # `rfv_calculator` — RFV que não olha para o futuro
# MAGIC
# MAGIC **O problema.** Recência, frequência e valor são as features mais comuns de
# MAGIC CRM, e a forma natural de calculá-las é agregar a base inteira por cliente.
# MAGIC Quando essas features alimentam um modelo que prevê algo a partir de uma
# MAGIC data de decisão, a agregação inteira inclui transações **posteriores** a
# MAGIC essa data. O modelo aprende com informação que não existiria na hora de
# MAGIC decidir, acerta no teste e fracassa em produção.
# MAGIC
# MAGIC **O que este script faz.** Calcula RFV com corte na data de referência,
# MAGIC inclusive, e não inventa score nenhum a partir disso.

# MAGIC
# MAGIC **Guia local completo:** [README deste script](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | sessão Spark/PySpark com operações de datas, agregações e joins |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | uma view temporária de sessão |
# MAGIC | Diferença Free × trabalho | valide tipos, ANSI, datas e chave não nula no ambiente alvo |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_scripts.rfv_calculator import rfv_calculator
from hub_snippets.testing import fixtures

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparo — um painel de transações por cliente

# COMMAND ----------

from pyspark.sql import functions as F

# O painel da fixture é entidade × mês, **balanceado**: toda entidade tem uma
# linha em todo mês. Isso é errado para RFV — com histórico idêntico, recência e
# frequência saem constantes e o exemplo não exercita nem o R nem o F.
#
# A amostragem quebra o balanceamento: cada cliente passa a ter o próprio
# histórico, que é como transação real se comporta.
painel = (
    fixtures.serie_temporal(n_entidades=40, n_periodos=24, seed=42)
    .withColumnRenamed("id_entidade", "id_cliente")
    .withColumnRenamed("dt_referencia", "dt_transacao")
    .sample(withReplacement=False, fraction=0.55, seed=7)
)
painel.createOrReplaceTempView("vw_exemplo_rfv")

print(f"linhas   : {painel.count()}")
print(f"clientes : {painel.select('id_cliente').distinct().count()}")
periodo = painel.agg(F.min("dt_transacao"), F.max("dt_transacao")).first()
print(f"período  : {periodo[0]} a {periodo[1]}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. RFV com corte na data de decisão

# MAGIC ```text
# MAGIC linhas   : 568
# MAGIC clientes : 40
# MAGIC período  : 2025-01-01 a 2026-12-01
# MAGIC ```
# MAGIC
# COMMAND ----------

# A data de referência é o instante da decisão: nada posterior a ela pode entrar.
DATA_DECISAO = "2026-06-01"

rfv = rfv_calculator(
    "vw_exemplo_rfv",
    col_cliente="id_cliente",
    col_data="dt_transacao",
    col_valor="valor",
    dt_referencia=DATA_DECISAO,
)
display(rfv.orderBy("id_cliente").limit(8))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC +----------+-----------+------------------+----------------+--------+--------------+---------+--------------+------------------+--------------+------------------+
# MAGIC |id_cliente|ultima_data|valor_total       |frequencia_total|recencia|frequencia_30d|valor_30d|frequencia_60d|valor_60d         |frequencia_90d|valor_90d         |
# MAGIC +----------+-----------+------------------+----------------+--------+--------------+---------+--------------+------------------+--------------+------------------+
# MAGIC |ent000    |2026-03-01 |1069.24           |9               |92      |0             |0.0      |0             |0.0               |0             |0.0               |
# MAGIC |ent001    |2026-06-01 |972.72            |11              |0       |1             |96.25    |2             |188.48000000000002|3             |278.17            |
# MAGIC |ent002    |2026-06-01 |906.5500000000001 |10              |0       |1             |96.39    |1             |96.39             |2             |187.35            |
# MAGIC |ent003    |2026-06-01 |1033.08           |11              |0       |1             |93.01    |2             |191.94            |3             |293.47            |
# MAGIC |ent004    |2026-06-01 |603.0799999999999 |11              |0       |1             |54.4     |1             |54.4              |2             |109.99000000000001|
# MAGIC |ent005    |2026-04-01 |969.58            |11              |61      |0             |0.0      |0             |0.0               |1             |90.89             |
# MAGIC |ent006    |2026-05-01 |1995.9299999999998|13              |31      |0             |0.0      |1             |155.82            |2             |314.41999999999996|
# MAGIC |ent007    |2026-05-01 |741.8             |10              |31      |0             |0.0      |1             |77.05             |2             |155.5             |
# MAGIC +----------+-----------+------------------+----------------+--------+--------------+---------+--------------+------------------+--------------+------------------+
# MAGIC ```
# MAGIC

# COMMAND ----------

# A tabela acima só ensina se as três dimensões variarem entre clientes. Este
# resumo prova que variam — e serviria de alarme se a fixture voltasse a ser
# balanceada, caso em que R e F sairiam constantes sem nada acusar.
colunas_rfv = [c for c in rfv.columns if c != "id_cliente"]
display(
    rfv.select([F.countDistinct(c).alias(f"valores_distintos_{c}") for c in colunas_rfv])
)

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC +-----------------------------+-----------------------------+----------------------------------+--------------------------+--------------------------------+---------------------------+--------------------------------+---------------------------+--------------------------------+---------------------------+
# MAGIC |valores_distintos_ultima_data|valores_distintos_valor_total|valores_distintos_frequencia_total|valores_distintos_recencia|valores_distintos_frequencia_30d|valores_distintos_valor_30d|valores_distintos_frequencia_60d|valores_distintos_valor_60d|valores_distintos_frequencia_90d|valores_distintos_valor_90d|
# MAGIC +-----------------------------+-----------------------------+----------------------------------+--------------------------+--------------------------------+---------------------------+--------------------------------+---------------------------+--------------------------------+---------------------------+
# MAGIC |5                            |40                           |9                                 |5                         |2                               |22                         |3                               |33                         |4                               |38                         |
# MAGIC +-----------------------------+-----------------------------+----------------------------------+--------------------------+--------------------------------+---------------------------+--------------------------------+---------------------------+--------------------------------+---------------------------+
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Executado no laboratório, a recência assume 5 valores
# MAGIC distintos entre os 40 clientes (de 0 a 151 dias) e o output acima registra
# MAGIC 9 valores distintos para a frequência total. Leia a tabela como evidência desta execução. Se qualquer uma dessas contagens vier **1**, a base
# MAGIC de exemplo está balanceada e o notebook deixou de exercitar aquela dimensão
# MAGIC — que é exatamente o defeito que a amostragem na célula de preparo corrige.
# MAGIC
# MAGIC Vale o hábito: sempre que um exemplo de feature devolver uma tabela,
# MAGIC conferir que as colunas variam. Tabela degenerada tem a mesma aparência de
# MAGIC tabela correta.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A prova de que o corte funciona

# COMMAND ----------

# Se o corte estiver certo, a frequência calculada tem de bater exatamente com a
# contagem de transações ATÉ a data de decisão — nem uma a mais.
esperado = (
    painel.filter(F.col("dt_transacao") <= F.lit(DATA_DECISAO))
    .groupBy("id_cliente").agg(F.count("*").alias("freq_esperada"))
)
conferencia = rfv.join(esperado, "id_cliente", "inner")
coluna_freq = [c for c in rfv.columns if "freq" in c.lower()][0]

divergentes = conferencia.filter(F.col(coluna_freq) != F.col("freq_esperada")).count()
depois_do_corte = painel.filter(F.col("dt_transacao") > F.lit(DATA_DECISAO)).count()

print(f"coluna de frequência          : {coluna_freq}")
print(f"clientes com divergência      : {divergentes}")
print(f"transações após a data de corte: {depois_do_corte} (todas descartadas)")

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC coluna de frequência          : frequencia_total
# MAGIC clientes com divergência      : 0
# MAGIC transações após a data de corte: 145 (todas descartadas)
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Zero divergências significa que nenhuma das transações
# MAGIC posteriores entrou no cálculo — e havia muitas, já que o painel vai até
# MAGIC bem depois de junho.
# MAGIC
# MAGIC Esta é a verificação que vale a pena repetir sempre que uma feature
# MAGIC temporal for construída: comparar o resultado do helper com uma contagem
# MAGIC filtrada à mão. É barata e pega a classe de erro mais cara da área.
# MAGIC
# MAGIC O erro de interpretação mais provável aqui é achar que o corte na data
# MAGIC basta. **Não basta**: se um dado só ficou disponível dias depois da data a
# MAGIC que se refere, usá-lo na decisão daquele dia continua sendo vazamento. Esse
# MAGIC caso é o do atraso de publicação, e quem trata dele é
# MAGIC `hub_snippets.spark.pit_join`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. O que ele deliberadamente **não** faz

# COMMAND ----------

print("colunas devolvidas:", rfv.columns)

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC colunas devolvidas: ['id_cliente', 'ultima_data', 'valor_total', 'frequencia_total', 'recencia', 'frequencia_30d', 'valor_30d', 'frequencia_60d', 'valor_60d', 'frequencia_90d', 'valor_90d']
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Não há coluna de "score RFV" nem de "segmento". As duas
# MAGIC convenções clássicas embutem uma escolha de negócio que o helper não tem como
# MAGIC fazer:
# MAGIC
# MAGIC - **Somar os quintis** (um número de 3 a 15) pressupõe que as três dimensões
# MAGIC   pesam igual — raramente verdade.
# MAGIC - **Concatenar os quintis** ("545") faz o oposto: impõe prioridade
# MAGIC   lexicográfica, com R dominando F e V.
# MAGIC
# MAGIC Nenhuma das duas é neutra, e o número resultante não é comparável entre
# MAGIC bases com quintis diferentes.
# MAGIC
# MAGIC O script devolve as três medidas cruas e devolve a decisão de combinar a
# MAGIC quem conhece o negócio.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este script
# MAGIC
# MAGIC - **Quando o dado tem atraso de publicação.** Corte por data de referência
# MAGIC   não é o mesmo que corte por disponibilidade. Use `pit_join`.
# MAGIC - **Para gerar segmento pronto.** Ele não pontua nem agrupa, de propósito.
# MAGIC - **Com uma única data de referência para toda a base**, se as decisões
# MAGIC   aconteceram em momentos diferentes: cada linha precisa do seu próprio
# MAGIC   instante, ou o corte fica frouxo para uns e apertado para outros.
# MAGIC - **Sem conferir o grão da tabela de origem.** Se a mesma transação aparece
# MAGIC   duas vezes, a frequência dobra e nada acusa.
