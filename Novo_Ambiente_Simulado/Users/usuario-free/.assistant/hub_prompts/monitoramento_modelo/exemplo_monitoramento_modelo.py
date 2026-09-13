# Databricks notebook source
# MAGIC %md
# MAGIC # `monitoramento_modelo` — monitorar sem transformar ruído em alarme
# MAGIC
# MAGIC 📘 Guia local: [`README.md`](./README.md)
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
# MAGIC | Escrita | **sim** — cria/sobrescreve `workspace.default.hub_exemplo_monitor_ref` e `workspace.default.hub_exemplo_monitor_atual` para o chat consultá-las |
# MAGIC | Diferença Free × trabalho | no trabalho, aponte o prompt para uma tabela real governada em vez da sintética |

# COMMAND ----------
# MAGIC %md
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
# MAGIC **Como ler.** A prevalência caiu de ~0,18 para ~0,11 e a taxa de nulo triplicou. As duas mudanças são reais e têm causas diferentes: uma pode ser sazonalidade, a outra é quase certamente problema de carga. Um monitoramento que trata as duas igual gera alarme que ninguém lê.

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
# MAGIC - Modelo/run/version: LightGBM binário de propensão a resposta, em produção desde 2026-01
# MAGIC - Serving endpoint, job ou pipeline: batch diário, escrita em tabela de score
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
# MAGIC Por que não   : prompt produz resposta de assistente, e nenhum job
# MAGIC                 reproduz isso. Resposta inventada é pior que resposta
# MAGIC                 nenhuma — ensina que o assistente faz algo que ele não faz.
# MAGIC Quem preenche : quem tiver acesso ao Genie Code do workspace.
# MAGIC ```
# MAGIC
# MAGIC **Como preencher**, quando for a hora:
# MAGIC
# MAGIC 1. Rode a Parte 1 deste notebook — ela cria/sobrescreve `workspace.default.hub_exemplo_monitor_ref` e `workspace.default.hub_exemplo_monitor_atual`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre **qual skill foi carregada** — é a única forma de saber se o
# MAGIC    roteamento está fazendo o que se espera fora da bateria de forward
# MAGIC    tests. Se não souber, pergunte no mesmo chat.
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
