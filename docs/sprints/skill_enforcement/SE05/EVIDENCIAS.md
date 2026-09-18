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

## Certificação local final

No HEAD funcional `0d4d6af630d2760c754313218f51cff0d6ad2375`:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE05_LOCAL
DERIVED_STALE       = false
failures            = 0
```

Todos os gates SE01–SE05, estrutura, renderer, render-diff e snapshot README passaram.

Evidence bundle:

```text
~/.ambiente_databricks/sef_certifications/20260918T002331Z_0d4d6af630d2
```

## Databricks Free

O HEAD funcional `0d4d6af630d2760c754313218f51cff0d6ad2375` foi publicado e verificado por conteúdo no workspace Free pessoal.

```text
arquivos controlados = 560
conteúdo              = 560/560
ausentes              = 0
obsoletos             = 0
plataforma            = 1 arquivo gerenciado (.assistant/.mcp_servers.json)
resultado             = APROVADO: 0 problema(s)
```

Relatório preservado:

```text
~/.ambiente_databricks/sef_certifications/se05_free_verify_0d4d6af630d2.json
```

O endpoint individual de import do probe retornou o `PROTOCOL_ERROR` de transporte já conhecido nas três tentativas. O fallback documentado por `workspace import-dir` passou, e o conteúdo exportado do notebook remoto ficou idêntico ao probe local.

### `SE05_FREE_PROBE_V1`

Resultado global:

```text
marker                      = SE05_FREE_PROBE_V1
status                      = PASS
published_package_mutated   = false
persistent_writes_performed = false
```

Casos:

```text
P01_l4_happy_path                        = PASS
P02_core_l3_cannot_finalize_l4           = PASS
P03_missing_required_input_fails_closed  = PASS
P04_incomplete_handoff_not_completed     = PASS
P05_completion_claim_tamper_detected     = PASS
```

No P01 foi observado:

```text
enforcement_status                 = PASS
receipt_present                    = true
postflight_status                  = PASS
completion_authorized              = true
completion_status                  = COMPLETED
verification_status                = VALID
verification_valid                 = true
verification_completion_authorized = true
completion_claim_consistent        = true
```

Nos P02–P05, nenhum cenário não canônico conseguiu autorização de completion. O P02 permaneceu `BLOCKED` e não-validável como finalização L4; o P03 terminou `FAIL` por input obrigatório ausente; o P04 terminou `REVIEW` por handoff incompleto; o P05 detectou adulteração como `INVALID`.

Classificação:

```text
DATABRICKS_FREE = PASS
```

## GitHub Actions

Nenhuma PR SE05 foi aberta durante desenvolvimento branch-first.

```text
GITHUB_ACTIONS = NOT_RUN
```

Isso é deliberado para preservar orçamento de CI; Actions só deve ser observado na release candidate.
