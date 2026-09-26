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

# MAGIC
# MAGIC **Guia local completo:** [README deste objeto](README.md).
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
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC mob  incidencia          mob  incidencia
# MAGIC   1  0.0100                7  0.2583
# MAGIC   2  0.0283                8  0.3183
# MAGIC   3  0.0617                9  0.3683
# MAGIC   4  0.1017               10  0.4300
# MAGIC   5  0.1550               11  0.4833
# MAGIC   6  0.2000               12  0.5417
# MAGIC
# MAGIC somando as taxas por MOB  : 295.7%   <- errado
# MAGIC contratos afetados        :  54.2%   <- correto
# MAGIC a soma exagera em 5.5x
# MAGIC ```
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
# MAGIC ### Nota de cor — resolvida em 18/08/2026
# MAGIC
# MAGIC Este módulo **redeclarava** `PALETA_CATEGORICA`, `AZUL_CAIXA` e
# MAGIC `PALETA_SEQUENCIAL` com literais idênticos aos de
# MAGIC `hub_snippets.constants.colors`. Hoje ele os **deriva** de lá, e a paleta
# MAGIC tem uma fonte só. Os nomes continuam na API pública do módulo, então nada
# MAGIC que importava daqui quebrou.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. A tabela de safras, que é o que o módulo entrega
# MAGIC
# MAGIC Até aqui o notebook mostrou **por que** a análise de safra existe. Esta
# MAGIC seção usa o módulo.
# MAGIC
# MAGIC Duas colunas de data precisam existir, e a fixture não as traz de graça:
# MAGIC `dt_originacao` é a safra virada em data, e `dt_referencia` é a foto. O
# MAGIC parâmetro `mob_col` diz que o MOB já está calculado — mas **não dispensa**
# MAGIC `dt_referencia`, que continua obrigatório. A célula abaixo fabrica `dt_ref` com
# MAGIC `mob × 30 dias` apenas para satisfazer o exemplo sintético; como `mob_col` é
# MAGIC fornecido, essa data não define o MOB e **30 dias não deve ser tratado como mês**.

# COMMAND ----------

import pandas as pd

from hub_snippets.ml.vintage_analysis import (
    build_vintage_table,
    compare_safras,
    plot_vintage_curves,
    plot_vintage_heatmap,
)

painel_pd["dt_orig"] = pd.to_datetime(painel_pd["safra"], format="%Y%m")
painel_pd["dt_ref"] = painel_pd["dt_orig"] + pd.to_timedelta(painel_pd["mob"] * 30, unit="D")

tabela = build_vintage_table(
    painel_pd,
    contract_id="id_contrato",
    dt_originacao="dt_orig",
    dt_referencia="dt_ref",
    target="inadimplente",
    mob_col="mob",
)
print(f"linhas na tabela de safras: {len(tabela)}")
print(tabela.head(8).to_string(index=False))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Vintage table: 3 safras, MOB range [0-12]
# MAGIC linhas na tabela de safras: 39
# MAGIC   safra  mob  n_contratos_observados  n_eventos_acumulados  n_contratos_safra  taxa_acumulada  cobertura_observada  taxa
# MAGIC 2025-01    0                     200                   0.0                200            0.00                  1.0  0.00
# MAGIC 2025-01    1                     200                   4.0                200            0.02                  1.0  0.02
# MAGIC 2025-01    2                     200                   6.0                200            0.03                  1.0  0.03
# MAGIC 2025-01    3                     200                  14.0                200            0.07                  1.0  0.07
# MAGIC 2025-01    4                     200                  22.0                200            0.11                  1.0  0.11
# MAGIC 2025-01    5                     200                  32.0                200            0.16                  1.0  0.16
# MAGIC 2025-01    6                     200                  46.0                200            0.23                  1.0  0.23
# MAGIC 2025-01    7                     200                  58.0                200            0.29                  1.0  0.29
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Uma linha por safra × MOB. A taxa acumulada é a fração de
# MAGIC contratos daquela safra que já tinham entrado em inadimplência **até**
# MAGIC aquele MOB. O helper só publica essa taxa quando todos os contratos da safra
# MAGIC estão observados naquele MOB; célula parcial fica `NaN`, não zero.
# MAGIC
# MAGIC A comparação entre safras só é honesta no mesmo MOB. É a armadilha que a
# MAGIC seção anterior demonstrou com números.

# COMMAND ----------

comparacao = compare_safras(tabela)
print(comparacao.to_string(index=False))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC   safra  n_contratos  taxa_mob_3  taxa_mob_6  taxa_mob_12 taxa_mob_24  vs_media_mob_3  vs_media_mob_6  vs_media_mob_12 vs_media_mob_24
# MAGIC 2025-01          200       0.070       0.230        0.555        None        0.008333           0.030         0.013333             NaN
# MAGIC 2025-02          200       0.050       0.145        0.530        None       -0.011667          -0.055        -0.011667             NaN
# MAGIC 2025-03          200       0.065       0.225        0.540        None        0.003333           0.025        -0.001667             NaN
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Cada linha é uma safra, cada coluna um checkpoint de MOB.
# MAGIC Célula vazia não é zero: é safra que ainda não chegou àquele MOB, e essa é
# MAGIC exatamente a diagonal incompleta que não se preenche com zero.

# COMMAND ----------

fig_curvas = plot_vintage_curves(tabela)
fig_heatmap = plot_vintage_heatmap(tabela)
print(f"curvas  : {type(fig_curvas).__name__} com {len(fig_curvas.data)} série(s)")
print(f"heatmap : {type(fig_heatmap).__name__} com {len(fig_heatmap.data)} camada(s)")

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC curvas  : Figure com 3 série(s)
# MAGIC heatmap : Figure com 1 camada(s)
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** As duas funções devolvem figuras Plotly e **não desenham
# MAGIC nada sozinhas** — quem renderiza é o notebook, com `fig.show()`. É a mesma
# MAGIC separação de `theme_plotly` e `badge`: o helper devolve o objeto, a
# MAGIC exibição é decisão de quem chama.
