# Databricks notebook source
# MAGIC %md
# MAGIC # `optuna_lgbm` — busca de hiperparâmetro que para quando deve
# MAGIC
# MAGIC **O problema.** Grid search testa combinações que já se sabe ruins e gasta o orçamento nas bordas. E busca sem validação separada acha o melhor jeito de decorar o conjunto de teste.
# MAGIC
# MAGIC **O que este helper faz.** Roda busca bayesiana com Optuna sobre o espaço do LightGBM, medindo na validação e devolvendo o estudo completo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `lightgbm e optuna` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma — este módulo não registra em lugar nenhum |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~1 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install lightgbm optuna

# COMMAND ----------
# MAGIC %restart_python

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparação
# MAGIC
# MAGIC `%restart_python` reinicia o interpretador, então tudo — inclusive o
# MAGIC `sys.path` — precisa vir **depois** dele.

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np

rng = np.random.default_rng(42)

from hub_snippets.ml.optuna_lgbm import optimize_lgbm


# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma busca curta, para caber no laboratório

# COMMAND ----------

n = 5000
X = rng.normal(0, 1, (n, 6))
y = ((1.1 * X[:, 0] - 0.7 * X[:, 1] + rng.normal(0, 0.9, n)) > 0.8).astype(int)

corte = 3800
X_tr, y_tr = X[:corte], y[:corte]
X_va, y_va = X[corte:], y[corte:]

# 15 trials e pouco para producao e suficiente para ver o mecanismo.
melhores, estudo = optimize_lgbm(X_tr, y_tr, X_va, y_va, task="binary", n_trials=15, metric="auc")
print("melhores parametros:")
for chave, valor in melhores.items():
    print(f"  {chave:24s} {valor}")
print("")
print(f"melhor valor: {estudo.best_value:.4f} | trials concluidos: {len(estudo.trials)}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC melhores parametros:
# MAGIC   learning_rate            0.0151
# MAGIC   num_leaves               70
# MAGIC   max_depth                3
# MAGIC   min_child_samples        92
# MAGIC   subsample                0.6294
# MAGIC   colsample_bytree         0.8313
# MAGIC   reg_alpha                0.0177
# MAGIC   reg_lambda               0.1203
# MAGIC
# MAGIC melhor valor: 0.9033 | trials concluidos: 15
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Quinze trials, melhor AUC **0,9033**. Os AUCs individuais dos
# MAGIC trials, que aparecem no log acima, ficaram entre **0,8926 e 0,9033** — uma
# MAGIC faixa de **um ponto percentual**. É o resultado típico e o mais mal
# MAGIC interpretado da otimização de hiperparâmetro.
# MAGIC
# MAGIC Repare na combinação escolhida: `num_leaves` **70** com `max_depth` **3**.
# MAGIC Uma árvore de profundidade 3 tem no máximo 8 folhas, então o limite de 70
# MAGIC **nunca é alcançado** — o parâmetro é inerte nesta combinação. A busca não
# MAGIC errou; ela simplesmente encontrou uma região onde aquele eixo não importa,
# MAGIC e qualquer valor ali dá no mesmo. Ler a lista como "os parâmetros ideais" e
# MAGIC transplantá-la para outro problema propaga um número sem sentido.
# MAGIC
# MAGIC E `min_child_samples` **92**, contra 20 do padrão, é a informação útil de
# MAGIC verdade: a busca pediu folhas bem maiores, o que costuma indicar que o
# MAGIC padrão estava permitindo folha específica demais para esta base.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Com poucos trials.** Abaixo de ~30, a busca bayesiana ainda está explorando; o resultado é quase sorteio.
# MAGIC - **Sobre a mesma partição usada para reportar.** O ótimo encontrado é ótimo *daquela* validação; reporte num terceiro conjunto.
# MAGIC - **Antes de ter feature boa.** Hiperparâmetro rende alguns pontos decimais; feature nova rende ordens de grandeza.
