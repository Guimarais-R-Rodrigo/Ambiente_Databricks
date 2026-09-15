# V12 — testes e estado das evidências

## Estado atual

A V12 continua em andamento. O head funcional endurecido `26f84d872bc6192ef67e792877934a5cd424e89a` possui 7/7 workflows reais da PR em `success`. `V12-AIBI-01` e `SEC-01` possuem execuções reais `PASS` em ambiente Databricks autorizado. `A11-01` foi executado com participante real autorizado e ficou **FAIL** por contraste insuficiente de texto monetário em Dark; a percepção humana não substituiu a medição objetiva. A tentativa AI/BI real `FAIL` anterior permanece preservada por classificação inadequada dos dados.

Human/UAT e as demais superfícies ambientais não são convertidos em PASS por esses resultados.

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
- workflow read-only e sem credenciais/cliente remoto Databricks.

`tools/tests/test_temas_v12_evidencia_real.py` acrescenta guardas permanentes sobre as evidências executadas:

- a tentativa AI/BI real #1 precisa continuar `FAIL`;
- a tentativa AI/BI real #2 precisa continuar `PASS` e ser aceita pelo mesmo `validate_evidence()` fail-closed;
- as queries sintéticas precisam continuar usando `FROM VALUES`;
- não podem voltar a referenciar `samples.nyctaxi`;
- não podem criar tabela, schema, Volume nem usar `INSERT`/`MERGE`;
- `SEC-01` precisa continuar com `identity_checked=true`, `permission_checked=true` e `synthetic_data_only=true`;
- o registro `SEC-01` não pode versionar e-mail, `workspace_id`, OpenSharing ID nem bytes da identidade;
- a permissão efetiva não pode ser sustentada por papel autodeclarado.

Esses testes validam os registros versionados. Eles não substituem nem reexecutam as observações reais no Databricks.

## Gates da candidata Git

1. V12 específica;
2. evidências reais AI/BI e SEC-01 versionadas;
3. regressões V01–V12;
4. compatibilidade visual V00;
5. paridade/contratos source-simulado exercitados pelas regressões anteriores;
6. validador estrutural/documental;
7. gate de escopo V12;
8. higiene de credenciais/identidade;
9. nenhum efeito remoto pelo CI.

A V12 não altera produto `.assistant`; a incorporação das evidências adiciona somente documentação, registros, SQL sintético, teste e ajuste do workflow read-only.

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

Nenhum run `FAILURE` acima foi reclassificado e nenhum `SKIP` é tratado como `PASS`.

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

## Evidência real `SEC-01`

`SEC-01_attempt-01.json` registra PASS ambiental observacional sem versionar PII. A identidade autenticada foi observada diretamente na UI e a permissão efetiva de edição foi comprovada pelas ações concluídas na mesma sessão sintética de `V12-AIBI-01` tentativa #2. Nenhum papel autodeclarado é usado como prova.

O registro contém somente fatos sanitizados e hashes dos artefatos observados. O teste permanente rejeitaria e-mail, `workspace_id`, OpenSharing ID ou tentativa de sustentar autorização por identidade autodeclarada.

## Failures intermediários ao incorporar as evidências

As evidências adicionaram arquivos versionados e as reconciliações documentais alteraram métricas medidas pelo validador. Os workflows falharam corretamente enquanto o bloco de métricas do README estava stale. Esses failures são parte do histórico, não ruído a apagar.

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

### `07a6dde44410855fd9170bf6e759a1ec3a2bf097`

A primeira reconciliação documental acertou `repo (identidade)=1422`, mas a edição do README reduziu a contagem real de links para `1887` e ainda declarava `1889`.

- V12 `34980425138`: FAILURE no validador; as suítes V12, evidência real, regressões e V00 passaram antes da falha; escopo/higiene ficou `SKIP`;
- V10 `34980425181`: FAILURE na validação estrutural/documental depois dos gates anteriores passarem;
- V11 `34980425298`: FAILURE na validação estrutural/documental depois dos gates anteriores passarem;
- CI geral `34980425337`: FAILURE no gate de validação, com medição real `1422` arquivos / `1887` links;
- V00 `34980425517`: SUCCESS;
- V01 `34980425371`: SUCCESS;
- V02 `34980425547`: SUCCESS.

### Incorporação de `SEC-01` e incidente Git preservado

Uma chamada incorreta produziu o commit `468eb637b2a3c5f76ceb1ea0cafdf4db999f7787`, no qual `README.md` ficou temporariamente substituído por um placeholder. A correção foi aditiva: nenhum reset e nenhum force. O commit fast-forward `4823f3ab13b7a153873003fd42b50e454f931dfd` restaurou byte a byte o README anterior e incorporou o registro `SEC-01` + teste. A comparação líquida contra o baseline anterior mostrou apenas esses dois arquivos como mudança efetiva.

No head reparado:

- V12 `34986472469`: FAILURE no validador;
  - V12 26/26 PASS;
  - evidências reais 2/2 PASS;
  - regressões V01–V12 485/485 PASS;
  - V00 12/12 PASS;
  - validador: medido `1423`, documentado `1422`;
  - links `1887` corretos;
  - escopo/higiene: SKIP.

O failure foi preservado e a métrica congelada foi corrigida sem relaxar o validador.

## Baseline verde após `SEC-01`

Head `ad4a66f65ae390f2e98576dffac83635963ecab6`: **7/7 workflows reais da PR em success**.

- V01 `34987044469`;
- V00 `34987044317` — SUCCESS, com a etapa condicional da branch isolada em `SKIP`;
- V02 `34987044361`;
- CI geral `34987044538`;
- V10 `34987044459`;
- V11 `34987044460`;
- V12 `34987044468`.

Auditoria V12:

