# Databricks notebook source
# MAGIC %md
# MAGIC # `cross_eda` — duas fontes, e se elas sustentam um modelo juntas
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
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. Os mesmos destinos são usados pelo exemplo de Feature Engineering.
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

print(f"fatos: {fatos.count()} decisões | features: {features.count()} registros")
fatos.show(3, truncate=False)
features.show(3, truncate=False)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A fixture foi gerada com `atraso_real_dias=3` e `pct_feature_futura=0.2`: uma em cada cinco features tem data de referência **posterior** à decisão que ela deveria explicar. É vazamento plantado, e é o que a resposta precisa encontrar sozinha.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`cross_eda.md`](./cross_eda.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC O campo `PONTO_NO_TEMPO` é o que separa uma resposta útil de uma perigosa. Ele está preenchido com a exigência explícita — sem ela, o assistente faz o join que parece certo e produz um modelo que não funciona.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-cross-eda-ml para comparar os recursos anexados e avaliar se formam uma
# MAGIC base de modelagem coerente, sem executar escrita ou treino.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - EDAs/notebooks/tabelas anexados: workspace.default.hub_exemplo_fatos e workspace.default.hub_exemplo_features
# MAGIC - Entidade âncora e granularidade: cliente; uma linha por decisão em `fatos`, várias por cliente em `features`
# MAGIC - Target/evento: `alvo` em `fatos` = 1 quando houve resposta em até 30 dias da decisão
# MAGIC - Cutoff/ponto de predição: **obrigatório**: só pode entrar feature cuja `dt_referencia` seja anterior a `dt_decisao`, com folga para o atraso de publicação
# MAGIC - Horizonte: 30 dias após `dt_decisao`
# MAGIC - Chaves de ligação por fonte: `id_cliente`
# MAGIC - Período esperado por fonte: 2026-01 a 2026-06 nas duas
# MAGIC - Fonte de verdade por conceito: não informado
# MAGIC - Foco: completo
# MAGIC - Restrições e dados sensíveis: serverless; use `hub_snippets.spark.pit_join` se o join point-in-time for necessário
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Faça inventário dos recursos realmente anexados; não invente resultados dos EDAs.
# MAGIC 2. Compare granularidade, chaves, cobertura temporal, atualidade, completude, target,
# MAGIC    população e filtros. Marque incompatibilidades sem normalizá-las silenciosamente.
# MAGIC 3. Proponha um grafo de joins e classifique cardinalidade esperada/observada. Calcule
# MAGIC    cobertura dos matches e risco de multiplicação, órfãos e viés de seleção.
# MAGIC 4. Faça análise ponto-no-tempo: quando cada atributo passou a estar disponível e se
# MAGIC    pode vazar evento, tratamento ou resultado posterior ao cutoff.
# MAGIC 5. Avalie complementaridade apenas com evidência; não confunda correlação com ganho
# MAGIC    incremental nem qualidade da fonte com poder preditivo.
# MAGIC 6. Em alto volume, use agregações e amostras controladas. Não colete nem exiba PII.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Mapa de fontes e joins propostos.
# MAGIC - Matriz de compatibilidade por fonte e dimensão.
# MAGIC - Scorecard de readiness com critérios, evidências e ressalvas.
# MAGIC - Lista de riscos P0/P1/P2 e ações necessárias antes de feature engineering.
# MAGIC - Recomendação: prosseguir, prosseguir com condicionantes ou bloquear, com evidência.
# MAGIC - Código de validação de joins somente se solicitado, sem gravar resultados.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme contagens antes/depois dos joins e cobertura por fonte/período.
# MAGIC - Separe fatos observados, inferências e itens não verificáveis.
# MAGIC - Declare explicitamente toda fonte não anexada ou EDA incompleta.
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
# MAGIC Skill esperada aqui: `hub-ml-cross-eda-ml`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Sem declarar o ponto no tempo.** É a única linha que separa este prompt de uma receita para vazamento.
# MAGIC - **Com uma fonte só.** O valor está no cruzamento; para uma tabela, use `eda_completa`.
# MAGIC - **Antes de saber o target.** Readiness é "dá para modelar isto?" — sem o isto, não há pergunta.
