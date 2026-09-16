# Skill Enforcement — ferramentas

Ferramentas de desenvolvimento do Skill Enforcement Framework (SEF). Este
diretório pertence ao repositório e **não é publicado como parte do Hub**.

## SE01

### Validar contratos

```powershell
python -B tools/skill_enforcement/validate_contracts.py
```

A validação é estática: lê JSON, resolve módulos sob
`ambiente_fonte/.assistant/`, inspeciona a fachada pública `__init__.py` por AST
e confere templates relativos. Ela não importa nem executa helpers.

Saída JSON para automação:

```powershell
python -B tools/skill_enforcement/validate_contracts.py --json
```

### Schema

`execution_contract.schema.json` documenta o schema v0.1. O validador Python é o
gate executável de desenvolvimento e usa somente a biblioteca padrão, para não
criar dependência nova no produto.

## SE02

A implementação publicada do preflight não vive em `tools/`; ela fica em:

`ambiente_fonte/.assistant/hub_scripts/skill_execution/`

A API pública é:

```python
from hub_scripts.skill_execution import run_preflight
```

O acionador fino da skill piloto vive em:

`ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/preflight.py`

O preflight resolve contrato, condições, APIs públicas e templates antes do core,
produzindo `PASS` ou `BLOCKED`. Ele não importa helpers analíticos para descobrir
APIs, não executa a EDA e não escreve no workspace.

Testes:

```powershell
python -B tools/tests/test_skill_enforcement_se01.py
python -B tools/tests/test_skill_enforcement_se02.py -v
```

## Limites vigentes

`mode="audit"` continua sendo o único modo aceito pelo contrato v0.1. `PASS` da
SE01 significa contrato válido; `PASS` da SE02 significa preflight resolvido.
Nenhum deles prova chamada posterior dos helpers, Execution Receipt, postflight
ou enforcement completo. SE03 permanece fora do escopo.