- 26/26 V12 PASS;
- 2/2 evidências reais PASS;
- 485/485 regressões PASS;
- 12/12 V00 PASS;
- validador `APROVADO: 0 falha(s), 0 aviso(s)`;
- `1423` arquivos / `1887` links;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`.

## Baseline endurecido antes de `A11-01`

Head `26f84d872bc6192ef67e792877934a5cd424e89a`: **7/7 workflows reais de `pull_request` em success**.

- V01 `35014029439`;
- V02 `35014029521`;
- V00 `35014029308` — SUCCESS, com `Gate da branch isolada sem depender da integração com main` em `SKIP`;
- V10 `35014029362`;
- CI geral `35014029316`;
- V11 `35014029450`;
- V12 `35014029276`.

Auditoria V12:

- 47/47 V12 PASS;
- 10/10 evidência/hardening permanente PASS;
- 514/514 regressões V01–V12 PASS;
- 12/12 V00 PASS;
- validador `APROVADO: 0 falha(s), 0 aviso(s)`;
- `1423` arquivos / `1887` links;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`.

O head intermediário `10785088ca85724fa298cf9681708eb5e5778eba` permanece historicamente FAILURE porque publicou matriz/validador endurecidos sem a suíte V12 correspondente; o reparo foi aditivo e não reclassificou esse failure.

## `A11-01` — tentativa #1, FAIL real preservado

Sessão em 15/09/2026, participante autorizado sanitizado como `P-MAINT-01`, papel `maintainer`, referência de autorização `AUTH-V12-A11-01-20260915-PR54`. O participante observou o render real do mesmo dashboard draft descartável, com queries temporariamente sintéticas por `VALUES`, sem `Publish`, e reportou **nenhuma irregularidade perceptiva** nos sete itens de revisão: Light/Dark, foco visível, alcançabilidade por teclado, keyboard trap, zoom 200%, dependência exclusiva de cor e rótulos/ícones.

A medição objetiva, porém, reprovou o oráculo. A coluna `Total Revenue` possui formatação condicional explícita do próprio dashboard: valores `< 51` usam texto `#9C2638`. Com o tema candidato importado, o fundo de widget em Dark é `#11171C`. Pela fórmula WCAG/sRGB, sem arredondar para aprovação:

- texto padrão `#11171C` sobre widget Light `#E8F4FD`: `16.154091708398724:1` — PASS contra 4,5:1;
- texto padrão `#E8ECF0` sobre widget Dark `#11171C`: `15.206494294052865:1` — PASS contra 4,5:1;
- `Total Revenue < 51`, `#9C2638` sobre widget Light `#E8F4FD`: `6.837793163467097:1` — PASS contra 4,5:1;
- `Total Revenue < 51`, `#9C2638` sobre widget Dark `#11171C`: `2.3624715346329377:1` — **FAIL** contra 4,5:1.

Logo, `A11-01 = FAIL` e `oracle_met=false`. A ausência de desconforto relatado pelo participante não substitui o limite objetivo. Nenhum texto foi classificado como “texto grande” para reduzir o limiar a 3:1.

Artefatos não versionados; somente hashes sanitizados são registrados aqui:

- export nativo após import do candidato: SHA-256 `1c136fa9218c49754caa849883a13cefb51a913ad5df7d47e773a5ea65085802`;
- captura Light 100%: SHA-256 `108cd1e5f2f9863aa9f190bcef2eca24a451a73e961d22e2104c2f7c016590e8`;
- captura Dark 100%: SHA-256 `717bb77127af33581303b7a1eeca715115087f9b9236084138dfd5975af2929a`;
- tema final restaurado: SHA-256 `71c8038d5b68b35ff888ea6bb7406dcfc74d5d1798b0af71626e592a2a50091b`;
- dashboard final restaurado desta sessão: SHA-256 `0ba3a8399728de7776c0c80ce505123e2553c44d864d47bd49283d8b0c000308`.

O rollback foi confirmado: as duas queries voltaram às versões originais com `samples.nyctaxi.trips`, e o tema retornou a `widgetHeaderAlignment = ALIGNMENT_UNSPECIFIED`. Em comparação com o export restaurado anterior, a única diferença foi uma quebra de linha final/linha vazia na query `route revenue`; não houve diferença lógica de SQL, layout, widgets ou tema.

A causa está fora dos três bindings diretos V11: `#9C2638` é cor explícita de formatação condicional do dashboard e não existe no repositório do Hub. A V12 **não** amplia a V11 nem automatiza campos `approximated`/`unsupported` para transformar esse FAIL em PASS. O achado precisa ser tratado como incompatibilidade de conteúdo/formatação do dashboard com Dark ou por uma decisão arquitetural posterior explicitamente aprovada.

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
- workspace theme/publicação sem autorização específica;
- identidade/permissão efetiva baseada apenas em autodeclaração.

## O que ainda não é PASS

Apesar de `V12-AIBI-01 = PASS` e `SEC-01 = PASS`, continuam sem PASS:

- `A11-01`: **FAIL observado** por contraste `2.3624715346329377:1` do texto `#9C2638` sobre fundo Dark `#11171C`;
- Visual Lab completo em browser/runtime (`V12-LAB-01`);
- App V10 real (`V12-APP-01`); deploy não autorizado;
- workspace theme/admin/snapshot/reaplicação (`V12-AIBI-02`); mutação não autorizada;
- `DOC-02`;
- `DOC-03`;
- `UAT-01`.

Nenhuma dessas lacunas foi convertida em aprovação por inferência.

## Regra para o próximo head

O run `35014029276` certifica o head `26f84d872bc6192ef67e792877934a5cd424e89a`; não certifica esta edição documental posterior. O novo head precisa repetir toda a cadeia e só poderá ser chamado de Git/local verde se suas próprias execuções terminarem corretamente.
