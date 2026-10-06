# V14 — Production Readiness e Operação Sustentada do Sistema de Temas

> **Nota administrativa — 06/10/2026.** S0 e S1 estão integradas. S1 foi integrada pela PR #72 em `79f53ba1` (16/09/2026). Os slots `BLOCKED` na matriz permanecem sem owner/backup/autoridade evidenciados. S2–S8 não possuem início comprovado; não há readiness, go-live ou autorização Databricks. Os rótulos candidatos e próximos gates abaixo preservam o registro pré-merge.

## Registro histórico preservado

Status: **S0 aceita, integrada e certificada; S1 — ownership, autoridade e modelo operacional em execução. Candidata S1 ainda não aceita nem integrada.**

Data de abertura da S1: 16/09/2026.

Baseline Git da S1: `main@e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493`, merge da PR #71 que integrou a S0.

## Comece aqui

A V14 não adiciona um novo mecanismo visual. Ela é a etapa de **production readiness, operação sustentada e decisão final de go-live** do Sistema de Temas.

A S0 já foi encerrada no Git. A S1 agora responde a uma pergunta diferente: **quais responsabilidades e autoridades estão realmente evidenciadas e quais ainda precisam permanecer bloqueadas?**

Para uma pessoa não técnica, a regra principal é:

> um owner técnico documentado não vira automaticamente owner operacional, aprovador, responsável por incidente, autoridade de go-live ou autoridade para aceitar risco.

Se o repositório não comprovar owner, backup ou autoridade, a S1 registra `BLOCKED`. Ela não inventa a resposta.

Use estes documentos nesta ordem:

1. [Plano Mestre V14](PLANO_MESTRE.md) — contrato de escopo aceito e integrado;
2. [Matriz S1 de ownership e autoridade](MATRIZ_OWNERSHIP.json) — estado estruturado das seis superfícies;
3. [Modelo operacional S1](S1_MODELO_OPERACIONAL.md) — responsabilidade e escalonamento;
4. [Checkpoint S1](CHECKPOINT_S1.md) — baseline, findings, concorrência, failures e certificação;
5. [Checkpoint S0](CHECKPOINT_S0.md) — evidência histórica da etapa já integrada;
6. [Auditoria pós-merge V13](../V13/AUDITORIA_POS_MERGE.md) — fechamento operacional herdado.

## S0 encerrada

A S0 foi aceita e integrada pela PR #71 no merge real de dois pais:

`e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493`

Pais:

- `350dcf0b37e730042ef961f12f11b30b2660d2c6` — `main` anterior;
- `9a50abe4e9a4239dbffd62b9c2e5f055c9ac58a2` — HEAD S0 aceito e certificado.

No pós-merge, **16/16 workflows de `push` concluíram em `success`**. O workflow V14 passou guarda S0, regressões canônicas, V00, validador e fronteira read-only. V12 passou também aplicabilidade e higiene na `main`; V13 passou S1–S7 e suas fronteiras; o CI geral passou o gate sem credenciais.

Esse resultado encerra a S0 no Git. Não constitui production readiness nem autorização Databricks.

## O que a S1 faz

A S1 segue estritamente o Plano Mestre:

- referencia os owners técnicos já canônicos;
- materializa a matriz de ownership/autoridade;
- distingue owner técnico de responsabilidade operacional;
- define slots de owner operacional, backup, aprovação, incidente, go-live e risco residual;
- mantém esses slots `BLOCKED` quando não existe evidência concreta;
- define um runbook de responsabilidade e escalonamento;
- testa owner ausente, backup ausente, self-approval e autoridade inventada;
- preserva a separação V01 entre aprovação e publicação.

A S1 **não executa S2** e não cria `MATRIZ_READINESS.json`.

## Ownership técnico evidenciado

A S1 não muda os owners técnicos herdados da V13:

| Superfície | Owner técnico canônico |
|---|---|
| `notebook_visual_core` | V02 |
| `visual_lab` | V05 |
| `transition_bundle` | V09 |
| `databricks_app` | V10 |
| `aibi_dashboard` | V11 |
| `workspace_theme` | V11 |

Esses owners apontam para contratos e artefatos versionados. Eles não provam autoridade corporativa.

## Autoridade operacional: estado fail-closed

A [matriz S1](MATRIZ_OWNERSHIP.json) contém, para cada superfície:

- `operational_owner`;
- `backup_operational_owner`;
- `change_approver`;
- `incident_responsible`;
- `go_live_authority`;
- `residual_risk_authority`.

