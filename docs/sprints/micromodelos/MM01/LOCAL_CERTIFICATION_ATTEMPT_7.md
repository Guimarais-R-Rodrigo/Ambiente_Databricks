# MM01 — Local Certification v1 — tentativa 7

Data: 2026-09-23

Status: **MECHANICAL_FAIL / BUNDLE_SANITIZATION_PASS**

## Identidade

A R7 foi executada sobre:

- HEAD `94ba596ca4385223248a102b9ff02c0252491c88`;
- tree `63b95857a232c11f9418836b737d60c46cf92b90`;
- main/merge-base `11851e137dd7793b351ac08fc211c0be90005dee`;
- `ahead_by=181`;
- `behind_by=0`;
- worktree versionada limpa;
- merge-ref materialmente equivalente ao HEAD.

## Gates antes da falha

Passaram:

- cinco bootstraps;
- `CERT_SELFTEST`: 16/16;
- `MM01_CANONICAL`: 47/47;
- `MM01_R02`: 3/3;
- `MM01_R03`: 1/1.

O gate `MM01_VALIDATE_ASSISTANT` foi iniciado, mas não recebeu `StepResult`.

## Falha

Durante o streaming do validator ocorreu:

`UnicodeEncodeError: 'charmap' codec can't encode character '\ufffd'`

O subprocesso produziu bytes com acentuação em codificação Windows. O certifier os decodificou como UTF-8 com replacement, gerando `�`; em seguida, a retransmissão para o stdout do processo pai, configurado com encoding `charmap`, não conseguiu codificar esse caractere.

A exceção ocorreu no transporte/observabilidade do output e impediu registrar o resultado mecânico do validator. Por isso:

- `MM01_VALIDATE_ASSISTANT=ERROR_UNRECORDED`;
- CI_LOCAL e V00–V13 permaneceram `NOT_RUN`;
- `postflight_ok=false`.

## Bundle

ZIP R7:

`3d111258ac387b24f2426c21c4c92b8ecb61de59adea8eaaede207645a3ac3ff`

Foram validados 15/15 checksums internos. A inspeção de sanitização do bundle parcial encontrou zero ocorrências dos paths HOME/REPO em formas literal ou escapada e zero padrões de token GitHub não redigidos.

## Correção posterior

Foram introduzidas duas defesas complementares:

- subprocessos executados por `run_step` recebem `PYTHONUTF8=1` e `PYTHONIOENCODING=utf-8`, garantindo stdout Python determinístico em UTF-8;
- a emissão ao console usa fallback `backslashreplace` quando o encoding do terminal não representa algum caractere, impedindo que o tee derrube a certificação.

Regressões específicas cobrem:

- subprocesso Python com stdio UTF-8;
- console `cp1252` diante de caractere não representável.

Nenhum gate funcional, workflow ou critério da MM01 foi relaxado.

A R7 permanece FAIL histórico e não é reclassificada.
