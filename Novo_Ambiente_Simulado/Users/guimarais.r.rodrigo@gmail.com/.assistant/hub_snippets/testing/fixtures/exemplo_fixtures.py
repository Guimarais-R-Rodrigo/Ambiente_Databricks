# Databricks notebook source
# MAGIC %md
# MAGIC # `testing.fixtures` — bases sintéticas para exemplo e teste
# MAGIC
# MAGIC **O que resolve.** Todo exemplo desta biblioteca precisa de dados. Se cada
# MAGIC um inventar os seus, três coisas dão errado: os números mudam a cada
# MAGIC execução e ninguém sabe se a diferença é bug ou sorteio; alguém acaba
# MAGIC apontando para uma tabela real "só para testar"; e o exemplo deixa de
# MAGIC reproduzir o problema que ele existe para mostrar.
# MAGIC
# MAGIC Este módulo é a fonte única desses dados. Quatro geradores, todos
# MAGIC determinísticos: mesma `seed`, mesma base, sempre.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime — **não instale nada** |
# MAGIC | Dados | 100% sintéticos, gerados aqui; nenhuma tabela é lida ou escrita |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

# O caminho da biblioteca depende do usuário logado. Estas três linhas abrem
# todos os notebooks do Hub — sem elas, o import abaixo falha.
import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

