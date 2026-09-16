# V13 — consolidação operacional do Sistema de Temas

## Estado vigente

A V13 está na etapa final **S7 — handoff operacional e fechamento**.

Cada sprint anterior só foi integrada depois de aceite explícito e certificação pós-merge da `main`.

Histórico integrado:

- S0 — PR #59, merge `1d46c9625fb5bfd6d1b666ddff055507238788bf`;
- S1 — PR #60, merge `70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`, pós-merge 15/15 `success`;
- S2 — PR #61, merge `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`, pós-merge 15/15 `success`;
- S3 — PR #62, merge `298dfb986f67cc4c560ae22b59d2fccad0716ec0`, pós-merge 15/15 `success`;
- S4 — PR #63, merge `29c3f1afa9147286627b18325380ce5b3c811331`, pós-merge 15/15 `success`;
- S5 — PR #64, merge `11e4e17f02d4ba7846f5b80bd88c0180124b5772`, pós-merge **16/16** `success`;
- S6 — PR #65, merge `6dfb8707835921f2f48020f383cf571902080109`, pós-merge **15/15** `success`.

A branch S7 nasce diretamente do merge S6 certificado. Nenhuma mutação Databricks foi executada para abrir esta etapa.

Para um operador novo, o ponto de entrada é:

- [S7 — handoff operacional e fechamento](S7_HANDOFF_OPERACIONAL.md).

O protocolo humano separado é:

- [S7 — homologação humana do handoff](S7_HOMOLOGACAO_HUMANA.md).

Estado humano atual:

`HUMAN-01 = PASS` — `HUMAN_EVIDENCE_RECORDED`.

A sessão real foi registrada pelo mantenedor com participante sanitizado `Tester`, autorizado e não construtor, duração de 5 minutos, zero ajuda, zero erros e H1–H6 em PASS. Esse resultado é formativo e não constitui production readiness.

**V14 não foi iniciada.**

## Baseline certificado da S7

Baseline Git:

`6dfb8707835921f2f48020f383cf571902080109`

Esse SHA é o merge da S6 na `main`.

Antes da abertura da S7 foram confirmados:

- PR #65 integrada a partir do HEAD S6 certificado `ed8857c3004d5d6ba8ec6745f26be02b569d0091`;
- `main` apontando para o merge S6;
- **15 workflows de `push`** associados ao merge;
- **15/15 `success`**;
- workflow V13 pós-merge com S1–S6, regressões, V00, validador e fronteiras verdes;
- workflow V12 pós-merge com seu gate estrito de `push` executado em `success`;
- nenhuma mutação Databricks executada pela S6;
- issue #57 permanecendo aberta com `A11-01 = FAIL`;
- `V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` permanecendo `BLOQUEADO_AUTORIZACAO`.

A S7 não reaproveita branch anterior como linha paralela.

## Plano canônico

O [Plano Mestre V13](PLANO_MESTRE.md), aceito pela PR #58, continua sendo o contrato de escopo.

A ordem permanece:

`S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → aceite → merge → auditoria pós-merge → V14`

A S7 implementa exclusivamente **handoff operacional e fechamento candidato da V13**.

Entregáveis do Plano Mestre cobertos pelo handoff:

- guia “comece aqui” do operador;
- roteiro de primeira operação;
- matriz de decisão “o que fazer quando...”;
- registro/referência dos ensaios;
- lista de dívidas transferíveis à V14;
- plano de rollback do próprio release V13;
- checkpoint V13 após os gates finais.

A homologação humana mínima foi executada e registrada. O PASS humano não foi inferido pela CI: decorre da sessão real informada pelo mantenedor e será apenas verificado pelos gates automatizados. Ainda são necessários checkpoint final, recertificação do SHA exato e aceite explícito antes da integração S7/V13.

## Artefatos históricos preservados

Os artefatos de sprints integradas são evidência histórica e não são reescritos para fingir estado atual:

