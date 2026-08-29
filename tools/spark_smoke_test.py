# Databricks notebook source
# MAGIC %md
# MAGIC # Smoke test serverless — helpers `hub_snippets`/`hub_scripts`
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
dbutils.widgets.dropdown("target_environment", "free", ["free", "work"], "Ambiente alvo")
dbutils.widgets.text("mlflow_experiment_path", "", "Experimento temporário (obrigatório no trabalho)")

ASSISTANT_ROOT = dbutils.widgets.get("assistant_root").strip()
TARGET_ENVIRONMENT = dbutils.widgets.get("target_environment").strip().lower()
MLFLOW_EXPERIMENT_PATH = dbutils.widgets.get("mlflow_experiment_path").strip()
if TARGET_ENVIRONMENT not in {"free", "work"}:
    raise ValueError("target_environment deve ser 'free' ou 'work'")
if not ASSISTANT_ROOT:
    current_user = spark.sql("SELECT current_user()").first()[0]
    ASSISTANT_ROOT = f"/Workspace/Users/{current_user}/.assistant"

print(f"Biblioteca sob teste: {ASSISTANT_ROOT}")
sys.path.insert(0, ASSISTANT_ROOT)

# Dependências declaradas como opcionais no ecossistema (requirements-optional).
OPTIONAL_PKGS = {
    "lightgbm", "xgboost", "catboost", "optuna", "shap", "umap", "prophet",
    "lifelines", "torch", "pytorch_tabnet", "statsmodels", "pmdarima",
    # Dependencias **escondidas**: nenhum modulo as importa no topo, e por isso
    # nenhuma analise de import as encontra. Quem as exige e a biblioteca de
    # terceiro, na chamada -- `DataFrame.to_markdown()` pede tabulate,
    # `DataFrame.style` pede jinja2. E a classe `exec` do catalogo de helpers.
    "tabulate", "jinja2",
}

results = {}


def run_case(name, fn):
    try:
        fn()
        results[name] = {"status": "PASS"}
    except ModuleNotFoundError as exc:
        status = "OPTIONAL_MISSING" if exc.name in OPTIONAL_PKGS else "FAIL"
        results[name] = {"status": status, "error": f"{type(exc).__name__}: {exc}"}
    except ImportError as exc:
        # `ImportError` sem `name` e o que o pandas levanta na dependencia
        # escondida: "Missing optional dependency 'tabulate'". Classificar como
        # FAIL diria que a biblioteca esta quebrada quando ela so precisa de
        # `%pip install`. O nome vem do texto porque nao vem do atributo.
        texto = str(exc).lower()
        achou = next((p for p in OPTIONAL_PKGS if p in texto), None)
        results[name] = {
            "status": "OPTIONAL_MISSING" if achou else "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
        }
    except Exception as exc:
        results[name] = {
            "status": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
            "trace": traceback.format_exc(limit=2),
        }

def run_case_bloqueado(name, fn, motivo, expected_exceptions, message_fragments):
    """Caso que **precisa** falhar, porque a plataforma o bloqueia.

    Existe por causa da regra que este projeto aprendeu na pele: *"foi testado"
    tem data de validade em ambiente gerenciado*. Um bloqueio documentado que
    deixa de existir é notícia tão relevante quanto um que aparece — e sem esta
    guarda a notícia chegaria como um `PASS` silencioso, ou nunca chegaria.

    Só passa quando classe **e** assinatura da mensagem correspondem ao bloqueio
    conhecido. Outra exceção é falha do teste ou do helper, não evidência de que a
    plataforma continua bloqueando.
    """
    try:
        fn()
    except Exception as exc:  # noqa: BLE001
        class_ok = type(exc).__name__ in set(expected_exceptions)
        message_ok = any(fragment.lower() in str(exc).lower() for fragment in message_fragments)
        if not (class_ok and message_ok):
            results[name] = {
                "status": "FAIL",
                "error": f"bloqueio inesperado: {type(exc).__name__}: {str(exc)[:300]}",
                "expected_exceptions": list(expected_exceptions),
                "expected_message_fragments": list(message_fragments),
            }
            return
        results[name] = {"status": "BLOQUEADO_ESPERADO",
                         "motivo": motivo,
                         "error": f"{type(exc).__name__}: {str(exc)[:200]}"}
        return
    results[name] = {
        "status": "FAIL",
        "error": f"executou, e deveria estar bloqueado ({motivo}). "
                 "O runtime mudou: revise `.claude/rules/free-vs-trabalho.md`",
    }


