# V12 — testes e estado das evidências

## Estado inicial

A V12 começa com **evidência Git/local apenas**. Nenhuma operação Databricks real e nenhuma sessão UAT foram executadas por esta candidata inicial.

## Suíte V12

`tools/tests/test_temas_v12.py` cobre:

- cinco casos humanos/ambientais canônicos herdados da V01;
- separação das três classes de evidência;
- preservação do fixture AI/BI como não importável;
- preservação do contrato V11 3/23/22 e dos três alvos diretos;
- recusa de `PASS` sem artefato;
- recusa de UAT sem participante autorizado;
- recusa de tempo não observado;
- recusa de mutação sem autorização/rollback;
- recusa de dados não sintéticos;
- export AI/BI stale/revisado divergente;
- drift semântico;
- fixture sintético usado como entrada Databricks;
- automação de `approximated` ou `unsupported`;
- publicação acidental;
- snapshot tratado como vínculo vivo;
- publicação de workspace-theme sem autorização própria;
- workflow read-only e sem credenciais/SDK remoto.

## Gates da candidata Git

1. V12 específica;
2. regressões V01–V12;
3. V00;
4. validador estrutural/documental;
5. gate de escopo V12;
6. higiene de credenciais/identidade;
7. nenhum efeito remoto.

Resultados de runs reais serão acrescentados sem reclassificar failures.

## O que não pode ser PASS ainda

Até execução real, permanecem `PENDENTE`/`BLOQUEADO`:

- Visual Lab em browser/runtime Databricks;
- App V10 implantado e usado por pessoas;
- export real AI/BI;
- binding contra export real;
- import real em draft;
- workspace theme/admin/snapshot/reaplicação;
- preservação real de queries/filtros/datasets;
- light/dark real;
- acessibilidade em render final;
- `DOC-02`, `DOC-03`, `A11-01`, `SEC-01`, `UAT-01`.
