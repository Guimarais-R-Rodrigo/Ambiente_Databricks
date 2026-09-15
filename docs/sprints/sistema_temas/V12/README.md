# V12 — homologação de jornadas com pessoas e ambiente

## Estado

**V12 em andamento. Camada Git/local validada; `V12-AIBI-01` e `SEC-01` homologados em ambiente Databricks real; demais jornadas continuam pendentes ou bloqueadas.**

A V12 parte da `main` `d106ef3158e5827a2eec3aa183dbb3b47885c960`, onde V00–V11 estão integradas. Ela não cria um novo engine de temas e não reabre a arquitetura V11: organiza e instrumenta a etapa canônica em que gaps deliberadamente deixados como “não homologados” passam a ser jornadas observáveis de **pessoa + ambiente**.

CI não vira UAT, um `PASS` de ambiente não prova compreensão humana e uma homologação formativa não significa prontidão de produção.

## Fonte canônica recuperada

A V01 determina que **“V12 testa jornadas com pessoas; V13/V14 consolidam operação e suporte”**. A matriz V01 mantém cinco cenários humanos/ambientais originalmente pendentes: `DOC-02`, `DOC-03`, `A11-01`, `SEC-01` e `UAT-01`. Nesta execução, `SEC-01` atingiu seu oráculo ambiental; os quatro casos restantes continuam sem PASS suficiente. V05, V10 e V11 acumulam pré-requisitos de ambiente para superfícies reais.

O repositório não fixa tamanho estatístico para a amostra formativa. Portanto a V12 registra cada sessão executada e não inventa `n`, representatividade ou SLA. A meta de 60 segundos de `DOC-02` e qualquer medição exploratória permanecem medições candidatas até decisão explícita.

## O que é

A V12 acrescenta uma camada de **protocolo e evidência**, não uma nova camada de tema:

- matriz canônica de casos e fronteiras;
- protocolo para ambiente Databricks e para UAT;
- validador local `tools/temas_v12_homologacao.py`;
- testes negativos para impedir falso `PASS`;
- workflow GitHub Actions read-only;
- registros de ambiente/humano somente quando realmente executados;
- evidências sanitizadas e verificáveis para jornadas reais autorizadas.

## Estado das classes de evidência

### Git/local

O head `ad4a66f65ae390f2e98576dffac83635963ecab6` é o baseline verde após a incorporação de `SEC-01`. Os sete workflows reais da PR concluíram em `success`. No workflow V12 `34987044468` foram comprovados:

