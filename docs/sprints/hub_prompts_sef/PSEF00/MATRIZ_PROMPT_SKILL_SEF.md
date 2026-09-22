# PSEF00 — matriz Prompt × Skill × SEF

**Policy observada na baseline:** `ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json` em `main@17640a6a31f562e9979d235ede27cf44cef9ebbf`.

`current_level` descreve enforcement implementado hoje. `target_level` é direção aprovada e não prova existência de gates.

| Prompt | Skill / rota | Current | Target | Rollout | Risco da skill | Interpretação PSEF00 |
|---|---|---:|---:|---|---|---|
| `auditoria_skills` | `hub-ml-auditoria-skills` | L3 | L3 | audit | high | 1:1; enforcement implementado |
| `baseline_orchestration` | `hub-ml-baseline-ml` | L0 | L4 | audit | critical | 1:1; target não implementado |
| `comentar_notebook` | `hub-ml-comentar-notebook` | L1 | L1 | audit | low | 1:1; contrato estático |
| `comparar_tabelas` | `hub-ml-eda-profissional / hub-ml-cross-eda-ml / hub-ml-monitoramento-modelo` | L4 / L0 / L0 | L4 / L4 / L4 | enforce / audit / audit | high / critical / critical | multirrota; resolver pelo objetivo |
| `cross_eda` | `hub-ml-cross-eda-ml` | L0 | L4 | audit | critical | 1:1 |
| `data_quality` | `hub-ml-eda-profissional` | L4 | L4 | enforce | high | 1:1; etapa protegida EDA |
| `eda_completa` | `hub-ml-eda-profissional` | L4 | L4 | enforce | high | 1:1; etapa protegida EDA |
| `eda_rapida` | `hub-ml-eda-profissional` | L4 | L4 | enforce | high | 1:1; etapa protegida EDA |
| `explainability` | `hub-ml-explainability` | L0 | L3 | audit | medium | 1:1 |
| `feature_engineering` | `hub-ml-feature-engineering` | L0 | L4 | audit | critical | 1:1 |
| `monitoramento_modelo` | `hub-ml-monitoramento-modelo` | L0 | L4 | audit | critical | 1:1 |
| `novo_projeto` | sem associação 1:1 | N/A | N/A | N/A | N/A | briefing transversal; Genie Code, concierge opcional para descoberta e especialista após definição do tipo de entrega |
| `pipeline` | `hub-ml-pipeline-builder` | L0 | L4 | audit | critical | 1:1 |
| `safra` | `hub-ml-analise-safra` | L0 | L3 | audit | high | 1:1 |
| `stat_check` | `hub-ml-validacao-estatistica` | L0 | L3 | audit | high | 1:1 |
| `tutor_explicar` | `hub-ml-tutor-databricks` | L0 | L0 | guidance | low | 1:1 |

## Notas de roteamento

### `comparar_tabelas`

É deliberadamente multirrota. A escolha depende do objetivo: perfil/qualidade → `hub-ml-eda-profissional`; joins → `hub-ml-cross-eda-ml`; drift → `hub-ml-monitoramento-modelo`. Depois de escolher a skill, a execução deve obedecer ao `current_level` e ao rollout dessa rota; não existe um nível único do prompt.

### `novo_projeto`

Não há associação 1:1 justificada. O briefing organiza charter/backlog e o README raiz já orienta usar Genie Code e selecionar uma skill especializada quando a natureza da entrega estiver clara. `hub-ml-concierge` pode ser útil para descoberta/composição, mas seu L1 termina em recomendação/handoff e não deve ser tratado como executor do projeto.

## Implicação central

A única rota de briefing auditada com `rollout_mode=enforce` é a família que seleciona `hub-ml-eda-profissional` (inclusive a rota EDA de `comparar_tabelas`). Nela, código manual/helper direto não substitui o entrypoint L4 protegido. Para as skills L0, o prompt pode pedir plano/código/execução autorizada, mas não pode apresentar preflight/Receipt/Postflight futuros como mecanismos atuais.
