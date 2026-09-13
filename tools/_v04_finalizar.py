"""Finalização transitória da V04.

Executado somente pelo workflow de preparação da candidata. Reconciliará
exclusivamente documentação/fachadas derivadas a partir da fonte V04 já testada.
O arquivo é removido antes do commit final.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: esperado 1 trecho para substituir, encontrado {count}: {old[:80]!r}")
    write(path, text.replace(old, new, 1))


def regex_once(path: str, pattern: str, replacement: str) -> None:
    text = read(path)
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S | re.M)
    if count != 1:
        raise SystemExit(f"{path}: regex esperava 1 ocorrência, encontrou {count}: {pattern[:100]!r}")
    write(path, updated)


def insert_before_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if block.strip() in text:
        raise SystemExit(f"{path}: bloco V04 já existe; finalizador não é idempotência silenciosa")
    if text.count(marker) != 1:
        raise SystemExit(f"{path}: marcador esperado uma vez: {marker!r}")
    write(path, text.replace(marker, block.rstrip() + "\n\n" + marker, 1))


# ---------------------------------------------------------------------------
# READMEs dos objetos: remover fatos que deixariam de ser verdade e ensinar V04.
# ---------------------------------------------------------------------------
replace_once(
    "ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md",
    "> CSS descreve como um elemento aparece. Este módulo oferece trechos de CSS para uso explícito; ele não é um painel central que reestiliza todo o Hub.",
    "> CSS descreve como um elemento aparece. O módulo preserva as constantes legadas e, na V04, também materializa estilos a partir de um `ResolvedTheme` recebido explicitamente; ele continua sem reestilizar o Hub de forma global.",
)
replace_once(
    "ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md",
    "O módulo também fornece `FONT_FAMILY`. Não contém um arquivo de fonte nem instala tipografia. **Na implementação lida, os componentes visuais da biblioteca não importam este módulo**; eles mantêm seus próprios estilos. O recurso serve a quem o usa explicitamente.",
    "O módulo também fornece `FONT_FAMILY`. Não contém um arquivo de fonte nem instala tipografia. Na V04, badges, divisores, KPI cards, cabeçalhos, índice e tabela pandas consomem este módulo **somente nas novas rotas `_resolvido`**. As rotas legadas continuam usando constantes compatíveis e não são reestilizadas por carregar um tema.",
)
replace_once(
    "ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md",
    "Não use este arquivo como controle global de identidade visual. Alterar `STYLE_KPI_CARD` não muda automaticamente o retorno de `kpi_card_html`: são implementações distintas.",
    "Não use este arquivo como controle global de identidade visual. `get_styles_resolvidos(theme)` devolve uma cópia para uso explícito; carregar ou editar uma configuração não reestiliza `kpi_card_html`, HTML já exibido nem outros componentes da sessão.",
)
replace_once(
    "ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md",
    "Você recebe nove constantes públicas: uma família de fontes e oito trechos de estilo. Entre eles estão cabeçalho, cartão, divisórias leve/pesada, estados de badge e item de índice. Não há uma função que recebe dados e retorna um relatório.",
    "A API mantém as constantes públicas de compatibilidade e acrescenta `get_styles_resolvidos(theme)`. A função recebe somente um `ResolvedTheme` notebook íntegro e devolve um dicionário novo com estilos para seção, card, divisores, badges, índice e tabela. Não recebe dados analíticos nem retorna relatório.",
)
replace_once(
    "ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md",
    "Há duplicação de CSS com componentes da pasta `visual`. O módulo já importa `colors`, ao contrário do que dizia uma passagem antiga do notebook, mas isso não o transforma em fonte única de todos os estilos.",
    "A V04 elimina a duplicação no **caminho resolvido** dos componentes cobertos, que passam a pedir estilos a `get_styles_resolvidos`. O caminho legado permanece congelado por compatibilidade e não deve ser confundido com um tema global ou folha de estilo de aplicação.",
)
insert_before_once(
    "ambiente_fonte/.assistant/hub_snippets/constants/styles/README.md",
    "## 10. Decisões e configurações que mais importam",
    """### Caminho V04 — tema explícito

