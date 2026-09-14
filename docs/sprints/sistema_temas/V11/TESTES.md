# V11 — testes e evidências

## Estado

Candidata em implementação. Este arquivo registra somente resultados observados; nenhum PASS local equivale a homologação Databricks.

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

A correção altera somente a expectativa do teste para o ID canônico real. A guarda de import e a varredura de todos os módulos Python continuam ativas. Como a suíte V11 falhou, sintaxe, regressões, V00, validador e escopo foram `SKIP` nesse run. O run `34901776770` permanece **FAILURE**.

## Ajustes para o próximo head

A revisão seguinte:
- mantém no README raiz somente as três métricas medidas pelo validador;
- mantém import robusto da fachada local/namespace;
- mantém varredura negativa de todos os módulos Python da ponte V11;
- corrige apenas o oráculo de `source_theme_id` para `hub-legado-notebook`;
- mantém fonte e espelho byte a byte equivalentes.

Os resultados dessa revisão devem ser registrados somente após execução real no head correspondente.

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
