# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.theme_plotly` — o tema, aplicado ao gráfico e não copiado nele
# MAGIC
# MAGIC **O problema.** Cada gráfico com seu `update_layout` produz vinte variações de fonte, margem e cor de fundo no mesmo relatório. E a decisão de mostrar quantos pontos foram plotados, que é a mais importante, ninguém repete.
# MAGIC
# MAGIC **O que este objeto oferece.** Aplica o tema institucional a uma figura Plotly, com subtítulo, fonte e a contagem de pontos declarada no rodapé.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | `plotly`, já presente no runtime |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.visual.theme_plotly import aplicar_tema, get_tema_eda, registrar_template_plotly

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. O mesmo gráfico, sem e com o tema

# COMMAND ----------

import numpy as np
import plotly.graph_objects as go

rng = np.random.default_rng(42)
x = np.arange(24)
y = 100 + np.cumsum(rng.normal(2, 6, 24))

figura = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", name="volume"))
figura.update_layout(title="Sem tema — o padrão do Plotly")
figura.show()

# COMMAND ----------

figura2 = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", name="volume"))
figura2.update_layout(title="Com tema")
aplicar_tema(
    figura2,
    subtitulo="Volume mensal, base sintética",
    fonte="hub_snippets.testing.fixtures",
    n=len(x),
)
figura2.show()

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** As duas figuras mostram os mesmos dados. A diferença que importa
# MAGIC não é a cor — é o **rodapé**: a versão com tema declara a fonte dos dados e
# MAGIC quantos pontos foram plotados.
# MAGIC
# MAGIC Parece detalhe e não é. Um gráfico de amostra e um gráfico da base inteira
# MAGIC são visualmente idênticos, e a diferença entre eles decide se a cauda que
# MAGIC não aparece é ausência de dado ou ausência de amostra. Sem o `n` no
# MAGIC rodapé, ninguém tem como saber — inclusive quem fez, três semanas depois.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O que há dentro do tema

# COMMAND ----------

tema = get_tema_eda()
for chave, valor in tema.items():
    texto = str(valor)
    print(f"  {chave:20s} {texto[:88]}{'...' if len(texto) > 88 else ''}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC template     plotly_white
# MAGIC font         {'family': 'Segoe UI, Roboto, sans-serif', 'size': 12, 'color': '#333333'}
# MAGIC title        {'font': {'size': 16, 'color': '#005CA9'}, 'x': 0.01, 'xanchor': 'left'}
# MAGIC colorway     ['#005CA9', '#F7941D', '#6CBDE1', '#333333', '#8DC63F', '#C4262E',
# MAGIC               '#7B2D8B', '#00A79D', '#F15A29', '#A7A9AC']
# MAGIC height       450
# MAGIC width        900
# MAGIC margin       {'l': 60, 'r': 30, 't': 70, 'b': 60}
# MAGIC legend       {'orientation': 'h', 'yanchor': 'bottom', 'y': -0.25, ...}
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O `colorway` são as **dez cores** de `PALETA_CATEGORICA`, e este
# MAGIC módulo as importa de `constants.colors` de verdade — não as redeclara. É o
# MAGIC contraexemplo positivo dos casos registrados em `constants.styles` e
# MAGIC `visual.badge`, onde a cópia foi feita.
# MAGIC
# MAGIC Duas escolhas de layout merecem nota. O **título alinhado à esquerda**
# MAGIC (`x: 0.01`) segue a leitura da página em vez de centralizar; e a
# MAGIC **legenda horizontal embaixo** (`y: -0.25`) devolve ao gráfico a largura
# MAGIC que uma legenda lateral consome — o que importa quando há série com nome
# MAGIC longo, que é o caso de quase toda categoria de negócio.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem declarar `n`.** O rodapé com a contagem é a parte que impede alguém de ler um gráfico de amostra como se fosse a base inteira.
# MAGIC - **Depois de `update_layout` com as mesmas chaves.** A ordem importa: aplique o tema por último, ou a customização volta ao padrão.
# MAGIC - **Em gráfico que vai para fora do Databricks.** A fonte `Segoe UI` pode não existir no destino, e o layout desloca.
