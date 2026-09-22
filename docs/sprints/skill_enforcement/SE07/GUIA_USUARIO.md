# SE07 — guia do usuário

Cada uma das 14 skills agora possui política explícita de enforcement.

```python
from hub_scripts.skill_execution import get_skill_enforcement_policy
p = get_skill_enforcement_policy("hub-ml-baseline-ml")
print(p.current_level, p.target_level, p.rollout_mode)
```

- `current_level`: o que realmente existe hoje;
- `target_level`: roadmap;
- `rollout_mode`: guidance/audit/warn/enforce.

Se current=L0 e target=L4, não diga que a skill já está em L4.

Na auditoria, use a ladder `citado → localizado → lido → importado → chamado → concluído`. Estado não demonstrado fica `NOT_OBSERVABLE`. PASS persistido só é “reverificado” após executar o verifier canônico.

A policy não autoriza deploy, escrita, retreino ou promoção.
