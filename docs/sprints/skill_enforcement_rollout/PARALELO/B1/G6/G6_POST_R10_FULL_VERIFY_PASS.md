# G6 pós-R10 — full content verify PASS

## Veredito do subgate

```text
G6_POST_R10_FULL_CONTENT_VERIFY = PASS
EFFECT = NONE
REMOTE_WRITES = 0
REPO_MUTATION = false
```

**Escopo:** este PASS encerra o subgate read-only de inventário/tipos/conteúdo após a publicação R10. Ele **não encerra o G6 agregado**. O G6 congelado também exige os dois probes Free e a coleta Genie definida no `external_manifest.json`, seguida de `verify_external_results.py`.

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

Os 17 objetos críticos do lote B1 aparecem no relatório. O hash reportado de `policy.json` é `957a8a4d30d2d1c04b0ec4a3c079e2fa784b24c512dc90386aa686f7cdf69d9d`, igual ao conteúdo local corrente usado pelo publisher R10.

## Segurança e autoridade

- `remote_writes = 0` neste subgate;
- publisher R10 não foi reexecutado;
- authorization record R10 permaneceu `CONSUMED_UNTOUCHED`;
- promotion = NOT_RUN;
- Genie = NOT_RUN;
- Ready = NOT_RUN;
- merge = NOT_RUN.

## Próxima condição do G6 agregado

Ainda são obrigatórios, sob autorização específica de seus efeitos:

1. criar/importar exatamente dois notebooks-probe temporários SHA-bound;
2. executar cada probe Free uma única vez;
3. executar as 20 variantes Genie congeladas, em chat novo por variante;
4. validar os outputs com `verify_external_results.py`.

Cleanup dos dois probes é efeito separado e opcional para o PASS do G6.

Enquanto esses canais permanecerem NOT_RUN:

```text
G6_EXTERNAL = IN_PROGRESS
G7_PROMOTION_PROPOSAL = NOT_AUTHORIZED
```
