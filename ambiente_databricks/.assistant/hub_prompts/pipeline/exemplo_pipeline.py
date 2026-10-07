# Databricks notebook source
# MAGIC %md
# MAGIC # `pipeline` — do notebook que funciona ao pipeline que roda sozinho
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
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. O preparo não cria pipeline nem prova MERGE/replay.
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
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`pipeline.md`](./pipeline.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `SCHEMA_EVOLUCAO` e `MODO` são os campos que separam um pipeline que sobrevive de um que quebra na primeira coluna nova. Quase nenhum pedido informal os menciona.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-pipeline-builder para desenhar um pipeline Databricks atual, testável e
# MAGIC operável. Não crie, implante nem execute recursos até eu autorizar explicitamente.
# MAGIC
# MAGIC BRIEFING
# MAGIC - Objetivo e consumidores: disponibilizar a base de clientes tratada para o time de CRM e para o treino do modelo de propensão
# MAGIC - Fontes/formato/modo de chegada: workspace.default.hub_exemplo_clientes
# MAGIC - Destinos e granularidade: camada silver e uma tabela gold agregada por UF e mês
# MAGIC - Batch/streaming/CDC: incremental por `dt_referencia`
# MAGIC - Chaves e ordenação/sequência: `id_cliente` + `dt_referencia`; sem dependência de ordem entre linhas
# MAGIC - Schema e evolução esperada: aceitar coluna nova; **falhar** em mudança de tipo de coluna existente
# MAGIC - Regras de qualidade: `id_cliente` não nulo e único na chave; `renda` nula tolerada até 10%; `alvo` só 0 ou 1
# MAGIC - SLA/SLO, volume e frequência: execução diária às 6h; até 15 minutos; volume esperado de 4 mil linhas por dia
# MAGIC - Ambientes/catálogos: três targets, com catálogo separado por ambiente
# MAGIC - Segurança/PII/permissões: Lakeflow Spark Declarative Pipelines; expectations declaradas, não checagem avulsa em notebook
# MAGIC - Modo de entrega: arquitetura e código; não faça deploy
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Confirme fontes, contratos, owners, checkpoint/estado e semântica de reprocessamento.
# MAGIC 2. Proponha arquitetura proporcional ao caso. Use Lakeflow Spark Declarative
# MAGIC    Pipelines quando adequado e explique a escolha; não force streaming sem necessidade.
# MAGIC 3. Defina idempotência, deduplicação, late data, evolução de schema, quarantine,
# MAGIC    qualidade e recuperação. Expectations devem ter ação explícita e justificativa.
# MAGIC 4. Proponha Declarative Automation Bundles para versionar recursos e targets de
# MAGIC    ambiente quando houver ciclo de deploy. Valide antes de implantar.
# MAGIC 5. Recomende serverless para novos pipelines quando suportado pelo caso, declarando
# MAGIC    requisitos/limitações; não invente disponibilidade regional ou permissões.
# MAGIC 6. Inclua observabilidade pelo event log, métricas, alertas e runbook.
# MAGIC 7. Não grave no destino, não faça deploy, não altere grants e não inicie pipeline
# MAGIC    sem mostrar diff/plano, ambiente alvo e impacto e obter autorização.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Arquitetura e fluxo bronze/silver/gold somente onde agregar valor.
# MAGIC - Contratos de input/output, chaves, watermark/CDC e qualidade.
# MAGIC - Árvore do projeto e recursos do bundle, se aplicável.
# MAGIC - Código/configuração propostos e testes.
# MAGIC - Plano de deploy dev→stage→prod, rollback, observabilidade e custo.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Teste duplicatas, atraso, reprocessamento, schema novo e falha parcial.
# MAGIC - Confirme que writes são idempotentes e destinos/ambientes são parametrizados.
# MAGIC - Separe recurso documentado da Databricks de convenção personalizada do projeto.
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
# MAGIC Skill esperada aqui: `hub-ml-pipeline-builder`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Antes de o notebook estar correto.** Pipeline industrializa o que existe; automatizar erro só o repete mais rápido.
# MAGIC - **Sem declarar o que fazer com esquema novo.** É a causa mais comum de pipeline que quebra de madrugada.
# MAGIC - **Com um ambiente só.** Sem separação dev/prod, o primeiro teste vai para produção.
