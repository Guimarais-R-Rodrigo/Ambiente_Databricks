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

A resolução de API pública é compartilhada com o preflight L2 por funções
internas do módulo canônico `hub_scripts.skill_execution.skill_execution`,
evitando semânticas diferentes entre L1 e L2 sem ampliar a API pública do Hub.

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

A suíte SE02 contém 22 casos, incluindo falsos positivos de `__all__`, module
path não canônico e consistência entre a resolução L1 e L2.

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

## Probe do Databricks Free

`se02_free_probe.py` é um notebook SOURCE de teste para o laboratório Free. Ele
não é publicado como parte de `.assistant/`.

Depois de o produto ter sido publicado e verificado, importe o probe
separadamente e execute-o no workspace. Ele cobre:

- `F02-P1`: preflight normal → `PASS`;
- `F02-C1`: condição falsa → item não aplicável sem bloqueio;
- `F02-B1`: remove `quick_profile` somente numa fixture temporária → `BLOCKED`.

O caso negativo não altera o pacote publicado.

Runbook completo:

`docs/sprints/skill_enforcement/SE02/RUNBOOK_FREE.md`

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
