# V13 — consolidação operacional do Sistema de Temas

> **Nota administrativa — 06/10/2026.** O fechamento S7 em `62e94048` foi seguido pela V14; “V14 não iniciada” abaixo descreve somente aquele fechamento. Este documento preserva o escopo e a próxima ação previstos no fechamento original. [Estado atual de Temas](../README.md) é o dono da continuidade; não repetir gates antigos por inferência.

## Registro histórico preservado

## Estado vigente

A **V13 está integrada e encerrada no Git** após S0–S7, aceite explícito, merge da S7 e certificação pós-merge da `main`.

Histórico integrado:

- S0 — PR #59, merge `1d46c9625fb5bfd6d1b666ddff055507238788bf`;
- S1 — PR #60, merge `70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`;
- S2 — PR #61, merge `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`;
- S3 — PR #62, merge `298dfb986f67cc4c560ae22b59d2fccad0716ec0`;
- S4 — PR #63, merge `29c3f1afa9147286627b18325380ce5b3c811331`;
- S5 — PR #64, merge `11e4e17f02d4ba7846f5b80bd88c0180124b5772`;
- S6 — PR #65, merge `6dfb8707835921f2f48020f383cf571902080109`;
- **S7 — handoff operacional e fechamento** — PR #66, merge `62e9404851d6a7902371bd5b6531a113d521311c`.

O merge S7/V13 teve **15/15 workflows de `push` em `success`**. A [auditoria pós-merge](AUDITORIA_POS_MERGE.md) confirmou os gates e identificou somente drift documental nos READMEs vivos, tratado por reconciliação separada sem alteração de runtime.

`HUMAN-01 = PASS` — `HUMAN_EVIDENCE_RECORDED`.

A sessão humana foi registrada pelo mantenedor com participante sanitizado `Tester`, autorizado e não construtor, duração de 5 minutos, zero ajuda, zero erros de interpretação e H1–H6 em PASS. O resultado é formativo e não constitui production readiness.

**V14 não foi iniciada.**

## Para quem nunca entrou no Hub

A V13 não cria uma nova engine de tema. Ela organiza a operação segura das capacidades já construídas nas V01–V12.

Comece pelo [handoff S7](S7_HANDOFF_OPERACIONAL.md). O fluxo é:

1. identificar superfície e owner na [matriz operacional](MATRIZ_OPERACIONAL.json);
2. executar o preflight S2;
3. interpretar `PASS`, `BLOCKED`, `FAIL` e `NOT_APPLICABLE` sem promover bloqueios;
4. usar S4 para diagnóstico;
5. usar S3 para release, Last Known Good e rollback;
6. consultar S5 para compatibilidade/acessibilidade;
7. consultar S6 para ensaios locais/simulados;
8. usar S7 para navegar entre os owners sem instrução verbal do autor.

O treinamento S7 usa artefatos versionados/sintéticos e não requer Databricks real.

## Plano canônico concluído

O [Plano Mestre V13](PLANO_MESTRE.md) definiu:

`S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → aceite → merge → auditoria pós-merge → V14`

A V13 concluiu a parte anterior à V14: inventário, preflight, release/rollback local, diagnóstico, compatibilidade/acessibilidade, ensaios, handoff, homologação humana mínima, certificação e auditoria pós-merge.

Isso **não** equivale a production readiness, autorização permanente de ambiente ou decisão de go-live.

## Owners compostos

| Necessidade | Owner vigente |
|---|---|
| inventário/superfície/ação | S1 |
| readiness/preflight | S2 |
| release/staging/LKG/rollback | S3 |
| diagnóstico/evidência segura | S4 |
| compatibilidade/acessibilidade | S5 |
| ensaios locais/simulados | S6 |
| handoff | S7 |
| schema/hash/contexto do tema | V02 |
| Visual Lab | V05 |
| bundle/transporte | V09 |
| App | V10 |
| AI/BI/workspace theme | V11 |
| evidência/homologação histórica | V12 |

