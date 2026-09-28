# G6.READ_ONLY_RECONCILE — bloqueio de autenticação

## Resultado observado

```text
G6_READ_ONLY_RECONCILE = BLOCKED_AUTHENTICATION
G6_FREEZE_SHA = c11c2dff07f0f7595ed545f32990e5d54f1fd583
G6_FREEZE_TREE = 15527a29db0e6bcefa639cfadd4d66eed1d32d83

auth describe:
  exit_code = 0
  status = error
  profile = DEFAULT
  host = https://dbc-72c8503a-bc27.cloud.databricks.com
  auth_type = databricks-cli

current-user me:
  exit_code = 1
  issue = INVALID_REFRESH_TOKEN

content verify = NOT_RUN
external writes = false
```

A tentativa parou antes de verificar o conteúdo remoto e não observou mismatch de produto.

## Classificação

```text
PRODUCT_MISMATCH_OBSERVED = false
REMOTE_EFFECT = NONE
AUTHENTICATION_BLOCKER = true
REFRESH_TOKEN_INVALID = true
READ_ONLY_ATTEMPT_RETRY_AUTHORIZED = false
```

A fase não deve ser repetida com a mesma credencial.

## Próxima ação possível

A documentação oficial do Databricks para OAuth user-to-machine define `databricks auth login` como o fluxo interativo que abre navegador e salva/atualiza um configuration profile. Como isso altera credenciais/configuração local, constitui remediação separada da reconciliação read-only.

Nenhum `auth login` está autorizado por este documento.