- [checkpoint S0](CHECKPOINT_S0.md);
- [inventário operacional S1](S1_INVENTARIO_OPERACIONAL.md);
- [checkpoint S1](CHECKPOINT_S1.md);
- [matriz operacional S1](MATRIZ_OPERACIONAL.json);
- [S2 — preflight operacional](S2_PREFLIGHT_OPERACIONAL.md);
- [checkpoint S2](CHECKPOINT_S2.md);
- [S3 — release, instalação, atualização e rollback](S3_RELEASE_OPERACIONAL.md);
- [checkpoint S3](CHECKPOINT_S3.md);
- [S4 — observabilidade e diagnóstico](S4_OBSERVABILIDADE_DIAGNOSTICO.md);
- [checkpoint S4](CHECKPOINT_S4.md);
- [S5 — compatibilidade e acessibilidade operacional](S5_COMPATIBILIDADE_ACESSIBILIDADE.md);
- [checkpoint S5](CHECKPOINT_S5.md);
- [S6 — ensaios operacionais por superfície](S6_ENSAIOS_OPERACIONAIS.md);
- [checkpoint S6](CHECKPOINT_S6.md);
- [checkpoint S7](CHECKPOINT_S7.md).

Exemplos de historicidade:

- a matriz S1 mantém `S2_NOT_IMPLEMENTED` porque registra o estado da S1;
- o relatório S6 mantém `s7_started = false` porque registra o momento da S6;
- checkpoints antigos podem dizer que a próxima sprint ainda não havia começado.

A S7 não “corrige” essas evidências históricas.

## Owners que a S7 compõe

A S7 não cria nova engine.

| Necessidade | Owner vigente |
|---|---|
| inventário/superfície/ação | S1 |
| readiness/preflight | S2 |
| release/staging/LKG/rollback | S3 |
| diagnóstico/evidência segura | S4 |
| compatibilidade/acessibilidade | S5 |
| ensaios locais/simulados | S6 |
| schema/hash/contexto do tema | V02 |
| Visual Lab | V05 |
| bundle/transporte | V09 |
| App | V10 |
| AI/BI/workspace theme local policy | V11 |
| evidência/homologação histórica | V12 |

A S7 referencia esses owners. Não duplica token, role policy, schema, binding, manifesto ou catálogo de status.

## Handoff operacional

[S7_HANDOFF_OPERACIONAL.md](S7_HANDOFF_OPERACIONAL.md) orienta uma pessoa nova a:

1. identificar superfície/owner;
2. executar preflight S2;
3. interpretar `PASS`, `BLOCKED`, `FAIL` e `NOT_APPLICABLE`;
4. usar S4 diante de bloqueio/falha;
5. localizar release/rollback S3;
6. consultar S5 quando houver compatibilidade/acessibilidade;
7. distinguir ensaio local S6 de homologação real;
8. parar diante de autorização/identidade/evidência ausentes.

O treinamento S7 usa somente tema versionado e requests temporários sob `.artifacts/`:

- cenário notebook local esperado em `PASS`;
- cenário workspace theme esperado em `BLOCKED`.

Nenhum cenário requer Databricks real.

## Gate humano

[S7_HOMOLOGACAO_HUMANA.md](S7_HOMOLOGACAO_HUMANA.md) define seis oráculos:

- H1 — navegação;
- H2 — notebook/preflight local;
- H3 — interpretação do workspace `BLOCKED`;
- H4 — diagnóstico;
- H5 — rollback;
- H6 — segurança/privacidade.

O participante precisa ser autorizado e não ter construído o procedimento. Não pode receber instrução verbal do autor durante a tarefa.

Sessão registrada:

- `participant_id = Tester`;
- autorizado = `true`;
- não construtor = `true`;
- duração = `5 minutos`;
- ajuda verbal = `0`;
- ajuda documental extra = `0`;
- erros de interpretação = `0`;
- H1–H6 = `PASS`.

Estado atual:

`HUMAN-01 = PASS`.

