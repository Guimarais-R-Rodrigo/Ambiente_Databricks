# G6 R5 partial-state read-only reconciliation — PASS

```text
authorization_ref = issue#114:comment#5837331711
effect = NONE
verify_exit_code = 1
verify_status = FAIL
scope = inventory-types-content
files_compared = 575
raw_error_count = 31

MISSING_REMOTE = 15
INCOMPLETE_REMOTE_READ = 15
DIVERGENT_CONTENT = 1
wrong_type/read_error/other = 0

domain-context-readme = CONFIRMED_CORRECT
domain-context-init = NOT_CREATED
remote_residual_state = SIMPLE_RESIDUAL
sanitized_evidence_sha256 = d255398df799f0262872db4b5b327cb4dc3b9be67178746923a009138f702435
```

The remote verifier correctly remains FAIL because 16 logical residual objects remain. The reconciliation itself is PASS because it produced complete read-only evidence and resolved the R5 unknown effect.
