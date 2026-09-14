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

A migração transitória abortou antes de commit porque o regex do Manual exigia um próximo heading `##`, mas o Sistema de Temas era a última seção do arquivo. Nenhuma integração transversal foi persistida por esse run. O regex foi corrigido para aceitar próximo heading **ou EOF**.

### `34866493021` — FAILURE transitório da primeira migração

A migração foi aplicada, mas a suíte V08 encontrou duas condições:

1. o template EDA ainda citava literalmente nomes da antiga política local ao dizer para não usá-los;
2. o teste de workflow read-only reprovou corretamente porque o próprio run de migração usava permissão de escrita temporária.

O mecanismo transitório foi removido pelo próprio commit de migração e o workflow permanente voltou a `contents: read`/`persist-credentials: false`.

### `34866578667` — FAILURE permanente por nomenclatura residual

Com o workflow já read-only, restou apenas a nomenclatura local residual do template EDA. A correção removeu inclusive esses identificadores textuais, mantendo a guarda estrita de “sem segunda fonte de tema”.

### `34866767026` — FAILURE documental

No head sincronizado após a correção textual:

- V08: **22/22 PASS**;
- regressões V01–V08: **405/405 PASS**;
- V00: **12/12 PASS**.

O bloqueio ficou restrito ao validador porque a saída colada do README raiz ainda refletia métricas anteriores.

### `34866944219` — FAILURE intermediário de espelho

Durante a revisão editorial do template EDA, a fonte foi atualizada em um commit e o espelho no commit imediatamente seguinte. O run disparado no commit intermediário reprovou corretamente `test_updated_assistant_surfaces_match_simulated_bytes`. Nenhum outro contrato foi utilizado para mascarar essa divergência.

### `34867002420` — FAILURE documental no head sincronizado

Depois de sincronizar o template revisado, passaram:

- V08: **22/22 PASS**;
- regressões V01–V08: **405/405 PASS**;
- V00: **12/12 PASS**.

A reprovação ficou somente na saída colada do README raiz. O validador mediu naquele checkout:

- helpers citados: **92**, contra 88 colados;
- Markdown/links: **217 arquivos / 1382 links**, contra 217/1383 colados;
- identidade do repositório: **1349 arquivos**, contra 1345 colados;
- links fora da raiz: **1850**, já coincidente.

Foram três falhas documentais e zero avisos. Esses valores ainda não eram finais porque checkpoint, índices e changelog da própria V08 ainda seriam estabilizados.

### `34867738695` — FAILURE de configuração do workflow transitório

A primeira tentativa de reconciliar índices/changelog por workflow foi recusada pelo GitHub antes de criar jobs. Nenhum arquivo de produto ou documentação foi alterado por esse run. A escrita foi redesenhada para usar um script transitório versionado e auto-removido.

### `34867935251` — FAILURE documental da medição final

Com checkpoint, índices vivos e changelog já estabilizados e workflow permanente novamente read-only, passaram:

- V08: **22/22 PASS**;
- regressões V01–V08: **405/405 PASS**;
- V00: **12/12 PASS**.

O validador apontou somente quatro divergências numéricas na saída colada do README raiz, com **0 avisos**. A medição final da candidata é:

- helpers citados: **92 caminhos**;
- Markdown/links: **217 arquivos / 1382 links relativos**;
- identidade do repositório: **1350 arquivos**;
- links fora da raiz: **1855**.

Esses são os valores usados na reconciliação final do README raiz. Nenhum failure acima é reclassificado retroativamente.

## Revisão editorial do template EDA

A primeira versão pós-migração removeu corretamente a política visual paralela, mas reduziu demais o conteúdo do antigo guia. A revisão seguinte recuperou convenções úteis — escolha de gráficos, anotações, emojis, números, tabelas, KPI-line, hierarquia, narrativa de resultados, índice e section headers — sem reintroduzir hexadecimais, paleta própria, dicionário de tema ou CSS visual paralelo.

Fonte e simulado voltaram a apontar para o mesmo conteúdo após a revisão.

## Estado de fechamento

A documentação final da sprint — checkpoint, índices vivos e changelog — foi concluída **antes** da medição final do README raiz. A próxima etapa é reconciliar exatamente os quatro números medidos no run `34867935251` e repetir o workflow V08 permanente no novo SHA.

O head final precisa comprovar:

- 22/22 testes V08;
- 405/405 regressões V01–V08;
- 12/12 V00;
- validador 0 falhas/0 avisos;
- `V08_RUNTIME_EDIT=0`;
- escopo verde.

Então o diff/base serão revisados e uma PR **draft** será aberta no SHA exato. A V08 não será mesclada sem aceite explícito de Rodrigo.

## O que PASS não prova

- seleção determinística de uma skill pela Genie Code;
- publicação/instalação no workspace;
- render real no browser Databricks;
- acessibilidade ou UAT humano;
- permissão/ACL real de pastas;
- que SHAP/Matplotlib ou Kaplan–Meier estejam tematizados;
- que documentação impeça tecnicamente um agente de ignorar orientação.
