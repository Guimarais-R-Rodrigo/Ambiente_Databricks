# P2 R5 — prepare PASS, binding literal do Python rejeitado pelo handoff

## Identidade

- candidate: `3d9b2d84bb9a82635319aacf30e37a55c13b4f39`
- tree: `f5ef5db196fd8a10b2aabeb803908c9297c05375`
- host: Windows 10.0.26200 / NTFS
- ENV-04: PASS
- preflight: PASS
- metatestes: 19/19 PASS

## Primeira nova falha

```text
P2_R5_LOCAL_QUALIFICATION = FAIL
FIRST_NEW_FAILURE_R5 = P2_R5_03_PREPARE / VENV_PYTHON_BINDING_MISMATCH
```

O prepare retornou PASS e congelou CPython 3.12.10, mas `sys.executable` foi observado pelo processo Codex sob o path físico redirecionado de `LocalCache\Local\...`, enquanto o handoff externo exigia igualdade literal com o path autorizado em `%LOCALAPPDATA%\AmbienteDatabricks\venvs\...`.

Os três valores derivados do release/handoff usaram o path físico redirecionado. A campanha e o package não foram executados.

## Classificação

```text
CANDIDATE_DOMAIN_DEFECT = false
B0_SHARED_MECHANISM_DEFECT = false
ENV04_DEFECT = false
INTERPRETER_BINARY_MISMATCH_OBSERVED = false
INTERPRETER_PATH_VIRTUALIZATION = true
B1_RELEASE_IDENTITY_MODEL_DEFECT = true
```

R5 permanece FAIL e não deve ser reexecutada.

## R6

R6 separa:
- `python_executable`: launcher literal autorizado;
- `python_runtime_executable_observed`: path físico observado por `sys.executable`;
- SHA-256 do launcher;
- SHA-256 do runtime observado;
- versão;
- implementação;
- estado de isolamento.

O prepare exige `--python-launcher`, faz probe direto desse launcher e só congela o release se o probe selecionar o mesmo runtime físico, mesma versão/implementação/isolamento e mesmo SHA-256. O handoff executa o launcher autorizado; o adapter revalida o runtime físico e os hashes.
