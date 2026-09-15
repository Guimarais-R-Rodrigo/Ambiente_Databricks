# Checkpoint V12 — homologação formativa em andamento

Data: 15/09/2026.

Branch: `codex/temas-v12-homologacao-jornadas-20260914`.

Base original: `d106ef3158e5827a2eec3aa183dbb3b47885c960`.

## Estado

A V12 permanece **aberta**. Há três estados distintos:

- **Git/local:** head `ad4a66f65ae390f2e98576dffac83635963ecab6` certificado 7/7 verde;
- **Databricks environment:** `V12-AIBI-01` e `SEC-01` possuem PASS real; os demais casos ambientais continuam pendentes/bloqueados;
- **Human/UAT:** não executado para os casos canônicos que exigem participante real.

Nenhum desses estados é promovido por inferência. `V12-AIBI-01 = PASS` e `SEC-01 = PASS` não significam `V12 = encerrada`.

## Decisões arquiteturais preservadas

- `ResolvedTheme` continua fonte configurável de verdade;
- `context="aibi"` continua reservado;
- matriz V11 continua 48 tokens = 3 `translated`, 23 `approximated`, 22 `unsupported`;
- somente `widget.background`, `visualization.categorical_palette` e `widget.corner_radius` são diretos;
- JSON nativo não é inventado;
- binding real exige bytes exportados, SHA-256 exato, JSON Pointers revisados e campos existentes;
- fixture V11 continua não importável;
- workspace theme e dashboard theme continuam escopos distintos;
- `Import theme` e `Publish` continuam gates separados;
- `approximated` e `unsupported` não são promovidos por observação informal;
- ausência de evidência, autorização quando aplicável, classificação de dados ou rollback quando aplicável falha fechado;
- identidade/permissão efetiva não é inferida de papel autodeclarado.

## Baseline Git/local atual

Head `ad4a66f65ae390f2e98576dffac83635963ecab6`: os sete workflows reais da PR concluíram com `success`.

- V01 `34987044469`: SUCCESS;
- V00 `34987044317`: SUCCESS, com a etapa condicional `Gate da branch isolada sem depender da integração com main` em `SKIP`;
- V02 `34987044361`: SUCCESS;
- CI geral `34987044538`: SUCCESS;
- V10 `34987044459`: SUCCESS;
- V11 `34987044460`: SUCCESS;
- V12 `34987044468`: SUCCESS.

No V12:

- V12: 26/26 PASS;
- evidências reais AI/BI + SEC-01: 2/2 PASS;
- regressões V01–V12: 485/485 PASS;
- V00: 12/12 PASS;
- validador: 0 falhas / 0 avisos;
- métricas: 1423 arquivos / 1887 links;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`;
- permissões do workflow: `Contents: read`, `Metadata: read`;
- checkout: `persist-credentials:false`.

O warning de Node 20 é da plataforma GitHub Actions, que força essas actions para Node 24; não é warning do validador do projeto.

## Homologação real `V12-AIBI-01`

### Autorizações

A execução ocorreu somente após autorização explícita do usuário, em três gates:

- `AUTH-V12-AIBI-01-20260915-PR54`: `Import theme` somente em dashboard draft descartável, sem `Publish`;
- `AUTH-V12-AIBI-01-TEMP-CUSTOM-20260915-PR54`: customização temporária para materializar/descobrir os campos nativos e rollback;
- `AUTH-V12-AIBI-01-SYNTH-VALUES-20260915-PR54`: substituição temporária das duas queries por SQL `VALUES` exclusivamente sintético e restauração integral.

Workspace theme, ACL, deploy do App e publicação continuaram e continuam fora do escopo autorizado.

### Descoberta do binding real

O primeiro export nativo do dashboard materializava apenas `widgetHeaderAlignment`; nenhum dos três destinos diretos podia ser inventado. A jornada de customização temporária permitiu observar um template nativo real com SHA-256:

`3f381314d8f2c99733a1094601b65d6d59263bc7d7d090ac6d533cb89e438412`

JSON Pointers revisados:

- `widget.background` → `/widgetBackgroundColor/light`;
- `widget.corner_radius` → `/widgetCornerRadius`;
- `visualization.categorical_palette` → `/visualizationColors`.

O tema notebook canônico V11 permaneceu `hub-legado-notebook`, modo light. Portanto somente o membro `light` do fundo do widget foi ligado; o valor dark nativo foi preservado.

### Tentativa #1 — FAIL preservado

A primeira importação real funcionou tecnicamente:

- candidato aceito pelo Databricks;
- Light/Dark observados;
- três valores diretos corretos;
- sem mudança semântica do dashboard;
- `published=false`;
- rollback restaurado.

Mesmo assim o registro ficou **FAIL**, porque as queries usavam `samples.nyctaxi.trips`, dado público de amostra, e o contrato de `V12-AIBI-01` exige `synthetic_data_only=true`. A falha não foi apagada nem transformada em PASS depois.

Registro: `evidencias/V12-AIBI-01/V12-AIBI-01_attempt-01.json`.

### Tentativa #2 — PASS real

As duas queries foram temporariamente substituídas por SQL `VALUES` gerado especificamente para a homologação, sem leitura de tabela e sem criação/persistência de objeto.

O baseline sintético e o pós-import conservaram `datasets` e `pages` estruturalmente idênticos. Assinatura semântica:

`85c7477027f9f26586e757c753fd29e909aca0e56469be7adeaa595723ee238b`

antes = depois.

O Databricks aceitou o candidato e exportou os valores esperados:

- `widgetBackgroundColor.light = #E8F4FD`;
- `widgetBackgroundColor.dark = #11171C` preservado;
- `widgetCornerRadius = 12`;
- `visualizationColors` = paleta V11 canônica de 10 cores.

