# G6 — gate humano para reconciliação read-only

Este documento não é autorização. Ele descreve a primeira autorização externa possível após o freeze G6.

## Operações incluídas

Somente no workspace pessoal/Free:
- `databricks auth describe -o json`;
- `databricks current-user me -o json`;
- confirmar profile/host pessoal e não corporativo;
- `tools/publicar_free.py --verify --conteudo` com profile/host explícitos;
- preservar outputs sanitizados.

## Operações excluídas

Esta autorização NÃO incluiria:
- `publicar_free.py --execute`;
- criação/importação de notebooks;
- execução dos probes Free;
- criação de chats Genie;
- remoção de notebooks temporários;
- alteração de policy;
- promoção;
- Ready;
- merge.

## Stop rule

Se o conteúdo remoto divergir do pacote local protegido, a fase termina em mismatch observado. Não publicar ou sobrescrever automaticamente.

## Estado

```text
AUTHORIZATION_REQUESTED_FOR = G6.READ_ONLY_RECONCILE
DECISION = PENDING_HUMAN
EFFECT = NONE
```
