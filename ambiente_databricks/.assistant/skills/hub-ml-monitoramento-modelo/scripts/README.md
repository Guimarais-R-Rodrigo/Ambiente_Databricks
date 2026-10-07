# Diagnósticos sintéticos de distribuição e performance

| Pergunta | Perfil | Condição |
|---|---|---|
| Mudou a distribuição dos scores? | `DRIFT_NUMERIC_LOCAL_V1` | sem labels; `n_bins=4`, `eps=1e-6` |
| Mudou a performance binária? | `BINARY_MATURE_PERFORMANCE_V1` | labels maduras em `evaluation_at` e política fornecida |

As duas rotas usam dados realmente sintéticos, pandas/NumPy/scikit-learn/SciPy e os helpers do perfil. Dados reais anonimizados não se tornam fixtures sintéticas. Resultados ficam em memória; nenhum status autoriza alerta, retreino ou promoção.

## Receita sintética e conferência

Os exemplos seguintes são receitas documentais. A execução exige as dependências e o ambiente indicados; não é autorização de efeito remoto. Preserve request/inputs e run_id fora do payload para verificar. Asserts abaixo são conferências didáticas, não substitutos dos gates canônicos.

```python
from pathlib import Path
import importlib.util
import sys

root = Path.cwd().resolve()  # execute da raiz .assistant autorizada
assert (root / "hub_scripts").is_dir(), "Confirme a raiz .assistant"
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
script_dir = root / "skills/hub-ml-monitoramento-modelo/scripts"
def load_script(filename):
    name = "readme_monitoramento_modelo_" + filename.replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def fixture():
    return {"schema_version": "SER11-REQUEST-1", "profile": "DRIFT_NUMERIC_LOCAL_V1",
            "synthetic": True, "requested_effect": "NONE", "model_id": "SYNTH-M01",
            "model_version": "v1", "population_id": "SYNTHETIC-P01", "score_name": "score",
            "reference_start": "2025-01-01T00:00:00Z", "reference_end": "2025-01-31T23:59:59Z",
            "current_start": "2025-02-01T00:00:00Z", "current_end": "2025-02-28T23:59:59Z",
            "n_bins": 4, "eps": 1e-6,
            "reference": [{"id": f"R{i}", "observed_at": "2025-01-15T00:00:00Z", "score": value}
                          for i, value in enumerate((0.1, 0.1, 0.3, 0.6, 0.9, None))],
            "current": [{"id": f"C{i}", "observed_at": "2025-02-15T00:00:00Z", "score": value}
                        for i, value in enumerate((0.2, 0.5, 0.7, 0.7, 0.95, None))]}
request = fixture()
runner = load_script("run.py")
verifier = load_script("verify.py")
run_id = "readme-drift-tentativa-001"
payload = runner.run(request, run_id=run_id)
assert payload["status"] == "PASS", payload
assert verifier.verify(payload, expected_request=request, expected_run_id=run_id)["valid"]
```

## Receita de performance com finalização

Use o mesmo carregador da receita anterior. Os thresholds abaixo são apenas a política da fixture, não regra universal. Confirme maturidade pelo instante de disponibilidade de cada label.

```python
def performance_fixture(ref_scores=(.1, .2, .3, .4, .6, .7, .8, .9),
            cur_scores=(.1, .4, .6, .8, .2, .3, .5, .7)):
    def rows(prefix, observed, label_at, scores):
        return [{"id": f"{prefix}{i}", "observed_at": observed,
                 "label_available_at": label_at, "score": score,
                 "label": int(i >= 4)} for i, score in enumerate(scores)]
    return {"schema_version": "SER12-REQUEST-1", "profile": "BINARY_MATURE_PERFORMANCE_V1",
            "synthetic": True, "requested_effect": "NONE", "model_id": "synthetic-model",
            "model_version": "v1", "population_id": "synthetic-population",
            "score_name": "score", "evaluation_at": "2025-03-10T00:00:00Z",
            "reference_start": "2025-01-01T00:00:00Z",
            "reference_end": "2025-01-31T23:59:59Z",
            "current_start": "2025-02-01T00:00:00Z",
            "current_end": "2025-02-28T23:59:59Z",
            "auc_thresholds": {"warning": 0.1, "critical": 0.2,
                               "direction": "higher", "delta": "absolute"},
            "reference": rows("R", "2025-01-15T00:00:00Z",
                              "2025-02-05T00:00:00Z", ref_scores),
            "current": rows("C", "2025-02-15T00:00:00Z",
                            "2025-03-01T00:00:00Z", cur_scores)}
request = performance_fixture()
preflight = load_script("preflight_performance.py")
runner = load_script("run_performance.py")
verifier = load_script("verify_performance.py")
run_id = "readme-performance-tentativa-001"
assert preflight.preflight(request)["status"] == "PASS"
payload = runner.run(request, run_id=run_id)
assert verifier.verify(payload, expected_request=request, expected_run_id=run_id)["valid"]
final = verifier.finalize(payload, expected_request=request, expected_run_id=run_id)
assert verifier.verify_finalized(final, expected_request=request, expected_run_id=run_id)["valid"]
assert final["scope_completion_authorized"] is True
```

O runner sozinho não autoriza encerrar o escopo de performance. Preserve `evaluation_at`, request e run_id externos e execute `verify`, `finalize` e `verify_finalized`; Postflight ausente ou inválido mantém o diagnóstico incompleto.
## Contrato e limites por rota

Execute `preflight.py::preflight`, depois `run.py::run`, e confira chamando a
função importada `verify.py::verify(payload, expected_request=request,
expected_run_id=run_id)`. Confira `valid=true` no retorno estruturado;
executar o arquivo `verify.py` diretamente não chama essa função.
O invocador deve guardar request, payload e run_id para auditoria posterior,
com request e run_id independentes do payload.
`release_manifest.json` fixa os bytes do contrato, runner, verifier e helper.

Na rota `DRIFT_NUMERIC_LOCAL_V1`: score sintético em [0,1] ou nulo,
IDs exclusivos e duas janelas disjuntas. PSI usa quantis da referência,
arestas repetidas deduplicadas, extremidades infinitas, bucket de nulos
e epsilon explícito. KS usa observações finitas. O verifier usa contagem
independente dos buckets e CDF empírica.

O resultado é diagnóstico de distribuição em memória. Essa primeira rota não avalia labels ou performance. Nenhuma rota autoriza alerta, retreino, ação remota ou promoção.
