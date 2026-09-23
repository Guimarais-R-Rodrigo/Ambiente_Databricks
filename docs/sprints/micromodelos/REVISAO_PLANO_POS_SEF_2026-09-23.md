# Revisão do Plano Mestre de Micromodelos pós-MM01, SEF/PSEF e SER

**Data:** 2026-09-23  
**Natureza:** adendo arquitetural e processual; não reescreve MM00/MM01 nem os ADRs aceitos.  
**Estado de implementação funcional:** `MM02 = NOT_STARTED`.

## 1. Autoridade e precedência

Esta revisão complementa `PLANO_MESTRE.md` somente nos pontos explicitamente alterados abaixo. Todo o restante do Plano Mestre original continua vigente.

A ordem de autoridade para execução futura é:

```text
ADRs aceitos
+ contrato MM01 integrado
+ Plano Mestre original
+ esta revisão, apenas nos pontos explicitamente alterados
+ policy/SEF/PSEF/SER efetivamente integrados no momento de cada gate
```

Uma PR aberta ou draft pode informar direção prospectiva, mas não governa a arquitetura presente. Quando houver divergência entre este documento e o estado Git posterior, deve-se reconsultar a `main` e registrar a mudança; não atualizar níveis por memória.

## 2. Evento motivador e estado observado

A MM01 foi aceita e integrada pela PR #51:

- HEAD integrado: `fa1a3653e60472d171307663d1175344bb3f6a8d`;
- base imediatamente anterior: `4bc7c9aada96468505e51f279cf32c107d0b6dbb`;
- merge: `73d7659dcf11509a7fba392221c4810d10401c35`;
- tree da branch e do merge: `58beb10f5d849fa01f2c94f2ee682c2b3276ea1e`.

Depois disso, a SER00/PR #101 também foi aceita e integrada. A `main` usada para abrir esta revisão é:

`dedde0741ed4c387c3a500adfbf7de2c6166aba5`.

Essa é uma divergência material em relação ao handoff inicial desta frente, que ainda tratava a PR #101 como draft. O GitHub vivo vence: **SER00 está integrada**. A integração da SER00, porém, é documental e não promoveu `current_level`, não alterou `policy.json` e não iniciou SER01.

A PSEF00/PR #98 está integrada. A PSEF01/PR #99 permanece aberta em draft e não é autoridade canônica.

## 3. O que permanece preservado

SEF/PSEF/SER não invalidam retroativamente:

- MM00;
- ADR-0014 a ADR-0020;
- schema MM01;
- R01–R08;
- máquina de estados;
- contrato YAML;
- matriz final;
- auditorias MM01;
- campanha R1–R10.

O primeiro impacto material de implementação SEF na linha de Micromodelos continua sendo MM04, quando deve nascer `hub-ml-micromodelos`. MM02 e MM03 permanecem anteriores a essa skill.

## 4. Snapshot SEF vigente

Fonte viva: `ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json`, blob observado `01cabb4dc45e7a2349e4b1630e3a322c4da75d6c`.

| Skill | Risco | Current | Target | Scope | Rollout | Status |
|---|---|---:|---:|---|---|---|
| hub-ml-analise-safra | high | L0 | L3 | stage_specific | audit | defined |
| hub-ml-auditoria-skills | high | L3 | L3 | stage_specific | audit | implemented |
| hub-ml-baseline-ml | critical | L0 | L4 | stage_specific | audit | defined |
| hub-ml-comentar-notebook | low | L1 | L1 | whole_skill | audit | implemented |
| hub-ml-concierge | low | L1 | L1 | whole_skill | audit | implemented |
| hub-ml-criar-objeto | high | L2 | L3 | stage_specific | audit | defined |
| hub-ml-cross-eda-ml | critical | L0 | L4 | stage_specific | audit | defined |
| hub-ml-eda-profissional | high | L4 | L4 | stage_specific | enforce | implemented |
| hub-ml-explainability | medium | L0 | L3 | stage_specific | audit | defined |
| hub-ml-feature-engineering | critical | L0 | L4 | stage_specific | audit | defined |
| hub-ml-monitoramento-modelo | critical | L0 | L4 | stage_specific | audit | defined |
| hub-ml-pipeline-builder | critical | L0 | L4 | stage_specific | audit | defined |
| hub-ml-tutor-databricks | low | L0 | L0 | whole_skill | guidance | implemented |
| hub-ml-validacao-estatistica | high | L0 | L3 | stage_specific | audit | defined |

