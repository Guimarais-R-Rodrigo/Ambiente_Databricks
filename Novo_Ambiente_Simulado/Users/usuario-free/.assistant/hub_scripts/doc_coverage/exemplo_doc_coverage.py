# Databricks notebook source
# MAGIC %md
# MAGIC # `doc_coverage` — mede adjacência, não qualidade
# MAGIC
# MAGIC **O problema.** Notebook sem explicação é o formato mais comum de dívida
# MAGIC técnica em análise: o código funciona, ninguém sabe por que aquelas escolhas
# MAGIC foram feitas, e três meses depois nem o autor sabe. Medir isso ajuda a
# MAGIC priorizar — mas medir errado é pior, porque cria a impressão de que o
# MAGIC problema foi resolvido.
# MAGIC
# MAGIC **O que este script faz.** Conta quantas células de código têm markdown
# MAGIC adjacente. **Só isso.** Ele não lê a explicação e não sabe se ela presta.

# MAGIC
# MAGIC **Guia local completo:** [README deste script](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico; o script não usa Spark |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | nenhum. Ele lê **arquivos**, não tabelas |
# MAGIC | Escrita | três arquivos temporários em `/tmp` do driver, removidos ao final |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_scripts.doc_coverage import SOURCE_MARKERS, doc_coverage

