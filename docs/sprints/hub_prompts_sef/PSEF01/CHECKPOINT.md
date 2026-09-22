# PSEF01 — checkpoint

**Estado:** `CANDIDATA_PARA_REVISAO`

## Identidade

```text
BASE_MAIN = 11851e137dd7793b351ac08fc211c0be90005dee
BRANCH    = psef/PSEF01-contrato-editorial-policy-aware
```

## Entrega

- contrato editorial transversal policy-aware implementado no README raiz;
- `current_level` e `target_level` distinguidos;
- precedência da rota canônica explicitada;
- prompt preservado como briefing, sem “SEF dos prompts”;
- zero alteração nos 16 briefings individuais;
- zero alteração em skills/policy/instruções/Manual.

## Gates

```text
PSEF01_SCOPE_VALIDATION      = PASS
PSEF01_POLICY_AWARE_CONTRACT = PASS
PSEF01_NO_LEVEL_HARDCODE     = PASS
DERIVED_STALE                = true
DERIVED_MANUAL_EDIT          = false
GITHUB_ACTIONS               = DEFERRED_NO_CREDITS
DATABRICKS_FREE              = NOT_RUN
GENIE_BEHAVIOR               = NOT_RUN
```

## Estado de integração

A candidata **não deve ser mergeada isoladamente** porque a fonte mudou e `Novo_Ambiente_Simulado/` não foi regenerado. Editar o derivado à mão violaria a arquitetura aceita.

O tratamento correto permanece:

```text
fonte acumulada PSEF01–PSEF05
        ↓
renderer canônico na PSEF06
        ↓
Novo_Ambiente_Simulado
        ↓
validação de equivalência
```

## Próximo gate

Revisão humana da PSEF01. Após aceite, a PSEF02 pode ser iniciada sobre esta candidata acumulada, sem merge isolado da PSEF01.