A baseline SER00 confirma cinco skills no target e nove abaixo do target. Esses targets foram revalidados arquiteturalmente, mas **target não é promoção**. `current_level` continua sendo a única descrição de capacidade presente.

## 5. PSEF e contrato de autoridade

A PSEF00 integrada congela o encadeamento:

```text
Prompt / briefing
→ Skill selecionada
→ policy.json / current_level
→ rota realmente implementada
→ helpers/scripts canônicos
→ evidência proporcional ao nível vigente
```

Princípios preservados:

1. prompt continua briefing;
2. prompt não recebe policy própria;
3. prompt não recebe Receipt próprio;
4. prompt não recebe Postflight próprio;
5. entrypoint protegido da skill não pode ser substituído por helper/código manual paralelo;
6. `current_level` governa a capacidade presente;
7. `target_level` é roadmap;
8. em prompt multirrota, a policy é resolvida **depois** da escolha da skill.

A PSEF01 draft pode ser consultada para direção, mas só a última PSEF integrada no momento do gate é autoridade.

## 6. SER integrada e efeito sobre Micromodelos

SER00 agora é parte da arquitetura integrada e acrescenta um plano explícito de rollout local-first. Ela não modifica a conclusão de que MM04 é o primeiro ponto de criação de nova skill em Micromodelos.

Consequências prospectivas:

- antes de MM04, reconsultar o estado SER já integrado e qualquer SER posterior que tenha sido aceita;
- não copiar `target_level` da SER para `current_level`;
- se uma skill reutilizada por Micromodelos tiver sido promovida entre duas sprints, a sprint consumidora deve resolver novamente a rota presente;
- a cardinalidade atual de 14 skills não deve ser tratada como fixa depois de MM04: a nova skill exige decisão e atualização canônica próprias, não atalho para “15ª entrada”.

## 7. Concorrência observada

| Frente | Estado em 2026-09-23 | Autoridade presente | Tratamento |
|---|---|---|---|
| MM01 / PR #51 | INTEGRATED | sim | não reabrir |
| PSEF00 / PR #98 | INTEGRATED | sim | baseline PSEF atual |
| PSEF01 / PR #99 | OPEN_DRAFT | não | direção prospectiva; reconsultar no gate |
| SER00 / PR #101 | INTEGRATED | sim | plano de rollout vigente; policy permanece sem promoção |
| antiga SE08 / PR #91 | OPEN_DRAFT histórico | não | SE08 integrada na main é autoridade |
| Visual Lab / PR #26 | OPEN_DRAFT | não | reconsultar em MM11 se ainda relevante |
| PRs antigas #5/#6 de READMEs/prompts | OPEN_DRAFT histórico | não | não incorporar por efeito colateral |

Somente `INTEGRATED` governa a arquitetura presente.

## 8. Matriz de impacto MM00–MM13

| Sprint | Impacto SEF/PSEF/SER | Tratamento |
|---|---|---|
| MM00 | sem impacto retroativo | histórico e ADRs preservados |
| MM01 | sem impacto funcional | aceita e integrada; não reabrir |
| MM02 | documental/semântico | fingerprint é identidade material; não é Receipt/evidência/aprovação |
| MM03 | revalidar ao iniciar | metadata collector continua componente interno, não skill por presunção |
| MM04 | **ALTO** | nova skill + SEF readiness + primeiro briefing próprio |
| MM05 | **ALTO** | discovery/multirrota + policy-aware routing |
| MM06 | **ALTO** | separar YAML/fingerprint/Receipt/MLflow/artifacts/aprovação |
| MM07 | documental/revalidar | pacote departamental; consumir estado vigente |
| MM08 | **ALTO** | separar enforcement de skill de autoridade/permissão ambiental |
| MM09 | **ALTO** | separar task correctness, agent adherence e canonical compliance |
| MM10 | **ALTO** | superfície de publicação/handoff sem autopublicação |
| MM11 | transversal | rebase SEF/PSEF/SER + Temas + monitoramento + experiência MM09/MM10 |
| MM12 | **ALTO** | skill de migração recebe perfil SEF próprio |
| MM13 | revalidar | catálogo/escala sem duplicar policy ou autoridade |

