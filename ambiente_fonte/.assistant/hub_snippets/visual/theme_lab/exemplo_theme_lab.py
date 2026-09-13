# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.theme_lab` — prévia pessoal do Sistema de Temas
# MAGIC
# MAGIC Este notebook usa somente dados sintéticos. Ele não consulta tabela corporativa,
# MAGIC não treina modelo e não publica tema. A referência empacotada é uma fixture de
# MAGIC compatibilidade, não uma identidade aprovada.
# MAGIC
# MAGIC **Antes de executar:** leia o [README deste objeto](README.md). O laboratório
# MAGIC interativo usa `ipywidgets` quando a versão do runtime for compatível; o Hub não
# MAGIC instala a biblioteca automaticamente.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | notebook Python com dependências do Hub; ipywidgets requer compute compatível |
# MAGIC | Tema | `ResolvedTheme` notebook válido |
# MAGIC | Dados | inteiramente sintéticos |
# MAGIC | Escrita | nenhuma até que `save_root` seja explicitamente informado |
# MAGIC | Publicação | não existe nesta V05 |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_lab import (
    build_ipywidgets_lab,
    compare_preview,
    create_theme_lab,
    get_control_specs,
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Criar rascunho isolado

# COMMAND ----------

referencia = load_reference_theme("notebook")
rascunho = create_theme_lab(referencia)

print("contexto:", rascunho.current.context)
print("fingerprint:", rascunho.current.fingerprint)
print("alterado?:", rascunho.dirty)
print("revisão local:", rascunho.revision)

# COMMAND ----------
# MAGIC %md
# MAGIC A criação do rascunho não muda a configuração, não registra template Plotly e
# MAGIC não cria arquivo. `dirty=False` significa apenas que a proposta local ainda é
# MAGIC igual ao ponto de partida.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Metadados dos controles vêm do contrato

# COMMAND ----------

for spec in get_control_specs(rascunho.current):
    if spec.primary:
        print(spec.label, "|", spec.token, "|", spec.unit, "|", spec.minimum, spec.maximum)

# COMMAND ----------
# MAGIC %md
# MAGIC A interface apresenta nomes legíveis, mas mantém o token técnico visível para
# MAGIC rastreabilidade. Tipo e limites continuam sendo validados pelo núcleo V02.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Alteração programática e comparação

# COMMAND ----------

hash_antes = rascunho.current.content_sha256
rascunho.apply_updates({
    "brand.primary": "#0066cc",
    "section.title_px": 20,
})

assert rascunho.current.tokens["brand.primary"] == "#0066CC"
assert rascunho.current.content_sha256 != hash_antes
assert rascunho.dirty

comparacao = compare_preview(rascunho)
comparacao.current.bar_figure.show()
comparacao.proposal.bar_figure.show()
displayHTML(comparacao.proposal.header_html)
displayHTML(comparacao.proposal.kpi_html)
displayHTML(comparacao.proposal.table_html)

# COMMAND ----------
# MAGIC %md
# MAGIC Os dois gráficos usam os mesmos dados sintéticos. A diferença deve estar no
# MAGIC layout visual. O laboratório não altera o array de dados para harmonizar a
# MAGIC aparência.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Desfazer e restaurar

# COMMAND ----------

rascunho.undo()
assert rascunho.current.content_sha256 == hash_antes
assert not rascunho.dirty

rascunho.apply_updates({"brand.primary": "#0066CC"})
rascunho.restore()
assert rascunho.current.content_sha256 == rascunho.base.content_sha256

print("Desfazer/restaurar conferidos sem publicação.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Abrir a interface ipywidgets
# MAGIC
# MAGIC Esta célula **constrói** a UI e o `display` abaixo a mostra. Estado de ipywidgets
# MAGIC não é promessa de persistência entre sessões; reexecute estas células ao abrir
# MAGIC outra sessão.

# COMMAND ----------

ui = build_ipywidgets_lab(rascunho)
display(ui.root)

# COMMAND ----------
# MAGIC %md
# MAGIC O botão **Salvar proposta** fica desabilitado porque nenhum `save_root` foi
# MAGIC informado. Isso evita transformar uma pasta implícita em destino autorizado.
# MAGIC Submeter e Publicar também ficam desabilitados nesta sprint.
# MAGIC
# MAGIC Para um laboratório autorizado com pasta de rascunhos, o mantenedor pode criar
# MAGIC a UI com `build_ipywidgets_lab(rascunho, save_root="<pasta-autorizada>")`.
# MAGIC A função apenas cria um JSON novo e se recusa a sobrescrever arquivo existente.
# MAGIC Ela não publica no Databricks.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Exportar JSON em memória

# COMMAND ----------

payload = rascunho.export_bytes()
print(payload.decode("utf-8")[:500])
print("bytes:", len(payload))
print("A saída acima é um rascunho em memória; nenhum arquivo foi criado.")
