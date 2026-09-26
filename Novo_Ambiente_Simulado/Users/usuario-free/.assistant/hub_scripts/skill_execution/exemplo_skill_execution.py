# Databricks notebook source
# MAGIC %md
# MAGIC # `skill_execution` — preflight L2 sem executar a EDA
# MAGIC
# MAGIC Este exemplo resolve o contrato piloto da EDA com contexto sintético. Ele
# MAGIC não lê dados, não executa Spark, não chama helpers analíticos e não escreve
# MAGIC no workspace.
# MAGIC
# MAGIC **Antes de usar:** veja o [README do objeto](README.md).

# COMMAND ----------

import json
import sys
from pathlib import Path


def _assistant_root_from_notebook_file() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".assistant":
            return parent
    raise RuntimeError("raiz .assistant não encontrada")


assistant_root = _assistant_root_from_notebook_file()
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from hub_scripts.skill_execution import run_preflight

skill_dir = assistant_root / "skills" / "hub-ml-eda-profissional"
context = {
    "local_sample_required": True,
    "tabular_preview_required": True,
    "numeric_columns": 4,
    "numeric_distributions_requested": True,
    "resolved_theme_selected": False,
    "visual_diagnostics_requested": True,
}

result = run_preflight(
    skill_dir / "execution_contract.json",
    assistant_root=assistant_root,
    context=context,
)

print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
assert result.status == "PASS"
assert result.writes_performed is False

# COMMAND ----------
# MAGIC %md
# MAGIC ## Invariantes já reproduzidos pela suíte SE02
# MAGIC
# MAGIC O happy path automatizado executado no GitHub Actions confirmou estes
# MAGIC invariantes. Este bloco não é uma captura do Databricks Free; a homologação
# MAGIC remota permanece um gate separado da sprint.
# MAGIC
# MAGIC ```text
# MAGIC status=PASS
# MAGIC blocking_issues=0
# MAGIC writes_performed=False
# MAGIC ```
