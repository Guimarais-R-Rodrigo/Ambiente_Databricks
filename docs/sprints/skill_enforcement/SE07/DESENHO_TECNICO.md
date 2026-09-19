# SE07 — desenho técnico

## Fonte canônica

`ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json`

## Resolver runtime

```python
from hub_scripts.skill_execution import get_skill_enforcement_policy
```

A API é somente leitura, falha fechado para skill desconhecida e separa `current_level` de `target_level`.

## Regra contra overclaim

```text
L0 -> SKILL.md
L1 -> execution_contract.json
L2 -> scripts/preflight.py
L3 -> scripts/run.py
L4 -> scripts/run_enforced.py + scripts/postflight.py
```

O validator SE07 confronta a política com os artifacts reais.

## Auditoria

A SE06 mostrou 3/3 `audit_false_reassurance=true`. Por isso a auditoria deve:

- resolver a policy da skill produtora;
- usar current como realidade e target como roadmap;
- preservar `citado → localizado → lido → importado → chamado → concluído`;
- usar `NOT_OBSERVABLE` para estado não demonstrado;
- distinguir PASS persistido de reverificação independente;
- não exigir Receipt/Postflight em bloqueio legítimo pré-execução;
- derivar aplicabilidade do contrato/contexto, não da existência no catálogo.

## Migração posterior

A elevação de níveis será feita por pequenos grupos, depois que registry/resolver e auditoria passarem local/Free. Não criar contratos em massa antes desse gate.
