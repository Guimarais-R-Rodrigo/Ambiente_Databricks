# V11 — testes e evidências

## Estado

V11 aceita e integrada no Git pelo PR #52. O head funcional/documental aceito é `5532ca6d8f1b243ca705088f4b57823a333b9b1f`; o merge funcional é `9305bc49eaf002caec042361bf35efa66af7ca18`. Este arquivo registra somente resultados observados; nenhum PASS local/GitHub equivale a homologação Databricks.

## Suíte específica

`tools/tests/test_temas_v11.py` cobre:
- cobertura exata dos 48 tokens notebook;
- contagem 3 traduzidos / 23 aproximados / 22 não suportados;
- `context="aibi"` ainda reservado;
- fontes oficiais somente em `docs.databricks.com`;
- projeção revalidando `ResolvedTheme`;
- recusa de contexto editorial pela fronteira V11;
- export determinístico e marcado como não nativo;
- conjunto exato de três bindings diretos;
- binding fixado por SHA-256;
- recusa de aproximação automatizada;
- recusa de JSON Pointer inexistente;
- binding seletivo com omissões explícitas;
- política de snapshot/reaplicação sem propagação universal;
- separação tema × publicação;
- guardas de admin/draft;
- fixture sintético não importável;
- preservação do fingerprint semântico;
- equivalência fonte/simulado;
- import da fachada tanto no modo local quanto pelo namespace do produto;
- workflow read-only;
- varredura dos módulos Python V11 contra API/SDK/CLI Databricks.

## Workflow

`.github/workflows/temas-v11-ci.yml` executa suíte V11, sintaxe em memória, regressões V01–V11, V00 e validador estrutural/documental. Ele não recebe credenciais Databricks e não possui passo remoto.

## Failures preservados

### Run `34900693160` — FAILURE funcional na primeira composição

No head `ed1fdaac22e3ceece54b6ada96427b5a8afcba95`, a suíte V11 executou **20 testes: 19 PASS / 1 FAILURE**. O caso de contexto editorial era corretamente recusado pelo núcleo V02, mas a exceção escapava como `ThemeError`, atravessando a fronteira pública da V11 em vez de ser normalizada para `AibiThemeError`.

A correção foi feita sem alterar V02 e sem relaxar o teste: `aibi_theme.py` tornou-se uma fachada pública pequena, com a implementação detalhada em `_aibi_theme_impl.py`, e a fronteira `notebook` passou a ser validada antes da delegação. O run permanece **FAILURE**.

### Run `34901091132` — FAILURE documental após gates funcionais verdes

No head `5eca34c95fc9970f864869282f59e2bb4cc61d56` passaram antes do validador:
- V11 específica: **20/20 PASS**;
- sintaxe da fachada: **PASS**;
- regressões V01–V11: **456/456 PASS**;
- compatibilidade V00: **12/12 PASS**.

O validador terminou com **3 falhas / 0 avisos** por métricas antigas no README raiz. A etapa de escopo V11 foi `SKIP` por consequência; ela não é reclassificada. O run permanece **FAILURE**.

### Run `34901776770` — FAILURE do novo oráculo de import

No head `8785822e045edf158f04ea41ea0f6c059ef11cb1`, a guarda de import pelo namespace do produto funcionou e a projeção foi criada corretamente, mas o teste comparou o `source_theme_id` com `legado_notebook`; a fixture canônica usa `hub-legado-notebook`. O único failure entre **21 testes** foi esse oráculo incorreto. As etapas posteriores ficaram `SKIP`; o run permanece **FAILURE**.

### Run `34904363803` — FAILURE documental no registro final

No head `795edf879c6f013553afa725a02473d49c909624`, V11 passou **21/21**, as regressões **457/457** e V00 **12/12**. O validador terminou em **3 falhas / 0 avisos** porque um SHA abreviado no checkpoint coincidiu com a guarda de identificador corporativo plausível; como o validador já tinha uma falha, não emitiu a linha `APROVADO`, e a conferência do README raiz falhou por consequência. O escopo ficou `SKIP`. A correção não alterou validador, produto ou testes funcionais. O run permanece **FAILURE**.