```python
from hub_snippets.constants.styles import get_styles_resolvidos
from hub_snippets.visual.tema import load_reference_theme

tema = load_reference_theme("notebook")
styles = get_styles_resolvidos(tema)
assert "section.container" in styles
```

A função revalida o `ResolvedTheme`, exige contexto `notebook` e não aceita dicionário cru. A configuração de referência reproduz os estilos legados. `dark` e `high_contrast` podem ser materializados quando a configuração completa é válida, mas isso não certifica acessibilidade nem homologa a renderização no Databricks.""",
)

replace_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md",
    "A pasta fornece `badge_status`, `badge_score` e `badge_inline`. Não é um motor de qualidade de dados. `badge_status` recebe o estado escolhido; `badge_score` escolhe um estado a partir de limites fixos na implementação.",
    "O caminho legado fornece `badge_status`, `badge_score` e `badge_inline`. A V04 acrescenta as variantes `_resolvido`, que mudam somente a apresentação quando recebem um tema explícito. O módulo não é um motor de qualidade de dados: `badge_status` recebe o estado escolhido e `badge_score` continua usando os mesmos limites fixos.",
)
replace_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md",
    "As cores de estado são parcialmente locais e não vêm de `constants.styles`. O escape de HTML não anonimiza conteúdo: mensagens ainda podem expor dados se o autor os inserir.",
    "Na rota V04, cores e dimensões de estado vêm de `constants.styles` materializado a partir do tema; a rota legada preserva os valores históricos. O escape de HTML não anonimiza conteúdo: mensagens ainda podem expor dados se o autor os inserir.",
)
insert_before_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/badge/README.md",
    "## 10. Decisões e configurações que mais importam",
    """### Caminho V04 — badge com tema explícito

```python
from hub_snippets.visual.badge import badge_status_resolvido
from hub_snippets.visual.tema import load_reference_theme

tema = load_reference_theme("notebook")
html = badge_status_resolvido("Conferido", tema, "ok")
```

Os cortes de `badge_score` não viram tokens e não mudam na V04. Apenas `status.*`, superfície informativa e dimensões do badge são materializados pelo tema. Um tipo desconhecido continua caindo no estilo informativo.""",
)

replace_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md",
    "As funções usam CSS próprio, não as constantes de `styles`. Os separadores mais fortes usam um valor de cor importado; mudanças de sessão não constituem mecanismo de atualização global. Mantenha os títulos mesmo quando a linha parecer suficiente.",
    "As funções legadas preservam seus estilos históricos. Na V04, as variantes `_resolvido` usam `constants.styles`: `divider.light`, `divider.medium` e `brand.primary` chegam do tema validado. Nenhuma delas cria mecanismo de atualização global. Mantenha os títulos mesmo quando a linha parecer suficiente.",
)
replace_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md",
    "[section_header](../section_header/section_header.py) oferece cabeçalho renderizado quando é necessário nomear a seção; [styles](../../constants/styles/README.md) permite composição HTML explícita, sem atualizar automaticamente estas funções.",
    "[section_header](../section_header/section_header.py) oferece cabeçalho renderizado quando é necessário nomear a seção; [styles](../../constants/styles/README.md) concentra a materialização da rota V04, sempre por chamada explícita.",
)
insert_before_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/divider/README.md",
    "## 10. Decisões e configurações que mais importam",
    """### Caminho V04 — divisória com tema explícito

`divider_light_resolvido(theme)`, `divider_medium_resolvido(theme)`, `divider_heavy_resolvido(theme)` e `divider_section_resolvido(theme)` mantêm a mesma estrutura HTML das funções históricas. O tema troca apenas cores mapeadas; margens e a composição de duas linhas da divisória de seção continuam contrato do componente.""",
)

replace_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md",
    "A conversão de chaves para string pode descartar uma entrada Markdown se, por exemplo, o dicionário tiver as chaves `1` e `\"1\"`. Essa limitação foi reproduzida; a recomendação é usar rótulos textuais únicos desde a entrada. O CSS é próprio: alterar `STYLE_KPI_CARD` em `styles` não modifica automaticamente estes cartões.",
    "A conversão de chaves para string pode descartar uma entrada Markdown se, por exemplo, o dicionário tiver as chaves `1` e `\"1\"`. Essa limitação foi reproduzida; a recomendação é usar rótulos textuais únicos desde a entrada. Na V04, `kpi_card_html_resolvido` obtém o CSS de `constants.styles`; `kpi_card_html` continua no caminho legado e não muda por carregar um tema.",
)
insert_before_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/README.md",
    "## 10. Decisões e configurações que mais importam",
    """### Caminho V04 — KPI HTML com tema explícito

