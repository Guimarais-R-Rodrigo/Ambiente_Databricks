# V12 — testes e estado das evidências

## Estado atual

A V12 continua em andamento. A camada Git/local tem baseline verde anterior e `V12-AIBI-01` possui agora uma execução real `PASS` em ambiente Databricks autorizado, com uma tentativa real `FAIL` anterior preservada por classificação inadequada dos dados.

Human/UAT e as demais superfícies ambientais não são convertidos em PASS por esse resultado.

## Suíte V12

`tools/tests/test_temas_v12.py` cobre:

- cinco casos humanos/ambientais canônicos herdados da V01;
- separação das três classes de evidência;
- preservação do fixture AI/BI como não importável;
- preservação do contrato V11 3/23/22 e dos três alvos diretos;
- recusa de PASS sem artefato ou sem oráculo explicitamente satisfeito;
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
- workflow read-only e sem credenciais/cliente remoto Databricks.

`tools/tests/test_temas_v12_evidencia_real.py` acrescenta uma guarda permanente sobre a evidência executada:

- a tentativa real #1 precisa continuar `FAIL`;
- a tentativa real #2 precisa continuar `PASS` e ser aceita pelo mesmo `validate_evidence()` fail-closed;
- as queries sintéticas precisam continuar usando `FROM VALUES`;
- não podem voltar a referenciar `samples.nyctaxi`;
- não podem criar tabela, schema, Volume nem usar `INSERT`/`MERGE`.

Esse teste valida o registro versionado. Ele não substitui nem reexecuta a observação real no Databricks.

## Gates da candidata Git

1. V12 específica;
2. evidência real AI/BI versionada;
3. regressões V01–V12;
4. compatibilidade visual V00;
5. paridade/contratos source-simulado exercitados pelas regressões anteriores;
6. validador estrutural/documental;
7. gate de escopo V12;
8. higiene de credenciais/identidade;
9. nenhum efeito remoto pelo CI.

A V12 não altera produto `.assistant`; a incorporação da evidência adiciona somente documentação, registros, SQL sintético, teste e ajuste do workflow read-only.

## Histórico original dos runs V12

| Run | Head | Resultado | Onde parou | Causa observada |
|---|---|---|---|---|
| `34908962030` | `fb2d0eaf319a37a1a62e322e7f8458a47097b4f0` | FAILURE | validador | métricas stale do README (`1409→1418`, `1887→1889`); escopo/higiene SKIP |
| `34909482529` | `a2347a3903ae3523d08da4fc83d16fa235a921b2` | FAILURE | escopo/higiene | fetch redundante tentou autenticar após `persist-credentials:false` |
| `34909599988` | `f1025c04cad574cd188c0809675a5edd1b9b7724` | FAILURE | escopo/higiene | repetição da classe do fetch redundante durante a transição |
| `34909800421` | `3b3538a5ad5a6b9bc4217d71a847651cb0bf83af` | FAILURE | escopo/higiene | regex Shell detectou seus próprios literais |
| `34910134591` | `53badbb723477e44d2df8f37b5ced7e025912c73` | FAILURE | escopo/higiene | autoinspeção Python ainda reconstruía literal proibido |
| `34910391401` | `c2cf064b1d1bb9983af75932b22976765df51c56` | SUCCESS | todos os gates | primeiro baseline técnico integralmente verde |
| `34913817674` | `2dca57907153b599d59e0b13c6eca8dafe1e03b0` | SUCCESS | todos os gates | fechamento documental pré-PR no head exato |

Nenhum run FAILURE acima foi reclassificado e nenhum `SKIP` é tratado como PASS.

## Workflows reais da PR no head inicial `2dca579...`

Os sete workflows de `pull_request` terminaram em `success`:

- V01 `34914095510`;
- V00 `34914095471`;
- V02 `34914095495`;
- CI geral `34914095474`;
- V10 `34914095525`;
- V11 `34914095528`;
- V12 `34914095527`.

No V00, a etapa condicional `Gate da branch isolada sem depender da integração com main` ficou `SKIP` e permanece `SKIP`.

## Evidência real AI/BI

### Tentativa #1 — FAIL fail-closed

A primeira execução real usou o dashboard de exemplo baseado em `samples.nyctaxi.trips`. Import, Light/Dark, semântica e rollback funcionaram, mas o dado é público de amostra e não sintético. Como o contrato exige `synthetic_data_only=true`, o registro ficou `FAIL` com `oracle_met=false`.

Arquivo: `evidencias/V12-AIBI-01/V12-AIBI-01_attempt-01.json`.

### Tentativa #2 — PASS

