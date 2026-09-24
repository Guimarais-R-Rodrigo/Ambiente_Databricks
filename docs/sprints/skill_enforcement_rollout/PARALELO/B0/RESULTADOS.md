# B0 — resultados

## Estado após a auditoria independente de 24/09/2026

A auditoria examinou a candidata `f803b50f898ac93eb0e5541ba428a3656dc4f732` e classificou o B0 como `BLOCKED_AUTHORING`. O branch recebeu posteriormente uma corretiva V3.

```text
AUDIT_BASE = f803b50f898ac93eb0e5541ba428a3656dc4f732
AUDIT_CORRECTIVE_V3 = IMPLEMENTED_REPO_SIDE
B0_TEST_METHODS_STATIC = 79

AUTHORING_PREFLIGHT_ON_FINAL_SHA = NOT_RUN
B0_FULL_METATESTS_ON_FINAL_SHA = NOT_RUN
COVERAGE_V3_ON_FINAL_SHA = NOT_RUN
LOCAL_QUALIFICATION = NOT_RUN
WINDOWS_JOB_OBJECT_PROOF = NOT_RUN
WINDOWS_NTFS_QUALIFICATION = NOT_RUN
SANDBOX_NEGATIVE_PERMISSIONS = NOT_RUN
HOST_RESOURCE_HEADROOM = NOT_RUN

POLICY_CHANGED = false
DATABRICKS_EFFECT = none
REAL_SKILL_CAMPAIGN = NOT_STARTED
```

### Implementado repo-side

- resultado/command-record/task/campaign V3 fail-closed;
- null, NA obrigatório e tipos inválidos rejeitados;
- causalidade e limites por intervalos;
- secret scan independente sobre SHARE final e filenames;
- reserved paths, symlink/path escape bloqueados;
- supervisor POSIX e Windows Job Object com assignment-before-release;
- collection real de unittest e COMMAND_ONLY com entrypoint verificado;
- `ROUND_START` + `RELEASE_SPEC` vinculados a SHA/tree/base/host/registry/coverage/policy/interpreter;
- verificação independente de artefatos persistidos;
- lease host-wide conservador de uma campanha;
- schemas V3 fechados e preflight de drift;
- `RELEASE_VERDICT` externo como único veredito de liberação.

### Deliberadamente não alegado

Não há PASS do SHA final, qualificação Windows, prova de sandbox, benchmark de ganho de paralelismo ou autorização de campanha real. Dispatch contínuo, cache de inventory e tuning de concorrência ficam fora do caminho crítico até existir medição do piloto.

O próximo executor deve rodar, no SHA final limpo, `preflight`, a suíte B0 e `coverage`. Somente após esses três verdes deve preparar o freeze e executar uma única rodada de `b0_release`.

## Rodada local de autoria — 7ad3846f — FAIL preservado

```text
AUTHORING_SHA = 7ad3846fb5b79590050adc7c11ff841e816fb6b9
AUTHORING_PREFLIGHT = PASS
METATESTS = FAIL
COLLECTED_AND_EXECUTED = 72
PASS = 68
FAIL = 2
SKIP = 2
COVERAGE_V3 = NOT_RUN_BY_FAIL_FAST
FREEZE = NOT_CREATED
B0_RELEASE = NOT_RUN
```

Falhas de autoria observadas: o coverage tentava normalizar IDs de suites reais a partir do nome importável, o que falha para `discover` fora de package e paths como `.assistant/hub-ml-concierge`; e um metateste documental ainda exigia o checkpoint transitório `B0_AUDIT_CORRECTIVE_V3_AUTHORING`. Ambas foram corrigidas repo-side em SHA posterior. O PASS parcial 68/72 permanece evidência histórica e não é certificado do novo SHA.
## Rodada local de autoria — 39d2fefa — FAIL preservado

```text
AUTHORING_SHA = 39d2fefa13fa747c2ab636e8a47cda06737d841e
AUTHORING_PREFLIGHT = PASS
METATESTS = PASS
COLLECTED_AND_EXECUTED = 74
PASS = 72
FAIL = 0
ERROR = 0
SKIP = 2
COVERAGE_V3 = FAIL_OUTPUT_ENCODING_CP1252
FREEZE = NOT_CREATED
B0_RELEASE = NOT_RUN
```

A coleta/normalização corrigida funcionou: os 77 metatestes completaram sem falha. O bloqueio seguinte ocorreu apenas na serialização do JSON do coverage para stdout em console Windows `cp1252`, ao encontrar o caractere `→`. O inventário não foi reclassificado; a saída CLI foi corrigida para JSON ASCII-safe, semanticamente equivalente após parsing. A rodada permanece FAIL histórica e exige reexecução integral no SHA novo.
## Rodada de release — freeze 49385c30 — FAIL preservado

```text
AUTHORING_SHA = ec132cccfe596dee7c5459346db59a0b573c226e
AUTHORING_PREFLIGHT = PASS
AUTHORING_METATESTS = PASS_74_COLLECTED_72_PASS_2_SKIP
AUTHORING_COVERAGE = PASS_21_SE08_9_CI_5_SER01_1353_UNIQUE_METHODS
FREEZE_SHA = 49385c306b03b1eeaf734e5b8daa4c2a4e5dc922
FREEZE_TREE = aa0b32fbf5f9728ac7fde326ace49490e1521abb
B0_RELEASE = FAIL
FIRST_FAILURE = metatests
RELEASE_STATUS = NOT_QUALIFIED
RAW_VALID = true
SHARE_VALID = true
RAW_SHARE_BINDING_VALID = true
ENVELOPE_VALID = true
```

