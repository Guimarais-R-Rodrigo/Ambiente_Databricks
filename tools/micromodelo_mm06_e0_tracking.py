"""Reproduz três runs MLflow E0 com a fixture MM09; usa backend local ignorado.

Exige MLflow instalado. O backend de arquivos está em manutenção no MLflow 3;
este ensaio faz opt-in explícito e não comprova o backend do Databricks Free.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "ambiente_databricks/.assistant")]
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"

import mlflow
from mlflow.tracking import MlflowClient
from hub_snippets.ml.mlflow_run import run_micromodelo
import micromodelo_mm09_lab as mm09

mlflow.set_tracking_uri((ROOT / ".artifacts/mlruns-mm06").resolve().as_uri())
result = mm09.run_greenfield_lab()
aggregate = result["scoring"]["aggregate"]
counts = aggregate["contagens"]
metrics = {
    "population": aggregate["populacao"],
    "count_true": counts["TRUE"],
    "count_false": counts["FALSE"],
    "count_indeterminate": counts["INDETERMINADO"],
    "score_min": aggregate["score_min"],
    "score_max": aggregate["score_max"],
    "score_mean": aggregate["score_media"],
    "score_count": aggregate["scores_emitidos"],
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
        "mm09_e0_sintetico", tipo=run_type,
        spec_fingerprint=result["spec_fingerprint"],
        dataset="synthetic:mm09_fixture@2026-09-29",
        split="synthetic:mesma_fixture_seis_entidades_sem_holdout",
        limitacoes=["fixture pequena e intencional", "sem dados reais ou holdout independente"],
        contrato_saida=contract, experimento="mm09_e0_synthetic_lab",
    ) as run:
        run.parametros({"regra": "mm09_greenfield", "versao_regra": "v1",
                        "limiar": 2, "janela_dias": 30,
                        "normalizacao": "SOMA_PONDERADA_0_100",
                        "politica_indeterminado": "INDETERMINADO",
                        "score_habilitado": True})
        run.agregados_medidos(metrics, referencia_execucao="mm09_e0_fixture_fixed_20260929")
        run_id = mlflow.active_run().info.run_id
    logged = MlflowClient().get_run(run_id)
    assert logged.data.tags["mm06.complete"] == "true"
    assert logged.data.tags["mm06.spec_fingerprint"] == result["spec_fingerprint"]
    assert logged.data.tags["mm06.run_type"] == run_type
    assert logged.data.metrics["population"] == 6.0
    assert logged.data.metrics["count_true"] == 1.0
    assert logged.data.metrics["count_false"] == 2.0
    assert logged.data.metrics["count_indeterminate"] == 3.0
    run_ids[run_type] = run_id
print(json.dumps({"status": "PASS_E0_LOCAL_FILE_MLFLOW", "run_ids": run_ids,
                  "fingerprint": result["spec_fingerprint"],
                  "counts": counts, "total": aggregate["populacao"]}, sort_keys=True))
