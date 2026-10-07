# Databricks notebook source
# MAGIC %md
# MAGIC # `survival_cox` — o efeito de cada variável sobre o tempo até o evento
# MAGIC
# MAGIC **O problema.** Kaplan-Meier compara curvas não ajustadas. Para estimar a associação entre renda e hazard de cancelamento condicionada às demais covariáveis do modelo, é preciso uma abordagem que também trate censura.
# MAGIC
# MAGIC **O que este helper faz.** Ajusta o modelo de riscos proporcionais de Cox e testa o pressuposto que ele exige, que é onde quase todo mundo escorrega.

# MAGIC
# MAGIC **Guia local completo:** [README deste objeto](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `lifelines` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~1 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install lifelines

# COMMAND ----------
# MAGIC %restart_python

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparação
# MAGIC
# MAGIC `%restart_python` reinicia o interpretador, então tudo — inclusive o
# MAGIC `sys.path` — precisa vir **depois** dele.

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np

rng = np.random.default_rng(42)

from hub_snippets.ml.survival_cox import train_cox_ph, validate_proportionality

# COMMAND ----------
# MAGIC %md
# MAGIC Este exemplo passa log_mlflow=False para desativar apenas o registro explícito do helper. Antes de habilitar tracking, confirme dependência, experimento, permissões, configuração do runtime e autologging da sessão. Uma falha numa configuração de serverless não determina o suporte em outras configurações.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base com dois efeitos de sinal oposto

# COMMAND ----------

import pandas as pd

n = 1200
renda_padrao = rng.normal(0, 1, n)      # protege: mais renda, menos risco
uso_limite = rng.normal(0, 1, n)        # agrava: mais uso, mais risco
risco = np.exp(-0.6 * renda_padrao + 0.5 * uso_limite)
tempo_ate_evento = rng.exponential(20.0 / risco)
duracao = np.minimum(tempo_ate_evento, 24.0)
evento = (tempo_ate_evento <= 24.0).astype(int)

base = pd.DataFrame({
    "duracao": duracao.round(2),
    "evento": evento,
    "renda_padrao": renda_padrao.round(4),
    "uso_limite": uso_limite.round(4),
})
print(f"linhas {len(base)} | eventos {evento.sum()} | censurados {(1 - evento).sum()}")

# COMMAND ----------

modelo, metricas = train_cox_ph(
    base, duration_col="duracao", event_col="evento",
    feature_cols=["renda_padrao", "uso_limite"], log_mlflow=False,
)
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC c_index                  0.6848
# MAGIC log_likelihood           -5224.94
# MAGIC aic                      10453.89
# MAGIC n_observations           1200
# MAGIC n_events                 815
# MAGIC
# MAGIC               exp(coef)  lower 95%  upper 95%             p
# MAGIC uso_limite     1.623689   1.513392   1.742026  1.475064e-41
# MAGIC renda_padrao   0.574532   0.533537   0.618676  9.563575e-49
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Os *hazard ratios* são a saída que interessa, e leem-se como
# MAGIC multiplicadores do risco instantâneo:
# MAGIC
# MAGIC - `uso_limite` **1,62**: cada desvio-padrão a mais no uso do limite
# MAGIC   multiplica o risco por 1,62 — 62% a mais.
# MAGIC - `renda_padrao` **0,57**: cada desvio-padrão a mais de renda **reduz** o
# MAGIC   risco a 57% do anterior. Valor abaixo de 1 é fator de proteção.
# MAGIC
# MAGIC Como esta base é sintética, dá para conferir: o efeito plantado foi
# MAGIC `+0,5` e `−0,6` em escala log, e `exp(0,5) = 1,65`, `exp(−0,6) = 0,55`. O
# MAGIC modelo recuperou os dois. É a checagem que raramente se pode fazer com
# MAGIC dado real, e que vale fazer sempre que se puder.
# MAGIC
# MAGIC O **C-index de 0,6848** é calculado no próprio ajuste e mede ordenação de
# MAGIC tempos/eventos nessa amostra. Não há corte universal que transforme 0,68 em
# MAGIC `bom` ou `ruim`. Neste sintético, os coeficientes recuperam aproximadamente os
# MAGIC parâmetros plantados, mas isso é diferente de demonstrar previsão individual
# MAGIC fora da amostra.


# COMMAND ----------

diagnostico = validate_proportionality(modelo, base, "duracao", "evento")
print(diagnostico.to_string())

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC         feature  test_statistic         p  violates_at_0_05
# MAGIC 0  renda_padrao        0.405410  0.524309             False
# MAGIC 1    uso_limite        0.748504  0.386950             False
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Este é o teste que quase todo mundo pula. Cox assume que o
# MAGIC efeito de cada variável é **constante ao longo do tempo** — o *hazard ratio*
# MAGIC de 1,62 vale igual no mês 1 e no mês 23. Aqui os dois p-valores estão bem
# MAGIC acima de 0,05 e o teste **não rejeita** proporcionalidade neste exemplo. Isso
# MAGIC era esperado numa base gerada com efeito constante, mas p alto não prova que
# MAGIC o pressuposto seja verdadeiro em dados reais.
# MAGIC
# MAGIC Em dado real a violação é comum, e o sintoma típico é uma variável que
# MAGIC separa muito no começo e deixa de separar depois. Quando isso acontece, o
# MAGIC coeficiente único vira uma média de dois regimes diferentes — e não
# MAGIC descreve nenhum dos dois. A saída é estratificar por essa variável ou
# MAGIC declarar interação com o tempo, não ignorar o teste.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem testar a proporcionalidade.** É o pressuposto central: o efeito da variável não pode mudar ao longo do tempo. A segunda célula existe para isso.
# MAGIC - **Para prever tempo individual.** Cox modela o *risco relativo*, não o tempo esperado de cada caso.
# MAGIC - **Com variável medida depois do início do acompanhamento.** É vazamento com outro nome — o mesmo que `pit_join` evita do lado do dado.
