# Databricks notebook source
# MAGIC %md
# MAGIC # `drift_detection` — PSI, KS e CSI — três medidas, três perguntas
# MAGIC
# MAGIC **O problema.** Quando alguém pergunta se os dados mudaram, a resposta depende de qual mudança importa. PSI mede deslocamento de forma numa variável numérica, KS a maior distância entre acumuladas, CSI a mesma ideia sobre categoria. Usar o índice errado devolve um número que responde outra pergunta.
# MAGIC
# MAGIC **O que este helper faz.** Calcula os três, e varre várias features de uma vez separando numéricas de categóricas.

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

from hub_snippets.ml.drift_detection import (
    calculate_csi, calculate_ks, calculate_psi, detect_drift_all_features,
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Duas populações que diferem em forma, não em média

# COMMAND ----------

ref = rng.normal(600, 40, 4000)
# metade em 520, metade em 680: mesma média, distribuição partida
atual = np.where(rng.random(4000) < 0.5, rng.normal(520, 25, 4000),
                 rng.normal(680, 25, 4000))

print(f"média  ref {ref.mean():7.2f} | atual {atual.mean():7.2f}")
print(f"desvio ref {ref.std():7.2f} | atual {atual.std():7.2f}")
print(f"PSI    {calculate_psi(ref, atual):.4f}")
ks_stat, ks_p = calculate_ks(ref, atual)  # devolve estatística E p-valor
print(f"KS     {ks_stat:.4f}  (p-valor {ks_p:.2e})")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** As médias praticamente coincidem e o desvio dobra. O PSI sai
# MAGIC alto porque compara a **forma** bin a bin; o KS mede a maior distância
# MAGIC entre as acumuladas, e também acusa.
# MAGIC
# MAGIC O KS vem acompanhado do **p-valor**, e isso muda a leitura: em base
# MAGIC grande, qualquer diferença minúscula sai significante. Com 4.000 linhas de
# MAGIC cada lado, o p-valor deixa de discriminar — a estatística é que informa.
# MAGIC
# MAGIC Os dois respondem perguntas próximas mas não iguais: PSI é sensível a
# MAGIC deslocamento em qualquer região; KS resume tudo num ponto único, o de maior
# MAGIC divergência. Uma mudança espalhada em várias faixas move o PSI e pode não
# MAGIC mover o KS.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Categórica pede CSI, não PSI

# COMMAND ----------

cat_ref = pd.Series(rng.choice(["SP", "RJ", "MG", "BA"], 3000, p=[.4, .3, .2, .1]))
cat_atual = pd.Series(rng.choice(["SP", "RJ", "MG", "BA"], 3000, p=[.25, .25, .25, .25]))
print(f"CSI entre as duas distribuições de UF: {calculate_csi(cat_ref, cat_atual):.4f}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** CSI é a mesma aritmética do PSI aplicada a categorias em vez
# MAGIC de faixas. A diferença que importa é conceitual: em numérica os bins vêm da
# MAGIC referência e são escolha de quem calcula; em categórica as "faixas" já
# MAGIC existem, e o índice fica estável.
# MAGIC
# MAGIC Passar categórica para `calculate_psi` não é erro sutil — é erro de tipo, e
# MAGIC a função não vai fingir que funciona.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Varrer muitas features de uma vez

# COMMAND ----------

base_ref = pd.DataFrame({"score": ref, "renda": rng.normal(5000, 1200, 4000),
                         "uf": cat_ref.sample(4000, replace=True).values})
base_atual = pd.DataFrame({"score": atual, "renda": rng.normal(5100, 1250, 4000),
                           "uf": cat_atual.sample(4000, replace=True).values})

# `feature_cols` é obrigatório e vem antes: ele declara o universo, e as duas
# listas seguintes dizem como tratar cada coluna dele.
relatorio = detect_drift_all_features(
    base_ref, base_atual,
    feature_cols=["score", "renda", "uf"],
    numeric_cols=["score", "renda"],
    categorical_cols=["uf"],
)
print(relatorio.to_string(index=False) if hasattr(relatorio, "to_string") else relatorio)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A varredura separa numéricas de categóricas e aplica o índice
# MAGIC certo em cada uma. `score` deve aparecer bem acima das outras — é a única
# MAGIC construída para mudar.
# MAGIC
# MAGIC O erro de interpretação mais provável: ordenar por índice e tratar o topo
# MAGIC como "as features que quebraram o modelo". Drift de entrada não implica
# MAGIC queda de performance, e uma feature que o modelo quase não usa pode
# MAGIC liderar a lista sem consequência alguma.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como prova de que o modelo piorou.** Mede a entrada; performance se mede com o alvo realizado.
# MAGIC - **Sobre a base inteira, em Spark.** É driver-side: amostre antes, com semente declarada.
# MAGIC - **Aceitando 0,1 e 0,25 como lei.** São heurística de crédito; num score que muda de escala a cada retreino, disparam sem motivo.
# MAGIC - **Em categórica de altíssima cardinalidade sem agrupar.** Cada categoria rara vira termo instável na soma.
