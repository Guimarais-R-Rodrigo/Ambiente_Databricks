# Databricks notebook source
# MAGIC %md
# MAGIC # `split_temporal` — separar treino e teste sem embaralhar o tempo
# MAGIC
# MAGIC **O problema.** A separação padrão de treino e teste é aleatória, e ela
# MAGIC pressupõe que as linhas são intercambiáveis. Quando há tempo envolvido, não
# MAGIC são: sortear embaralha períodos, e o modelo treina com dezembro para prever
# MAGIC março. Ele aprende o futuro, acerta no teste, e fracassa em produção — sem
# MAGIC que nenhuma métrica de validação acuse.
# MAGIC
# MAGIC **O que este helper faz.** Corta por período de calendário, não por sorteio:
# MAGIC tudo até uma data treina, tudo depois testa.
# MAGIC
# MAGIC > Este notebook é a segunda metade do assunto **vazamento temporal**. A
# MAGIC > primeira — trazer histórico para a decisão sem trazer o futuro junto —
# MAGIC > está em `hub_snippets.spark.pit_join`. Os dois erros costumam aparecer
# MAGIC > juntos, e corrigir só um deixa o modelo vazando pelo outro.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos; `temporal_split` opera sobre **pandas**, não Spark |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

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
# MAGIC ## 1. O erro: sortear linhas quando há tempo envolvido
# MAGIC
# MAGIC Decidido o que entra na base, falta decidir o que é treino e o que é
# MAGIC teste. Aqui o erro clássico é sortear linhas ao acaso.
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
# MAGIC **Como ler.** Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC convertido para pandas: 720 linhas (volume controlado)
# MAGIC     treino:   480 linhas  |  2025-01-01 a 2026-04-01
# MAGIC  validação:    90 linhas  |  2026-06-01 a 2026-08-01
# MAGIC      teste:    90 linhas  |  2026-10-01 a 2026-12-01
# MAGIC ```
# MAGIC
# MAGIC Os períodos **não se sobrepõem**: cada faixa de datas pertence a uma
# MAGIC partição só. É exatamente isso que o sorteio aleatório destrói.
# MAGIC
# MAGIC Agora some: 480 + 90 + 90 = **660 das 720 linhas**. Sessenta linhas —
# MAGIC 8,3% da base — não estão em partição nenhuma. Os meses **2026-05** e
# MAGIC **2026-09** sumiram, e cada mês vale 30 entidades.
# MAGIC
# MAGIC Não é defeito: é `gap_periods`, que tem padrão **1** e é a decisão de
# MAGIC projeto mais consequente do módulo. O intervalo existe porque o target
# MAGIC leva tempo para se materializar — se você prevê inadimplência em 12
# MAGIC meses, o último mês do treino ainda não sabe o próprio desfecho quando a
# MAGIC validação começa. Sem o intervalo, treino e validação compartilham a
# MAGIC janela em que o target estava se formando, e o teste sai otimista.
# MAGIC
# MAGIC O preço é perder um período em cada fronteira. Vale conferir a conta em
# MAGIC base real: com poucos períodos, `gap_periods=1` pode custar caro, e a
# MAGIC alternativa é declarar `gap_periods=0` **sabendo** o que se está abrindo
# MAGIC mão — não por descuido.
# MAGIC
# MAGIC ## Resumo para levar
# MAGIC
# MAGIC | Situação | O que usar | O que acontece sem |
# MAGIC |---|---|---|
# MAGIC | Separar treino e teste com tempo envolvido | `temporal_split` | teste otimista, produção decepciona |
# MAGIC | Dar tempo ao target para se materializar | `gap_periods` | treino e validação dividem a janela de formação do target |
# MAGIC | Impedir que a mesma entidade caia nos dois lados | `group_col` | o modelo reconhece a entidade, não o padrão |
# MAGIC
# MAGIC Para trazer atributo histórico até a data da decisão — o passo **anterior**
# MAGIC a este —, o helper é `hub_snippets.spark.pit_join`, com notebook próprio.
# MAGIC
# MAGIC Quando precisar de explicação linha a linha do código interno, use a
# MAGIC skill `@hub-ml-tutor-databricks` com o módulo anexado — ela lê a versão
# MAGIC atual do arquivo, então a explicação nunca fica desatualizada.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Passando um DataFrame do Spark.** `temporal_split` é pandas. Colete a
# MAGIC   base — com limite verificável — antes de chamar.
# MAGIC - **Quando não há ordem temporal real.** Se as linhas são de fato
# MAGIC   intercambiáveis, o corte por data só reduz a base de treino sem ganho.
# MAGIC - **Como única defesa contra vazamento.** Ele resolve a separação. Feature
# MAGIC   construída com informação futura continua vazando, e é `pit_join` quem
# MAGIC   trata disso.
# MAGIC - **Com um único ponto de corte, em série longa.** Um corte só mede um
# MAGIC   momento; para saber se o modelo aguenta o tempo, use `walk_forward`.
