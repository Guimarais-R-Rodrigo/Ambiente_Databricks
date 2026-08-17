# Databricks notebook source
# MAGIC %md
# MAGIC # `constants.styles` — CSS compartilhado para `displayHTML`
# MAGIC
# MAGIC **O problema.** Cada bloco de HTML num notebook carrega seu próprio `style="..."` inline, e a primeira mudança de identidade visual exige editar dezenas de notebooks. Pior: as versões divergem, e o relatório fica com três tons de cinza que deveriam ser um.
# MAGIC
# MAGIC **O que este objeto oferece.** Nove constantes de CSS, prontas para interpolar em `displayHTML`.

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

from hub_snippets.constants.styles import FONT_FAMILY, STYLE_BADGE_FAIL, STYLE_BADGE_OK, STYLE_BADGE_WARN, STYLE_DIVIDER_HEAVY, STYLE_DIVIDER_LIGHT, STYLE_KPI_CARD, STYLE_SECTION_HEADER

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. O efeito de cada estilo, renderizado

# COMMAND ----------

displayHTML(f"""
<div style="{STYLE_SECTION_HEADER}">
  <b>STYLE_SECTION_HEADER</b> — cabeçalho de seção, com a barra à esquerda
</div>
<span style="{STYLE_KPI_CARD}">STYLE_KPI_CARD — 3.375.674 linhas</span>
<span style="{STYLE_KPI_CARD}">92,8% de cobertura</span>
<hr style="{STYLE_DIVIDER_LIGHT}">
<span style="{STYLE_BADGE_OK}">OK</span>
<span style="{STYLE_BADGE_WARN}">ATENÇÃO</span>
<span style="{STYLE_BADGE_FAIL}">FALHA</span>
<hr style="{STYLE_DIVIDER_HEAVY}">
""")

# COMMAND ----------

print("FONT_FAMILY:", FONT_FAMILY)
print("")
print("STYLE_SECTION_HEADER:")
print(" ", STYLE_SECTION_HEADER)

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC FONT_FAMILY: Segoe UI, Roboto, sans-serif
# MAGIC
# MAGIC STYLE_SECTION_HEADER:
# MAGIC   background:#F8F9FA; border-left:4px solid #005CA9; padding:12px 16px;
# MAGIC   margin:8px 0 12px 0; border-radius:4px; font-family:Segoe UI, Roboto, sans-serif;
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** São strings de CSS, prontas para interpolar dentro de um
# MAGIC `style="..."`. A escolha de entregar string em vez de função é deliberada:
# MAGIC assim elas compõem com qualquer HTML, e nada no módulo precisa saber o que
# MAGIC está sendo estilizado.
# MAGIC
# MAGIC ## Dívida registrada: os hexadecimais estão copiados
# MAGIC
# MAGIC Repare no `#005CA9` da borda esquerda e no `#F8F9FA` do fundo. Os dois
# MAGIC existem em `constants.colors` como `AZUL_CAIXA` e `BG_SECTION` — e este
# MAGIC módulo **não importa nenhum dos dois**. Ele não tem uma linha de `import`.
# MAGIC
# MAGIC Consequência prática: uma mudança de identidade visual feita em
# MAGIC `colors.py` não alcança os estilos. Os cabeçalhos continuariam azuis
# MAGIC enquanto os gráficos mudariam de cor, e o sintoma apareceria como
# MAGIC "inconsistência do relatório", longe da causa.
# MAGIC
# MAGIC É o mesmo padrão de `PALETA_CATEGORICA` redeclarada em `ml.curves_plotly`,
# MAGIC registrado no notebook daquele objeto. Unificar muda o comportamento de
# MAGIC quem já usa, e por isso é decisão de produto — etapa 2, não conversão.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Em e-mail.** Cliente de e-mail ignora boa parte de CSS moderno; o que renderiza aqui não renderiza lá.
# MAGIC - **Como folha de estilo de aplicação.** São strings para interpolar em HTML de notebook, não um sistema de design.
# MAGIC - **Editando a string na chamada.** Se precisa de variação, acrescente uma constante ao módulo — a próxima pessoa vai procurar lá.
