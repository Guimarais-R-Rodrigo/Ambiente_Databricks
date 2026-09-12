# V04 — componentes HTML, estilos compartilhados e tabelas

## Estado desta sprint

**CANDIDATA EM IMPLEMENTAÇÃO E VALIDAÇÃO.** A V04 parte da `main`
`b83a7cde84d7a44fc8a1fed996fda4f8b5b1eec2`, que já contém V03 e R04-A.
Esta sprint não está aceita nem integrada enquanto seu PR não passar pelos gates
e receber decisão explícita do mantenedor.

Não há publicação no Databricks nesta etapa. Não há seletor visual, folha de
estilo global ou migração automática de todos os notebooks.

## Para quem nunca entrou no Hub

Você pode continuar usando o Hub exatamente como antes. As funções históricas
continuam existindo e usam a aparência histórica quando chamadas sem a nova rota.

A V04 acrescenta uma escolha explícita para quem **já possui um `ResolvedTheme`**:
usar funções com sufixo `_resolvido`. Elas mudam apenas a apresentação do bloco
que está sendo criado naquela chamada. Não alteram outros componentes já exibidos,
não gravam configuração na sessão e não publicam tema.

Exemplo sintético:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.section_header import section_header_html_resolvido

tema = load_reference_theme("notebook")
html = section_header_html_resolvido(
    tema,
    titulo="Resumo executivo",
    descricao="Base sintética para demonstração.",
)
```

A configuração de referência mantém a aparência legada. Uma configuração
notebook completa e válida pode mudar as propriedades visuais mapeadas pelo
contrato.

## Objetivo técnico

A V03 conectou o núcleo de temas ao Plotly. A V04 aplica o mesmo princípio aos
componentes HTML e à tabela pandas:

1. manter as APIs legadas e seus defaults;
2. centralizar o CSS do caminho novo em `hub_snippets.constants.styles`;
3. aceitar somente `ResolvedTheme` íntegro, revalidado pelo núcleo V02;
4. não aceitar CSS livre vindo da configuração;
5. não manter tema global oculto;
6. preservar textos, cálculos, dados, cortes de score e ordem dos componentes;
7. documentar a diferença entre compatibilidade de código e homologação visual.

## Componentes cobertos

| Componente | Caminho legado preservado | Nova rota opt-in |
|---|---|---|
| Badge de status | `badge_status(...)` | `badge_status_resolvido(..., theme, ...)` |
| Badge de score | `badge_score(...)` | `badge_score_resolvido(..., theme, ...)` |
| Badge informativo | `badge_inline(...)` | `badge_inline_resolvido(..., theme)` |
| Divisores | `divider_*()` | `divider_*_resolvido(theme)` |
| KPI card HTML | `kpi_card_html(...)` | `kpi_card_html_resolvido(..., theme)` |
| Cabeçalho de seção | `section_header_html(...)` | `section_header_html_resolvido(theme, ...)` |
| Índice EDA | `gerar_indice_eda(...)` | `gerar_indice_eda_resolvido(theme, ...)` |
| Tabela pandas | `display_styled(...)` | `display_styled_resolvido(..., theme, ...)` |
| CSS compartilhado | constantes `STYLE_*` | `get_styles_resolvidos(theme)` |

`kpi_card_markdown` não recebe tema porque Markdown é uma representação textual.
O índice resolvido aceita `markdown=True` por compatibilidade de fluxo, mas nessa
saída o tema é apenas validado; nenhum CSS é inserido no texto.

## O que o tema pode alterar nesta sprint

A V04 usa os tokens notebook já aprovados no ADR-0013 e promovidos na V02. Não
cria novo schema nem altera o fingerprint do contrato.

Os principais grupos consumidos são:

- `brand.primary`;
- `text.primary` e `text.secondary`;
- `surface.section` e `surface.card`;
- `divider.light` e `divider.medium`;
- `status.ok_*`, `status.warn_*` e `status.fail_*`;
- `semantic.negative`;
- `table.header_text`;
- `font.family` nos componentes HTML;
- dimensões de `section.*`, `card.*` e `badge.*`.

Algumas propriedades históricas que não possuem token no contrato permanecem
fixas. A V04 não inventa controles para margem, raio do item do índice ou fonte
da tabela apenas para aumentar a quantidade de opções.

## Centralização sem estado global

`get_styles_resolvidos(theme)` materializa um **novo dicionário** a cada chamada.
O dicionário contém somente propriedades construídas a partir de tokens
validados e constantes controladas pelo código. Alterar essa cópia não altera o
`ResolvedTheme` nem futuras chamadas.

Os componentes V04 usam essa materialização apenas quando a função `_resolvido`
é chamada. As funções legadas continuam consumindo constantes históricas.
Portanto, editar ou carregar um tema não reestiliza silenciosamente notebooks em
execução.

## Integridade e fail-closed

As rotas V04 recusam:

- dicionário cru em lugar de `ResolvedTheme`;
- `ResolvedTheme` com fingerprint adulterado;
- tema de contexto `readme`/`presentation` em componente de notebook;
- qualquer configuração que o núcleo V02 não consiga revalidar.

A materialização chama `export_theme(theme)` antes de usar os tokens. Isso faz o
adaptador consumir a representação canônica revalidada, em vez de confiar em
campos mutáveis ou copiados do resultado.

## `dark` e `high_contrast`

Diferentemente do adaptador Plotly V03, os componentes HTML da V04 não precisam
recusar automaticamente `dark` ou `high_contrast`: o contrato notebook contém
cores completas de texto e superfície e a materialização não depende de defaults
do Plotly.

Isso **não** significa que esses modos estejam visualmente homologados ou que o
nome `high_contrast` constitua certificação de acessibilidade. Contraste,
legibilidade, foco, zoom e comportamento no `displayHTML` ainda exigem avaliação
visual/runtime própria.

## Tabelas pandas

`display_styled_resolvido` muda somente a apresentação:

- `brand.primary` → fundo do cabeçalho;
- `table.header_text` → texto do cabeçalho;
- `semantic.negative` → cor do destaque de números negativos nas colunas
  selecionadas.

A tabela de entrada não é alterada. `highlight_cols` e `format_dict` preservam o
contrato existente. O identificador aleatório produzido pelo `Styler` impede usar
igualdade byte a byte do HTML como prova estável; os testes normalizam somente
esse UUID e o alias histórico `white`/`#FFFFFF` quando comparam a referência.

