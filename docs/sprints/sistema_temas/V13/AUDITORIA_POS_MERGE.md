# V13 — auditoria pós-merge e fechamento

Data: 16/09/2026.

Escopo: auditoria posterior à integração da S7/V13, sem iniciar V14 e sem executar qualquer mutação Databricks.

## 1. Objeto auditado

A S7 foi aceita explicitamente pelo mantenedor e integrada pela PR #66 a partir do HEAD certificado:

`4f84ba40e8fa45a04acf976e776440f04a037706`

Merge na `main`:

`62e9404851d6a7902371bd5b6531a113d521311c`

O merge foi realizado com proteção pelo SHA esperado do HEAD da PR. A `main` anterior era:

`6dfb8707835921f2f48020f383cf571902080109`

## 2. Certificação pós-merge

O GitHub disparou 15 workflows de `push` associados ao merge `62e9404851d6a7902371bd5b6531a113d521311c`.

Resultado observado:

**15/15 workflows concluídos em `success`.**

O workflow `Contrato operacional V13`, run `35106812430`, confirmou no merge:

- S1: 20/20 PASS;
- S2: 27/27 PASS;
- S3: 21/21 PASS;
- S4: 30/30 PASS;
- S5: 32/32 PASS;
- S6: 28/28 PASS;
- S7: 28/28 PASS;
- regressões V01–V13: 701/701 PASS;
- compatibilidade V00: 12/12 PASS;
- validador estrutural/documental: `APROVADO: 0 falha(s), 0 aviso(s)`;
- `repo (identidade) = 1456`;
- `repo (links) = 1942`;
- `worktree (extras) = 0`.

Fronteiras observadas no mesmo run:

- `V13_S1_REMOTE_MUTATION=0`;
- `V13_S2_NETWORK=0`;
- `V13_S2_REMOTE_MUTATION=0`;
- `V13_S3_NETWORK=0`;
- `V13_S3_REMOTE_MUTATION=0`;
- `V13_S3_LOCAL_DRY_RUN_ONLY=1`;
- `V13_S4_NETWORK=0`;
- `V13_S4_REMOTE_MUTATION=0`;
- `V13_S4_DIAGNOSIS_READ_ONLY=1`;
- `V13_S5_NETWORK=0`;
- `V13_S5_REMOTE_MUTATION=0`;
- `V13_S5_CONTRAST_PREFLIGHT_LOCAL=1`;
- `V13_S6_NETWORK=0`;
- `V13_S6_REMOTE_MUTATION=0`;
- `V13_S6_IMPLICIT_PUBLICATION=0`;
- `V13_S6_LOCAL_OR_SIMULATED_REHEARSALS=5`;
- `V13_S6_REAL_ENVIRONMENT_CASES_BLOCKED=3`;
- `V13_S7_NETWORK=0`;
- `V13_S7_REMOTE_MUTATION=0`;
- `V13_S7_DATABRICKS_MUTATION=0`;
- `V13_S7_HUMAN_VALIDATION=PASS`;
- `V13_S7_HUMAN_EVIDENCE=VERSIONED_HUMAN_SESSION`;
- `V13_V14_NOT_STARTED=1`.

O workflow usa permissão `contents: read`, checkout com `persist-credentials: false` e não recebe credenciais Databricks. Os avisos do runner sobre ações que ainda declaram Node.js 20, executadas pelo GitHub em Node.js 24, não produziram falha dos gates.

## 3. V12 no merge V13

O workflow `Homologação de jornadas V12`, run `35106812487`, também concluiu em `success` no mesmo SHA.

No `push` da `main`, diferentemente de uma PR fora da V12, o gate estrito foi aplicável:

