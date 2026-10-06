# Política de enforcement por skill — SEF

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

## Como consultar o nível admitido

A policy declara `current_level`, `target_level`, `scope_mode` e `protected_surfaces` de cada skill. Micromodelos está L1/audit; isso não classifica todas as skills como L1. Runners presentes podem ter evidência sintética sem que a policy tenha sido promovida. Confira o registro antes de executar: o alvo futuro não autoriza capacidade ausente.

A promoção para o workspace do trabalho exige gate próprio. Ela não é autorizada por target, CI local ou aceite de dívida histórica. Ferramentas de publicação do laboratório não são rota de escrita corporativa.

`known_debt` pode conter descrição anterior à implementação: em Micromodelos, existe adapter metadata-only no módulo de domínio, embora a dívida cite sua ausência. Essa divergência textual não altera L1/audit nem comprova homologação. Sua reconciliação exige decisão específica da policy.

## Evidência e auditoria

Um PASS salvo em notebook é evidência observada. Só chame o resultado de reverificado depois de executar o verificador canônico sobre os artefatos e inputs correspondentes. Preserve as restrições `AUDIT_FALSE_REASSURANCE`, `AUDIT_STATE_LADDER` e `AUDIT_CONDITIONAL_APPLICABILITY` da policy; nomes normativos não são dispensas.