# COMMAND ----------
# MAGIC %md ## 1. Import de todos os módulos

# COMMAND ----------

import hub_scripts  # noqa: E402
import hub_snippets  # noqa: E402

# Cópia deliberada da regra de tools/notebook_marker.py. O smoke test roda dentro
# do workspace, onde `tools/` não existe, então não há como importar a versão
# canônica. `validate_assistant.py` confere que as duas não divergiram.
MARCADOR_NOTEBOOK = "# Databricks notebook source"
_PREFIXOS_TOLERADOS = ("#!", "# -*-", "# coding", "# vim:")


def modulo_e_notebook(module_finder, nome, ispkg):
    """Um notebook de exemplo é submódulo importável — e importá-lo o executa.

    Com uma pasta por objeto, cada snippet tem ao lado um notebook didático que o
    `walk_packages` enumera. Importá-lo roda o notebook inteiro fora de contexto:
    `NameError: name 'spark' is not defined`, classificado como FAIL, para cada um
    deles.

    Pacote nunca é notebook: o arquivo dele é `__init__.py`, sem caminho de
    módulo resolvível. Na dúvida, importa — pular um pacote silenciaria justamente
    a API pública que os `__init__.py` passaram a declarar.
    """
    if ispkg:
        return False
    origem = getattr(module_finder, "path", None)
    if not origem:
        return False
    caminho = f"{origem}/{nome.rsplit('.', 1)[-1]}.py"
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            conteudo = arquivo.read(4096)
    except OSError:
        return False
    for linha in conteudo.lstrip("﻿").splitlines():
        despida = linha.strip()
        if not despida:
            continue
        if despida == MARCADOR_NOTEBOOK:
            return True
        if despida.startswith(_PREFIXOS_TOLERADOS):
            continue
        return False
    return False


notebooks_pulados = []
for pacote in (hub_snippets, hub_scripts):
    prefixo = f"{pacote.__name__}."
    for module_info in pkgutil.walk_packages(pacote.__path__, prefix=prefixo):
        if modulo_e_notebook(module_info.module_finder, module_info.name, module_info.ispkg):
            notebooks_pulados.append(module_info.name)
            continue
        run_case(
            f"import:{module_info.name}",
            lambda name=module_info.name: importlib.import_module(name),
        )

print(f"notebooks pulados no import: {len(notebooks_pulados)}")

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
# MAGIC %md ## 3. Testes funcionais — hub_snippets.spark

# COMMAND ----------

def t_null_summary():
    from hub_snippets.spark.null_summary import null_summary
    out = null_summary(df_nulls).collect()
    assert len(out) > 0


def t_smart_sample():
    from hub_snippets.spark.smart_sample import smart_sample
    sampled = smart_sample(df, n=60, stratify_col="categoria")
    assert sampled.count() == 60
    rare = spark.range(101).withColumn(
        "stratum", F.when(F.col("id") == 0, F.lit("rare")).otherwise(F.lit("common"))
    )
    rare_sample = smart_sample(rare, n=10, stratify_col="stratum")
    assert rare_sample.count() == 10
    assert rare_sample.filter(F.col("stratum") == "rare").count() == 1


def t_date_features():
    from hub_snippets.spark.date_features import extrair_features_data
    out = extrair_features_data(df, "data", holiday_dates=["2026-04-21"])
    assert len(out.columns) > len(df.columns)


def t_psi():
    from hub_snippets.spark.psi_calculator import calcular_psi, interpretar_psi
    df_base = df.filter(F.col("safra") == "2026-S1")
    df_atual = df.filter(F.col("safra") == "2026-S2")
    psi = calcular_psi(df_base, df_atual, "valor")
    assert psi >= 0
    interpretar_psi(psi)
    interpretar_psi(psi, warning_threshold=0.1, critical_threshold=0.25)


def t_safe_display():
    from hub_snippets.spark.safe_display import safe_display
    safe_display(df, limit=5, display_fn=lambda d: d.show(3))



