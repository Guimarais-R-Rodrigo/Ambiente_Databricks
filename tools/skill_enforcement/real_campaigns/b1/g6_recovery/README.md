# G6 probe recovery — residual SER05 only

This package exists only because the first remaining-G6 probe-import attempt ended in a partial remote state.

It does **not** modify the frozen G6 package under `../g6/` and does not reopen the R10 product publisher.

Contract:

- `ser03_free_probe` is read-only and must already exist with exact normalized content;
- `ser05_l2_free_probe` may be absent (CREATE) or already exact (ALREADY_CORRECT);
- a divergent object fails closed;
- the SHA-bound directory must already exist;
- no mkdir, overwrite, cleanup or retry is implemented;
- any residual material write is only `ser05_l2_free_probe`;
- OAuth U2M token is obtained just-in-time through the already qualified R10 helper;
- the material request reuses the frozen R10 direct Python HTTP/1.1 transport;
- authorization is external, single-use and bound to the recovery package digest;
- if a failure occurs after write start and before readback proof, the effect is UNKNOWN.

Modes:

```text
--validate-local  # no remote access
--reconcile       # remote read-only; no authorization record consumed
--execute         # requires a new explicit residual-write authorization
```

Promotion, policy mutation, probe execution, Genie, cleanup, Ready and merge are outside this package.
