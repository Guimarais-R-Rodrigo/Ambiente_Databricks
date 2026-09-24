# B0 — checkpoint de autoria

```text
B0.1 GOVERNANCE = PREPARED
B0.2 COVERAGE_CONTRACTS = IMPLEMENTED_CANDIDATE
B0.3 EXECUTOR = IMPLEMENTED_CANDIDATE
B0.4 VERIFIER_BUNDLE = IMPLEMENTED_CANDIDATE
B0.5 HOST_QUALIFICATION = NOT_RUN_LOCAL
B0.6 PILOTS = NOT_RUN_LOCAL
B0.7 RELEASE_REVIEW = PENDING
POLICY_CHANGED = false
DATABRICKS_EFFECT = none
SKILL_CAMPAIGN_STARTED = false
```

Próximo gate: preparação mecânica do snapshot via `freeze_prepare.py`, commit de freeze após inspeção do diff e, somente então, execução local single-round do qualificador B0 em diretório externo novo. Correção funcional posterior exige novo SHA; o executor local não edita o candidato.
