# Checkpoint V14 — S1: ownership, autoridade e modelo operacional

Data: 16/09/2026.

Branch: `codex/temas-v14-s1-ownership-autoridade-20260916`.

Estado: **S1 em execução; candidata ainda não aceita nem integrada. Métricas medidas e correção fail-closed pendente de recertificação. S2 não iniciada.**

## 1. Baseline S0 integrado e certificado

A S1 nasce exclusivamente depois do aceite e fechamento da S0.

- PR S0: #71;
- HEAD S0 aceito: `9a50abe4e9a4239dbffd62b9c2e5f055c9ac58a2`;
- merge S0 / `main` de abertura S1: `e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493`;
- pais do merge: `350dcf0b37e730042ef961f12f11b30b2660d2c6` + `9a50abe4e9a4239dbffd62b9c2e5f055c9ac58a2`;
- pós-merge S0: **16/16 workflows de `push` em `success`**;
- workflow V14 pós-merge: guarda S0, regressões canônicas, V00, validador e fronteira read-only em `success`;
- V12 pós-merge: protocolo, evidência, regressões, V00, validador, aplicabilidade e higiene em `success`;
- V13 pós-merge: S1–S7, regressões, V00, validador e fronteiras em `success`;
- CI geral pós-merge: gate sem credenciais em `success`.

A S0 está encerrada no Git. Este checkpoint não reabre a S0.

## 2. Contrato canônico da S1

O Plano Mestre define a S1 como **Ownership, autoridade e modelo operacional**.

A S1 deve:

- transformar owner técnico/handoff em responsabilidade operacional explícita;
- definir substituição, aprovação e autoridade para risco/go-live sem inventar pessoas ou canais;
- entregar matriz de ownership/autoridade;
- entregar runbook de responsabilidade/escalonamento;
- testar owner ausente, self-approval indevido e autoridade inventada;
- falhar fechado: owner, backup ou autoridade não evidenciados => `BLOCKED`.

S2 e `MATRIZ_READINESS.json` não pertencem à S1.

## 3. Evidência encontrada

### Ownership técnico

O V13 já evidencia owners técnicos por superfície e a S1 apenas os referencia:

| Superfície | Owner técnico |
|---|---|
| `notebook_visual_core` | V02 |
| `visual_lab` | V05 |
| `transition_bundle` | V09 |
| `databricks_app` | V10 |
| `aibi_dashboard` | V11 |
| `workspace_theme` | V11 |

A V01 continua sendo a política canônica de papéis e proíbe self-approval quando revisão independente é exigida. Aprovação não implica poder de publicação.

### Ownership e autoridade operacionais

Não foi encontrada no repositório evidência suficiente para promover a `EVIDENCED`, em nenhuma das seis superfícies:

- owner operacional;
- backup operacional;
- aprovador de mudança real;
- responsável por incidente real;
- autoridade de go-live;
- autoridade de risco residual.

Resultado correto: **todos esses slots permanecem `BLOCKED`**.

A S1 não transforma um papel abstrato da V01 em identidade real, nem transforma um owner técnico V02/V05/V09/V10/V11 em autoridade corporativa.

## 4. Concorrência na abertura da S1

Fotografia após o merge S0:

- PR #69 / SE01: comparação contra `main@e89ef4f...` = `ahead_by=21`, `behind_by=5`, merge-base `350dcf0b37e730042ef961f12f11b30b2660d2c6`; toca `README.md` e permanece iniciativa própria;
- PR #51 / MM01: `ahead_by=139`, `behind_by=183`, merge-base `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`; toca `README.md` e permanece iniciativa própria.

Nenhuma dessas frentes é incorporada silenciosamente pela S1. Se a `main` avançar antes do aceite, a branch S1 deverá reconciliar o avanço de forma aditiva e ser recertificada.

## 5. Estados herdados preservados