def t_join_diagnostics():
    from hub_snippets.spark.join_diagnostics import diagnosticar_join
    from hub_snippets.testing import fixtures
    esq = fixtures.base_tabular(n=200, seed=1)
    dir_ = fixtures.base_tabular(n=200, seed=1, n_entidades=100).select("id_cliente", "uf")
    d = diagnosticar_join(esq, dir_, "id_cliente")
    # As chaves são contrato: renomeá-las sem propagar já quebrou notebook antes.
    for chave in ("linhas_esquerda", "cobertura_pct_chaves_validas",
                  "expansao_prevista_left", "expansao_prevista_inner",
                  "multiplicidade_max_direita", "linhas_descartadas_chave_nula"):
        assert chave in d, f"chave ausente no retorno: {chave}"
    assert d["linhas_esquerda"] == 200


def t_pit_join():
    from hub_snippets.spark.pit_join import pit_join
    from hub_snippets.testing import fixtures
    fatos, feats = fixtures.fatos_e_features(n_decisoes=100, seed=3)
    resultado, diag = pit_join(
        fatos, feats, chave="id_cliente",
        ts_decisao="dt_decisao", ts_feature="dt_referencia",
        atraso_publicacao_dias=3,
    )
    for chave in ("linhas_fato", "cobertura_pct_linhas_validas",
                  "sem_feature_disponivel_na_data", "atraso_publicacao_dias"):
        assert chave in diag, f"chave ausente no diagnóstico: {chave}"
    assert (
        diag["com_feature"]
        + diag["sem_chave_ou_data"]
        + diag["entidade_sem_historico"]
        + diag["sem_feature_disponivel_na_data"]
        == diag["linhas_fato"]
    )
    # Nenhuma feature marcada como futura pode ter atravessado o join.
    assert resultado.filter("eh_futura = true").count() == 0


for case in [
    t_null_summary, t_smart_sample, t_date_features, t_psi, t_safe_display,
    t_join_diagnostics, t_pit_join,
]:
    run_case(f"func:{case.__name__[2:]}", case)

# COMMAND ----------
# MAGIC %md ## 4. Testes funcionais — hub_scripts

# COMMAND ----------

def t_quick_profile():
    from hub_scripts.quick_profile import quick_profile
    out = quick_profile("vw_smoke_tx", sample_fraction=1.0)
    # Asserção de contrato: o nome da chave importa tanto quanto o valor.
    assert out["total_rows"] > 0
    assert out["sample_rows"] <= out["total_rows"]


def t_data_quality_check():
    from hub_scripts.data_quality_check import data_quality_check
    data_quality_check("vw_smoke_tx", ["tx_id"], "data")
    with_null_pk = df.limit(4).unionByName(
        df.limit(1).withColumn("tx_id", F.lit(None).cast("long"))
    )
    with_null_pk.createOrReplaceTempView("vw_smoke_null_pk")
    out = data_quality_check("vw_smoke_null_pk", ["tx_id"])
    assert out["status"] == "fail"
    assert out["checks"]["pk_uniqueness"]["null_key_rows"] == 1


def t_rfv_calculator():
    from hub_scripts.rfv_calculator import rfv_calculator
    out = rfv_calculator(
        "vw_smoke_tx", "cliente_id", "data", "valor", "2026-05-31"
    )
    assert out.count() > 0


def t_drift_detector():
    from hub_scripts.drift_detector import drift_detector
    drift_detector("vw_smoke_tx", "safra", "2026-S1", "2026-S2", cols=["valor"])
    numeric_cohort = spark.range(20).withColumn(
        "period", F.when(F.col("id") < 10, F.lit(1)).otherwise(F.lit(2))
    ).withColumn("value", F.col("id").cast("double"))
    numeric_cohort.createOrReplaceTempView("vw_smoke_numeric_cohort")
    detected = drift_detector("vw_smoke_numeric_cohort", "period", "1", "2")
    assert "period" not in detected


def t_schema_to_yaml():
    from hub_scripts.schema_to_yaml import schema_to_dict, schema_to_yaml
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
    from hub_snippets.constants.format_br import fmt_brl, fmt_int, fmt_pct
    assert fmt_int(3375674) == "3.375.674"
    fmt_brl(12345.67)
    fmt_pct(0.928)


def t_theme_plotly():
    importlib.import_module("hub_snippets.visual.theme_plotly")


run_case("func:format_br", t_format_br)
run_case("func:theme_plotly", t_theme_plotly)