print(f"biblioteca: /Workspace/Users/{usuario}/.assistant")
print(f"geradores disponíveis: {', '.join(fixtures.__all__)}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. `base_tabular` — o caso geral
# MAGIC
# MAGIC ```text
# MAGIC biblioteca: /Workspace/Users/<username>/.assistant
# MAGIC geradores disponíveis: base_tabular, serie_temporal, fatos_e_features, safras
# MAGIC ```
# MAGIC
# MAGIC **Para que serve.** É a base de partida de qualquer exemplo que precise de
# MAGIC uma tabela de clientes: uma chave, uma categórica, uma numérica com
# MAGIC ausentes e um alvo binário. Os ausentes existem de propósito — helper que
# MAGIC nunca viu nulo quebra na primeira tabela de verdade.

# COMMAND ----------

# `pct_nulos_renda` e `prevalencia_alvo` são declarados, não sorteados: quem lê o
# exemplo precisa saber que 4% de nulos é escolha, não acaso do gerador.
clientes = fixtures.base_tabular(n=500, seed=42, pct_nulos_renda=0.04, prevalencia_alvo=0.25)

display(clientes.limit(5))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC +----------+---+--------+-------------+----+
# MAGIC |id_cliente|uf |renda   |dt_referencia|alvo|
# MAGIC +----------+---+--------+-------------+----+
# MAGIC |cli00000  |MG |1962.7  |2026-03-04   |1   |
# MAGIC |cli00001  |RS |14018.94|2026-01-23   |0   |
# MAGIC |cli00002  |SP |NULL    |2026-02-25   |1   |
# MAGIC |cli00003  |RS |11883.03|2026-04-18   |1   |
# MAGIC |cli00004  |SP |16474.46|2026-02-10   |0   |
# MAGIC +----------+---+--------+-------------+----+
# MAGIC ```
# MAGIC

# COMMAND ----------

from pyspark.sql import functions as F

resumo = clientes.agg(
    F.count("*").alias("linhas"),
    F.countDistinct("id_cliente").alias("clientes_distintos"),
    F.sum(F.col("renda").isNull().cast("int")).alias("renda_nula"),
    F.round(F.avg("alvo"), 3).alias("prevalencia_alvo"),
).collect()[0]

print(f"linhas            : {resumo['linhas']}")
print(f"clientes distintos: {resumo['clientes_distintos']}")
print(f"renda nula        : {resumo['renda_nula']}")
print(f"prevalência alvo  : {resumo['prevalencia_alvo']}")

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC linhas            : 500
# MAGIC clientes distintos: 500
# MAGIC renda nula        : 13
# MAGIC prevalência alvo  : 0.268
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** `clientes distintos` igual a `linhas` significa **chave
# MAGIC única** — é o padrão. Para exercitar diagnóstico de join, passe
# MAGIC `n_entidades` menor que `n` e a chave passa a ter duplicidade proposital.
# MAGIC
# MAGIC A prevalência sai próxima de 0,25, não exata: o gerador sorteia linha a
# MAGIC linha em vez de fixar a contagem. Isso é deliberado — base real também não
# MAGIC tem prevalência redonda, e exemplo que depende de número exato esconde
# MAGIC essa realidade de quem aprende.
# MAGIC
# MAGIC O erro de leitura mais provável aqui: tratar `renda_nula` como defeito da
# MAGIC fixture. Não é. É o material com que se testa o tratamento de ausentes.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. `fatos_e_features` — a fixture que torna vazamento **detectável**
# MAGIC
# MAGIC **Para que serve.** É a única das quatro desenhada para provar que um
# MAGIC helper está certo, e não só para alimentá-lo. Parte das linhas de feature
# MAGIC tem data posterior à decisão: um join point-in-time correto **precisa**
# MAGIC descartá-las. Se sobrarem no resultado, houve vazamento — e o teste vê.

# COMMAND ----------

fatos, features = fixtures.fatos_e_features(n_decisoes=300, seed=42, pct_feature_futura=0.2)

futuras = features.filter("eh_futura").count()
print(f"decisões        : {fatos.count()}")
print(f"linhas de feature: {features.count()}")
print(f"  das quais publicadas DEPOIS da decisão: {futuras}")

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC decisões        : 300
# MAGIC linhas de feature: 656
# MAGIC   das quais publicadas DEPOIS da decisão: 56
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A coluna `eh_futura` não existe em dado real: é gabarito.
# MAGIC Ela existe para que o teste possa afirmar "nenhuma dessas linhas
# MAGIC atravessou o join", que é uma verificação bem mais forte do que conferir a
# MAGIC contagem final.
# MAGIC
# MAGIC Um detalhe do desenho que economiza depuração: **cada decisão recebe um
# MAGIC cliente próprio**. Se a mesma entidade aparecesse em duas decisões, uma
# MAGIC feature "futura" para a decisão de março seria legitimamente passada para a
# MAGIC decisão de junho — e a marca deixaria de valer como critério.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. `serie_temporal` e `safras` — os painéis
# MAGIC
# MAGIC `serie_temporal` é painel entidade × mês, para lags, janelas móveis e
# MAGIC split temporal. `safras` é painel contrato × MOB, com incidência que cresce
# MAGIC ao longo da vida do contrato, imitando maturação.

# COMMAND ----------

painel = fixtures.serie_temporal(n_entidades=20, n_periodos=24, seed=42)
carteira = fixtures.safras(n_contratos=400, seed=42, mob_maximo=12)

print(f"série temporal: {painel.count()} linhas "
      f"({painel.select('id_entidade').distinct().count()} entidades × 24 períodos)")
print(f"safras        : {carteira.count()} linhas "
      f"({carteira.select('id_contrato').distinct().count()} contratos × 12 MOB)")

display(
    carteira.groupBy("mob").agg(F.round(F.avg("inadimplente"), 4).alias("incidencia"))
    .orderBy("mob")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC série temporal: 480 linhas (20 entidades × 24 períodos)
# MAGIC safras        : 4800 linhas (400 contratos × 12 MOB)
# MAGIC +---+----------+
# MAGIC |mob|incidencia|
# MAGIC +---+----------+
# MAGIC |1  |0.005     |
# MAGIC |2  |0.0225    |
# MAGIC |3  |0.065     |
# MAGIC |4  |0.0925    |
# MAGIC |5  |0.1375    |
# MAGIC |6  |0.185     |
# MAGIC |7  |0.24      |
# MAGIC |8  |0.31      |
# MAGIC |9  |0.37      |
# MAGIC |10 |0.4275    |
# MAGIC |11 |0.475     |
# MAGIC |12 |0.5475    |
# MAGIC +---+----------+
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A incidência sobe monotonicamente com o MOB porque contrato
# MAGIC que entrou em inadimplência não volta — é acumulado, não taxa do mês.
# MAGIC Comparar duas safras em MOBs diferentes por causa disso é a armadilha
# MAGIC clássica de análise de safra, e é exatamente o que esta fixture permite
# MAGIC demonstrar.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O mesmo `seed` devolve a mesma base

# COMMAND ----------

a = fixtures.base_tabular(n=100, seed=7).collect()
b = fixtures.base_tabular(n=100, seed=7).collect()
c = fixtures.base_tabular(n=100, seed=8).collect()

print(f"seed 7 == seed 7 : {a == b}")
print(f"seed 7 == seed 8 : {a == c}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC ```text
# MAGIC seed 7 == seed 7 : True
# MAGIC seed 7 == seed 8 : False
# MAGIC ```
# MAGIC
# MAGIC - **Para estimar desempenho ou custo.** São centenas de linhas em memória;
# MAGIC   nada aqui diz como o helper se comporta com milhões.
# MAGIC - **Para validar regra de negócio.** As distribuições são plausíveis, não
# MAGIC   representativas. Nenhuma conclusão sobre a carteira sai daqui.
# MAGIC - **Como base para teste de aceitação de modelo.** Fixture prova que o
# MAGIC   código roda e que o helper faz o que promete — não que o modelo serve.
# MAGIC - **Materializando em tabela.** Nenhum gerador grava, de propósito. Se
# MAGIC   precisar persistir, faça explicitamente e no seu schema de rascunho.
