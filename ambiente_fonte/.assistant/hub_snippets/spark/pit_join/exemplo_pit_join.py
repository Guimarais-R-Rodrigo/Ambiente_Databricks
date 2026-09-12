# Databricks notebook source
# MAGIC %md
# MAGIC # `pit_join` — trazer histórico sem trazer o futuro junto
# MAGIC
# MAGIC **O problema.** Para treinar um modelo, precisamos reconstruir a informação
# MAGIC disponível no instante de cada decisão. Trazer a versão mais recente sem
# MAGIC considerar esse instante pode introduzir informação futura e tornar a
# MAGIC avaliação incompatível com o uso real. Isso não determina automaticamente
# MAGIC qual será a métrica; compromete o desenho da análise.
# MAGIC
# MAGIC **O que este helper faz.** Junta cada decisão à última versão da feature
# MAGIC que **já estava disponível** naquele momento — considerando também o atraso
# MAGIC de publicação, que é a parte que quase todo mundo esquece.

# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas históricas abaixo foram preservadas; a revisão R02 não as transforma em execução recente.
# MAGIC
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | requer PySpark e sessão compatível; conferir plano e comportamento no ambiente alvo |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | este exemplo não homologa todos os runtimes; custo exige plano e medidas sobre dados representativos |

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
# MAGIC ```text
# MAGIC biblioteca acessível
# MAGIC ```
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
# MAGIC ```text
# MAGIC DECISÕES (uma linha por decisão de crédito):
# MAGIC +----------+----------+----+
# MAGIC |id_cliente|dt_decisao|alvo|
# MAGIC +----------+----------+----+
# MAGIC |cli00000  |2026-05-27|1   |
# MAGIC |cli00001  |2026-05-30|0   |
# MAGIC |cli00002  |2026-06-27|0   |
# MAGIC +----------+----------+----+
# MAGIC only showing top 3 rows
# MAGIC HISTÓRICO DE SCORE (várias versões por cliente):
# MAGIC +----------+-------------+------------+---------+
# MAGIC |id_cliente|dt_referencia|score_bureau|eh_futura|
# MAGIC +----------+-------------+------------+---------+
# MAGIC |cli00000  |2026-04-30   |413.9       |false    |
# MAGIC |cli00000  |2026-05-09   |813.0       |false    |
# MAGIC |cli00001  |2026-05-15   |354.4       |false    |
# MAGIC |cli00001  |2026-05-23   |482.0       |false    |
# MAGIC |cli00002  |2026-05-28   |692.4       |false    |
# MAGIC |cli00002  |2026-06-04   |878.9       |false    |
# MAGIC +----------+-------------+------------+---------+
# MAGIC only showing top 6 rows
# MAGIC ```
# MAGIC
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
# MAGIC ```text
# MAGIC decisões originais      : 200
# MAGIC linhas após o join      : 433
# MAGIC linhas com score futuro : 33
# MAGIC ```
# MAGIC
# MAGIC Dois estragos aconteceram de uma vez, e nenhum deles emitiu erro:
# MAGIC
# MAGIC **A base inchou.** Cada decisão virou várias linhas, uma por versão do
# MAGIC score. Se você treinar assim, os clientes com mais versões de score pesam
# MAGIC mais no modelo — sem que ninguém tenha decidido isso.
# MAGIC
# MAGIC **Entrou informação do futuro.** As linhas com `eh_futura = true` são
# MAGIC scores posteriores à decisão. Usá-los como características nesse instante
# MAGIC pode produzir uma avaliação otimista, pois eles não estariam disponíveis
# MAGIC na mesma situação de uso real.
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
# MAGIC O parâmetro `atraso_publicacao_dias` merece atenção. Data de referência e
# MAGIC disponibilidade são conceitos distintos; o atraso depende da fonte. No
# MAGIC cenário sintético, o atraso é de 3 dias, então um score de 10/01 só
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
# MAGIC ```text
# MAGIC DIAGNÓSTICO:
# MAGIC   linhas_fato: 200
# MAGIC   com_feature: 200
# MAGIC   sem_chave_ou_data: 0
# MAGIC   entidade_sem_historico: 0
# MAGIC   sem_feature_disponivel_na_data: 0
# MAGIC   cobertura_pct_linhas_validas: 100.0
# MAGIC   linhas_feature_com_ts_nulo: 0
# MAGIC   linhas_com_empate_de_instante: 0
# MAGIC   atraso_publicacao_dias: 3
# MAGIC   janela_maxima_dias: None
# MAGIC   fuso_da_sessao: Etc/UTC
# MAGIC   colunas_trazidas: ['score_bureau', 'eh_futura']
# MAGIC ```
# MAGIC
# MAGIC Compare com o join ingênuo: o número de linhas continua igual ao número
# MAGIC de decisões, e a cobertura diz quantas decisões conseguiram um score
# MAGIC elegível.
# MAGIC
# MAGIC Uma checagem da fixture para a presença dos registros marcados como futuros;
# MAGIC não é prova de ausência de todas as formas de vazamento:

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
# MAGIC ```text
# MAGIC linhas no resultado         : 200
# MAGIC decisões originais          : 200
# MAGIC scores do futuro que entraram: 0   <- tem de ser zero
# MAGIC +----------+----------+----+------------+---------+
# MAGIC |id_cliente|dt_decisao|alvo|score_bureau|eh_futura|
# MAGIC +----------+----------+----+------------+---------+
# MAGIC |cli00000  |2026-05-27|1   |813.0       |false    |
# MAGIC |cli00001  |2026-05-30|0   |482.0       |false    |
# MAGIC |cli00002  |2026-06-27|0   |878.9       |false    |
# MAGIC |cli00003  |2026-04-20|0   |335.7       |false    |
# MAGIC |cli00004  |2026-04-03|1   |654.6       |false    |
# MAGIC +----------+----------+----+------------+---------+
# MAGIC only showing top 5 rows
# MAGIC ```
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
    print(f"atraso {atraso:>3} dias -> cobertura {diag['cobertura_pct_linhas_validas']:>6}%")

