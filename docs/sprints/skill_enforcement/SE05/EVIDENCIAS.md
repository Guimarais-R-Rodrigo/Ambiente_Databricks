# SE05 — evidências de desenvolvimento

## Escopo

Este arquivo registra evidências observadas durante a construção da SE05. Ele não substitui os gates finais `FULL_SE05_LOCAL` e Databricks Free.

## Evidência unitária / micro-evals

No HEAD intermediário `8e08a193bfc3a9b4d8c032047af0f0809e4c2c77`:

```text
execution_contract       = PASS
SE05 postflight tests    = 15/15 PASS
sintaxe componentes SE05 = PASS
```

Casos cobertos incluem:

- happy path completo;
- output manual sem Receipt;
- required/conditional omitidos;
- skip sem justificativa;
- template ausente;
- handoff incompleto;
- artifacts adulterados;
- stale Receipt;
- optional ausente;
- Postflight adulterado;
- config de postflight ausente.

## Evidência de integração L4

No HEAD `2a1d8afd2d072e29bfe16bf2a8e549688e4742f3`:

```text
SE05 runner integration = 7/7 PASS
```

Foi observado:

- happy path `run_enforced → Receipt → Postflight → completion` autorizado;
- core L3/SE04 isolado sem autorização L4;
- `pk_columns` ausente impedindo PASS;
- `safe_display` aplicável sem renderer falhando fechado;
- helper falho ficando em `called` e fora de `completed`;
- claim de completion adulterado detectado;
- release manifest protegendo componentes SE05.

## Certifier parcial

No mesmo HEAD `2a1d8afd2d072e29bfe16bf2a8e549688e4742f3` foi executado:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se05 --skip-render --verbose
```

Resultados funcionais observados:

```text
contract_v0_1        = PASS
se01_regression      = PASS
se02_regression      = PASS
se03_regression      = PASS
se04_receipt_tests   = PASS
se04_runner_tests    = PASS
se05_postflight      = PASS
se05_runner          = PASS
assistant_structure  = PASS com 1 aviso local de __pycache__
readme_snapshot      = FAIL por snapshot desatualizado
```

Classificação correta dessa execução:

```text
LOCAL_CERTIFICATION = FAIL
scope               = PARTIAL_SE05_NO_RENDER
DERIVED_STALE       = false
failures            = 1
```

A falha foi exclusivamente o snapshot README, não as suítes funcionais.

## `__pycache__` local

O aviso de duas pastas `__pycache__` surgiu depois de usar `python -m py_compile` no gate manual. Esses diretórios são resíduos locais/ignorados, não artefatos da SE05 e não devem ser versionados.

A correção operacional é remover somente `__pycache__` antes do certifier final e evitar `py_compile` como check final; usar AST parsing quando uma verificação sem escrita for necessária.

## Materialização final do simulado

No commit `65fe556ea70e17610af47cc3d6f1a4abf7438533` foi executado o renderer canônico após limpeza dos resíduos locais de Python.

Resultado observado:

```text
render_simulado.py --write = PASS
arquivos renderizados      = 561
git diff --check            = PASS
derivado versionado        = PASS
validate_assistant.py       = PASS
falhas estruturais          = 0
avisos estruturais          = 0
worktree final              = CLEAN
branch_vs_main              = 0 behind / 25 ahead
```

As mudanças do renderer ficaram restritas ao derivado esperado da SE05: README/skill/contrato/manifest atualizados e os novos componentes `postflight` e `run_enforced`.

## Snapshot README

As contagens finais observadas após a materialização foram:

```text
helpers citados    = 96
markdown / links   = 223 / 1409
normas do molde    = 75
python (AST)       = 230
repo (identidade)  = 1563
repo (links)       = 2019
```

O snapshot raiz foi reconciliado com essas contagens. Como essa reconciliação altera apenas arquivos já existentes e não adiciona links, ela não muda a cardinalidade observada.

## Databricks Free

Ainda não executado para a SE05.

Estado atual:

```text
DATABRICKS_FREE = NOT_RUN
```

O probe determinístico `SE05_FREE_PROBE_V1` foi preparado para execução posterior ao `FULL_SE05_LOCAL`.

## GitHub Actions

Nenhuma PR SE05 foi aberta durante desenvolvimento branch-first.

```text
GITHUB_ACTIONS = NOT_RUN
```

Isso é deliberado para preservar orçamento de CI; Actions só deve ser observado na release candidate.
