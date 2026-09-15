# Checkpoint V12 — homologação formativa em andamento

Data: 15/09/2026.

Branch: `codex/temas-v12-homologacao-jornadas-20260914`.

Base original: `d106ef3158e5827a2eec3aa183dbb3b47885c960`.

## Estado

A V12 permanece **aberta**. Há três estados distintos:

- **Git/local:** gates funcionais exercitados e baseline técnico anterior verde;
- **Databricks environment:** `V12-AIBI-01` possui PASS real autorizado; os demais casos ambientais continuam pendentes/bloqueados;
- **Human/UAT:** não executado para os casos canônicos que exigem participante real.

Nenhum desses estados é promovido por inferência. `V12-AIBI-01 = PASS` não significa `V12 = encerrada`.

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
- ausência de evidência, autorização, classificação de dados ou rollback falha fechado.

## Baseline Git/local anterior

Run `34913817674`, head `2dca57907153b599d59e0b13c6eca8dafe1e03b0`: **SUCCESS**.

- V12: 26/26 PASS;
- regressões V01–V12: 483/483 PASS;
- V00: 12/12 PASS;
- validador: 0 falhas / 0 avisos;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`.

Na PR #54, os sete workflows do evento `pull_request` daquele head concluíram em `success`; a etapa condicional do workflow V00 permaneceu `SKIP` e nunca foi reclassificada.

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

O teste permanente `tools/tests/test_temas_v12_evidencia_real.py` garante que a tentativa #1 continue FAIL, a tentativa #2 continue validável como PASS e as queries versionadas continuem sintéticas/`VALUES`.

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

Também permanecem failures os workflows disparados pelos commits intermediários de evidência. A causa foi documental: adicionar a evidência aumentou a contagem medida de arquivos e tornou o bloco de métricas do README stale; as suítes funcionais anteriores ao validador continuaram verdes.

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

Todos esses resultados permanecem com sua conclusão real. Nenhum `FAILURE` ou `SKIP` é chamado de PASS.

## Pendências canônicas da V12

Continuam sem evidência suficiente para PASS:

- `DOC-02`;
- `DOC-03`;
- `A11-01` completo;
- `SEC-01`;
- `UAT-01`;
- Visual Lab real (`V12-LAB-01`);
- App V10 real (`V12-APP-01`), cujo deploy não está autorizado;
- workspace theme/snapshot/reaplicação (`V12-AIBI-02`), cuja mutação administrativa não está autorizada.

## Trabalho paralelo e reconciliação

A PR #51 de micromodelos permanece trabalho paralelo legítimo. `CHANGELOG.md` continua deliberadamente fora desta candidata para não criar conflito documental artificial. Se a `main` avançar antes da integração, a V12 deve reconciliar sobre a base vigente sem force-push e repetir todos os gates.

## Próximo gate

Esta reconciliação atualiza o estado real e a métrica medida de arquivos sem criar novos artefatos. O commit resultante precisa de CI próprio. Só depois de uma árvore novamente verde a candidata pode prosseguir para as demais homologações. A PR #54 permanece draft e V13 permanece bloqueada.