```python
from hub_snippets.visual.kpi_card import kpi_card_html_resolvido
from hub_snippets.visual.tema import load_reference_theme

tema = load_reference_theme("notebook")
html = kpi_card_html_resolvido({"Linhas": "1.000"}, tema)
```

A V04 não tematiza `kpi_card_markdown`: Markdown permanece textual. O tema controla somente a apresentação HTML do card; valores, ordem, unidades e contexto continuam responsabilidade do chamador.""",
)

replace_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md",
    "Antes de montar o HTML, o código converte os campos para texto e aplica `html.escape`, que representa sinais como `<` e `>` de modo que apareçam como conteúdo, não como marcação. O módulo monta seu próprio CSS com as cores importadas; não consome automaticamente `STYLE_SECTION_HEADER`.",
    "Antes de montar o HTML, o código converte os campos para texto e aplica `html.escape`, que representa sinais como `<` e `>` de modo que apareçam como conteúdo, não como marcação. A rota legada usa as constantes históricas; `section_header_html_resolvido` obtém container, título e descrição da materialização central da V04.",
)
replace_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md",
    "Editar a constante `STYLE_SECTION_HEADER` não altera o CSS usado nesta implementação. Alterações nas constantes de cores exigem considerar a importação e o estado da sessão, e não atualizam HTML já exibido. Escape de texto reduz a interpretação de marcação, mas não comprova acessibilidade, contraste suficiente ou semântica correta do título. Essas checagens continuam necessárias no destino.",
    "Carregar outro tema não altera `section_header_html` nem HTML já exibido. Somente a chamada explícita de `section_header_html_resolvido(theme, ...)` usa os tokens do tema recebido. Escape de texto reduz a interpretação de marcação, mas não comprova acessibilidade, contraste suficiente ou semântica correta do título; essas checagens continuam necessárias no destino.",
)
insert_before_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/section_header/README.md",
    "## 10. Decisões e configurações que mais importam",
    """### Caminho V04 — cabeçalho com tema explícito

A função `section_header_html_resolvido(theme, ...)` mantém o preenchimento por `SECOES_EDA`, os defaults e o escape da rota legada. `brand.primary`, superfícies, texto, fonte e dimensões `section.*` passam a vir do `ResolvedTheme` notebook recebido explicitamente.""",
)

replace_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/index_generator/README.md",
    "O parâmetro `markdown` muda apenas o formato da string. Não há varredura de células, ordenação automática, deduplicação ou acompanhamento de progresso. Os estilos HTML são montados no próprio módulo com cores importadas.",
    "O parâmetro `markdown` muda apenas o formato da string. Não há varredura de células, ordenação automática, deduplicação ou acompanhamento de progresso. A rota legada usa estilos históricos; `gerar_indice_eda_resolvido` obtém os estilos HTML da materialização V04. Em `markdown=True`, o tema é validado, mas nenhum CSS é inserido no texto.",
)
insert_before_once(
    "ambiente_fonte/.assistant/hub_snippets/visual/index_generator/README.md",
    "## 10. Decisões e configurações que mais importam",
    """### Caminho V04 — índice HTML com tema explícito

`gerar_indice_eda_resolvido(theme, etapas_ativas=..., markdown=False)` preserva a ordem, repetições e conteúdo de `SECOES_EDA`. O tema controla fonte, cor principal, superfície de item e texto secundário somente na saída HTML.""",
)

insert_before_once(
    "ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/README.md",
    "## 10. Decisões e configurações que mais importam",
    """### Caminho V04 — tabela com tema explícito

```python
from hub_snippets.display.dataframe_styled import display_styled_resolvido
from hub_snippets.visual.tema import load_reference_theme

tema = load_reference_theme("notebook")
html = display_styled_resolvido(resumo, tema, highlight_cols=["variacao"])
```

