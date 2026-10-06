# Categoria `display` — exibição e leitura de resultados analíticos

<!-- readme-categoria: 1.0.0 -->

Agrupa helpers de apresentação de DataFrames, matrizes e distribuições para tornar resultados mais legíveis sem confundir visualização com transformação de negócio.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais com contrato e evidência delimitada por objeto; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Use quando o dado já existe e a necessidade principal é inspecionar ou comunicar o resultado em tabela, matriz ou grade.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Entrada/API | Retorno e efeito |
|---|---|---|
| [`correlation_matrix`](correlation_matrix/README.md) | Spark → `plot_correlation` ou variante resolvida | figura + pares; cálculo distribuído, matriz quadrática no driver |
| [`dataframe_styled`](dataframe_styled/README.md) | pandas → `display_styled` ou variante resolvida | HTML local; não converte Spark; requer Jinja2 |
| [`distribution_grid`](distribution_grid/README.md) | Spark → `plot_distributions` ou variante resolvida | figura; recorte para pandas e dados dos histogramas no browser |

Antes do primeiro import, siga a [preparação da biblioteca](../README.md#passo-a-passo-operacional-como-usar-um-snippet).

As rotas `_resolvido` recebem tema explícito; as legadas mantêm o comportamento padrão. Correlação coleta uma matriz, distribuição coleta linhas limitadas e tabela estilizada já recebe pandas local. Nunca converta uma base Spark inteira apenas porque a categoria se chama display.

## Cuidados da categoria

Recursos de display podem coletar ou materializar dados no driver dependendo do objeto. Confira volume, efeito e dependências no guia local.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 3 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/display/`.
