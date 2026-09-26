# G6 minimal publisher R4 — remote write authorization gate

## Candidate

```text
publisher_freeze_sha = 3ef1f14e728338540a4426f297c90ee2f576ec92
publisher_freeze_tree = baecc5498c1a0fef63a7f8dfba21d615ca2b33df
manifest_sha256 = 57574ddbdadfd344776bcb2b37142248b9af95671d5efd818a4dda6bcae6ae9e
publisher_package_sha256 = 47f230f2ffef57510d1c92b7d94dac3ded766ccbba81368d4058ef2b78aaf7c9
effect = REMOTE_PACKAGE_WRITE
target_profile = FREE
target_host = https://dbc-72c8503a-bc27.cloud.databricks.com
objects = 17
one_write_attempt = true
```

A future authorization must bind all values above and the exact ordered object IDs.

R4 additionally enforces:
- authorization record outside the repo;
- atomic consumption immediately before first material write;
- no consumption on read-only preflight failure;
- 16 create-if-missing entries;
- one conditional policy overwrite;
- parent directory precondition;
- FILE RAW import/export;
- notebook SOURCE/PYTHON;
- readback type/language/hash;
- UNKNOWN effect after write start when success is not known.

No authorization is implied by this document.
