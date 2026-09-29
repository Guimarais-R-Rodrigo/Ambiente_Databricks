# Databricks notebook source
# MAGIC %md
# MAGIC # Exemplo sintético — micromodelo com objetivo conhecido
# MAGIC
# MAGIC Este notebook contém um briefing preenchido para copiar no chat com
# MAGIC `@hub-ml-micromodelos`. Não acessa catálogo, cria YAML, executa a skill,
# MAGIC registra resposta real ou demonstra runtime Genie Code.

# COMMAND ----------

briefing = """Use @hub-ml-micromodelos no modo OBJETIVO_CONHECIDO.
Decisão a apoiar: priorizar revisão humana de contatos de campanha sintética.
Característica preliminar: interesse recente em canal digital.
Entidade e grão: cliente sintético por mês; chave lógica id_cliente_sintetico.
População e horizonte: clientes sintéticos elegíveis; 30 dias.
Fonte: CATALOGO_PRODUTO, objeto sintético ainda não observado.
Dono/uso: analista de laboratório; sem decisão automatizada.
Ambiente/restrição: E0, fixture sintética, metadata somente.
Pedido original: ticket-sintetico-001.
Crie rascunho progressivo MM01, preserve INDETERMINADO e registre lacunas.
Não afirme execução nem aprovação não observadas."""
print(briefing)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Registro de resposta real (preencher após teste conversacional)
# MAGIC
# MAGIC - Ambiente e data: `NOT_RUN`
# MAGIC - Skill/rota efetivamente observada: `NOT_RUN`
# MAGIC - Resposta sanitizada ou referência: `NOT_RUN`
# MAGIC - YAML validado por comando: `NOT_RUN`
# MAGIC - Falhas, incertezas e próximo passo: `PENDENTE`
# MAGIC
# MAGIC ```text
# MAGIC NÃO EXECUTADO — nenhuma resposta do Genie Code foi capturada para este
# MAGIC briefing. Preencher aqui após teste conversacional real e sanitizado.
# MAGIC ```
