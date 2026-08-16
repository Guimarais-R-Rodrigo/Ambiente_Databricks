# Databricks notebook source
# MAGIC %md
# MAGIC # Vazamento temporal: por que `pit_join` e `temporal_split` existem
# MAGIC
# MAGIC > **Material didático do Hub — não é auto-descoberto pelo Genie Code.**
# MAGIC > Abra, execute célula a célula e leia os comentários. Nenhum dado real é
# MAGIC > usado: tudo vem das fixtures sintéticas da própria biblioteca.
# MAGIC
# MAGIC ## O que você vai entender aqui
# MAGIC
# MAGIC Vazamento (*leakage*) é quando o modelo aprende com informação que **não
# MAGIC existia** no momento em que a decisão precisava ser tomada. O resultado é
# MAGIC cruel: o modelo fica excelente no teste e fracassa em produção — e a
# MAGIC diferença só aparece meses depois, quando o prejuízo já ocorreu.
# MAGIC
# MAGIC Este notebook mostra o problema acontecendo, e depois mostra os dois
# MAGIC helpers que o evitam. Você não precisa entender o código por dentro: o
# MAGIC objetivo é entender **o que dá errado sem eles**.

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
# MAGIC ## 1. O cenário
# MAGIC
# MAGIC Imagine que você decide conceder crédito a um cliente **hoje**. Para
# MAGIC decidir, usa o score de bureau daquele cliente. A pergunta que define
# MAGIC tudo é: **qual versão do score você tinha em mãos naquele momento?**
# MAGIC
# MAGIC A fixture abaixo cria essa situação de propósito. Ela devolve duas
# MAGIC tabelas e marca, na coluna `eh_futura`, as linhas de score que só
# MAGIC passaram a existir **depois** da decisão — as que jamais poderiam ter
# MAGIC sido usadas.

# COMMAND ----------

fatos, features = fixtures.fatos_e_features(n_decisoes=200, seed=11, atraso_real_dias=3)

print("DECISÕES (uma linha por decisão de crédito):")
fatos.show(3, truncate=False)

print("HISTÓRICO DE SCORE (várias versões por cliente):")
features.orderBy("id_cliente", "dt_referencia").show(6, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC Repare na terceira coluna do histórico: para o mesmo cliente existem
# MAGIC várias versões do score, cada uma com sua data de referência. E algumas
# MAGIC têm `eh_futura = true`.
# MAGIC
# MAGIC ## 2. O jeito errado, e por que ele engana
# MAGIC
# MAGIC O caminho intuitivo é juntar as duas tabelas pelo cliente. É o que
# MAGIC quase todo mundo escreve na primeira vez:

# COMMAND ----------

# ATENÇÃO: este é o exemplo do que NÃO fazer.
juncao_ingenua = fatos.join(features, "id_cliente", "left")

total_linhas = juncao_ingenua.count()
linhas_vazadas = juncao_ingenua.filter(F.col("eh_futura") == True).count()  # noqa: E712

print(f"decisões originais      : {fatos.count()}")
print(f"linhas após o join      : {total_linhas}")
print(f"linhas com score futuro : {linhas_vazadas}")

# COMMAND ----------

# MAGIC %md
# MAGIC Dois estragos aconteceram de uma vez, e nenhum deles emitiu erro:
# MAGIC
# MAGIC **A base inchou.** Cada decisão virou várias linhas, uma por versão do
# MAGIC score. Se você treinar assim, os clientes com mais versões de score pesam
# MAGIC mais no modelo — sem que ninguém tenha decidido isso.
# MAGIC
# MAGIC **Entrou informação do futuro.** As linhas com `eh_futura = true` são
# MAGIC scores que só existiram depois da decisão. O modelo vai aprender com
# MAGIC elas, ficar ótimo no teste, e não ter esse dado disponível quando for
# MAGIC usado de verdade.
# MAGIC
# MAGIC É por isso que a skill de feature engineering exige, textualmente,
# MAGIC *"feature_timestamp ≤ prediction_timestamp respeitando atraso de
# MAGIC publicação"*.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. O jeito certo: `pit_join`
# MAGIC
# MAGIC *Point-in-time* (ou *as-of*) significa: para cada decisão, traga **a
# MAGIC última versão do score que já estava disponível naquele instante**.
# MAGIC
# MAGIC O parâmetro `atraso_publicacao_dias` merece atenção. Um score com data de
# MAGIC referência 10/01 raramente está disponível no dia 10 — o bureau leva
# MAGIC alguns dias para publicar. Se o atraso real é de 3 dias, esse score só
# MAGIC pode entrar em decisões a partir de 13/01. **Ignorar o atraso cria
# MAGIC vazamento mesmo usando data de referência no passado** — é o erro mais
# MAGIC sutil dos três.

# COMMAND ----------

from hub_snippets.spark.pit_join import pit_join

resultado, diagnostico = pit_join(
    fatos,
    features,
    chave="id_cliente",
    ts_decisao="dt_decisao",
    ts_feature="dt_referencia",
    atraso_publicacao_dias=3,          # o bureau leva 3 dias para publicar
    colunas_feature=["score_bureau", "eh_futura"],
)

print("DIAGNÓSTICO:")
for chave, valor in diagnostico.items():
    print(f"  {chave}: {valor}")

# COMMAND ----------

# MAGIC %md
# MAGIC Compare com o join ingênuo: o número de linhas continua igual ao número
# MAGIC de decisões, e a cobertura diz quantas decisões conseguiram um score
# MAGIC elegível.
# MAGIC
# MAGIC A prova de que o vazamento foi eliminado:

# COMMAND ----------

vazadas = resultado.filter(F.col("eh_futura") == True).count()  # noqa: E712

print(f"linhas no resultado         : {resultado.count()}")
print(f"decisões originais          : {fatos.count()}")
print(f"scores do futuro que entraram: {vazadas}   <- tem de ser zero")

resultado.show(5, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. O atraso de publicação, na prática
# MAGIC
# MAGIC Para ver que o parâmetro faz diferença real, rode o mesmo join com
# MAGIC atrasos diferentes. Quanto maior o atraso declarado, menos scores são
# MAGIC elegíveis — porque menos deles já estavam publicados na data da decisão.

# COMMAND ----------

for atraso in [0, 3, 30, 60]:
    _, diag = pit_join(
        fatos, features, "id_cliente", "dt_decisao", "dt_referencia",
        atraso_publicacao_dias=atraso, colunas_feature=["score_bureau"],
    )
    print(f"atraso {atraso:>3} dias -> cobertura {diag['cobertura_pct']:>6}%")

# COMMAND ----------

# MAGIC %md
# MAGIC **A lição:** o atraso não é um detalhe de configuração, é uma
# MAGIC característica da fonte de dados. Descubra o valor real com quem opera a
# MAGIC fonte. Declarar zero por omissão é assumir publicação instantânea, o que
# MAGIC quase nunca é verdade.

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
# MAGIC skill `@rodrigo-tutor-databricks` com o módulo anexado — ela lê a versão
# MAGIC atual do arquivo, então a explicação nunca fica desatualizada.
