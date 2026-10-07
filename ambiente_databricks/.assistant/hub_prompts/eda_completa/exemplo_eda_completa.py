# Databricks notebook source
# MAGIC %md
# MAGIC # `eda_completa` — EDA que sustenta decisão de modelagem
# MAGIC
# MAGIC 📘 Guia local: [`README.md`](./README.md)
# MAGIC
# MAGIC **O arquivo do prompt não executa por si só.** Aqui somente o preparo
# MAGIC executa código. O briefing é texto para a interação autorizada, e a
# MAGIC resposta real deve ser registrada com evidência; continua pendente neste exemplo.
# MAGIC
# MAGIC | Parte | O que é | Roda? |
# MAGIC |---|---|---|
# MAGIC | 1 | preparo: cria a base sintética a que o prompt se refere | **sim** |
# MAGIC | 2 | o prompt preenchido, pronto para copiar | não; é texto |
# MAGIC | 3 | a resposta real do Genie Code, colada de um chat | **exige uma pessoa** |

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | sessão Spark compatível com as fixtures e permissões de escrita no destino confirmado |
# MAGIC | Bibliotecas | PySpark e pacote Hub importável; dependências de análise dependem da rota escolhida |
# MAGIC | Dados | sintéticos, de `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | **sim, overwrite** — sobrescreve `workspace.default.hub_exemplo_clientes` |
# MAGIC | Diferença Free × trabalho | fonte real exige autorização, revisão de dados sensíveis e contrato próprio; este preparo é sintético |

# COMMAND ----------
# MAGIC %md
# MAGIC **Antes de executar a Parte 1 ou Run all:** o preparo sobrescreve `workspace.default.hub_exemplo_clientes`
# MAGIC com `mode("overwrite")`. Confira destino e autorização; pode substituir dados
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. O preparo não executa a EDA.
# MAGIC
# MAGIC O nome também é usado por EDA, Baseline, Explainability, Novo Projeto, Pipeline e Stat Check.
# MAGIC
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

base = fixtures.base_tabular(n=4000, seed=42, pct_nulos_renda=0.06,
                             prevalencia_alvo=0.18)
base.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes")

print(f"linhas: {base.count()}")
base.printSchema()
base.show(5, truncate=False)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Cinco colunas, 4.000 linhas, `renda` com cerca de 6% de nulos e `alvo` em torno de 18%. Os nulos e o desbalanceamento são deliberados: um prompt que produz resposta boa numa base perfeita não diz nada sobre a base que você tem.

