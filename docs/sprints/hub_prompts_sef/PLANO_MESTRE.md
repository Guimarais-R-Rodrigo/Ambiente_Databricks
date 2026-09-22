# Plano Mestre PSEF00–PSEF07

## Objetivo

Reconciliar `hub_prompts` com a arquitetura de skills e com o Skill Enforcement Framework consolidado após a SE08, preservando a separação entre briefing, método, enforcement e implementação.

O plano foi materializado na PSEF00. As sprints posteriores permanecem **não executadas** até aceite explícito do checkpoint anterior.

## Regras transversais

1. `policy.json` é a fonte machine-readable para `current_level`, `target_level`, `rollout_mode`, risco e artefatos implementados.
2. `current_level` governa o que existe hoje. `target_level` é roadmap e não prova existência de contrato, preflight, runner, Receipt ou Postflight.
3. Quando a skill vigente possuir entrypoint canônico para etapa protegida, o briefing não cria rota paralela.
4. Prompt continua sendo briefing; não receberá policy própria, níveis L0–L4 próprios, Receipt próprio ou postflight próprio.
5. `ambiente_fonte/` é fonte; `Novo_Ambiente_Simulado/` é derivado.
6. Actions fica separado: `GITHUB_ACTIONS=DEFERRED_NO_CREDITS` durante PSEF00–PSEF07, salvo decisão humana posterior.
7. Alteração behavior-bearing exige validação proporcional; alteração puramente documental não herda PASS de outro SHA por declaração.
8. Nenhuma sprint autoriza promoção corporativa.

## PSEF00 — reconciliação, inventário, baseline e freeze

**Objetivo:** fotografar o estado real, congelar escopo e registrar achados sem editar prompts produtivos.

**Entregáveis:** inventário 16/49, matriz prompt→skill→policy, achados, checkpoint e este Plano Mestre.

**Gate:** `LOCAL_DOCUMENTATION_VALIDATION=PASS`; `GITHUB_ACTIONS=DEFERRED_NO_CREDITS`; aceite humano antes de PSEF01.

## PSEF01 — contrato editorial transversal e navegação policy-aware

**Objetivo:** ajustar a documentação de entrada de `hub_prompts` para tornar explícita a precedência Skill → policy/current_level → rota vigente → helper, sem duplicar a policy.

**Escopo candidato:** `hub_prompts/README.md` e convenções comuns de redação.

**Critérios:**
- substituir a “sinergia triangular” por fluxo compatível com SEF;
- explicar `current_level` versus `target_level`;
- explicar que helper direto/código manual não substitui entrypoint protegido;
- preservar que prompts não são auto-descobertos;
- não hardcodar níveis em todos os briefings.

## PSEF02 — reconciliação das rotas EDA L4

**Objetivo:** alinhar `eda_rapida`, `eda_completa` e `data_quality` — e a rota EDA de `comparar_tabelas` — ao `current_level=L4`/`rollout_mode=enforce` de `hub-ml-eda-profissional`.

**Critérios:**
- manter objetivo e contrato de saída do briefing;
- quando houver execução protegida pela skill, apontar para a rota canônica vigente;
- não autorizar PySpark/SQL/helper direto como substituto de `run_enforced`/postflight;
- não declarar conclusão sem a autorização mecânica exigida pela skill;
- não duplicar detalhes internos que pertençam a `SKILL.md`.

## PSEF03 — reconciliação das skills com enforcement já implementado

**Objetivo:** alinhar briefings associados a skills cujo `current_level` já é superior a L0 sem inventar enforcement adicional.

**Escopo candidato:** `auditoria_skills` (L3), `comentar_notebook` (L1) e regras multirrota de `comparar_tabelas`.

**Critérios:** refletir apenas gates realmente implementados; manter o escopo editorial de L1 e a rota L3 da auditoria; preservar autoridade dos verifiers da skill produtora.

## PSEF04 — reconciliação dos briefings L0 e semântica de roadmap

**Objetivo:** revisar os briefings associados a skills L0 para evitar overclaim e ambiguidade entre “helper implementado” e “enforcement implementado”.

**Escopo candidato:** `baseline_orchestration`, `cross_eda`, `explainability`, `feature_engineering`, `monitoramento_modelo`, `pipeline`, `safra`, `stat_check`, `tutor_explicar`, além do roteamento de `novo_projeto`.

**Critérios:**
- não mencionar gates futuros como atuais;
- preservar uso de helpers já existentes sem converter isso em L2/L3/L4;
- manter autorização de escrita/deploy separada de geração de código;
- não forçar associação 1:1 em `novo_projeto`.

## PSEF05 — READMEs locais e notebooks de exemplo

**Objetivo:** reconciliar documentação humana e efeitos operacionais dos exemplos com os briefings já ajustados.

**Critérios:**
- uniformizar alertas de escrita persistente/overwrite;
- corrigir a lacuna do README de `novo_projeto`;
- preservar separação entre preparo sintético do notebook e execução do prompt;
- conferir exemplos contra os briefings sem transformar notebook em runner alternativo.

## PSEF06 — integração documental, renderer e validação estática

**Objetivo:** integrar a redação final com `MANUAL_TECNICO.md`, `.assistant_instructions.md`, índices e derivado sem criar fontes concorrentes.

**Critérios:**
- atualizar Manual/instruções somente se houver lacuna real;
- rematerializar derivado exclusivamente pelo renderer canônico;
- provar equivalência fonte→derivado;
- executar validações estruturais e regressões locais pertinentes;
- registrar qualquer divergência, sem relaxar validadores para obter PASS.

## PSEF07 — certificação final e fechamento

**Objetivo:** certificar a iniciativa no regime disponível, consolidar evidências e preparar encerramento.

**Canais separados:**
- local: obrigatório;
- Databricks Free: quando behavior-bearing e aplicável;
- Genie behavioral screening: quando alterações puderem mudar comportamento;
- GitHub Actions: `DEFERRED_NO_CREDITS` enquanto a restrição persistir.

A sprint só pode ser integrada após revisão e aceite humano explícitos.

## PSEF-ACTIONS-RECERTIFICATION — campanha futura independente

Fora do caminho crítico PSEF00–PSEF07.

Quando créditos forem restaurados, testar **uma única vez** a HEAD final integrada da iniciativa, registrar workflows disparados e resultados e preservar failures sem `rerun-until-green`. Essa campanha não reclassifica retroativamente os canais locais/Free/Genie.
