# Databricks notebook source
# MAGIC %md
# MAGIC # `feature_engineering` — especificar features sem vazar o futuro
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
# MAGIC | Escrita | **sim, overwrite** — sobrescreve `workspace.default.hub_exemplo_fatos` e `workspace.default.hub_exemplo_features` |
# MAGIC | Diferença Free × trabalho | fonte real exige autorização, revisão de dados sensíveis e contrato próprio; este preparo é sintético |

# COMMAND ----------
# MAGIC %md
# MAGIC **Antes de executar a Parte 1 ou Run all:** o preparo sobrescreve `workspace.default.hub_exemplo_fatos` e `workspace.default.hub_exemplo_features`
# MAGIC com `mode("overwrite")`. Confira destino e autorização; pode substituir dados
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. Os mesmos destinos são usados pelo exemplo de Cross-EDA; não há materialização governada de features neste preparo.
# MAGIC
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

fatos, features = fixtures.fatos_e_features(n_decisoes=1500, seed=42,
                                            atraso_real_dias=3,
                                            pct_feature_futura=0.2)
fatos.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_fatos")
features.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_features")

print(f"decisões: {fatos.count()} | registros de feature: {features.count()}")
print("atraso de publicação plantado: 3 dias | features com data futura: ~20%")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** As duas tabelas são as mesmas do `cross_eda`, e o vazamento plantado é o mesmo. A diferença é o que se pede: lá era diagnóstico, aqui é **especificação** — o que construir, com que janela, e como provar que não vaza.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`feature_engineering.md`](./feature_engineering.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `JANELA_OBSERVACAO` e `PONTO_NO_TEMPO` fazem par: a janela diz quanto passado usar, e o ponto no tempo diz até quando. Faltando uma das duas, a feature parece bem definida e não é.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-feature-engineering para desenhar e, se autorizado, implementar features
# MAGIC reprodutíveis, sem leakage e compatíveis com o volume.
# MAGIC
# MAGIC BRIEFING
# MAGIC - Entidade/granularidade: cliente; uma linha por decisão
# MAGIC - Chave da entidade: id_cliente
# MAGIC - Target/evento positivo: `alvo` = 1 quando houve resposta em até 30 dias de `dt_decisao`
# MAGIC - Tempo de observação: 90 dias anteriores a `dt_decisao`
# MAGIC - Instante de predição: **obrigatório**, com atraso de publicação de 3 dias — nenhuma feature pode usar dado que ainda não estava disponível na decisão
# MAGIC - Horizonte do target: 30 dias
# MAGIC - Fontes anexadas e chaves: workspace.default.hub_exemplo_features, por `id_cliente`, as-of em `dt_referencia`
# MAGIC - Frequência de scoring: a base de decisão é diária; as features são atualizadas semanalmente
# MAGIC - Features existentes: nenhuma
# MAGIC - Restrições/PII/compute: serverless; use `hub_snippets.spark.pit_join` e `hub_snippets.spark.join_diagnostics`
# MAGIC - Modo: plano e código; não execute
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Confirme granularidade, disponibilidade temporal e momento real de cada fonte.
# MAGIC 2. Crie uma especificação com nome, definição, fonte, janela, cutoff, fórmula, tipo,
# MAGIC    tratamento de nulos, owner e testes. Não use informação posterior à predição.
# MAGIC 3. Proponha famílias comportamentais, temporais, RFV, estabilidade e contexto somente
# MAGIC    quando justificadas pelo caso; evite proxies sensíveis sem avaliação apropriada.
# MAGIC 4. Valide cardinalidade e multiplicação de linhas antes/depois de cada join.
# MAGIC 5. Prefira PySpark/Spark SQL, agregações incrementais e funções determinísticas. Evite
# MAGIC    Python UDF quando houver função nativa e não use `toPandas()` irrestrito.
# MAGIC 6. Quando houver reuso entre treino e inferência, proponha publicação e lineage em
# MAGIC    Feature Engineering in Unity Catalog, sem assumir que já está configurado.
# MAGIC 7. No modo PLANO, não gere escrita. No modo CÓDIGO, gere sem executar. Só implemente
# MAGIC    ou publique após autorização explícita e ambiente alvo confirmado.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Diagrama textual do ponto-no-tempo e fontes.
# MAGIC - Feature specification priorizada com risco de leakage e custo.
# MAGIC - Código parametrizado/idempotente, se solicitado.
# MAGIC - Testes: unicidade, cobertura, estabilidade, janela, cutoff e parity treino/inferência.
# MAGIC - Evidências, pressupostos, features rejeitadas e próximos passos.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Demonstre que nenhuma feature vê o futuro do target.
# MAGIC - Confirme contagens e granularidade após joins.
# MAGIC - Separe ganho hipotético de ganho medido; não faça alegação regulatória automática.
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
# MAGIC 1. Se o preparo for necessário, confirme destino e autorização: ele sobrescreve `workspace.default.hub_exemplo_fatos` e `workspace.default.hub_exemplo_features`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre contexto e skill selecionados com evidência disponível.
# MAGIC    Relato do assistente não comprova sozinho leitura, importação, chamada
# MAGIC    ou conclusão; confira os artefatos exigidos pela rota da skill.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-feature-engineering`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Sem janela de observação.** "Média de transações" sem janela é uma feature diferente a cada execução.
# MAGIC - **Sem atraso de publicação.** Data de referência no passado não garante disponibilidade; é o vazamento que mais passa.
# MAGIC - **Para uma feature só.** O valor está no conjunto e nas suas fronteiras temporais comuns.
