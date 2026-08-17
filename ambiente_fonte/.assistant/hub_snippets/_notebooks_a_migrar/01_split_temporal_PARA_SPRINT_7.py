# Databricks notebook source
# MAGIC %md
# MAGIC # RASCUNHO — material de `split_temporal`, para a Sprint 7
# MAGIC
# MAGIC **Não é um notebook do Hub.** É a metade que sobrou quando o notebook de
# MAGIC vazamento temporal foi dividido: a parte de `pit_join` virou
# MAGIC `spark/pit_join/exemplo_pit_join.py`, e esta aqui espera a conversão de
# MAGIC `ml/split_temporal`.
# MAGIC
# MAGIC Ao converter, esta metade precisa recuperar sozinha o contexto que a outra
# MAGIC dava: o que é vazamento temporal, e por que separar treino e teste por
# MAGIC sorteio destrói a ordem do tempo. Hoje o texto começa em "a segunda
# MAGIC armadilha" e se refere a um join que não está mais no arquivo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparação
# MAGIC
# MAGIC A linha abaixo torna a biblioteca importável. `.assistant` é a pasta que
# MAGIC contém `hub_snippets`; adicionamos ela ao caminho de busca do Python.

# COMMAND ----------

import sys

current_user = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{current_user}/.assistant")

from pyspark.sql import functions as F
from hub_snippets.testing import fixtures

print("biblioteca acessível")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. A segunda armadilha: separar treino e teste
# MAGIC
# MAGIC Resolvido o join, falta decidir o que é treino e o que é teste. Aqui o
# MAGIC erro clássico é sortear linhas ao acaso.
# MAGIC
# MAGIC Sortear funciona quando as linhas são independentes. Quando há tempo
# MAGIC envolvido, não são: sortear coloca no treino linhas de **depois** das que
# MAGIC ficaram no teste. O modelo passa a "ver o futuro" de novo, por outro
# MAGIC caminho.
# MAGIC
# MAGIC `temporal_split` separa por **período de calendário**, não por posição de
# MAGIC linha, e aceita um intervalo de segurança (`gap_periods`) entre treino e
# MAGIC teste — útil quando o target leva tempo para se materializar.

# COMMAND ----------

from hub_snippets.ml.split_temporal import temporal_split

painel_spark = fixtures.serie_temporal(n_entidades=30, n_periodos=24, seed=5)
print("PAINEL (uma linha por entidade e mês):")
painel_spark.show(3, truncate=False)

# ATENÇÃO — diferença que confunde na primeira vez: `temporal_split` trabalha
# com pandas, não com Spark. Ele roda no driver, sobre dados já reduzidos.
# Passar um DataFrame Spark aqui produz o erro `Attribute 'copy' is not
# supported`, que não diz nada sobre a causa real.
#
# Isso não é descuido do módulo: definir splits é decisão sobre metadados
# (quais períodos), não processamento de volume. Reduza antes com agregação ou
# amostra, e só então chame — nunca converta uma tabela inteira ao driver.
painel = painel_spark.toPandas()
print(f"\nconvertido para pandas: {len(painel)} linhas (volume controlado)")

treino, validacao, teste = temporal_split(painel, date_col="dt_referencia")

for nome, parte in [("treino", treino), ("validação", validacao), ("teste", teste)]:
    if len(parte):
        print(
            f"{nome:>10}: {len(parte):>5} linhas  |  "
            f"{parte['dt_referencia'].min()} a {parte['dt_referencia'].max()}"
        )
    else:
        print(f"{nome:>10}: vazio")

# COMMAND ----------

# MAGIC %md
# MAGIC Repare que os períodos **não se sobrepõem**: cada faixa de datas pertence
# MAGIC a uma partição só. É exatamente isso que o sorteio aleatório destrói.
# MAGIC
# MAGIC ## Resumo para levar
# MAGIC
# MAGIC | Situação | O que usar | O que acontece sem |
# MAGIC |---|---|---|
# MAGIC | Trazer atributo histórico para uma decisão | `pit_join` | base incha e entra dado do futuro |
# MAGIC | Fonte demora a publicar o dado | `atraso_publicacao_dias` | vazamento sutil, difícil de detectar |
# MAGIC | Separar treino e teste com tempo envolvido | `temporal_split` | teste otimista, produção decepciona |
# MAGIC
# MAGIC Quando precisar de explicação linha a linha do código interno, use a
# MAGIC skill `@hub-ml-tutor-databricks` com o módulo anexado — ela lê a versão
# MAGIC atual do arquivo, então a explicação nunca fica desatualizada.
