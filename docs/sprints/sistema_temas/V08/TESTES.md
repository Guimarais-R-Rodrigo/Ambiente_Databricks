# V08 — testes e evidências

## Escopo automatizado

A V08 foi aberta a partir da `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`. Nenhuma mudança runtime é permitida nesta sprint.

A suíte específica `tools/tests/test_temas_v08.py` cobre:

- completude da matriz transversal;
- equivalência byte a byte entre superfícies `.assistant` alteradas e `Novo_Ambiente_Simulado`;
- equivalência entre as três cópias do Manual Técnico;
- remoção de rótulos vivos obsoletos V04/V05;
- template EDA sem paleta/tema paralelo, hexadecimais de política ou registro global legado recomendado;
- presença de `ResolvedTheme`, `load_reference_theme` e `aplicar_tema_resolvido` no fluxo de EDA;
- roteamento de Concierge/criação de objeto ao padrão central;
- skills de baseline, safra e monitoramento distinguindo aparência de cálculo/política;
- explicabilidade registrando SHAP/Matplotlib como limite de theming;
- workflow V08 permanente read-only.

O workflow também executa:

```bash
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/validate_assistant.py --conferir-readme
```

E reprova se `git diff` contra o SHA-base V08 contiver alteração Python em `ambiente_fonte/.assistant/hub_snippets/**` ou `hub_scripts/**`.

## Failures preservados

### `34866320427` — FAILURE antes da escrita

A migração transitória abortou antes de commit porque o regex do Manual exigia um próximo heading `##`, mas o Sistema de Temas era a última seção do arquivo. Nenhuma integração transversal foi persistida por esse run.

### `34866493021` — FAILURE transitório da primeira migração

A migração foi aplicada, mas a suíte V08 encontrou nomenclatura visual local residual no template EDA e o teste de workflow read-only reprovou corretamente porque o próprio run era write-enabled.

### `34866578667` — FAILURE permanente por nomenclatura residual

Com o workflow já read-only, restou apenas a nomenclatura local residual do template EDA. A correção removeu inclusive esses identificadores textuais.

### `34866767026` — FAILURE documental

Passaram V08 **22/22**, regressões V01–V08 **405/405** e V00 **12/12**. O bloqueio ficou restrito ao README raiz desatualizado.

### `34866944219` — FAILURE intermediário de espelho

Durante a revisão editorial do template EDA, fonte e simulado ficaram temporariamente diferentes entre dois commits sequenciais. A guarda de espelho reprovou corretamente.

### `34867002420` — FAILURE documental no head sincronizado

Passaram V08 **22/22**, regressões **405/405** e V00 **12/12**. O validador encontrou apenas métricas antigas no README raiz.

### `34867738695` — FAILURE de configuração transitória

Uma tentativa de reconciliação foi recusada antes da criação de jobs. Nenhum arquivo de produto foi alterado por esse run.

### `34867935251` e `34869358530` — FAILURES documentais de medição

Com checkpoint, índices e changelog estabilizados, os testes permaneceram verdes e o validador mediu o estado final pré-compactação do README. Os failures foram preservados e não mascarados.

### Checks da PR #42 no head `cf5f4523...`

V00, V01, V02 e V03 concluíram com `success`. CI geral, V04, V05, V06 e V08 falharam somente em validação documental. Nos workflows V04/V05/V06/V08, as suítes específicas, regressões cumulativas e V00 passaram antes da etapa documental. No CI geral, todas as demais etapas do gate local passaram.

### `34871141693` — FAILURE documental de uma linha

Depois da compactação do README raiz, passaram:

- V08: **22/22**;
- regressões V01–V08: **405/405**;
- V00: **12/12**.

O validador encontrou apenas uma divergência: `repo (links)` estava colado como 1851 e o valor real era **1850**. Foram **1 falha e 0 avisos**.

### `34871866915` — FAILURE documental após fechamento da candidata

Depois da atualização do checkpoint e deste registro, passaram novamente:

- V08: **22/22**;
- regressões V01–V08: **405/405**;
- V00: **12/12**.

A única divergência foi `repo (links)`: **1850 colado versus 1849 real**. Foram **1 falha e 0 avisos**. As etapas posteriores de guarda runtime e escopo foram corretamente puladas porque o validador já havia reprovado.

### `34873780887` — FAILURE de configuração no fechamento pós-merge

A primeira tentativa transitória de reconciliar o bloco V08 no changelog foi recusada pelo GitHub antes da criação de jobs porque o conteúdo multilinha não estava encapsulado de forma válida no YAML. Nenhum arquivo de produto ou changelog foi alterado por esse run.

### `34873908522` — FAILURE transitório com escrita controlada

A segunda tentativa usou o bloco do changelog codificado e a etapa `Reconciliar bloco V08 do changelog (transitório)` concluiu com `success`, produzindo o commit `8ea54df54d64e764f1d7a3f01d18e84ef7a7dde5`. A suíte V08 do próprio run reprovou depois, como esperado, porque o workflow daquela execução estava temporariamente com `contents: write` e `persist-credentials: true`; regressões posteriores foram puladas. O workflow permanente foi restaurado byte a byte para read-only no commit seguinte.

