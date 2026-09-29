# Databricks notebook source
# E1: execute este notebook somente no Free com o pacote sintético importado.
# Ajuste KIT_ROOT para a pasta importada se Path.cwd() não apontar para ela.
from pathlib import Path
import importlib.util
import json
import sys

KIT_ROOT = Path.cwd()
if not (KIT_ROOT / "tools" / "micromodelo_mm09_lab.py").is_file():
    raise RuntimeError("Defina KIT_ROOT para a pasta importada do kit Free")
sys.path.insert(0, str(KIT_ROOT / "tools"))

capabilities = {name: importlib.util.find_spec(name) is not None
                for name in ("yaml", "jsonschema", "regex", "mlflow")}
capabilities["spark"] = "spark" in globals()
print("CAPABILITIES", json.dumps(capabilities, sort_keys=True))
if not all(capabilities[name] for name in ("yaml", "jsonschema", "regex")):
    raise RuntimeError("Dependência de contrato ausente; veja requirements-free.txt")

# COMMAND ----------
import micromodelo_mm09_lab as lab

result = lab.run_greenfield_lab()
aggregate = result["scoring"]["aggregate"]
individual = result["scoring"]["individual"]
counts = aggregate["contagens"]
assert sum(counts.values()) == len(individual)
assert counts == {"TRUE": 1, "FALSE": 2, "INDETERMINADO": 3}
assert result["metadata_coverage"] == "ESCOPO_OBSERVADO"
assert result["governance_handoff"]["publication_executed"] is False
print("SYNTHETIC_CODE_LAB", json.dumps({
    "status": "EXECUTED_IN_CURRENT_RUNTIME",
    "environment_claim": "RECORD_SEPARATELY",
    "fingerprint": result["spec_fingerprint"],
    "counts": counts,
    "total": len(individual),
    "tracking": {k: v["status"] for k, v in result["tracking"].items()},
}, sort_keys=True))

# COMMAND ----------
import micromodelo_mm01_contract as mm01
import micromodelo_mm10_handoff as mm10
import micromodelo_mm12_migration_lab as mm12
import micromodelo_mm13_catalog as mm13

schema = mm01.load_schema(KIT_ROOT / "docs/sprints/micromodelos/MM01/micromodelo.schema.json")
handoff = mm10.prepare_handoff(result["spec"], schema, aggregate)
assert handoff["status"] == "DRAFT_NOT_SUBMITTED"
assert handoff["published"] is False
catalog = mm13.build_catalog([result["spec"]], schema)
source = catalog[0]["fontes"][0]
impact = mm13.impact_by_source(catalog, **source)
assert len(impact["declared_consumers"]) == 1
fixture_rows = [
    {"fixture_namespace": "MM12_FICTICIO", "synthetic": True,
     "id_entidade": item["id_entidade"], "classificacao": item["classificacao"],
     "score": item["score_heuristico_0_100"]}
    for item in individual
]
rehearsal = mm12.rehearse_equivalence(fixture_rows, [dict(x) for x in fixture_rows])
assert rehearsal["status"] == "EQUIVALENT_LAB"
assert rehearsal["migration_skill_routable"] is False
print("CATALOG_MIGRATION_LAB", json.dumps({
    "catalog_entries": len(catalog),
    "declared_impact": len(impact["declared_consumers"]),
    "migration_status": rehearsal["status"],
    "corporate_v1_verified": rehearsal["corporate_v1_verified"],
    "handoff_status": handoff["status"],
}, sort_keys=True))

