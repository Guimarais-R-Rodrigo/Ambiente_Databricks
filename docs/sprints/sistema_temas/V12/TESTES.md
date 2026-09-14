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

## Histórico preservado

### Run `34908962030` — FAILURE

Head: `fb2d0eaf319a37a1a62e322e7f8458a47097b4f0`.

- V12 específica: **26/26 PASS**;
- regressões cumulativas V01–V12: **483/483 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- validador estrutural/documental: **FAILURE** por duas métricas stale no README raiz;
- valor colado para `repo (identidade)`: `1409`; valor medido: `1418`;
- valor colado para `repo (links)`: `1887`; valor medido: `1889`;
- gate de escopo/higiene: **SKIP**, porque a etapa anterior falhou.

A causa é documental e compatível com a adição dos arquivos V12. A correção atualiza somente os valores medidos e o estado vivo da documentação; o validador não foi enfraquecido nem alterado. Este run permanece `FAILURE` no histórico.

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

Resultados de novos runs serão acrescentados sem reclassificar o `34908962030`.