# G6 pós-R10 — full content verify PASS

## Veredito

```text
G6_POST_R10_FULL_CONTENT_VERIFY = PASS
G6_EXTERNAL = PASS
EFFECT = NONE
REMOTE_WRITES = 0
REPO_MUTATION = false
```

Bundle auditado: `G6_POST_R10_FULL_VERIFY_EVIDENCE_20260926.zip`

SHA-256 do bundle:

`1d593b6859d5b97c33454be395b94513fd1ffa7912bfd08249637fc636b3d34c`

## Identidade

- source commit: `7d0a2656345e596ff735332acc22d1c18d9e8758`
- source tree: `81587c74c60577aefd733e5711ac2651dbb16669`
- profile: `FREE`
- host: `https://dbc-72c8503a-bc27.cloud.databricks.com`
- scope: `inventory-types-content`
- verify invocations: 1
- exit code: 0

## Resultado

```text
files_compared = 590
file_records = 590
errors = 0

MISSING_REMOTE = 0
OBSOLETE_REMOTE = 0
OBJECT_TYPE_MISMATCH = 0
CONTENT_DIVERGENCE = 0
REMOTE_READ_INCOMPLETE = 0
SOURCE_MIRROR_DRIFT = 0
AUTH_OR_TARGET_FAILURE = 0
OTHER = 0
```

Package hashes:

- raw: `576134eb3e8d5c6d52be306a35351960df3be2ecb2b1b4602749864f5cca16ff`
- normalized: `5ac3db2f3104c6829e3d17314ef386afcd7e4b3ce6cc095db75e044318fe332f`

## Auditoria independente do bundle

O ZIP contém somente:

- `full_content_verify.json`
- `SUMMARY.json`
- `GIT_STATE.txt`

Não há path traversal nem entrada symlink.

Os 590 paths são únicos e os 590 records possuem `path`, `raw_sha256`, `normalized_sha256` e `type` válidos.

Os dois hashes agregados foram recomputados a partir dos registros usando a mesma ordenação de `Path` do host Windows (`PureWindowsPath`) e coincidem exatamente com o relatório.

A varredura sanitizada não encontrou valores de:

- `Authorization: Bearer`
- `access_token`
- `refresh_token`
- token JWT-like

Os 17 objetos críticos do lote B1 aparecem no relatório, incluindo o README já correto, os 15 objetos criados na R10 e `policy.json`. O hash reportado de `policy.json` é `957a8a4d30d2d1c04b0ec4a3c079e2fa784b24c512dc90386aa686f7cdf69d9d`, igual ao conteúdo local corrente usado pelo publisher R10.

## Segurança e autoridade

- `remote_writes = 0` neste gate;
- publisher R10 não foi reexecutado;
- authorization record R10 permaneceu `CONSUMED_UNTOUCHED`;
- promotion = NOT_RUN;
- Genie = NOT_RUN;
- Ready = NOT_RUN;
- merge = NOT_RUN.

O G6 está encerrado. O próximo gate é G7, que prepara before/after, riscos e rollback e exige autorização humana específica antes de qualquer mutação de `policy.json`.
