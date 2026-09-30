# Databricks notebook source
"""Synthetic runtime probe for the eight current skill candidates."""
from __future__ import annotations

import copy
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import sys
import traceback
import uuid
from pathlib import Path

MARKER = "SKILLS_DELIVERY_FREE_PROBE_V2"
SKILLS = {
    "safra": "hub-ml-analise-safra",
    "explainability": "hub-ml-explainability",
    "estatistica": "hub-ml-validacao-estatistica",
    "cross_eda": "hub-ml-cross-eda-ml",
    "cross_pit": "hub-ml-cross-eda-ml",
    "features": "hub-ml-feature-engineering",
    "feature_pit": "hub-ml-feature-engineering",
    "baseline": "hub-ml-baseline-ml",
    "monitoramento": "hub-ml-monitoramento-modelo",
    "monitor_performance": "hub-ml-monitoramento-modelo",
    "pipeline_spec": "hub-ml-pipeline-builder",
    "pipeline_execution": "hub-ml-pipeline-builder",
}
sys.dont_write_bytecode = True


def _widget_root() -> Path:
    dbutils.widgets.text("assistant_root", "", "Published .assistant path")
    value = dbutils.widgets.get("assistant_root").strip()
    if not value:
        raise ValueError("assistant_root widget is required")
    path = Path(value).resolve()
    if path.name != ".assistant" or not path.is_dir():
        raise ValueError("assistant_root must point to an existing .assistant directory")
    return path


