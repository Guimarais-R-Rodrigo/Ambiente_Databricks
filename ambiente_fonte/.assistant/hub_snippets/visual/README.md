# Categoria `visual` — componentes visuais, tema e composição

<!-- readme-categoria: 1.0.0 -->

Agrupa componentes de identidade visual, cards, divisores, cabeçalhos e temas usados para padronizar a apresentação dos notebooks e gráficos do Hub.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais com contrato e evidência delimitada por objeto; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Entre aqui quando o objetivo for composição visual, tema ou consistência de apresentação, e não cálculo estatístico ou transformação do dataset.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Entrada/API | Retorno e efeito |
|---|---|---|
| [`badge`](badge/README.md) | Texto/status/score; legado ou `_resolvido` | HTML; cortes locais no score |
| [`divider`](divider/README.md) | Sem dados; legado ou `_resolvido(theme)` | HTML; sem ação de sessão |
| [`index_generator`](index_generator/README.md) | Etapas declaradas; legado ou resolvido | HTML/Markdown; sem navegação ou verificação de execução |
| [`kpi_card`](kpi_card/README.md) | Métricas formatadas; HTML legado/resolvido ou Markdown | string; não calcula indicadores |
| [`section_header`](section_header/README.md) | Etapa/textos; legado ou resolvido | HTML; não cria sumário nativo |
| [`tema`](tema/README.md) | Configuração completa / arquivo JSON autorizado | ResolvedTheme/bytes; valida, não aplica |
| [`theme_lab`](theme_lab/README.md) | Tema notebook/light e proposta | experimenta/compara; pode salvar sessão em pasta autorizada |
| [`theme_plotly`](theme_plotly/README.md) | Figura/tema | muta figura; registro opcional e ativação de default são efeitos de sessão |

Antes do primeiro import, siga a [preparação da biblioteca](../README.md#passo-a-passo-operacional-como-usar-um-snippet).

Rota de tema: validar em `tema` → aplicar explicitamente no consumidor → experimentar em `theme_lab` → salvar somente quando desejado e autorizado. Comece pelo [primeiro uso do laboratório](theme_lab/GUIA_PRIMEIRO_USO.md). Presença no pacote não comprova instalação ou homologação de interface.

## Cuidados da categoria

A aparência não valida a análise. Mantenha separado o que é tema, o que é dado e o que é decisão de negócio.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 8 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/visual/`.