As duas queries foram substituídas temporariamente por SQL `VALUES` sintético, sem criar ou persistir objetos. O candidato foi importado no draft e depois revertido.

Fatos principais:

- ambiente: `databricks_free_lab`;
- dashboard draft: verdadeiro;
- dados somente sintéticos: verdadeiro;
- rollback verificado: verdadeiro;
- template revisado/usado SHA-256: `3f381314d8f2c99733a1094601b65d6d59263bc7d7d090ac6d533cb89e438412`;
- semantic before = semantic after = `85c7477027f9f26586e757c753fd29e909aca0e56469be7adeaa595723ee238b`;
- `approximated_automated=false`;
- `unsupported_automated=false`;
- `published=false`;
- Light/Dark observado: verdadeiro;
- oráculo satisfeito: verdadeiro;
- rollback original/final normalizado: `79582c3964612a1d7ca4570efbdb7a53ea8585d9ffdf6a45527abf4abf88f69d`.

Arquivo: `evidencias/V12-AIBI-01/V12-AIBI-01_attempt-02.json`.

## Failures intermediários ao incorporar a evidência

A evidência adicionou arquivos versionados; isso deixou a métrica `repo (identidade)` do README stale. Os workflows falharam corretamente na validação documental. Esses failures são parte do histórico, não ruído a apagar.

### `79083bcbc3070e62c76bd2d671418900cbb29645`

- V12 `34978774818`: FAILURE — medido `1419`, documentado `1418`; escopo/higiene SKIP;
- V10 `34978774655`: FAILURE na validação estrutural/documental;
- V11 `34978774702`: FAILURE na validação estrutural/documental;
- CI geral `34978774632`: FAILURE no gate de validação;
- V00/V01/V02: SUCCESS.

### `0b531876e8beb20549af17b144cde66675e82092`

- V12 `34978818024`: FAILURE na validação estrutural/documental; escopo/higiene SKIP;
- V10 `34978817355`: FAILURE na validação estrutural/documental;
- V11 `34978817520`: FAILURE na validação estrutural/documental;
- CI geral `34978817473`: FAILURE no gate de validação;
- V00/V01/V02: SUCCESS.

### `efb1b24ceb64a09ec4dcea22f81710515f80556c`

- V12 `34979351097`: FAILURE;
  - V12 26/26 PASS;
  - evidência real 1/1 PASS;
  - regressões V01–V12 484/484 PASS;
  - V00 12/12 PASS;
  - validador: FAILURE porque mediu `1422` arquivos e o README declarava `1418`;
  - links permaneceram `1889`;
  - escopo/higiene: SKIP.
- V10 `34979351146`: FAILURE na validação estrutural/documental depois de suíte, sintaxe, regressões, V00 e bundle passarem;
- V11 `34979351167`: FAILURE na validação estrutural/documental depois de suíte, sintaxe, regressões e V00 passarem;
- CI geral `34979351152`: FAILURE no gate de validação;
- V00 `34979351137`: SUCCESS;
- V01 `34979351048`: SUCCESS;
- V02 `34979351188`: SUCCESS.

A correção desta rodada é documental: atualizar o estado real e a métrica medida no README. Nenhum gate é relaxado.

## Testes negativos relevantes

A suíte continua falhando fechado para:

- evidência ausente/oráculo não satisfeito;
- participante não autorizado;
- duração humana inventada;
- mutação sem autorização/rollback;
- dado não sintético onde sintético é requisito;
- SHA de export stale/divergente;
- drift semântico;
- fixture V11 usado como entrada Databricks;
- automação de capacidade aproximada/não suportada;
- publicação acidental;
- claim de propagação automática de snapshot;
- workspace theme/publicação sem autorização específica.

## O que ainda não é PASS

Apesar de `V12-AIBI-01 = PASS`, continuam `PENDENTE` ou `BLOQUEADO`:

- Visual Lab completo em browser/runtime (`V12-LAB-01`);
- App V10 real (`V12-APP-01`); deploy não autorizado;
- workspace theme/admin/snapshot/reaplicação (`V12-AIBI-02`); mutação não autorizada;
- `SEC-01`;
- `A11-01` completo;
- `DOC-02`;
- `DOC-03`;
- `UAT-01`.

Nenhuma dessas lacunas foi convertida em aprovação por inferência.

## Regra para o próximo head

O run `34979351097` comprova as suítes e a falha documental do head `efb1b24...`; não certifica o commit que corrige a documentação. O próximo head precisa repetir toda a cadeia e só poderá ser chamado de Git/local verde se suas próprias execuções terminarem corretamente.
