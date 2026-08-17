# Databricks notebook source
# MAGIC %md
# MAGIC # `walk_forward` — validar como o modelo vai ser usado
# MAGIC
# MAGIC **O problema.** Uma validação com um corte só responde se o modelo funcionou naquele mês. A pergunta real é se ele funciona mês após mês, retreinado, como vai acontecer em produção. E há uma armadilha a mais: quando o alvo demora a se realizar, treinar até ontem e testar hoje usa rótulo que ainda não existiria.
# MAGIC
# MAGIC **O que este helper faz.** Roda validação que avança no tempo, retreinando a cada janela, com `gap` entre treino e teste.

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

from hub_snippets.ml.walk_forward import walk_forward_cv

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Um painel mensal e um baseline honesto

# COMMAND ----------

meses = pd.date_range("2024-01-01", periods=24, freq="MS")
linhas = []
for mes in meses:
    for _ in range(200):
        x = float(rng.normal(0, 1))
        linhas.append(
            {"dt": mes, "x": x, "y": int(rng.random() < 1 / (1 + np.exp(-x)))}
        )
painel = pd.DataFrame(linhas)


def modelo_simples(treino, teste):
    """Prediz pela média do treino: baseline que não aprende nada.

    O contrato de `model_fn` é devolver um **dicionário** de métricas, não um
    número — assim cada janela pode reportar mais de uma, e a coluna do
    resultado tem nome.
    """
    predito = np.full(len(teste), treino["y"].mean())
    erro = float(np.mean((teste["y"] - predito) ** 2))
    return {"brier": round(erro, 5), "n_teste": len(teste)}


sem_gap = walk_forward_cv(
    painel, date_col="dt", target_col="y", model_fn=modelo_simples,
    min_train_periods=6, test_periods=1, step=1, gap=0,
)
print(f"janelas sem gap: {len(sem_gap)}")
print(sem_gap.head(6).to_string(index=False) if hasattr(sem_gap, "head") else sem_gap[:6])

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Cada linha é uma janela: treina com os meses anteriores,
# MAGIC testa no seguinte, avança. O número de janelas sai de `min_train_periods`,
# MAGIC `test_periods` e `step` — e é ele que diz quanta evidência a validação
# MAGIC produziu de fato.
# MAGIC
# MAGIC A **dispersão** entre janelas importa mais que a média: métrica média boa
# MAGIC com variância alta é um modelo que funciona em alguns meses.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O `gap`, que quase ninguém usa

# COMMAND ----------

com_gap = walk_forward_cv(
    painel, date_col="dt", target_col="y", model_fn=modelo_simples,
    min_train_periods=6, test_periods=1, step=1, gap=3,
)
print(f"janelas sem gap : {len(sem_gap)}")
print(f"janelas com gap : {len(com_gap)}   (gap = 3 meses)")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O `gap` descarta os períodos entre treino e teste, e existe
# MAGIC para um caso concreto: **quando o alvo demora a se realizar**. Se a
# MAGIC inadimplência só é conhecida três meses depois da originação, treinar com
# MAGIC dados até maio para prever junho usa rótulos que, em junho, ainda não
# MAGIC existiriam.
# MAGIC
# MAGIC Sem `gap` a validação fica otimista e nada acusa: o número sai bom porque
# MAGIC a informação vazou pela janela, não pela feature. É a forma de vazamento
# MAGIC que sobrevive tanto ao `pit_join` quanto ao `split_temporal`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem `gap`, quando o alvo demora a se realizar.** A validação fica otimista por construção.
# MAGIC - **Com poucas janelas.** Três janelas não são evidência de estabilidade; são três números.
# MAGIC - **Sobre DataFrame do Spark.** É pandas: colete antes, com limite.
# MAGIC - **Como substituto de monitoramento.** Ele valida o passado; degradação futura se mede em produção.
