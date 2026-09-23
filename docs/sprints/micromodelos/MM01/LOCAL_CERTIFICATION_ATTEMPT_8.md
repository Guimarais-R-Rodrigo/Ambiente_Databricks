# MM01 — Local Certification v1 — tentativa 8

Data: 2026-09-23

Status: **MECHANICAL_FAIL / BUNDLE_SANITIZATION_PASS / UNICODE_STREAMING_PASS**

## Identidade

A R8 foi executada uma única vez sobre:

- HEAD `a5bb60a27ad8b0ab5cb8953642efbcdb14211328`;
- tree `5229d70b75000c8697fcd8409954e5a99c9b11f8`;
- `origin/main` e merge-base `11851e137dd7793b351ac08fc211c0be90005dee`;
- `ahead_by=189`;
- `behind_by=0`;
- worktree versionada limpa;
- merge-ref materialmente equivalente ao HEAD.

## Gates

Passaram:

- cinco bootstraps;
- `CERT_SELFTEST=18/18`;
- `MM01_CANONICAL=47/47`;
- `MM01_R02=3/3`;
- `MM01_R03=1/1`;
- `MM01_VALIDATE_ASSISTANT=PASS`, 0 falhas / 0 avisos;
- snapshot `1680/2109/0`;
- preflight e workflow pins.

O hardening de encoding pós-R7 funcionou:

- zero `UnicodeEncodeError`;
- zero `UnicodeDecodeError`;
- zero `ERROR_UNRECORDED`;
- zero U+FFFD nos arquivos textuais do bundle;
- todos os arquivos textuais UTF-8 válidos.

## Falha

`CI_LOCAL` reprovou exclusivamente no subgate SEF.

A regressão `test_timeout_real_parent_child_external_oracle_and_partial_streams` encontrou:

`PermissionError: [WinError 32]`

durante a remoção do arquivo temporário `stderr` no Windows.

O histórico SE08 já classificava WinError32 como intermitente e sem root cause estabelecida. Foi confirmado que os blobs de `tools/skill_enforcement/certify_local.py` e `tools/tests/test_certify_local.py` eram idênticos entre MM01 e `main`, portanto não foi introduzida corretiva SEF dentro da MM01.

## Bundle

SHA-256:

`8d2242f36213d34d7ca80b22ad4d324685927a1a205334f27ffc414240352b24`

Verificação independente:

- 16/16 checksums internos válidos;
- `BUNDLE_SANITIZATION=PASS`;
- zero leaks HOME/REPO literal ou escapado;
- zero padrões GitHub token não redigidos;
- `UNICODE_STREAMING=PASS`.

A R8 permanece FAIL histórico e não reclassifica qualquer rodada anterior.
