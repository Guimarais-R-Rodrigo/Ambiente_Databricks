# Pipeline: especificação, execução local e probe Delta

| Rota | Efeito | Dependência/autorização |
|---|---|---|
| Preflight de especificação | lê contrato e valida pedido, sem efeito de dados | Python; não consulta permissões reais |
| `run_local` | cria/consulta/remove view temporária Spark | sessão Spark UTC e execução autorizada |
| `run_delta` | cria/MERGE/lê/remove tabela Delta sintética | autorização explícita, destino novo e marca de propriedade |

A última rota não é deploy de Job. `UNKNOWN` ou cleanup incerto exige inspeção dos recursos da tentativa anterior. Não repetir escrita para descobrir se a anterior funcionou.

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
script_dir = root / "skills/hub-ml-pipeline-builder/scripts"
def load_script(filename):
    name = "readme_pipeline_builder_" + filename.replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def request():
    spec = {
        "schema_version": "SER13-SPEC-1", "synthetic": True,
        "operation": "VALIDATE_SPEC", "environment": "LOCAL_SYNTHETIC",
        "scope": "PERSONAL", "source": "synthetic_source",
        "destination": "synthetic_destination", "write_mode": "MERGE",
        "incremental": "BATCH", "primary_keys": ["id"],
        "columns": ["id", "event_at", "value"], "event_time": "event_at",
        "watermark_seconds": None, "idempotency": "MERGE_ON_KEYS",
        "permissions": "UNKNOWN", "schedule": None,
        "rollback": "NOT_APPLICABLE_NO_EFFECT"}
    return {
        "schema_version": "SER13-LOCAL-RUN-1", "synthetic": True,
        "operation": "RUN_LOCAL_SPARK", "spec": spec,
        "prior_rows": [{"id": 1, "event_at": "2026-01-01T00:00:00Z", "value": 10},
                       {"id": 2, "event_at": "2026-01-01T00:00:00Z", "value": 30}],
        "batch_rows": [{"id": 1, "event_at": "2026-01-02T00:00:00Z", "value": 20},
                       {"id": 3, "event_at": "2026-01-01T00:00:00Z", "value": 40}]}
request_local = request()
# Da raiz .assistant, use sessão Spark já autorizada/configurada para UTC.
# Não crie compute nem execute este trecho sem a sessão correspondente.
preflight = load_script("preflight.py")
pre = preflight.preflight(request_local["spec"])
assert preflight.verify_preflight(pre, expected_request=request_local["spec"])["valid"]
# Oráculo manual, independente do payload: a linha mais recente do id1 vence.
expected_rows = [
    {"id": 1, "event_at": "2026-01-02T00:00:00Z", "value": 20},
    {"id": 2, "event_at": "2026-01-01T00:00:00Z", "value": 30},
    {"id": 3, "event_at": "2026-01-01T00:00:00Z", "value": 40}]
# Somente se a execução local com view temporária estiver autorizada:
runner = load_script("run_local.py")
verifier = load_script("verify_local.py")
run_id = "readme-pipeline-tentativa-001"
payload = runner.run(request_local, spark, run_id=run_id)
checked = verifier.verify(payload, expected_request=request_local,
    expected_rows=expected_rows, expected_run_id=run_id)
assert checked["valid"], checked
```

A receita usa uma especificação completa, com permissões `UNKNOWN` permitidas apenas para planejar. Para efeito Delta, a API exata é `execute(request, expected_rows, spark, authorization, run_id=..., compute_payload=None)`. O pedido de autorização deve vincular operação/destino/digest e cleanup previstos; não preencha `authorized=true` por conta própria. Não execute o probe como teste de instalação.
## Contrato e limites por rota

A entrada [preflight.py](preflight.py) valida o perfil sintético
`LOCAL_SYNTHETIC_SPEC_V1` descrito no [schema](../input.schema.json).
Ele reutiliza o preflight SEF, lê o template canônico e vincula request e fontes.
Não executa diagnósticos Spark, não cria tabelas/jobs nem emite Receipt de deploy.

```text
python skills/hub-ml-pipeline-builder/scripts/preflight.py --request request.json
```

A especificação exige ambiente local sintético, escopo pessoal, origem e destino
sintéticos distintos, chave/schema/event time, modo de escrita planejado,
incrementalidade e política de idempotência explícitos. O modo planejado é
apenas conteúdo da especificação. Permissões UNKNOWN não impedem planejar,
mas nunca autorizam escrita; nenhuma permissão real é consultada.
Schedule deve ser nulo e rollback identifica ausência de efeito.

`verify_preflight(payload, expected_request=request_confiavel)` revalida o
pedido mantido pelo chamador e os hashes das fontes atuais. Não extraia o
pedido esperado do payload a verificar. PASS valida somente a especificação;
`deployment_status=NOT_RUN`, `effects_authorized=false` e ausência de Receipt
são invariantes. Operações DEPLOY/WRITE/RUN são rejeitadas antes de qualquer efeito.

Escrita persistente exige escolha explícita de operação e destino, autorização vinculada e conferência do resultado real. Testes locais não autorizam deploy.

## Execução sintética Spark local

`run_local.run(request, spark, run_id=...)` recebe um envelope fechado. O bloco abaixo é **ilustrativo e incompleto**: `spec` precisa de uma especificação válida, como a receita completa anterior:

```json
{
  "schema_version": "SER13-LOCAL-RUN-1",
  "synthetic": true,
  "operation": "RUN_LOCAL_SPARK",
  "spec": {"...": "spec SER13-SPEC-1 validada"},
  "prior_rows": [{"id": 1, "event_at": "2026-01-01T00:00:00Z", "value": 10}],
  "batch_rows": [{"id": 1, "event_at": "2026-01-02T00:00:00Z", "value": 20}]
}
```

O perfil exige spec BATCH/MERGE, colunas exatas `id,event_at,value`,
chave `id`, sem watermark, linhas inteiras dentro dos limites do runner e
instantes UTC completos. Cada lote tem id único. O evento mais recente vence;
instante igual com conteúdo diferente é conflito. Reaplicar o mesmo lote sobre
as linhas retornadas produz o mesmo estado. Saída contém linhas observadas,
hash, contagem e diagnóstico do helper `data_quality_check`.

`verify_local.verify(payload, expected_request=request_confiavel,
expected_rows=linhas_esperadas_confiaveis, expected_run_id=run_id)`
confere resultado contra um oráculo externo, o Receipt e os hashes da release.
O payload não fornece os valores esperados. O runner cria view Spark temporária
de nome aleatório, consulta e remove a view; não faz escrita persistente.
Falha de helper ou limpeza bloqueia PASS. Este Receipt prova a execução local
de uma transformação limitada, não deploy ou execução de job Databricks.


## Probe Delta sintético Free

run_delta.py::execute recebe request SER13-LOCAL-RUN-1,
expected_rows independentes, autorização explícita do caller, run_id
e Spark. Pode receber compute_payload já produzido por run_local.py;
sempre o verifica com verify_local.py antes de CREATE. O registro de efeito
não é Receipt V1 e não autoriza deploy. A operação admite apenas tabela
workspace.default.skills_delivery_<32hex> nova, gerenciada, marcada na
criação por run_id, digest do request e nonce. Verifica sessão, marcas,
readback e replay; DROP só após revalidar as marcas. Uma falha após
CREATE pode deixar status UNKNOWN e exige inspeção humana, sem retry.
A rota Delta deve ser conferida no laboratório autorizado; o sucesso da transformação local não comprova escrita Delta no destino.
