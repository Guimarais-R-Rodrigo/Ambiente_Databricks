# G6 direct HTTP/1.1 U2M publisher R10 — local PASS

```text
G6_DIRECT_HTTP11_U2M_PUBLISH_R10_LOCAL_VALIDATION = PASS
R10_FREEZE_SHA = b89cc5f1579caf8af6784ca5761c114fb6a6df09
R10_FREEZE_TREE = 45ddb0252795c6ba70fbbc04740346c1cfd082cc
MANIFEST_SHA256 = 067e05e6f228efddbf963edf02a0059108a6a58fc97be4441087d23e5be4ca3a
PUBLISHER_PACKAGE_SHA256 = b4c186b2838bfa04e6d5475d6a7d23561a8957b3fcea9539be612d11e032f0f6
METATESTS = 48/48 PASS
VALIDATE_ASSISTANT = PASS
COVERAGE = 25/25
REMOTE_ACCESS = NOT_RUN
REMOTE_EXECUTION = NOT_AUTHORIZED
```

R10 keeps the convergent manifest unchanged.

Material transport:
- OAuth U2M access token retrieved just-in-time via Databricks CLI auth token;
- token memory-only;
- material write via Python stdlib http.client HTTPSConnection;
- direct HTTP/1.1 POST to /api/2.0/workspace/import;
- exactly one request per material object;
- no automatic retry;
- no material workspace write through the Databricks CLI.

R9 remains historical BLOCKED_DEPENDENCY and R8 remains historical FAIL with its authorization consumed.