## Compatibilidade prometida

A V04 mede explicitamente:

- assinaturas das funções legadas;
- HTML legado de badges, divisores, KPI cards, cabeçalhos e índice;
- equivalência semântica da tabela pandas;
- escape de textos onde o componente já possuía escape;
- manutenção dos cortes de `badge_score`;
- preservação do DataFrame de entrada;
- ausência de mutação ou estado visual global.

A configuração de referência deve reproduzir a aparência histórica. Isso não
autoriza substituir todos os usos antigos pelas rotas novas nesta sprint.

## Fora de escopo

A V04 não implementa:

- seletor ou Visual Lab em notebook;
- edição de temas por usuário não técnico;
- Databricks Apps/Streamlit;
- AI/BI Dashboard themes;
- publicação, aprovação ou rollback de tema no workspace;
- migração de gráficos adicionais de ML;
- CSS global que atravesse o isolamento de `displayHTML`;
- recoloração de imagens raster;
- certificação de acessibilidade.

Esses itens permanecem em sprints próprias do plano V00–V14.

## Testes

A bateria específica está em
[`tools/tests/test_temas_v04.py`](../../../../tools/tests/test_temas_v04.py).
Ela é complementada pelas regressões V00–V03, pelo `validate_assistant.py` e pelo
gate completo `tools/ci_local.py` na candidata final.

O histórico de execuções, inclusive falhas que não devem ser promovidas a PASS,
fica em [TESTES.md](TESTES.md).

## Aceite e integração

O término técnico da implementação não significa aceite. O checkpoint desta
sprint diferencia:

- implementação;
- testes automatizados;
- revisão/aceite humano;
- integração Git;
- homologação visual/runtime no Databricks.

A próxima ação após uma candidata verde é revisar o PR e o
[CHECKPOINT_V04.md](CHECKPOINT_V04.md). Sem aceite explícito, não fazer merge e
não iniciar V05.