# COMMAND ----------
# MAGIC %md ## 6. Testes funcionais — os 16 módulos de núcleo de `ml`
# MAGIC
# MAGIC Os notebooks destes dezesseis executaram uma vez, em 17/08/2026. Isto aqui
# MAGIC é outra coisa: a bateria **repetível**, que roda de novo antes de cada
# MAGIC replicação. A execução de uma vez prova que funcionou naquele dia; só a
# MAGIC bateria prova que continua funcionando.
# MAGIC
# MAGIC As chamadas saem dos notebooks que executaram com `SUCCESS` — invocação
# MAGIC provada vale mais que invocação deduzida da docstring, e foi lendo
# MAGIC docstring em vez de assinatura que nove notebooks desta biblioteca
# MAGIC nasceram quebrados.

# COMMAND ----------

import numpy as np  # noqa: E402
from hub_snippets.testing import fixtures  # noqa: E402


def _amostra_binaria(n=400, seed=7):
    """Rótulo e probabilidade correlacionados, para métrica não degenerar."""
    rng = np.random.default_rng(seed)
    y = rng.binomial(1, 0.2, n)
    p = np.clip(rng.normal(0.5, 0.2, n) + y * 0.3, 0.001, 0.999)
    return y, p


def t_split_temporal():
    from hub_snippets.ml.split_temporal import temporal_split
    # Trabalha em **pandas**, não em Spark: o módulo chama `df.copy()`, que o
    # Spark Connect não expõe. O notebook do objeto avisa disso em caixa alta, e
    # a primeira versão deste teste ignorou o aviso e passou um DataFrame Spark.
    painel = fixtures.serie_temporal(n_entidades=10, n_periodos=24, seed=1).toPandas()
    tr, va, te = temporal_split(painel, date_col="dt_referencia")
    assert len(tr) + len(va) + len(te) <= len(painel)
    assert len(tr) > 0 and len(te) > 0


def t_walk_forward():
    from hub_snippets.ml.walk_forward import walk_forward_cv
    painel = fixtures.serie_temporal(n_entidades=5, n_periodos=24, seed=2).toPandas()
    painel = painel.rename(columns={"dt_referencia": "dt", "valor": "y"})

    def modelo(treino, teste):
        return {"mae": float(abs(teste["y"].mean() - treino["y"].mean()))}

    dobras = walk_forward_cv(painel, date_col="dt", target_col="y",
                             model_fn=modelo, min_train_periods=6,
                             test_periods=1, step=1, gap=0)
    assert len(dobras) > 0


def t_woe_iv_calculator():
    from hub_snippets.ml.woe_iv_calculator import calculate_woe_iv, classify_iv
    base = fixtures.base_tabular(n=600, seed=3)
    tabela, iv = calculate_woe_iv(base, feature_col="uf", target_col="alvo")
    assert iv >= 0
    assert isinstance(classify_iv(iv), str)


def t_drift_detection():
    from hub_snippets.ml.drift_detection import (
        calculate_csi, calculate_ks, calculate_psi, detect_drift_all_features,
    )
    rng = np.random.default_rng(11)
    ref, atual = rng.normal(0, 1, 500), rng.normal(0.4, 1, 500)
    assert calculate_psi(ref, atual) > 0
    ks = calculate_ks(ref, atual)
    # Contrato registrado na auditoria da Sprint 7: devolve tupla, não número.
    assert isinstance(ks, tuple)
    import pandas as pd
    cat_ref = pd.Series(["a"] * 60 + ["b"] * 40)
    cat_atual = pd.Series(["a"] * 40 + ["b"] * 60)
    assert calculate_csi(cat_ref, cat_atual) > 0
    base_ref = fixtures.base_tabular(n=400, seed=4).toPandas()
    base_at = fixtures.base_tabular(n=400, seed=5).toPandas()
    out = detect_drift_all_features(
        base_ref, base_at, feature_cols=["renda", "uf"],
        numeric_cols=["renda"], categorical_cols=["uf"],
    )
    assert len(out) > 0


def t_metrics_report():
    from hub_snippets.ml.metrics_report import (
        calculate_binary_metrics, calculate_regression_metrics,
    )
    y, p = _amostra_binaria()
    m = calculate_binary_metrics(y, p)
    # O nome da chave é contrato: quem consome quebra sem erro de import.
    for chave in ("auc_roc", "ks_pct", "gini", "lift_10pct", "prevalence"):
        assert chave in m, f"chave ausente: {chave}"
    calculate_regression_metrics(np.arange(50.0), np.arange(50.0) + 0.5)


