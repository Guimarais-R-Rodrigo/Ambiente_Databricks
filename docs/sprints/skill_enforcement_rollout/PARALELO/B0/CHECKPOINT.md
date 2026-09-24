# B0 — checkpoint de autoria

```text
B0.1 GOVERNANCE = PREPARED
B0.2 COVERAGE_CONTRACTS = CORRECTED_CANDIDATE
B0.3 EXECUTOR = CORRECTED_CANDIDATE
B0.4 VERIFIER_BUNDLE = CORRECTED_CANDIDATE
B0.5 HOST_QUALIFICATION = NOT_RUN_LOCAL
B0.6 PILOTS = NOT_RUN_LOCAL
B0.7 RELEASE_REVIEW = PENDING

RV01_TO_RV07 = CORRECTED_REPO_SIDE
CORRECTIVE_ADVERSARIAL_ISOLATED = 9/9 PASS
B0_TEST_METHODS = 52
B0_FULL_METATESTS_ON_CHECKOUT = NOT_RUN
POLICY_CHANGED = false
DATABRICKS_EFFECT = none
SKILL_CAMPAIGN_STARTED = false
```

A corretiva fecha os achados de revisão sobre composição do gate dos pilotos, reconstrução independente de DAG/global stop/limites, bindings de tarefa/comando/log, allowlist fechada do registry, protocolo RAW/SHARE não circular, cobertura de manifestos aninhados, secret scan fail-closed para binário não examinável e persistência/hash sobre bytes exatos.

Os 9 testes adversariais isolados foram executados sobre a lógica corretiva antes da publicação. A suíte versionada passou de 39 para 52 métodos, mas ainda deve ser executada no checkout real; não se transporta o PASS histórico de 39/39 para o novo SHA.

Próximo gate: executar os 52 metatestes e o inventário de cobertura no checkout real. Se verdes, fazer a preparação mecânica do snapshot via `freeze_prepare.py`, inspecionar que o único delta permitido é `README.md`, criar o freeze e executar uma única rodada de `b0_release` em diretório externo novo. Correção funcional posterior exige novo SHA; o executor local não edita o candidato.
