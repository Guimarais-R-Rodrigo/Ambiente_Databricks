# SE07 — runbook Free

## Objetivo

Validar registry/resolver e a correção epistemológica da auditoria.

## Pré-condição

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE07_LOCAL
DERIVED_STALE       = false
failures            = 0
```

## Probe

```python
from hub_scripts.skill_execution import get_skill_enforcement_policy

eda = get_skill_enforcement_policy("hub-ml-eda-profissional")
audit = get_skill_enforcement_policy("hub-ml-auditoria-skills")
tutor = get_skill_enforcement_policy("hub-ml-tutor-databricks")

assert eda.current_level == "L4"
assert audit.current_level == "L0"
assert audit.target_level == "L3"
assert tutor.current_level == tutor.target_level == "L0"
```

Sem escrita persistente e sem execução analítica.

Depois executar A07-1..A07-3 de [TESTES.md](TESTES.md), cada um em chat novo. Registrar primeira resposta; não repetir resultado ruim seletivamente.
