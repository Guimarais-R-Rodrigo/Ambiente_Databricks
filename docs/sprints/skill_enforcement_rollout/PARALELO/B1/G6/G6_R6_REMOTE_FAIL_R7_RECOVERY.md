# G6 R6 remote failure and R7 recovery

R6:
```text
result = FAIL
authorization_ref = issue#114:comment#5837785336
authorization_consumed = true
preconditions = PASS
records = 1
writes_started = 1
write_success = 0
unknown = 1
first_failure = domain-context-init: IMPORT_FAILED / PROTOCOL_ERROR
```

The failure repeated the same RAW Python file transport symptom observed in R5.

R7 replaces `workspace import --file` with official `api put /api/2.0/workspace/import` JSON/base64 requests and introduces convergent preconditions so an already-correct object is skipped rather than treated as a blocker.

No R7 remote execution is authorized by this document.
