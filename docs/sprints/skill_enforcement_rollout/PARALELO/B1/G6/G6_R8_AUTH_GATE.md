# G6 R8 convergent POST publisher — remote authorization gate

Candidate identity:

```text
freeze_sha = 607a4272a34e896c38192094bf24821494d32328
freeze_tree = 561ec2fe75b75535f8fed459341cfeaf8992167d
manifest_sha256 = 067e05e6f228efddbf963edf02a0059108a6a58fc97be4441087d23e5be4ca3a
publisher_package_sha256 = c72711ee0cdecbb0ebc6d9db64ed68bd062c2bec0c88fad28357a323d356319e
target_profile = FREE
target_host = https://dbc-72c8503a-bc27.cloud.databricks.com
candidate_objects = 16
effect = REMOTE_PACKAGE_WRITE
one_write_attempt = true
```

Convergent rules:
- missing create candidate -> CREATE;
- exact existing candidate -> ALREADY_CORRECT and skip;
- divergent existing candidate -> fail closed;
- policy at authorized stale hash -> OVERWRITE;
- policy already at current local hash -> ALREADY_CORRECT;
- policy at another hash -> fail closed.

Not authorized by this document:
- remote execution;
- full republish;
- retry after material authorization consumption;
- directory creation;
- probes;
- Genie;
- cleanup/delete;
- repository policy mutation;
- promotion;
- Ready;
- merge.
