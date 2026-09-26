# G6 publisher R5 — partial remote failure

## Result

```text
G6_MINIMAL_REMOTE_PACKAGE_WRITE_R5 = FAIL
authorization_ref = issue#114:comment#5837135604
authorization_consumed = true
consumption_marker_present = true

preconditions = PASS
records = 2
writes_started = 2
write_success = 1
verification_pass = 1

created = 1
updated = 0
unknown = 1

first_failure =
domain-context-init: IMPORT_FAILED / connection error: PROTOCOL_ERROR
```

## Known remote effects

Confirmed created and readback-verified:
- `domain-context-readme`

Unknown effect:
- `domain-context-init`

Not run:
- remaining 15 manifest objects, including `policy`.

No retry, full verify, probe, Genie or cleanup was executed.

## Recovery rule

The consumed R5 authorization cannot be reused.

Because one object is confirmed written and one has unknown effect, no new write authorization should be proposed until a fresh read-only reconciliation establishes the actual remote state.

Preferred reconciliation is the existing canonical full content verifier rather than a new one-off implementation:

`tools/publicar_free.py --verify --conteudo`

This is a read-only remote operation and requires its own explicit authorization in this rollout.
