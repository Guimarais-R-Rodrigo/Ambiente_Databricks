# Databricks notebook source
# MAGIC %md
# MAGIC # `explainability` — explicar o modelo para quem decide, e para quem audita
# MAGIC
# MAGIC **Prompt não executa.** Ele é um briefing para colar num chat, e a
# MAGIC resposta vem de uma interação que notebook nenhum reproduz. Este notebook
# MAGIC tem três partes, e só as duas primeiras rodam:
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
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, de `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | **sim** — cria a tabela `workspace.default.hub_exemplo_clientes` para o chat poder consultá-la |
# MAGIC | Diferença Free × trabalho | no trabalho, aponte o prompt para uma tabela real governada em vez da sintética |

# COMMAND ----------
# MAGIC %md
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
# MAGIC O briefing em branco está em [`explainability.md`](./explainability.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC O campo `PUBLICO` muda a resposta mais que qualquer outro: o mesmo modelo explicado para o comitê e para o time técnico produz dois documentos que não se parecem.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-explainability para explicar o modelo anexado com rigor, respeitando o
# MAGIC objetivo, o público e as limitações do método.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Modelo/MLflow run/URI: LightGBM binário, treinado com `hub_snippets.ml.train_lgbm` sobre a base da Parte 1
# MAGIC - Dataset e split: workspace.default.hub_exemplo_clientes; treino até 2026-04, teste em 2026-05/06
# MAGIC - Target/evento positivo: `alvo` = 1 quando o cliente respondeu à campanha
# MAGIC - Objetivo da explicação: global e comunicação; o caso individual entra só como exemplo
# MAGIC - Público e nível técnico: dois: um resumo para o gestor da campanha e uma seção técnica para o time de modelagem
# MAGIC - Métodos desejados: SHAP; proponha alternativa se o custo for alto
# MAGIC - Amostra/segmentos/período: amostra de 1.000 linhas do teste; sem segmentação
# MAGIC - Features proibidas/PII: serverless; `shap` exige `%pip install shap==0.44.1` — ver `hub_snippets/requirements-optional.txt`
# MAGIC - Modo: plano e código; não execute
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Confirme versão do modelo, transformação, ordem/schema das features e split.
# MAGIC 2. Diferencie performance de explicabilidade: AUC não é percentual de casos corretos.
# MAGIC 3. Para SHAP, declare o explainer, background, espaço da saída (log-odds, score ou
# MAGIC    probabilidade quando suportado) e tratamento multiclasse. Valores SHAP são
# MAGIC    contribuições relativas ao baseline, não percentuais causais.
# MAGIC 4. Produza visão global e local somente no nível solicitado. Não conclua causalidade,
# MAGIC    fairness ou conformidade a partir de importância de variável isolada.
# MAGIC 5. Faça sanity checks: estabilidade por amostra/tempo/segmento, sinal esperado,
# MAGIC    correlação entre features e sensibilidade do background.
# MAGIC 6. Não exponha registros individuais ou atributos sensíveis. Não publique artefatos
# MAGIC    nem altere o modelo sem autorização explícita.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Resumo executivo e definição correta de cada visual/métrica.
# MAGIC - Achados globais e locais separados, com evidência e incerteza.
# MAGIC - Limitações, riscos de interpretação e validações pendentes.
# MAGIC - Código reprodutível, se solicitado, com amostragem e seed declaradas.
# MAGIC - Recomendações que não extrapolem o método.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme modelo, dataset, split, população e espaço da saída.
# MAGIC - Verifique que classes e sinais estão rotulados corretamente.
# MAGIC - Diferencie associação, contribuição do modelo e efeito causal.
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
# MAGIC Por que não   : prompt produz resposta de assistente, e nenhum job
# MAGIC                 reproduz isso. Resposta inventada é pior que resposta
# MAGIC                 nenhuma — ensina que o assistente faz algo que ele não faz.
# MAGIC Quem preenche : quem tiver acesso ao Genie Code do workspace.
# MAGIC ```
# MAGIC
# MAGIC **Como preencher**, quando for a hora:
# MAGIC
# MAGIC 1. Rode a Parte 1 deste notebook — ela cria `workspace.default.hub_exemplo_clientes`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre **qual skill foi carregada** — é a única forma de saber se o
# MAGIC    roteamento está fazendo o que se espera fora da bateria de forward
# MAGIC    tests. Se não souber, pergunte no mesmo chat.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-explainability`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Para afirmar causa.** SHAP explica a previsão do modelo, não o fenômeno.
# MAGIC - **Sem declarar o público.** Um relatório que serve aos dois não serve a nenhum.
# MAGIC - **Como validação.** Explicar um modelo ruim em detalhe não o torna bom.