def _module(root: Path, skill: str, script: str, label: str):
    path = root / "skills" / SKILLS[skill] / "scripts" / script
    spec = importlib.util.spec_from_file_location("probe_" + label, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("runner unavailable: " + label)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _versions():
    names = ("numpy", "pandas", "scipy", "scikit-learn", "shap", "pyspark", "jsonschema", "mlflow")
    result = {"python": sys.version.split()[0]}
    for name in names:
        try:
            result[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            # Managed runtimes can expose modules through another distribution
            # (for example mlflow-skinny or databricks-connect).
            module_name = {"scikit-learn": "sklearn"}.get(name, name)
            try:
                module = importlib.import_module(module_name)
                version = getattr(module, "__version__", "UNREPORTED")
                result[name] = "MODULE:" + str(version) + "; DISTRIBUTION_METADATA_ABSENT"
            except ImportError:
                result[name] = "IMPORT_UNAVAILABLE"
    return result


def _hashes(root: Path):
    """Hash union of all current release manifests and L2 specification gate."""
    paths = set()
    for skill in SKILLS.values():
        folder = root / "skills" / skill
        manifest = folder / "release_manifest.json"
        if manifest.is_file():
            paths.add(manifest)
            for artifact in json.loads(manifest.read_text(encoding="utf-8"))["artifacts"]:
                paths.add(root / artifact["path"])
    pipeline = root / "skills" / SKILLS["pipeline_spec"]
    paths.update(pipeline / relative for relative in
                 ("execution_contract.json", "input.schema.json", "scripts/preflight.py",
                  "templates/pipeline_spec.md"))
    paths.update(root / relative for relative in
                 ("hub_scripts/skill_execution/__init__.py",
                  "hub_scripts/skill_execution/skill_execution.py",
                  "hub_scripts/skill_execution/domain_context/__init__.py",
                  "hub_scripts/skill_execution/domain_context/release.py"))
    return {str(path.relative_to(root)).replace("\\", "/"): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(paths)}


def _record(name, run, verify, tamper):
    run_id = "free-probe-" + name + "-" + uuid.uuid4().hex
    payload = run(run_id)
    verdict = verify(payload, run_id)
    replay = verify(payload, run_id + "-replay")
    altered = copy.deepcopy(payload)
    tamper(altered)
    changed = verify(altered, run_id)
    ok = (payload.get("status") == "PASS" and isinstance(payload.get("receipt"), dict)
          and verdict.get("valid") is True and replay.get("valid") is False
          and changed.get("valid") is False)
    return {"ok": ok, "run_id": run_id, "status": payload.get("status"),
            "receipt_id": (payload.get("receipt") or {}).get("receipt_id"),
            "verification": verdict, "replay": replay, "tamper": changed,
            "blocking_issues": (payload.get("trace") or {}).get("blocking_issues", [])}


def _disable_autolog():
    # Synthetic sklearn fits must not create an MLflow run by ambient autologging.
    try:
        import mlflow
        mlflow.autolog(disable=True)
        mlflow.sklearn.autolog(disable=True)
        return "disabled"
    except ImportError:
        return "mlflow_absent"


def _safra(root):
    fixture = json.loads(r'''{"expected_table":[{"cobertura_observada":1.0,"mob":0,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":0,"safra":"2026-01","taxa":0.0,"taxa_acumulada":0.0},{"cobertura_observada":1.0,"mob":1,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-01","taxa":0.5,"taxa_acumulada":0.5},{"cobertura_observada":0.5,"mob":2,"n_contratos_observados":1,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-01","taxa":null,"taxa_acumulada":null},{"cobertura_observada":1.0,"mob":0,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-02","taxa":0.5,"taxa_acumulada":0.5},{"cobertura_observada":1.0,"mob":1,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-02","taxa":0.5,"taxa_acumulada":0.5}],"fixture_id":"VF-F01-CUMULATIVE","request":{"absence_policy":"MISSING_ROW_NOT_ZERO","cohort_roster":[{"id":"a1","originated_at":"2026-01-01T00:00:00Z"},{"id":"a2","originated_at":"2026-01-01T00:00:00Z"},{"id":"b1","originated_at":"2026-02-01T00:00:00Z"},{"id":"b2","originated_at":"2026-02-01T00:00:00Z"}],"cutoff":"2026-03-01T00:00:00Z","denominator":"MOB0_UNIQUE_IDS_FIXED_PER_COHORT","duplicate_policy":"REJECT","estimand":"BINARY_CUMULATIVE_INCIDENCE","max_mob":2,"periodicity":"MONTH","population_id":"synthetic-VF-F01-CUMULATIVE","profile":"MONTHLY_BINARY_PILOT_V1","requested_effect":"NONE","rows":[{"id":"a1","mob":0,"observed_at":"2026-01-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a2","mob":0,"observed_at":"2026-01-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a1","mob":1,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":1},{"id":"a2","mob":1,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a1","mob":2,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":1},{"id":"b1","mob":0,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":0},{"id":"b2","mob":0,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":1},{"id":"b1","mob":1,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":0},{"id":"b2","mob":1,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":1}],"schema_version":"SER03-REQUEST-1","semantic_mode":"CUMULATIVE","synthetic":true},"source":"B1_PREPARACAO_SER03_SER05 fixtures; monthly synthetic decisions only"}''')
    request, oracle = fixture["request"], fixture["expected_table"]
    runner = _module(root, "safra", "run.py", "safra_run")
    verifier = _module(root, "safra", "verify.py", "safra_verify")
    return _record("safra", lambda rid: runner.run(request, run_id=rid),
                   lambda p, rid: verifier.verify(p, expected_request=request,
                                                  expected_run_id=rid, expected_table=oracle),
                   lambda p: p["result"]["table"][0].__setitem__("n_eventos_acumulados", 99))


def _explainability(root):
    import numpy as np
    from sklearn.linear_model import LinearRegression
    request = json.loads(r'''{"schema_version":"SER02-EXPLAINABILITY-REQUEST-1","profile":"LINEAR_REGRESSION_SYNTHETIC_V1","synthetic":true,"requested_effect":"NONE","model":{"model_id":"synthetic-linear-1","model_type":"linear","task":"regression","estimator":"sklearn.LinearRegression","intercept":3,"coefficients":[2,-1]},"feature_names":["x1","x2"],"row_ids":["r1","r2"],"sample_ids":["r2"],"X":[[1,2],[2,1]],"background":[[0,0]]}''')
    X = np.asarray(request["X"], dtype=np.float64)
    background = np.asarray(request["background"], dtype=np.float64)
    model = LinearRegression().fit(np.array([[0, 0], [1, 0], [0, 1]], dtype=float),
                                   np.array([3, 5, 2], dtype=float))
    model.hub_model_id = request["model"]["model_id"]
    runner = _module(root, "explainability", "run.py", "ex_run")
    verifier = _module(root, "explainability", "verify.py", "ex_verify")
    return _record("explainability",
                   lambda rid: runner.run(request, model=model, X=X, background=background, run_id=rid),
                   lambda p, rid: verifier.verify(p, expected_request=request, expected_model=model,
                                                  expected_X=X, expected_background=background,
                                                  expected_run_id=rid),
                   lambda p: p["result"]["shap_values"][0].__setitem__(0, 999))


def _estatistica(root):
    request = json.loads(r'''{"schema_version":"SER04-REQUEST-1","profile":"TWO_SAMPLE_KS_PILOT_V1","synthetic":true,"population_id":"synthetic-ser04-ks-separated","unit":"one independent synthetic observation","question":"Do the two synthetic distributions differ?","hypothesis":"TWO_SIDED_DISTRIBUTION_DIFFERENCE","estimand":"MAX_ABSOLUTE_ECDF_DIFFERENCE","independence":"TWO_INDEPENDENT_IID_CONTINUOUS_SAMPLES_NO_TIES","multiple_testing":"ONE_PREREGISTERED_COMPARISON_NOT_APPLICABLE","alpha":0.05,"reference":[1,2,3,4],"comparison":[5,6,7,8],"requested_effect":"NONE"}''')
    runner = _module(root, "estatistica", "run.py", "stat_run")
    verifier = _module(root, "estatistica", "verify.py", "stat_verify")
    oracle_p = 2 / math.comb(8, 4)
    return _record("estatistica", lambda rid: runner.run(request, run_id=rid),
                   lambda p, rid: verifier.verify(p, expected_request=request, expected_run_id=rid,
                                                  expected_statistic=1.0, expected_p_value=oracle_p),
                   lambda p: p["result"].__setitem__("statistic_D", 0.5))


def _cross_eda(root, spark):
    from hub_scripts.skill_execution.domain_context import digest
    context = json.loads(r'''{"context":{"anchor":"anchor_snapshot","anchor_grain":"ONE_ROW_PER_ENTITY_DECISION","cardinality":"N:1","decision_at":"2026-01-10T00:00:00Z","entity_keys":["entity_id"],"not_applicable_reason":"Synthetic static attribute declared invariant over the decision period.","null_key_policy":"REJECT","pit":"NOT_APPLICABLE","profile":"CONTEXT_ONLY_PILOT_V1","requested_effect":"NONE","schema_version":"SER05-CONTEXT-1","sources":[{"columns":["entity_id","reference_at","available_at"],"content_sha256":"94444ab59ced9bdfee79fc8ec48536354243cc000436bb2f10e355228e48f056","grain":"ONE_ROW_PER_ENTITY_DECISION","id":"anchor_snapshot","snapshot_id":"anchor_snapshot_synthetic_v1"},{"columns":["entity_id","reference_at","available_at"],"content_sha256":"ee1e053a125aed64b6d65664727da742764683266b2c6a146d332737a88261ed","grain":"ENTITY_SNAPSHOT","id":"attributes_snapshot","snapshot_id":"attributes_snapshot_synthetic_v1"}],"synthetic":true,"temporal":null},"expected_context":{"context_status":"RESOLVED_FOR_L2","effect":"NONE","join_executed":false,"ml_readiness":"NOT_EVALUATED","pit":"NOT_APPLICABLE"},"fixture_id":"CE-F02-STATIC-CONTEXT","source_id_note":"Synthetic declared identifiers, not verification of source contents"}''')["context"]
    datasets = {
        "anchor_snapshot": [{"entity_id": "a", "value": 1},
                            {"entity_id": "b", "value": 2},
                            {"entity_id": "c", "value": 3}],
        "attributes_snapshot": [{"entity_id": "a", "flag": 1},
                                {"entity_id": "b", "flag": 0}],
    }
    for source in context["sources"]:
        rows = datasets[source["id"]]
        source["columns"] = list(rows[0])
        source["content_sha256"] = digest(rows)
    oracle = {
        "linhas_esquerda": 3, "linhas_direita": 2,
        "chaves_nulas_esquerda": 0, "chaves_nulas_direita": 0,
        "linhas_descartadas_chave_nula": 0, "linhas_com_match": 2,
        "linhas_sem_match_chave_valida": 1, "cobertura_pct_chaves_validas": 66.67,
        "multiplicidade_max_direita": 1, "multiplicidade_media_direita": 1.0,
        "relacao": "1:1 ou N:1 — join preserva a cardinalidade",
        "linhas_apos_join_left": 3, "linhas_apos_join_inner": 2,
        "expansao_prevista_left": 1.0, "expansao_prevista_inner": 0.667,
        "exemplos_sem_match": [{"entity_id": "c"}], "exemplos_chave_nula": [],
    }
    runner = _module(root, "cross_eda", "run_diagnostic.py", "cross_run")
    verifier = _module(root, "cross_eda", "verify_diagnostic.py", "cross_verify")
    return _record("cross_eda", lambda rid: runner.run(context, datasets, spark, run_id=rid),
                   lambda p, rid: verifier.verify(p, expected_context=context,
                                                  expected_datasets=datasets, expected_run_id=rid,
                                                  expected_diagnostic=oracle),
                   lambda p: p["result"]["diagnostic"].__setitem__("linhas_com_match", 3))


def _features(root):
    def row(rid, entity, day, value):
        return {"id": rid, "entity_id": entity, "event_at": f"2026-01-{day:02d}T00:00:00+00:00",
                "available_at": f"2026-01-{day + 1:02d}T00:00:00+00:00", "value": value}
    request = {"schema_version": "SER07-REQUEST-1", "profile": "FIXED_LAG_L1_V1",
               "synthetic": True, "population_id": "synthetic-panel-01",
               "decision_at": "2026-01-10T00:00:00+00:00", "window_days": 4,
               "requested_effect": "NONE",
               "temporal": {"reference_column": "event_at", "availability_column": "available_at",
                            "lag_kind": "CONSTANT", "lag_days": 1, "boundary": "LE",
                            "timezone": "UTC", "tie_break": "REJECT", "bitemporal": False},
               "rows": [row("a7", "A", 7, 1), row("a8", "A", 8, 2),
                        row("a10", "A", 10, 5), row("a11", "A", 11, 7),
                        row("b7", "B", 7, 10), row("b8", "B", 8, 20)]}
    oracle = [{"id": "a8", "entity_id": "A", "event_at": "2026-01-08", "lag_1": 1.0},
              {"id": "b8", "entity_id": "B", "event_at": "2026-01-08", "lag_1": 10.0}]
    runner = _module(root, "features", "run.py", "features_run")
    verifier = _module(root, "features", "verify.py", "features_verify")
    return _record("features", lambda rid: runner.run(request, run_id=rid),
                   lambda p, rid: verifier.verify(p, expected_request=request, expected_run_id=rid,
                                                  expected_features=oracle),
                   lambda p: p["result"]["features"][0].__setitem__("lag_1", 99))


def _baseline(root):
    request = {"schema_version": "SER09-REQUEST-1", "profile": "BINARY_TEMPORAL_LOCAL_V1",
               "synthetic": True, "requested_effect": "NONE", "population_id": "SYNTHETIC-P01",
               "target": "target", "positive_class": 1, "unit": "synthetic_entity",
               "date_column": "observed_at", "feature_order": ["feature"], "train_pct": 0.5,
               "val_pct": 0.25, "gap_periods": 0, "period_unit": "M", "threshold": 0.5, "seed": 17,
               "rows": [{"id": f"B{i:02d}", "observed_at": f"2024-{i:02d}-01T00:00:00Z",
                         "feature": float(i % 5), "target": i % 2} for i in range(1, 13)]}
    runner = _module(root, "baseline", "run.py", "baseline_run")
    verifier = _module(root, "baseline", "verify.py", "baseline_verify")
    return _record("baseline", lambda rid: runner.run(request, run_id=rid),
                   lambda p, rid: verifier.verify(p, expected_request=request, expected_run_id=rid),
                   lambda p: p["result"]["partitions"]["holdout"]["metrics"].__setitem__("auc_roc", 0.1234))


def _monitoramento(root):
    request = {"schema_version": "SER11-REQUEST-1", "profile": "DRIFT_NUMERIC_LOCAL_V1",
               "synthetic": True, "requested_effect": "NONE", "model_id": "SYNTH-M01",
               "model_version": "v1", "population_id": "SYNTHETIC-P01", "score_name": "score",
               "reference_start": "2025-01-01T00:00:00Z", "reference_end": "2025-01-31T23:59:59Z",
               "current_start": "2025-02-01T00:00:00Z", "current_end": "2025-02-28T23:59:59Z",
               "n_bins": 4, "eps": 1e-6,
               "reference": [{"id": f"R{i}", "observed_at": "2025-01-15T00:00:00Z", "score": value}
                             for i, value in enumerate((0.1, 0.1, 0.3, 0.6, 0.9, None))],
               "current": [{"id": f"C{i}", "observed_at": "2025-02-15T00:00:00Z", "score": value}
                           for i, value in enumerate((0.2, 0.5, 0.7, 0.7, 0.95, None))]}
    runner = _module(root, "monitoramento", "run.py", "monitor_run")
    verifier = _module(root, "monitoramento", "verify.py", "monitor_verify")
    return _record("monitoramento", lambda rid: runner.run(request, run_id=rid),
                   lambda p, rid: verifier.verify(p, expected_request=request, expected_run_id=rid),
                   lambda p: p["result"].__setitem__("psi", p["result"]["psi"] + 0.123456))


def _monitor_performance(root):
    def rows(prefix, observed, label_at, scores):
        return [{"id": f"{prefix}{i}", "observed_at": observed,
                 "label_available_at": label_at, "score": score,
                 "label": int(i >= 4)} for i, score in enumerate(scores)]
    request = {
        "schema_version": "SER12-REQUEST-1", "profile": "BINARY_MATURE_PERFORMANCE_V1",
        "synthetic": True, "requested_effect": "NONE", "model_id": "synthetic-model",
        "model_version": "v1", "population_id": "synthetic-population",
        "score_name": "score", "evaluation_at": "2025-03-10T00:00:00Z",
        "reference_start": "2025-01-01T00:00:00Z",
        "reference_end": "2025-01-31T23:59:59Z",
        "current_start": "2025-02-01T00:00:00Z",
        "current_end": "2025-02-28T23:59:59Z",
        "auc_thresholds": {"warning": 0.1, "critical": 0.2,
                           "direction": "higher", "delta": "absolute"},
        "reference": rows("R", "2025-01-15T00:00:00Z", "2025-02-05T00:00:00Z",
                          (.1, .2, .3, .4, .6, .7, .8, .9)),
        "current": rows("C", "2025-02-15T00:00:00Z", "2025-03-01T00:00:00Z",
                        (.1, .4, .6, .8, .2, .3, .5, .7)),
    }
    runner = _module(root, "monitor_performance", "run_performance.py",
                     "monitor_performance_run")
    verifier = _module(root, "monitor_performance", "verify_performance.py",
                       "monitor_performance_verify")
    run_id = "free-probe-monitor-performance-" + uuid.uuid4().hex
    payload = runner.run(request, run_id=run_id)
    raw = verifier.verify(payload, expected_request=request, expected_run_id=run_id)
    final = verifier.finalize(payload, expected_request=request, expected_run_id=run_id)
    checked = verifier.verify_finalized(final, expected_request=request, expected_run_id=run_id)
    replay = verifier.verify_finalized(final, expected_request=request,
                                       expected_run_id=run_id + "-replay")
    altered = copy.deepcopy(final)
    altered["handoff"]["model_id"] = "tampered-model"
    tamper = verifier.verify_finalized(altered, expected_request=request,
                                       expected_run_id=run_id)
    immature = copy.deepcopy(request)
    immature["current"][0]["label_available_at"] = "2025-03-11T00:00:00Z"
    blocked = runner.run(immature, run_id=run_id + "-immature")
    result = payload.get("result") or {}
    ok = (payload.get("status") == "PASS" and isinstance(payload.get("receipt"), dict)
          and raw["valid"] is True and payload["scope_completion_authorized"] is False
          and checked["valid"] is True and final["scope_completion_authorized"] is True
          and final["postflight"]["status"] == "PASS"
          and replay["valid"] is False and tamper["valid"] is False
          and result.get("monitor_status") == "🔴 Crítico"
          and result.get("investigation_decision") == "INVESTIGATE_RETRAINING_CANDIDATE"
          and result.get("automatic_retrain_authorized") is False
          and result.get("action_performed") is False
          and result.get("promotion_authorized") is False
          and blocked.get("status") == "BLOCKED" and blocked.get("receipt") is None
          and blocked.get("trace", {}).get("resources_called") == [])
    return {"ok": ok, "status": payload.get("status"), "receipt_id":
            (payload.get("receipt") or {}).get("receipt_id"),
            "raw_verification": raw, "postflight_status": final["postflight"]["status"],
            "scope_completion_authorized": final["scope_completion_authorized"],
            "final_verification": checked, "replay": replay, "tamper": tamper,
            "immature_label_status": blocked.get("status"),
            "immature_label_issues": blocked.get("trace", {}).get("blocking_issues", []),
            "auc_roc": result.get("metrics", {}).get("current", {}).get("auc_roc")}


def _pipeline_spec(root):
    request = {"schema_version": "SER13-SPEC-1", "synthetic": True,
               "operation": "VALIDATE_SPEC", "environment": "LOCAL_SYNTHETIC", "scope": "PERSONAL",
               "source": "synthetic_source", "destination": "synthetic_destination",
               "write_mode": "MERGE", "incremental": "WATERMARK", "primary_keys": ["id"],
               "columns": ["id", "event_at", "value"], "event_time": "event_at",
               "watermark_seconds": 60, "idempotency": "MERGE_ON_KEYS", "permissions": "UNKNOWN",
               "schedule": None, "rollback": "NOT_APPLICABLE_NO_EFFECT"}
    gate = _module(root, "pipeline_spec", "preflight.py", "pipeline_preflight")
    payload = gate.preflight(request)
    valid = gate.verify_preflight(payload, expected_request=request)
    changed_request = copy.deepcopy(request)
    changed_request["destination"] = "synthetic_other"
    replay = gate.verify_preflight(payload, expected_request=changed_request)
    altered = copy.deepcopy(payload)
    altered["effects_authorized"] = True
    tamper = gate.verify_preflight(altered, expected_request=request)
    ok = (payload["status"] == "PASS" and valid["valid"] is True
          and replay["valid"] is False and tamper["valid"] is False
          and payload["receipt"] is None and payload["deployment_status"] == "NOT_RUN"
          and payload["effects_authorized"] is False and payload["writes_performed"] is False)
    return {"ok": ok, "status": payload["status"], "verification": valid,
            "replay": replay, "tamper": tamper, "receipt_id": None,
            "deployment_status": payload["deployment_status"],
            "issues": payload["issues"]}


def _pit_fixture():
    from hub_scripts.skill_execution.domain_context import digest
    facts = [
        {"decision_id": "d1", "entity_id": "a", "decision_at": "2026-01-10T00:00:00Z"},
        {"decision_id": "d2", "entity_id": "b", "decision_at": "2026-01-10T00:00:00Z"},
        {"decision_id": "d3", "entity_id": "c", "decision_at": "2026-01-10T00:00:00Z"},
    ]
    features = [
        {"entity_id": "a", "reference_at": "2026-01-08T00:00:00Z",
         "available_at": "2026-01-09T00:00:00Z", "feature_value": 1},
        {"entity_id": "a", "reference_at": "2026-01-09T00:00:00Z",
         "available_at": "2026-01-10T00:00:00Z", "feature_value": 2},
        {"entity_id": "a", "reference_at": "2026-01-10T00:00:00Z",
         "available_at": "2026-01-11T00:00:00Z", "feature_value": 3},
        {"entity_id": "b", "reference_at": "2026-01-01T00:00:00Z",
         "available_at": "2026-01-02T00:00:00Z", "feature_value": 9},
    ]
    datasets = {"facts": facts, "history": features}
    context = {
        "schema_version": "SER05-CONTEXT-1", "profile": "CONTEXT_ONLY_PILOT_V1",
        "synthetic": True, "sources": [
            {"id": "facts", "snapshot_id": "synthetic-facts-v1",
             "content_sha256": digest(facts), "grain": "ONE_ROW_PER_ENTITY_DECISION",
             "columns": list(facts[0])},
            {"id": "history", "snapshot_id": "synthetic-history-v1",
             "content_sha256": digest(features), "grain": "FEATURE_HISTORY",
             "columns": list(features[0])},
        ],
        "anchor": "facts", "entity_keys": ["entity_id"],
        "anchor_grain": "ONE_ROW_PER_ENTITY_DECISION", "cardinality": "N:1",
        "decision_at": "2026-01-10T00:00:00Z", "pit": "APPLICABLE",
        "temporal": {"reference_column": "reference_at", "availability_column": "available_at",
                     "lag_kind": "CONSTANT", "lag_days": 1, "boundary": "LE",
                     "timezone": "UTC", "tie_break": "REJECT", "bitemporal": False},
        "null_key_policy": "REJECT", "requested_effect": "NONE",
    }
    return context, datasets


def _cross_pit(root, spark):
    context, datasets = _pit_fixture()
    runner = _module(root, "cross_pit", "run_pit.py", "pit_run")
    verifier = _module(root, "cross_pit", "verify_pit.py", "pit_verify")
    run_id = "free-probe-cross-pit-" + uuid.uuid4().hex
    prior_tz = spark.conf.get("spark.sql.session.timeZone")
    try:
        spark.conf.set("spark.sql.session.timeZone", "UTC")
        base = runner.run(context, datasets, spark, window_days=5, run_id=run_id)
    finally:
        spark.conf.set("spark.sql.session.timeZone", prior_tz)
    if base["status"] != "PASS":
        return {"ok": False, "status": base["status"],
                "blocking_issues": base["trace"]["blocking_issues"]}
    final = verifier.finalize(base, expected_context=context, expected_datasets=datasets,
                              expected_window_days=5, expected_run_id=run_id)
    arguments = {"expected_context": context, "expected_datasets": datasets,
                 "expected_window_days": 5, "expected_run_id": run_id}
    checked = verifier.verify_finalized(final, **arguments)
    replay = verifier.verify_finalized(final, **{**arguments, "expected_run_id": run_id + "-replay"})
    unfinalized = verifier.verify_finalized(base, **arguments)
    altered = copy.deepcopy(final)
    altered["result"]["records"][0]["feature_value"] = 999
    tamper = verifier.verify_finalized(altered, **arguments)
    observed = [r["feature_value"] for r in final["result"]["records"]]
    ok = (checked["valid"] is True and replay["valid"] is False
          and unfinalized["valid"] is False and tamper["valid"] is False
          and observed == [2, None, None]
          and final["postflight"]["status"] == "PASS"
          and final["scope_completion_authorized"] is True)
    return {"ok": ok, "status": base["status"],
            "receipt_id": (final["receipt"] or {}).get("receipt_id"),
            "postflight_id": final["postflight"].get("postflight_id"),
            "verification": checked, "replay": replay, "tamper": tamper,
            "missing_finalizer": unfinalized,
            "local_scope_completion": final["scope_completion_authorized"],
            "observed_values": observed}



def _feature_pit(root, spark):
    context, datasets = _pit_fixture()
    adapter = _module(root, "feature_pit", "run_pit_features.py", "feature_pit_view")
    upstream_id = "free-probe-feature-pit-upstream-" + uuid.uuid4().hex
    view_id = "free-probe-feature-pit-view-" + uuid.uuid4().hex
    prior_tz = spark.conf.get("spark.sql.session.timeZone")
    try:
        spark.conf.set("spark.sql.session.timeZone", "UTC")
        payload = adapter.compose(context, datasets, spark, window_days=5,
                                  upstream_run_id=upstream_id, view_run_id=view_id)
    finally:
        spark.conf.set("spark.sql.session.timeZone", prior_tz)
    if payload["status"] != "PASS":
        return {"ok": False, "status": payload["status"], "issues": payload.get("issues")}
    expected = {"expected_context": context, "expected_datasets": datasets,
                "expected_window_days": 5, "expected_upstream_run_id": upstream_id,
                "expected_view_run_id": view_id}
    checked = adapter.verify(payload, **expected)
    replay = adapter.verify(payload, **{**expected, "expected_view_run_id": view_id + "-replay"})
    altered = copy.deepcopy(payload)
    altered["result"]["features"][0]["feature_value"] = 999
    tamper = adapter.verify(altered, **expected)
    no_finalizer = copy.deepcopy(payload)
    no_finalizer["upstream_evidence"]["postflight"] = None
    missing = adapter.verify(no_finalizer, **expected)
    observed = [row["feature_value"] for row in payload["result"]["features"]]
    ok = (checked["valid"] is True and replay["valid"] is False and tamper["valid"] is False
          and missing["valid"] is False and observed == [2, None, None]
          and payload["receipt"] is None and payload["fit_performed"] is False
          and payload["materialization_performed"] is False)
    return {"ok": ok, "status": payload["status"], "verification": checked,
            "replay": replay, "tamper": tamper, "missing_finalizer": missing,
            "upstream_receipt_id": payload["result"]["upstream_receipt_id"],
            "upstream_postflight_id": payload["result"]["upstream_postflight_id"],
            "observed_values": observed}


def _pipeline_execution(root, spark):
    spec = {
        "schema_version": "SER13-SPEC-1", "synthetic": True,
        "operation": "VALIDATE_SPEC", "environment": "LOCAL_SYNTHETIC",
        "scope": "PERSONAL", "source": "synthetic_source",
        "destination": "synthetic_destination", "write_mode": "MERGE",
        "incremental": "BATCH", "primary_keys": ["id"],
        "columns": ["id", "event_at", "value"], "event_time": "event_at",
        "watermark_seconds": None, "idempotency": "MERGE_ON_KEYS",
        "permissions": "UNKNOWN", "schedule": None,
        "rollback": "NOT_APPLICABLE_NO_EFFECT",
    }
    request = {
        "schema_version": "SER13-LOCAL-RUN-1", "synthetic": True,
        "operation": "RUN_LOCAL_SPARK", "spec": spec,
        "prior_rows": [
            {"id": 1, "event_at": "2026-01-01T00:00:00Z", "value": 10},
            {"id": 2, "event_at": "2026-01-01T00:00:00Z", "value": 30},
        ],
        "batch_rows": [
            {"id": 1, "event_at": "2026-01-02T00:00:00Z", "value": 20},
            {"id": 3, "event_at": "2026-01-01T00:00:00Z", "value": 40},
        ],
    }
    expected = [request["batch_rows"][0], request["prior_rows"][1], request["batch_rows"][1]]
    runner = _module(root, "pipeline_execution", "run_local.py", "pipeline_local_run")
    verifier = _module(root, "pipeline_execution", "verify_local.py", "pipeline_local_verify")
    run_id = "free-probe-pipeline-local-" + uuid.uuid4().hex
    first = runner.run(request, spark, run_id=run_id)
    if first["status"] != "PASS":
        return {"ok": False, "status": first["status"],
                "blocking_issues": first["trace"]["blocking_issues"]}
    checked = verifier.verify(first, expected_request=request, expected_rows=expected,
                              expected_run_id=run_id)
    replay = verifier.verify(first, expected_request=request, expected_rows=expected,
                             expected_run_id=run_id + "-replay")
    changed_request = copy.deepcopy(request)
    changed_request["batch_rows"][0]["value"] = 21
    changed_data = verifier.verify(first, expected_request=changed_request,
                                   expected_rows=expected, expected_run_id=run_id)
    altered = copy.deepcopy(first)
    altered["result"]["rows"][0]["value"] = 999
    tamper = verifier.verify(altered, expected_request=request, expected_rows=expected,
                             expected_run_id=run_id)
    repeat_request = copy.deepcopy(request)
    repeat_request["prior_rows"] = first["result"]["rows"]
    second_id = run_id + "-repeat"
    second = runner.run(repeat_request, spark, run_id=second_id)
    repeat_verdict = verifier.verify(second, expected_request=repeat_request,
                                     expected_rows=expected, expected_run_id=second_id)
    ok = (checked["valid"] is True and replay["valid"] is False
          and changed_data["valid"] is False and tamper["valid"] is False
          and second["status"] == "PASS" and repeat_verdict["valid"] is True
          and first["result"]["output_sha256"] == second["result"]["output_sha256"]
          and first["trace"]["resources_completed"] == ["data_quality_check"]
          and second["trace"]["resources_completed"] == ["data_quality_check"]
          and first["result"]["persistent_write"] is False
          and first["result"]["deployment_status"] == "NOT_RUN")
    return {"ok": ok, "status": first["status"], "receipt_id": first["receipt"]["receipt_id"],
            "repeat_receipt_id": (second.get("receipt") or {}).get("receipt_id"),
            "verification": checked, "replay": replay, "changed_data": changed_data,
            "tamper": tamper, "repeat": repeat_verdict,
            "output_sha256": first["result"]["output_sha256"],
            "deployment_status": first["result"]["deployment_status"]}


def main():
    report = {"marker": MARKER, "status": "FAIL", "cases": {},
              "scope": "synthetic skill profiles; Pipeline MERGE, PIT and mature-label performance finalized by scope",
              "genie_homologation": False, "persistent_writes_performed": False}
    try:
        root = _widget_root()
        report["assistant_root"] = str(root)
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        report["versions"] = _versions()
        report["published_hashes_before"] = _hashes(root)
        report["mlflow_autolog"] = _disable_autolog()
        # Databricks provides spark in notebook scope; do not create or stop the session.
        session = globals().get("spark")
        if session is None:
            raise RuntimeError("active Databricks spark session is required")
        for name, fn in (
            ("safra", lambda: _safra(root)),
            ("explainability", lambda: _explainability(root)),
            ("estatistica", lambda: _estatistica(root)),
            ("cross_eda", lambda: _cross_eda(root, session)),
            ("cross_pit", lambda: _cross_pit(root, session)),
            ("feature_pit", lambda: _feature_pit(root, session)),
            ("features", lambda: _features(root)),
            ("baseline", lambda: _baseline(root)),
            ("monitoramento", lambda: _monitoramento(root)),
            ("monitor_performance", lambda: _monitor_performance(root)),
            ("pipeline_spec", lambda: _pipeline_spec(root)),
            ("pipeline_execution", lambda: _pipeline_execution(root, session)),
        ):
            try:
                report["cases"][name] = fn()
            except Exception as exc:
                report["cases"][name] = {"ok": False, "error": type(exc).__name__ + ":" + str(exc),
                                         "traceback": traceback.format_exc(limit=3)}
        report["published_hashes_after"] = _hashes(root)
        report["published_package_mutated"] = report["published_hashes_before"] != report["published_hashes_after"]
        if len(report["cases"]) == len(SKILLS) and all(x["ok"] for x in report["cases"].values()) and not report["published_package_mutated"]:
            report["status"] = "PASS"
    except Exception as exc:
        report["fatal_error"] = type(exc).__name__ + ":" + str(exc)
    output = json.dumps(report, ensure_ascii=False, sort_keys=True, default=str)
    print(output)
    dbutils.notebook.exit(output)


main()