A rota V04 usa `brand.primary` no cabeçalho, `table.header_text` no texto do cabeçalho e `semantic.negative` no realce de negativos. O DataFrame, `highlight_cols` e `format_dict` mantêm o contrato histórico. A fonte da tabela permanece fixa porque o contrato V01 não atribui `font.family` a esse consumidor.""",
)

# ---------------------------------------------------------------------------
# Guia, contexto canônico e índices.
# ---------------------------------------------------------------------------
insert_before_once(
    "ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md",
    "## Para pedir ajuda",
    """## Usar a rota V04 em um componente HTML

A V04 é opt-in. Resolva/carregue primeiro um tema notebook íntegro; depois passe-o à função `_resolvido` do componente. Exemplo:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.section_header import section_header_html_resolvido

tema = load_reference_theme("notebook")
html = section_header_html_resolvido(
    tema,
    titulo="Resumo",
    descricao="Base sintética.",
)
```

A referência mantém a aparência histórica. Outras configurações completas podem mudar somente propriedades cobertas pelo contrato. Não passe dicionário cru, não edite `_values` e não use a função como folha de estilo global. `dark` e `high_contrast` são materializáveis no HTML quando válidos, porém isso não constitui homologação visual ou de acessibilidade.

Para voltar ao comportamento anterior, use a função sem `_resolvido`; não é necessário limpar um tema global porque a V04 não cria um.""",
)

replace_once(
    "CLAUDE.md",
    "- README didático por pasta de objeto: `ADR-0012`, ratificado em 2026-09-12;\n  contrato 1.0.0 estabilizado após aceite do piloto. R03-A/R03-B foram integradas\n  à main com V01 pelo PR nº 13; R04-A é a leva atual de seis snippets Spark em\n  branch de revisão. Estado e retomada: `docs/sprints/readmes_objetos/README.md`.",
    "- README didático por pasta de objeto: `ADR-0012`, ratificado em 2026-09-12;\n  contrato 1.0.0 estabilizado após aceite do piloto. R03-A/R03-B foram integradas\n  pelo PR nº 13 e a R04-A foi integrada pelo PR nº 17, reconciliada com a V02.\n  R04-B permanece separada. Estado e retomada: `docs/sprints/readmes_objetos/README.md`.",
)
replace_once(
    "CLAUDE.md",
    "A V03 está em desenvolvimento na branch `codex/temas-v03`, com adaptador Plotly opt-in; ainda não há aceite, merge ou migração de consumidores legados. Estado: `docs/sprints/sistema_temas/V03/CHECKPOINT_V03.md`.",
    "A V03 foi aceita e integrada pelo PR #16 no commit `b83a7cde84d7a44fc8a1fed996fda4f8b5b1eec2`, após reconciliação com a R04-A. A V04 é a candidata atual: componentes HTML, estilos compartilhados e tabela pandas recebem rotas opt-in `_resolvido`, preservando as APIs legadas. Sem publicação Databricks ou início da V05. Estado: `docs/sprints/sistema_temas/V04/CHECKPOINT_V04.md`.",
)

regex_once(
    "docs/sprints/sistema_temas/README.md",
    r"## Etapa atual — V03 aceita; integração Git autorizada pelo PR #16\n.*?(?=## Aceite de integração Git — 12/09/2026)",
    """## Etapa atual — V04 candidata sobre V03 + R04-A integradas

V00–V03 estão integradas no Git. A V03 foi mesclada pelo PR #16 no commit
`b83a7cde84d7a44fc8a1fed996fda4f8b5b1eec2`, depois de reconciliar a R04-A já
integrada pelo PR #17. Os cinco checks permanentes da V03 passaram novamente na
`main` após o merge.

A [V04 — componentes HTML, estilos e tabelas](V04/README.md) é a etapa corrente
em branch própria. Ela acrescenta apenas rotas opt-in `_resolvido` para badges,
divisores, KPI cards, cabeçalho, índice e tabela pandas, além da materialização
central de CSS em `constants.styles`. As APIs legadas permanecem o default.

Para quem nunca entrou no Hub: não há nada para ativar no Databricks. A V04 não
instala seletor, não cria CSS global e não migra notebooks automaticamente. Leia o
[README V04](V04/README.md), o [checkpoint](V04/CHECKPOINT_V04.md) e o
[guia operacional](../../../ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md).

Não houve publicação Databricks, auditoria independente ou homologação visual.
Aceite e integração Git da V04 permanecem gates posteriores à candidata verde.

""",
)
replace_once(
    "docs/sprints/sistema_temas/README.md",
    "## Continuidade — V03\n\nA V02 está aceita e integrada no Git. A [V03](V03/README.md) recebeu aceite explícito\nde Rodrigo e teve sua integração Git autorizada pelo PR #16: integra explicitamente o\nnúcleo com Plotly preservando o comportamento legado por padrão. O estado efetivo do\nmerge fica registrado na PR; não há publicação Databricks e V04/V05 não foram iniciadas.",
    "## Continuidade — V03/V04\n\nA V03 foi aceita e integrada pelo PR #16; seu adaptador Plotly continua opt-in. A [V04](V04/README.md) parte da `main` desse merge e estende a mesma arquitetura aos componentes HTML e à tabela pandas. V04 ainda é candidata: sem aceite, merge, publicação Databricks ou início da V05.",
)

insert_before_once(
    "docs/sprints/README.md",
    "A [V03](sistema_temas/V03/README.md) recebeu aceite explícito de Rodrigo e teve sua integração Git autorizada pelo PR #16. Ela acrescenta apenas um adaptador Plotly opt-in, preserva o caminho legado por padrão e não migra consumidores existentes. O estado efetivo do merge é registrado na PR. Não houve publicação Databricks; homologação operacional, auditoria independente e avaliação com usuário iniciante permanecem pendentes.",
    """### Continuidade do Sistema de Temas — V04

A V03 foi efetivamente integrada pelo PR #16 no commit `b83a7cde`. A [V04](sistema_temas/V04/README.md) é a candidata corrente para componentes HTML, estilos compartilhados e tabela pandas. O caminho novo é opt-in e não altera automaticamente consumidores legados; aceite, merge e homologação Databricks continuam separados.""",
)

# O helper acima insere ANTES do parágrafo V03; movemos a leitura para ficar V03 -> V04
# sem reescrever o histórico, trocando apenas a ordem dos dois blocos recém adjacentes.
text = read("docs/sprints/README.md")
block = """### Continuidade do Sistema de Temas — V04

A V03 foi efetivamente integrada pelo PR #16 no commit `b83a7cde`. A [V04](sistema_temas/V04/README.md) é a candidata corrente para componentes HTML, estilos compartilhados e tabela pandas. O caminho novo é opt-in e não altera automaticamente consumidores legados; aceite, merge e homologação Databricks continuam separados.

"""
para = "A [V03](sistema_temas/V03/README.md) recebeu aceite explícito de Rodrigo e teve sua integração Git autorizada pelo PR #16. Ela acrescenta apenas um adaptador Plotly opt-in, preserva o caminho legado por padrão e não migra consumidores existentes. O estado efetivo do merge é registrado na PR. Não houve publicação Databricks; homologação operacional, auditoria independente e avaliação com usuário iniciante permanecem pendentes."
if block + para not in text:
    raise SystemExit("docs/sprints/README.md: ordem V04/V03 inesperada")
write("docs/sprints/README.md", text.replace(block + para, para + "\n\n" + block.rstrip(), 1))

# ---------------------------------------------------------------------------
# Gate, changelog e Manual.
# ---------------------------------------------------------------------------
replace_once(
    "tools/ci_local.py",
    "1. Temas — adaptador Plotly V03 + núcleo V02 + contrato V01 (todas as `test_temas*.py`)",
    "1. Temas — HTML/tabelas V04 + Plotly V03 + núcleo V02 + contrato V01 (todas as `test_temas*.py`)",
)
replace_once(
    "tools/ci_local.py",
    '"temas", "Contrato/implementação do sistema de temas V03 + V02 + V01",',
    '"temas", "Sistema de temas V04 + V03 + V02 + V01",',
)

changelog_entry = """## 2026-09-12 — V04: componentes HTML e tabelas opt-in (Codex)

### Adicionado

- (Codex) `get_styles_resolvidos(theme)` materializa CSS de notebook a partir do `ResolvedTheme` revalidado, sem CSS livre ou estado global.
- (Codex) Variantes `_resolvido` para badges, divisores, KPI card HTML, cabeçalho de seção, índice EDA e tabela pandas.
- (Codex) Suíte V04 com 29 casos e workflow permanente somente leitura.

### Atualizado

- (Codex) Componentes cobertos usam `constants.styles` no caminho V04; APIs legadas, cortes de score, conteúdo, ordem e dados permanecem preservados.
- (Codex) Notebook/READMEs dos objetos, guia operacional, Manual e índices documentam o uso opt-in e os limites de `dark`/`high_contrast`.
- (Codex) Gate `temas` continua descobrindo todas as `test_temas*.py`, agora descrito até V04.

### Notas

- (Codex) Code-check `34726526972` permanece FAILURE: V04/temas/V00 passaram, mas checkout raso e notebook `styles` não exercitando a nova API reprovaram o validador.
- (Codex) Code-check corrigido `34726621227`: 29 V04, 298 temas V01–V04, 12 V00 e `validate_assistant` aprovados.
- (Codex) V04 é candidata: sem aceite, merge, publicação Databricks, homologação visual/acessibilidade ou início da V05.

"""
replace_once(
    "CHANGELOG.md",
    "entre parênteses. Template: `.claude/templates/changelog-entry.md`.\n\n",
    "entre parênteses. Template: `.claude/templates/changelog-entry.md`.\n\n" + changelog_entry,
)

manual_path = "ambiente_fonte/.assistant/MANUAL_TECNICO.md"
manual = read(manual_path)
manual_marker = "## Sistema de Temas — V04 (candidata)"
if manual_marker in manual:
    raise SystemExit("Manual já contém seção V04 inesperada")
manual_add = """

---

## Sistema de Temas — V04 (candidata)

A V04 estende o tema validado aos componentes HTML e à tabela pandas sem mudar o
caminho atual por padrão. As funções históricas continuam válidas. Para usar o
tema, carregue/resolva um contexto `notebook` pelo núcleo V02 e escolha a função
`_resolvido` correspondente.

| Objeto | API V04 opt-in |
|---|---|
| `constants.styles` | `get_styles_resolvidos(theme)` |
| `visual.badge` | `badge_status_resolvido`, `badge_score_resolvido`, `badge_inline_resolvido` |
| `visual.divider` | `divider_light_resolvido`, `divider_medium_resolvido`, `divider_heavy_resolvido`, `divider_section_resolvido` |
| `visual.kpi_card` | `kpi_card_html_resolvido` |
| `visual.section_header` | `section_header_html_resolvido` |
| `visual.index_generator` | `gerar_indice_eda_resolvido` |
| `display.dataframe_styled` | `display_styled_resolvido` |

A referência notebook reproduz a aparência histórica. O caminho resolvido
revalida o `ResolvedTheme`, recusa dicionário cru e contexto não-notebook e não
mantém tema global. `dark` e `high_contrast` podem ser materializados pelos
componentes HTML quando a configuração é válida, mas isso não equivale a
homologação de acessibilidade nem de renderização no Databricks.

Não migre chamadas existentes em massa nesta sprint. Não há publicação,
seletor, Visual Lab ou aprovação operacional de tema. Consulte
`hub_padroes/identidade_visual/GUIA_OPERACIONAL.md` e
`docs/sprints/sistema_temas/V04/README.md` no repositório de manutenção.
"""
write(manual_path, manual.rstrip() + manual_add + "\n")

# Checkpoint só vira candidata técnica se este conjunto chegar a um commit após
# os gates do workflow. O próprio workflow não fará push em caso de falha.
replace_once(
    "docs/sprints/sistema_temas/V04/CHECKPOINT_V04.md",
    "| Implementação funcional | EM VALIDAÇÃO |\n| Regressões automatizadas | EM VALIDAÇÃO |\n| Documentação operacional | EM CONSTRUÇÃO |",
    "| Implementação funcional | CANDIDATA |\n| Regressões automatizadas | CANDIDATA — exige run final verde |\n| Documentação operacional | CANDIDATA |",
)

print("V04: reconciliação documental preparada com sucesso")
