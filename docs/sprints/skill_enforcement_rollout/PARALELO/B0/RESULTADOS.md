# B0 — resultados

## Estado após a auditoria independente de 24/09/2026

A auditoria examinou a candidata `f803b50f898ac93eb0e5541ba428a3656dc4f732` e classificou o B0 como `BLOCKED_AUTHORING`. O branch recebeu posteriormente uma corretiva V3.

```text
AUDIT_BASE = f803b50f898ac93eb0e5541ba428a3656dc4f732
AUDIT_CORRECTIVE_V3 = IMPLEMENTED_REPO_SIDE
B0_TEST_METHODS_STATIC = 76

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

A coleta/normalização corrigida funcionou: os 76 metatestes completaram sem falha. O bloqueio seguinte ocorreu apenas na serialização do JSON do coverage para stdout em console Windows `cp1252`, ao encontrar o caractere `→`. O inventário não foi reclassificado; a saída CLI foi corrigida para JSON ASCII-safe, semanticamente equivalente após parsing. A rodada permanece FAIL histórica e exige reexecução integral no SHA novo.

