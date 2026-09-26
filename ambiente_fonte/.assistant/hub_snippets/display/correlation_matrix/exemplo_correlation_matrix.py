# Databricks notebook source
# MAGIC %md
# MAGIC # `display.correlation_matrix` — correlação sem ler cem números
# MAGIC
# MAGIC **O problema.** Uma matriz de correlação com 15 variáveis tem 105 pares. Impressa como tabela, ninguém encontra o par que importa — e o par que importa costuma ser o que denuncia redundância ou vazamento.
# MAGIC
# MAGIC **O que este objeto oferece.** Desenha a matriz como mapa de calor e retorna, separadamente, a lista de pares que atingem um limiar declarado. O limiar não acrescenta realce às células.

# MAGIC
# MAGIC **Antes de executar:** consulte o [README deste objeto](README.md) para entender o conceito, os requisitos e os efeitos do exemplo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | confira as dependências e a compatibilidade descritas no README; não há equivalência universal entre runtimes |
# MAGIC | Bibliotecas | Plotly disponível; NumPy para gerar os dados sintéticos desta demonstração |
# MAGIC | Dados | sintéticos, com correlação plantada |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | a falha histórica abaixo exige conferir suporte a `VectorAssembler` e `Correlation.corr` no compute escolhido |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.display.correlation_matrix import plot_correlation

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base com redundância plantada

# COMMAND ----------

import numpy as np
from pyspark.sql import functions as F

rng = np.random.default_rng(42)
n = 3000
renda = rng.normal(5000, 1500, n)
base = spark.createDataFrame(
    [
        (float(renda[i]),
         # limite_credito e quase uma copia de renda: correlacao ~0,97
         float(renda[i] * 3 + rng.normal(0, 400)),
         float(rng.normal(40, 12)),
         float(rng.normal(0, 1)))
        for i in range(n)
    ],
    "renda double, limite_credito double, idade double, ruido double",
)
print(f"linhas: {base.count()} | colunas: {len(base.columns)}")

# COMMAND ----------

try:
    plot_correlation(base, threshold_highlight=0.8)
except Exception as erro:
    print("não executou neste runtime:")
    print(f"  {type(erro).__name__}: {str(erro).splitlines()[0][:150]}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC linhas: 3000 | colunas: 4
# MAGIC não executou neste runtime:
# MAGIC   Py4JError: An error occurred while calling
# MAGIC   None.org.apache.spark.ml.feature.VectorAssembler
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A base foi construída com `limite_credito` valendo três vezes a
# MAGIC `renda` mais um ruído pequeno. O comentário numérico na célula de geração
# MAGIC foi preservado como histórico, mas o coeficiente deve ser calculado, não
# MAGIC inferido daquela anotação. Em um ambiente compatível, esse par deve mostrar
# MAGIC associação positiva forte; a lista de pares e o mapa são saídas distintas.
# MAGIC A transcrição acima registra uma execução antiga, não o teste da R03-B.
# MAGIC
# MAGIC O par redundante é o achado que este helper existe para produzir: duas
# MAGIC variáveis quase idênticas num modelo dividem a importância entre si, e cada
# MAGIC uma parece menos relevante do que é. Em modelo linear, a instabilidade é
# MAGIC pior — os coeficientes podem até trocar de sinal.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Para concluir causalidade.** Correlação alta entre renda e limite não diz qual determina qual — neste caso, sabemos, porque plantamos.
# MAGIC - **Com variável categórica codificada como número.** A correlação de Pearson sobre código de agência mede a ordem do código, que não significa nada.
# MAGIC - **Como único critério de seleção de feature.** Correlação com o alvo ignora interação; variável fraca sozinha pode ser forte em par.
# MAGIC - **Sem avaliar volume e população.** O cálculo distribuído depende de linhas e colunas; Spearman também ordena valores. O driver recebe a matriz k×k, mas isso não elimina custo ou risco de memória. Amostrar pode ser uma decisão justificada, desde que seu efeito na representatividade seja avaliado.
# MAGIC - **Sem conferir nulos e escala.** As linhas incompletas são removidas conjuntamente. A escala sequencial `Blues` deixa correlações negativas fortes claras; leia sinal e módulo, não apenas intensidade da cor.