print(f"marcadores de célula reconhecidos: {SOURCE_MARKERS}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparo — dois notebooks sintéticos, um documentado e outro não

# MAGIC ```text
# MAGIC marcadores de célula reconhecidos: {'.py': ('# COMMAND ----------', ('# MAGIC %md', '# MAGIC %md-sandbox')), '.sql': ('-- COMMAND ----------', ('-- MAGIC %md', '-- MAGIC %md-sandbox')), '.scala': ('// COMMAND ----------', ('// MAGIC %md', '// MAGIC %md-sandbox')), '.r': ('# COMMAND ----------', ('# MAGIC %md', '# MAGIC %md-sandbox'))}
# MAGIC ```
# MAGIC
# COMMAND ----------

import json
import pathlib

BEM = pathlib.Path("/tmp/hub_exemplo_documentado.py")
MAL = pathlib.Path("/tmp/hub_exemplo_seco.py")

BEM.write_text(
    "# Databricks notebook source\n"
    "# MAGIC %md\n"
    "# MAGIC ## Carga da base\n"
    "# MAGIC Lê a tabela de contatos do mês, filtrando quem foi efetivamente contatado.\n"
    "\n# COMMAND ----------\n\n"
    "df = spark.table('exemplo').filter('contatado = 1')\n"
    "\n# COMMAND ----------\n"
    "# MAGIC %md\n"
    "# MAGIC ## Agregação\n"
    "# MAGIC Uma linha por segmento, com a taxa de resposta.\n"
    "\n# COMMAND ----------\n\n"
    "resumo = df.groupBy('segmento').count()\n",
    encoding="utf-8",
)
MAL.write_text(
    "# Databricks notebook source\n"
    "df = spark.table('exemplo').filter('contatado = 1')\n"
    "\n# COMMAND ----------\n\n"
    "resumo = df.groupBy('segmento').count()\n"
    "\n# COMMAND ----------\n\n"
    "resumo.write.mode('overwrite').saveAsTable('destino')\n",
    encoding="utf-8",
)
print(f"documentado: {BEM}\nseco       : {MAL}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. A medida nos dois casos

# MAGIC ```text
# MAGIC documentado: /tmp/hub_exemplo_documentado.py
# MAGIC seco       : /tmp/hub_exemplo_seco.py
# MAGIC ```
# MAGIC
# COMMAND ----------

for rotulo, caminho in [("documentado", BEM), ("seco", MAL)]:
    resultado = doc_coverage(str(caminho))
    print(f"--- {rotulo} ---")
    print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC --- documentado ---
# MAGIC {
# MAGIC   "path": "/tmp/hub_exemplo_documentado.py",
# MAGIC   "format": ".py",
# MAGIC   "total_code_cells": 2,
# MAGIC   "total_markdown_cells": 2,
# MAGIC   "coverage_pct": 100.0,
# MAGIC   "uncovered_cell_indexes": [],
# MAGIC   "metric_note": "Adjacency heuristic; review explanatory quality separately."
# MAGIC }
# MAGIC --- seco ---
# MAGIC {
# MAGIC   "path": "/tmp/hub_exemplo_seco.py",
# MAGIC   "format": ".py",
# MAGIC   "total_code_cells": 3,
# MAGIC   "total_markdown_cells": 0,
# MAGIC   "coverage_pct": 0.0,
# MAGIC   "uncovered_cell_indexes": [
# MAGIC     0,
# MAGIC     1,
# MAGIC     2
# MAGIC   ],
# MAGIC   "metric_note": "Adjacency heuristic; review explanatory quality separately."
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A diferença entre os dois é exatamente o que o script se
# MAGIC propõe a medir: presença de markdown ao lado do código. Nada além disso.
# MAGIC
# MAGIC O erro de interpretação mais provável — e o motivo de este notebook
# MAGIC existir — é tratar cobertura alta como notebook bem documentado. Uma célula
# MAGIC de markdown escrita `## Agregação` conta igual a uma que explique **por que**
# MAGIC se agrupou por segmento e não por canal. A primeira não ajuda ninguém e
# MAGIC pontua o mesmo.
# MAGIC
# MAGIC Use o número para **achar o que revisar**, nunca para declarar revisado.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A prova de que ele não lê o conteúdo

# COMMAND ----------

VAZIO = pathlib.Path("/tmp/hub_exemplo_vazio.py")
VAZIO.write_text(
    "# Databricks notebook source\n"
    "# MAGIC %md\n"
    "# MAGIC .\n"          # markdown que não explica coisa alguma
    "\n# COMMAND ----------\n\n"
    "df = spark.table('exemplo')\n",
    encoding="utf-8",
)
print(json.dumps(doc_coverage(str(VAZIO)), indent=2, ensure_ascii=False, default=str))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC {
# MAGIC   "path": "/tmp/hub_exemplo_vazio.py",
# MAGIC   "format": ".py",
# MAGIC   "total_code_cells": 1,
# MAGIC   "total_markdown_cells": 1,
# MAGIC   "coverage_pct": 100.0,
# MAGIC   "uncovered_cell_indexes": [],
# MAGIC   "metric_note": "Adjacency heuristic; review explanatory quality separately."
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** `coverage_pct` sai em **100,0** — o mesmo valor do notebook
# MAGIC bem documentado da célula anterior. Um markdown com um ponto final produz a
# MAGIC mesma cobertura que um parágrafo explicativo. Isso não é defeito a corrigir: qualquer medida
# MAGIC automática de qualidade de texto seria pior, porque erraria com aparência de
# MAGIC autoridade. O script declara o que mede, e o limite é a informação mais
# MAGIC honesta que ele tem a dar.

# COMMAND ----------

for p in (BEM, MAL, VAZIO):
    p.unlink(missing_ok=True)
print("arquivos temporários removidos")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este script
# MAGIC
# MAGIC ```text
# MAGIC arquivos temporários removidos
# MAGIC ```
# MAGIC
# MAGIC - **Como métrica de qualidade.** Ele mede adjacência de markdown. Texto
# MAGIC   vazio pontua igual a explicação boa.
# MAGIC - **Como meta de equipe.** Métrica que vira meta deixa de medir: o caminho
# MAGIC   mais curto para 100% é encher o notebook de títulos.
# MAGIC - **Sobre `.ipynb` esperando precisão.** O tratamento de notebook JSON é
# MAGIC   heurística; o formato-fonte com marcador é o caso confiável.
# MAGIC - **Para avaliar código que não é notebook.** Módulo de biblioteca se
# MAGIC   documenta por docstring, e isto aqui não olha docstring.
