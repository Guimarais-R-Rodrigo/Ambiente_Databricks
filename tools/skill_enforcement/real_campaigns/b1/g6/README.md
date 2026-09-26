# SER B1 G6 — pacote externo preparado

Este diretório contém artefatos de **autoria** para G6. Nada aqui representa execução externa.

- `external_manifest.json`: fases, efeitos e autoridades.
- `genie_manifest.json`: 16 casos canônicos / 20 variantes congeladas.
- `ser03_free_probe.py`: probe Free do núcleo real SER03 L3 com fixtures sintéticas R7.
- `ser05_l2_free_probe.py`: probe Free de contexto/preflight SER05 L2, sem join material.
- `validate_package.py`: validador local fail-closed do pacote.

Os probes ficam fora de `.assistant` e não são produto publicado. O produto qualificado continua preso a `08c2a93c4c9dede1e759abe28c07242b4116f47e`.

Execução externa requer autorização humana específica, incluindo efeitos remotos temporários quando houver import de probe ou publicação necessária.
