# Categoria `constants` — constantes, formatos e identidade compartilhada

<!-- readme-categoria: 1.0.0 -->

Reúne valores e convenções reutilizáveis para formatação brasileira, cores, estilos e símbolos usados por outros componentes do Hub.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais já validados; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Entre aqui quando a dúvida for sobre apresentação padronizada, formatação monetária/percentual ou constantes compartilhadas, e não sobre cálculo analítico do dado.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Papel resumido | Documentação |
|---|---|---|
| [`colors`](colors/README.md) | cores com significado consistente | [guia local](colors/README.md) |
| [`emojis`](emojis/README.md) | símbolos para orientar a leitura | [guia local](emojis/README.md) |
| [`format_br`](format_br/README.md) | apresentar números sem mudar o que eles significam | [guia local](format_br/README.md) |
| [`styles`](styles/README.md) | aparência reutilizável para blocos HTML | [guia local](styles/README.md) |

## Cuidados da categoria

Alterar uma constante pode afetar vários consumidores. Leia o README do objeto e procure imports cruzados antes de mudar valores públicos.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 4 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/constants/`.
