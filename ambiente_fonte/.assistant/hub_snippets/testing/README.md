# Categoria `testing` — fixtures e dados sintéticos para testes e exemplos

<!-- readme-categoria: 1.0.0 -->

Contém geradores de dados sintéticos usados por notebooks e testes para exercitar contratos sem depender de dados reais do workspace.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais com contrato e evidência delimitada por objeto; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Use para exemplos reproduzíveis, testes de contrato e cenários controlados antes de envolver dados reais.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Papel resumido | Documentação |
|---|---|---|
| [`fixtures`](fixtures/README.md) | dados sintéticos com propósito de teste | [guia local](fixtures/README.md) |

Os [testes internos](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks) são infraestrutura de regressão, não novos objetos nem API pública.

| Gerador de `fixtures` | Caso de uso |
|---|---|
| `base_tabular` | registros, nulos e chaves repetidas |
| `serie_temporal` | entidade × mês |
| `fatos_e_features` | par de decisões e histórico com versões futuras |
| `safras` | contrato × MOB, evento acumulado |

A geração monta listas **localmente em Python**, antes do DataFrame Spark. Para quotas exatas de borda, use linhas explícitas; probabilidades não garantem contagens.

## Cuidados da categoria

Fixtures não representam distribuição real nem homologam comportamento em produção. A suíte do mantenedor fica em `tools/tests/runtime/` no repositório e não é distribuída com o produto.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 1 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/testing/`.
