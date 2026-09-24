## 2026-09-24 — B0 da execução paralela governada da SER

### Implementado

- (ChatGPT) Formalizado o ADR-0023 e versionado o plano detalhado de execução paralela governada, preservando SER02–SER16 e o ADR-0022.
- (ChatGPT) Implementada candidata B0 em `tools/skill_enforcement/parallel/`: contratos fechados, command registry sem shell/inline code, scheduler com resource/exclusivity limits, launcher read-only, verifier independente, inventário de cobertura por método, RAW/SHARE, host probe e dois pilotos sintéticos.
- (ChatGPT) Adicionados metatestes do mecanismo e checkpoint B0. O launcher B0 proíbe escrita no repositório; renderer/snapshot/policy/integração permanecem etapas seriais externas aos workers.

### Limites

- (ChatGPT) B0 ainda requer qualificação local Windows/NTFS e teste efetivo de sandbox/permissões. Nenhuma campanha de SER02–SER14 foi iniciada. `policy.json`, skills e Databricks não foram alterados por esta implementação.
