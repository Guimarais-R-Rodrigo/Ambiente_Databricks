# PSEF01 — validação

## Validações repo-side executadas

### V01 — escopo

Esperado: a alteração funcional da PSEF01 fica restrita ao README raiz de `hub_prompts`.

### V02 — contrato policy-aware

O README fonte deve conter, de forma não ambígua:
- `Policy SEF / current_level`;
- distinção `current_level` × `target_level`;
- `rollout_mode` associado à skill/policy;
- referência relativa válida a `hub_padroes/skill_enforcement/policy.json`;
- precedência de entrypoint canônico em etapa protegida;
- proibição de transformar prompt em policy/níveis/Receipt/Postflight próprios.

### V03 — não hardcode

O README pode explicar L0–L4 como conceito, mas não deve duplicar a classificação individual das 14 skills nem congelar níveis por prompt.

### V04 — preservação de escopo

Não alterar briefings individuais, skills, policy, instruções globais, Manual ou helpers.

### V05 — derivado

Confirmar que o derivado continua com o blob anterior e, portanto, está deliberadamente stale. Não editar o espelho manualmente.

## Resultado

```text
PSEF01_SCOPE_VALIDATION      = PASS
PSEF01_POLICY_AWARE_CONTRACT = PASS
PSEF01_NO_LEVEL_HARDCODE     = PASS
PSEF01_PROTECTED_SURFACES    = PASS
DERIVED_STALE                = true
DERIVED_MANUAL_EDIT          = false
GITHUB_ACTIONS               = DEFERRED_NO_CREDITS
DATABRICKS_FREE              = NOT_RUN
GENIE_BEHAVIOR               = NOT_RUN
```

`DERIVED_STALE=true` não é classificado como PASS de integração. É um bloqueio explícito de merge desta candidata isolada até a rematerialização canônica prevista na PSEF06.