### `34874103274` — FAILURE documental no fechamento pós-merge

Com o workflow permanente novamente read-only, passaram antes do validador:

- V08: **22/22 PASS**;
- regressões V01–V08: **405/405 PASS**;
- V00: **12/12 PASS**.

O validador apontou uma única divergência, com **0 avisos**: `repo (links)` estava colado como **1849**, enquanto o estado documental pós-merge media **1850**. As etapas de guarda runtime e escopo foram corretamente puladas após a reprovação documental. Esse failure permanece evidência histórica e não é reclassificado.

Nenhum failure acima é reclassificado retroativamente.

## Sucessos finais antes do merge

### `34871401757` — SUCCESS permanente read-only intermediário

No head `e80c3abc974022cc3daec8533af4cf47ed09d801`, o workflow permanente concluiu integralmente com `success`:

- V08: **22/22 PASS**;
- regressões V01–V08: **405/405 PASS**;
- V00: **12/12 PASS**;
- validador: **APROVADO — 0 falhas, 0 avisos**;
- `V08_RUNTIME_EDIT=0`;
- escopo: **PASS**;
- `GITHUB_TOKEN`: `Contents: read`, `Metadata: read`;
- checkout com `persist-credentials: false`.

Naquele checkout, antes da última atualização documental, `repo (links)` era **1850**.

### `34872178809` — SUCCESS permanente read-only no head final

No head final `9af5615d79b02cbd86f5a6d084444c83f203ae03`, o gate V08 de push comprovou:

- V08: **22/22 PASS**;
- regressões V01–V08: **405/405 PASS**;
- V00: **12/12 PASS**;
- validador: **APROVADO — 0 falhas, 0 avisos**;
- helpers citados: **92**;
- Markdown/links: **217 / 1382**;
- identidade do repositório: **1350 arquivos**;
- links fora da raiz: **1849**;
- `V08_RUNTIME_EDIT=0`;
- escopo: **PASS**.

## Checks finais da PR #42

No mesmo head final `9af5615d79b02cbd86f5a6d084444c83f203ae03`, todos os checks disparados pela PR #42 concluíram com `success`:

- V00 — `34872182858`;
- V01 — `34872182762`;
- V02 — `34872182754`;
- V03 — `34872182780`;
- V04 — `34872182788`;
- V05 — `34872183073`;
- V06 — `34872182761`;
- CI geral — `34872182808`;
- V08 — `34872182789`.

## Aceite e merge

Rodrigo autorizou explicitamente a integração da V08. A PR #42 foi marcada como pronta e mesclada com proteção pelo head esperado `9af5615d79b02cbd86f5a6d084444c83f203ae03`.

O merge efetivo na `main` é `622d2c962a80998cf990b57036f7ae503bfc0458`. A árvore do merge é idêntica à árvore da candidata testada.

## Pós-merge na `main`

No merge `622d2c962a80998cf990b57036f7ae503bfc0458`, os dez workflows disparados por `push` concluíram com `success`:

- V00 — `34872703807`;
- V01 — `34872703784`;
- V02 — `34872703942`;
- V03 — `34872703701`;
- V04 — `34872703770`;
- V05 — `34872703955`;
- V06 — `34872703775`;
- V07 — `34872703931`;
- V08 — `34872703962`;
- CI geral — `34872703809`.

Não houve workflow pós-merge em failure, cancelado ou ainda em execução quando a bateria foi fechada.

## Revisão editorial do template EDA

A primeira versão pós-migração removeu corretamente a política visual paralela, mas reduziu demais o conteúdo do antigo guia. A revisão seguinte recuperou convenções úteis — escolha de gráficos, anotações, emojis, números, tabelas, KPI-line, hierarquia, narrativa de resultados, índice e section headers — sem reintroduzir hexadecimais, paleta própria, dicionário de tema ou CSS visual paralelo.

Fonte e simulado permanecem equivalentes nas superfícies cobertas pela V08.

## README raiz

O README raiz foi compactado para permanecer uma entrada operacional atual e direcionar o histórico detalhado ao índice de sprints, onde ele já é mantido de forma canônica. A compactação eliminou duplicação documental e mantém o bloco de métricas verificável pelo gate.

No head funcional integrado `9af5615d79b02cbd86f5a6d084444c83f203ae03`, `repo (links)` era **1849**. Após a reconciliação documental pós-merge, a medição real passou a **1850**, sem alteração de runtime.

## Estado encerrado

A V08 está integrada no Git. Este fechamento não publica o Hub no Databricks, não altera ACL/compute e não homologa browser, acessibilidade ou UAT.

A V09 não foi iniciada.

## O que PASS não prova

- seleção determinística de uma skill pela Genie Code;
- publicação/instalação no workspace;
- render real no browser Databricks;
- acessibilidade ou UAT humano;
- permissão/ACL real de pastas;
- que SHAP/Matplotlib ou Kaplan–Meier estejam tematizados;
- que documentação impeça tecnicamente um agente de ignorar orientação.
