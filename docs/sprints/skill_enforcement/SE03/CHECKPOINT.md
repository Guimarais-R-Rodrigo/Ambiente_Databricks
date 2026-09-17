# SE03 — checkpoint de abertura

## Estado

**SE03 INICIADA.**

- baseline: `main@0f1a8b18e8e7380aad75be096b0ce167e14f9662`;
- origem: PR #74 / SE02 integrada por squash;
- branch: `sef/SE03-entrypoint-estrutural`;
- estratégia: branch-first, sem PR durante desenvolvimento;
- implementação funcional: **ainda não iniciada neste checkpoint**;
- publicação Databricks: não executada;
- GitHub Actions: não usados como motor iterativo.

## Fechamento herdado da SE02

A SE02 encerrou com:

```text
LOCAL_CERTIFICATION        = PASS
SYNTHETIC_AGENT_SCREENING = MIXED
DATABRICKS_FREE            = PASS
GITHUB_ACTIONS             = DEFERRED_CREDIT
FULLY_CERTIFIED            = false
HUMAN_ACCEPTANCE           = PASS
```

Limitações transferidas:

- F02-A1: bypass aceito quando o agente foi pressionado a pular o preflight;
- F02-A2: contexto declarado contraditório prevaleceu sobre fato derivável;
- L2 correto quando acionado, mas não obrigatório estruturalmente;
- ausência de trace/receipt para provar universalmente o caminho real.

## Decisões já congeladas pela revisão do plano

1. SE03 é o experimento principal de L3 estrutural.
2. Deve existir um único entrypoint canônico para o core protegido.
3. O entrypoint deve executar o preflight SE02 existente.
4. Deve haver verificação de integridade mínima da release.
5. O runner deve chamar apenas primitives canônicas nas etapas protegidas.
6. `ExecutionTraceV0` mínimo pertence à SE03.
7. Receipt formal pertence à SE04.
8. Postflight/conclusão fail-closed pertence à SE05.
9. E01–E12 entram no critério de aceite da SE03.
10. Provenance deve distinguir `runtime_derived`, `user_intent` e `agent_declared`.
11. Desenvolvimento é local-first e sem PR até release candidate.

## Decisões a congelar antes do código funcional

- path e assinatura do único runner;
- primitive set mínimo protegido;
- política exata para conflito de provenance;
- schema final de `ReleaseManifestV0`;
- schema final de `ExecutionTraceV0`;
- taxonomia mínima de falhas;
- mecanismo de instrumentação de primitives chamadas;
- definição de output sintético suficiente para E03/E08/E12;
- regra de detecção de trace stale;
- fronteira entre core protegido e etapas ainda interpretativas.

## Riscos de abertura

### R1 — runner virar segundo catálogo

Mitigação: runner referencia APIs públicas existentes; não copia lógica de helper.

### R2 — trace virar autorreporte

Mitigação: campos de chamadas/digests são derivados pelo código do runner/evaluator.

### R3 — fingerprint ornamental

Mitigação: manifest inclui somente artefatos necessários para provar acoplamento canônico.

### R4 — provenance resolvida por convenção textual

Mitigação: valor, source e evidence precisam de representação estruturada e testes E10.

### R5 — antecipar SE04/SE05

Mitigação: `ExecutionTraceV0` permanece mínimo; sem receipt formal ou postflight nesta sprint.

### R6 — abrir PR cedo e consumir CI

Mitigação: branch remota sem PR até local + Free + documentação estarem estabilizados.

## Primeiro vertical slice planejado

O primeiro incremento funcional deve ser deliberadamente pequeno:

1. API única do runner;
2. contexto sintético estruturado;
3. integridade do contrato + runner + uma primitive required;
4. chamada do preflight existente;
5. execução de uma única primitive canônica protegida;
6. `ExecutionTraceV0` mínimo;
7. evaluator que distingue execução pelo runner de chamada direta;
8. testes E01, E04 e E07.

Somente depois desse slice passar localmente o runner deve crescer para mais primitives e adversariais.

## Estado dos gates na abertura

```text
LOCAL_CERTIFICATION        = NOT_RUN_SE03
SYNTHETIC_AGENT_SCREENING = NOT_RUN_SE03
DATABRICKS_FREE            = NOT_RUN_SE03
GITHUB_ACTIONS             = NOT_RUN_SE03
FULLY_CERTIFIED            = false
PR                         = NOT_OPEN
```

## Próximo checkpoint

Fechar `DESENHO_TECNICO.md` com as decisões pendentes e implementar o primeiro vertical slice E01/E04/E07 sem abrir PR.