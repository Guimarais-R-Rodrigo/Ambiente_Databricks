# Baseline binário temporal local — candidato

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
usa o perfil computacional SER09 e registra **o objeto de modelo treinado
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