def t_curves_plotly():
    from hub_snippets.ml.curves_plotly import (
        plot_ks_curve, plot_lift_curve, plot_pr_curve, plot_roc_curve,
    )
    y, p = _amostra_binaria()
    for f in (plot_roc_curve, plot_pr_curve, plot_lift_curve, plot_ks_curve):
        assert f(y, p) is not None
    try:
        plot_lift_curve(np.zeros(10), np.linspace(0.1, 0.9, 10))
        raise AssertionError("lift deveria rejeitar target de classe única")
    except ValueError as exc:
        assert "both classes" in str(exc)


def t_score_bands():
    from hub_snippets.ml.score_bands import generate_score_bands
    y, p = _amostra_binaria()
    faixas = generate_score_bands(p * 1000, y, n_bands=5, higher_score_is_better=True)
    assert len(faixas) > 0
    try:
        generate_score_bands(np.ones(4), np.array([0, 1, 0, 1]))
        raise AssertionError("bandas deveriam rejeitar score constante")
    except ValueError as exc:
        assert "must vary" in str(exc)


def t_scorecard_builder():
    from hub_snippets.ml.scorecard_builder import build_scorecard
    from hub_snippets.ml.woe_iv_calculator import calculate_woe_iv
    base = fixtures.base_tabular(n=600, seed=6)
    tabela, _ = calculate_woe_iv(base, feature_col="uf", target_col="alvo")
    # **A costura entre os dois módulos, e ela não é automática.**
    # `calculate_woe_iv` devolve um DataFrame **Spark** cuja coluna de faixa se
    # chama como a feature; `build_scorecard` quer **pandas** com as colunas
    # `faixa` e `woe`. Os dois passam sozinhos, e o notebook do scorecard monta a
    # tabela à mão -- então a junção nunca tinha sido exercitada por ninguém.
    # Estas duas linhas são a ponte, e existem aqui para que ela não quebre em
    # silêncio.
    ponte = tabela.toPandas().rename(columns={"uf": "faixa"})[["faixa", "woe"]]
    # `coefs` é **array na ordem de `feature_names`**, não dicionário. A auditoria
    # da Sprint 7 registrou exatamente esta confusão num notebook; a primeira
    # versão deste teste a repetiu.
    out = build_scorecard(
        coefs=np.array([-0.45]), intercept=-2.1, feature_names=["uf"],
        woe_tables={"uf": ponte}, pdo=20, base_score=600, base_odds=50,
    )
    assert len(out) > 0
    try:
        build_scorecard(
            coefs=np.array([np.inf]), intercept=-2.1, feature_names=["uf"],
            woe_tables={"uf": ponte},
        )
        raise AssertionError("scorecard deveria rejeitar coeficiente infinito")
    except ValueError as exc:
        assert "finite" in str(exc)


def t_clustering_suite():
    from hub_snippets.ml.clustering_suite import run_clustering_pipeline, select_k
    rng = np.random.default_rng(8)
    pontos = np.vstack([rng.normal(m, 0.5, (80, 2)) for m in (0, 5, 10)])
    assert select_k(pontos, k_range=range(2, 6), method="silhouette") is not None
    base = fixtures.base_tabular(n=300, seed=9).toPandas()
    base = base.dropna(subset=["renda"])
    base["f2"] = base["renda"] * 0.5
    assert run_clustering_pipeline(base, feature_cols=["renda", "f2"], k=3,
                                   scaler="standard", log_mlflow=False) is not None


def t_isolation_forest():
    from hub_snippets.ml.isolation_forest import profile_anomalies, train_isolation_forest
    base = fixtures.base_tabular(n=300, seed=10).toPandas().dropna(subset=["renda"])
    base["b"] = base["renda"] * 0.3
    base["c"] = base["renda"] * -0.2
    saida = train_isolation_forest(base, feature_cols=["renda", "b", "c"],
                                   contamination=0.02, log_mlflow=False)
    assert saida is not None


def t_cluster_profiling():
    from hub_snippets.ml.cluster_profiling import profile_clusters, top_differentiators
    base = fixtures.base_tabular(n=300, seed=12).toPandas().dropna(subset=["renda"])
    base["idade"] = (base["renda"] / 1000).astype(int)
    base["cluster"] = base.index % 3
    perfis = profile_clusters(base, feature_cols=["renda", "idade"], cluster_col="cluster")
    assert len(perfis) > 0
    assert top_differentiators(perfis, cluster_id=0, top_n=2) is not None