- V12 específica: **26/26 PASS**;
- teste dedicado das evidências reais AI/BI + SEC-01: **2/2 PASS**;
- regressões V01–V12: **485/485 PASS**;
- V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**;
- métricas medidas: **1423 arquivos / 1887 links**;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`.

No workflow V00, a etapa condicional `Gate da branch isolada sem depender da integração com main` permaneceu `SKIP`; esse estado não é promovido a PASS. O warning de Node 20 pertence à plataforma GitHub Actions e não é warning do validador do projeto.

### Databricks environment — `V12-AIBI-01`

`V12-AIBI-01` possui **PASS real de ambiente** em dashboard AI/BI descartável em estado draft, no Databricks Free Edition, com dados sintéticos gerados somente por SQL `VALUES` e sem `Publish`.

A evidência fica em `docs/sprints/sistema_temas/V12/evidencias/V12-AIBI-01/`.

A cadeia observada foi:

1. export nativo real e descoberta fail-closed dos campos existentes;
2. template real fixado por SHA-256 `3f381314d8f2c99733a1094601b65d6d59263bc7d7d090ac6d533cb89e438412`;
3. binding revisado somente para os três mapeamentos `translated/direct` da V11:
   - `widget.background` → `/widgetBackgroundColor/light`;
   - `widget.corner_radius` → `/widgetCornerRadius`;
   - `visualization.categorical_palette` → `/visualizationColors`;
4. substituição temporária das duas queries por `VALUES` inline sintéticos, sem criar tabela, schema, Volume ou arquivo;
5. `Import theme` no dashboard draft;
6. observação real em Light e Dark;
7. preservação estrutural de `datasets` e `pages` antes/depois do import;
8. assinatura semântica sintética idêntica antes/depois: `85c7477027f9f26586e757c753fd29e909aca0e56469be7adeaa595723ee238b`;
9. `published=false`;
10. rollback integral de tema e queries, com assinatura normalizada original/final restaurada `79582c3964612a1d7ca4570efbdb7a53ea8585d9ffdf6a45527abf4abf88f69d`.

A primeira tentativa real permanece **FAIL**. Ela havia comprovado tecnicamente import, Light/Dark, invariância semântica e rollback, mas usou `samples.nyctaxi.trips`, que é dado público de amostra e não dado sintético. Como a matriz exige `synthetic_data_only=true`, a execução foi reprovada fail-closed e não foi reclassificada depois.

As autorizações operacionais registradas foram:

- `AUTH-V12-AIBI-01-20260915-PR54` — import de tema somente em dashboard draft descartável, sem `Publish`;
- `AUTH-V12-AIBI-01-TEMP-CUSTOM-20260915-PR54` — customização temporária para descobrir JSON Pointers reais e posterior rollback;
- `AUTH-V12-AIBI-01-SYNTH-VALUES-20260915-PR54` — substituição temporária das duas queries por `VALUES` sintéticos e restauração integral.

Essas autorizações **não** abrangem workspace theme, ACL, deploy do App ou publicação.

### Databricks environment — `SEC-01`

`SEC-01` possui **PASS real de ambiente** como jornada observacional, sem nova mutação. O oráculo exige identidade e permissões efetivas observadas, sem aceitar valor autodeclarado como autorização.

A evidência sanitizada registra somente fatos booleanos e hashes. A identidade autenticada e o workspace foram observados no menu de conta do mesmo Databricks Free Edition usado pela tentativa sintética válida de `V12-AIBI-01`; nome, e-mail, identificador de workspace e bytes da captura não foram versionados.

A permissão efetiva foi comprovada comportamentalmente pelas ações concluídas na mesma sessão sintética: edição temporária das queries e `Import theme` em dashboard draft. O registro não inventa rótulo de papel como “Admin” ou “Editor” e não usa papel autodeclarado. O próprio `SEC-01` não executou mutação adicional.

O arquivo versionado é `docs/sprints/sistema_temas/V12/evidencias/SEC-01/SEC-01_attempt-01.json`. O teste permanente confirma `identity_checked=true`, `permission_checked=true`, `synthetic_data_only=true`, ausência de e-mail/identificador sensível no JSON e aceitação pelo mesmo validador fail-closed da V12.

### Human/UAT e demais superfícies

Continuam sem `PASS` real:

- `DOC-02`;
- `DOC-03`;
- `A11-01` completo;
- `UAT-01`;
- `V12-LAB-01` — Visual Lab completo em browser/runtime real;
- `V12-APP-01` — App V10 real; deploy continua não autorizado;
- `V12-AIBI-02` — workspace theme, herança, snapshot e reaplicação; alteração de workspace theme continua não autorizada.

Nenhum deles é promovido pelos PASS ambientais de `V12-AIBI-01` e `SEC-01`.

## Quando usar

Use a V12 quando a pergunta depender de algo que teste local ou CI não consegue provar sozinho. Exemplos: uma pessoa consegue completar o primeiro uso sem ajuda verbal; a renderização final é legível no browser; identidade/permissão efetivas são as esperadas; um dashboard draft preserva queries, filtros, datasets e semântica após operação autorizada; ou uma configuração real produz o comportamento previsto.

Também use o protocolo para registrar corretamente um bloqueio. Falta de permissão, ambiente, participante, rollback ou autorização é resultado operacional válido e deve ficar como `PENDENTE` ou `BLOQUEADO_*`, nunca como `PASS` presumido.

## Quando não usar

Não use a V12 para:

- alterar tokens, paletas ou arquitetura só para facilitar homologação;
- substituir testes unitários, regressões ou CI por avaliação humana;
- tratar revisão do autor como UAT independente;
- usar fixture sintético V11 como se fosse artefato nativo Databricks;
- automatizar capacidades classificadas como `approximated` ou `unsupported`;
- transformar importação/configuração em autorização de publicação;
- declarar produção pronta apenas porque uma jornada funcionou uma vez em ambiente controlado.

## Pré-requisitos

Antes de qualquer sessão:

1. confirme o caso da matriz e o oráculo;
2. identifique uma classe sanitizada de ambiente autorizado;
3. confirme a classificação permitida dos dados;
4. defina participante/papel quando houver evidência humana;
5. fixe artefatos e hashes necessários;
6. planeje evidência sem credenciais, segredos ou PII;
7. defina rollback/saída segura para qualquer mutação;
8. obtenha autorização explícita adicional antes da primeira mutação real.

Sem esses itens, não avance.

## Passo a passo operacional

1. Localize o caso em `matriz_homologacao.json` e leia seu oráculo.
2. Execute primeiro os gates Git/local. Falha local bloqueia promoção da candidata.
3. Classifique a evidência como Git/local, Databricks environment ou Human/UAT.
4. Para observação somente leitura, registre ambiente, versão, browser/runtime e artefatos pertinentes.
5. Para mutação, registre operação, ambiente, risco, rollback, evidência esperada e referência da autorização.
6. Execute exatamente a jornada de `PROTOCOLO_HOMOLOGACAO.md`, sem ampliar escopo durante a sessão.
7. Preserve artefatos/hashes e fatos observados.
8. Valide o registro com `tools/temas_v12_homologacao.py`.
9. Marque `PASS` apenas quando o oráculo estiver satisfeito pela classe correta de evidência.
10. Em erro/ambiguidade, interrompa e registre o estado real.

## Resultado esperado e como saber se funcionou

| Classe | Sinal de sucesso | O que continua não provado |
|---|---|---|
| Git/local | suíte, regressões, V00, validador e gate de escopo/higiene verdes no mesmo head | comportamento real Databricks e compreensão humana |
| Databricks environment | jornada realmente observada, com autorização quando aplicável, artefatos, rollback quando aplicável e oráculo satisfeitos | UAT, representatividade e produção |
| Human/UAT | participante autorizado executa a jornada e satisfaz o oráculo | autorização administrativa, deploy, produção ou generalização estatística |

“Revisado”, “testado”, “homologado em ambiente”, “UAT aprovado”, “acessibilidade avaliada”, “pronto para produção” e “publicado” não são sinônimos.

## Erros comuns

Interrompa ou invalide a homologação diante de:

- CI usado como evidência de UAT;
- duração estimada tratada como observada;
- participante não autorizado;
- export AI/BI diferente daquele cujo SHA foi revisado;
- JSON Pointer/campo nativo inventado;
- alteração inesperada de query, filtro, dataset ou semântica durante a jornada;
- automação de `approximated`/`unsupported`;
- publicação acidental;
- snapshot tratado como vínculo vivo;
- dado que não atende à classificação exigida pelo caso;
- ausência de rollback ou autorização específica quando aplicáveis.

A tentativa AI/BI #1 é exemplo deliberadamente preservado de fail-closed por classificação inadequada dos dados.

## O que é automatizado e o que depende de humano

A automação V12 verifica formato/coerência de evidências, hashes, contratos V11, cenários negativos, regressões e ausência de ação remota no CI. O teste `tools/tests/test_temas_v12_evidencia_real.py` garante que a tentativa AI/BI #1 continue `FAIL`, a tentativa #2 continue validável como `PASS`, as queries sintéticas permaneçam `VALUES` sem criação de objetos ou referência à amostra NYC Taxi e o registro `SEC-01` permaneça sanitizado e validável.

Essa automação **não reproduz** o workspace nem substitui as observações reais que geraram os registros.

## Escopo V12

A V12 cobre:

1. documentação/primeiro uso (`DOC-02`, `DOC-03`);
2. render final e acessibilidade (`A11-01`);
3. identidade/permissões efetivas (`SEC-01`, agora com PASS ambiental);
4. primeiro uso sem ajuda verbal (`UAT-01`);
5. Visual Lab real quando houver ambiente autorizado;
6. App V10 real quando houver deploy de teste explicitamente autorizado;
7. AI/BI V11 em dashboard draft real (`V12-AIBI-01`, com PASS ambiental);
8. workspace theme/snapshot/reaplicação somente em workspace de teste e com autorização administrativa específica.

Operação recorrente, suporte, custos/retention operacionais e readiness de produção ficam para V13/V14 ou gates posteriores.

## O que não está autorizado

As autorizações já exercidas em `V12-AIBI-01` não autorizam:

- deploy de Databricks App;
- mudança de workspace theme;
- ACL/grupos;
- `Publish` de dashboard;
- compute/recurso adicional pago;
- uso de dados corporativos/reais para fabricar evidência;
- qualquer mutação fora do roteiro explicitamente autorizado.

`SEC-01` foi observacional e não amplia nenhuma autorização.

## Gates Git/local

Execute:

```bash
python -B tools/tests/test_temas_v12.py -v
python -B tools/tests/test_temas_v12_evidencia_real.py -v
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/validate_assistant.py --conferir-readme
```

Para critérios e classificação use `ESCOPO_E_ACEITE.md`.

## Saída segura e rollback

Se faltar autorização, ambiente, identidade, rollback, evidência ou pessoa apropriada, registre `BLOQUEADO_*` ou `PENDENTE` e encerre a sessão sem fabricar resultado.

Se uma mutação autorizada já ocorreu e o oráculo falhou, execute somente o rollback registrado antes da operação. Se o rollback não puder ser confirmado, interrompa novas ações e registre o estado como bloqueado até revisão humana.

## Próximo gate

O fechamento de `SEC-01` **não fecha a V12**. Permanecem as jornadas humanas e ambientais listadas acima; qualquer nova mutação exige seu próprio gate de autorização. V13 permanece bloqueada.