- protocolo/mutantes: 47/47 PASS;
- evidência real: 11/11 PASS;
- regressões transversais: 701/701 PASS;
- V00: 12/12 PASS;
- validador: 0 falhas / 0 avisos;
- métricas: 1456 arquivos / 1942 links;
- `V12_SCOPE=APPLICABLE`;
- `Escopo V12 e higiene`: PASS;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`.

A allowlist V12 não foi ampliada pela S7.

## 4. Evidência humana S7

A homologação humana registrada permanece:

- `participant_id = Tester`;
- participante autorizado = `true`;
- participante não construiu o procedimento = `true`;
- duração observada = 5 minutos;
- ajuda verbal = 0;
- ajuda documental extra = 0;
- erros de interpretação = 0;
- H1–H6 = PASS;
- `HUMAN-01 = PASS`.

A fonte da evidência é o relato do mantenedor após a sessão real. Git/CI não observaram nem fabricaram a sessão; apenas verificam o registro versionado.

Uma única sessão é evidência formativa de handoff, não base para inferência estatística, SLA, SLO, production readiness ou go-live.

## 5. Estados herdados

O fechamento V13 preserva:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance histórico V12;
- `A11-01 = FAIL`;
- issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

Nenhum desses estados é promovido por inferência a partir da integração V13.

## 6. Contratos V11 preservados

Continuam congelados:

- `ResolvedTheme` como fonte configurável de verdade;
- `context="aibi"` reservado;
- 48 tokens = 3 `translated`, 23 `approximated`, 22 `unsupported`;
- somente três bindings diretos autorizados;
- `dashboard_sintetico.json` não é import nativo;
- `cellFormat` não vira token;
- `approximated` e `unsupported` não são automatizados;
- dashboard theme é distinto de workspace theme;
- `Import theme` é distinto de `Publish`.

## 7. Achado da auditoria pós-merge

A certificação técnica da `main` passou integralmente, mas a leitura semântica pós-merge encontrou um drift documental de estado vivo:

- o README raiz ainda chamava a S7 de candidata;
- `docs/sprints/sistema_temas/V13/README.md` ainda listava passos pré-merge como pendentes;
- `docs/sprints/sistema_temas/README.md` ainda anunciava V13 em S0;
- `docs/sprints/README.md` ainda anunciava V13 em S0.

Classificação: **drift documental pós-merge**, sem impacto em runtime ou contratos funcionais.

A correção é feita em branch própria de fechamento, de forma aditiva, sem reescrever checkpoints históricos. Os quatro READMEs vivos são sincronizados para registrar V13 integrada/encerrada e V14 não iniciada.

Este próprio arquivo acrescenta um caminho versionado; portanto as métricas 1456/1942 pertencem ao merge S7 auditado, não devem ser presumidas para a candidata documental de fechamento. O runner deve medir novamente a árvore e o README raiz só pode ser reconciliado com números efetivamente observados.

### 7.1 Primeira candidata da reconciliação documental

Durante a montagem desta correção, a PR #56/SE00 avançou a `main` para `3341f58a8ebffac8b3f0f8837c7d0d6f8aa0b245`. A branch V13 foi reconciliada aditivamente por merge de dois pais, sem rebase, reset ou force-push.

Primeiro HEAD reconciliado da PR #67:

`88dfa3d8397aa1605b4eb067da1a9e1cfbfe4b87`

Nesse SHA:

- V00, V01 e V02 concluíram em `success`;
- CI geral, V10, V11, V12 e V13 concluíram em `failure`;
- no CI geral, todos os grupos funcionais aplicáveis passaram e somente `validacao` falhou;
- o runner mediu **1481 arquivos / 1959 links**;
- o README raiz ainda declarava a baseline SE00 **1480 / 1957**;
- o validador registrou exatamente **2 falhas / 0 avisos**, ambas por essa divergência;
- no V13, S1–S7, 701/701 regressões e V00 12/12 passaram; `Validação estrutural e documental` falhou e as fronteiras S1–S7 ficaram `skipped`, não PASS;
- no V12, protocolo/mutantes, evidência real, regressões e V00 passaram; o validador falhou e `Aplicabilidade do escopo estrito V12` e `Escopo V12 e higiene` ficaram `skipped`.

Por isso, esse SHA **não** é classificado como `V12_SCOPE=NOT_APPLICABLE`: o step de aplicabilidade não chegou a executar.

A correção seguinte altera somente os dois números medidos no README raiz e preserva este failure como parte da trilha de auditoria. Nenhum gate foi relaxado.

## 8. Ausência de mutação Databricks

Nem a integração S7 nem esta auditoria executaram:

- deploy de App;
- alteração de ACL ou grupos;
- workspace theme;
- `Import theme` remoto;
- `Publish`;
- edição de dashboard real;
- persistência no workspace;
- criação/alteração de UC Volume;
- qualquer outra mutação Databricks.

## 9. Fronteira com V14

A V13 encerra consolidação operacional e handoff. Permanecem reservados à V14, sem antecipação nesta auditoria:

- production readiness final;
- owner operacional definitivo e substitutos;
- suporte sustentado;
- severidades/incidentes formais;
- SLA/SLO apenas se houver base real;
- escalonamento e canais corporativos;
- retenção/housekeeping final;
- custos observados em operação real;
- calendário de revisão/depreciação;
- decisão final de go-live.

**V14 não foi iniciada.**

## 10. Critério de fechamento

A V13 pode ser considerada encerrada no Git quando a reconciliação documental desta auditoria estiver integrada após:

1. CI do SHA exato da candidata documental;
2. medição/reconciliação fail-closed das métricas do README raiz;
3. merge sem drift de `main`;
4. certificação pós-merge da reconciliação;
5. preservação explícita da issue #57 e dos três casos `BLOQUEADO_AUTORIZACAO`.

A etapa seguinte exige decisão separada. **Não iniciar V14 por inferência deste fechamento.**
