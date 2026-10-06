# Runners: textos anteriores preservados

Baseline `2f5a0cb94f82b78324f6a79d70af7d03e7b57040`; documentos históricos, não receita vigente.

## R0084

# Scripts candidatos — SER03: perfil mensal binário candidato, com cálculo canônico e Receipt V1

Esta pasta contém `preflight.py`, `run.py` e `verify.py`. As fachadas canônicas SEF são reutilizadas. `current_level` na policy não é alterado por estes arquivos.

As entradas são fechadas pelo código e descritas em [input.schema.json](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-analise-safra/scripts/../input.schema.json). O [contrato](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-analise-safra/scripts/../execution_contract.json) usa schema SEF 0.1, modo audit.

Os campos sintéticos e o perfil explícito são obrigatórios. Nenhum comando aqui grava output de domínio em disco: a função retorna estruturas em memória e a CLI emite JSON ASCII-safe. A coleta de evidência será responsabilidade da campanha autorizada.

Somente o perfil descrito foi implementado. Suporte a trimestre/comparações e join/Spark/Postflight L4 não deve ser inferido. O manifesto e os hashes não autenticam um usuário e não autorizam publicação.

Estado local: runner integrado, testes de domínio e regressões executados, com renderer conferido. O perfil mensal cobre `semantic_mode=EVENT` e `CUMULATIVE`, denominador fixo pelo roster, imaturidade e observações incompletas. A homologação no Free/Genie é uma etapa separada; não inferir certificação ou promoção por este README.


## R0085

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


## R0089

# Scripts candidatos de Explainability

`preflight.py` fecha o pedido sintético; `run.py` vincula modelo e arrays em cópias `float64` de conversão exata, confere o release e executa o helper canônico; `verify.py` recebe entradas externas e compara SHAP com o oráculo analítico de regressão linear. O contrato SEF está em [execution_contract.json](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-explainability/scripts/../execution_contract.json), e a forma estrutural em [input.schema.json](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-explainability/scripts/../input.schema.json). Nenhum script persiste o resultado. O Receipt V1 vincula a execução local ao release atual, pedido e run_id; não autentica usuário nem autoriza promoção.

Exemplo sintético em `tools/tests/test_skill_enforcement_explainability.py` no repositório de autoria. O perfil aceita uma única linha de background, `sklearn.LinearRegression` escalar e saída bruta. Classificação, árvores, KernelSHAP e plots ficam fora desta rota candidata. O teste local não é homologação de Databricks/Genie.


## R0090

# Features — lag sintético local

O perfil `FIXED_LAG_L1_V1` executa
`hub_snippets.ml.lgbm_temporal.create_temporal_features`, sem fit ou persistência.
O preflight fechado fica em `run.py::preflight`; `run.py::run` emite Receipt
e `verify.py::verify` recebe request, run_id e features esperadas independentes.

Campos exigidos: `schema_version=SER07-REQUEST-1`, profile, synthetic=true,
population_id, decision_at UTC, window_days inteiro entre 1 e 365,
requested_effect=NONE, temporal e rows. O contexto temporal exige
reference_column=event_at, availability_column=available_at, lag_kind=CONSTANT,
lag_days=1, boundary=LE, timezone=UTC, tie_break=REJECT, bitemporal=false.
Cada linha contém id, entity_id, event_at, available_at e value numérico finito
entre -1e9 e 1e9. Eventos são à meia-noite UTC, com disponibilidade um dia depois;
o grão entidade/instante e os IDs são únicos. No máximo 1.000 linhas.

A janela de eventos é inclusiva: [decision_at - window_days, decision_at].
Só entram linhas disponíveis até decision_at. O lag é a observação anterior
**dentro dessa janela elegível e da mesma entidade**, não o dia anterior.
O helper ordena as observações; warm-up sem histórico é removido.
`eligible_ids` mantém o denominador antes do warm-up; `features=[]` significa
que nenhuma linha tinha histórico suficiente, não sucesso analítico de negócio.

Exemplo completo reproduzível: fixture `_request` em
`tools/tests/test_ser07_feature_engineering.py` no repositório de desenvolvimento.
Na raiz da skill, a entrada CLI aceita:

```text
python scripts/run.py --request request.json --run-id execution-id
```

Nunca marque dados reais como sintéticos. Receipts são evidência de integridade
e vínculos, não autenticação de origem ou homologação Genie.


## Vista de features derivada do PIT Cross-EDA

scripts/run_pit_features.py::compose chama run_pit, finalize e verify_finalized
do Cross-EDA para o perfil COMPOSED_PIT_FEATURE_VIEW_V1. Só projeta
feature_value e available_at por decision_id após a prova local PASS.
scripts/run_pit_features.py::verify recebe inputs/IDs esperados externos,
revalida o Postflight upstream e compara toda a projeção. O payload inclui
prova upstream literal e linhagem de hashes/cutoff/janela/Receipt/Postflight.
Sem Receipt FE novo, fit, materialização ou prontidão de negócio. O contrato
pit_view_contract.json limita a composição ao perfil sintético.
# Materialização PIT sintética (SER08)

`run_pit_materialization.py::effect_request` recebe a view produzida por
`run_pit_features.py::compose` e os inputs externos originais. O digest desse
request compõe a autorização explícita para `execute`. A operação requer
Spark UTC, principal e namespace `workspace.default` correspondentes,
alvo pessoal novo `skills_delivery_<32 hex>` e cleanup `DROP_OWNED`.

