# Baseline binário temporal: cálculo e tracking autorizado

Escolha a rota antes de executar:

| Rota | Efeito | Preparação |
|---|---|---|
| `run.py` | fit sintético e resultado em memória | pandas, NumPy, scikit-learn; sem MLflow |
| `run_tracking.py` | cria experimento/run/modelo MLflow, readback e soft delete | backend Databricks, sessão/identidade e autorização `SER10-AUTH-1` vinculada |

A segunda rota não é teste de instalação. `BLOCKED`/`UNKNOWN_RESIDUE` exigem inspeção dos IDs e tentativa anterior antes de decidir qualquer repetição.

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
script_dir = root / "skills/hub-ml-baseline-ml/scripts"
def load_script(filename):
    name = "readme_baseline_ml_" + filename.replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def fixture():
    return {"schema_version": "SER09-REQUEST-1", "profile": "BINARY_TEMPORAL_LOCAL_V1",
            "synthetic": True, "requested_effect": "NONE", "population_id": "SYNTHETIC-P01",
            "target": "target", "positive_class": 1, "unit": "synthetic_entity",
            "date_column": "observed_at", "feature_order": ["feature"], "train_pct": 0.5,
            "val_pct": 0.25, "gap_periods": 0, "period_unit": "M", "threshold": 0.5, "seed": 17,
            "rows": [{"id": f"B{i:02d}", "observed_at": f"2024-{i:02d}-01T00:00:00Z",
                      "feature": float(i % 5), "target": i % 2} for i in range(1, 13)]}
request = fixture()
runner = load_script("run.py")
verifier = load_script("verify.py")
run_id = "readme-baseline-tentativa-001"
payload = runner.run(request, run_id=run_id)
assert payload["status"] == "PASS", payload
checked = verifier.verify(payload, expected_request=request, expected_run_id=run_id)
assert checked["valid"], checked
# Oráculo do calendário explícito: treino meses1–6, validação7–9, holdout10–12.
assert payload["result"]["partitions"]["train"]["ids"] == [f"B{i:02d}" for i in range(1, 7)]
```

A receita usa a fixture independente do perfil e não abre tracking. Guarde request/IDs antes de chamar. O verificador refaz partições/fit/métricas a partir das entradas confiadas; PASS não aprova um modelo para uso real. A verificação final do tracking não relê o modelo após exclusão; soft delete não é apagamento físico.
## Contrato e limites por rota

Execute `preflight.py::preflight`, depois `run.py::run`, e confira chamando a
função importada `verify.py::verify(payload, expected_request=request,
expected_run_id=run_id)`. Confira `valid=true` no retorno estruturado;
executar o arquivo `verify.py` diretamente não chama essa função.
O invocador deve guardar request, payload e run_id para auditoria posterior,
com request e run_id independentes do payload.
`release_manifest.json` fixa os bytes do contrato, runner, verifier e helpers.

Somente o perfil sintético `BINARY_TEMPORAL_LOCAL_V1` é executável:
12 ou mais meses distintos, um ID por mês, target binário conhecido na
fixture, feature numérica finita, classes ambas presentes em cada partição,
50/25/25, gap zero, seed 17 e threshold 0.5. Split por meses usa o helper
público; StandardScaler e LogisticRegression são ajustados somente no
treino. O helper público calcula as métricas; o resultado expõe somente
AUC ROC e Brier por partição, que o verifier confere independentemente.

Resultado e Receipt são locais e em memória. Nenhum run MLflow, artefato,
promoção ou ação no workspace é produzido. O verifier confere partições,
fit, scores e métricas com o request confiado, além do Receipt/release.

## Tracking efêmero pessoal

`run_tracking.run_tracking(request, authorization, spark, run_id=...)`
usa o perfil computacional `BINARY_TEMPORAL_LOCAL_V1` e registra **o objeto de modelo treinado
nessa execução**, sem reajustá-lo para logging; o verifier ajusta seu oráculo
independente. Requer `tracking_uri` e `registry_uri` do MLflow configurados
como `databricks`, ausência de run ativo, experimento ainda inexistente e usuário
derivado de `spark.sql("SELECT current_user() AS user")`.

O record externo de autorização deve ter exatamente:
`schema_version=SER10-AUTH-1`, `authorized=true`,
`effect=CREATE_EXPERIMENT_RUN_LOG_MODEL_SOFTDELETE`,
`target_experiment=/Users/<current_user>/hub_lab/skills_delivery_<hex8-32>`,
`request_sha256` do request, `run_id` da computação, `current_user`,
`retention=SOFT_DELETE_AFTER_READBACK` e `authorization_id` não vazio.
O record vincula escopo, mas não autentica uma decisão humana por si só.

O adapter chama o helper público `run_governado`, registra parâmetros,
métricas holdout, tags de binding e o Pipeline exato com input example.
Enquanto o experimento está ativo, `verify_tracking.verify_live` lê
independentemente run, experimento, assinatura, exemplo e modelo remoto e
compara predições com o oráculo da computação. O runner chama esse verifier
na mesma tentativa antes de qualquer delete; veredito inválido bloqueia
PASS mas ainda inicia cleanup dos IDs próprios. Em seguida observa soft
delete do run **antes** de deletar o experimento e confirma o experimento
deletado por ID; o nome pode ser movido para Trash.

Falha parcial retorna `BLOCKED`, IDs criados, tentativas e
`UNKNOWN_RESIDUE` quando cleanup é ambíguo. Não há retry automático.
`verify_tracking.verify_finalized` exige request, autorização, run_id,
usuário autenticado e cliente externos, confere Receipt e consistência da
evidência live registrada, mais o estado atual deleted do experimento.
Após delete do experimento, o Free pode recusar runs/get e artefatos: este
verifier final **não** reconfirma o modelo remoto nessa fase. O veredito
histórico no payload não autentica sozinho uma chamada remota; PASS do runner
depende da chamada live real. Soft delete não equivale a apagamento físico.
