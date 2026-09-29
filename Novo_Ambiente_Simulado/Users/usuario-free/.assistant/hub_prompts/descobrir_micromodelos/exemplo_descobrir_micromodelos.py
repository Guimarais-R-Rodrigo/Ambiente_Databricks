# Databricks notebook source
# MAGIC %md
# MAGIC # Exemplo sintético — descobrir oportunidades
# MAGIC
# MAGIC Este notebook prepara um briefing. Não consulta metadata, não chama
# MAGIC a skill, não cria shortlist real e não prova roteamento no Genie Code.

# COMMAND ----------

briefing = """Use @hub-ml-micromodelos no modo DESCOBRIR_OPORTUNIDADES.
Área/decisão: priorizar revisão humana de campanhas sintéticas.
Catálogo lógico: CATALOGO_PRODUTO; binding físico sintético a confirmar.
Schemas: somente os autorizados para a fixture E0.
Entidade/população: clientes sintéticos elegíveis.
Restrições: metadata somente, até cinco candidatas, nenhuma leitura de linhas.
Critérios qualitativos: utilidade, explicabilidade e risco temporal.
Entregue ESCOPO_OBSERVADO, shortlist deduplicada, incertezas e próximo passo.
Não invente contagens, permissão de SELECT ou aprovação de negócio."""
print(briefing)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Registro de resposta real (preencher após teste conversacional)
# MAGIC
# MAGIC - Ambiente e data: `NOT_RUN`
# MAGIC - Skill/rota efetivamente observada: `NOT_RUN`
# MAGIC - Metadata e escopo observados: `NOT_RUN`
# MAGIC - Resposta sanitizada ou referência: `NOT_RUN`
# MAGIC - Deduplicação, incertezas e próximo passo: `PENDENTE`
# MAGIC
# MAGIC ```text
# MAGIC NÃO EXECUTADO — nenhuma resposta do Genie Code foi capturada para este
# MAGIC briefing. Preencher aqui após teste conversacional real e sanitizado.
# MAGIC ```
