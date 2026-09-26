# Checkpoint V09 — kit de instalação/transição

## Estado

**ACEITA E INTEGRADA NO GIT; SEM PUBLICAÇÃO DATABRICKS.**

Aceite explícito: Rodrigo, 14/09/2026 — “voce tem meu aceite”.

Entrega funcional:

- PR #45 — `V09 — integrar Sistema de Temas ao kit de transição`;
- head validado: `3b69dd25fd4af434fda414496c2ca3d80fd78a8e`;
- merge real na `main`: `0f7234c4734f1974ebb1a20123f3c26626c67ef3`;
- `merged_at`: `2026-09-14T18:24:36Z`;
- árvore candidata = árvore do merge: `26689420a2c0693c0ff0c08f625e80babb2180a8`.

Correção pós-merge:

- PR #46 — `V09 — corrigir preparação Node do workflow operacional`;
- head validado: `d1c67f06d96b929a58961c50fc31c06ca7c0cfe2`;
- merge real na `main`: `4ae714a35a0aafd930a8cd796d962b0a79449b88`;
- `merged_at`: `2026-09-14T18:32:29Z`;
- árvore candidata corretiva = árvore do merge: `32de1224093407d6fc91e08842c6f5ef3d0f456a`.

O SHA `4ae714a35a0aafd930a8cd796d962b0a79449b88` é a referência técnica final da V09 antes deste fechamento exclusivamente documental.

## Achado de entrada

O kit existente já empacotava a árvore sanitizada completa e protegia FILEs por SHA256. A integração do Sistema de Temas, contudo, era implícita: o manifesto não nomeava um subconjunto temático obrigatório e o bundle não tinha uma guarda específica contra perda desse contrato.

## Decisão V09

Adicionar uma guarda offline de inventário e um bloco declarativo `theme_contract` ao manifesto v2, preservando todo o fluxo de aceite existente.

O contrato distingue explicitamente:

- **transportar:** obrigatório e protegido por hash;
- **ativar:** somente opt-in/manual;
- **publicar:** não realizado pela V09.

## Implementação integrada

- `tools/temas_v09_transicao.py`: contrato, validação fail-closed do inventário e verificação pós-build do ZIP;
- `tools/bundle_implantacao.py`: valida o contrato antes de criar o ZIP e grava `theme_contract` no manifesto;
- `tools/tests/test_temas_v09.py`: mutantes negativos, invariantes, verificação dos bytes do ZIP e guarda da preparação Node do workflow operacional;
- `docs/playbooks/checklist-replicacao.md`: instrução operacional para usuário não técnico;
- `.github/workflows/temas-v09-ci.yml`: gate permanente read-only, incluindo reabertura do ZIP gerado;
- `.github/workflows/kit-transicao-trabalho.yml`: gate V09, Spark local, preparação do compositor V06 e verificação do ZIP antes de `upload-artifact`.

## Limite arquitetural deliberado

O núcleo `tools/aceite_trabalho.py` continua genérico. Ele é embutido no notebook offline e não deve importar outro módulo de `tools/`, que não é levado ao destino. Duplicar nele os nove caminhos temáticos criaria uma segunda fonte de verdade.

Por isso, a cadeia de confiança V09 é:

1. contrato canônico antes do build;
2. validação dos bytes efetivamente colocados no ZIP depois do build;
3. manifesto fixado pelo hash que o notebook já recebe;
4. conferência SHA256 de todos os FILEs pelo aceite no staging/final;
5. conferência humana explícita do `theme_contract` pelo checklist.

## Failures históricos preservados

Os três runs abaixo permanecem **FAILURE**. Nenhum foi reclassificado como success.

### `34877035267` — FAILURE

Head `17a95762b9f6dc19c13cf008ee581bc7c1041d26`.

- 7/8 testes V09 passaram;
- único erro: `test_transition_checklist_names_theme_contract`;
- causa: o checklist usava corretamente `manual_opt_in`, mas o teste procurava `manual/opt-in`;
- ação correta: corrigir o oráculo textual, sem relaxar a implementação.

### `34877297808` — FAILURE

Head `b7d16ab6eccf59a266353dc74502cf51703ad8c3`.

- V09: 8/8 PASS;
- kit: 43 testes, 36 PASS + 7 SKIP explícitos por Spark local desabilitado nessa chamada;
- V01–V09: 413/413 PASS;
- V00: 12/12 PASS;
- kit real: 535 arquivos + `MANIFEST.json`;
- bloqueio: `validate_assistant.py --conferir-readme` encontrou `1350` no README contra `1355` arquivos medidos;
- resultado do validador: 1 falha / 0 avisos.

### `34880619346` — FAILURE pós-merge do PR #45

Merge funcional `0f7234c4734f1974ebb1a20123f3c26626c67ef3`.

