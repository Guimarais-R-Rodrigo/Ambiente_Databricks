# Databricks notebook source
# MAGIC %md
# MAGIC # Drift: o que o PSI mede, e o que ele **não** mede
# MAGIC
# MAGIC > **Material didático do Hub — não é auto-descoberto pelo Genie Code.**
# MAGIC > Dados sintéticos apenas.
# MAGIC
# MAGIC ## Por que este notebook existe
# MAGIC
# MAGIC O ambiente anterior a este continha um cálculo de PSI **incorreto**:
# MAGIC comparava média e desvio padrão entre dois períodos. Parecia razoável,
# MAGIC produzia um número, e esse número não era PSI.
# MAGIC
# MAGIC O erro é fácil de cometer e difícil de perceber, porque o resultado
# MAGIC errado também "funciona": sobe quando a média muda, desce quando não
# MAGIC muda. Só que ele é cego para o tipo de mudança que mais importa.

# COMMAND ----------

import sys

current_user = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{current_user}/.assistant")

from pyspark.sql import functions as F
from hub_snippets.testing import fixtures

print("biblioteca acessível")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. O que o PSI realmente faz
# MAGIC
# MAGIC PSI (*Population Stability Index*) compara **a forma de duas
# MAGIC distribuições**, não seus resumos. O procedimento é:
# MAGIC
# MAGIC 1. dividir a variável em faixas, usando **apenas o período de
# MAGIC    referência** para definir os cortes;
# MAGIC 2. medir que proporção da população cai em cada faixa, nos dois períodos;
# MAGIC 3. somar o quanto essas proporções divergem.
# MAGIC
# MAGIC O passo 1 é o que mais se erra: se os cortes forem recalculados no
# MAGIC período novo, você compara cada distribuição consigo mesma e o índice
# MAGIC tende a zero mesmo havendo mudança real.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Onde o atalho falha
# MAGIC
# MAGIC Vamos construir duas populações com **exatamente a mesma média** e
# MAGIC formas completamente diferentes. Um comparador de média não vê nada.

# COMMAND ----------

base = fixtures.base_tabular(n=4000, seed=1, pct_nulos_renda=0.0)

# Período de referência: renda concentrada no meio da faixa.
referencia = base.withColumn("renda", F.lit(10000.0) + F.randn(seed=7) * 800)

# Período atual: mesma média, mas a população se dividiu em dois grupos —
# metade empobreceu, metade enriqueceu.
atual = base.withColumn(
    "renda",
    F.when(F.rand(seed=9) < 0.5, F.lit(4000.0) + F.randn(seed=11) * 500)
     .otherwise(F.lit(16000.0) + F.randn(seed=13) * 500),
)

resumo_ref = referencia.agg(F.avg("renda").alias("media"), F.stddev("renda").alias("desvio")).first()
resumo_atu = atual.agg(F.avg("renda").alias("media"), F.stddev("renda").alias("desvio")).first()

print(f"referência: média {resumo_ref['media']:>9.2f}   desvio {resumo_ref['desvio']:>8.2f}")
print(f"atual     : média {resumo_atu['media']:>9.2f}   desvio {resumo_atu['desvio']:>8.2f}")
print()
print("Se você comparasse apenas a média, concluiria que nada mudou.")

# COMMAND ----------

# MAGIC %md
# MAGIC A média praticamente não se moveu. Mas a população se partiu ao meio:
# MAGIC ninguém mais ganha o valor médio. Para um modelo de crédito, isso é uma
# MAGIC mudança enorme — e o comparador de média não vê.
# MAGIC
# MAGIC Agora o PSI de verdade:

# COMMAND ----------

from hub_snippets.spark.psi_calculator import calcular_csi, calcular_psi, interpretar_psi

psi = calcular_psi(referencia, atual, col="renda", n_bins=10)

print(f"PSI = {psi:.4f}")
print(interpretar_psi(psi))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Por que a interpretação não vem pronta
# MAGIC
# MAGIC Repare que `interpretar_psi` devolveu o valor e mandou compará-lo com a
# MAGIC política calibrada — não disse "crítico" nem "aceitável".
# MAGIC
# MAGIC Isso é deliberado. Circula pela indústria uma régua de bolso — 0,1 e 0,25
# MAGIC — que **não é norma de lugar nenhum**. O limite adequado depende do
# MAGIC modelo, da variável, do tamanho da amostra e do risco do negócio. Uma
# MAGIC variável ruidosa pode passar de 0,1 todo mês sem significar nada; uma
# MAGIC variável estável cruzar 0,05 pode ser sinal sério.
# MAGIC
# MAGIC Por isso o helper só classifica quando **você** informa os limites:

# COMMAND ----------

print("Sem política definida:")
print("  ", interpretar_psi(psi))
print()
print("Com limites calibrados para esta feature:")
print("  ", interpretar_psi(psi, warning_threshold=0.10, critical_threshold=0.25))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Drift de dados não é queda de performance
# MAGIC
# MAGIC Esta é a confusão mais cara da área, e vale fixar:
# MAGIC
# MAGIC | Pergunta | O que responde |
# MAGIC |---|---|
# MAGIC | A população mudou? | PSI / CSI — **não precisa de label** |
# MAGIC | O modelo piorou? | AUC, KS, calibração — **precisa de label** |
# MAGIC
# MAGIC A população pode mudar sem o modelo piorar, e o modelo pode piorar sem a
# MAGIC população mudar. PSI alto é sinal para **investigar**, nunca autorização
# MAGIC para retreinar. É por isso que o `PerformanceMonitor` da biblioteca
# MAGIC sinaliza degradação e jamais decide o retreino: essa decisão exige
# MAGIC investigação, comparação campeão-desafiante e aprovação humana.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Varrer várias features de uma vez
# MAGIC
# MAGIC Em produção você não olha uma variável: olha o conjunto. `calcular_csi`
# MAGIC faz a mesma conta para uma lista de colunas.

# COMMAND ----------

csi = calcular_csi(referencia, atual, feature_cols=["renda"], n_bins=10)

for coluna, valor in csi.items():
    print(f"{coluna:>10}: {valor:.4f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo para levar
# MAGIC
# MAGIC - PSI compara **formas de distribuição**, não médias. Comparar média e
# MAGIC   desvio não é PSI, ainda que produza um número plausível.
# MAGIC - Os cortes das faixas saem **só da referência**. Recalcular no período
# MAGIC   novo esconde a mudança que se quer medir.
# MAGIC - Não existe limite universal. Faixa sem calibração é chute com aparência
# MAGIC   de norma.
# MAGIC - Drift responde "a população mudou?". Performance responde "o modelo
# MAGIC   piorou?". São perguntas diferentes e exigem dados diferentes.
# MAGIC
# MAGIC Para o caso de comparar duas coortes de uma mesma tabela — a rotina mensal
# MAGIC típica —, o atalho é `hub_scripts.drift_detector`, que aplica esta mesma
# MAGIC lógica recebendo o nome da tabela e as duas datas.