# COMMAND ----------
# Tracking MLflow opcional: habilite somente se a capacidade estiver presente.
# Runs são sintéticas e usam a instância MLflow configurada pelo seu Free.
RUN_TRACKING_CHECK = False
if RUN_TRACKING_CHECK:
    if not capabilities["mlflow"]:
        raise RuntimeError("MLflow indisponível; tracking Free NOT_RUN")
    sys.path.insert(0, str(KIT_ROOT / "product_overlay" / ".assistant"))
    import mlflow
    # No Spark Connect do Free, a descoberta implícita do registry URI consulta
    # uma configuração indisponível. Fixe o serviço Databricks explicitamente.
    mlflow.set_registry_uri("databricks")
    from hub_snippets.ml.mlflow_run import run_micromodelo

    workspace_home = KIT_ROOT.parent.as_posix()
    if not workspace_home.startswith("/Workspace/Users/"):
        raise RuntimeError("KIT_ROOT deve estar na home pessoal do Free")
    experiment_path = (workspace_home.removeprefix("/Workspace")
                       + "/mm09_free_synthetic_lab_e1_20260929")

    measured = {
        "population": aggregate["populacao"],
        "count_true": counts["TRUE"],
        "count_false": counts["FALSE"],
        "count_indeterminate": counts["INDETERMINADO"],
        "score_min": aggregate["score_min"],
        "score_max": aggregate["score_max"],
        "score_mean": aggregate["score_media"],
    }
    contract = {
        "grain": "uma classificação por entidade e janela sintética",
        "classification_field": "classificacao",
        "classification_values": ["TRUE", "FALSE", "INDETERMINADO"],
        "score_field": "score_heuristico_0_100",
        "score_semantics": "FORCA_EVIDENCIA",
    }
    run_ids = {}
    for run_type in ("DEVELOPMENT", "VALIDATION", "SCORING"):
        with run_micromodelo(
            "mm09_free_sintetico", tipo=run_type,
            spec_fingerprint=result["spec_fingerprint"],
            dataset="synthetic:mm09_fixture@2026-09-29",
            split="synthetic:mesma_fixture_seis_entidades_sem_holdout",
            limitacoes=["fixture pequena", "sem dados reais ou holdout independente"],
            contrato_saida=contract, experimento=experiment_path,
        ) as run:
            run.parametros({
                "regra": "mm09_greenfield", "versao_regra": "v1", "limiar": 2,
                "janela_dias": 30, "normalizacao": "SOMA_PONDERADA_0_100",
                "politica_indeterminado": "INDETERMINADO", "score_habilitado": True,
            })
            run.agregados_medidos(measured,
                                 referencia_execucao="mm09_free_fixture_fixed_20260929")
            run_ids[run_type] = mlflow.active_run().info.run_id
    print("MLFLOW_TRACKING_CHECK", json.dumps({
        "status": "EXECUTED_IN_CURRENT_RUNTIME", "run_ids": run_ids,
        "fingerprint": result["spec_fingerprint"],
    }, sort_keys=True))

# COMMAND ----------
# O adapter Databricks real é um teste separado, somente com catálogo/schema
# sintéticos autorizados no Free. Consulte README.md antes de ativá-lo.
RUN_METADATA_CHECK = False
LAB_CATALOG = "PREENCHER_CATALOGO_SINTETICO"
LAB_SCHEMA = "PREENCHER_SCHEMA_SINTETICA"
if RUN_METADATA_CHECK:
    if "spark" not in globals():
        raise RuntimeError("Spark indisponível; metadata Databricks NOT_RUN")
    import micromodelo_mm03_metadata as mm03
    import micromodelo_mm07_databricks as mm07

    binding = mm03.Binding(LAB_CATALOG)
    provider = mm07.DatabricksMetadataProvider(spark, binding)
    collector = mm03.MetadataCollector(provider, binding)
    discovered = collector.discover([LAB_SCHEMA])
    metadata = collector.envelope(discovered, {})
    print("DATABRICKS_METADATA_CHECK", json.dumps({
        "observation_status": metadata["observation_status"],
        "coverage": metadata["coverage"],
        "catalog_complete": metadata["catalog_complete"],
        "schema_status": discovered["schemas"]["status"],
        "object_status": discovered["objects"][LAB_SCHEMA]["status"],
        "object_count_observed": len(discovered["objects"][LAB_SCHEMA]["items"]),
        "capabilities": provider.capabilities,
    }, sort_keys=True))
