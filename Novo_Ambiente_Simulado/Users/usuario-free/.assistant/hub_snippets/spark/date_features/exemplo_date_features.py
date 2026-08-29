# Databricks notebook source
# MAGIC %md
# MAGIC # `date_features` — calendário como feature, sem inventar feriado
# MAGIC
# MAGIC **O problema.** Extrair ano, mês e dia da semana de uma data é trivial, e
# MAGIC por isso cada notebook faz do seu jeito, com nomes diferentes. Quando essas
# MAGIC colunas viram feature de modelo, a divergência de nome vira retrabalho — e
# MAGIC a parte que **não** é trivial, o feriado, costuma sair errada: cada país e
# MAGIC cada segmento têm o seu calendário, e nenhum deles é dedutível da data.
# MAGIC
# MAGIC **O que este helper faz.** Deriva as features de calendário com nomes
# MAGIC padronizados e aceita a lista de feriados **do seu projeto** — sem embutir
# MAGIC uma.

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

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from pyspark.sql import functions as F

from hub_snippets.spark.date_features import (
    FIXED_NATIONAL_HOLIDAYS_BR,
    extrair_features_data,
)
from hub_snippets.testing import fixtures

print(f"feriados nacionais de data fixa: {len(FIXED_NATIONAL_HOLIDAYS_BR)}")
print(FIXED_NATIONAL_HOLIDAYS_BR)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. As features de calendário

# MAGIC ```text
# MAGIC feriados nacionais de data fixa: 9
# MAGIC {'10-12', '05-01', '11-20', '09-07', '01-01', '11-02', '04-21', '12-25', '11-15'}
# MAGIC ```
# MAGIC
# COMMAND ----------

base = fixtures.base_tabular(n=500, seed=42)
com_datas = extrair_features_data(base, "dt_referencia")

novas = [c for c in com_datas.columns if c not in base.columns]
print(f"colunas acrescentadas ({len(novas)}): {novas}")
display(com_datas.select("dt_referencia", *novas).limit(8))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC colunas acrescentadas (9): ['dia_semana_iso', 'is_fim_semana', 'dia_mes', 'semana_ano', 'mes', 'trimestre', 'ano', 'is_feriado_nacional_fixo', 'is_feriado_calendario']
# MAGIC +-------------+--------------+-------------+-------+----------+---+---------+----+------------------------+---------------------+
# MAGIC |dt_referencia|dia_semana_iso|is_fim_semana|dia_mes|semana_ano|mes|trimestre|ano |is_feriado_nacional_fixo|is_feriado_calendario|
# MAGIC +-------------+--------------+-------------+-------+----------+---+---------+----+------------------------+---------------------+
# MAGIC |2026-03-04   |3             |false        |4      |10        |3  |1        |2026|false                   |false                |
# MAGIC |2026-01-23   |5             |false        |23     |4         |1  |1        |2026|false                   |false                |
# MAGIC |2026-02-25   |3             |false        |25     |9         |2  |1        |2026|false                   |false                |
# MAGIC |2026-04-18   |6             |true         |18     |16        |4  |2        |2026|false                   |false                |
# MAGIC |2026-02-10   |2             |false        |10     |7         |2  |1        |2026|false                   |false                |
# MAGIC |2026-01-27   |2             |false        |27     |5         |1  |1        |2026|false                   |false                |
# MAGIC |2026-03-09   |1             |false        |9      |11        |3  |1        |2026|false                   |false                |
# MAGIC |2026-01-21   |3             |false        |21     |4         |1  |1        |2026|false                   |false                |
# MAGIC +-------------+--------------+-------------+-------+----------+---+---------+----+------------------------+---------------------+
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Os nomes são o produto principal aqui. Um modelo treinado com
# MAGIC `mes` e servido com `month` quebra em produção, e o erro aparece longe da
# MAGIC causa. Padronizar o nome é o que o helper resolve, e é mais valioso do que
# MAGIC a aritmética de datas, que qualquer um escreve.
# MAGIC
# MAGIC Use o parâmetro `prefixo` quando houver mais de uma data na mesma tabela —
# MAGIC `dt_contrato` e `dt_evento` produziriam colunas homônimas.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Feriado é decisão do projeto, não do helper

# COMMAND ----------

