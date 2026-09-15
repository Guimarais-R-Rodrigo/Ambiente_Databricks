# Evidência V12 — AI/BI `V12-AIBI-01`

Data da execução: 15/09/2026.

Caso canônico: `V12-AIBI-01` — tema AI/BI em dashboard draft real.

Commit de produto/protocolo observado: `2dca57907153b599d59e0b13c6eca8dafe1e03b0`.

Ambiente sanitizado: `databricks_free_lab`.

## Resultado

Foram preservadas duas tentativas independentes.

### Tentativa 1 — `FAIL`

A primeira execução comprovou tecnicamente export/binding/import em draft, observação Light/Dark, ausência de `Publish`, invariância semântica e rollback. Ela foi mantida como **FAIL** porque o dashboard usava `samples.nyctaxi.trips`, dado público de amostra e não dado sintético. O contrato V12 exige `synthetic_data_only=true`; a evidência não foi promovida por conveniência.

Registro: `V12-AIBI-01_attempt-01.json`.

### Tentativa 2 — `PASS`

A segunda execução substituiu temporariamente as duas queries do dashboard por SQL `VALUES` inline, sem tabela, schema, Volume, arquivo ou outra persistência de dados. As queries exatas e sanitizadas estão versionadas nesta pasta.

O candidato V11 foi importado no mesmo dashboard **draft**. Foram observados Light e Dark. Não houve `Publish`, alteração de workspace theme, ACL ou deploy de App.

Entre o baseline sintético e o pós-import:

- `datasets` permaneceram estruturalmente idênticos;
- `pages` permaneceram estruturalmente idênticas;
- o hash semântico `sha256(canonical_json({datasets,pages}))` permaneceu `85c7477027f9f26586e757c753fd29e909aca0e56469be7adeaa595723ee238b`;
- somente `uiSettings.theme` foi materializado/alterado pelo tema;
- `widget.background` foi aplicado somente no membro `light`;
- `widget.corner_radius` ficou `12`;
- `visualization.categorical_palette` ficou com a paleta canônica V11;
- `published=false`.

Após o teste, o tema e as duas queries originais foram restaurados. A assinatura semântica normalizada do estado original e do estado final restaurado é `79582c3964612a1d7ca4570efbdb7a53ea8585d9ffdf6a45527abf4abf88f69d`.

Registro: `V12-AIBI-01_attempt-02.json`.

## Autorizações

- `AUTH-V12-AIBI-01-20260915-PR54`: `Import theme` em dashboard draft descartável, dados de teste, sem `Publish`;
- `AUTH-V12-AIBI-01-TEMP-CUSTOM-20260915-PR54`: customização temporária necessária para descobrir JSON Pointers nativos;
- `AUTH-V12-AIBI-01-SYNTH-VALUES-20260915-PR54`: substituição temporária das duas queries por `VALUES` sintéticos e rollback integral.

## Binding real observado

O template nativo real usado pelo binding possui SHA-256:

`3f381314d8f2c99733a1094601b65d6d59263bc7d7d090ac6d533cb89e438412`

JSON Pointers revisados:

- `widget.background` → `/widgetBackgroundColor/light`;
- `widget.corner_radius` → `/widgetCornerRadius`;
- `visualization.categorical_palette` → `/visualizationColors`.

Nenhum item `approximated` ou `unsupported` foi automatizado.

## Artefatos e privacidade

Os JSONs completos exportados do dashboard e as capturas de tela não são versionados aqui. O Git preserva apenas hashes SHA-256 e fatos sanitizados no registro de evidência. Isso evita gravar identificadores efêmeros do dashboard ou metadados de UI desnecessários.

As duas queries sintéticas, por outro lado, são versionadas integralmente porque foram geradas para este teste, não contêm dados reais e permitem auditar `synthetic_data_only=true`.

## Limites do `PASS`

Este `PASS` comprova somente `V12-AIBI-01`. Ele **não** comprova:

- workspace theme, herança, snapshot ou reaplicação (`V12-AIBI-02`);
- Databricks App (`V12-APP-01`);
- Visual Lab completo (`V12-LAB-01`);
- identidade/permissão efetiva de `SEC-01`;
- acessibilidade completa `A11-01`;
- `DOC-02`, `DOC-03` ou `UAT-01`;
- prontidão de produção;
- publicação de dashboard.

A primeira tentativa continua registrada como `FAIL`; não foi apagada nem reclassificada.
