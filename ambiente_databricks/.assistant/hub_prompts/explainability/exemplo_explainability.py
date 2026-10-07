# Databricks notebook source
# MAGIC %md
# MAGIC # `explainability` — explicar o modelo para quem decide, e para quem audita
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
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. O preparo não treina modelo nem calcula SHAP.
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
# MAGIC - Modelo/MLflow run/URI: LightGBM binário PRETENDIDO; nenhum modelo foi treinado na Parte 1. Artefato/run/URI: NÃO INFORMADO; produzir somente plano.
# MAGIC - Dataset e split: workspace.default.hub_exemplo_clientes; treino até 2026-04, teste em 2026-05/06
# MAGIC - Target/evento positivo: `alvo` = 1 quando o cliente respondeu à campanha
# MAGIC - Objetivo da explicação: global e comunicação; o caso individual entra só como exemplo
# MAGIC - Público e nível técnico: dois: um resumo para o gestor da campanha e uma seção técnica para o time de modelagem
# MAGIC - Métodos desejados: SHAP; proponha alternativa se o custo for alto
# MAGIC - Amostra/segmentos/período: amostra de 1.000 linhas do teste; sem segmentação
# MAGIC - Features proibidas/PII: NÃO INFORMADO; não expor registros individuais
# MAGIC - Ambiente/dependências: serverless; conferir SHAP e a versão compatível em `hub_snippets/requirements-optional.txt`; instalação requer autorização separada
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
# MAGIC Skill esperada aqui: `hub-ml-explainability`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Para afirmar causa.** SHAP explica a previsão do modelo, não o fenômeno.
# MAGIC - **Sem declarar o público.** Um relatório que serve aos dois não serve a nenhum.
# MAGIC - **Como validação.** Explicar um modelo ruim em detalhe não o torna bom.
