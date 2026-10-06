# Categoria `spark` — operações distribuídas e diagnósticos Spark

<!-- readme-categoria: 1.0.0 -->

Reúne helpers para datas, joins, nulos, amostragem, PSI, exibição segura e relações point-in-time sobre DataFrames Spark.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais com contrato e evidência delimitada por objeto; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Use quando a operação precisa permanecer distribuída ou quando cardinalidade, temporalidade e volume tornam inadequada uma solução puramente local.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Entrada/API | Retorno e efeito |
|---|---|---|
| [`date_features`](date_features/README.md) | `extrair_features_data(df, col_data, ...)` | DataFrame; transformação lazy, pode substituir nomes |
| [`join_diagnostics`](join_diagnostics/README.md) | `diagnosticar_join(esquerda, direita, chave, ...)` | dicionário; ações Spark e pequenas coletas |
| [`null_summary`](null_summary/README.md) | `null_summary(df, ...)` | DataFrame agregado; contagem e coleta agregada no driver |
| [`pit_join`](pit_join/README.md) | `pit_join(fatos, features, chave, ts_decisao, ts_feature, atraso_publicacao_dias=...)` | DataFrame + diagnóstico; join, contagens e agregado local |
| [`psi_calculator`](psi_calculator/README.md) | `calcular_psi` / `calcular_csi` / `interpretar_psi` | float/dicionário/texto; quantis e agregados Spark para o driver |
| [`safe_display`](safe_display/README.md) | `safe_display(df, display_fn=display, ...)` | None; conta prévia e chama renderer |
| [`smart_sample`](smart_sample/README.md) | `smart_sample(df, n, ...)` | DataFrame; ações/contagens, amostra limitada com restrições |

Antes do primeiro import, siga a [preparação da biblioteca](../README.md#passo-a-passo-operacional-como-usar-um-snippet).

## Cuidados da categoria

A API curta não elimina custo de shuffle, coleta ou join. Confira o plano, o grão e os efeitos de cada helper antes de escalar.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 7 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/spark/`.
