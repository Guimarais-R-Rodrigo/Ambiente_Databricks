# V12 — testes e estado das evidências

## Estado atual

A V12 possui **evidência Git/local verde**, mas nenhuma operação Databricks real e nenhuma sessão UAT foram executadas. O primeiro head que concluiu integralmente o workflow V12 foi `c2cf064b1d1bb9983af75932b22976765df51c56`, no run `34910391401`.

Esse resultado prova a candidata Git/local daquele head. Não prova browser/runtime Databricks, permissão efetiva, deploy, import/export real, acessibilidade final ou compreensão de usuário.

## Suíte V12

`tools/tests/test_temas_v12.py` cobre:

- cinco casos humanos/ambientais canônicos herdados da V01;
- separação das três classes de evidência;
- preservação do fixture AI/BI como não importável;
- preservação do contrato V11 3/23/22 e dos três alvos diretos;
- recusa de `PASS` sem artefato ou sem oráculo explicitamente satisfeito;
- recusa de UAT sem participante autorizado;
- recusa de tempo não observado;
- recusa de mutação sem autorização e rollback;
- recusa de dados não sintéticos;
- export AI/BI stale ou divergente daquele revisado;
- drift semântico;
- fixture sintético usado como entrada Databricks;
- automação de `approximated` ou `unsupported`;
- publicação acidental;
- snapshot tratado como vínculo vivo;
- publicação de workspace theme sem autorização própria;
- contraste medido sem arredondamento oportunista;
- isolamento de identidade do App e ausência de ação de publicação;
- workflow read-only e sem credenciais ou cliente remoto Databricks.

## Gates da candidata Git

1. V12 específica;
2. regressões V01–V12;
3. compatibilidade visual V00;
4. paridade e contratos source/simulado já cobertos pelas regressões V07/V08/V10/V11 pertinentes;
5. validador estrutural/documental;
6. gate de escopo V12;
7. higiene de credenciais/identidade;
8. nenhum efeito remoto.

A V12 não altera produto `.assistant`; portanto não cria uma segunda cópia para manter manualmente. Os testes cumulativos exercitam as guardas permanentes de paridade das superfícies temáticas anteriores, inclusive AI/BI e App.

## Histórico preservado dos runs V12

| Run | Head | Resultado | Onde parou | Causa observada |
|---|---|---|---|---|
| `34908962030` | `fb2d0eaf319a37a1a62e322e7f8458a47097b4f0` | **FAILURE** | validador estrutural/documental | métricas stale do README raiz: identidade `1409` versus `1418` medida; links `1887` versus `1889` medidos; escopo/higiene ficou `SKIP` |
| `34909482529` | `a2347a3903ae3523d08da4fc83d16fa235a921b2` | **FAILURE** | escopo/higiene | `git fetch` redundante tentou autenticar depois que `persist-credentials: false` removeu corretamente a credencial do checkout; exit 128 |
| `34909599988` | `f1025c04cad574cd188c0809675a5edd1b9b7724` | **FAILURE** | escopo/higiene | run já disparado durante a transição e repetiu a mesma classe operacional do fetch redundante; suítes e validador anteriores permaneceram verdes |
| `34909800421` | `3b3538a5ad5a6b9bc4217d71a847651cb0bf83af` | **FAILURE** | escopo/higiene | regex Shell de higiene detectou os próprios literais de paths proibidos dentro do workflow e emitiu `V12_HYGIENE_FAIL` |
| `34910134591` | `53badbb723477e44d2df8f37b5ced7e025912c73` | **FAILURE** | escopo/higiene | autoinspeção Python do workflow ainda reconstruía um literal proibido e emitiu `V12_WORKFLOW_HYGIENE_FAIL` |
| `34910391401` | `c2cf064b1d1bb9983af75932b22976765df51c56` | **SUCCESS** | todos os gates concluídos | correção preservou a higiene e evitou auto-match; nenhum gate foi relaxado |

Todos os runs `FAILURE` acima continuam failures. Em nenhum deles uma etapa `SKIP` é tratada como `PASS`.

## Detalhe do primeiro run verde integral

Run `34910391401`, head `c2cf064b1d1bb9983af75932b22976765df51c56`:

- V12 específica: **26/26 PASS**;
- regressões cumulativas V01–V12: **483/483 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- métricas confirmadas pelo validador: `1418` arquivos na varredura de identidade e `1889` links fora da raiz analisada;
- gate de escopo/higiene: **PASS**;
- marcador do workflow: `V12_SCOPE=PASS`;
- marcador do workflow: `V12_REMOTE_MUTATION=0`.

O checkout permaneceu com `persist-credentials: false`, e o workflow teve permissões de conteúdo somente leitura. A correção das falhas intermediárias foi feita na instrumentação V12; V00–V11 e o runtime do Hub não precisaram ser alterados para obter o run verde.

## Testes negativos relevantes

A suíte falha fechado, entre outros, para:

- evidência ausente ou sem oráculo satisfeito;
- participante não autorizado;
- duração humana inventada;
- operação mutável sem autorização ou rollback;
- dado real em jornada que exige fixture sintética;
- SHA de export AI/BI stale;
- divergência entre export revisado e usado;
- alteração inesperada de semântica;
- tentativa de importar fixture sintético;
- automação de capacidade aproximada ou não suportada;
- publicação acidental;
- claim de propagação automática de snapshot;
- workspace theme/publicação sem autorização específica.

Esses testes demonstram que o **validador de evidência** recusa registros inválidos; eles não substituem a execução real dos cenários que simulam.

## O que não pode ser PASS ainda

Até execução real, permanecem `PENDENTE` ou `BLOQUEADO`:

- Visual Lab em browser/runtime Databricks;
- App V10 implantado e usado por pessoas;
- export real AI/BI;
- binding contra export real;
- import real em draft;
- workspace theme, permissões administrativas, snapshot e reaplicação;
- preservação real de queries, filtros e datasets;
- preservação real da semântica dos widgets;
- light/dark real;
- acessibilidade em render final;
- `DOC-02`, `DOC-03`, `A11-01`, `SEC-01`, `UAT-01`.

Nenhuma dessas lacunas foi convertida em aprovação por inferência.

## Regra para o head final da PR

O run `34910391401` certifica `c2cf064b1d1bb9983af75932b22976765df51c56`. Qualquer commit posterior deve executar novamente os gates; resultados antigos não aprovam uma árvore nova. O head exato submetido à PR draft deve ter sua própria rodada verde antes de ser apresentado para aceite.