def t_lgbm_temporal():
    from hub_snippets.ml.lgbm_temporal import create_temporal_features
    painel = fixtures.serie_temporal(n_entidades=5, n_periodos=24, seed=13).toPandas()
    painel = painel.rename(columns={"dt_referencia": "dt", "id_entidade": "id"})
    com_id = create_temporal_features(painel, target_col="valor", date_col="dt",
                                      lags=[1], rolling_windows=[3], entity_cols=["id"])
    sem_id = create_temporal_features(painel, target_col="valor", date_col="dt",
                                      lags=[1], rolling_windows=[3])
    # O contrato que a auditoria da Sprint 7 fixou: o módulo termina em dropna(),
    # e ignorar a entidade descarta MENOS linhas porque mistura as séries.
    assert len(com_id) < len(sem_id)
    painel["aux_missing"] = 1.0
    painel.loc[painel.index[-1], "aux_missing"] = np.nan
    preservado = create_temporal_features(
        painel, target_col="valor", date_col="dt", lags=[1],
        rolling_windows=[], calendar_features=False, entity_cols=["id"],
    )
    assert preservado["aux_missing"].isna().sum() == 1
    try:
        create_temporal_features(
            painel, target_col="valor", date_col="dt", lags=[],
            rolling_windows=[1], calendar_features=False, entity_cols=["id"],
        )
        raise AssertionError("rolling window 1 deveria ser rejeitada")
    except ValueError as exc:
        assert ">= 2" in str(exc)


def t_performance_monitor():
    from hub_snippets.ml.performance_monitor import EXAMPLE_THRESHOLDS, PerformanceMonitor
    mon = PerformanceMonitor(baseline_metrics={"auc": 0.78},
                             model_name="smoke", policy=EXAMPLE_THRESHOLDS)
    mon.add_period("2026-01", {"auc": 0.77}, n_predictions=1000)
    mon.add_period("2026-02", {"auc": 0.60}, n_predictions=1000)
    assert mon.get_current_status() is not None
    assert mon.should_retrain() is not None
    mon.generate_report()


def t_vintage_analysis():
    from hub_snippets.ml.vintage_analysis import (
        build_vintage_table, compare_safras, plot_vintage_curves, plot_vintage_heatmap,
    )
    import pandas as pd
    painel = fixtures.safras(n_contratos=200, seed=14).toPandas()
    # A fixture entrega safra como `AAAAMM` e o MOB como inteiro; o módulo quer
    # duas colunas de data. `dt_referencia` é obrigatório mesmo com `mob_col`.
    painel["dt_orig"] = pd.to_datetime(painel["safra"], format="%Y%m")
    painel["dt_ref"] = painel["dt_orig"] + pd.to_timedelta(painel["mob"] * 30, unit="D")
    tabela = build_vintage_table(
        painel, contract_id="id_contrato", dt_originacao="dt_orig",
        dt_referencia="dt_ref", target="inadimplente", mob_col="mob",
    )
    assert len(tabela) > 0
    assert plot_vintage_curves(tabela) is not None
    assert plot_vintage_heatmap(tabela) is not None
    assert compare_safras(tabela) is not None
    gap = pd.DataFrame([
        {"c": "a", "o": "2024-01-01", "r": "2024-01-01", "y": 1, "mob": 0},
        {"c": "a", "o": "2024-01-01", "r": "2024-03-01", "y": 1, "mob": 2},
        {"c": "b", "o": "2024-01-01", "r": "2024-01-01", "y": 0, "mob": 0},
        {"c": "b", "o": "2024-01-01", "r": "2024-02-01", "y": 0, "mob": 1},
        {"c": "b", "o": "2024-01-01", "r": "2024-03-01", "y": 0, "mob": 2},
    ])
    gap_table = build_vintage_table(
        gap, "c", "o", "r", "y", mob_col="mob", target_is_cumulative=True,
    )
    middle = gap_table.loc[gap_table["mob"] == 1].iloc[0]
    assert pd.isna(middle["taxa_acumulada"])
    assert middle["cobertura_observada"] == 0.5


