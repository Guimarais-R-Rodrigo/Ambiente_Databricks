# Databricks notebook source
# MAGIC %md
# MAGIC # `lgbm_temporal` — lags e janelas, com a entidade no lugar certo
# MAGIC
# MAGIC **O problema.** Criar lag e média móvel é trivial num painel de uma série. Num painel de muitas entidades — clientes, contratos, agências — a mesma operação sem particionar por entidade puxa o valor do **cliente anterior** para dentro da feature. O resultado é plausível, e o modelo aprende ruído.
# MAGIC
# MAGIC **O que este helper faz.** Cria lags, rollings, calendário e tendência em pandas. `entity_cols` é opcional para série única; em painel, declará-la isola o histórico por entidade. O objeto não treina LightGBM apesar do nome legado.

# MAGIC
# MAGIC **Guia local completo:** [README deste objeto](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side** |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

from hub_snippets.ml.lgbm_temporal import create_temporal_features

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Um painel de várias entidades

# COMMAND ----------

meses = pd.date_range("2025-01-01", periods=12, freq="MS")
linhas = []
for ent in ("A", "B", "C"):
    nivel = {"A": 100, "B": 500, "C": 900}[ent]
    for m in meses:
        linhas.append({"id": ent, "dt": m, "valor": nivel + float(rng.normal(0, 5))})
painel = pd.DataFrame(linhas).sort_values(["id", "dt"]).reset_index(drop=True)

print(painel.groupby("id")["valor"].mean().round(1).to_string())

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** As três entidades vivem em patamares muito diferentes — 100,
# MAGIC 500 e 900. É de propósito: se o lag vazar entre entidades, a diferença
# MAGIC aparece de forma gritante em vez de se esconder no ruído.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Com a entidade declarada

# COMMAND ----------

com_ent = create_temporal_features(
    painel, target_col="valor", date_col="dt",
    lags=[1], rolling_windows=[3], entity_cols=["id"],
)
print(f"linhas restantes: {len(com_ent)}")
print("linhas por entidade:", com_ent.groupby("id").size().to_dict())
print("primeira data que sobrou, por entidade:",
      {k: str(v.date()) for k, v in com_ent.groupby("id")["dt"].min().items()})

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC Features temporais: 9 linhas removidas por NaN de lags
# MAGIC linhas restantes: 27
# MAGIC linhas por entidade: {'A': 9, 'B': 9, 'C': 9}
# MAGIC primeira data que sobrou, por entidade: {'A': '2025-04-01', 'B': '2025-04-01', 'C': '2025-04-01'}
# MAGIC ```
# MAGIC
# MAGIC Nove linhas removidas, **três por entidade** — cada uma perde os três
# MAGIC primeiros meses, que é o que a janela móvel de 3 exige para existir. É por
# MAGIC isso que todas as entidades passam a começar em abril.
# MAGIC
# MAGIC Repare no que **não** dá para conferir aqui: a função termina com um
# MAGIC `dropna()`, de modo que o DataFrame devolvido tem zero nulos por
# MAGIC construção. Contar nulos na saída não diagnostica nada — o número é sempre
# MAGIC zero, com ou sem vazamento. O que denuncia é **quantas linhas foram
# MAGIC removidas**, e a próxima seção mostra por quê.

# COMMAND ----------
# MAGIC %md
# MAGIC Sem entity_cols, datas repetidas são recusadas pelo default on_duplicate_dates="raise". A próxima chamada é um contraexemplo intencional e deve ser executada esperando ValueError. Para uma demonstração separada da contaminação entre entidades, use keep deliberadamente e compare lags por entidade; não adote essa configuração para o painel real.

# COMMAND ----------

sem_ent = create_temporal_features(
    painel, target_col="valor", date_col="dt",
    lags=[1], rolling_windows=[3],
)
print(f"linhas restantes: {len(sem_ent)}")
print("linhas por entidade:", sem_ent.groupby("id").size().to_dict())

# a linha que denuncia: B vive perto de 500 — de onde veio o lag dela?
b_com = com_ent[com_ent["id"] == "B"].iloc[0]
b_sem = sem_ent[sem_ent["id"] == "B"].iloc[0]
print("")
print(f"primeira linha de B, com entidade : dt={b_com['dt'].date()}  lag_1={b_com['lag_1']:.1f}")
print(f"primeira linha de B, sem entidade : dt={b_sem['dt'].date()}  lag_1={b_sem['lag_1']:.1f}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Saída preservada de um ensaio com implementação anterior à
# MAGIC recusa padrão de datas repetidas. A chamada acima, com o default atual,
# MAGIC lança ValueError e não produz as 33 linhas mostradas abaixo. O bloco
# MAGIC ilustra o risco de misturar entidades, não um resultado atual garantido.
# MAGIC
# MAGIC ```text
# MAGIC Features temporais: 3 linhas removidas por NaN de lags
# MAGIC linhas restantes: 33
# MAGIC linhas por entidade: {'A': 11, 'B': 11, 'C': 11}
# MAGIC
# MAGIC primeira linha de B, com entidade : dt=2025-04-01  lag_1=502.3
# MAGIC primeira linha de B, sem entidade : dt=2025-02-01  lag_1=898.2
# MAGIC ```
# MAGIC
# MAGIC **Sobraram 33 linhas em vez de 27.** Sem `entity_cols` você perde menos
# MAGIC dados, começa o painel dois meses antes e o modelo treina com mais
# MAGIC exemplos. Toda métrica de volume melhora. É por isso que o erro sobrevive:
# MAGIC ele não parece erro, parece eficiência.
# MAGIC
# MAGIC A denúncia está numa linha só. B vive perto de **500**. Com a entidade
# MAGIC declarada, o lag de B é **502,3** — o próprio mês anterior de B. Sem ela, o
# MAGIC lag de B é **898,2**, que é o valor de **C** em janeiro: a função ordena
# MAGIC por data, e a linha anterior à de B em fevereiro é a de C em janeiro.
# MAGIC
# MAGIC O modelo aprende que "o mês passado desta entidade valia 898" para uma
# MAGIC entidade que nunca passou de 510. O treino converge, a métrica sai boa, e o
# MAGIC erro só aparece em produção — onde as entidades não chegam nessa ordem.
# MAGIC
# MAGIC A verificação que funciona: **compare a contagem de linhas removidas**. Com
# MAGIC `entity_cols`, ela é proporcional ao número de entidades (9 = 3 × 3). Sem,
# MAGIC ela é a de um painel só (3). Remoção pequena demais é a assinatura do
# MAGIC vazamento lateral.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem `entity_cols`, em painel de várias entidades.** É o erro que este notebook existe para mostrar.
# MAGIC - **Com data que não possa ser normalizada ou grão temporal mal definido.** A implementação atual ordena internamente; o risco é fornecer data/grão sem semântica adequada, não deixar de pré-ordenar.
# MAGIC - **Em série com buracos.** Lag de 1 é a linha anterior, não o mês anterior — se faltam meses, os dois deixam de coincidir.
# MAGIC - **Sobre DataFrame do Spark.** É pandas: colete antes, com limite.

# COMMAND ----------
# MAGIC %md
# MAGIC Contrato de entrada: datas são normalizadas antes da ordenação; date_format é obrigatório para texto ambíguo. lag_n significa n observações anteriores da entidade, não n períodos de calendário. A função preserva colunas do chamador e verifica colisões com novas features.
