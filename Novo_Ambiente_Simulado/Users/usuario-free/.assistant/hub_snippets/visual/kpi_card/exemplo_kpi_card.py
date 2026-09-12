# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.kpi_card` — os números que decidem, antes dos que explicam
# MAGIC
# MAGIC **O problema.** O número que responde a pergunta do gestor costuma estar na célula 40, depois de trinta gráficos. Quem tem cinco minutos não chega lá, e decide com a impressão que teve das duas primeiras telas.
# MAGIC
# MAGIC **O que este objeto oferece.** Um bloco de cartões com as métricas que importam — em HTML para o notebook, ou em Markdown para colar em outro lugar.

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
# MAGIC | Dados | textos e valores definidos nas células; nenhuma tabela externa |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.visual.kpi_card import kpi_card_html, kpi_card_markdown

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. A mesma informação em dois formatos

# COMMAND ----------

metricas = {
    "Linhas": "3.375.674",
    "Cobertura": "92,8%",
    "Período": "2025-01 a 2026-08",
    "Alerta": "2 colunas com nulo acima de 30%",
}

displayHTML(kpi_card_html(metricas))

# COMMAND ----------

print(kpi_card_markdown(metricas))

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC > **3.375.674** Linhas | **92,8%** Cobertura | **2025-01 a 2026-08** Período | **2 colunas com nulo acima de 30%** Alerta
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Há duas representações textuais para destinos distintos.
# MAGIC Markdown precisa de um renderizador compatível para ganhar sua formatação;
# MAGIC HTML também pode ser consumido fora do notebook, conforme o destino.
# MAGIC Copiar para um e-mail não garante nenhuma das duas apresentações.
# MAGIC
# MAGIC Repare que a função **não formata número**: quem passou "3.375.674" e
# MAGIC "92,8%" já formatou, com `constants.format_br`. A separação é deliberada —
# MAGIC o cartão decide layout, não escala nem casas decimais.
# MAGIC
# MAGIC E repare no quarto cartão. "2 colunas com nulo acima de 30%" não é uma
# MAGIC métrica, é uma **ressalva** — e é o cartão mais importante dos quatro. Um
# MAGIC bloco de KPI só com números bons é propaganda; o que o torna útil é caber
# MAGIC nele o que está errado.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Com muitos indicadores sem prioridade.** A função não limita a quantidade; selecione os principais e compare uma tabela quando ela organizar melhor os detalhes.
# MAGIC - **Com número sem contexto.** "AUC 0,78" não decide nada; "AUC 0,78, era 0,81 no trimestre" decide.
# MAGIC - **Como substituto da explicação.** Use-o próximo à decisão apoiada e mantenha texto sobre período, população e limitações.
