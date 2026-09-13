# Databricks notebook source
# MAGIC %md
# MAGIC # `walk_forward` — validar como o modelo vai ser usado
# MAGIC
# MAGIC **O problema.** Uma validação com um corte só responde se o modelo funcionou naquele mês. A pergunta real é se ele funciona mês após mês, retreinado, como vai acontecer em produção. E há uma armadilha a mais: quando o alvo demora a se realizar, treinar até ontem e testar hoje usa rótulo que ainda não existiria.
# MAGIC
# MAGIC **O que este helper faz.** Cria janelas expansivas e chama `model_fn(train, test)` em cada uma, com `gap` opcional. O callback é quem precisa treinar/preprocessar somente no treino e devolver métricas.

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
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC brier: 0.2502 ± 0.0004
# MAGIC n_teste: 200.0000 ± 0.0000
# MAGIC janelas sem gap: 18
# MAGIC
# MAGIC fold  train_end  test_start  n_train  n_test    brier
# MAGIC    1    2024-06     2024-07     1200     200  0.25051
# MAGIC    2    2024-07     2024-08     1400     200  0.25061
# MAGIC    3    2024-08     2024-09     1600     200  0.25008
# MAGIC    4    2024-09     2024-10     1800     200  0.25005
# MAGIC ```
# MAGIC
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
# MAGIC **Como ler.** O `gap` pula posições entre treino e teste e pode representar
# MAGIC **maturação do alvo** quando configurado de acordo com a latência real. Aqui ele
# MAGIC conta períodos observados; uma base com meses ausentes não transforma `gap=3`
# MAGIC automaticamente em três meses corridos. Sem gap, a validação **pode** ficar
# MAGIC otimista quando rótulos recentes ainda não estariam disponíveis no instante
# MAGIC simulado. `pit_join` e `split_temporal` resolvem outros eixos e não escolhem
# MAGIC essa latência por você.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem `gap`, quando o alvo demora a se realizar.** A validação fica otimista por construção.
# MAGIC - **Com poucas janelas.** Três janelas não são evidência de estabilidade; são três números.
# MAGIC - **Sobre DataFrame do Spark.** É pandas: colete antes, com limite.
# MAGIC - **Como substituto de monitoramento.** Ele valida o passado; degradação futura se mede em produção.
