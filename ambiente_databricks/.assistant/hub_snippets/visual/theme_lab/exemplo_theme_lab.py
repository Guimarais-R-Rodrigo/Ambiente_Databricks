# Databricks notebook source
# MAGIC %md
# MAGIC # Aparência do Hub — prévia pessoal
# MAGIC
# MAGIC Comece pelo [guia de primeiro uso](GUIA_PRIMEIRO_USO.md) e pelo
# MAGIC [README](README.md). Este notebook não consulta dados corporativos,
# MAGIC não treina modelos, não aprova e não publica temas. As referências
# MAGIC empacotadas abaixo são **demonstrações**, não temas operacionais aprovados.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Preparação do caminho — responsabilidade do mantenedor
# MAGIC
# MAGIC Substitua o placeholder na cópia autorizada. O operador final não deve
# MAGIC precisar editar cores, hashes ou JSON no código.

# COMMAND ----------
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if not (assistant_root / "hub_snippets").is_dir():
    raise FileNotFoundError("Peça ao mantenedor o notebook com o caminho autorizado preenchido.")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from hub_snippets.visual.theme_lab import (
    build_ipywidgets_lab,
    build_theme_lab_launcher,
    compare_preview,
    create_theme_lab_from_preset,
    get_control_specs,
    get_demo_presets,
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Escolher uma referência de demonstração e provar isolamento
# MAGIC
# MAGIC Esta célula exercita a API sem gravar arquivos. Reexecutá-la cria outro
# MAGIC rascunho; depois de começar a editar pelo painel, não use Executar tudo.

# COMMAND ----------
# V05_DEMO_BEGIN
presets = get_demo_presets()
print("presets demonstrativos:", [item.key for item in presets])
rascunho = create_theme_lab_from_preset(presets, "legado_notebook")
hash_base = rascunho.base.content_sha256
print("contexto:", rascunho.current.context)
print("alterado ao abrir:", rascunho.dirty)
cor_alternativa = rascunho.current.tokens["brand.accent"]
rascunho.apply_updates({"brand.primary": cor_alternativa, "section.title_px": 20})
print("cor aplicada:", rascunho.current.tokens["brand.primary"])
print("alterado após aplicar:", rascunho.dirty)
print("base preservada:", rascunho.base.content_sha256 == hash_base)
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
# MAGIC Saída sintética observada em Python; não é captura da interface Databricks:
# MAGIC
# MAGIC ```text
# MAGIC presets demonstrativos: ['legado_notebook', 'executivo_claro']
# MAGIC contexto: notebook
# MAGIC alterado ao abrir: False
# MAGIC cor aplicada: #F7941D
# MAGIC alterado após aplicar: True
# MAGIC base preservada: True
# MAGIC desfeito: True
# MAGIC restaurado: True
# MAGIC JSON somente em memória: True
# MAGIC ```
# MAGIC
# MAGIC `dirty` compara proposta e base. Nenhuma linha acima salva ou publica.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Conferir os campos
# MAGIC
# MAGIC Tipos e limites vêm do schema canônico. Cobertura de prévia é informada
# MAGIC separadamente: campo sem consumidor aparece desabilitado na interface.

# COMMAND ----------
for spec in get_control_specs(rascunho.current):
    if spec.primary:
        print(spec.label, "|", spec.unit, "|", spec.minimum, spec.maximum)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Editor de um rascunho já escolhido
# MAGIC
# MAGIC Esta rota é útil para manutenção/teste direto. Sem `save_root`, o botão de
# MAGIC salvamento do JSON avulso fica desabilitado.

# COMMAND ----------
ui = build_ipywidgets_lab(rascunho)
display(ui.root)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Entrada guiada recomendada para usuário iniciante
# MAGIC
# MAGIC O launcher oferece seleção de ponto de partida e, quando o mantenedor passa
# MAGIC uma pasta autorizada, salvamento/reabertura de **sessão rastreável**.
# MAGIC Aqui não informamos pasta para evitar escrita no exemplo.

# COMMAND ----------
launcher = build_theme_lab_launcher(render_initial=False)
display(launcher.root)

# COMMAND ----------
# MAGIC %md
# MAGIC Em uma cópia preparada pelo mantenedor, a chamada pode receber
# MAGIC `save_root=PASTA_AUTORIZADA`. Após escolher uma base e aplicar alterações,
# MAGIC o operador informa o nome da sessão e usa **Salvar sessão rastreável**.
# MAGIC Em nova execução, escolhe a sessão no dropdown e usa **Reabrir sessão**.
# MAGIC A base original, proposta, histórico e revisão são revalidados pelos hashes;
# MAGIC a proposta não vira silenciosamente uma nova base.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Comparação fora do painel
# MAGIC
# MAGIC Use esta célula se o frontend não desenhar as figuras embutidas. Ela usa o
# MAGIC mesmo rascunho em memória e os mesmos dados sintéticos.

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
# MAGIC ## 7. Conferir o ambiente de uso
# MAGIC
# MAGIC O [guia](GUIA_PRIMEIRO_USO.md) descreve fallback `dbutils.widgets`, salvamento, reabertura e erros. Confirme prévia, acessibilidade e permissões no destino. Testes Python não comprovam navegador Databricks, p95, ACL ou uso autônomo. Este notebook não submete, aprova, publica, recolore PNGs ou altera consumidores externos.
