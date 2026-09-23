# MM01 — checkpoint pós-merge

**Estado vigente:** `INTEGRADA`  
**Data:** 2026-09-23  
**Próxima sprint:** `MM02 = NOT_STARTED`

Este documento consolida o fechamento da MM01 sem reescrever os checkpoints, auditorias ou tentativas de certificação históricas.

## Identidade de integração

| Item | Valor |
|---|---|
| PR | #51 — `MM01 — contrato canônico de micromodelos` |
| HEAD da branch integrada | `fa1a3653e60472d171307663d1175344bb3f6a8d` |
| base imediatamente anterior ao merge | `4bc7c9aada96468505e51f279cf32c107d0b6dbb` |
| tree da branch integrada | `58beb10f5d849fa01f2c94f2ee682c2b3276ea1e` |
| merge commit | `73d7659dcf11509a7fba392221c4810d10401c35` |
| tree do merge | `58beb10f5d849fa01f2c94f2ee682c2b3276ea1e` |
| equivalência HEAD → merge | sem arquivos materiais no compare; mesma tree |
| estado da PR | `closed / merged=true` |
| aceite humano | explícito antes do merge, refletido também na mensagem do merge |

A `main` continuou avançando depois da MM01. No início desta revisão pós-merge ela estava em `dedde0741ed4c387c3a500adfbf7de2c6166aba5`, merge da SER00/PR #101. Isso não reabre a MM01.

## Fechamento técnico preservado

A última rodada versionada da campanha MM01 é a R10, executada sobre `c43273fbb0cf40c1b9a3bc176cc1d4fd11d781a6` contra `main@515e673b17f21d4c912d9ae866a7e31967fd4488`:

- 50 StepResults;
- 49 `PASS`;
- somente `V12_SCOPE_STRICT=SKIP_ALLOWED`;
- CI local 10/10;
- V00–V13 executáveis em PASS;
- snapshot `1682/2109/0`;
- preflight/postflight idênticos;
- bundle `MM01_LOCAL_CERT_R10_c43273fbb0cf.zip` com SHA-256 `34f0ea4518eb8d2c8042871b40451e8c956710b95ccc097d9cc23ca2b14ad6ab`.

A auditoria independente final não demonstrou blocker técnico nem violação material de R01–R08. A limitação probatória F-01 foi encerrada pela auditoria complementar com acesso byte a byte ao bundle; o veredito consolidado foi `APTA_PARA_CONTRADITORIO`. O contraditório final não encontrou divergência bloqueante.

O fechamento documental posterior foi preservado em `72e222718996d89f34ac200149f8594f1d534c86`. Depois, a `main` avançou pela manutenção A07/PR #105; a branch MM01 incorporou essa `main` por merge real e chegou ao HEAD final `fa1a3653e60472d171307663d1175344bb3f6a8d`. O merge da PR #51 registra que a integração ocorreu após certificação local, auditoria independente + complementar, contraditório final, fechamento documental e aceite humano explícito.

Não é criado aqui um número de rodada adicional que não exista nos documentos versionados. O histórico R1–R10 permanece exatamente como histórico.

## Revalidação e merge

O fechamento aceito registrou revalidação final sem blocker, com diff final restrito ao fechamento documental antes da integração. O estado Git hoje oferece ainda uma prova direta adicional: a tree do HEAD integrado da branch e a tree do merge da PR #51 são idênticas (`58beb10f...`), e o compare HEAD → merge não contém arquivos.

Isso comprova a integração material da candidata final, sem reclassificar nenhuma rodada anterior.

## Fronteiras preservadas

A MM01 integrou somente o contrato canônico da especificação e sua infraestrutura de validação. Permanecem fora dela:

- `spec_fingerprint` — MM02;
- descoberta metadata-only — MM03;
- `hub-ml-micromodelos` e primeiro briefing próprio — MM04;
- contrato definitivo de tracking/MLflow — MM06;
- publicação corporativa real e ACLs;
- migração de legado — MM12.

`GOVERNANCA_EXTERNA` continua a autoridade final de publicação.

## Estado de avanço

```text
MM00 = INTEGRADA
MM01 = ACEITA_E_INTEGRADA
MM02 = NOT_STARTED
```

A próxima execução funcional só pode começar depois do aceite e merge da revisão documental pós-MM01/SEF. Este checkpoint não inicia MM02.
