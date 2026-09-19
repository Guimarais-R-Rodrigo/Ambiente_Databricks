# Política de enforcement por skill — SE07

Este diretório publica a política canônica de **nível de enforcement** do Skill Enforcement Framework (SEF).

Arquivo principal: [policy.json](policy.json).

## Regra fundamental

`current_level` descreve somente o nível que possui evidência estrutural implementada **agora**.

`target_level` é roadmap aprovado. Ele não autoriza dizer que a skill já possui preflight, runner, Receipt ou Postflight.

Isso evita transformar citações de helpers em alegações falsas de enforcement.

## Níveis

| Nível | Significado | Evidência mínima |
|---|---|---|
| L0 | Guidance | `SKILL.md` |
| L1 | Contract | contrato estruturado e referências resolvidas |
| L2 | Preflight | `PreflightResult` antes da lógica protegida |
| L3 | Deterministic execution | runner/primitives canônicas + Receipt |
| L4 | Fail-closed postflight | Postflight PASS antes de conclusão homologada |

Uma skill pode ter política por etapa. O `target_level` representa o nível máximo aprovado; `protected_surfaces` diz onde ele se aplica.

## Operação

Use a API pública:

```python
from hub_scripts.skill_execution import get_skill_enforcement_policy

policy = get_skill_enforcement_policy("hub-ml-feature-engineering")
print(policy.current_level, policy.target_level, policy.rollout_mode)
```

A API é somente leitura. Não altera contrato, arquivos, runtime ou estado de execução.

## Rollout

- `guidance`: orientação, sem gate estrutural;
- `audit`: mede e registra; não bloqueia por target ainda não implementado;
- `warn`: desvio é acusado e exige revisão;
- `enforce`: requisito implementado pode bloquear homologação.

A SE07 começa com política explícita 14/14. Migração de uma skill para L1–L4 só ocorre quando os artefatos correspondentes existem e os testes pertinentes passam.

## Dívida da auditoria

A política da `hub-ml-auditoria-skills` carrega explicitamente os achados da SE06:

- `AUDIT_FALSE_REASSURANCE`;
- `AUDIT_STATE_LADDER`;
- `AUDIT_CONDITIONAL_APPLICABILITY`.

A auditoria não pode chamar de “reverificado” um PASS apenas persistido no notebook.