O efeito usa o motor Delta compartilhado com Pipeline Builder, com perfil
fechado de cinco colunas. Preserva IDs texto, timestamps UTC de micros e
`feature_value` BIGINT nullable. Propriedades Delta ligam a tabela a hashes
da view, fontes, contexto, cutoff, Receipt e Postflight. O registro de efeito
separa versões observadas após primeiro MERGE e replay, hash do readback,
ID da tabela e resultado da remoção. Não executa fit nem materialização de
negócio; um `UNKNOWN` nunca autoriza retry automático.
O limite de valor aceito pelo PIT upstream continua [-1.000.000, 1.000.000];
`BIGINT` descreve o armazenamento, não amplia o domínio permitido.


## R0092

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


## R0093

# Pipeline Builder — validação local de especificação

A entrada [preflight.py](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-pipeline-builder/scripts/preflight.py) valida o perfil sintético
`LOCAL_SYNTHETIC_SPEC_V1` descrito no [schema](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-pipeline-builder/scripts/../input.schema.json).
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


## R0094

# Execução SER04 — KS de duas amostras independentes

Este é um perfil **candidato local** de uma única comparação bicaudal com
amostras numéricas contínuas, independentes e sem empates. A independência e
seleção i.i.d. são declarações do autor do estudo; o runner não as infere.
O request é fechado e sintético no piloto. O preflight rejeita inteiros cuja conversão
para float64 perca precisão e empates após a conversão, antes do helper.

Execute a partir da raiz publicada da `.assistant`, com Python que tenha
`numpy`, `pandas` e `scipy`:

```text
python skills/hub-ml-validacao-estatistica/scripts/preflight.py --request request.json
python skills/hub-ml-validacao-estatistica/scripts/run.py --request request.json --run-id SER04-EXAMPLE-1 > run.json
python skills/hub-ml-validacao-estatistica/scripts/verify.py --payload run.json --request request.json --run-id SER04-EXAMPLE-1 --expected-statistic 1 --expected-p-value 0.02857142857142857
```

Use arquivos e `run_id` únicos por tentativa para não sobrescrever evidência.
Interrompa a sequência se preflight ou run devolver código diferente de zero.
O runner imprime o payload JSON em stdout; ele **não** cria `run.json` sozinho.
O redirecionamento acima preserva esse payload para o verificador. A CLI de
`verify.py` exige o payload, o request e um oráculo independente; imprime um
JSON com `valid`, `status` e `issues` e retorna código zero somente quando
`valid=true`. Guarde esse output. Ausência de erro ou stdout vazio não prova
verificação. Os valores esperados devem vir de fonte confiável externa ao
payload, nunca do próprio resultado sob teste.

O JSON sintético em `fixtures/ks_separated_request.json` possui
`reference=[1,2,3,4]` e `comparison=[5,6,7,8]`: oráculo independente
`D=1`; sob H0 e oito postos sem empates, apenas duas das
`binomial(8,4)=70` rotulações extremas dão `D=1`, portanto
`p=1/35`. O método do helper é `scipy.stats.ks_2samp` com
`method=auto`; esta fixture pequena usa a rota exata da versão de SciPy
testada localmente. Outros tamanhos não ganham promessa de p exato.

`verify.py::verify` deve receber o request e run_id esperados de fonte
confiável, mais `expected_statistic=1` e `expected_p_value=1/35`.
Não extraia esses argumentos do payload testado. O Receipt prova vínculo
da execução e integridade da release; o oráculo confere o número. O
resultado não contém IC, equivalência, causalidade ou decisão de negócio.
Não persiste arquivo, tabela ou modelo.


## R0088

# Scripts candidatos — Cross-EDA

`preflight.py` preserva o contexto L2, fechado por [input.schema.json](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/scripts/../input.schema.json) e [execution_contract.json](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/scripts/../execution_contract.json). Ele não executa Spark nem comprova cobertura.

`run_diagnostic.py` executa o helper público `diagnosticar_join` em Spark para duas fontes sintéticas estáticas, com PIT `NOT_APPLICABLE`, chave da âncora única e cardinalidade sem expansão. Use `verify_diagnostic.py` com request e run_id esperados para conferir resultado, Receipt e integridade dos artefatos. O [contrato diagnóstico](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/scripts/../diagnostic_contract.json) e o [manifesto](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/scripts/../release_manifest.json) delimitam essa rota.

Os testes locais em `tools/tests/test_ser05_diagnostic.py` exercitam Spark real, cardinalidade, chaves inválidas, hashes e replay. O resultado comprova somente o diagnóstico estático; não entrega join de negócio, PIT temporal, postflight L4 ou autorização de publicação. Receipt e hashes não autenticam usuário nem substituem homologação Genie.

Nenhuma rota altera a policy. Os resultados ficam em memória; persistir evidência local não promove o candidato.

## PIT SER06 local

Use run_pit.py::run para executar pit_join no perfil LOCAL_SYNTHETIC_PIT_V1 e verify_pit.py::finalize + verify_finalized para Postflight e oráculo independente. Requer Spark UTC; fontes sintéticas limitadas a 500 linhas, atraso constante com disponibilidade explicitamente conferida, LE e janela positiva. Semânticas LT, variável e bitemporal bloqueiam. O PASS local não comprova readiness de negócio ou homologação Databricks.

