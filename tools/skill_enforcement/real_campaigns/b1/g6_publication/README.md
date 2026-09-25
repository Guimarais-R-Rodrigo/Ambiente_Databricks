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
