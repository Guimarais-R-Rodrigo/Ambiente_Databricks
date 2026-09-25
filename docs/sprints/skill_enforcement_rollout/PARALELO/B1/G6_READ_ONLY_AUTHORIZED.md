# G6.READ_ONLY_RECONCILE — autorização humana registrada

Autorização humana específica registrada em:

`issue#114:comment#5834465790`

Válida somente para o freeze:

```text
SHA = c11c2dff07f0f7595ed545f32990e5d54f1fd583
TREE = 15527a29db0e6bcefa639cfadd4d66eed1d32d83
```

Target esperado:
- profile: `FREE`;
- host: `https://dbc-72c8503a-bc27.cloud.databricks.com`;
- workspace pessoal/Free;
- efeito autorizado: `NONE`.

A autorização cobre apenas reconciliação read-only. Publicação, import, probes, Genie, cleanup, policy, promoção, Ready e merge continuam não autorizados.

Qualquer mismatch de host/usuário/conteúdo encerra a fase sem correção remota automática.