Light e Dark foram observados no browser; não houve `Publish`.

Depois do teste, tema e queries originais foram restaurados. A assinatura semântica normalizada original/final é:

`79582c3964612a1d7ca4570efbdb7a53ea8585d9ffdf6a45527abf4abf88f69d`.

Registro: `evidencias/V12-AIBI-01/V12-AIBI-01_attempt-02.json`.

## Homologação real `SEC-01`

`SEC-01` foi executado como observação no mesmo Databricks Free Edition e não exigiu nova mutação. O oráculo canônico exige que identidade e permissões efetivas sejam observadas no ambiente e proíbe tratar valor autodeclarado como autorização.

A identidade autenticada e o workspace foram observados diretamente no menu da conta. Por higiene e privacidade, o repositório não guarda nome, e-mail, identificador de workspace nem a captura com PII; o registro guarda somente hashes dos bytes recebidos/recortados e fatos sanitizados.

A permissão efetiva de edição foi demonstrada pelas ações concluídas na mesma sessão da tentativa sintética válida de `V12-AIBI-01`: edição temporária das queries e `Import theme` em dashboard draft. Nenhum rótulo de papel foi inventado ou usado como prova.

Registro: `evidencias/SEC-01/SEC-01_attempt-01.json`.

O teste permanente `tools/tests/test_temas_v12_evidencia_real.py` valida tanto a cadeia AI/BI quanto `SEC-01`, incluindo ausência de e-mail e identificadores sensíveis no JSON versionado.

## Failures V12 preservados — linha original

Nenhum failure anterior foi apagado ou reclassificado:

| Run | Head | Estado | Causa principal |
|---|---|---|---|
| `34908962030` | `fb2d0eaf319a37a1a62e322e7f8458a47097b4f0` | FAILURE | métricas stale do README; escopo/higiene SKIP |
| `34909482529` | `a2347a3903ae3523d08da4fc83d16fa235a921b2` | FAILURE | fetch redundante incompatível com checkout sem credencial persistida |
| `34909599988` | `f1025c04cad574cd188c0809675a5edd1b9b7724` | FAILURE | repetição da mesma classe operacional durante a transição |
| `34909800421` | `3b3538a5ad5a6b9bc4217d71a847651cb0bf83af` | FAILURE | auto-match da regex Shell de higiene |
| `34910134591` | `53badbb723477e44d2df8f37b5ced7e025912c73` | FAILURE | autoinspeção Python ainda detectava literal proibido reconstruído |

## Failures intermediários da incorporação de evidência

Também permanecem failures os workflows disparados pelos commits intermediários de evidência. As causas documentais não foram ocultadas e os gates não foram relaxados.

### Head `79083bcbc3070e62c76bd2d671418900cbb29645`

