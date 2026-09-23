# MM01 — Local Certification v1 — tentativa 9

Data: 2026-09-23

Status do executor: **PASS**

Status de sanitização: **PASS**

Status Unicode streaming: **PASS**

Status para freeze final: **NÃO VIGENTE APÓS DRIFT POSTERIOR DA MAIN**

## Identidade certificada

A R9 foi executada uma única vez sobre:

- HEAD `a5bb60a27ad8b0ab5cb8953642efbcdb14211328`;
- tree `5229d70b75000c8697fcd8409954e5a99c9b11f8`;
- `origin/main` e merge-base `11851e137dd7793b351ac08fc211c0be90005dee`;
- `ahead_by=189`;
- `behind_by=0`;
- worktree limpa;
- checkout não shallow.

Manifest:

- `status=PASS`;
- `preflight_ok=true`;
- `postflight_ok=true`;
- `failure=null`;
- `same_as_preflight=true`.

## Gates

Foram registrados exatamente 50 steps:

- 49 `PASS`;
- somente `V12_SCOPE_STRICT=SKIP_ALLOWED`;
- nenhum required step ausente ou extra.

Passaram, entre outros:

- `CERT_SELFTEST=18/18`;
- `MM01_CANONICAL=47/47`;
- `MM01_R02=3/3`;
- `MM01_R03=1/1`;
- `MM01_VALIDATE_ASSISTANT=PASS`;
- `CI_LOCAL=PASS`, 10/10 subgates;
- V00, V01, V02, V10, V11, V12 e V13;
- regressões V10/V11/V12/V13: 742 testes por rodada, com 9 skips internos de escopo/plataforma.

No CI local:

- `sef=OK`;
- `infrastructure_errors=[]`;
- nenhum WinError32 foi observado.

Classificação:

`WINERROR32_R9=NOT_REPRODUCED`

Isso não declara root cause corrigida.

## Snapshot e evidência

A R9 confirmou:

- `repo (identidade)=1680`;
- `repo (links)=2109`;
- `worktree (extras)=0`.

Os 17 hashes críticos foram idênticos no preflight e postflight.

Os nove workflows-fonte apresentaram blobs iguais aos pins e zero snippets ausentes.

## Bundle

ZIP SHA-256:

`74d39f615fc1507653f74b7ed87972c83aad6f14b1e1738eee6e6ce8a2fcd776`

Verificação independente:

- 55 entries;
- 54/54 checksums válidos;
- nomes e hashes coerentes;
- zero decode errors UTF-8;
- zero HOME/REPO real em formas literal/escapada;
- zero `ghp_` ou `github_pat_`;
- zero U+FFFD;
- zero `UnicodeEncodeError`;
- zero `UnicodeDecodeError`;
- zero `ERROR_UNRECORDED`.

Logo:

- `MECHANICAL_CERTIFICATION=PASS`;
- `BUNDLE_SANITIZATION=PASS`;
- `UNICODE_STREAMING=PASS`;
- `WINERROR32_R9=NOT_REPRODUCED`.

## Drift posterior da main

Depois da conclusão da R9, a `main` avançou de `11851e137dd7793b351ac08fc211c0be90005dee` para `515e673b17f21d4c912d9ae866a7e31967fd4488` pela integração da PR #102.

Esse delta alterou:

- `tools/tests/test_certify_storage_cleanup.py`;
- `tools/tests/test_se08_windows_corrective.py`;
- `CHANGELOG.md`;
- `README.md`.

A corretiva é transversal e diretamente relacionada à instrumentação de storage/WinError32. Por isso, embora a R9 permaneça um PASS válido para seu baseline congelado, ela não pode ser usada como certificação final contra a `main` vigente.

A branch MM01 foi posteriormente reconciliada com a nova `main` por merge operacional real. Uma nova certificação integral é obrigatória sobre o SHA pós-reconciliação.

A R9 não reclassifica nenhuma tentativa anterior.
