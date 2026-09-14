# Checkpoint V10 — Databricks App de gestão visual

## Estado

**CANDIDATA TECNICAMENTE VERDE NA BRANCH; SEM ACEITE, MERGE OU DEPLOY DATABRICKS.**

Base: `d6655411ca4ac1834b0983f6ce6bdadc30b831bb`.

Branch: `codex/temas-v10-databricks-app-20260914`.

Head técnico com gate completo verde antes do registro final de evidências: `c114cddedd7775cecb1cf8b672ad33e4a9f5365f`.

Run integralmente verde nesse head: `34886828579`.

## Escopo recuperado

V10 é a frente de Databricks App de gestão visual. V11 permanece reservada para AI/BI. O App reutiliza os contratos e o Visual Lab já integrados e deve ter identidade, papéis, persistência, retenção, custos e deploy/rollback explicitamente definidos.

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

## Arquivos principais da candidata

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

### Run `34886828579` — SUCCESS

No head `c114cddedd7775cecb1cf8b672ad33e4a9f5365f`:

- V10 específica: **19/19 PASS**;
- sintaxe Streamlit compilada em memória: **PASS**;
- regressões V01–V10: **436/436 PASS**;
- V00: **12/12 PASS**;
- bundle: **247 arquivos + `V10_APP_MANIFEST.json`**;
- verificação de inventário, tamanho e SHA-256 do bundle: **PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- escopo V10: **PASS**, sem deploy/aprovação/promoção/ativação/publicação.

## Gates antes de pedir aceite

1. suíte V10 verde — **FECHADO**;
2. regressões V01–V10 verdes — **FECHADO**;
3. V00 verde — **FECHADO**;
4. bundle V10 criado e verificado — **FECHADO**;
5. source/simulado equivalentes — **FECHADO**;
6. validador 0 falhas / 0 avisos — **FECHADO**;
7. PR mergeável e checks reais verdes — **PENDENTE DA PR**;
8. diff sem temporários e sem credenciais — **FECHADO NA AUDITORIA PRÉ-PR**;
9. documentação com resultados reais e failures preservados — **FECHADO NA BRANCH; A REVALIDAR NO HEAD DOCUMENTAL FINAL**.

A comparação pré-PR mostrou a candidata à frente da base, sem commits atrás, e alterações restritas ao App V10, seu espelho, tooling/testes/CI e documentação. Não entram schema, tokens, paleta ou adaptadores visuais existentes.

## Pendências que não bloqueiam a candidata Git, mas bloqueiam homologação operacional

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

Reexecutar o workflow no head documental final. Se continuar integralmente verde, abrir a PR V10 em **draft**, auditar mergeability e todos os checks realmente disparados. A PR pode ser apresentada como candidata pronta para aceite, mas o merge continua dependente de aceite explícito de Rodrigo. V11 não deve ser iniciada.
