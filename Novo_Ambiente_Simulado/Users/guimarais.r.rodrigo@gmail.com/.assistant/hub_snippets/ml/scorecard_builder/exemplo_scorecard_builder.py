# Databricks notebook source
# MAGIC %md
# MAGIC # `scorecard_builder` — pontos legíveis, que não são probabilidade
# MAGIC
# MAGIC **O problema.** Um scorecard converte um modelo logístico em pontos inteiros para que a decisão seja auditável por quem não lê código. O preço é que os pontos deixam de ser probabilidade — e a leitura natural, de que 620 é o dobro de 310, é falsa.
# MAGIC
# MAGIC **O que este helper faz.** Converte coeficientes e tabelas WOE em pontos, com PDO, score base e odds base declarados.

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

from hub_snippets.ml.scorecard_builder import build_scorecard

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Do modelo para os pontos

# COMMAND ----------

# Coeficientes de um logístico treinado sobre variáveis já transformadas em WOE.
feature_names = ["renda_woe", "tempo_woe", "uso_limite_woe"]
coefs = np.array([-0.45, -0.30, 0.62])  # array, na ordem de feature_names
woe_tables = {
    "renda_woe": pd.DataFrame(
        {"faixa": ["baixa", "media", "alta"], "woe": [0.72, -0.05, -0.81]}
    ),
    "tempo_woe": pd.DataFrame(
        {"faixa": ["<1a", "1-5a", ">5a"], "woe": [0.55, -0.10, -0.60]}
    ),
    "uso_limite_woe": pd.DataFrame(
        {"faixa": ["<30%", "30-70%", ">70%"], "woe": [-0.68, 0.02, 0.90]}
    ),
}

card = build_scorecard(
    coefs=coefs,
    intercept=-2.1,
    feature_names=feature_names,
    woe_tables=woe_tables,
    pdo=20,
    base_score=600,
    base_odds=50,
)
print(card.to_string(index=False))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Cada faixa de cada variável recebe pontos, e o score de um
# MAGIC cliente é a soma das faixas dele — aritmética que qualquer pessoa confere
# MAGIC à mão. É essa a razão de o scorecard existir num setor regulado.
# MAGIC
# MAGIC Os três parâmetros que definem a escala são declarados, não descobertos:
# MAGIC `base_score=600` com `base_odds=50` fixa a referência, e `pdo=20` diz
# MAGIC quantos pontos dobram a chance.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Por que a diferença de pontos não é diferença de risco

# COMMAND ----------

for pontos in (540, 560, 580, 600, 620):
    odds = 50 * 2 ** ((pontos - 600) / 20)
    prob = odds / (1 + odds)
    print(f"  {pontos} pontos -> odds {odds:8.2f} : 1 -> P(bom) = {100 * prob:.2f}%")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A escala é **logarítmica**: cada 20 pontos dobra as odds, não
# MAGIC a probabilidade. Os mesmos 20 pontos valem muito na faixa baixa e quase
# MAGIC nada na alta, como a tabela acima mostra.
# MAGIC
# MAGIC O erro de interpretação mais provável é somar, promediar ou comparar
# MAGIC diferenças de pontos como se fossem risco. "A carteira ganhou 15 pontos em
# MAGIC média" não corresponde a nenhuma variação de inadimplência interpretável.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Tratando pontos como probabilidade.** A escala é log-odds; a conversão exige `pdo`, `base_score` e `base_odds`.
# MAGIC - **Promediando score de carteira.** A média de uma escala logarítmica não é a escala da média.
# MAGIC - **Comparando scorecards com PDO diferentes.** 600 num não é 600 no outro.
# MAGIC - **Sem revalidar as tabelas WOE.** Os pontos herdam o binning; se a distribuição mudou, os pontos mentem antes do modelo.
