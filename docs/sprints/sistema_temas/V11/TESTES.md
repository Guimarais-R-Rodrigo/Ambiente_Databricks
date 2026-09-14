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
- recusa de contexto editorial;
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
- workflow read-only sem API/SDK/CLI Databricks.

## Workflow

`.github/workflows/temas-v11-ci.yml` executa suíte V11, sintaxe em memória, regressões V01–V11, V00 e validador estrutural/documental. Ele não recebe credenciais Databricks e não possui passo remoto.

## Evidências

A preencher com IDs e resultados reais dos runs desta branch. Failures, se ocorrerem, permanecem registrados como failures e não serão reclassificados.

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