- `DOC-02 = PASS` no alcance documentado;
- `DOC-03 = PASS` no alcance documentado;
- `SEC-01 = PASS` no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` no alcance evidenciado;
- `HUMAN-01 = PASS` somente como evidência formativa, sem inferência estatística;
- `A11-01 = FAIL` e issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

V11 permanece congelada: 48 tokens = 3 `translated` + 23 `approximated` + 22 `unsupported`; somente três bindings diretos; `context="aibi"` reservado; `cellFormat` fora do contrato de tokens.

## 6. Artefatos S1

A candidata materializa:

- `MATRIZ_OWNERSHIP.json` — referências técnicas + slots operacionais fail-closed;
- `S1_MODELO_OPERACIONAL.md` — responsabilidade, autoridade e escalonamento;
- `CHECKPOINT_S1.md` — baseline, findings, concorrência, failures e certificação;
- `tools/temas_v14_ownership.py` — validador local/read-only;
- `tools/tests/test_temas_v14_s1.py` — positivos, negativos e fronteiras;
- evolução do workflow V14 para executar S0 histórica + S1 antes das regressões.

A guarda S0 continua histórica e não deve impedir uma S1 legitimamente autorizada. O checkpoint S0 não é reescrito para fingir que S1 já existia naquele momento.

## 7. Não-escopo S1

A S1 não altera:

- `.assistant/**`;
- `Novo_Ambiente_Simulado/**`;
- runtime Python do produto;
- schema/tokens/consumidores;
- App V10;
- binder V11;
- contratos/evidências V01–V13;
- `V14/PLANO_MESTRE.md`;
- `CHANGELOG.md`.

Também não executa:

- deploy de App;
- ACL/grupos/compute;
- workspace theme;
- `Import theme` remoto;
- `Publish`;
- edição real de dashboard;
- persistência Databricks;
- aceite de risco residual;
- production readiness;
- decisão de go-live;
- S2.

## 8. Failures intermediários preservados

Os failures abaixo permanecem historicamente verdadeiros para os SHAs em que ocorreram. Nenhum deles é reclassificado retroativamente como PASS.

### Failure 1 — teste de imports excessivamente amplo

HEAD `a0479a5748cd0a5fc0feca4e11d4222f8a00cce2`, workflow V14 run `35131346020`, job `104912834882`.

- regressão histórica S0: `success`;
- CLI do validador S1: `success`;
- testes S1: **21/22 PASS, 1 FAIL**;
- teste que falhou: `test_validator_has_no_network_databricks_or_mutation_clients`;
- causa: a primeira versão do teste procurava a substring `databricks` no código-fonte completo e confundia o identificador legítimo `databricks_app` com import/cliente Databricks;
- regressões canônicas, V00, validador estrutural e fronteira S1 ficaram `skipped` no workflow V14 após esse failure;
- workflows independentes V00/V01/V02 concluíram em `success`;
- CI/V10/V11/V12/V13/V14 concluíram em `failure` pela propagação do mesmo teste S1 na suíte global, não por seis defeitos semânticos distintos.

A correção `26831f88f219ba3ed401b4dd9922385e3223627f` alterou somente `tools/tests/test_temas_v14_s1.py`, substituindo busca textual por inspeção AST dos imports proibidos. Matriz, runbook, README e métricas não foram alterados nessa correção.

### Failure 2 — medição fail-closed das métricas S1

HEAD `26831f88f219ba3ed401b4dd9922385e3223627f`, workflow V14 run `35131705079`, job `104914028455`.

Antes do validador estrutural:

- regressão histórica S0: **17 testes OK, 1 `skipped` esperado** porque a allowlist S0 só se aplica à branch S0;
- validador S1: `success`;
- testes S1: **22/22 PASS**;
- regressões canônicas V01–V14 S1: **740 testes OK, 1 `skipped` histórico**;
- compatibilidade V00: **12/12 PASS**.

O runner mediu:

- repo identidade: **1490 arquivos**;
- repo links: **1978 links**;
- worktree extras: **0**;
- README ainda declarava 1485/1971;
- resultado do validador: **2 falhas / 0 avisos**;
- fronteira S1 ficou `skipped` depois do failure, e não é chamada de PASS.

No mesmo HEAD, V00/V01/V02 concluíram em `success`; CI/V10/V11/V12/V13/V14 concluíram em `failure` pela mesma divergência documental do snapshot README.

### Snapshot medido para a correção

Os únicos valores autorizados para corrigir o README são os observados pelo runner:

- repo identidade: **1490 arquivos**;
- repo links: **1978 links**;
- worktree extras: **0**.

A correção não relaxa o validador e não estima contagem. O HEAD resultante precisa ser recertificado integralmente.

## 9. Estado Git da candidata

- baseline S1: `e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493`;
- primeiro HEAD completo: `a0479a5748cd0a5fc0feca4e11d4222f8a00cce2`;
- segundo HEAD, após correção test-only: `26831f88f219ba3ed401b4dd9922385e3223627f`;
- PR: #72, Draft;
- S2 permanece não iniciada.

A certificação final será atribuída somente ao HEAD que contiver o snapshot medido 1490/1978, preservar este histórico e concluir os workflows reais. Se a `main` avançar, a certificação ficará stale e exigirá reconciliação aditiva.

## 10. Gate de aceite da S1

Antes de solicitar aceite, o HEAD exato deve demonstrar:

- matriz S1 válida;
- owner técnico exato nas seis superfícies;
- slots operacionais sem evidência em `BLOCKED`;
- negativos para owner ausente, backup ausente, self-approval e autoridade inventada;
- nenhuma identidade/canal corporativo inventado;
- regressões V01–V14 verdes;
- V00 verde;
- validador com métricas reais reconciliadas;
- issue #57 aberta;
- três bloqueios V12 preservados;
- zero mutação Databricks;
- `V14_S2_NOT_STARTED=1`;
- `main`, merge-base, ahead/behind e concorrência reconfirmados.

Mesmo após aceite S1, **S2 só pode começar com autorização explícita separada**.
