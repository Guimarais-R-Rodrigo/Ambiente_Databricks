# V12 — testes, evidências e histórico de execução

## Regra de leitura

Este arquivo é o ledger de testes/evidências da V12. `PASS`, `FAIL`, `BLOQUEADO_AUTORIZACAO`, `SKIP` e `PENDENTE` são estados distintos. CI/local não prova Databricks; Databricks não prova UAT; percepção humana não substitui medição objetiva.

## Baseline reconciliado com a `main`

A `main` avançou durante a homologação para `28669f99db27cf23df73549297bbf57eda033f58` pela integração da frente de Skill Enforcement. A V12 foi reconciliada aditivamente pelo merge `fd8f5dfdd6354e10964feaa51d10ede746c8c970`, sem rebase/reset/force.

Esse head ficou `behind_by=0`, mergeável e com 7/7 workflows de PR em `success`:

- V00 `35026047301`;
- V02 `35026047191`;
- V01 `35026047195`;
- CI geral `35026047390`;
- V12 `35026047355`;
- V10 `35026047337`;
- V11 `35026047348`.

No V12 `35026047355`:

- `test_temas_v12.py`: 47/47 PASS;
- `test_temas_v12_evidencia_real.py`: 10/10 PASS;
- regressões V01–V12: 514/514 PASS;
- V00: 12/12 PASS;
- validador: `APROVADO: 0 falha(s), 0 aviso(s)`;
- `repo (identidade) = 1424`;
- `repo (links) = 1887`;
- `worktree (extras) = 0`;
- higiene = 17 caminhos integrais + 3 documentos compartilhados pelo diff;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`.

Este commit de fechamento acrescenta **um método permanente** para validar as evidências humanas reais e preservar o FAIL de `A11-01`. Por isso o resultado esperado é 11 testes no arquivo de evidência e 515 regressões acumuladas, mas essas contagens só podem ser chamadas de certificadas depois do CI do próprio head de fechamento.

## Evidência real AI/BI

### `V12-AIBI-01` tentativa #1 — FAIL preservado

A primeira tentativa comprovou tecnicamente import em draft, Light/Dark, invariância semântica, `published=false` e rollback, mas usou `samples.nyctaxi.trips`. O contrato exigia `synthetic_data_only=true`; por isso permaneceu FAIL.

### `V12-AIBI-01` tentativa #2 — PASS

A segunda tentativa substituiu temporariamente as duas queries por SQL `VALUES` sintético, sem criar tabela, schema, Volume ou arquivo.

Fatos principais:

- ambiente sanitizado: `databricks_free_lab`;
- dashboard draft: verdadeiro;
- `synthetic_data_only=true`;
- `published=false`;
- Light/Dark observado;
- template nativo revisado SHA-256 `3f381314d8f2c99733a1094601b65d6d59263bc7d7d090ac6d533cb89e438412`;
- assinatura semântica antes/depois `85c7477027f9f26586e757c753fd29e909aca0e56469be7adeaa595723ee238b`;
- rollback original/final `79582c3964612a1d7ca4570efbdb7a53ea8585d9ffdf6a45527abf4abf88f69d`;
- `approximated_automated=false`;
- `unsupported_automated=false`.

O hardening exige os hashes de rollback somente para PASS, preservando a tentativa histórica FAIL sem fabricar evidência retroativa.

## Evidência real `SEC-01`

`SEC-01 = PASS` como evidência `databricks_environment`.

- identidade autenticada observada no ambiente;
- permissão efetiva demonstrada pelas ações realmente concluídas na sessão sintética válida de AI/BI;
- `self_declared_role_used=false`;
- `identity_bytes_versioned=false`;
- nenhum nome, e-mail, workspace ID ou screenshot com PII é versionado.

A especialização V01 `human_required=true` → V12 `databricks_environment` está explicitamente ratificada e não afeta `DOC-02`, `DOC-03`, `A11-01` ou `UAT-01`.

## Evidência humana real — sessão `P-UAT-01`

Participante real autorizado; papel sanitizado `nontechnical_user`; identidade pessoal não versionada.

Foram entregues somente:

- `ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md`;
- `ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md`.

Versão observada: `89486948045e7222232f8d3aa4c602151f46c6c1`.

Artefato lógico sanitizado da sessão: SHA-256 `9277a8d9a12675dc4dcab8ca920531d10f65e230205df55059539bac91ac530e`.

### `DOC-02 = PASS`

- participante autorizado: verdadeiro;
- próxima ação identificada sem ajuda: verdadeiro;
- tempo observado: 25 segundos;
- `help_events=[]`;
- a referência de 60 s permanece candidata/exploratória e não SLA inventado;
- `oracle_met=true`.

### `DOC-03 = PASS`

- participante autorizado: verdadeiro;
- distinguiu corretamente prévia, salvar, submeter, aprovar, publicar e recuperar sessão;
- não confundiu salvar com publicar;
- não prometeu persistência além do descrito;
- `help_events=[]`;
- `oracle_met=true`.

### `UAT-01 = PASS`

- participante autorizado: verdadeiro;
- duração observada: 360 segundos;
- `help_events=[]`;
- escolheu/explicou ponto de partida, ajuste, aplicação/comparação, desfazer e salvar;
- explicou corretamente quem é afetado pela alteração;
- `journey_completed=true`;
- `shared_change_absent=true`;
- `journey_mode=textual_v01`;
- `oracle_met=true`.

Esse PASS é a rota textual prevista pela V01. Não prova o frontend real do Visual Lab e não substitui `V12-LAB-01`.

## `A11-01` — FAIL real preservado

Participante autorizado sanitizado como `P-MAINT-01`; autorização específica `AUTH-V12-A11-01-20260915-PR54`.

A sessão usou o mesmo dashboard draft descartável com dados temporariamente sintéticos, sem Publish, e depois restaurou tema/queries originais.

Revisão humana:

- Light 100%: observada;
- Dark 100%: observada;
- foco/teclado: sem irregularidade percebida;
- keyboard trap: não observado;
- zoom 200% Light/Dark: sem irregularidade percebida;
- dependência exclusiva de cor: não relatada;
- rótulos/ícones: sem irregularidade percebida.

A percepção humana não foi usada para sobrescrever a medição objetiva. A formatação condicional explícita do dashboard possui regras em `Total Revenue` que foram efetivamente exercitadas pela massa sintética:

| Par observado | Ratio | Exigido | Resultado |
|---|---:|---:|---|
| `#9C2638` sobre `#E8F4FD` (Light) | 6.837793163467097 | 4.5 | PASS |
| `#9C2638` sobre `#11171C` (Dark) | 2.3624715346329377 | 4.5 | **FAIL** |
| `#FFD465` sobre `#E8F4FD` (Light) | 1.264684095079348 | 4.5 | **FAIL** |
| `#FFD465` sobre `#11171C` (Dark) | 12.773222792356847 | 4.5 | PASS |

