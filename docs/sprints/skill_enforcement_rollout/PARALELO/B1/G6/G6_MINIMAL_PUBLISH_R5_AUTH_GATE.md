# G6 minimal publisher R5 — remote authorization gate

Candidate:

```text
publisher_freeze_sha = 66f531dacbbd67ac972812a0057c932183c1aba1
publisher_freeze_tree = fcfcc03a7d38cdd4e14a821a382b2a88c1781811
manifest_sha256 = 57574ddbdadfd344776bcb2b37142248b9af95671d5efd818a4dda6bcae6ae9e
publisher_package_sha256 = 774c4351e48becb4ccdcf13a375aedec635718c3c2c8dd7eb6f447e47e87ce62
target_profile = FREE
target_host = https://dbc-72c8503a-bc27.cloud.databricks.com
effect = REMOTE_PACKAGE_WRITE
objects = 17
one_write_attempt = true
parent_bootstrap = ALREADY_DONE_3_OF_3
```

Any R5 authorization must bind all values above and the exact ordered 17 object IDs.

No new mkdirs is required or authorized by this gate.

Still excluded:
- full republish;
- retry after material write consumption;
- extra directories;
- probes;
- Genie;
- cleanup/delete;
- repository policy mutation;
- promotion;
- Ready;
- merge.