- 12 workflows foram disparados pelo push;
- 11 terminaram `success`;
- `Kit de transição para o trabalho` falhou no primeiro gate local antes de V09, Spark, geração do kit e upload;
- causa real: o runner não instalava previamente as dependências Node do compositor V06 antes de `python tools/ci_local.py --verbose`;
- as etapas seguintes ficaram corretamente `skipped`;
- correção: PR #46 adicionou Node 22, `pnpm@10.34.5`, instalação com `--frozen-lockfile` e teste de regressão de ordenação.

Esse run permanece **FAILURE** e constitui evidência da causa que motivou a correção.

## Validação da correção — PR #46

No head `d1c67f06d96b929a58961c50fc31c06ca7c0cfe2`, os cinco checks realmente disparados pela PR concluíram com `success`:

- Regressões da instrumentação V00 — run `34881120187`;
- Contrato de temas V01 — run `34881120270`;
- Núcleo de temas V02 — run `34881120196`;
- CI local reproduzível — run `34881120184`;
- Kit de transição e temas V09 — run `34881120261`.

O diff corretivo tinha somente dois arquivos: `.github/workflows/kit-transicao-trabalho.yml` e `tools/tests/test_temas_v09.py`.

## Pós-merge final — workflows realmente disparados

No push da `main` no SHA `4ae714a35a0aafd930a8cd796d962b0a79449b88`, foram disparados exatamente **12 workflows**. Todos concluíram com `success`:

| Workflow | Run ID | Conclusão |
|---|---:|---|
| Regressões da instrumentação V00 | `34881426341` | success |
| Contrato de temas V01 | `34881426372` | success |
| Núcleo de temas V02 | `34881426402` | success |
| Adaptador Plotly V03 | `34881426334` | success |
| Componentes HTML e tabelas V04 | `34881426326` | success |
| Visual Lab notebook V05 | `34881426353` | success |
| Assets e geração V06 | `34881426337` | success |
| Consumidores e formatos V07 | `34881426400` | success |
| Integração transversal V08 | `34881426331` | success |
| Kit de transição e temas V09 | `34881426379` | success |
| CI local reproduzível | `34881426388` | success |
| Kit de transição para o trabalho | `34881426374` | success |

Não são contados aqui workflows que não foram disparados por esse `push`.

## Gate operacional final

O run `34881426374` executou o workflow operacional completo e terminou `success`.

Passaram, na ordem:

- checkout sem credenciais persistentes;
- Python 3.11;
- Java 17;
- Node 22;
- dependências Python e `pyspark==4.0.1`;
- `pnpm@10.34.5` e dependências do compositor V06 com `--frozen-lockfile`;
- `python tools/ci_local.py --verbose`;
- `python -B tools/tests/test_temas_v09.py -v` — **12/12 PASS**;
- `python tools/tests/test_transicao_trabalho.py --spark -v` — **43/43 PASS com Spark local**;
- geração do kit — **535 arquivos + `MANIFEST.json`**;
- validação do ZIP — `theme_contract` v1 com **9/9 caminhos e SHA256 válido**, `manual_opt_in`, `not_performed`;
- `upload-artifact` somente depois da validação do ZIP.

O kit gerado registrou commit `4ae714a35a0a`; SHA256 do `MANIFEST.json`: `7b8e811038bb34a4aebade9d3c58e2c308495ce60ccc563bb860ff43ade8e6ea`.

O artefato GitHub Actions `kit-transicao-trabalho` foi criado com artifact ID `10363302284`; isso é transporte de evidência no GitHub Actions e **não é publicação no Databricks**.

No CI local do mesmo head:

- validador: **APROVADO — 0 falhas / 0 avisos**;
- identidade medida: **1355 arquivos**;
- links fora da raiz: **1850**;
- `GITHUB_TOKEN`: `Contents: read` / `Metadata: read`.

## Escopo do diff funcional

A V09 funcional não alterou qualquer arquivo do produto em `ambiente_fonte/.assistant` ou `Novo_Ambiente_Simulado`. O runtime, schema temático, tokens, paletas, APIs legadas e rotas `_resolvido` permaneceram byte a byte como estavam na base V08. A mudança funcional ficou na ferramenta de empacotamento e nas guardas offline.

A correção pós-merge também não alterou produto/runtime; somente preparou corretamente o runner do workflow operacional e adicionou a respectiva regressão.

## Restrições preservadas

- sem registro global de tema;
- sem alteração de paleta/schema/tokens;
- sem alteração de dados, métricas, amostragem, denominadores, thresholds, embeddings ou lógica analítica;
- sem upload manual, publicação ou chamada Databricks;
- sem alteração de ACL, compute, workspace, Spark/SQL/MLflow remoto;
- Spark do gate operacional foi **local no runner**, não Databricks;
- sem homologação declarada de browser, acessibilidade ou UAT;
- V10 não iniciada por este fechamento.

## Próximo gate

Este arquivo integra o fechamento documental pós-merge. O próximo gate é validar e integrar a PR documental correspondente, confirmar o estado vivo da `main` e somente então considerar a V09 integralmente encerrada. **A V10 não pode iniciar antes desse fechamento documental.**