Nenhum texto foi classificado como texto grande. Portanto `A11-01 = FAIL`, `oracle_met=false`.

Hashes sanitizados da sessão:

- tema pós-import `1c136fa9218c49754caa849883a13cefb51a913ad5df7d47e773a5ea65085802`;
- screenshot Light `108cd1e5f2f9863aa9f190bcef2eca24a451a73e961d22e2104c2f7c016590e8`;
- screenshot Dark `717bb77127af33581303b7a1eeca715115087f9b9236084138dfd5975af2929a`;
- tema final restaurado `71c8038d5b68b35ff888ea6bb7406dcfc74d5d1798b0af71626e592a2a50091b`;
- dashboard final restaurado `0ba3a8399728de7776c0c80ce505123e2553c44d864d47bd49283d8b0c000308`.

O rollback foi confirmado. A única divergência frente ao export restaurado anterior foi newline final em uma query, sem diferença lógica de SQL, layout, widgets ou tema.

A issue #57 preserva o achado. As cores problemáticas pertencem a `cellFormat` do dashboard, não aos três bindings diretos da V11; nenhuma ampliação silenciosa foi feita.

## Estados ambientais encerrados por bloqueio explícito

### `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`

A matriz classifica a jornada como mutação real. Não existe autorização específica para essa mutação e o pré-requisito de Visual Lab real já disponível em ambiente autorizado não foi estabelecido. Nenhuma operação foi executada para “fazer passar”.

### `V12-APP-01 = BLOQUEADO_AUTORIZACAO`

O App real exigiria deploy de teste. Deploy não foi autorizado. Nenhuma ACL, grupo, Volume ou App foi criado/alterado.

### `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`

Workspace theme/admin/snapshot/reaplicação exigem autorização administrativa específica. `Publish`, se necessário em subteste, é outro gate e também não foi autorizado. Nenhuma dessas operações ocorreu.

## História de failures preservada

Nenhum failure anterior foi reclassificado:

- `34908962030`: métricas stale do README;
- `34909482529` e `34909599988`: fetch redundante incompatível com checkout sem credencial persistida;
- `34909800421`: regex Shell detectou seus próprios literais;
- `34910134591`: autoinspeção Python ainda reconstruía literal proibido;
- `79083b...`, `0b5318...`, `efb1b...`, `07a6dd...`: failures documentais de métricas durante incorporação das evidências;
- commit `468eb637...`: README temporariamente substituído por placeholder; reparo aditivo `4823f3ab...`, sem reset/force;
- workflow V12 `34986472469`: failure de métrica 1423 vs 1422, depois reconciliado;
- `10785088...`: hardening parcial sem a suíte atualizada; V12/V10/V11/CI falharam legitimamente; reparo aditivo `26f84d...`;
- `A11-01`: FAIL real de contraste, issue #57.

`SKIP` também não é reclassificado: a etapa condicional do V00 permanece SKIP quando sua condição não se aplica.

## Testes negativos permanentes

A V12 continua recusando, entre outros:

- PASS sem artefato;
- oráculo não satisfeito;
- participante não autorizado;
- duração humana inventada;
- mutação sem autorização/rollback;
- dado não sintético onde sintético é requisito;
- export stale;
- drift semântico;
- fixture V11 usado como entrada Databricks;
- automação de `approximated`/`unsupported`;
- publicação acidental;
- workspace theme/publicação sem autorização própria;
- papel autodeclarado como autorização;
- bytes de identidade versionados;
- rollback divergente;
- credencial/identificador/path sensível em qualquer conteúdo novo permitido pela V12.

## Gate de fechamento

Todos os casos V12 têm estado explícito. O commit que consolida este ledger e o novo teste humano precisa ter CI próprio. Somente depois desse verde a candidata pode ser apresentada ao usuário para aceite de integração.

Mesmo com CI verde, o aceite deve ser informado sobre dois fatos não negociáveis:

1. `A11-01` permanece **FAIL** rastreado na issue #57;
2. `V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` permanecem **BLOQUEADO_AUTORIZACAO**.

V13 não deve começar antes da decisão de aceite, merge da PR #54 e auditoria pós-merge.
