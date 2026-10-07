<!-- Template: cabeçalho %md de notebook completo (skill hub-ml-comentar-notebook) -->

```md
# [Título do notebook]

| Campo | Valor |
|-------|-------|
| **Autor** | [autor/equipe informados ou NÃO INFORMADO] |
| **Versão** | [versão observada do artefato ou NÃO INFORMADA] |
| **Criação** | [YYYY-MM-DD] |
| **Última atualização** | [YYYY-MM-DD] |
| **Projeto** | [NOME_DO_PROJETO] |
| **Catálogo principal** | `[CATALOGO]` |
| **Schema principal** | `[SCHEMA]` |
| **Status** | [estado comprovado e fonte, ou NÃO INFORMADO] |

## Objetivo

[4 a 8 linhas explicando o propósito do notebook, o problema que resolve e
o resultado esperado.]

## Público-alvo

[Quem deve conseguir ler e entender este notebook: PO, eng. de dados, eng.
de ML, analista de negócio.]

## Contexto no projeto

[Posicionamento dentro do projeto/produto. Ex.: "Este notebook é a etapa de
escrita Delta da camada gold do pipeline de Renda Fixa, executado após o
notebook de transformação."]

## Fontes (entradas)

- `[CATALOGO].[SCHEMA].[TABELA_ENTRADA_1]` — [breve descrição]
- `[CATALOGO].[SCHEMA].[TABELA_ENTRADA_2]` — [breve descrição]
- Parâmetro `data_referencia` (widget) — formato `YYYY-MM-DD`.

## Saídas previstas versus observadas

[Relacionar apenas saídas presentes no código; registrar evidência da execução ou NÃO EXECUTADO. Não inventar tabela/log/métrica para completar o molde.]

- `[CATALOGO].[SCHEMA].[TABELA_SAIDA]` — [descrição].
- Registro em `[CATALOGO].[SCHEMA].[TABELA_LOG_EXECUCAO]`.
- Atualização em `[CATALOGO].[SCHEMA].[TABELA_METRICAS]`.

## Premissas

- [Premissa 1: ex.: "Tabela X é atualizada antes da execução deste notebook."]
- [Premissa 2: ex.: "Existe uma chave única `id_cliente` em `tabela_y`."]
- [Premissa 3]

## Limitações

- [Limitação 1: ex.: "Não trata clientes com cadastro inativo há mais de
  365 dias — esses são tratados em notebook separado."]
- [Limitação 2]

## Riscos conhecidos

- ⚠️ [Risco 1: ex.: "Tabela X eventualmente apresenta duplicidade na chave;
  o notebook aplica `dropDuplicates` por critério explícito."]
- ⚠️ [Risco 2]

## Instruções de execução

1. [Pré-requisito 1: ex.: "Verificar que o notebook `02_transformacao` foi
   executado com sucesso para a `data_referencia` desejada."]
2. [Pré-requisito 2]
3. Configurar widget `data_referencia` para a data desejada.
4. Executar célula a célula em ordem, **não em paralelo**.
5. Conferir resumo executivo no final.
```
