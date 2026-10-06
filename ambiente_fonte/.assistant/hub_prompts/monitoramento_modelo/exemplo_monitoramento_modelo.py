# Databricks notebook source
# MAGIC %md
# MAGIC # `monitoramento_modelo` — monitorar sem transformar ruído em alarme
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
# MAGIC | Escrita | **sim, overwrite** — sobrescreve `workspace.default.hub_exemplo_monitor_ref` e `workspace.default.hub_exemplo_monitor_atual` |
# MAGIC | Diferença Free × trabalho | fonte real exige autorização, revisão de dados sensíveis e contrato próprio; este preparo é sintético |

# COMMAND ----------
# MAGIC %md
# MAGIC **Antes de executar a Parte 1 ou Run all:** o preparo sobrescreve `workspace.default.hub_exemplo_monitor_ref` e `workspace.default.hub_exemplo_monitor_atual`
# MAGIC com `mode("overwrite")`. Confira destino e autorização; pode substituir dados
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. As fixtures não provam serving, inferências, tracking ou performance de modelo real.
# MAGIC
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

# Dois períodos da mesma base, com prevalência e nulos diferentes — que é o
# que o monitoramento precisa distinguir de ruído.
base_ref = fixtures.base_tabular(n=3000, seed=42, prevalencia_alvo=0.18,
                                 pct_nulos_renda=0.04)
base_atual = fixtures.base_tabular(n=3000, seed=7, prevalencia_alvo=0.11,
                                   pct_nulos_renda=0.12)
base_ref.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_monitor_ref")
base_atual.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_monitor_atual")

for nome, df in (("referência", base_ref), ("atual", base_atual)):
    prev = df.filter("alvo = 1").count() / df.count()
    nulos = df.filter("renda is null").count() / df.count()
    print(f"{nome:12s} prevalência {prev:.3f} | renda nula {nulos:.3f}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A fixture solicita prevalências de 0,18 e 0,11 e nulidade de 0,04 e 0,12. Confira os valores calculados; as diferenças são plantadas no gerador. Em dados reais, sazonalidade ou problema de carga seriam hipóteses a investigar, não causas demonstradas por essas taxas.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`monitoramento_modelo.md`](./monitoramento_modelo.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `TARGET_E_LABEL_DELAY` é o campo que decide se o monitoramento de performance é possível. Se o rótulo demora 30 dias, você não tem performance de ontem — tem drift de entrada, que é outra coisa.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-monitoramento-modelo para desenhar ou avaliar monitoramento técnico e de
# MAGIC negócio do modelo anexado, sem alterar produção.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Modelo/run/version: cenário ilustrativo de LightGBM de propensão; nenhum modelo real ou produção é comprovado por estas fixtures
# MAGIC - Serving endpoint, job ou pipeline: batch diário PROPOSTO; endpoint/job/tabela de score reais NÃO INFORMADOS
# MAGIC - Baseline de referência: workspace.default.hub_exemplo_monitor_ref, período de treino
# MAGIC - Dados atuais e janela: workspace.default.hub_exemplo_monitor_atual, últimos 30 dias
# MAGIC - Target/evento e atraso do rótulo: `alvo` observável 30 dias após a decisão — a performance do mês corrente ainda não existe
# MAGIC - Métricas e direção de melhora: AUC (maior é melhor), PSI por feature (menor é melhor), taxa de nulo (menor é melhor)
# MAGIC - Segmentos críticos: por UF
# MAGIC - SLOs/thresholds existentes: proponha, e diga o que cada limite custa em alarme falso
# MAGIC - Frequência e owners: diário; dono é o time de CRM analítico
# MAGIC - Modo: desenho e código; não execute
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Confirme lineage entre modelo, features, inferências, predições e rótulos.
# MAGIC 2. Separe saúde operacional (erro, latência, throughput), qualidade dos dados,
# MAGIC    drift, qualidade preditiva, calibração e métricas de negócio.
# MAGIC 3. Compare sempre com baseline e direção corretos; melhoria não deve gerar alerta por
# MAGIC    causa de `abs(delta)`. Inclua amostra, volume, incerteza e sazonalidade.
# MAGIC 4. Trate ausência/nulos como categoria observável quando relevante e monitore
# MAGIC    cobertura/latência de rótulos antes de calcular performance.
# MAGIC 5. Proponha níveis de alerta, owner, janela, deduplicação, runbook e critério de
# MAGIC    resolução. Retreino deve ser decisão governada, não reação automática a um ponto.
# MAGIC 6. Não altere endpoint, registre webhooks, reinicie job ou promova modelo sem pedido
# MAGIC    separado e autorização explícita.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Mapa de monitoramento e lacunas de observabilidade.
# MAGIC - Catálogo de métricas com fórmula, fonte, janela, direção, limite e owner.
# MAGIC - Diagnóstico com evidência e severidade, distinguindo incidente de variação esperada.
# MAGIC - Código/queries idempotentes, se solicitado.
# MAGIC - Runbook e critérios de investigação, rollback e eventual retreino.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme alinhamento temporal predição-rótulo e denominadores.
# MAGIC - Teste cenários de melhora, piora, sem rótulo, nulos e baixo volume.
# MAGIC - Não atribua causa ao drift sem investigação adicional.
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
# MAGIC 1. Se o preparo for necessário, confirme destino e autorização: ele sobrescreve `workspace.default.hub_exemplo_monitor_ref` e `workspace.default.hub_exemplo_monitor_atual`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre contexto e skill selecionados com evidência disponível.
# MAGIC    Relato do assistente não comprova sozinho leitura, importação, chamada
# MAGIC    ou conclusão; confira os artefatos exigidos pela rota da skill.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-monitoramento-modelo`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Confundindo drift com queda de performance.** Drift de entrada não implica modelo pior; são medidas diferentes.
# MAGIC - **Sem considerar o atraso do rótulo.** Cobrar AUC de ontem quando o rótulo leva 30 dias produz número inventado.
# MAGIC - **Com limiar copiado de artigo.** 0,1 e 0,25 de PSI são referência, não norma; calibre na sua série.