- V12 `34978774818`: FAILURE — validador mediu `1419` arquivos contra `1418` documentados; escopo/higiene SKIP;
- V10 `34978774655`: FAILURE na validação estrutural/documental;
- V11 `34978774702`: FAILURE na validação estrutural/documental;
- CI geral `34978774632`: FAILURE no gate que incorpora a validação documental.

### Head `0b531876e8beb20549af17b144cde66675e82092`

- V12 `34978818024`: FAILURE na validação estrutural/documental; escopo/higiene SKIP;
- V10 `34978817355`: FAILURE na validação estrutural/documental;
- V11 `34978817520`: FAILURE na validação estrutural/documental;
- CI geral `34978817473`: FAILURE no gate correspondente.

### Head `efb1b24ceb64a09ec4dcea22f81710515f80556c`

- V12 `34979351097`: FAILURE — 26/26 V12, 1/1 evidência real, 484/484 regressões e 12/12 V00 passaram; validador mediu `1422` arquivos contra `1418` no README; escopo/higiene SKIP;
- V10 `34979351146`: FAILURE somente depois de suas suítes/bundle/V00 passarem, na validação estrutural/documental;
- V11 `34979351167`: FAILURE somente depois de suas suítes/V00 passarem, na validação estrutural/documental;
- CI geral `34979351152`: FAILURE no gate de validação;
- V00 `34979351137`, V01 `34979351048` e V02 `34979351188`: SUCCESS.

### Head `07a6dde44410855fd9170bf6e759a1ec3a2bf097`

- V12 `34980425138`: FAILURE no validador porque a contagem documentada de links estava stale (`1889` documentado, `1887` medido); suítes anteriores passaram e escopo/higiene ficou SKIP;
- V10 `34980425181`, V11 `34980425298` e CI geral `34980425337`: FAILURE na mesma classe documental;
- V00 `34980425517`, V01 `34980425371` e V02 `34980425547`: SUCCESS.

### Incorporação de `SEC-01`

Durante a operação Git houve uma chamada incorreta que criou o commit `468eb637b2a3c5f76ceb1ea0cafdf4db999f7787`, substituindo temporariamente `README.md` por um placeholder na branch. O incidente foi declarado imediatamente e corrigido **sem reset e sem force** por novo commit fast-forward `4823f3ab13b7a153873003fd42b50e454f931dfd`, que restaurou byte a byte o blob anterior do README e incorporou a evidência `SEC-01`. A comparação líquida entre o baseline anterior e o commit reparado comprovou somente dois arquivos de diferença: o registro `SEC-01` e o teste de evidência real.

O workflow V12 `34986472469` no head `4823f3ab13b7a153873003fd42b50e454f931dfd` permaneceu **FAILURE**: 26/26 V12, 2/2 evidências reais, 485/485 regressões e 12/12 V00 passaram; o validador mediu `1423` arquivos contra `1422` documentados; escopo/higiene ficou SKIP. A métrica foi então reconciliada no head `ad4a66f65ae390f2e98576dffac83635963ecab6`, que obteve 7/7 workflows verdes.

Todos esses resultados permanecem com sua conclusão real. Nenhum `FAILURE` ou `SKIP` é chamado de PASS.

## Pendências canônicas da V12

Continuam sem evidência suficiente para PASS:

- `DOC-02`;
- `DOC-03`;
- `A11-01` completo;
- `UAT-01`;
- Visual Lab real (`V12-LAB-01`);
- App V10 real (`V12-APP-01`), cujo deploy não está autorizado;
- workspace theme/snapshot/reaplicação (`V12-AIBI-02`), cuja mutação administrativa não está autorizada.

`SEC-01` deixou a lista de pendências porque seu oráculo ambiental foi satisfeito e validado; isso não promove nenhum caso humano.

## Trabalho paralelo e reconciliação

A PR #51 de micromodelos permanece trabalho paralelo legítimo. `CHANGELOG.md` continua deliberadamente fora desta candidata para não criar conflito documental artificial. Se a `main` avançar antes da integração, a V12 deve reconciliar sobre a base vigente sem force-push e repetir todos os gates.

## Próximo gate

A PR #54 permanece draft. O fechamento de `SEC-01` não autoriza deploy do App, workspace theme, ACL nem `Publish`. As próximas jornadas devem respeitar suas próprias classes de evidência e gates de autorização. V13 permanece bloqueada.
