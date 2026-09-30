# Pipeline Builder — validação local de especificação

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

PB-B01/PB-B02/PB-B03 permanecem pendentes para a superfície de efeito: escolha
humana da operação/destino, contrato de autorização e prova de readback real.
Testes locais e mocks não comprovam deploy nem homologação Genie.

## Execução sintética Spark local

`run_local.run(request, spark, run_id=...)` recebe um envelope fechado:

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
A execução local de teste usa Spark para o cálculo e FakeSpark para
as transições de efeito; Delta real deve ser observado no Free.