# COMMAND ----------

# MAGIC %md
# MAGIC ```text
# MAGIC atraso   0 dias -> cobertura  100.0%
# MAGIC atraso   3 dias -> cobertura  100.0%
# MAGIC atraso  30 dias -> cobertura    5.0%
# MAGIC atraso  60 dias -> cobertura    0.0%
# MAGIC ```
# MAGIC
# MAGIC **A lição:** o atraso não é um detalhe de configuração, é uma
# MAGIC característica da fonte de dados. Descubra o valor real com quem opera a
# MAGIC fonte. Declarar zero é assumir disponibilidade no instante de referência;
# MAGIC isso pode ser correto em algumas fontes, mas precisa ser confirmado.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem saber o atraso de publicação da fonte.** O parâmetro é
# MAGIC   obrigatório de propósito: um palpite errado aqui produz vazamento com
# MAGIC   aparência de rigor. Se ninguém sabe o atraso, descobrir é o primeiro
# MAGIC   passo, não usar zero.
# MAGIC - **Quando uma única data de corte permite solução mais simples.** Ainda
# MAGIC   é necessário selecionar a última versão elegível por chave; só filtrar
# MAGIC   a data não resolve múltiplas versões nem empates.
# MAGIC - **Como garantia contra todo vazamento.** Ele resolve o temporal na
# MAGIC   junção. Alvo construído com informação futura, feature derivada da
# MAGIC   população inteira podem vazar por outros caminhos. Um split aleatório
# MAGIC   também pode ser inadequado em problemas temporais; avalie o desenho.
# MAGIC - **Em volume grande, sem olhar o plano.** A junção é por intervalo, e o
# MAGIC   custo dela depende de otimização que só se confirma com `explain()` sobre
# MAGIC   dado representativo.
# MAGIC
# MAGIC A segunda metade do assunto — separar treino e teste sem vazar — está em
# MAGIC `hub_snippets.ml.split_temporal`.
