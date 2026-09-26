# G6.READ_ONLY_RECONCILE attempt 2 — REMOTE_CONTENT_MISMATCH

## Resultado

```text
attempt_1 = BLOCKED_AUTHENTICATION / preserved
auth_remediation = PASS / preserved
attempt_2 = REMOTE_CONTENT_MISMATCH

verify_exit_code = 1
verify_status = FAIL
scope = inventory-types-content
files_compared = 574
error_count = 33

missing_remote_count = 16
divergent_content_count = 1
incomplete_remote_read_count = 16

package_raw_sha256 =
576134eb3e8d5c6d52be306a35351960df3be2ecb2b1b4602749864f5cca16ff

package_normalized_sha256 =
5ac3db2f3104c6829e3d17314ef386afcd7e4b3ce6cc095db75e044318fe332f
```

Nenhum efeito remoto foi executado.

## Interpretação inicial

O verifier primeiro computa objetos ausentes por inventário e depois tenta exportar/comparar todos os arquivos locais. Um objeto ausente pode, portanto, gerar:
1. `ausente no remoto`;
2. `leitura remota incompleta` na comparação de conteúdo.

Como as contagens são exatamente 16 + 16, existe forte hipótese de os dois grupos referirem-se aos mesmos 16 paths. Isso precisa ser confirmado no relatório literal; não deve ser assumido como fato final.

Há ainda 1 `conteúdo divergente` que precisa ter seu path identificado.

## Próxima etapa

A próxima etapa é puramente local: ler o `remote_content_verify.json` já produzido na tentativa 2, deduplicar/classificar os erros e produzir inventário sanitizado.

Nenhum novo comando Databricks deve ser executado.

Publicação permanece não autorizada.
