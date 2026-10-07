# Databricks notebook source
# MAGIC %md
# MAGIC # `baseline_orchestration` — o baseline que decide se vale a pena continuar
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
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. A fixture não treina modelo.
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
# MAGIC O briefing em branco está em [`baseline_orchestration.md`](./baseline_orchestration.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `COLUNAS_PROIBIDAS` e `PONTO_NO_TEMPO` são os dois campos que impedem o baseline de sair excelente e inútil. Uma AUC alta pede investigação de leakage, split e população; o valor isolado não prova vazamento nem qualidade.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-baseline-ml para construir um baseline simples, auditável e apropriado
# MAGIC ao problema. Priorize uma referência honesta antes de otimização complexa.
# MAGIC
# MAGIC DEFINIÇÃO
# MAGIC - Dataset/features: workspace.default.hub_exemplo_clientes
# MAGIC - Unidade e chave: uma linha por cliente e data; `id_cliente` + `dt_referencia`
# MAGIC - Target e semântica do evento: `alvo` = 1 quando o cliente respondeu à campanha
# MAGIC - Tipo: classificação binária
# MAGIC - Ponto de predição/cutoff: nenhuma feature pode usar informação posterior a `dt_referencia`
# MAGIC - Horizonte: 30 dias
# MAGIC - Período disponível: 2026-01 a 2026-06
# MAGIC - Split e justificativa: temporal — treino até 2026-04, teste em 2026-05/06 — porque há data e o uso real é prever o próximo período
# MAGIC - Colunas proibidas/PII: qualquer coluna derivada de `alvo`; `id_cliente` como preditor
# MAGIC - Métrica primária e custo de erro: AUC como métrica principal; o custo de falso positivo é uma abordagem desperdiçada, o de falso negativo é um cliente não abordado
# MAGIC - Restrições de compute/prazo/bibliotecas: serverless; use `hub_snippets.ml.split_temporal` e `hub_snippets.ml.train_lgbm`
# MAGIC - Modo: plano e código; não execute
# MAGIC
# MAGIC DIAGNÓSTICO ANTES DO TREINO
# MAGIC 1. Confirme schema, volume, target, prevalência/faixa, duplicidade e granularidade.
# MAGIC 2. Verifique leakage, disponibilidade temporal, censura, grupos relacionados e
# MAGIC    desbalanceamento. Não use variável cuja informação surge depois do cutoff.
# MAGIC 3. Escolha split coerente: temporal quando há produção no futuro, por grupo quando
# MAGIC    entidades se repetem, estratificado somente quando isso não causa leakage.
# MAGIC 4. Defina baseline ingênuo e baseline de modelo. Deep learning, tuning amplo ou
# MAGIC    modelos complexos só entram depois de uma referência mais simples.
# MAGIC 5. Apresente plano, custo provável e dependências antes de executar.
# MAGIC
# MAGIC EXECUÇÃO SEGURA
# MAGIC - Use seed e registre versões, parâmetros, schema das features e split.
# MAGIC - Use MLflow para registrar parâmetros, métricas e artefatos quando disponível;
# MAGIC   informe claramente se logging ou tracking não puder ser validado.
# MAGIC - Avalie no holdout uma única vez para decisão final; ajuste no conjunto de validação.
# MAGIC - Para classificação, inclua métricas adequadas à prevalência e à decisão; não trate
# MAGIC   AUC como percentual de acertos. Para regressão, declare unidade e sensibilidade a
# MAGIC   outliers. Para survival/ranking/time series, use métricas próprias do problema.
# MAGIC - Não registre PII ou amostras brutas como artefatos.
# MAGIC - Não promova modelo, não grave tabela, não publique endpoint e não altere produção
# MAGIC   sem pedido separado e confirmação explícita.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Problem framing e pressupostos.
# MAGIC - Tabela de candidatos e justificativa do baseline escolhido.
# MAGIC - Código modular e parametrizado, se solicitado.
# MAGIC - Resultados por split/tempo/segmento com incerteza ou variabilidade quando viável.
# MAGIC - Comparação com baseline ingênuo, erros relevantes e riscos.
# MAGIC - Registro de reprodutibilidade e próximos experimentos priorizados.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme ausência de sobreposição/leakage entre splits.
# MAGIC - Confirme que preprocessing foi ajustado somente no treino.
# MAGIC - Verifique consistência entre direção da métrica, evento positivo e threshold.
# MAGIC - Diferencie resultados medidos, inferências e expectativas.
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
# MAGIC Skill esperada aqui: `hub-ml-baseline-ml`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Como modelo final.** Baseline é piso, não entrega.
# MAGIC - **Sem declarar as colunas proibidas.** É a forma mais comum de produzir um resultado excelente e sem valor.
# MAGIC - **Com split aleatório em dado temporal.** O teste fica otimista e a produção decepciona.
