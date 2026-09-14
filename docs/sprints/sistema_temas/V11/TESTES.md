# V11 — testes e evidências

## Estado

Candidata técnica com navegação/documentação reconciliada. O último head funcional/documental integralmente verde antes deste registro é `6561dfbe147c454fdc07eebac3d644b6ae1bf6d0`, run `34904743766`. Este arquivo registra somente resultados observados; nenhum PASS local equivale a homologação Databricks.

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
- varredura de todos os módulos Python V11 contra API/SDK/CLI Databricks.

## Workflow

`.github/workflows/temas-v11-ci.yml` executa suíte V11, sintaxe em memória, regressões V01–V11, V00 e validador estrutural/documental. Ele não recebe credenciais Databricks e não possui passo remoto.

## Failures preservados

### Run `34900693160` — FAILURE funcional na primeira composição

No head `ed1fdaac22e3ceece54b6ada96427b5a8afcba95`, a suíte V11 executou **20 testes: 19 PASS / 1 FAILURE**. O caso de contexto editorial era corretamente recusado pelo núcleo V02, mas a exceção escapava como `ThemeError`, atravessando a fronteira pública da V11 em vez de ser normalizada para `AibiThemeError`.

A correção foi feita sem alterar V02 e sem relaxar o teste: `aibi_theme.py` tornou-se uma fachada pública pequena, com a implementação detalhada em `_aibi_theme_impl.py`, e a fronteira `notebook` passou a ser validada antes da delegação. O run `34900693160` permanece **FAILURE**.

### Run `34901091132` — FAILURE documental após gates funcionais verdes

No head `5eca34c95fc9970f864869282f59e2bb4cc61d56` passaram antes do validador:
- V11 específica: **20/20 PASS**;
- sintaxe da fachada: **PASS**;
- regressões V01–V11: **456/456 PASS**;
- compatibilidade V00: **12/12 PASS**.

O validador terminou com **3 falhas / 0 avisos**, exclusivamente por três métricas antigas no README raiz:

```text
markdown / links   : 222 arquivos / 1394 links relativos
python (AST)       : 221 arquivos
repo (identidade)  : 1409 arquivos varridos no repositório editável/derivado
```

O valor de `repo (links)` observado permaneceu **1878**. A etapa de escopo V11 foi `SKIP` por consequência do failure anterior do job; ela não é reclassificada como PASS. O run `34901091132` permanece **FAILURE**.

### Run `34901776770` — FAILURE do novo oráculo de import

No head `8785822e045edf158f04ea41ea0f6c059ef11cb1`, a guarda nova de import pelo namespace do produto funcionou e a projeção foi criada corretamente, mas o teste comparou o `source_theme_id` com `legado_notebook`. A fixture canônica V02 usa `hub-legado-notebook`; portanto o único failure entre **21 testes** foi um oráculo incorreto introduzido pelo próprio endurecimento.

A correção alterou somente a expectativa do teste para o ID canônico real. A guarda de import e a varredura de todos os módulos Python continuam ativas. Como a suíte V11 falhou, sintaxe, regressões, V00, validador e escopo foram `SKIP` nesse run. O run `34901776770` permanece **FAILURE**.

### Run `34904363803` — FAILURE documental no registro final

No head `795edf879c6f013553afa725a02473d49c909624`, a suíte V11 passou **21/21**, as regressões passaram **457/457** e V00 passou **12/12**. O validador terminou em **3 falhas / 0 avisos** porque `CHECKPOINT_V11.md` abreviou o SHA base como prefixo seguido de reticências; esse texto coincidiu com a guarda de identificador corporativo plausível. Como o validador já tinha uma falha, ele não emitiu a linha `APROVADO`, e a conferência do README raiz também falhou por consequência. O escopo V11 ficou `SKIP`.

A correção usa o SHA completo e não altera o validador, o produto ou os testes funcionais. O run `34904363803` permanece **FAILURE**.

## Evidências integralmente verdes

### Run `34902083889` — SUCCESS no head `0d3180c50428d8716b44f264b915a91243ba96c3`

A execução confirmou:
- V11 específica: **21/21 PASS**;
- sintaxe da fachada compilada em memória: **PASS**;
- regressões cumulativas V01–V11: **457/457 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- etapa de escopo: **PASS**;
- token do workflow: `Contents: read`;
- checkout: `persist-credentials: false`.

Esse foi o primeiro gate integralmente verde antes da reconciliação final de navegação.

### Run `34902853430` — SUCCESS no head documental `5bb8234422fdd284a9e14815ef566ec0b52a2952`

Depois da reconciliação da navegação e dos documentos vivos, o gate completo foi repetido e confirmou:
- V11 específica: **21/21 PASS**;
- sintaxe da fachada compilada em memória: **PASS**;
- regressões cumulativas V01–V11: **457/457 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- etapa de escopo: **PASS**;
- source/simulado V11 byte a byte equivalentes;
- token do workflow: `Contents: read`;
- checkout: `persist-credentials: false`;
- nenhuma operação/API/SDK/CLI Databricks executada.

### Run `34904743766` — SUCCESS após correção de higiene documental

No head `6561dfbe147c454fdc07eebac3d644b6ae1bf6d0`, a execução repetiu integralmente:
- V11 específica: **21/21 PASS**;
- sintaxe V11: **PASS**;
- regressões V01–V11: **457/457 PASS**;
- V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- escopo V11: **PASS**.

Esse run comprova que a falha `34904363803` era exclusivamente textual e que a correção não alterou comportamento funcional.

Métricas verificáveis vigentes:

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

Este registro documental move o head novamente; o workflow V11 deve ser repetido uma última vez no head definitivo e, se verde, esse resultado será usado como evidência pré-PR sem nova edição documental.

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

Esses gates não bloqueiam uma candidata Git estritamente local, mas bloqueiam homologação operacional.