A falha ocorreu apenas dentro do `b0_release`: o supervisor executou os metatestes com ambiente sanitizado sem `HOME/USERPROFILE/HOMEDRIVE/HOMEPATH`; no Windows, `Path.home()` levantou `RuntimeError` ao importar `certify_local.py` via coverage. O preflight interno passou. O envelope de falha foi íntegro: manifests RAW/SHARE, binding e todos os hashes referenciados pelo `RELEASE_VERDICT` foram recalculados independentemente e conferem.

O freeze `49385c30...` é preservado como evidência histórica, mas foi invalidado pela correção funcional posterior. Não pode ser reutilizado como candidata de release. O supervisor passou a preservar apenas as variáveis não sensíveis de identidade do home necessárias ao runtime, mantendo tokens/credenciais fora da allowlist, e a suíte ganhou reprodução direta de `Path.home()` no child environment.
## Rodada de release — freeze f6516959a2f973ea1e163da80548e8ebb0e235cf — FAIL preservado

```text
AUTHORING_SHA = e62861bb13d5da5ab3248ab094225aaf4ded5b41
AUTHORING_TREE = 11ded361baf8b242a6eb8eacf1e29e2ed08d5b53
AUTHORING_PREFLIGHT = PASS
AUTHORING_METATESTS = PASS_76_COLLECTED_74_PASS_2_SKIP
AUTHORING_COVERAGE = PASS_21_SE08_9_CI_5_SER01_1353_UNIQUE_METHODS
FREEZE_SHA = f6516959a2f973ea1e163da80548e8ebb0e235cf
FREEZE_TREE = 11ded361baf8b242a6eb8eacf1e29e2ed08d5b53
FREEZE_KIND = EMPTY_MARKER_TREE_IDENTICAL_TO_AUTHORING
B0_RELEASE = FAIL
FIRST_FAILURE = metatests
RELEASE_STATUS = NOT_QUALIFIED
RAW_VALID = true
SHARE_VALID = true
RAW_SHARE_BINDING_VALID = true
ENVELOPE_VALID = true
```

A autoria externa ao supervisor passou integralmente, inclusive coverage com 1.353 IDs únicos. O `freeze_prepare` reportou `changed=false`; o commit `f6516959a2f973ea1e163da80548e8ebb0e235cf` é um marcador vazio de freeze, com a mesma tree da autoria, 0 adições e 0 deleções.

Dentro do `b0_release`, o preflight interno passou e os metatestes reprovaram somente `test_coverage_has_no_empty_method_map`: `ci:temas` virou `COLLECTION_ERROR` quando o coverage foi reexecutado sob o ambiente sanitizado do supervisor. O bundle completo `b0_e62861bb_f6516959a2f973ea1e163da80548e8ebb0e235cf_20260924_complete.zip` teve SHA-256 `bd6e6949cbcb574988fcaf4795fcd069fbba13bd0f5ad21889def105449e53b3`; manifests RAW/SHARE, binding e hashes do release verdict foram recalculados e conferem.

A corretiva posterior amplia apenas a allowlist de metadados não sensíveis do runtime Windows (por exemplo `APPDATA`, `LOCALAPPDATA`, `COMSPEC`, `PATHEXT` e locale), preservando exclusão de credenciais. A suíte ganhou um discriminante end-to-end que executa o coverage completo com exatamente `_clean_env()` e exige PASS/21/9/5. O metateste de coverage também passa a exibir `collection_errors` detalhados em eventual falha. O freeze `f6516959a2f973ea1e163da80548e8ebb0e235cf` é histórico e não pode ser reutilizado.

## Rodada de autoria — 39e86591 — FAIL no freeze_prepare preservado

```text
AUTHORING_SHA = 39e86591d710100acb32590e38fc6dac4db50d3f
AUTHORING_PREFLIGHT = PASS
AUTHORING_METATESTS = PASS_77_COLLECTED_75_PASS_2_SKIP
AUTHORING_COVERAGE = PASS_21_SE08_9_CI_5_SER01_1353_UNIQUE_METHODS
FREEZE_PREPARE = FAIL
FREEZE_CREATED = NO
B0_RELEASE = NOT_RUN
```

O `freeze_prepare` executou o validator baseline e parou em três arquivos de rastreabilidade: `CHANGELOG.md`, `B0/RESULTADOS.md` e `CONTROLE_PLANO.json`. O gatilho não era identidade pessoal real: o SHA completo `f6516959a2f973ea1e163da80548e8ebb0e235cf`, cuja forma abreviada anterior coincide com a heurística corporativa `letra + 6–8 dígitos`. A correção preserva a rastreabilidade substituindo o referência pelo SHA Git completo `f6516959a2f973ea1e163da80548e8ebb0e235cf`, sem afrouxar `CORPORATE_RE`.

O bundle `b0_39e86591_20260924_authoring.zip` teve SHA-256 `889abb4969a9db6f64d55c1026095de86c7d144901e600db1c0a7a6c68712024`. A saída do `freeze_prepare` nessa rodada foi emitida pelo console em cp1252; a autoria posterior tornou o JSON CLI ASCII-safe e moveu a verificação de higiene para o preflight, para que essa classe de falha apareça antes do freeze.

Nenhum freeze foi criado e nenhum `b0_release` foi executado nesta rodada.

