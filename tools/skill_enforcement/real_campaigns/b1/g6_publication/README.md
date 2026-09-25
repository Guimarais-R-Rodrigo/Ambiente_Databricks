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
