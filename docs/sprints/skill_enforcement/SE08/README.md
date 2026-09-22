# SE08 — CI, operação, documentação e gate de promoção ao trabalho

**Status:** encerrada, certificada e integrada. `SE08_RC_FULLY_CERTIFIED=true`, `SE08_INTEGRATED=true` e `SE08_POST_MERGE_ACTIONS=PASS`. A promoção ao workspace do trabalho permanece bloqueada.

## Objetivo

Tornar o Skill Enforcement Framework uma capacidade permanente do Hub sem
confundir estrutura válida, comportamento do Genie Code, publicação no Free e
promoção ao workspace do trabalho.

A SE08 operacionaliza o que foi construído em SE01–SE07. O fechamento da sprint
não promove níveis de enforcement e não reclassifica dívidas históricas.

## Estado final integrado

Release candidate funcional e de produto:

```text
RC_SHA                      = ee1cf04b031497bb5b7ddfa47ce28b8015d15668
RC_TREE                     = d29fb8221c08ab3ea1fb0198004d4720d4785f92
LOCAL_CERTIFICATION         = PASS
WINDOWS_R5                  = READY_FOR_REVIEW
FULL_SE08_LOCAL             = PASS
GITHUB_ACTIONS              = PASS
DATABRICKS_FREE             = PASS
GENIE_BEHAVIORAL_SCREENING  = NOT_APPLICABLE
SE08_RC_FULLY_CERTIFIED     = true
```

A PR #90 integrou a RC em `main@627bcc798261451b70d396550fb5f11ca6d609c2`.
A primeira rodada pós-merge teve 18/19 workflows em success e revelou uma falha
de portabilidade da suíte SE07 em Python 3.11: `PosixPath.is_junction` não
existia naquele runtime. A falha foi preservada e não recebeu rerun.

A PR #92 corrigiu somente a portabilidade da suíte e o filtro de dependências do
workflow de transição. O merge resultou em:

```text
SE08_INTEGRATION_SHA     = 431c46fcffc9345ad4c24280ba13f2ba1dba579b
SE08_INTEGRATED          = true
SE08_POST_MERGE_ACTIONS  = PASS
```

A rodada de push desse SHA concluiu 17/17 workflows disparados em `success`,
incluindo o mesmo `Kit de transição para o trabalho` em Python 3.11.

A PR #93 executou somente o fechamento documental da SE08 e foi integrada em
`85474968f5548c13a9a41a3c84f99b3e18f6874c`. A rodada de push desse merge
documental concluiu 18/18 workflows disparados em `success`, incluindo os
workflows dedicados `Skill Enforcement SE01` e `Skill Enforcement SE02`.
Esse merge não altera a classificação dos bytes de produto da RC.

## Evidência dos gates

### Windows e FULL

A campanha R5 executou no SHA da RC:

- Windows corrective: 10/10 PASS;
- storage cleanup: 9/9 PASS;
- certifier regression: exit 0, 51 métodos, um skip de escopo;
- CI Windows: PASS 10/10;
- FULL SE08: PASS 21/21;
- zero failures, gate failures e infrastructure errors;
- `release_clean_certification=true`;
- `scope_complete=true`.

Bundle Windows R5 SHA-256:
`215176bd9804ab38b2d55678778f1d0defaa334c5040aa13ce5810a43d105d03`.

O WinError32 histórico não foi reproduzido na R5. Isso não significa root cause
corrigida. As ocorrências R2–R4 continuam preservadas como evidência histórica
de intermitência.

### Databricks Free

A mesma RC foi publicada no workspace pessoal/Free pelo publicador canônico:

- dry-run PASS;
- publicação PASS;
- verify rápido PASS;
- verify completo PASS;
- verify por conteúdo PASS;
- 573/573 arquivos comparados;
- zero ausentes;
- zero obsoletos;
- 14/14 skills;
- 5/5 diretórios hub;
- `source_commit=ee1cf04b031497bb5b7ddfa47ce28b8015d15668`;
- `SE08_FREE_OPERATIONAL_INTEGRITY_V1=PASS`.

Bundle Free SHA-256:
`630a0920955bbba2a7140e03c95d6e7149331ecf26aeb4f08a459130a98a2aae`.

### Genie Code

O delta SE08 não alterou `.assistant_instructions.md`, `policy.json`,
`skills/*/SKILL.md` ou `skills/*/scripts/**`. Portanto não houve novo
comportamento executável/conversacional a homologar e
`GENIE_BEHAVIORAL_SCREENING=NOT_APPLICABLE` para a SE08.

O screening da SE07 permanece histórico; ele não foi reexecutado nem
reclassificado: `SE07_GENIE_BEHAVIORAL_SCREENING=PASS`.

## Equivalência entre RC e main final

Entre a RC certificada e o SHA de integração da SE08 (`431c46fcffc9345ad4c24280ba13f2ba1dba579b`), somente estes arquivos não documentais adicionais mudaram:

- `.github/workflows/kit-transicao-trabalho.yml`;
- `tools/tests/test_skill_enforcement_se07.py`.

Não houve mudança em `ambiente_fonte/`, `Novo_Ambiente_Simulado/`, policy,
certifier ou conteúdo publicado no Free. No Windows, quando `Path.is_junction`
existe, o helper corretivo continua chamando a mesma API; no Python 3.11 sem essa
API, o fallback foi provado pelo workflow que originalmente falhou.

A PR #93 acrescentou somente os cinco arquivos documentais de fechamento
(`CHANGELOG.md` e quatro documentos em `docs/sprints/skill_enforcement/`).

A evidência Windows/Free continua vinculada aos bytes de produto da RC. A prova
pós-merge da corretiva pertence ao SHA de integração `431c46fcffc9345ad4c24280ba13f2ba1dba579b`; não se afirma que o FULL Windows foi reexecutado nesse merge nem no merge documental.

## Dívidas históricas preservadas

- SE06: 24/25; `S06-A1-R4=NOT_RUN`; `SE06_DOD=INCOMPLETE`;
  `SE06_FULLY_CERTIFIED=false`;
- SE07: encerrada por decisão humana com residual conhecido;
  `SE07_FULLY_CERTIFIED=false`;
- WinError32: intermitente; owner/root cause não estabelecidos;
- criar-objeto: L2 global; piloto L3 stage-specific não promove a skill inteira.

## Gate de promoção ao trabalho

O Plano Mestre exige, cumulativamente:

1. validações locais pertinentes em PASS;
2. renderer sem divergência;
3. publicação Free verificada por conteúdo;
4. casos críticos SE06 sem escaped non-compliance;
5. zero achados críticos/altos em aberto relacionados ao enforcement;
6. documentação operacional completa;
7. aceite explícito do usuário;
8. plano de rollback definido.

A decisão G2 preservou `SE06_DOD=INCOMPLETE` e declarou explicitamente que a
exceção de sequência SE06 → SE07 não satisfaz o gate corporativo da SE08.

Portanto:

```text
PROMOCAO_TRABALHO = BLOQUEADA
```

O aceite humano dado para integrar a SE08 não autoriza replicação corporativa,
mudança de policy, promoção de níveis ou publicação no workspace do trabalho.

## Operação futura

A matriz local e o procedimento de reprodução permanecem em
[RUNBOOK_LOCAL.md](RUNBOOK_LOCAL.md). A SE08 só deve ser reaberta por mudança
funcional, regressão observada, decisão explícita sobre a dívida herdada ou nova
autorização de rollout.
