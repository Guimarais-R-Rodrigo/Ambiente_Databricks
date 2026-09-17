# Skill Enforcement — ferramentas

Ferramentas de desenvolvimento do Skill Enforcement Framework (SEF). Este
diretório pertence ao repositório e **não é publicado como parte do Hub**.

A estratégia vigente a partir de 2026-09-17 é local-first: testes e validações
determinísticas rodam localmente durante desenvolvimento; GitHub Actions é
reservado para a release candidate/Ready-for-review e para a certificação
pós-merge.

## SE01

### Validar contratos

```powershell
python -B tools/skill_enforcement/validate_contracts.py
```

A validação é estática: lê JSON, resolve módulos sob
`ambiente_fonte/.assistant/`, inspeciona a fachada pública `__init__.py` por AST
e confere templates relativos. Ela não importa nem executa helpers analíticos.

A resolução de API pública é compartilhada com o preflight L2 por
`hub_scripts.skill_execution.resource_resolution`, evitando que contrato e
preflight tenham semânticas diferentes para `__all__`, module path ou símbolo
público.

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

## Certificação local reproduzível

Entry point canônico:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se02
```

Por padrão o certifier:

1. exige worktree limpo;
2. valida contrato v0.1;
3. executa regressão SE01;
4. executa a suíte SE02;
5. executa validação estrutural;
6. materializa `Novo_Ambiente_Simulado` pelo renderer canônico;
7. falha se o renderer deixar diff (`DERIVED_STALE`);
8. confere snapshot README;
9. preserva stdout/stderr, exit code, duração, ambiente e estado Git em evidence bundle.

O evidence bundle é gravado fora do repositório por padrão em:

```text
~/.ambiente_databricks/sef_certifications/<timestamp>_<sha>/
```

Para escolher destino explícito:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se02 --evidence-dir C:\temp\sef-cert
```

A execução continua após um failure para revelar achados adicionais. O exit code
final continua fail-closed: qualquer step reprovado retorna código diferente de
zero.

### Subgate do CI local

`tools/ci_local.py` chama o certifier em modo parcial/read-only:

```text
--skip-render --no-evidence --allow-dirty
```

Esse subgate existe para detectar regressões SEF no gate geral do repositório. Ele
**não substitui** a certificação SE02 completa porque não prova renderer/diff.

## GitHub Actions

O workflow dedicado da SE02 chama o mesmo `certify_local.py`. Enquanto a PR está
Draft, o job é `skipped` antes de alocar runner. Ao marcar Ready-for-review, a
certificação remota volta a executar. `concurrency.cancel-in-progress=true`
evita manter certificações stale em paralelo.

A ausência de execução remota por falta de crédito deve ser registrada como
`GITHUB_ACTIONS = DEFERRED_CREDIT`, nunca como PASS.

## Limites vigentes

`mode="audit"` continua sendo o único modo aceito pelo contrato v0.1. `PASS` da
SE01 significa contrato válido; `PASS` da SE02 significa preflight resolvido.
Nenhum deles prova chamada posterior dos helpers, Execution Receipt, postflight
ou enforcement completo. SE03 permanece fora do escopo funcional desta branch.
