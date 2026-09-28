# G6 R9 bloqueada e recuperação R10

## Histórico preservado

- R8: `FAIL_FIRST_WRITE_PROTOCOL_ERROR`; autorização `issue#114:comment#5839374341` consumida; `domain-context-init` terminou com efeito `UNKNOWN`.
- R9: `BLOCKED_DEPENDENCY`; `databricks-sdk` ausente no venv ENV04; zero edição, instalação, commit, push ou acesso de rede.

## Estratégia R10

R10 preserva o manifest convergente e toda a classificação existente. A CLI continua restrita a autenticação e operações read-only. Em uma futura execução separadamente autorizada, o token U2M será obtido just-in-time por `databricks auth token`, mantido somente em memória e usado em uma única requisição material:

```text
POST /api/2.0/workspace/import
transport = Python http.client / HTTP/1.1
automatic_retry = false
```

A aquisição ocorre depois do preflight e do recheck convergente, mas antes do consumo atômico da autorização. Falha de autenticação não consome a autorização nem inicia write; falha depois de `write_started=true` permanece `UNKNOWN` e interrompe o fluxo.

## Autoridade

Esta revisão é somente autoria e qualificação local. Execução remota, authorization record, probes, Genie, cleanup, promoção, Ready e merge permanecem não autorizados.
