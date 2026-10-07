# Databricks notebook source
# MAGIC %md
# MAGIC # `explainability_report` — explicar o modelo sem prometer causa
# MAGIC
# MAGIC **O problema.** Um relatório de explicabilidade circula por gente que não leu o modelo, e a leitura natural de "renda é a variável mais importante" é causal: mexer na renda muda o resultado. SHAP não diz isso — diz quanto cada variável contribuiu para a previsão **daquele modelo**, que pode estar apoiado numa correlação espúria.
# MAGIC
# MAGIC **O que este helper faz.** Gera a versão executiva e a técnica do mesmo conjunto de importâncias, com a ressalva de causalidade embutida.

# MAGIC
# MAGIC **Guia local completo:** [README deste objeto](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side** |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

from hub_snippets.ml.explainability_report import (
    generate_executive_report, generate_technical_summary,
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Importâncias já calculadas

# COMMAND ----------

# O helper recebe as importâncias prontas: quem as calcula é o shap_explainer,
# que depende de biblioteca opcional. Aqui elas entram como dado.
shap_importance = pd.DataFrame({
    "feature": ["uso_limite", "atraso_medio", "renda", "tempo_relacionamento"],
    "pct_importance": [41.0, 28.0, 19.0, 12.0],  # em %, somando 100
})
nomes_negocio = {
    "uso_limite": "percentual do limite utilizado",
    "atraso_medio": "atraso médio de pagamento",
    "renda": "renda declarada",
    "tempo_relacionamento": "tempo de relacionamento",
}

executivo = generate_executive_report(
    shap_importance,
    feature_business_names=nomes_negocio,
    target_description="probabilidade de inadimplência em 12 meses",
    model_metric=0.78,
    metric_name="AUC",
)
print(executivo)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O relatório traduz nome técnico para nome de negócio e
# MAGIC apresenta a ordem de contribuição. A tradução não é cosmética: quem decide
# MAGIC não sabe o que é `uso_limite`, e um relatório que exige glossário não é
# MAGIC lido.
# MAGIC
# MAGIC Repare no que ele **não** diz: que reduzir o uso do limite reduz a
# MAGIC inadimplência. A contribuição é para a previsão do modelo, não para o
# MAGIC fenômeno — e essa distinção some no resumo de quem apresenta.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A versão técnica serve para outra pergunta

# COMMAND ----------

nativa = pd.DataFrame({
    "feature": ["uso_limite", "renda", "atraso_medio", "tempo_relacionamento"],
    "pct_importance": [35.0, 30.0, 22.0, 13.0],
})
try:
    print(generate_technical_summary(shap_importance, native_importance=nativa))
except ImportError as erro:
    print(f"não executado neste laboratório: {erro}")

# COMMAND ----------
# MAGIC %md
# MAGIC Registro do impedimento encontrado no ensaio sintético de referência:
# MAGIC
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO no laboratório
# MAGIC Por que não   : ImportError: Missing optional dependency 'tabulate'.
# MAGIC ```
# MAGIC
# MAGIC O resumo técnico exige tabulate. Para comparar rankings, os dois DataFrames precisam de feature e rank, com uma linha por feature. A fixture acima ainda não fornece rank: crie-o de acordo com a ordenação de cada importância antes da chamada. Esse exemplo precisa dessa preparação adicional para concluir.
# MAGIC
# MAGIC **Como ler, quando roda.** As duas ordenações **discordam**: SHAP põe `atraso_medio` em
# MAGIC segundo e a importância nativa põe `renda`. Discordância é comum e não é
# MAGIC defeito — as duas podem medir quantidades diferentes. A definição de
# MAGIC importância nativa depende do estimador/configuração (por exemplo, ganho,
# MAGIC redução de impureza ou contagem de splits); SHAP atribui contribuição no
# MAGIC espaço de saída explicado pelo modelo.
# MAGIC
# MAGIC Correlação entre features **pode** contribuir para a discordância, mas não
# MAGIC é a única causa: definições de importância, amostra e propriedades do modelo
# MAGIC também importam. Discordância é sinal para investigar, não para escolher a
# MAGIC ordenação que agrada.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como evidência causal.** SHAP explica o modelo, não o fenômeno.
# MAGIC - **Para justificar recusa a um cliente.** Explicação de modelo não é fundamentação de decisão individual sob regulação.
# MAGIC - **Com uma ordenação só, quando os métodos discordam.** A discordância é a informação.
# MAGIC - **Sem a métrica do modelo junto.** Explicar bem um modelo ruim é explicar bem um erro.
