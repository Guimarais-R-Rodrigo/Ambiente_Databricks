# Databricks notebook source
# MAGIC %md
# MAGIC # `display.dataframe_styled` — a tabela que destaca o que precisa ser visto
# MAGIC
# MAGIC **O problema.** Uma tabela de resultado com dez linhas e seis colunas tem sessenta números, e o que decide costuma ser um. Sem destaque, quem lê procura; procurando, erra.
# MAGIC
# MAGIC **O que este objeto oferece.** Formata um DataFrame pandas com destaque por coluna e formatação declarada, devolvendo HTML.

# MAGIC
# MAGIC **Antes de executar:** consulte o [README deste objeto](README.md) para entender o conceito, os requisitos e os efeitos do exemplo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | confira as dependências e a compatibilidade descritas no README; não há equivalência universal entre runtimes |
# MAGIC | Bibliotecas | **instala `jinja2` na primeira célula** — ver a seção 2 |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Efeitos | instala biblioteca e reinicia Python; o helper gera HTML, sem gravar tabela |
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

# `variacao_pp` tem negativos DE PROPOSITO: o realce do helper e por valor
# negativo, nao por limiar. Sem um negativo na base, nada e destacado.
tabela = pd.DataFrame({
    "coluna": ["id_cliente", "renda", "uf", "dt_referencia", "score"],
    "nulos_pct": [0.0, 12.4, 0.3, 0.0, 31.7],
    "distintos": [3375674, 48213, 27, 24, 99812],
    "psi": [0.001, 0.084, 0.012, 0.000, 0.312],
    "variacao_pp": [0.0, -3.2, 0.1, 0.0, -11.5],
})
print(tabela.to_string(index=False))

# COMMAND ----------

# `display_styled` devolve HTML — quem renderiza e o notebook.
# ATENCAO ao format_dict: "{:,.0f}" produz separador AMERICANO (3,375,674),
# que e exatamente o que `constants.format_br` existe para evitar. Formate
# antes, com fmt_int, e passe a coluna ja como texto.
from hub_snippets.constants.format_br import fmt_int

tabela["distintos"] = tabela["distintos"].map(fmt_int)

html = display_styled(
    tabela,
    highlight_cols=["variacao_pp"],
    format_dict={"nulos_pct": "{:.1f}%", "psi": "{:.3f}", "variacao_pp": "{:+.1f}"},
)
displayHTML(html)

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC        coluna  nulos_pct  distintos   psi  variacao_pp
# MAGIC    id_cliente        0.0    3375674 0.001          0.0
# MAGIC         renda       12.4      48213 0.084         -3.2
# MAGIC            uf        0.3         27 0.012          0.1
# MAGIC dt_referencia        0.0         24 0.000          0.0
# MAGIC         score       31.7      99812 0.312        -11.5
# MAGIC ```
# MAGIC
# MAGIC **Como ler — e qual regra de destaque está implementada.**
# MAGIC
# MAGIC O realce **é por valor, restrito às colunas declaradas**: dentro de
# MAGIC `highlight_cols`, ele pinta de vermelho e negrito o que for **negativo**.
# MAGIC Não é gradiente, não é "destaque a coluna inteira", e não conhece limiar
# MAGIC de negócio nenhum.
# MAGIC
# MAGIC Esta demonstração inclui negativos para exercitar o contrato de realce. Valores positivos de PSI ou nulidade não são destacados por essa regra.
# MAGIC
# MAGIC A consequência prática: para "PSI acima de 0,25 é alerta" este helper não
# MAGIC serve como está. Ou você calcula uma coluna de desvio (negativa quando
# MAGIC ruim), ou o limiar vira uma constante e o realce, código seu.
# MAGIC
# MAGIC **E repare no `format_dict`.** `"{:,.0f}"` produz `3,375,674` — separador
# MAGIC americano, dentro de uma biblioteca que tem `constants.format_br`
# MAGIC justamente para evitar isso. A saída de `Styler.format` não passa pelo
# MAGIC nosso formatador; a defesa é formatar antes e entregar a coluna como
# MAGIC texto, que é o que a célula acima faz.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sobre DataFrame do Spark.** É pandas; agregue e limite antes de qualquer coleta, conferindo memória e sensibilidade dos campos.
# MAGIC - **Com centenas de linhas.** O destaque perde função quando tudo está na tela; agregue antes.
# MAGIC - **Como saída de dado.** É apresentação. O que alimenta processo seguinte sai em Parquet, não em HTML.

# MAGIC - **Com HTML não confiável nas células.** O helper não ativa escape. Use dados controlados; o destaque visual não é uma política de sanitização.
