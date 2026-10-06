# Databricks notebook source
# MAGIC %md
# MAGIC [Conceito, requisitos e limites deste prompt](README.md).
# MAGIC
# MAGIC # Exemplo sintético — objetivo conhecido
# MAGIC
# MAGIC Três partes: preparo textual executável, prompt exato e resposta real. O preparo não consulta catálogo nem cria registros; a resposta veio de chat manual no Free.
# MAGIC
# MAGIC | Item | Condição |
# MAGIC |---|---|
# MAGIC | Dados | Somente fixture textual sintética, sem linhas. |
# MAGIC | Leitura/escrita | Nenhuma tabela; o preparo imprime um dicionário local. |
# MAGIC | Genie Code | A parte 3 veio de chat novo no Free com skill carregada. |
# MAGIC | Runtime | O preparo abaixo foi executado localmente em E0; não demonstra runtime E1. |
# MAGIC
# MAGIC **Quando não usar:** para validar YAML MM01, consultar catálogo ou medir
# MAGIC comportamento em registros. Essas etapas exigem contratos e autorizações próprios.

# COMMAND ----------

# Parte 1 — preparo executável da fixture textual; sem catálogo ou registros.
fixture_textual = {
    "decisao": "priorizar revisão humana de contatos fictícios",
    "entidade": "entidade fictícia por mês",
    "populacao": "seis entidades sintéticas, sem linhas fornecidas",
    "fonte_logica": "CATALOGO_PRODUTO, sem binding físico autorizado",
    "horizonte": "30 dias PROPOSTO",
}
print(fixture_textual)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Saída real do preparo local E0
# MAGIC
# MAGIC ```text
# MAGIC {'decisao': 'priorizar revisão humana de contatos fictícios', 'entidade': 'entidade fictícia por mês', 'populacao': 'seis entidades sintéticas, sem linhas fornecidas', 'fonte_logica': 'CATALOGO_PRODUTO, sem binding físico autorizado', 'horizonte': '30 dias PROPOSTO'}
# MAGIC ```
# MAGIC
# MAGIC Esta saída é apenas a impressão da fixture textual; não é resposta do
# MAGIC Genie Code nem evidência de catálogo ou runtime E1.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 2 — prompt preenchido
# MAGIC
# MAGIC Abra um chat novo no Databricks Free, selecione `@hub-ml-micromodelos` no menu e cole este texto:
# MAGIC
# MAGIC ```text
# MAGIC Use @hub-ml-micromodelos no modo OBJETIVO_CONHECIDO.
# MAGIC
# MAGIC BRIEFING
# MAGIC - Decisão a apoiar: priorizar revisão humana de contatos fictícios.
# MAGIC - Característica e definição preliminar: interesse recente em canal digital; definição operacional PENDENTE.
# MAGIC - Entidade, grão, chave e data de referência: entidade fictícia por mês; chave lógica e data de referência PENDENTE.
# MAGIC - População e horizonte: seis entidades sintéticas; 30 dias PROPOSTO, não aprovado.
# MAGIC - Fontes conhecidas, referência lógica e estado de observação: CATALOGO_PRODUTO é referência lógica; nenhum objeto ou binding físico foi autorizado ou observado neste chat.
# MAGIC - Dono, consumidor, uso pretendido e usos proibidos: dono PENDENTE; consumidor proposto é revisão humana; proibidas decisão automática, publicação e inferência sobre pessoas reais.
# MAGIC - Ambiente, permissões, privacidade e orçamento: E1 Databricks Free, fixture textual sintética fornecida aqui; não consulte catálogo nem registros e não execute código; somente resposta textual.
# MAGIC - Referência do pedido original: ticket-sintetico-mm04-p1.
# MAGIC
# MAGIC TAREFA
# MAGIC 1. Confirme o ambiente e a rota efetivamente disponível da skill e policy atual.
# MAGIC 2. Separe fato observado, inferência, proposta, aprovação e medição. Não invente
# MAGIC    fonte, target, valor, limiar, dono, permissão ou resultado de execução.
# MAGIC 3. Se houver binding e autorização, comece pela metadata do catálogo
# MAGIC    configurado: faça shortlist antes de pedir colunas/tags/constraints. Se o
# MAGIC    briefing trouxer só fixture textual, não consulte catálogo; marque a
# MAGIC    metadata como `FORNECIDA`. Não consulte linhas, contagens ou valores neste modo.
# MAGIC 4. Somente se o template/schema MM01 1.0.0 estiver realmente acessível,
# MAGIC    atualize progressivamente um único micromodelo.yaml, preservando pendências
# MAGIC    e estados válidos. Valide pela rota canônica disponível e reporte o resultado
# MAGIC    real. Sem template/schema, não invente YAML: entregue checklist textual de
# MAGIC    fatos e lacunas com `YAML_NAO_CRIADO` e `MM01_NAO_VALIDADO`.
# MAGIC 5. Explicite hipóteses favoráveis, contra-hipóteses, semântica de
# MAGIC    TRUE/FALSE/INDETERMINADO e o que poderia invalidar a ideia. Não trate falta
# MAGIC    de evidência como FALSE. Sem evidência observada e rubrica explícita, marque
# MAGIC    `SCORE_INDETERMINADO`; não trate score 0-100 como probabilidade sem calibração.
# MAGIC 6. Entregue plano de estudo e handoff às skills especialistas apropriadas,
# MAGIC    cada qual sob sua policy atual. Não publique nem avance fase por suposição.
# MAGIC
# MAGIC SAÍDA
# MAGIC - Resumo da decisão, escopo observado e lacunas.
# MAGIC - YAML MM01 quando houver template/schema acessível, com resultado real da
# MAGIC   validação; caso contrário, checklist textual e `YAML_NAO_CRIADO`.
# MAGIC - Proveniência dos campos relevantes, incertezas e decisões pendentes.
# MAGIC - Próxima etapa, responsável sugerido e evidência E0/E1/E2 realmente obtida.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parte 3 — resposta real e limites
# MAGIC
# MAGIC Conversa E1 de 29/09/2026, caso P1, com fixture textual fornecida.
# MAGIC
# MAGIC - A resposta registrou `YAML_NAO_CRIADO`, `MM01_NAO_VALIDADO` e `SCORE_INDETERMINADO`.
# MAGIC - Não alegou consulta a registros ou publicação.
# MAGIC - Ressalva: chamou alguns campos do briefing de `OBSERVADO`; a proveniência correta é `FORNECIDA`.
# MAGIC - A policy integrada não foi verificada independentemente nessa resposta; ler um contrato estático não substitui consultar a policy vigente.
# MAGIC
# MAGIC Essa conversa não demonstra execução de runtime E1, validação MM01,
# MAGIC aceite humano ou homologação corporativa. Use os contratos locais para a próxima etapa.
