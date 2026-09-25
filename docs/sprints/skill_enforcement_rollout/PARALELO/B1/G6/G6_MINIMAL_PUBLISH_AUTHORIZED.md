# G6 minimal corrective publisher — human authorization

Authorization reference:

`issue#114:comment#5835957014`

Binding:

```text
publisher_freeze_sha = 74117255dedebde0b30ed027cab6494974240d83
publisher_freeze_tree = 88ba0bb4efa07867c8adea7ea65c6e690d12a288
manifest_sha256 = 57574ddbdadfd344776bcb2b37142248b9af95671d5efd818a4dda6bcae6ae9e
target_profile = FREE
target_host = https://dbc-72c8503a-bc27.cloud.databricks.com
effect = REMOTE_PACKAGE_WRITE
one_attempt = true
object_count = 17
```

Authorized:
- 16 create-if-missing objects from the frozen manifest;
- 1 conditional overwrite of `policy.json`, only while its remote normalized SHA-256 remains the forensically observed historical value;
- per-object readback/hash verification after each successful write.

Not authorized:
- full republish;
- write retry;
- probes;
- Genie;
- cleanup;
- repository policy mutation;
- promotion;
- Ready;
- merge.

Execution status remains `NOT_RUN`.
