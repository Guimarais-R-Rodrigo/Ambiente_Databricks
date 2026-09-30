# Drift numérico local — candidato

Execute `preflight.py::preflight`, depois `run.py::run`, e confira chamando a
função importada `verify.py::verify(payload, expected_request=request,
expected_run_id=run_id)`. Confira `valid=true` no retorno estruturado;
executar o arquivo `verify.py` diretamente não chama essa função.
O invocador deve guardar request, payload e run_id para auditoria posterior,
com request e run_id independentes do payload.
`release_manifest.json` fixa os bytes do contrato, runner, verifier e helper.

Somente `DRIFT_NUMERIC_LOCAL_V1`: score sintético em [0,1] ou nulo,
IDs exclusivos e duas janelas disjuntas. PSI usa quantis da referência,
arestas repetidas deduplicadas, extremidades infinitas, bucket de nulos
e epsilon explícito. KS usa observações finitas. O verifier usa contagem
independente dos buckets e CDF empírica.

O resultado é diagnóstico de distribuição em memória. Sem labels,
performance, threshold, alerta, retreino, ação remota ou promoção.
