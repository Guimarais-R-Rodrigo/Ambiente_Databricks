# Databricks notebook source
# MAGIC %md
# MAGIC # `constants.styles` — CSS compartilhado para `displayHTML`
# MAGIC
# MAGIC **O problema.** Cada bloco de HTML num notebook carrega seu próprio `style="..."` inline, e a primeira mudança de identidade visual exige editar dezenas de notebooks. Pior: as versões divergem, e o relatório fica com três tons de cinza que deveriam ser um.
# MAGIC
# MAGIC **O que este objeto oferece.** Nove constantes de CSS, prontas para interpolar em `displayHTML`.

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
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |

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
# MAGIC ## O que está centralizado e o que ainda está separado
# MAGIC
# MAGIC A implementação atual importa `constants.colors` e usa suas constantes
# MAGIC em parte do CSS. Essas strings são montadas ao importar o módulo: não
# MAGIC constituem uma ligação dinâmica que refaz todos os estilos da sessão.
# MAGIC
# MAGIC Os componentes `visual/badge`, `visual/divider` e `visual/kpi_card`
# MAGIC mantêm CSS próprio e não consomem `constants.styles` nesta base.
# MAGIC Alterar `STYLE_KPI_CARD` não altera automaticamente esses componentes.
# MAGIC O uso mostrado aqui é a composição explícita da constante pelo notebook.
# MAGIC
# MAGIC As cores de estado e alguns cinzas continuam declarados localmente.
# MAGIC Não presumir igualdade byte a byte entre strings de CSS: espaços e ordem
# MAGIC de propriedades também fazem parte do retorno. Esta sprint não unifica
# MAGIC CSS nem altera a identidade visual; o README descreve o alcance real.
# MAGIC
# MAGIC O contraste de `STYLE_BADGE_WARN` precisa de revisão antes de uso como
# MAGIC texto pequeno: confira a medição e a referência no [README](README.md).

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem conferir o destino.** A exibição no notebook não comprova suporte de outro renderizador; teste o documento final antes de distribuí-lo.
# MAGIC - **Como folha de estilo de aplicação.** São strings para interpolar em HTML de notebook, não um sistema de design.
# MAGIC - **Editando a string na chamada.** Para experimento isolado, use uma cópia local identificada. Mudança compartilhada exige revisão própria, não edição silenciosa do padrão.
