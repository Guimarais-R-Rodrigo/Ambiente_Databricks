# Databricks notebook source
# MAGIC %md
# MAGIC # Smoke test serverless — helpers `x_snippets`/`x_scripts`
# MAGIC
# MAGIC Gate da fase 3 (herdado da auditoria do Codex): executar os helpers no
# MAGIC runtime Databricks real, com **dados sintéticos**. O resultado sai como
# MAGIC JSON via `dbutils.notebook.exit` para leitura pelo job submitter.

# COMMAND ----------

import datetime
import importlib
import json
import pkgutil
import random
import sys
import traceback

# O notebook roda em qualquer workspace: por padrão usa a pasta .assistant do
# usuário logado. No workspace do trabalho não há CLI — executar pela UI, e
# ajustar o widget apenas se a biblioteca estiver em outro caminho.
dbutils.widgets.text("assistant_root", "", "Caminho da pasta .assistant (vazio = usuário logado)")

ASSISTANT_ROOT = dbutils.widgets.get("assistant_root").strip()
if not ASSISTANT_ROOT:
    current_user = spark.sql("SELECT current_user()").first()[0]
    ASSISTANT_ROOT = f"/Workspace/Users/{current_user}/.assistant"

print(f"Biblioteca sob teste: {ASSISTANT_ROOT}")
sys.path.insert(0, ASSISTANT_ROOT)

# Dependências declaradas como opcionais no ecossistema (requirements-optional).
OPTIONAL_PKGS = {
    "lightgbm", "xgboost", "catboost", "optuna", "shap", "umap", "prophet",
    "lifelines", "torch", "pytorch_tabnet", "statsmodels",
}

results = {}


def run_case(name, fn):
    try:
        fn()
        results[name] = {"status": "PASS"}
    except ModuleNotFoundError as exc:
        status = "OPTIONAL_MISSING" if exc.name in OPTIONAL_PKGS else "FAIL"
        results[name] = {"status": status, "error": f"{type(exc).__name__}: {exc}"}
    except Exception as exc:
        results[name] = {
            "status": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
            "trace": traceback.format_exc(limit=2),
        }

# COMMAND ----------
# MAGIC %md ## 1. Import de todos os módulos

# COMMAND ----------

import x_snippets  # noqa: E402

for module_info in pkgutil.walk_packages(x_snippets.__path__, prefix="x_snippets."):
    run_case(
        f"import:{module_info.name}",
        lambda name=module_info.name: importlib.import_module(name),
    )

for script in [
    "data_quality_check", "doc_coverage", "drift_detector", "naming_checker",
    "quick_profile", "rfv_calculator", "schema_to_yaml",
]:
    run_case(
        f"import:x_scripts.{script}",
        lambda name=script: importlib.import_module(f"x_scripts.{name}"),
    )

# COMMAND ----------
# MAGIC %md ## 2. Dados sintéticos

# COMMAND ----------

from pyspark.sql import functions as F  # noqa: E402

random.seed(42)
base_date = datetime.date(2026, 1, 1)
rows = []
for i in range(400):
    day = base_date + datetime.timedelta(days=random.randint(0, 180))
    rows.append((
        i,
        f"c{i % 40:03d}",
        day,
        round(random.uniform(10, 500), 2),
        random.choice(["A", "B", "C"]),
        "2026-S1" if day < datetime.date(2026, 4, 1) else "2026-S2",
    ))

df = spark.createDataFrame(
    rows,
    "tx_id long, cliente_id string, data date, valor double, categoria string, safra string",
)
df_nulls = df.withColumn(
    "valor", F.when(F.col("tx_id") % 10 == 0, None).otherwise(F.col("valor"))
)
df_nulls.createOrReplaceTempView("vw_smoke_tx")
print(f"base sintética: {df.count()} linhas")

# COMMAND ----------
# MAGIC %md ## 3. Testes funcionais — x_snippets.spark

# COMMAND ----------

