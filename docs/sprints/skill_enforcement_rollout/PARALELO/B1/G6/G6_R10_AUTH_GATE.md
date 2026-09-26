# G6 R10 remote authorization gate

```text
publisher_freeze_sha = b89cc5f1579caf8af6784ca5761c114fb6a6df09
publisher_freeze_tree = 45ddb0252795c6ba70fbbc04740346c1cfd082cc
manifest_sha256 = 067e05e6f228efddbf963edf02a0059108a6a58fc97be4441087d23e5be4ca3a
publisher_package_sha256 = b4c186b2838bfa04e6d5475d6a7d23561a8957b3fcea9539be612d11e032f0f6
target_profile = FREE
target_host = https://dbc-72c8503a-bc27.cloud.databricks.com
effect = REMOTE_PACKAGE_WRITE
candidate_objects = 16
one_write_attempt = true
material_transport = PYTHON_HTTP_CLIENT_HTTP11
auth_source = DATABRICKS_CLI_U2M_TOKEN
automatic_retry = false
```

Convergent semantics remain unchanged:
- missing create candidate -> CREATE;
- exact existing type/content -> ALREADY_CORRECT;
- divergent existing object -> fail closed;
- stale policy -> OVERWRITE;
- policy already equal to local-current -> ALREADY_CORRECT.

No remote execution is authorized by this document.
