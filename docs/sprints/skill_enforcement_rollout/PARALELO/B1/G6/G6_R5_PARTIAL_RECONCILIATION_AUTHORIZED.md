# G6 R5 partial-state read-only reconciliation authorization

Authorization reference:

`issue#114:comment#5837331711`

```text
action = G6_R5_PARTIAL_STATE_READ_ONLY_RECONCILIATION
effect = NONE
mechanism = tools/publicar_free.py --verify --conteudo
target_profile = FREE
target_host = https://dbc-72c8503a-bc27.cloud.databricks.com
remote_writes = false
```

Authorized:
- inventory/list/status;
- export/read;
- full content comparison;
- local JSON evidence outside the repository.

Not authorized:
- publication/import;
- overwrite;
- mkdirs;
- delete/cleanup;
- probes;
- Genie;
- repository policy mutation;
- promotion;
- Ready;
- merge.

The consumed R5 material authorization `issue#114:comment#5837135604` is not reusable.