## 9. Gates novos

### 9.1 `MM04_SEF_READINESS`

Antes de criar `hub-ml-micromodelos`, reler `policy.json`, SEF integrado, última PSEF integrada, SER integrada, `.assistant_instructions.md` e o contrato vigente de criação de skills.

Decidir explicitamente:

- `risk_class`;
- `current_level` inicial realmente sustentado;
- `target_level`;
- `scope_mode`;
- `rollout_mode`;
- `policy_status`;
- protected surfaces;
- entrypoints e handoffs;
- ações persistentes;
- evidência proporcional;
- autorização;
- bypass rules.

Skill nova não nasce L4 por intenção. `current_level` não é atribuído por target.

### 9.2 `MM04_PSEF_PROMPT_READINESS`

MM04 cria também o primeiro briefing `micromodelo_novo`. Antes de materializá-lo, reler a última PSEF efetivamente integrada.

Se PSEF01+ estiver integrada, consumir seu contrato. Se a PSEF ainda não estiver suficientemente estabilizada, registrar decisão explícita entre postergar o briefing ou proceder sob o contrato canônico integrado. Nunca usar draft como autoridade nem avançar silenciosamente.

### 9.3 `MM05_PROMPT_CONTRACT_READY`

Antes do prompt de descoberta:

```text
Prompt
→ Skill
→ policy/current_level
→ rota vigente
→ helper/runner canônico
```

Para multiskill:

```text
objetivo
→ selecionar skill
→ consultar policy da skill escolhida
→ executar a rota atual
```

Não criar nível único artificial para prompt multirrota.

### 9.4 `MM06_EVIDENCE_MODEL`

Formalizar objetos distintos:

- YAML: definição canônica do micromodelo;
- `spec_fingerprint`: identidade semântica da especificação material;
- Execution Receipt: evidência de etapa protegida quando exigida pelo SEF;
- MLflow run: histórico operacional/experimental;
- artifacts/resultados: evidência da run;
- decisão/aprovação humana: governança.

Nenhum substitui o outro. Em particular: fingerprint não é Receipt, não prova execução, não prova aprovação; YAML não é log; MLflow run não altera automaticamente o estado aprovado do YAML.

### 9.5 `MM08_ENVIRONMENT_AUTHORITY`

Antes de homologação no trabalho, separar:

```text
enforcement da skill
≠
autorização corporativa
```

SEF não concede catálogo, ACL, direito de publicar, autoridade institucional ou permissão para dados restritos. O workspace corporativo continua autoridade dessas permissões.

### 9.6 `MM09_BEHAVIORAL_AND_CANONICAL`

No piloto greenfield medir separadamente:

- **task correctness** — tarefa analítica correta;
- **agent adherence** — prompt/skill/handoffs seguidos;
- **canonical compliance** — entrypoints/Receipt/Postflight usados quando exigidos.

Mínimo adversarial: positivo, negativo, `@menção`, bypass explícito, helper manual paralelo, conflito prompt × skill, target × current, handoff L4, handoff para L0, ação persistente sem autorização e completion sem Postflight quando aplicável.

### 9.7 `MM10_PUBLICATION_SURFACE`

Antes de publicação/handoff, decidir se a preparação da superfície exige enforcement próprio. Preservar ADR-0017: `GOVERNANCA_EXTERNA` é autoridade final. SEF não publica automaticamente.