Nenhum failure ou `SKIP` acima é reclassificado.

## Evidências integralmente verdes

### Run `34902083889` — primeiro gate verde

Head `0d3180c50428d8716b44f264b915a91243ba96c3`:
- V11 específica: **21/21 PASS**;
- sintaxe: **PASS**;
- regressões V01–V11: **457/457 PASS**;
- V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**;
- escopo V11: **PASS**.

### Run `34902853430` — navegação/documentação revalidada

Head `5bb8234422fdd284a9e14815ef566ec0b52a2952`: repetiu V11 **21/21**, regressões **457/457**, V00 **12/12**, validador **0/0**, escopo **PASS**, source/simulado equivalentes e workflow read-only.

### Run `34904743766` — correção de higiene documental revalidada

Head `6561dfbe147c454fdc07eebac3d644b6ae1bf6d0`: repetiu integralmente V11 **21/21**, regressões **457/457**, V00 **12/12**, validador **0/0** e escopo **PASS**.

### Run `34905080083` — gate definitivo pré-PR

Head final `5532ca6d8f1b243ca705088f4b57823a333b9b1f`:
- V11 específica: **21/21 PASS**;
- sintaxe V11: **PASS**;
- regressões V01–V11: **457/457 PASS**;
- V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- escopo V11: **PASS**;
- source/simulado equivalentes;
- `Contents: read` e checkout sem credenciais persistentes.

Métricas verificáveis nesse head:

```text
skills             : 14 · 14/14 com as 5 seções estruturais
prompts            : 16 · 161 campos com guia e contrato humano
helpers citados    : 92 caminhos verificados
markdown / links   : 222 arquivos / 1395 links relativos
notebooks / links  : 80 notebooks / 101 links relativos
readmes de objeto  : 76/76 operacionais; 3/3 exemplares; 0 pendentes
pastas de objeto   : 62 conferidas
forma da pasta     : 60 conferidas
contrato de dados  : 62 pares
contrato de entrada: 60 pares
saída colada       : 79 notebooks com bloco real, 0 sem
idioma da docstring: 62 módulos, 0 com docstring em inglês
normas do molde    : 72 arquivos, 0 violações
notebook exercita  : 60 objetos, 0 notebook(s) que só importam
python (AST)       : 221 arquivos
instrucoes         : 9043/20000 caracteres
repo (identidade)  : 1409 arquivos varridos no repositório editável/derivado
repo (links)       : 1887 links fora da raiz analisada
worktree (extras)  : 0

APROVADO: 0 falha(s), 0 aviso(s)
```

## Evidência real de PR

A PR #52 foi aberta inicialmente em draft sobre o head exato `5532ca6d8f1b243ca705088f4b57823a333b9b1f`. **11/11 workflows reais de `pull_request`** concluíram com `success`:
- V00;
- V01;
- V02;
- V03;
- V04;
- V05;
- V06;
- V08;
- V10;
- V11;
- CI local reproduzível.

Após aceite explícito, a PR foi marcada pronta e integrada sem alterar o head aceito.

## Evidência pós-merge funcional

Merge: `9305bc49eaf002caec042361bf35efa66af7ca18`.

Os **13 workflows** disparados por `push` na `main` concluíram com `success`; não houve `failure` nem job remanescente em execução na auditoria final. Isso fecha o gate funcional de integração da V11.

## Gates de ambiente ainda pendentes

- export real de theme JSON;
- binding revisado contra esse export;
- Import theme em dashboard draft;
- teste de tema de workspace por administrador;
- teste de reaplicação/snapshot;
- browser light/dark;
- preservação real de query/filter;
- acessibilidade;
- UAT.

Esses gates não invalidam o fechamento Git da V11, mas bloqueiam qualquer afirmação de homologação operacional. Nenhuma mutação Databricks foi executada pela V11.