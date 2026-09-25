# G6 local package validation — R1 FAIL preservado

## Identidade

```text
candidate_sha = 814ae6f3286b367f45173b9b36b426317f9806e3
candidate_tree = 7110eea3df2e0c9a281e98a16cbe24f55e3d129c
G6_LOCAL_01_VALIDATE_PACKAGE = PASS
G6_LOCAL_02_METATESTS = FAIL
tests_observed = 6
failures = 1
errors = 0
skips = 0
```

Primeira falha:

`test_cleanup_is_separate_effect_and_not_pre_authorized`

O manifest já declarava:
- efeito separado `TEMPORARY_WORKSPACE_OBJECT_DELETE`;
- `authorized=false`;
- prerequisite: autorização separada somente após outputs/export evidence preservados e auditados.

O teste, porém, exigia a substring literal `"after evidence"`, ausente porque o texto dizia `"after outputs/export evidence are preserved and audited"`.

## Classificação

```text
G6_PACKAGE_SEMANTIC_DEFECT = false
G6_AUTHORITY_DEFECT = false
TEST_ORACLE_TEXTUAL_BRITTLENESS = true
REMOTE_EXECUTION = NOT_RUN
FREEZE = NOT_CREATED
```

R1 permanece FAIL e não deve ser reexecutada.

## Corretiva R2

A corretiva substitui o oráculo textual por campos estruturais no manifest:

```json
{
  "requires_evidence_preserved": true,
  "requires_separate_authorization": true
}
```

O validator e o metateste passam a exigir esses campos. O texto narrativo de prerequisite continua informativo, mas deixa de ser autoridade mecânica.
