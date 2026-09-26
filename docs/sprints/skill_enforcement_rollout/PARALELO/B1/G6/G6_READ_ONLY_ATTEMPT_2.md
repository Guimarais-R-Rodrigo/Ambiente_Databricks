# G6.READ_ONLY_RECONCILE — tentativa 2

## Autoridade

Reusa a autorização existente:

`issue#114:comment#5834465790`

Ela continua vinculada ao mesmo freeze e ao mesmo efeito `NONE`.

```text
freeze_sha = c11c2dff07f0f7595ed545f32990e5d54f1fd583
freeze_tree = 15527a29db0e6bcefa639cfadd4d66eed1d32d83
auth_remediation = PASS
attempt_1 = BLOCKED_AUTHENTICATION / preserved
attempt_2 = AUTHORIZED_NOT_RUN
```

## Escopo

Permitido:
- `auth describe --profile FREE`;
- `current-user me --profile FREE`;
- `publicar_free.py --verify --conteudo`;
- evidência local sanitizada.

Proibido:
- publicação;
- import;
- probes;
- Genie;
- cleanup;
- policy;
- promoção;
- Ready;
- merge.

Se o verify remoto divergir, a tentativa termina em `REMOTE_CONTENT_MISMATCH`. Nenhuma escrita corretiva é autorizada.
