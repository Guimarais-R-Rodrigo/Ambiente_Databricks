# Databricks notebook source
# MAGIC %md
# MAGIC # Aparência do Hub — prévia pessoal V05
# MAGIC
# MAGIC Comece pelo [guia de primeiro uso](GUIA_PRIMEIRO_USO.md) e pelo
# MAGIC [README](README.md). Este notebook não consulta dados corporativos,
# MAGIC não treina modelos e não publica. O exemplo usa referência sintética.
# MAGIC O mantenedor precisa preparar caminho e dependências antes da entrega.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Preparação do caminho — responsabilidade do mantenedor
# MAGIC
# MAGIC Substitua o placeholder uma única vez na cópia autorizada do notebook.
# MAGIC Não há consulta SQL para descobrir usuário e nenhuma instalação automática.
# MAGIC O operador final não precisa editar cor nem JSON no código.
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Ambiente | notebook Python com o pacote completo do Hub |
# MAGIC | Dependências | validação: jsonschema/referencing; galeria: pandas/Plotly/Jinja2; painel: ipywidgets/IPython |
# MAGIC | Dados | sintéticos, em memória |
# MAGIC | Escrita | apenas clique Salvar com pasta autorizada; esta demonstração não define pasta |
# MAGIC | Publicação | inexistente nesta sprint |

# COMMAND ----------
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if not (assistant_root / "hub_snippets").is_dir():
    raise FileNotFoundError("Peça ao mantenedor o notebook com o caminho autorizado preenchido.")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_lab import (
    build_ipywidgets_lab, compare_preview, create_theme_lab, get_control_specs,
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Criar, experimentar e restaurar sem gravar
# MAGIC
# MAGIC Execute a célula inteira. Ela demonstra as operações usando somente valores
# MAGIC já presentes no tema de referência, sem introduzir outro contrato de entrada.
# MAGIC Reexecutá-la cria outro rascunho: não a use para atualizar o painel.

# COMMAND ----------
# V05_DEMO_BEGIN
referencia = load_reference_theme("notebook")
rascunho = create_theme_lab(referencia)
hash_base = referencia.content_sha256
print("contexto:", rascunho.current.context)
print("alterado ao abrir:", rascunho.dirty)
cor_alternativa = rascunho.current.tokens["brand.accent"]
rascunho.apply_updates({"brand.primary": cor_alternativa, "section.title_px": 20})
print("cor aplicada:", rascunho.current.tokens["brand.primary"])
print("alterado após aplicar:", rascunho.dirty)
print("referência preservada:", referencia.content_sha256 == hash_base)
rascunho.undo()
print("desfeito:", rascunho.current.content_sha256 == hash_base)
rascunho.apply_updates({"section.title_px": 20})
rascunho.restore()
print("restaurado:", rascunho.current.content_sha256 == hash_base)
payload = rascunho.export_bytes()
print("JSON somente em memória:", isinstance(payload, bytes))
# V05_DEMO_END

# COMMAND ----------
# MAGIC %md
# MAGIC Saída da célula acima, executada em Python local em 13/09/2026 com o
# MAGIC núcleo V02 e o módulo V05 desta revisão; não é captura do Databricks:
# MAGIC
# MAGIC ```text
# MAGIC contexto: notebook
# MAGIC alterado ao abrir: False
# MAGIC cor aplicada: #F7941D
# MAGIC alterado após aplicar: True
# MAGIC referência preservada: True
# MAGIC desfeito: True
# MAGIC restaurado: True
# MAGIC JSON somente em memória: True
# MAGIC ```
# MAGIC
# MAGIC O JSON não é aprovação. `dirty` compara a proposta com a referência; não
# MAGIC significa que existe um arquivo salvo. O histórico fica apenas nesta sessão.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Conferir os campos antes de abrir a interface
# MAGIC
# MAGIC O contrato controla tipos e limites. Cobertura de prévia é informada à parte:
# MAGIC campo sem componente na galeria aparece desabilitado, não como botão sem efeito.

# COMMAND ----------
for spec in get_control_specs(rascunho.current):
    if spec.primary:
        print(spec.label, "|", spec.unit, "|", spec.minimum, spec.maximum)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Abrir o painel
# MAGIC
# MAGIC Depois desta célula, use os botões do painel, não Executar tudo.
# MAGIC A mensagem inicial deve dizer prévia pessoal. Sem `save_root`, Salvar fica
# MAGIC desabilitado. Reabrir sessão exige preparar outro painel; não promete recuperar
# MAGIC o rascunho anterior. A compatibilidade visual precisa ser conferida no runtime.

# COMMAND ----------
ui = build_ipywidgets_lab(rascunho)
display(ui.root)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Comparação fora do painel
# MAGIC
# MAGIC Use esta célula se os controles aparecem, mas o frontend não desenha as
# MAGIC figuras dentro do painel. Os mesmos objetos são exibidos pelo notebook.
# MAGIC Não execute outra vez a criação do rascunho: isso perderia seu trabalho.

# COMMAND ----------
comparacao = compare_preview(rascunho)
for painel in (comparacao.current, comparacao.proposal):
    displayHTML(painel.header_html)
    displayHTML(painel.kpi_html)
    painel.bar_figure.show()
    painel.series_figure.show()
    painel.heatmap_figure.show()
    displayHTML(painel.table_html)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Sem ipywidgets, ou para salvar e reabrir
# MAGIC
# MAGIC O [guia](GUIA_PRIMEIRO_USO.md) contém a rota nativa `dbutils.widgets`,
# MAGIC a ordem das células de aplicação, recuperação pelo JSON e solução de erros.
# MAGIC O mantenedor habilita a pasta de rascunhos fora da fonte do Hub e confere
# MAGIC permissões. Salvar nunca significa submeter, aprovar ou publicar.
# MAGIC Não confunda o modo escuro da interface Databricks com um tema `dark`:
# MAGIC a galeria completa desta revisão é limitada a `light`.
