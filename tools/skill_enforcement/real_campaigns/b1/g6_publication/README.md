# G6 corrective minimal publication package

This package is deliberately outside `g6/` so the validated G6 freeze remains byte-identical.

It implements only the 17-object corrective delta proven by mismatch forensics:
- 16 objects that must still be absent remotely before their one-time create;
- one stale `policy.json` whose remote normalized SHA-256 must still equal the historical observed hash before overwrite.

Local validation:

```powershell
python -B -m tools.skill_enforcement.real_campaigns.b1.g6_publication.minimal_publish --validate-local
python -B -m unittest tools.tests.test_ser_b1_g6_publication -v
```

Remote execution is not authorized by this package. `--execute` additionally requires an external authorization record bound to the exact manifest SHA-256, the exact 17 object IDs, target FREE host, one-attempt semantics, and effect `REMOTE_PACKAGE_WRITE`.

The publisher fails closed:
- all 17 remote preconditions are checked before the first write;
- each precondition is checked again immediately before its own write;
- missing objects are imported without overwrite;
- only the stale policy object may use overwrite;
- every successful write is exported and hash-verified immediately;
- first failure stops remaining writes;
- the output requires a separate full `publicar_free.py --verify --conteudo` after a successful run.

No probe, Genie, cleanup, policy promotion, Ready or merge is part of this package.

## R2 missing-object proof

R1 stopped before the first write because the missing proof depended on a literal CLI error token. R2 uses structured parent-directory listing instead: a target is considered missing only after get-status does not succeed and a successful JSON workspace list of its parent omits the exact target path. Parent-list failure or malformed output remains fail-closed.

R1 authorization is consumed and cannot be reused.

## R3 adversarial hardening

R2 local PASS is preserved. Before another remote attempt, R3 hardens the whole publisher class: list payload variants, missing-parent recursion, parent DIRECTORY preconditions, RAW FILE import/export, post-write object-type checks, normalized host/corporate guard, authorization V2 bound to executable package digest and ordered object set, external auth record, atomic one-write-attempt consumption, and UNKNOWN effect after write start when success is not known.

The 17-object manifest remains byte-identical. R3 requires a new local qualification and a new human authorization.

R3 also includes mocked end-to-end state-machine tests: all 17 records succeeding, a remote-precondition failure that must not consume the write authorization, and an exception after write start that must mark the effect UNKNOWN and stop immediately.

## R4 explicit adversarial coverage closure

R3 functional guards passed locally, but qualification correctly failed because four required negative classes were not represented by explicit tests. R4 adds direct regressions for invalid workspace-list JSON, non-object list rows, authorization symlink rejection, and manifest-digest drift. It also versions `adversarial_coverage.json` and a metatest that requires the named regression methods to remain present.

No publisher functional code or 17-object manifest changed in R4.

## R5 export protocol correction after real Free preflight

The three authorized parent directories were successfully created and verified. R4 then stopped before any package write because the Free workspace rejected FILE export with `format=RAW` when the CLI requested JSON/base64 (`direct_download=false`).

R5 preserves:
- FILE **import** as `RAW` to prevent notebook inference;
- notebook import/export as `SOURCE/PYTHON`;
- exact 17-object manifest;
- parent-directory preconditions;
- authorization V2 and atomic consumption.

R5 changes FILE **export/readback** to `AUTO`, which is the protocol already used by the canonical `tools/publicar_free.py` content verifier that previously compared the remote package. Safety is preserved by requiring `get-status object_type=FILE` before every FILE readback, including the stale-policy precondition.

The existing R4 write authorization is bound to the R4 executable digest and therefore cannot authorize R5. R5 requires its own local qualification, package digest, freeze, and explicit remote authorization.

## R6 residual publisher after R5 partial-state reconciliation

The canonical read-only reconciliation resolved the R5 transport uncertainty:
- `domain-context-readme` is present, FILE, and content-correct;
- `domain-context-init` was not created;
- 15 objects remain missing;
- `policy.json` remains the expected historical stale revision;
- no wrong types or unexplained read errors exist.

R6 therefore removes `domain-context-readme` from the material-write manifest and binds the residual manifest to sanitized reconciliation evidence SHA-256 `d255398df799f0262872db4b5b327cb4dc3b9be67178746923a009138f702435`.

The publisher validator no longer hardcodes 17/16/1. Counts are declared by the closed manifest and mechanically checked against the entries. R6 currently declares 16 total objects: 15 create-if-missing plus one conditional policy overwrite.

This makes the publisher reusable for a shrinking residual set without another code change solely for count changes.

## R7 convergent recovery after repeated RAW .py transport failure

R6 again failed on the first `domain-context-init.py` import with `PROTOCOL_ERROR`, after all preconditions passed. This is the second independent occurrence on the same RAW Python workspace file. R7 therefore removes the CLI multipart `workspace import --file` path.

R7 uses the officially supported generic CLI API request:

`databricks api put /api/2.0/workspace/import --json <payload>`

The request body carries base64 `content`, explicit `RAW` for FILE, `SOURCE/PYTHON` for notebook, and explicit overwrite only for the policy update.

R7 also becomes convergent:
- create candidates use `MISSING_OR_EXACT_CONTENT`;
- policy uses `REMOTE_STALE_OR_EXACT_LOCAL`;
- a candidate that already exists with the exact expected type/content is `ALREADY_CORRECT` and skipped without a write;
- an existing create candidate with divergent content/type still fails closed;
- policy already at local-current content is skipped;
- only actually required material writes consume authorization.

This means a future transport-unknown effect can be safely reconciled by the next authorized execution's preflight without requiring a new residual manifest solely to determine whether an object landed.

## R8 canonical Workspace Import method correction

The authorized R7 attempt preserved all convergent preconditions but failed on its first material write because Workspace Import was invoked with `api put`, producing `PROTOCOL_ERROR`; its authorization is consumed and must not be reused.

R8 changes only the material transport method to the canonical Workspace Import request:

`databricks api post /api/2.0/workspace/import --json <payload>`

The convergent classifiers, inline JSON/base64 payload, FILE `RAW`, notebook `SOURCE/PYTHON`, conditional policy overwrite, authorization V2, atomic consumption, readback and UNKNOWN handling remain unchanged. R8 remote execution requires a new explicit authorization.
