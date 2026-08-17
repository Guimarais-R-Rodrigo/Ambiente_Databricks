# Databricks notebook source
# MAGIC %md
# MAGIC # `constants.colors` — a paleta, e por que ela é fechada
# MAGIC
# MAGIC **O problema.** Cada notebook escolhendo cor por conta própria produz um relatório onde a mesma categoria muda de cor entre páginas, e onde 'vermelho' às vezes significa alerta e às vezes é só a terceira série do gráfico.
# MAGIC
# MAGIC **O que este objeto oferece.** Vinte e duas constantes: cores institucionais, paletas prontas e cores com significado declarado.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | nenhum — este objeto não recebe dados |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.constants.colors import COR_ALERTA, COR_NEGATIVO, COR_NEUTRO, COR_POSITIVO, PALETA_CATEGORICA, PALETA_DIVERGENTE, PALETA_SEQUENCIAL

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. As três paletas, e para que serve cada uma

# COMMAND ----------

for nome, paleta in [("CATEGORICA", PALETA_CATEGORICA),
                     ("SEQUENCIAL", PALETA_SEQUENCIAL),
                     ("DIVERGENTE", PALETA_DIVERGENTE)]:
    print(f"{nome:12s} {len(paleta):2d} cores  {paleta}")

# COMMAND ----------

# O valor de uma paleta so aparece quando ela e vista. displayHTML existe no
# notebook; num modulo importado, nao — e por isso o helper devolve string.
def amostra(paleta, rotulo):
    quadrados = "".join(
        f'<span style="display:inline-block;width:44px;height:44px;'
        f'background:{c};border:1px solid #ccc;" title="{c}"></span>'
        for c in paleta
    )
    return f'<div style="margin:8px 0"><b>{rotulo}</b><br>{quadrados}</div>'

displayHTML(
    amostra(PALETA_CATEGORICA, "PALETA_CATEGORICA — séries sem ordem")
    + amostra(PALETA_SEQUENCIAL, "PALETA_SEQUENCIAL — intensidade crescente")
    + amostra(PALETA_DIVERGENTE, "PALETA_DIVERGENTE — desvio em torno de um centro")
)

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC CATEGORICA   10 cores  ['#005CA9', '#F7941D', '#6CBDE1', '#333333', '#8DC63F',
# MAGIC                         '#C4262E', '#7B2D8B', '#00A79D', '#F15A29', '#A7A9AC']
# MAGIC SEQUENCIAL    5 cores  ['#E6F0FA', '#99C2E8', '#4D94D6', '#005CA9', '#003D73']
# MAGIC DIVERGENTE    5 cores  ['#C4262E', '#F7941D', '#FFB800', '#8DC63F', '#005CA9']
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** As três não são intercambiáveis, e trocar uma pela outra muda a
# MAGIC afirmação do gráfico:
# MAGIC
# MAGIC | Paleta | Quando | O que ela afirma |
# MAGIC |---|---|---|
# MAGIC | **Categórica** (10) | séries sem ordem — UF, produto, canal | "estas coisas são diferentes" |
# MAGIC | **Sequencial** (5) | intensidade que só cresce — volume, contagem | "isto é mais que aquilo" |
# MAGIC | **Divergente** (5) | desvio em torno de um centro — variação, resíduo | "isto está acima e aquilo abaixo" |
# MAGIC
# MAGIC O erro que mais aparece é usar sequencial para variação percentual: −20% e
# MAGIC +20% recebem tons de azul de intensidade parecida, e o gráfico esconde
# MAGIC justamente a mudança de sinal, que era o assunto.
# MAGIC
# MAGIC **A categórica acaba em dez** — e isso é limite, não coincidência. Um
# MAGIC gráfico com quinze séries reaproveita cor a partir da décima primeira, e
# MAGIC duas categorias diferentes passam a ter a mesma. Se são quinze, agrupe.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. As cores semânticas são um contrato, não uma sugestão

# COMMAND ----------

for nome, valor in [("COR_POSITIVO", COR_POSITIVO), ("COR_NEGATIVO", COR_NEGATIVO),
                    ("COR_NEUTRO", COR_NEUTRO), ("COR_ALERTA", COR_ALERTA)]:
    print(f"  {nome:16s} {valor}")

displayHTML("".join(
    f'<span style="background:{v};color:#fff;padding:6px 14px;margin-right:8px;'
    f'border-radius:4px;font-family:Segoe UI">{n}</span>'
    for n, v in [("POSITIVO", COR_POSITIVO), ("NEGATIVO", COR_NEGATIVO),
                 ("NEUTRO", COR_NEUTRO), ("ALERTA", COR_ALERTA)]
))

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC COR_POSITIVO     #8DC63F
# MAGIC COR_NEGATIVO     #C4262E
# MAGIC COR_NEUTRO       #6C757D
# MAGIC COR_ALERTA       #FFB800
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Estas quatro existem para que "verde" signifique a mesma coisa em
# MAGIC todo o material. É um contrato barato de manter e caro de perder: um
# MAGIC relatório em que vermelho às vezes é alerta e às vezes é só a sexta série
# MAGIC da paleta categórica ensina o leitor a ignorar a cor.
# MAGIC
# MAGIC Repare que `COR_POSITIVO` **é** o `VERDE` da paleta categórica, e
# MAGIC `COR_NEGATIVO` **é** o `VERMELHO`. Ou seja, um gráfico categórico com seis
# MAGIC ou mais séries vai usar as duas cores semânticas como cor qualquer. Não há
# MAGIC como o módulo evitar isso — mas vale saber, porque é onde o contrato se
# MAGIC rompe sozinho.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Com mais de dez categorias.** A paleta categórica acaba em dez; a partir da décima primeira, cor deixa de distinguir. Agrupe em "outros" antes.
# MAGIC - **Para escala contínua com zero significativo.** Use a divergente, não a sequencial — a sequencial esconde o sinal da diferença.
# MAGIC - **Como sistema de acessibilidade.** Nenhuma destas paletas foi verificada para daltonismo. Cor sozinha nunca deve carregar a informação.
