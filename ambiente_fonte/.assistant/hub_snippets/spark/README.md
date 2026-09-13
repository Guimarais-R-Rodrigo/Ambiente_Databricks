# Categoria `spark` — operações distribuídas e diagnósticos Spark

<!-- readme-categoria: 1.0.0 -->

Reúne helpers para datas, joins, nulos, amostragem, PSI, exibição segura e relações point-in-time sobre DataFrames Spark.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais já validados; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Use quando a operação precisa permanecer distribuída ou quando cardinalidade, temporalidade e volume tornam inadequada uma solução puramente local.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Papel resumido | Documentação |
|---|---|---|
| [`date_features`](date_features/README.md) | transformar uma data em atributos de calendário explícitos | [guia local](date_features/README.md) |
| [`join_diagnostics`](join_diagnostics/README.md) | medir cobertura e expansão antes de juntar | [guia local](join_diagnostics/README.md) |
| [`null_summary`](null_summary/README.md) | resumir ausência por coluna com limiares explícitos | [guia local](null_summary/README.md) |
| [`pit_join`](pit_join/README.md) | reconstruir a informação disponível no momento da decisão | [guia local](pit_join/README.md) |
| [`psi_calculator`](psi_calculator/README.md) | medir mudança de distribuição com referência fixa | [guia local](psi_calculator/README.md) |
| [`safe_display`](safe_display/README.md) | limitar a prévia antes de chamar o renderer | [guia local](safe_display/README.md) |
| [`smart_sample`](smart_sample/README.md) | criar amostras limitadas com opção de preservar estratos | [guia local](smart_sample/README.md) |

## Cuidados da categoria

A API curta não elimina custo de shuffle, coleta ou join. Confira o plano, o grão e os efeitos de cada helper antes de escalar.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 7 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/spark/`.