A V13 referencia esses owners; não duplica token, role policy, schema, binding, manifesto ou catálogo de status.

## Estados herdados preservados

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 evidenciado;
- `A11-01 = FAIL`, issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

O PASS humano S7 não altera esses estados nem autoriza os três casos ambientais bloqueados.

## Contratos V11 preservados

- `ResolvedTheme` continua fonte configurável de verdade;
- `context="aibi"` continua reservado;
- 48 tokens = 3 `translated`, 23 `approximated`, 22 `unsupported`;
- únicos bindings diretos: `surface.card -> widget.background`, `palette.categorical -> visualization.categorical_palette`, `card.radius_px -> widget.corner_radius`;
- `dashboard_sintetico.json` não é import nativo;
- `cellFormat` não vira token;
- `approximated`/`unsupported` não são automatizados;
- dashboard theme ≠ workspace theme;
- `Import theme` ≠ `Publish`.

## Certificação pós-merge

No merge `62e9404851d6a7902371bd5b6531a113d521311c`, o workflow V13 run `35106812430` confirmou:

- S1 20/20, S2 27/27, S3 21/21, S4 30/30, S5 32/32, S6 28/28 e S7 28/28 PASS;
- regressões V01–V13: 701/701 PASS;
- V00: 12/12 PASS;
- validador: 0 falhas / 0 avisos;
- `V13_S7_NETWORK=0`;
- `V13_S7_REMOTE_MUTATION=0`;
- `V13_S7_DATABRICKS_MUTATION=0`;
- `V13_S7_HUMAN_VALIDATION=PASS`;
- `V13_S7_HUMAN_EVIDENCE=VERSIONED_HUMAN_SESSION`;
- `V13_V14_NOT_STARTED=1`.

No mesmo SHA, o workflow V12 run `35106812487` executou seu gate de `push` com `V12_SCOPE=APPLICABLE`, higiene em PASS e zero mutação remota.

## Rollback

O Last Known Good Git anterior à S7 é o merge S6:

`6dfb8707835921f2f48020f383cf571902080109`.

Se o merge S7 precisar ser revertido, use reversão normal em branch/PR própria e nova certificação. Não use force-push/reset da `main`.

## Evidência histórica

Checkpoints antigos permanecem como retrato do momento em que foram produzidos. Eles não são reescritos para fingir o estado atual.

- [checkpoint S0](CHECKPOINT_S0.md)
- [inventário S1](S1_INVENTARIO_OPERACIONAL.md)
- [checkpoint S1](CHECKPOINT_S1.md)
- [S2](S2_PREFLIGHT_OPERACIONAL.md) e [checkpoint S2](CHECKPOINT_S2.md)
- [S3](S3_RELEASE_OPERACIONAL.md) e [checkpoint S3](CHECKPOINT_S3.md)
- [S4](S4_OBSERVABILIDADE_DIAGNOSTICO.md) e [checkpoint S4](CHECKPOINT_S4.md)
- [S5](S5_COMPATIBILIDADE_ACESSIBILIDADE.md) e [checkpoint S5](CHECKPOINT_S5.md)
- [S6](S6_ENSAIOS_OPERACIONAIS.md) e [checkpoint S6](CHECKPOINT_S6.md)
- [handoff S7](S7_HANDOFF_OPERACIONAL.md)
- [homologação humana S7](S7_HOMOLOGACAO_HUMANA.md)
- [checkpoint S7](CHECKPOINT_S7.md)
- [auditoria pós-merge](AUDITORIA_POS_MERGE.md)

## Fronteira V14

Permanecem reservados à V14: production readiness final, owner operacional definitivo/substitutos, suporte sustentado, severidades/incidentes, SLA/SLO apenas com base real, escalonamento, retenção/housekeeping final, custos reais, revisão/depreciação e decisão final de go-live.

**V14 não foi iniciada.** A abertura da V14 exige decisão separada do mantenedor.