Se houver entrypoint protegido de preparação do handoff, definir preflight/Receipt/Postflight proporcional. Não criar autopublicação.

### 9.8 `MM11_TRANSVERSAL_REBASE`

Antes do freeze V1, reler SEF, policy, PSEF, SER integrada, Sistema de Temas, monitoramento disponível e experiência real de MM09/MM10. Não assumir que estados observados em MM04 permanecem iguais.

### 9.9 `MM12_MIGRATION_SKILL_SEF`

`hub-ml-padronizar-micromodelo` recebe avaliação própria de risk/current/target/scope/rollout, arquivos escritos, equivalência antes/depois, autorização, rollback, proveniência, histórico, breaking changes, testes positivos/negativos, bypass e canonical compliance.

Não herdar automaticamente o perfil de `hub-ml-micromodelos`.

## 10. Sequência revisada

```text
MM00
  ↓
MM01 — INTEGRADA
  ↓
MM02 — fingerprint
  ↓
MM03 — metadata-only
  ↓
MM04_SEF_READINESS
  ↓
MM04_PSEF_PROMPT_READINESS
  ↓
MM04 — objetivo conhecido / skill
  ↓
MM05_PROMPT_CONTRACT_READY
  ↓
MM05 — discovery
  ↓
MM06_EVIDENCE_MODEL
  ↓
MM06 — notebook / README / tracking
  ↓
MM07
  ↓
MM08_ENVIRONMENT_AUTHORITY
  ↓
MM08
  ↓
MM09_BEHAVIORAL_AND_CANONICAL
  ↓
MM09
  ↓
MM10_PUBLICATION_SURFACE
  ↓
MM10
  ↓
MM11_TRANSVERSAL_REBASE
  ↓
MM11
  ↓
MM12_MIGRATION_SKILL_SEF
  ↓
MM12
  ↓
MM13
```

Não existe dependência PSEF adicional para MM02/MM03. PSEF se torna material antes do primeiro prompt/skill da MM04.

## 11. Fronteira congelada de MM02

MM02 continua sendo **fingerprint semântico da especificação**.

Regras:

1. não é hash bruto do YAML;
2. mudanças editoriais não devem necessariamente mudar o fingerprint;
3. mudanças materiais devem mudar o fingerprint;
4. materialidade deve se apoiar nas autoridades canônicas da MM01, não criar normalizador semântico concorrente;
5. fingerprint não é Execution Receipt;
6. fingerprint não prova execução;
7. fingerprint não prova aprovação, publicação ou homologação;
8. a sprint é completamente sintética e repo-side.

Mudanças materiais incluem, conforme o Plano Mestre: fonte, janela, regra, peso, threshold, missing policy, semântica TRUE/FALSE, significado do score e contrato de saída.

MM02 não acessa Databricks, catálogo, registros, MLflow, publicação, skills ou prompts.

## 12. Fronteira prospectiva de MM03

MM03 permanece metadata-only:

1. schemas/objetos visíveis;
2. nomes/tipos/descrições/tags;
3. shortlist;
4. detalhes apenas de candidatas;
5. dados somente depois, se necessário e autorizado.

Continuam proibidos no modo metadata-only: `count(*)`, profiling de registros, sample de clientes, consulta de valores e inferência de catálogo completo a partir de visibilidade parcial.

MM03 não cria enforcement de skill por presunção. Reavaliar no início real da sprint.

## 13. Regra de reconsulta

No início de toda sprint impactada e imediatamente antes de um gate de freeze/certificação:

1. reconfirmar `main`, PRs e concorrência;
2. reler `policy.json`;
3. usar `current_level` como capacidade presente;
4. identificar a última PSEF integrada;
5. identificar a última SER integrada e promoções efetivamente aceitas;
6. reconsultar Temas/monitoramento quando a sprint tocar essas superfícies;
7. registrar qualquer divergência relevante em vez de adaptar silenciosamente.

A revisão é deliberadamente aditiva. Mudança futura material exige novo adendo/ADR quando aplicável; não reescrever ADR histórico aceito.
