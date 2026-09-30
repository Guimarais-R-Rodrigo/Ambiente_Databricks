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

A SE07 começou com 14/14 skills. A reconciliação posterior de Micromodelos
amplia o catálogo corrente para 15/15 com L1 estático; o baseline histórico
permanece registrado na campanha SE07. Migração de uma skill para L1–L4 só ocorre quando os artefatos correspondentes existem e os testes pertinentes passam.

## Operação permanente a partir da SE08

A policy deixa de ser apenas artefato da sprint SE07 e passa a integrar os gates
permanentes do Hub:

- o validador geral confere contratos e policy contra a mesma raiz analisada;
- o gate local usa o perfil cumulativo SE08 em modo parcial/read-only;
- a certificação FULL SE08 inclui regressões anteriores, policy, I/O, renderer,
  diff do derivado e snapshot documental;
- publicação/verify no Free e comportamento do Genie Code continuam evidências
  separadas, nunca inferidas do gate local.

A promoção para o workspace do trabalho exige gate próprio. Ela não é autorizada
por `target_level`, por uma rodada verde de CI ou pelo aceite humano de uma
dívida histórica. O publicador do Free continua proibido como rota de escrita no
workspace corporativo.

## Dívida da auditoria

A política da `hub-ml-auditoria-skills` carrega explicitamente os achados da SE06:

- `AUDIT_FALSE_REASSURANCE`;
- `AUDIT_STATE_LADDER`;
- `AUDIT_CONDITIONAL_APPLICABILITY`.

A auditoria não pode chamar de “reverificado” um PASS apenas persistido no notebook.
