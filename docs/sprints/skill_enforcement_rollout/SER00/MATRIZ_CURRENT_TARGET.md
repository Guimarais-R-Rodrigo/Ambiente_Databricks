# SER00 — current, target e revisão 14/14

Snapshot de `11851e137dd7793b351ac08fc211c0be90005dee`, policy blob `01cabb4dc45e7a2349e4b1630e3a322c4da75d6c`. Estes valores são observados, não promoções aprovadas pela SER.

| Skill | Risco | Current | Target | Scope | Rollout | Status | Ordem |
|---|---|---|---|---|---|---|---|
| hub-ml-analise-safra | high | L0 | L3 | stage_specific | audit | defined | SER03 |
| hub-ml-auditoria-skills | high | L3 | L3 | stage_specific | audit | implemented | REGRESSION_ONLY/SER15/SER16 |
| hub-ml-baseline-ml | critical | L0 | L4 | stage_specific | audit | defined | SER09/SER10 |
| hub-ml-comentar-notebook | low | L1 | L1 | whole_skill | audit | implemented | REGRESSION_ONLY/SER15/SER16 |
| hub-ml-concierge | low | L1 | L1 | whole_skill | audit | implemented | REGRESSION_ONLY/SER15/SER16 |
| hub-ml-criar-objeto | high | L2 | L3 | stage_specific | audit | defined | SER01 |
| hub-ml-cross-eda-ml | critical | L0 | L4 | stage_specific | audit | defined | SER05/SER06 |
| hub-ml-eda-profissional | high | L4 | L4 | stage_specific | enforce | implemented | REGRESSION_ONLY/SER15/SER16 |
| hub-ml-explainability | medium | L0 | L3 | stage_specific | audit | defined | SER02 |
| hub-ml-feature-engineering | critical | L0 | L4 | stage_specific | audit | defined | SER07/SER08 |
| hub-ml-monitoramento-modelo | critical | L0 | L4 | stage_specific | audit | defined | SER11/SER12 |
| hub-ml-pipeline-builder | critical | L0 | L4 | stage_specific | audit | defined | SER13/SER14 |
| hub-ml-tutor-databricks | low | L0 | L0 | whole_skill | guidance | implemented | REGRESSION_ONLY/SER15/SER16 |
| hub-ml-validacao-estatistica | high | L0 | L3 | stage_specific | audit | defined | SER04 |

## Revisão crítica de todos os targets

`CONFIRMED` significa target revalidado e aceito arquiteturalmente na SER00. Não significa implementação comprovada, promoção de `current_level` ou autorização de SER01. Não há proposta de reduzir target para eliminar gaps.

### hub-ml-analise-safra

CONFIRMED: cálculo de incidência e maturidade merece Receipt, mas decisões de negócio continuam humanas; a primitive pandas cobre target binário e não todos os denominadores possíveis.

### hub-ml-auditoria-skills

CONFIRMED: L3 comprova execução da auditoria, sem homologar automaticamente a produtora. Preservar NOT_REVERIFIED quando faltar adapter.

### hub-ml-baseline-ml

CONFIRMED: risco de leakage e efeitos de treino/tracking justificam L4 por etapa; não fixar algoritmo nem exigir tracking inexistente para obter PASS.

### hub-ml-comentar-notebook

CONFIRMED: L1 é proporcional ao contrato editorial; preservação de células deve ser conferida, não inferida nem confundida com execução analítica.

### hub-ml-concierge

CONFIRMED: descoberta e handoff são read-only; tornar a recomendação um runner analítico ampliaria indevidamente o escopo.

### hub-ml-criar-objeto

CONFIRMED: target L3 e escopo stage-specific aceitos em 2026-09-22. A SER01 deve provar a matriz operação×tipo×host×efeito; o piloto Windows create/readme/agregador não sustenta promoção global e `current_level` permanece L2 até evidência suficiente.

### hub-ml-cross-eda-ml

CONFIRMED: diagnósticos L3 e PIT L4 protegem cardinalidade/tempo. PIT não aplicável precisa de decisão explícita, não execução fictícia.

### hub-ml-eda-profissional

CONFIRMED: preservar L4/enforce e o finalizer canônico existentes; não reabrir rollout funcional.

### hub-ml-explainability

CONFIRMED: binding L2 e cálculo L3 são proporcionais; interpretação, causalidade e fairness não se tornam decisões determinísticas.

### hub-ml-feature-engineering

CONFIRMED: L4 protege tempo e materialização, não criatividade. Autorização não substitui Receipt/Postflight nem prova escrita.

### hub-ml-monitoramento-modelo

CONFIRMED: métricas L3 e fronteira de retreino/promoção L4; drift não prova queda de performance nem autoriza ação.

### hub-ml-pipeline-builder

CONFIRMED: risco material justifica L4, mas helpers diagnósticos não são deployer. Falta de operação testável mantém promoção bloqueada.

### hub-ml-tutor-databricks

CONFIRMED: L0 é suficiente para explicação sem execução implícita; exemplos não são testes nem homologação.

### hub-ml-validacao-estatistica

CONFIRMED: plano L2 e cálculos L3; a seleção metodológica não pode ser automatizada como se todos os métodos do SKILL já tivessem API canônica.

## Métricas de baseline

| Métrica | Valor observado |
|---|---:|
| SKILLS_TOTAL | 14 |
| SKILLS_AT_TARGET | 5 |
| SKILLS_BELOW_TARGET | 9 |
| L0_COUNT | 9 |
| L1_COUNT | 2 |
| L2_COUNT | 1 |
| L3_COUNT | 1 |
| L4_COUNT | 1 |
| TARGET_L0_COUNT | 1 |
| TARGET_L1_COUNT | 2 |
| TARGET_L2_COUNT | 0 |
| TARGET_L3_COUNT | 5 |
| TARGET_L4_COUNT | 6 |
| CONTRACT_FILES_PRESENT | 5 |
| PREFLIGHT_FILES_PRESENT | 3 |
| RUNNER_FILES_PRESENT | 3 |
| PROMOTED_L3_OR_HIGHER_SKILLS | 2 |
| POSTFLIGHT_FILES_PRESENT | 1 |

O terceiro runner físico é o piloto criar-objeto. Não contabilizá-lo como L3 global. `CONTRACTS_VALID_THIS_SESSION=NOT_RUN`; presença de cinco contratos não é um novo PASS 5/5. LOCAL/FREE/GENIE de promoções SER permanecem NOT_RUN.

## Regra de rollout candidata

Preservar EDA em `enforce`, auditoria/comentar/concierge em `audit` e tutor em `guidance`. O aceite da SER00 não altera nenhum `rollout_mode`. Nas nove skills, manter `audit` durante construção e primeira certificação. Para targets L3, considerar `warn` somente por decisão humana justificada; o validator atual recusa `enforce` abaixo de L4. Para as cinco novas L4, a ativação de `enforce` exige evidência discriminante, ausência de bypass relevante e autorização separada. Nenhuma duração ou promoção automática audit→warn→enforce é presumida.

`execution_contract.mode=audit` no schema 0.1 é outro campo: não editar esse valor para simular rollout. O mecanismo fail-closed de uma rota L4 e seu modo de implantação devem ser descritos separadamente.
