# MM01 — Local Certification v1 — tentativa 6

Data: 2026-09-23

Status: **MECHANICAL_FAIL / BUNDLE_SANITIZATION_PASS**

## Preparação

O checkout local foi primeiro fast-forwarded de `3e3e105f60e92f6ca58502cf0c92f4f461a84b04` para o HEAD remoto canônico `94ba596ca4385223248a102b9ff02c0252491c88`, com worktree limpa e sem criação de commits locais.

## Falha

A execução canônica R6 foi iniciada uma única vez e falhou antes do preflight e antes de qualquer step porque o certifier encontrou resíduos gerados preexistentes e ignorados pelo Git:

- `.artifacts/v10-app`;
- `tools/readme_visuals/node_modules`.

Manifest:

- `status=FAIL`;
- `preflight_ok=false`;
- `postflight_ok=false`;
- zero steps executados.

A worktree versionada permaneceu limpa e a identidade Git permaneceu:

- HEAD `94ba596ca4385223248a102b9ff02c0252491c88`;
- main/merge-base `11851e137dd7793b351ac08fc211c0be90005dee`;
- `ahead_by=181`;
- `behind_by=0`.

## Bundle

ZIP R6:

`a236aa9d30a59b9b62aa3523ecb4a741eb86385a77d5ac585be8d45f999ae884`

O pequeno bundle de falha passou a verificação de sanitização, mas isso não prova a sanitização do caminho completo porque nenhum log de gate foi produzido.

## Tratamento

Nenhuma mudança de código foi necessária para esse finding.

Antes da rodada seguinte, os dois resíduos conhecidos foram inspecionados, confirmados como ignorados e sem arquivos versionados e removidos exclusivamente do checkout dedicado.

A R6 permanece FAIL histórico e não é reclassificada.
