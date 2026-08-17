# Databricks notebook source
# MAGIC %md
# MAGIC # `display.dataframe_styled` — a tabela que destaca o que precisa ser visto
# MAGIC
# MAGIC **O problema.** Uma tabela de resultado com dez linhas e seis colunas tem sessenta números, e o que decide costuma ser um. Sem destaque, quem lê procura; procurando, erra.
# MAGIC
# MAGIC **O que este objeto oferece.** Formata um DataFrame pandas com destaque por coluna e formatação declarada, devolvendo HTML.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `jinja2` na primeira célula** — ver a seção 2 |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------
# MAGIC %pip install jinja2

# COMMAND ----------
# MAGIC %restart_python

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.display.dataframe_styled import display_styled

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma tabela de diagnóstico, com e sem destaque

# COMMAND ----------

import pandas as pd

tabela = pd.DataFrame({
    "coluna": ["id_cliente", "renda", "uf", "dt_referencia", "score"],
    "nulos_pct": [0.0, 12.4, 0.3, 0.0, 31.7],
    "distintos": [3375674, 48213, 27, 24, 99812],
    "psi": [0.001, 0.084, 0.012, 0.000, 0.312],
})
print(tabela.to_string(index=False))

# COMMAND ----------

# `display_styled` devolve HTML — quem renderiza e o notebook.
html = display_styled(
    tabela,
    highlight_cols=["nulos_pct", "psi"],
    format_dict={"nulos_pct": "{:.1f}%", "psi": "{:.3f}", "distintos": "{:,.0f}"},
)
displayHTML(html)

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC        coluna  nulos_pct  distintos   psi
# MAGIC    id_cliente        0.0    3375674 0.001
# MAGIC         renda       12.4      48213 0.084
# MAGIC            uf        0.3         27 0.012
# MAGIC dt_referencia        0.0         24 0.000
# MAGIC         score       31.7      99812 0.312
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A tabela crua acima tem vinte números, e dois decidem: `score`
# MAGIC com **31,7%** de nulos e **PSI 0,312**. A versão estilizada destaca as duas
# MAGIC colunas pedidas e formata cada uma na sua escala — percentual com uma casa,
# MAGIC PSI com três, contagem com separador de milhar.
# MAGIC
# MAGIC Repare que o destaque é **por coluna**, não por valor. A função não sabe
# MAGIC quais valores são ruins; ela realça a coluna que você declarou que importa,
# MAGIC e o gradiente faz o resto. Isso é uma limitação honesta: um limiar de
# MAGIC negócio ("PSI acima de 0,25 é alerta") continua sendo decisão sua, e o
# MAGIC lugar dele é uma constante nomeada no seu notebook.
# MAGIC
# MAGIC E é o formato que expõe a diferença de escala. `distintos` com 3.375.674 ao
# MAGIC lado de `psi` com 0,001 na mesma tabela sem formatação é ilegível; com
# MAGIC `format_dict`, as duas colunas passam a ser comparáveis com a vizinha.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sobre DataFrame do Spark.** É pandas; colete antes, com limite.
# MAGIC - **Com centenas de linhas.** O destaque perde função quando tudo está na tela; agregue antes.
# MAGIC - **Como saída de dado.** É apresentação. O que alimenta processo seguinte sai em Parquet, não em HTML.
