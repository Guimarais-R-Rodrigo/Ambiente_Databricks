# Databricks notebook source
# MAGIC %md
# MAGIC # Conferir temas — exemplo sintético
# MAGIC Leia o [guia do objeto](README.md) antes de executar. Sem instalação, consultas, tabelas, gráficos ou arquivos gravados. A validação exige as bibliotecas declaradas e não homologa Databricks.

# COMMAND ----------
from pathlib import Path
import sys

# Preencha somente se a descoberta local não encontrar a pasta do Hub.
HUB_ROOT = ""
_start = Path(__file__).absolute().parent if "__file__" in globals() else Path.cwd()
_candidates = [Path(HUB_ROOT)] if HUB_ROOT else [
    candidate for parent in [_start, *_start.parents]
    for candidate in (parent, parent / ".assistant", parent / "ambiente_fonte/.assistant")
]
_root = next((p for p in _candidates if (p / "hub_snippets/visual/tema/tema.py").is_file()), None)
if _root is None:
    raise RuntimeError("Preencha HUB_ROOT com a pasta .assistant recebida do mantenedor; consulte README.md.")
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
from hub_snippets.visual.tema import load_reference_theme, resolve_theme, export_theme, ThemeError

# COMMAND ----------
# MAGIC %md
# MAGIC ## Referência
# MAGIC Espere notebook, 48 tokens e #005CA9. Os avisos não autorizam publicação.

# COMMAND ----------
referencia = load_reference_theme("notebook")
print(referencia.context, len(referencia.tokens), referencia.tokens["brand.primary"])
print(referencia.warnings)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Cópia e exportação
# MAGIC Alterar a cópia não muda o original. Exportar só devolve bytes em memória.

# COMMAND ----------
proposta = referencia.to_dict()
proposta["tokens"]["brand.primary"] = "#112233"
conferida = resolve_theme(proposta, expected_context="notebook")
print("Original:", referencia.tokens["brand.primary"], "Proposta:", conferida.tokens["brand.primary"])
exportada = export_theme(conferida)
reimportada = resolve_theme(exportada)
print("Mesmo conteúdo:", conferida.fingerprint == reimportada.fingerprint)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Erro esperado
# MAGIC A configuração incompleta é recusada. Não há substituição pelo legado.

# COMMAND ----------
incompleta = referencia.to_dict()
del incompleta["tokens"]["brand.primary"]
try:
    resolve_theme(incompleta)
except ThemeError as erro:
    if erro.code != "SCHEMA_REQUIRED":
        raise
    print(erro.code, erro.field, erro.action)
else:
    raise AssertionError("A configuração incompleta deveria ter sido recusada.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Saída observada em Python local — 12/09/2026
# MAGIC Esta execução não certifica Databricks nem Windows.
# MAGIC ```text
# MAGIC notebook 48 #005CA9
# MAGIC ('CONTRATO_VALIDADO_NAO_APROVADO', 'APLICACAO_VISUAL_NAO_EXECUTADA')
# MAGIC Original: #005CA9 Proposta: #112233
# MAGIC Mesmo conteúdo: True
# MAGIC SCHEMA_REQUIRED $.tokens.brand.primary Preencha todos os campos; não há preenchimento automático.
# MAGIC ```
