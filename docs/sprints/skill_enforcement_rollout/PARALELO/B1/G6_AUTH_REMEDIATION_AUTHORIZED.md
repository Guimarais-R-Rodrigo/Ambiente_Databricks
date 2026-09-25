# G6 — autorização para remediação OAuth U2M

Autorização humana registrada em:

`issue#114:comment#5834668546`

Escopo exato:

```text
profile = FREE
host = https://dbc-72c8503a-bc27.cloud.databricks.com
local credential/config mutation = AUTHORIZED
remote workspace write = NOT_AUTHORIZED
```

A fase pode renovar OAuth U2M e validar `auth describe` + `current-user me`. Ela termina imediatamente após essas verificações.

Não executar verify de conteúdo, publicação, import, probes, Genie, cleanup, policy, promoção, Ready ou merge.
