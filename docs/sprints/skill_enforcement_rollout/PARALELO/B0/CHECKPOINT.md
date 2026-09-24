# B0 — checkpoint de autoria

```text
B0.1 GOVERNANCE = PREPARED
B0.2 COVERAGE_CONTRACTS = AUDIT_CORRECTIVE_V3
B0.3 EXECUTOR = AUDIT_CORRECTIVE_V3
B0.4 VERIFIER_BUNDLE = AUDIT_CORRECTIVE_V3
B0.5 HOST_QUALIFICATION = NOT_RUN_LOCAL
B0.6 PILOTS = NOT_RUN_LOCAL
B0.7 RELEASE_REVIEW = PENDING

AUDITED_BASE_SHA = f803b50f898ac93eb0e5541ba428a3656dc4f732
AUD01_AUD06_AUD08_AUD10_AUD12 = REPO_SIDE_CORRECTIVE_IMPLEMENTED
AUD07_WINDOWS_JOB_DESIGN = HARDENED_ASSIGN_BEFORE_CHILD_START
AUD09_ROUND_IDENTITY = IMPLEMENTED_V3
AUD11_HOST_COORDINATION = SINGLE_LAUNCHER_OS_LEASE
HOST_PROOF = PENDING_WINDOWS_NTFS_SANDBOX_RESOURCE_HEADROOM
P2_OPTIMIZATIONS = DEFERRED_UNTIL_MEASURED_PILOT

B0_TEST_METHODS_STATIC = 72
AUTHORING_PREFLIGHT_ON_FINAL_SHA = NOT_RUN
B0_FULL_METATESTS_ON_FINAL_SHA = NOT_RUN
COVERAGE_V3_ON_FINAL_SHA = NOT_RUN
LOCAL_QUALIFICATION = NOT_RUN

POLICY_CHANGED = false
DATABRICKS_EFFECT = none
SKILL_CAMPAIGN_STARTED = false
```

A V3 não transforma a auditoria em certificado. As correções acima são autoria publicada no branch; a execução integral do preflight, dos 72 metatestes, do inventory e da qualificação continua obrigatória no SHA final.

O próximo gate é exclusivamente local e fail-fast: preflight → metatestes → coverage. Qualquer falha retorna à autoria com os primeiros bytes/logs preservados; o executor não corrige, não altera testes e não repete até ficar verde. Somente depois ocorre freeze mecânico e uma rodada única de `b0_release`.