def t_null_summary():
    from x_snippets.spark.null_summary import null_summary
    out = null_summary(df_nulls).collect()
    assert len(out) > 0


def t_smart_sample():
    from x_snippets.spark.smart_sample import smart_sample
    sampled = smart_sample(df, n=60, stratify_col="categoria")
    assert 0 < sampled.count() <= 60


def t_date_features():
    from x_snippets.spark.date_features import extrair_features_data
    out = extrair_features_data(df, "data", holiday_dates=["2026-04-21"])
    assert len(out.columns) > len(df.columns)


def t_psi():
    from x_snippets.spark.psi_calculator import calcular_psi, interpretar_psi
    df_base = df.filter(F.col("safra") == "2026-S1")
    df_atual = df.filter(F.col("safra") == "2026-S2")
    psi = calcular_psi(df_base, df_atual, "valor")
    assert psi >= 0
    interpretar_psi(psi)
    interpretar_psi(psi, warning_threshold=0.1, critical_threshold=0.25)


def t_safe_display():
    from x_snippets.spark.safe_display import safe_display
    safe_display(df, limit=5, display_fn=lambda d: d.show(3))


for case in [t_null_summary, t_smart_sample, t_date_features, t_psi, t_safe_display]:
    run_case(f"func:{case.__name__[2:]}", case)

# COMMAND ----------
# MAGIC %md ## 4. Testes funcionais — x_scripts

# COMMAND ----------

def t_quick_profile():
    from x_scripts.quick_profile import quick_profile
    out = quick_profile("vw_smoke_tx", sample_fraction=1.0)
    assert out["row_count"] if "row_count" in out else out


def t_data_quality_check():
    from x_scripts.data_quality_check import data_quality_check
    data_quality_check("vw_smoke_tx", ["tx_id"], "data")


def t_rfv_calculator():
    from x_scripts.rfv_calculator import rfv_calculator
    out = rfv_calculator(
        "vw_smoke_tx", "cliente_id", "data", "valor", "2026-05-31"
    )
    assert out.count() > 0


def t_drift_detector():
    from x_scripts.drift_detector import drift_detector
    drift_detector("vw_smoke_tx", "safra", "2026-S1", "2026-S2", cols=["valor"])


def t_schema_to_yaml():
    from x_scripts.schema_to_yaml import schema_to_dict, schema_to_yaml
    payload = schema_to_dict("vw_smoke_tx", include_stats=True)
    assert payload["columns"]
    schema_to_yaml("vw_smoke_tx")


for case in [
    t_quick_profile, t_data_quality_check, t_rfv_calculator,
    t_drift_detector, t_schema_to_yaml,
]:
    run_case(f"func:{case.__name__[2:]}", case)

# COMMAND ----------
# MAGIC %md ## 5. Driver-side — constants e visual

# COMMAND ----------

def t_format_br():
    from x_snippets.constants.format_br import fmt_brl, fmt_int, fmt_pct
    assert fmt_int(3375674) == "3.375.674"
    fmt_brl(12345.67)
    fmt_pct(0.928)


def t_theme_plotly():
    importlib.import_module("x_snippets.visual.theme_plotly")


run_case("func:format_br", t_format_br)
run_case("func:theme_plotly", t_theme_plotly)

# COMMAND ----------
# MAGIC %md ## 6. Sumário

# COMMAND ----------

summary = {
    "total": len(results),
    "pass": sum(1 for r in results.values() if r["status"] == "PASS"),
    "fail": sum(1 for r in results.values() if r["status"] == "FAIL"),
    "optional_missing": sum(
        1 for r in results.values() if r["status"] == "OPTIONAL_MISSING"
    ),
    "runtime": f"serverless (spark {spark.version})",
    "results": results,
}
print(json.dumps(summary, indent=2, ensure_ascii=False)[:8000])
dbutils.notebook.exit(json.dumps(summary, ensure_ascii=False))
