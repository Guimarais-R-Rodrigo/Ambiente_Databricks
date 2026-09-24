# B0 — checkpoint de autoria

```text
B0.1 GOVERNANCE = PREPARED
B0.2 COVERAGE_CONTRACTS = CORRECTED_CANDIDATE
B0.3 EXECUTOR = CORRECTED_CANDIDATE
B0.4 VERIFIER_BUNDLE = CORRECTED_CANDIDATE
B0.5 HOST_QUALIFICATION = NOT_RUN_LOCAL
B0.6 PILOTS = NOT_RUN_ON_LOCAL_CHECKOUT
B0.7 RELEASE_REVIEW = CORRECTIVE_REVALIDATION_PENDING

PR113_FIRST_CANDIDATE = 318b51c13f70915377624ba59a10724e0e2fd101
RV01_TO_RV07 = FIXED_IN_CORRECTIVE_CANDIDATE_PENDING_FULL_CHECKOUT_REVALIDATION
TARGETED_AUTHORING_TESTS = 65/65 PASS
FULL_B0_METATESTS = 69 TOTAL / NOT_RUN_ON_FULL_CHECKOUT_AFTER_CORRECTIVE
POLICY_CHANGED = false
DATABRICKS_EFFECT = none
SKILL_CAMPAIGN_STARTED = false
MERGE = NOT_AUTHORIZED
```

A primeira candidata permanece evidência histórica da descoberta adversarial e não é reclassificada. A corretiva precisa de revalidação no checkout real do novo SHA antes de `freeze_prepare.py`. Correção funcional durante a campanha local continua proibida: finding funcional retorna à autoria, produz novo SHA e exige rodada nova.
