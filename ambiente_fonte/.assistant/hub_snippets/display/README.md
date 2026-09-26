# Categoria `display` — exibição e leitura de resultados analíticos

<!-- readme-categoria: 1.0.0 -->

Agrupa helpers de apresentação de DataFrames, matrizes e distribuições para tornar resultados mais legíveis sem confundir visualização com transformação de negócio.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais já validados; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Use quando o dado já existe e a necessidade principal é inspecionar ou comunicar o resultado em tabela, matriz ou grade.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Papel resumido | Documentação |
|---|---|---|
| [`correlation_matrix`](correlation_matrix/README.md) | entenda relações entre variáveis numéricas | [guia local](correlation_matrix/README.md) |
| [`dataframe_styled`](dataframe_styled/README.md) | apresente uma tabela sem mudar seus dados | [guia local](dataframe_styled/README.md) |
| [`distribution_grid`](distribution_grid/README.md) | veja a forma das variáveis, não só a média | [guia local](distribution_grid/README.md) |

## Cuidados da categoria

Recursos de display podem coletar ou materializar dados no driver dependendo do objeto. Confira volume, efeito e dependências no guia local.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 3 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/display/`.