# COMMAND ----------
# MAGIC %md
# MAGIC **Rota da análise:** ao selecionar a EDA profissional, siga `run_enforced`,
# MAGIC Receipt, handoff e `finalize_or_raise`; conclusão exige Postflight PASS e
# MAGIC `completion.authorized=true`. `PENDING_POSTFLIGHT` ainda não é conclusão.
# MAGIC Helpers/SQL manuais não são bypass. Veja a [skill](../../skills/hub-ml-eda-profissional/SKILL.md).
# MAGIC
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`eda_completa.md`](./eda_completa.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC A diferença para o `eda_rapida` está em duas linhas: aqui o **target está definido** e o **entregável é declarado**. As duas mudam o que o assistente produz, não só o tamanho da resposta.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-eda-profissional para construir uma EDA completa, auditável e adequada
# MAGIC ao volume, sem alterar os dados de origem.
# MAGIC
# MAGIC BRIEFING
# MAGIC - Recurso principal: workspace.default.hub_exemplo_clientes
# MAGIC - Contexto de negócio/decisão: campanha de relacionamento em CRM bancário; queremos priorizar quem abordar no próximo ciclo
# MAGIC - Unidade de análise: uma linha por cliente e data de referência
# MAGIC - Chave primária/candidata: `id_cliente` + `dt_referencia`, a confirmar
# MAGIC - Coluna temporal: dt_referencia
# MAGIC - Target e evento positivo: `alvo` = 1 quando o cliente respondeu à campanha em até 30 dias
# MAGIC - Período e filtros: 2026-01 a 2026-06, sem filtro
# MAGIC - Volume estimado: 4.000 linhas
# MAGIC - Foco prioritário: qualidade, granularidade e relação de cada variável com o target
# MAGIC - Restrições de compute, prazo e bibliotecas: serverless, sem `cache()`; nada de `toPandas()` sem limite
# MAGIC - Entregável: notebook, com células markdown antes de cada bloco de código
# MAGIC
# MAGIC PRÉ-REQUISITOS
# MAGIC 1. Verifique o recurso anexado, schema, comentários do Unity Catalog e permissões.
# MAGIC 2. Liste ambiguidades que mudariam a análise; faça perguntas somente sobre bloqueios.
# MAGIC 3. Declare plano, número esperado de varreduras e estratégia de amostragem.
# MAGIC
# MAGIC ESCOPO MÍNIMO
# MAGIC 1. Estrutura: schema, tipos, volume, duplicidade, chaves e granularidade observada.
# MAGIC 2. Qualidade: nulos, valores inválidos, cardinalidade, extremos, consistência e
# MAGIC    cobertura temporal. Não confunda ausência permitida com erro.
# MAGIC 3. Univariada: estatísticas robustas e distribuições adequadas ao tipo de variável.
# MAGIC 4. Bivariada/multivariada: relações relevantes, segmentos, tempo e target, quando
# MAGIC    aplicável; correlação não implica causalidade.
# MAGIC 5. Risco de modelagem: leakage temporal/alvo, viés de seleção, drift, desbalanceamento
# MAGIC    e representatividade, se houver finalidade de ML.
# MAGIC 6. Visualização: Plotly quando útil; agregue/amostre antes de coletar ao driver.
# MAGIC
# MAGIC SEGURANÇA E CUSTO
# MAGIC - Priorize PySpark/Spark SQL. Não faça `toPandas()` ou `collect()` irrestrito.
# MAGIC - Não revele PII, segredos ou valores individuais; use agregação/mascaramento.
# MAGIC - Não escreva tabelas, não sobrescreva notebooks e não instale dependências sem
# MAGIC   apresentar o impacto e obter autorização explícita.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Resumo executivo orientado à decisão.
# MAGIC - Inventário de qualidade com evidência, severidade, impacto e recomendação.
# MAGIC - Notebook/código organizado por células idempotentes, com parâmetros no início.
# MAGIC - Tabelas e gráficos com títulos, unidade, período, base e observações.
# MAGIC - Conclusões ligadas às evidências, limitações e backlog priorizado.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Registre recursos, filtros, período, contagens e amostra efetivamente usados.
# MAGIC - Valide que joins não multiplicaram linhas e que denominadores são explícitos.
# MAGIC - Separe achados observados, hipóteses e recomendações.
# MAGIC - Liste o que não foi possível verificar e por quê.
# MAGIC ```

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 3 — a resposta real
# MAGIC
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO — depende de uma pessoa
# MAGIC
# MAGIC O que falta   : colar aqui a resposta que o Genie Code deu ao prompt
# MAGIC                 da Parte 2, num chat novo, com a base da Parte 1 criada.
# MAGIC Evidência    : nenhuma resposta desta interação foi registrada e revisada.
# MAGIC                Não invente conteúdo para completar o exemplo. O preparo
# MAGIC                não prova execução nem conclusão canônica da skill.
# MAGIC Quem preenche : quem tiver acesso ao Genie Code do workspace.
# MAGIC ```
# MAGIC
# MAGIC **Como preencher**, quando for a hora:
# MAGIC
# MAGIC 1. Se o preparo for necessário, confirme destino e autorização: ele sobrescreve `workspace.default.hub_exemplo_clientes`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre contexto e skill selecionados com evidência disponível.
# MAGIC    Relato do assistente não comprova sozinho leitura, importação, chamada
# MAGIC    ou conclusão; confira os artefatos exigidos pela rota da skill.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-eda-profissional`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Sem target definido.** Metade do valor da EDA completa é a relação com o alvo; sem ele, use `eda_rapida`.
# MAGIC - **Em base que ainda vai mudar.** EDA sobre esquema instável envelhece antes de ser lida.
# MAGIC - **Como entregável final.** Ela informa a decisão de modelagem; quem decide é você.
