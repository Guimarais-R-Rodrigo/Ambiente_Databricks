# Databricks notebook source
# MAGIC %md
# MAGIC # `constants.emojis` — o índice de uma EDA, e o vocabulário de leitura
# MAGIC
# MAGIC **O problema.** Duas pessoas fazendo EDA no mesmo time produzem dois roteiros diferentes, e quem lê precisa reaprender a estrutura a cada notebook. E emoji escolhido no impulso vira ruído: três símbolos diferentes para 'atenção' na mesma página.
# MAGIC
# MAGIC **O que este objeto oferece.** Dois mapas: as nove etapas canônicas de uma EDA, com emoji e descrição, e um vocabulário semântico fechado.

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

from hub_snippets.constants.emojis import SECOES_EDA, SEMANTICA

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. As nove etapas

# COMMAND ----------

for numero, dados in SECOES_EDA.items():
    print(f"  {numero}  {dados['emoji']}  {dados['titulo']:26s} {dados['descricao']}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC   0  🎯  Contexto da Análise        Define objetivo, escopo e premissas da exploração.
# MAGIC   1  📐  Inventário Inicial         Reconhece estrutura, volume, tipos e perfil geral dos dados.
# MAGIC   2  🔑  Granularidade e Chaves     Identifica o que representa uma linha e valida unicidade.
# MAGIC   3  ✅  Qualidade de Dados         Diagnostica nulos, duplicatas, outliers e inconsistências.
# MAGIC   4  📊  Análise Univariada         Distribuição individual de cada variável numérica, categórica e temporal.
# MAGIC   5  🔗  Análise Bivariada          Correlações, relações entre variáveis e com o target.
# MAGIC   6  🎨  Visualizações              Gráficos interativos do relatório final com Plotly.
# MAGIC   7  🛠️  Recomendações Técnicas     Tratamentos, features candidatas e riscos para modelagem.
# MAGIC   8  📈  Relatório Executivo        Síntese final com achados, impactos e próximos passos.
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A ordem é o conteúdo. **Granularidade (2) vem antes de qualidade
# MAGIC (3)**, e isso não é detalhe: contar nulos numa tabela cuja linha você ainda
# MAGIC não sabe o que representa produz um número sem significado. Se a base tem
# MAGIC uma linha por contrato-mês e você achava que era por contrato, "12% de
# MAGIC nulos" não quer dizer nada.
# MAGIC
# MAGIC Da mesma forma, **bivariada (5) vem depois de univariada (4)**: correlação
# MAGIC entre duas variáveis com distribuição que você não olhou é um número que
# MAGIC pode estar sendo produzido por dois outliers.
# MAGIC
# MAGIC As nove são roteiro, não formulário — a etapa que não se aplica se pula.
# MAGIC O que o mapa impede é a **ordem** errada, que é o erro caro.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O vocabulário semântico

# COMMAND ----------

for chave, emoji in SEMANTICA.items():
    print(f"  {emoji}  {chave}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC   📊  resultado
# MAGIC   🔍  interpretacao
# MAGIC   💼  negocio
# MAGIC   ➡️  proximo_passo
# MAGIC   📌  insight
# MAGIC   ✅  ok
# MAGIC   ❌  falha
# MAGIC   ⚠️  atencao
# MAGIC   🟢  status_positivo
# MAGIC   🟡  status_medio
# MAGIC   🔴  status_critico
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Onze símbolos, e a lista é fechada de propósito. O ganho de um
# MAGIC vocabulário está em ser pequeno o suficiente para ser aprendido: quem lê o
# MAGIC segundo relatório já sabe que 🔍 abre interpretação e ➡️ abre próximo passo,
# MAGIC e passa a navegar pelo símbolo.
# MAGIC
# MAGIC Repare na separação entre `ok`/`falha`/`atencao` e o trio de status
# MAGIC colorido. Os primeiros são **verdito binário sobre uma checagem**; os
# MAGIC segundos são **grau numa escala**. Misturá-los — usar ✅ para "está bom" e
# MAGIC 🟢 para "passou" no mesmo documento — desfaz a distinção.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como obrigação.** As nove etapas são um roteiro, não um formulário. Análise que não precisa de sobrevivência não abre a seção.
# MAGIC - **Inventando símbolo fora do mapa.** O valor do vocabulário é ser fechado; um emoji novo por notebook desfaz o ganho.
# MAGIC - **Em documento que será impresso ou exportado para PDF.** Emoji renderiza de forma inconsistente fora do navegador.
