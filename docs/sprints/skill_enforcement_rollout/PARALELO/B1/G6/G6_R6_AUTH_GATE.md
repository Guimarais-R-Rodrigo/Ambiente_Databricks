# G6 R6 residual publisher — remote authorization gate

Candidate:

```text
publisher_freeze_sha = d583c495baed2ab5f2f96453b69232ec3ad30be7
publisher_freeze_tree = 31aedaf256cc6ef1eea5a03412825df313eb747d
manifest_sha256 = 1115e497852c2290dae0c5f1ec247df0de9f19e92e89385cc3f1659855d2cf9e
publisher_package_sha256 = a4f838c64d5e4f3ad902a401ab52b642e10c8d22eadde9e19e61bb647d16181f
residual_evidence_sha256 = d255398df799f0262872db4b5b327cb4dc3b9be67178746923a009138f702435
target_profile = FREE
target_host = https://dbc-72c8503a-bc27.cloud.databricks.com
effect = REMOTE_PACKAGE_WRITE
objects = 16
missing = 15
conditional_overwrite = 1
one_write_attempt = true
```

The exact ordered residual object IDs are the R6 manifest entries. `domain-context-readme` is excluded and must not be rewritten.

The three parent directories already exist and are not part of this gate.

Still excluded:
- full republish;
- retry after material write consumption;
- directory creation;
- probes;
- Genie;
- cleanup/delete;
- repository policy mutation;
- promotion;
- Ready;
- merge.