Esse PASS cobre somente a homologação humana formativa do handoff. Não altera resultados V12, não fecha #57 e não substitui production readiness V14.

## Estados herdados preservados

A S7 não altera os resultados V12:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance de ambiente observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 evidenciado;
- `A11-01 = FAIL`, issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

O aceite para iniciar S7 não foi interpretado como autorização para reexecutar os três casos ambientais bloqueados.

## Contratos V11 que continuam congelados

- `ResolvedTheme` continua fonte configurável de verdade;
- `context="aibi"` continua reservado;
- 48 tokens = 3 `translated`, 23 `approximated`, 22 `unsupported`;
- únicos bindings diretos: `surface.card -> widget.background`, `palette.categorical -> visualization.categorical_palette`, `card.radius_px -> widget.corner_radius`;
- `dashboard_sintetico.json` não é import nativo;
- `cellFormat` não vira token;
- `approximated`/`unsupported` não são automatizados;
- dashboard theme ≠ workspace theme;
- `Import theme` ≠ `Publish`.

## Dívidas e fronteira V14

A S7 registra para continuidade, sem resolver por decreto:

- A11-01/issue #57;
- três casos ambientais V12 ainda bloqueados;
- estados visuais não observados que não podem ser inferidos.

Permanecem reservados à V14:

- production readiness final;
- owner operacional definitivo/substitutos;
- suporte sustentado;
- severidades/incidentes formais;
- SLA/SLO somente se houver base real;
- escalonamento/canais corporativos;
- retenção/housekeeping final;
- custos observados em operação real;
- calendário de revisão/depreciação;
- decisão final de go-live.

A S7 não inventa esses elementos.

## CI e fronteiras

O workflow V13 permanece:

- `permissions: contents: read`;
- checkout `persist-credentials: false`;
- sem `DATABRICKS_HOST`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

A candidata executa S1/S2/S3/S4/S5/S6/S7 antes das regressões completas.

Fronteiras vivas S7:

- `V13_S7_NETWORK=0`;
- `V13_S7_REMOTE_MUTATION=0`;
- `V13_S7_DATABRICKS_MUTATION=0`;
- `V13_S7_HUMAN_VALIDATION=PASS`;
- `V13_S7_HUMAN_EVIDENCE=VERSIONED_HUMAN_SESSION`;
- `V13_V14_NOT_STARTED=1`.

A antiga asserção `V13_S7_NOT_STARTED=1` permanece apenas como fato histórico da S6, não como fronteira viva.

## Rollback do release V13

O LKG Git antes do fechamento S7 é o merge S6:

`6dfb8707835921f2f48020f383cf571902080109`.

Se a futura integração S7 causar regressão, o handoff exige reversão normal do merge em branch/PR própria, preservação da evidência e recertificação. Force-push/reset da `main` não fazem parte do runbook.

Como a S7 não executa mutação Databricks, ela não cria estado remoto para apagar. Qualquer rollback remoto futuro continua pertencendo ao owner específico e a uma autorização separada.

## Métricas do README raiz

O protocolo de medição continua fail-closed:

1. a inclusão do checkpoint S7 muda a árvore;
2. o runner mede identidade e links reais;
3. qualquer failure fica preservado;
4. o README raiz só é reconciliado com números observados;
5. o SHA final é recertificado.

## Próxima ação

A candidata S7 já concluiu:

1. suíte própria e regressões S1–S6/V01–V13/V00;
2. validação documental e fronteiras;
3. homologação humana real e sanitizada;
4. criação de `CHECKPOINT_S7.md` com a evidência real.

Restam:

5. medir/reconciliar a árvore que contém o checkpoint;
6. recertificar o HEAD exato;
7. reconfirmar `main`, merge-base, ahead/behind, diff, issue #57 e concorrência;
8. parar para aceite explícito antes de integrar/encerrar V13.

`HUMAN-01 = PASS` não significa que a PR já esteja integrada ou que V14 tenha começado.

**V14 não foi iniciada.**