# A lista embutida cobre apenas feriados nacionais de DATA FIXA. Móveis
# (Carnaval, Páscoa, Corpus Christi) e estaduais precisam ser informados.
com_feriados = extrair_features_data(
    base, "dt_referencia",
    holiday_dates=["2026-02-17", "2026-04-03", "2026-06-04"],  # móveis de 2026
)
coluna_feriado = [c for c in com_feriados.columns if "feriad" in c.lower()][0]

print(f"coluna de feriado: {coluna_feriado}")
display(
    com_feriados.groupBy(coluna_feriado).count().orderBy(coluna_feriado)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC coluna de feriado: is_feriado_nacional_fixo
# MAGIC +------------------------+-----+
# MAGIC |is_feriado_nacional_fixo|count|
# MAGIC +------------------------+-----+
# MAGIC |false                   |493  |
# MAGIC |true                    |7    |
# MAGIC +------------------------+-----+
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A lista embutida tem apenas os feriados **nacionais de data
# MAGIC fixa**. Carnaval, Páscoa e Corpus Christi mudam de data todo ano e não
# MAGIC estão lá; feriado estadual e municipal também não.
# MAGIC
# MAGIC Isso é escolha de projeto, não limitação. Um helper que embutisse "os
# MAGIC feriados do Brasil" estaria errado para metade dos casos — a agência de
# MAGIC Salvador não opera nos mesmos dias que a de Curitiba —, e o erro seria
# MAGIC invisível: as colunas sairiam preenchidas, só que com o calendário errado.
# MAGIC
# MAGIC O erro de interpretação mais provável é supor que a lista está completa.
# MAGIC Ela está **declarada**, que é diferente: você vê o que entrou.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Feature de calendário e vazamento temporal

# COMMAND ----------

# Features de calendário são seguras contra vazamento por natureza: derivam da
# própria data da linha, não de dado que chegou depois. Esta é a exceção
# tranquila num domínio onde quase tudo exige cuidado temporal.
amostra = com_datas.select("dt_referencia", *novas).limit(3).collect()
for linha in amostra:
    print(dict(linha.asDict()))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC {'dt_referencia': datetime.date(2026, 3, 4), 'dia_semana_iso': 3, 'is_fim_semana': False, 'dia_mes': 4, 'semana_ano': 10, 'mes': 3, 'trimestre': 1, 'ano': 2026, 'is_feriado_nacional_fixo': False, 'is_feriado_calendario': False}
# MAGIC {'dt_referencia': datetime.date(2026, 1, 23), 'dia_semana_iso': 5, 'is_fim_semana': False, 'dia_mes': 23, 'semana_ano': 4, 'mes': 1, 'trimestre': 1, 'ano': 2026, 'is_feriado_nacional_fixo': False, 'is_feriado_calendario': False}
# MAGIC {'dt_referencia': datetime.date(2026, 2, 25), 'dia_semana_iso': 3, 'is_fim_semana': False, 'dia_mes': 25, 'semana_ano': 9, 'mes': 2, 'trimestre': 1, 'ano': 2026, 'is_feriado_nacional_fixo': False, 'is_feriado_calendario': False}
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Cada valor sai da própria `dt_referencia` da linha. Não há
# MAGIC agregação, não há join, não há nada que possa trazer informação do futuro.
# MAGIC
# MAGIC A ressalva fica no **feriado**: se a lista que você passar for construída
# MAGIC depois do período analisado — por exemplo, um calendário publicado no fim do
# MAGIC ano —, ela é conhecimento posterior. Na prática raramente importa, porque
# MAGIC feriado é anunciado com antecedência; vale saber que a exceção existe.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Esperando calendário completo.** A lista embutida é só nacional de data
# MAGIC   fixa. Móveis, estaduais e municipais são responsabilidade de quem chama.
# MAGIC - **Com várias datas na tabela, sem `prefixo`.** As colunas colidem.
# MAGIC - **Para dia útil bancário.** Isso depende de calendário de compensação,
# MAGIC   que não é derivável da data nem coberto aqui.
# MAGIC - **Sobre coluna de timestamp, esperando componente de hora.** O helper
# MAGIC   trata data; hora e fuso são outro assunto e outro conjunto de armadilhas.
