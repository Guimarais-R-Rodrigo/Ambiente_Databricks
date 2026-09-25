# G6 — gate de remediação de autenticação

## Estado

```text
AUTH_REMEDIATION = PREPARED_NOT_AUTHORIZED
REMOTE_WORKSPACE_WRITE = false
LOCAL_CREDENTIAL_MUTATION = true
```

## Objetivo proposto

Restabelecer autenticação OAuth U2M exclusivamente para o workspace pessoal Free e profile `FREE`, sem executar qualquer leitura de produto ou escrita no workspace durante a própria remediação.

Target:

```text
profile = FREE
host = https://dbc-72c8503a-bc27.cloud.databricks.com
```

## Sequência proposta

1. listar profiles existentes de forma read-only;
2. registrar somente nomes/hosts/status sanitizados;
3. executar uma única vez o login interativo:
   `databricks auth login --host https://dbc-72c8503a-bc27.cloud.databricks.com --profile FREE`;
4. completar a autenticação no navegador;
5. validar `auth describe --profile FREE`;
6. validar `current-user me --profile FREE`;
7. parar.

Não executar `publicar_free.py`, verify de conteúdo, publicação, import, probes, Genie ou cleanup nesta mesma fase.

Após PASS da remediação, a reconciliação read-only ganha uma nova tentativa explícita; a tentativa bloqueada anterior permanece histórica.
