# G6 mismatch forensics — PASS

## Resultado

```text
FORENSICS = PASS
artifact_sha256 = c92cc638d2ed46c45f5f53d085e81e0408d3b89fa4ec2e1a3b219366e90a7da7
remote_package_state = STALE_INCOMPLETE

raw_errors = 33
missing = 16
incomplete_read = 16
intersection = 15
missing_equals_incomplete = false
logical_missing_equals_incomplete = true
unique_paths_reported = 18
logical_unique_defects = 17
```

A diferença entre os sets é apenas a representação do notebook `exemplo_domain_context`: inventário remoto usa path sem `.py`, enquanto a export/content compare referencia o source local com `.py`.

## Ausências

Todos os 16 objetos ausentes:
- existem em fonte e produto local;
- já pertencem ao R7 e ao freeze G6;
- entraram juntos no commit P1 `d2b6079ee2e6ecec628d14411afbdbdb878a5fb9`.

## Conteúdo divergente

```text
path = .assistant/hub_padroes/skill_enforcement/policy.json
local_sha256 = 957a8a4d30d2d1c04b0ec4a3c079e2fa784b24c512dc90386aa686f7cdf69d9d
remote_sha256_prefix = b68d378b4552
historical_match = true
matching_commit = a01d12ff4e0cb7cfd795ade164f9ce9daad372ba
matching_sha256 = b68d378b4552f0f2800e82a47faf48961af68c0c95f416bb580582fc48f47be9
```

Não foram observados objetos obsoletos, type mismatches, skill mismatches, directory missing independentes ou outras anomalias.

Nenhuma chamada Databricks foi feita durante a perícia.
