# G6 OAuth remediation — PASS

## Resultado

```text
G6_AUTH_REMEDIATION = PASS
authorization_ref = issue#114:comment#5834668546
freeze_sha = c11c2dff07f0f7595ed545f32990e5d54f1fd583

target profile = FREE
target host = https://dbc-72c8503a-bc27.cloud.databricks.com

PRE_AUTH:
  exit_code = 0
  profile = FREE
  host_match = true
  authentication_valid = true

OAUTH_LOGIN:
  exit_code = 0

POST_AUTH:
  exit_code = 0
  profile_match = true
  host_match = true
  authentication_valid = true

CURRENT_USER:
  exit_code = 0
  resolved = true
```

## Efeitos

```text
workspace_write_performed = false
content_verify_performed = false
publication_performed = false
probe_import_performed = false
probe_execution_performed = false
genie_performed = false
cleanup_performed = false
```

A remediação encerrou após autenticação, como autorizado.

A tentativa 1 de `G6.READ_ONLY_RECONCILE` continua histórica como `BLOCKED_AUTHENTICATION`. O PASS da remediação habilita uma nova tentativa explícita da mesma fase read-only; não reclassifica a tentativa 1.
