# Checkpoint V10 — Databricks App de gestão visual

## Estado

**V10 ACEITA E INTEGRADA NO GIT; FECHAMENTO DOCUMENTAL PÓS-MERGE EM CURSO; SEM DEPLOY DATABRICKS.**

Base de início: `d6655411ca4ac1834b0983f6ce6bdadc30b831bb`.

Branch funcional: `codex/temas-v10-databricks-app-20260914`.

Head reconciliado aceito: `cb942ee955ff9236f19099e5ed4ceee9beb32000`.

PR funcional: #48.

Merge funcional na `main`: `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`.

Rodrigo deu aceite explícito em 14/09/2026. O aceite cobriu a integração Git da V10 e não autorizou deploy Databricks.

## Escopo recuperado

V10 é a frente de Databricks App de gestão visual. V11 permanece reservada para AI/BI. O App reutiliza os contratos e o Visual Lab já integrados e mantém identidade, papéis, persistência, retenção, custos e deploy/rollback explicitamente definidos.

## Decisões

- nenhum novo schema de tema;
- nenhum novo token/paleta;
- `context="app"` continua não implementado como contexto temático;
- o App gerencia temas `notebook` existentes;
- identidade vem do proxy Databricks, nunca do JSON de tema;
- persistência usa UC Volume via recurso `theme_storage`;
- namespace de usuário usa SHA-256 do identificador em memória;
- path produtivo precisa seguir `/Volumes/<catalog>/<schema>/<volume>` e traversal/symlink são recusados;
- política de retenção: sem delete automático/usuário e sem reescrita de histórico;
- aprovação/publicação/promoção ausentes do código;
- bundle de deploy é derivado em `.artifacts/`, nunca fonte editável paralela;
- CI é local/read-only e não recebe credenciais Databricks.

## Arquivos principais integrados

- `ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/app.py`;
- `.../app_service.py`;
- `.../app.yaml`;
- `.../requirements.txt`;
- `.../README.md`;
- `.../GUIA_PRIMEIRO_USO.md`;
- `.../DEPLOY_ROLLBACK.md`;
- espelho equivalente em `Novo_Ambiente_Simulado`;
- `tools/temas_v10_app.py`;
- `tools/tests/test_temas_v10.py`;
- `.github/workflows/temas-v10-ci.yml`;
- documentação V10 e matriz de papéis.

## Evidências obtidas

### Run `34884790130` — FAILURE preservado

A suíte V10 passou, mas o cumulativo terminou **433/434** porque a etapa `py_compile` do próprio runner gerou dois `.pyc` transitórios apenas na árvore fonte. A correção passou a validar sintaxe em memória e a equivalência ignora somente caches não versionados. Não houve divergência versionada de produto.

### Run `34885407907` — FAILURE preservado

No head `0ddcdd6b92372186c130d226c4b72d141cb7d67e` passaram V10 **19/19**, regressões V01–V10 **436/436**, V00 **12/12**, bundle **247 arquivos + manifesto** e a verificação de hashes/tamanhos. O validador reprovou com **7 falhas / 0 avisos** por métricas antigas no README raiz e um link relativo inválido no README espelhado do App. O run permanece FAILURE.

### Run `34886250755` — FAILURE preservado

No head `88cfea4d5cf29991c5bad23b61a3bec97feb2978`, todos os gates funcionais continuaram verdes, mas o validador encontrou **4 falhas / 0 avisos** porque quatro métricas do README raiz ainda estavam stale. A medição real foi 220 Markdown / 1394 links relativos, 219 arquivos Python AST, 1373 arquivos na identidade do repo e 1869 links fora da raiz. O README foi reconciliado com esses números sem alteração do validador. O run permanece FAILURE.

### Primeiras evidências integralmente verdes

O run `34886828579`, no head `c114cddedd7775cecb1cf8b672ad33e4a9f5365f`, confirmou V10 **19/19**, regressões V01–V10 **436/436**, V00 **12/12**, bundle **247 arquivos + `V10_APP_MANIFEST.json`**, verificação de inventário/tamanho/SHA-256, validador **0 falhas / 0 avisos** e escopo sem deploy/aprovação/promoção/ativação/publicação.

O push final original `34887162337`, no head `8e59739cbe3e1ce6d49503e7c953c82a98d2dc2c`, repetiu o gate completo com **SUCCESS**.

### Reconciliação com a MM00 e checks reais da PR #48

A `main` avançou com a MM00 enquanto a V10 aguardava integração. A candidata foi reconciliada sem alterar o produto V10; o head aceito passou a ser `cb942ee955ff9236f19099e5ed4ceee9beb32000`.

Nesse head, dez workflows reais de `pull_request` concluíram com `success`:

- `34894892652` — Contrato de temas V01;
- `34894892747` — Adaptador Plotly V03;
- `34894892632` — Assets e geração V06;
- `34894892622` — Databricks App de gestão visual V10;
- `34894892726` — Regressões da instrumentação V00;
- `34894892777` — CI local reproduzível;
- `34894892631` — Componentes HTML e tabelas V04;
- `34894892738` — Visual Lab notebook V05;
- `34894892661` — Núcleo de temas V02;
- `34894892620` — Integração transversal V08.

Os failures iniciais de PR que terminaram antes da alocação do runner continuam históricos e não foram reclassificados.

### Integração e pós-merge

O PR #48 foi integrado no commit `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b` após o aceite explícito. No pós-merge, **12/12 workflows disparados por `push` na `main` concluíram com `success`**; o workflow específico V10 é o run `34896944061`. Não houve failure pós-merge nesse commit.

## Gates de fechamento Git

1. suíte V10 verde — **FECHADO**;
2. regressões V01–V10 verdes — **FECHADO**;
3. V00 verde — **FECHADO**;
4. bundle V10 criado e verificado — **FECHADO**;
5. source/simulado equivalentes — **FECHADO**;
6. validador 0 falhas / 0 avisos — **FECHADO**;
7. PR mergeável e checks reais verdes — **FECHADO**;
8. diff sem temporários e sem credenciais — **FECHADO**;
9. aceite explícito — **FECHADO**;
10. merge funcional — **FECHADO**;
11. workflows pós-merge — **FECHADO, 12/12 SUCCESS**;
12. reconciliação documental viva — **EM FECHAMENTO NESTA ETAPA DOCUMENTAL**.

## Pendências que não bloqueiam o fechamento Git, mas bloqueiam homologação operacional

- deploy autorizado de Databricks App;
- associação real do UC Volume;
- permissões/grupos reais;
- teste de headers reais;
- teste multiusuário no workspace;
- browser/acessibilidade;
- UAT V12;
- custo observado;
- procedimento de deploy/rollback executado no destino.

## Próximo passo

Integrar esta reconciliação exclusivamente documental após os gates da própria PR. Depois disso, a V10 fica fechada no Git. V11/AI-BI permanece uma sprint separada e não é iniciada por este fechamento.