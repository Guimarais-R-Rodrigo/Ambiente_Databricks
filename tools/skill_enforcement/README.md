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
gate executável desta sprint e usa somente a biblioteca padrão, para não criar
dependência nova no produto.

## Limite da SE01

`mode="audit"` é o único modo aceito. `PASS` significa “contrato estática e
estruturalmente válido”; não significa preflight, chamada de helper, receipt,
postflight ou enforcement.