Na abertura da S1, nenhum desses slots possui identidade/autoridade concreta suficientemente evidenciada no repositório. Portanto **todos permanecem `BLOCKED`**.

Isso não significa que nenhuma pessoa real possa exercer esses papéis na organização. Significa apenas que a S1 não possui evidência versionada suficiente para afirmar quem é essa pessoa ou grupo.

Não foram inventados nomes, grupos, e-mails, canais, plantões, SLA/SLO, comitês ou autoridades.

## Política V01 preservada

A [governança V01](../V01/GOVERNANCA.md) continua sendo a fonte canônica de papéis:

- `Leitor` não aprova nem publica;
- `Proponente` não pode se autoaprovar;
- `Aprovador` revisa e decide aprovação, mas aprovação não implica poder técnico de publicação;
- `Publicador` promove somente revisão aprovada e autorizada;
- `Mantenedor` mantém contrato/testes, sem receber automaticamente aprovação estética ou administração de workspace.

A S1 não atribui esses papéis abstratos a pessoas reais sem evidência.

## Estados herdados preservados

| Item | Estado | Interpretação na S1 |
|---|---|---|
| `DOC-02` | `PASS` | somente no alcance documentado |
| `DOC-03` | `PASS` | somente no alcance documentado |
| `SEC-01` | `PASS` | somente no alcance observado |
| `UAT-01` | `PASS` | somente textual |
| `V12-AIBI-01` | `PASS` | somente no alcance V12 evidenciado |
| `HUMAN-01` | `PASS` | evidência formativa; não é readiness estatística |
| `A11-01` | `FAIL` | issue #57 permanece aberta |
| `V12-LAB-01` | `BLOQUEADO_AUTORIZACAO` | não reclassificado |
| `V12-APP-01` | `BLOQUEADO_AUTORIZACAO` | não reclassificado |
| `V12-AIBI-02` | `BLOQUEADO_AUTORIZACAO` | não reclassificado |

`PASS`, `FAIL`, `BLOQUEADO_AUTORIZACAO`, `BLOCKED` e `NOT_APPLICABLE` não são sinônimos.

## Contratos V11 congelados

A V14 referencia os owners anteriores e não cria segunda fonte de verdade.

A fronteira V11 permanece:

- `ResolvedTheme` como fonte configurável de verdade;
- `context="aibi"` reservado;
- 48 tokens = **3 `translated`, 23 `approximated`, 22 `unsupported`**;
- somente três bindings diretos;
- `cellFormat` fora do contrato de tokens;
- `approximated` e `unsupported` não automatizados;
- dashboard theme e workspace theme como superfícies distintas;
- `Import theme` distinto de `Publish`.

A S1 não copia schema, tokens, bindings, preflight, release/rollback ou protocolo de evidência.

## Concorrência

Na abertura da S1:

- PR #69 / SE01 está `ahead_by=21`, `behind_by=5` contra a `main` S0 e toca `README.md`;
- PR #51 / MM01 está `ahead_by=139`, `behind_by=183` e também toca `README.md`.

Essas frentes permanecem independentes. Qualquer avanço da `main` antes do aceite S1 exige reconciliação aditiva e nova certificação. Não será usado reset ou force-push como mecanismo de reconciliação.

## Guarda e CI V14

O workflow V14 continua read-only e passa a executar:

1. regressão da guarda histórica S0;
2. validador de ownership/autoridade S1;
3. testes S1, incluindo mutantes negativos;
4. regressões canônicas `test_temas*.py`;
5. compatibilidade V00;
6. `validate_assistant.py --conferir-readme`;
7. fronteira S1 read-only.

A S1 não usa credenciais Databricks e não executa rede ou mutação remota.

## Limites operacionais

Nesta S1:

- nenhuma mutação Databricks é executada;
- `V14_S1_REMOTE_MUTATION=0`;
- `V14_S1_DATABRICKS_MUTATION=0`;
- production readiness não é declarada;
- go-live não é decidido;
- issue #57 não é fechada;
- os três bloqueios V12 não viram PASS;
- owner técnico não vira autoridade corporativa por inferência;
- **S2–S8 não foram iniciadas**.

## Próximo gate

A S1 só poderá ser considerada candidata aceita depois de:

1. certificar o HEAD exato nos workflows reais;
2. preservar qualquer failure intermediário;
3. medir e reconciliar as métricas do README pelo runner;
4. reconfirmar `main`, merge-base, concorrência e issue #57;
5. demonstrar zero mutação Databricks e S2 não iniciada;
6. obter **aceite explícito do mantenedor**.

O aceite da S1 não inicia S2 automaticamente.