def t_explainability_report():
    import pandas as pd
    from hub_snippets.ml.explainability_report import (
        generate_executive_report, generate_technical_summary,
    )
    imp = pd.DataFrame({"feature": ["renda", "idade"],
                        "importance": [0.6, 0.4],
                        "pct_importance": [60.0, 40.0]})
    texto = generate_executive_report(
        imp, feature_business_names={"renda": "Renda", "idade": "Idade"},
        target_description="probabilidade de inadimplência",
        model_metric=0.78, metric_name="AUC",
    )
    assert isinstance(texto, str) and len(texto) > 0
    # A segunda chama `to_markdown()`, que exige `tabulate` — dependência
    # escondida, ausente no Free. `run_case` a classifica como opcional.
    generate_technical_summary(imp)


for case in [
    t_split_temporal, t_walk_forward, t_woe_iv_calculator, t_drift_detection,
    t_metrics_report, t_curves_plotly, t_score_bands, t_scorecard_builder,
    t_clustering_suite, t_isolation_forest, t_cluster_profiling, t_lgbm_temporal,
    t_performance_monitor, t_vintage_analysis, t_explainability_report,
]:
    run_case(f"ml:{case.__name__[2:]}", case)


def t_mlflow_start_free():
    """Prova somente a fronteira bloqueada e limpa qualquer run se ela mudar."""
    import mlflow

    run_id = None
    try:
        run = mlflow.start_run(run_name="hub-smoke-free-delete-me")
        run_id = run.info.run_id
    finally:
        if mlflow.active_run() is not None:
            mlflow.end_run(status="KILLED")
        if run_id is not None:
            mlflow.tracking.MlflowClient().delete_run(run_id)


def t_mlflow_run_work():
    """Executa o contrato completo e remove o run temporário ao terminar."""
    if not MLFLOW_EXPERIMENT_PATH:
        raise ValueError("mlflow_experiment_path é obrigatório no ambiente work")

    import mlflow
    import pandas as pd
    from sklearn.dummy import DummyClassifier
    from hub_snippets.ml.mlflow_run import run_governado

    x = pd.DataFrame({"x": [0.0, 1.0, 2.0, 3.0]})
    y = np.array([0, 0, 1, 1])
    model = DummyClassifier(strategy="prior").fit(x, y)
    run_id = None
    try:
        with run_governado(
            "hub-smoke-work-delete-me",
            dataset="synthetic:tools/spark_smoke_test.py",
            split="synthetic holdout not applicable",
            limitacoes=["teste temporário de integração; não é modelo de decisão"],
            experimento=MLFLOW_EXPERIMENT_PATH,
        ) as governed:
            active = mlflow.active_run()
            run_id = active.info.run_id if active is not None else None
            governed.parametros({"strategy": "prior"})
            governed.metricas({"accuracy_smoke": float(model.score(x, y))})
            governed.modelo(model, exemplo_entrada=x.head(2), nome="smoke_model")
    finally:
        if mlflow.active_run() is not None:
            mlflow.end_run(status="KILLED")
        if run_id is not None:
            mlflow.tracking.MlflowClient().delete_run(run_id)


if TARGET_ENVIRONMENT == "free":
    run_case_bloqueado(
        "ml:mlflow_start_free",
        t_mlflow_start_free,
        "MLflow start_run bloqueado no serverless (Spark Connect)",
        expected_exceptions=("AnalysisException",),
        message_fragments=("spark.mlflow.modelRegistryUri", "CONFIG_NOT_AVAILABLE"),
    )
else:
    run_case("ml:mlflow_run_work", t_mlflow_run_work)

# COMMAND ----------
# MAGIC %md ## 7. Sumário

# COMMAND ----------

summary = {
    "total": len(results),
    "pass": sum(1 for r in results.values() if r["status"] == "PASS"),
    "fail": sum(1 for r in results.values() if r["status"] == "FAIL"),
    "optional_missing": sum(
        1 for r in results.values() if r["status"] == "OPTIONAL_MISSING"
    ),
    "bloqueado_esperado": sum(
        1 for r in results.values() if r["status"] == "BLOQUEADO_ESPERADO"
    ),
    "target_environment": TARGET_ENVIRONMENT,
    "runtime": f"serverless (spark {spark.version})",
    "results": results,
}
print(json.dumps(summary, indent=2, ensure_ascii=False)[:8000])
dbutils.notebook.exit(json.dumps(summary, ensure_ascii=False))
