# Databricks notebook source
# MAGIC %md
# MAGIC # `constants.styles` — CSS compartilhado para `displayHTML`
# MAGIC
# MAGIC **O problema.** Cada bloco de HTML num notebook pode carregar seu próprio `style="..."` inline, e uma mudança de identidade visual passa a exigir edição dispersa. O módulo mantém as constantes legadas e oferece uma materialização opt-in a partir do Sistema de Temas.
# MAGIC
# MAGIC **O que este objeto oferece.** Constantes de CSS para compatibilidade e `get_styles_resolvidos(theme)` para produzir os estilos HTML a partir de um `ResolvedTheme` notebook já validado.

# MAGIC
# MAGIC Antes de executar, consulte o [guia do objeto](README.md): conceito, requisitos, efeitos e limites.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | exemplo usa sessão Spark para localizar usuário; renderização conforme notebook |
# MAGIC | Bibliotecas | biblioteca padrão Python e módulos locais do Hub; confira a preparação da sessão |
# MAGIC | Dados | nenhum — este objeto não recebe dados |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | confira compatibilidade e renderização no destino; a demonstração não homologa todo runtime |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.constants.styles import FONT_FAMILY, STYLE_BADGE_FAIL, STYLE_BADGE_OK, STYLE_BADGE_WARN, STYLE_DIVIDER_HEAVY, STYLE_DIVIDER_LIGHT, STYLE_KPI_CARD, STYLE_SECTION_HEADER, get_styles_resolvidos
from hub_snippets.visual.tema import load_reference_theme

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. O efeito dos estilos legados, renderizado

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
# MAGIC Executado no laboratório, o resultado legado é:
# MAGIC
# MAGIC ```text
# MAGIC FONT_FAMILY: Segoe UI, Roboto, sans-serif
# MAGIC
# MAGIC STYLE_SECTION_HEADER:
# MAGIC   background:#F8F9FA; border-left:4px solid #005CA9; padding:12px 16px;
# MAGIC   margin:8px 0 12px 0; border-radius:4px; font-family:Segoe UI, Roboto, sans-serif;
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** As constantes continuam strings de CSS e preservam o caminho existente. Isso não as transforma em estado global nem reestiliza HTML já exibido.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Tema explícito — tema explícito, sem estado global

# COMMAND ----------

tema = load_reference_theme("notebook")
styles_resolvidos = get_styles_resolvidos(tema)

assert styles_resolvidos["card.kpi"] == STYLE_KPI_CARD
assert styles_resolvidos["section.container"] == STYLE_SECTION_HEADER

displayHTML(f"""
<div style="{styles_resolvidos['section.container']}">
  <h3 style="{styles_resolvidos['section.title']}">Tema notebook resolvido</h3>
  <p style="{styles_resolvidos['section.description']}">A referência legada reproduz o visual existente; outra configuração validada pode mudar apenas a apresentação.</p>
</div>
""")

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que está centralizado e o que continua separado
# MAGIC
# MAGIC `get_styles_resolvidos` revalida um `ResolvedTheme` e materializa um dicionário de CSS para cabeçalho de seção, KPI card, divisores, badges, índice e cabeçalho/destaque de tabela. Não existe campo de CSS livre no tema.
# MAGIC
# MAGIC `visual/badge`, `visual/divider`, `visual/kpi_card`, `visual/section_header`, `visual/index_generator` e `display/dataframe_styled` consomem essa materialização nas funções `_resolvido`. As funções antigas continuam usando as constantes legadas e não mudam de aparência por efeito implícito.
# MAGIC
# MAGIC A configuração de referência reproduz os estilos legados dos componentes HTML. `dark` e `high_contrast` podem ser materializados quando a configuração completa é válida, mas isso não constitui certificação de acessibilidade ou homologação visual no Databricks.
# MAGIC
# MAGIC O contraste do badge de atenção da referência histórica continua uma limitação conhecida; confira a medição e a referência no [README](README.md).

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem conferir o destino.** A exibição no notebook não comprova suporte de outro renderizador; teste o documento final antes de distribuí-lo.
# MAGIC - **Como folha de estilo global.** A função devolve um dicionário para uso explícito; não injeta CSS na sessão.
# MAGIC - **Passando dicionário cru.** As variantes resolvidas aceitam somente `ResolvedTheme` íntegro produzido pelo núcleo de temas.
# MAGIC - **Editando a string na chamada.** Para experimento isolado, use uma cópia local identificada. Mudança compartilhada exige revisão própria, não edição silenciosa do padrão.
