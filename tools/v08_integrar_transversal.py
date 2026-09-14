"""Migração transitória V08 — integra skills, padrões e Manual ao Sistema de Temas.

O script é deliberadamente fail-closed: cada marcador deve existir exatamente uma
vez e toda superfície .assistant alterada precisa coincidir com o ambiente
simulado antes da edição. Ele não altera módulos runtime.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ambiente_fonte/.assistant"
MIRROR = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free/.assistant"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one occurrence, found {count}")
    return text.replace(old, new, 1)


def insert_before(text: str, marker: str, block: str, label: str) -> str:
    return replace_once(text, marker, block.rstrip() + "\n\n" + marker, label)


def regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE | re.DOTALL)
    if count != 1:
        raise SystemExit(f"{label}: regex matches={count}")
    return updated


def patch_pair(relative: str, transform) -> None:
    source = SOURCE / relative
    mirror = MIRROR / relative
    source_text = source.read_text(encoding="utf-8")
    mirror_text = mirror.read_text(encoding="utf-8")
    if source_text != mirror_text:
        raise SystemExit(f"{relative}: source/simulated diverged before V08")
    updated = transform(source_text)
    source.write_text(updated, encoding="utf-8")
    mirror.write_text(updated, encoding="utf-8")


def patch_assistant_readme(text: str) -> str:
    new = """### 🎨 Sistema de Temas — V00–V07 integradas no Git

O Sistema de Temas possui um núcleo validado (`ResolvedTheme`), adaptadores opt-in para Plotly e HTML, Visual Lab de autoria em notebook, geração editorial orientada por tema e consumidores runtime integrados em `display`/`ml`. **Nada disso troca automaticamente o padrão da equipe nem publica um tema.**

Para autoria e comparação, comece pelo [Visual Lab](hub_snippets/visual/theme_lab/README.md). Para contrato, tokens, primeiro uso e limites, consulte o [padrão de identidade visual](hub_padroes/identidade_visual/README.md). Para um consumidor concreto, abra o README local e use a rota `_resolvido` quando ela existir.

A V07 integrou, entre outros, correlação, distribuições, curvas de ML, timeline de monitoramento, UMAP e safras. `dataframe_styled` já era coberto pela V04. SHAP/Matplotlib e Kaplan–Meier permanecem exceções explícitas ao theming atual; selecionar um tema não autoriza afirmar que seus plots foram recoloridos.

Integração Git não equivale a publicação no workspace, aprovação visual, acessibilidade, ACL real ou UAT. A V08 organiza transversalmente essas orientações em skills, padrões e Manual sem criar uma segunda fonte de verdade.

"""
    pattern = r"^### 🎨 Visual Lab do Sistema de Temas — V05 candidata\n.*?(?=^> \*\*INFRAESTRUTURA EDITORIAL DO HUB\.\*\*)"
    return regex_once(text, pattern, new, "assistant README theme section")


def patch_skills_readme(text: str) -> str:
    text = replace_once(
        text,
        "- **Gabaritos de Estilo Visual**, como `estilo_visual_eda.md`: orientam paleta, hierarquia e leitura de gráficos.",
        "- **Gabaritos de Estilo Visual**, como `estilo_visual_eda.md`: orientam composição, hierarquia e leitura; paletas e tokens configuráveis pertencem ao `ResolvedTheme` e ao padrão `hub_padroes/identidade_visual`, não ao template da skill.",
        "skills README visual template bullet",
    )
    block = """## 🎨 Skills e Sistema de Temas

Skills podem **recomendar** consumidores visuais, mas não são fonte de paleta, token ou aprovação. Quando uma tarefa pedir identidade visual, tema ou consistência entre gráficos:

1. trate `hub_padroes/identidade_visual` e `ResolvedTheme` como fontes canônicas;
2. use a rota `_resolvido` do consumidor quando ela existir;
3. mantenha dados, métricas, thresholds e decisões analíticas independentes da aparência;
4. não presuma publicação ou homologação no Databricks;
5. preserve limites declarados — por exemplo, SHAP/Matplotlib e Kaplan–Meier não possuem theming V07 homologado.

`estilo_visual_eda.md` continua útil para decisões **editoriais da EDA** (estrutura, escolha de gráfico, anotações e leitura), mas não pode redeclarar a paleta do Hub.
"""
    return insert_before(text, '<a id="estrutura-de-uma-skill-profissional"></a>', block, "skills README theme section")


def patch_concierge(text: str) -> str:
    block = """### 3.1. Rota específica para tema e identidade visual

Quando o pedido mencionar tema, identidade visual, paleta, Visual Lab, aparência de gráficos ou consistência visual, não trate um template de skill nem `constants.colors` como fonte configurável. Verifique primeiro `HUB_ROOT/hub_padroes/identidade_visual/README.md` e a seção vigente do Sistema de Temas no Manual.

- autoria/comparação em notebook: `hub_snippets.visual.theme_lab`;
- Plotly: `hub_snippets.visual.theme_plotly` e rotas `_resolvido` dos consumidores;
- HTML/tabelas: rotas `_resolvido` documentadas pelos componentes V04;
- assets editoriais: contrato V06, sem promoção automática;
- consumidores V07: confirmar a função `_resolvido` concreta antes de recomendar.

Explicite limites: **SHAP/Matplotlib** e **Kaplan–Meier** permanecem exceções ao theming V07. Um tema válido não significa publicado, aprovado ou homologado no browser Databricks. Se a solicitação for somente escolher cores, encaminhe ao fluxo de autoria/contrato em vez de inventar uma paleta na resposta.
"""
    return insert_before(text, "### 4. Verificar antes de recomendar", block, "concierge visual route")


def patch_create_object(text: str) -> str:
    block = """#### Sistema de Temas em objetos visuais

Ao criar um objeto que aceite aparência configurável, não invente `TEMA_*`, paleta local ou JSON paralelo. Consulte `hub_padroes/identidade_visual`, receba/propague um `ResolvedTheme` quando o contrato do objeto exigir theming e reutilize o adaptador/consumidor `_resolvido` existente.

`hub_snippets.constants.colors` continua válido para **compatibilidade legada** e componentes não configuráveis que já dependem dessas constantes; ele não é a fonte de um tema novo. Não altere cálculo, threshold, agregação ou amostragem para fazer uma proposta visual funcionar. Não registre template global como efeito padrão de um objeto novo.
"""
    text = insert_before(text, "### 6. Escrever o notebook, que não é opcional", block, "create-object theme rules")
    text = replace_once(
        text,
        "| Tema visual e rodapé com a contagem de pontos | `hub_snippets.visual.theme_plotly` |\n| Paleta e cores semânticas | `hub_snippets.constants.colors` |",
        "| Tema visual configurável e rodapé | `hub_snippets.visual.tema`, `hub_snippets.visual.theme_plotly` |\n| Cores institucionais legadas | `hub_snippets.constants.colors` — compatibilidade legada; não é fonte de tema novo |",
        "create-object helper table",
    )
    return text


def patch_eda_skill(text: str) -> str:
    text = replace_once(
        text,
        "Consultar [templates/estilo_visual_eda.md](templates/estilo_visual_eda.md) apenas para orientação visual customizada, não como API nativa Databricks.",
        "Consultar [templates/estilo_visual_eda.md](templates/estilo_visual_eda.md) para composição e leitura da EDA. Paleta/tokens configuráveis vêm de `ResolvedTheme` e do padrão `hub_padroes/identidade_visual`; o template não é uma segunda fonte de tema.",
        "eda skill template role",
    )
    block = """Quando um tema notebook validado tiver sido selecionado, mantenha a mesma análise e use as rotas opt-in: `plot_correlation_resolvido`, `plot_distributions_resolvido` e `aplicar_tema_resolvido`/outro consumidor `_resolvido` aplicável. Sem tema selecionado, preserve as APIs legadas. `ResolvedTheme` muda aparência coberta pelo contrato; não muda agregação Spark, amostra, denominador ou interpretação.

"""
    return replace_once(text, "`quick_profile` distingue", block + "`quick_profile` distingue", "eda skill resolved routes")


def new_eda_visual_template(_: str) -> str:
    return """# Estilo Visual — EDA Profissional sobre o Sistema de Temas

Este template orienta **composição, hierarquia e leitura** de uma EDA. Ele não é fonte de paleta, token ou aprovação. As escolhas configuráveis pertencem ao contrato `hub_padroes/identidade_visual` e chegam ao consumidor por `ResolvedTheme`.

## 1. Fonte de verdade visual

- Não declare `PALETA_EDA`, `TEMA_EDA` ou dicionário paralelo de tema.
- Não copie valores de `TOKENS.md` para “congelar” uma aparência local.
- Não registre template global como preparação padrão do notebook; **não registre template global** apenas para aplicar uma proposta.
- Se não houver tema explicitamente selecionado, use as APIs legadas do Hub.
- Se houver tema notebook válido, use as rotas `_resolvido` do consumidor.

Fluxo mínimo para uma figura Plotly genérica:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido

tema = load_reference_theme("notebook")
fig = ...  # mesmos dados, agregações e eixos da análise
aplicar_tema_resolvido(fig, tema, subtitulo="Recorte analisado", n=n_amostra)
fig.show()
```

Para componentes especializados, prefira a própria rota resolvida, por exemplo `plot_correlation_resolvido`, `plot_distributions_resolvido`, curvas `*_resolvido`, `plot_vintage_curves_resolvido` ou `plot_timeline_resolvido`. Isso evita reconstruir semântica de cor no notebook.

## 2. O que o tema pode e não pode mudar

O tema pode controlar propriedades visuais cobertas pelo contrato, como tipografia, dimensões, margens, paletas e cores semânticas. Ele **não** muda:

- filtro, população ou data de corte;
- amostragem, seed ou agregação;
- bins, denominadores e unidade;
- threshold analítico ou política de monitoramento;
- métrica, modelo ou conclusão de negócio.

Aparência consistente não valida a análise.

## 3. Escolha de gráficos

| Tipo de dado/pergunta | Visual sugerido | Cuidados |
| --- | --- | --- |
| numérica univariada | histograma, ECDF ou box plot | declarar amostra/agregação |
| categórica | barras ordenadas | mostrar denominador, top-N e cauda |
| temporal | linha em frequência regular | rotular janela e gaps |
| associação numérica | scatter/agregado ou correlação | sinal não implica causalidade |
| matriz com centro significativo | heatmap divergente | preservar centro e domínio |
| comparação de segmentos | small multiples ou barras | manter escala comparável |

Use Plotly para gráficos do relatório quando a interatividade ajudar. Visualização nativa pode ser melhor para exploração ou agregações que devem ficar no backend. Matplotlib permanece válido para casos estáticos específicos, mas não herda automaticamente o Sistema de Temas Plotly.

## 4. Anotações e rodapé

Todo gráfico material deve deixar explícitos, quando aplicável:

- N amostral ou volume agregado;
- fonte/snapshot;
- janela, segmento ou recorte;
- unidade e denominador;
- uma anotação de destaque somente quando houver achado realmente sustentado.

Não transforme anotação em conclusão causal. Em rotas Plotly do Hub, use os argumentos de rodapé do adaptador/consumidor em vez de criar um segundo estilo.

## 5. Hierarquia do notebook

- `#`: título único do notebook;
- `##`: etapas principais;
- `###`: subseções/resultados;
- `####`: tópicos internos quando necessários.

Evite profundidade excessiva. Emojis são semânticos e limitados; não substituem títulos informativos.

## 6. Números e tabelas

Formate números com `hub_snippets.constants.format_br` quando o público exigir padrão brasileiro. Não implemente formatação monetária/percentual em vários pontos do notebook.

Em tabelas Markdown:

- prefira até seis colunas por bloco legível;
- alinhe números à direita quando a superfície permitir;
- use nomes técnicos em backticks;
- destaque somente o que possui significado analítico;
- não esconda denominador ou unidade.

## 7. Componentes HTML e seções

Para índice, cabeçalho, badges, divisores e KPI cards, prefira os helpers `hub_snippets.visual`. Se houver um `ResolvedTheme`, use a rota `_resolvido` correspondente quando documentada. Não monte CSS/HTML manual apenas para contornar os componentes V04.

Uma célula pós-código pode resumir poucos KPIs materiais em uma linha de leitura rápida, mas o valor precisa vir da saída observada. Não invente número para completar layout.

## 8. Consumidores com limite explícito

- SHAP/Matplotlib: o theming V07 não cobre sua aparência interna nem o PNG salvo pelo helper.
- Kaplan–Meier: permanece com a ordem visual legada até existir token que represente sua semântica sem remapeamento silencioso.

Não prometa consistência temática para essas superfícies apenas porque o restante do notebook usa `ResolvedTheme`.

## 9. Referências do Hub

| Necessidade | Fonte/consumidor |
| --- | --- |
| contrato e primeiro uso | `hub_padroes/identidade_visual/README.md` e `GUIA_OPERACIONAL.md` |
| carregar/validar tema | `hub_snippets.visual.tema` |
| aplicar tema Plotly | `hub_snippets.visual.theme_plotly.aplicar_tema_resolvido` |
| correlação | `hub_snippets.display.correlation_matrix.plot_correlation_resolvido` |
| distribuições | `hub_snippets.display.distribution_grid.plot_distributions_resolvido` |
| índice/cabeçalho/cards | rotas `_resolvido` dos componentes `hub_snippets.visual` |
| autoria/comparação | `hub_snippets.visual.theme_lab` |

O template EDA organiza a apresentação. A fonte de verdade do tema permanece fora desta skill.
"""


def patch_baseline(text: str) -> str:
    block = """Se um `ResolvedTheme` notebook tiver sido selecionado para a entrega, as curvas podem usar `plot_roc_curve_resolvido`, `plot_pr_curve_resolvido`, `plot_lift_curve_resolvido` e `plot_ks_curve_resolvido`. Isso é somente aparência: métricas, probabilidades, thresholds e a seleção do modelo continuam definidos pelo fluxo analítico, não pelo tema.

"""
    return replace_once(text, "`temporal_split` e `walk_forward_cv`", block + "`temporal_split` e `walk_forward_cv`", "baseline theme boundary")


def patch_vintage(text: str) -> str:
    block = """Com um `ResolvedTheme` notebook explicitamente selecionado, use `plot_vintage_curves_resolvido` e `plot_vintage_heatmap_resolvido`. Essas rotas mudam paleta/layout, não MOB, denominador, maturidade, cobertura ou taxa. Sem tema selecionado, mantenha as funções legadas.

"""
    return replace_once(text, "`build_vintage_table` calcula", block + "`build_vintage_table` calcula", "vintage theme boundary")


def patch_monitoring(text: str) -> str:
    block = """Se a entrega usar um `ResolvedTheme` notebook validado, `PerformanceMonitor.plot_timeline_resolvido` e as curvas `*_resolvido` podem ajustar a aparência. O tema não recalibra threshold, baseline, direção da métrica, status nem decisão de retreino; política e evidência continuam independentes da camada visual.

"""
    return replace_once(text, "`interpretar_psi` só classifica", block + "`interpretar_psi` só classifica", "monitoring theme boundary")


def patch_explainability(text: str) -> str:
    block = """Para curvas diagnósticas Plotly auxiliares, um tema notebook validado pode ser aplicado pelas rotas como `plot_roc_curve_resolvido`. **SHAP/Matplotlib é uma exceção explícita:** o Sistema de Temas V07 não controla o estilo interno dos plots SHAP nem o PNG salvo por `shap_explainer`. Não prometa recoloração/consistência temática dessas figuras apenas porque o notebook usa `ResolvedTheme` em outros gráficos.

"""
    return replace_once(text, "`shap` é dependência opcional", block + "`shap` é dependência opcional", "explainability theme boundary")


def patch_patterns_index(text: str) -> str:
    old = """## Sistema de Temas

O [padrão de identidade visual](identidade_visual/README.md) define configurações
completas e sua validação. É transversal, não um sétimo tipo de objeto. V02 integra o núcleo; V03 e V04 acrescentam consumidores opt-in. Não há painel, tema global, migração automática de notebooks ou publicação implícita.
"""
    new = """## Sistema de Temas

O [padrão de identidade visual](identidade_visual/README.md) é o contrato transversal; não é um sétimo tipo de objeto. `ResolvedTheme` é a representação validada. V03/V04 integram consumidores Plotly/HTML, V05 fornece o Visual Lab opt-in, V06 conecta geração editorial e V07 amplia os consumidores runtime e formatos exercitados.

Templates e skills podem orientar composição, mas não redeclaram tokens ou paletas. Para um objeto visual configurável novo, use o contrato central e a rota `_resolvido` aplicável. Não há tema global automático, migração silenciosa de notebooks ou publicação implícita.
"""
    return replace_once(text, old, new, "patterns theme section")


def patch_identity_readme(text: str) -> str:
    text = replace_once(
        text,
        "> **PADRÃO TRANSVERSAL DO HUB · V02 INTEGRADA; CONSUMO OPT-IN ATÉ V04.** Não é um novo tipo de objeto,\n> App ou configuração ativa de todos os notebooks. Nada muda na rotina legada.",
        "> **PADRÃO TRANSVERSAL DO HUB · V02–V07 INTEGRADAS NO GIT.** Não é um novo tipo de objeto,\n> App ou configuração ativa de todos os notebooks. Consumo e autoria continuam opt-in; nada muda silenciosamente na rotina legada.",
        "identity header",
    )
    old_state = "**Estado vigente no Git:** V02 integrou o núcleo de carga/validação/resolução; V03 acrescentou o adaptador Plotly opt-in; V04 estendeu a mesma arquitetura aos componentes HTML, estilos compartilhados e tabela pandas por rotas `_resolvido`. As APIs legadas permanecem o default. Integração Git não equivale a publicação no workspace, homologação visual/runtime, acessibilidade ou aprovação de uma identidade."
    new_state = "**Estado vigente no Git:** V02 integrou o núcleo de carga/validação/resolução; V03 o adaptador Plotly; V04 componentes HTML/tabela; V05 o Visual Lab de autoria; V06 a geração editorial orientada por tema; V07 consumidores runtime e formatos exercitados. `ResolvedTheme` permanece a fonte efetiva para consumo configurável e as APIs legadas continuam o default. Integração Git não equivale a publicação no workspace, homologação visual/runtime, acessibilidade ou aprovação de uma identidade."
    text = replace_once(text, old_state, new_state, "identity current state")
    return replace_once(
        text,
        "separados; V00–V04 integradas no Git não oferecem, por si só, comando ou autorização para publicar um tema.",
        "separados; V00–V07 integradas no Git não oferecem, por si só, comando ou autorização para publicar um tema.",
        "identity integrated range",
    )


def patch_operational_guide(text: str) -> str:
    old = """O núcleo V02 está integrado no Git como verificador com exemplo guiado, não como painel de cores. V03 e V04 acrescentam consumidores opt-in, sem trocar o caminho legado por padrão.
Seu notebook atual continua igual. Para usar o pacote no workspace de trabalho, a revisão integrada ainda precisa ser instalada/publicada pelo procedimento autorizado e homologada no destino. Não publique arquivos por conta própria para experimentar uma cor.
"""
    new = """O núcleo V02 está integrado no Git como verificador/resolvedor. V03/V04 acrescentam consumidores Plotly/HTML opt-in; V05 oferece o Visual Lab; V06 integra geração editorial; V07 amplia consumidores runtime e formatos exercitados. Nenhuma dessas camadas troca o caminho legado por padrão.
Seu notebook atual continua igual. Para usar o pacote no workspace de trabalho, a revisão integrada ainda precisa ser instalada/publicada pelo procedimento autorizado e homologada no destino. Não publique arquivos por conta própria para experimentar uma cor.
"""
    text = replace_once(text, old, new, "operational intro")
    text = replace_once(
        text,
        "Não confunda `export_theme` com salvar: ele devolve bytes em memória. Salvar em\numa pasta, compartilhar, aprovar e publicar são ações distintas. Essas operações permanecem fora de V00–V04 integradas; uma etapa futura só pode ser considerada disponível quando estiver efetivamente integrada e homologada no escopo correspondente.",
        "Não confunda `export_theme` com salvar: ele devolve bytes em memória. Salvar em\numa pasta, compartilhar, aprovar e publicar são ações distintas. V05 pode persistir sessão/proposta em pasta autorizada e V06 pode gerar variantes editoriais candidatas, mas nenhuma dessas ações equivale a aprovar ou publicar um tema. Publicação e homologação no workspace continuam gates separados.",
        "operational save boundary",
    )
    block = """## Usar o Visual Lab V05

Para editar/comparar uma proposta sem mudar o padrão da equipe, abra `hub_snippets.visual.theme_lab`. Ele parte de configuração notebook validada, aplica alterações de forma atômica e compara Atual/Proposta com dados sintéticos. Salvar uma sessão preserva trabalho; não publica nem aprova o tema.

## Usar consumidores V07

Quando um consumidor documentar uma rota `_resolvido`, carregue primeiro um `ResolvedTheme` íntegro e passe-o explicitamente. Exemplos incluem `plot_correlation_resolvido`, `plot_distributions_resolvido`, curvas de ML, timeline de monitoramento, UMAP e safras. A rota temática muda somente propriedades visuais cobertas; dados, agregações, amostragem, métricas e thresholds permanecem os mesmos.

SHAP/Matplotlib e Kaplan–Meier continuam exceções explícitas ao theming atual. Não assuma suporte apenas porque outras figuras do notebook usam um tema.

## Geração editorial V06

A geração orientada por tema recebe um derivado controlado do `ResolvedTheme` e produz candidatos fora do pacote visual ativo. Gerar um asset não o promove. Preserve hashes/recursos congelados e siga o fluxo de revisão antes de qualquer substituição.

"""
    return insert_before(text, "## Para pedir ajuda", block, "operational V05-V07 sections")


MANUAL_SECTION = """## Sistema de Temas — V00–V07 integradas no Git

O Sistema de Temas está integrado no repositório até a V07. Isso significa que o contrato, os adaptadores e consumidores descritos abaixo existem no produto versionado; **não** significa que um tema tenha sido publicado no workspace, aprovado visualmente ou homologado em browser/acessibilidade.

### Camadas e responsabilidade

- **V02 — núcleo:** carrega, valida e resolve configurações completas em `ResolvedTheme`. Não aplica nem aprova aparência.
- **V03 — Plotly:** `aplicar_tema_resolvido` e registro explícito de template; sem efeito global por import.
- **V04 — HTML/tabelas:** componentes `_resolvido` e estilos derivados do mesmo tema.
- **V05 — Visual Lab:** autoria/comparação opt-in em notebook, com sessão e histórico; não publica.
- **V06 — assets/geração:** renderização editorial orientada por tema em área candidata; geração não promove asset.
- **V07 — consumidores/formatos:** correlação, distribuições, curvas de ML, monitoramento, UMAP e safras recebem rotas temáticas explícitas; HTML Plotly local foi exercitado.

A fonte canônica de campos/limites está em `hub_padroes/identidade_visual/theme.schema.json`; a referência de tokens é `TOKENS.md`. Skills e templates podem orientar uso e composição, mas não devem copiar paletas para criar uma segunda política visual.

### Fluxo recomendado para notebook

1. Se você só quer o comportamento histórico, use a API legada.
2. Para escolher/editar uma proposta, use o Visual Lab ou carregue uma configuração completa pela API `hub_snippets.visual.tema`.
3. Para uma figura/componente tematizável, use a rota `_resolvido` documentada pelo objeto.
4. Revise saída, dados, unidade e limites; aparência não valida o resultado analítico.
5. Trate salvar, compartilhar, aprovar e publicar como ações diferentes.

### Limites atuais

- `dark`/`high_contrast` têm cobertura diferente entre HTML e Plotly; não trate modo válido como homologação de acessibilidade.
- SHAP/Matplotlib e o PNG do helper SHAP permanecem fora do theming V07.
- Kaplan–Meier preserva aparência legada enquanto sua ordem de cores não estiver representada pelo contrato sem remapeamento silencioso.
- PNG Plotly/Kaleido, PDF, PPTX e render real no browser Databricks não foram homologados pela V07.
- Tema não muda threshold, métrica, amostra, agregação, modelo, policy ou decisão de negócio.

### V08 — integração transversal em execução

A V08 não adiciona runtime: ela reconcilia skills, padrões e este Manual para que todos apontem às mesmas fontes de verdade e limites das V02–V07. Até aceite/merge da V08, essa reconciliação deve ser tratada como candidata de documentação transversal, não como nova capacidade publicada.

Para primeiro uso, consulte `hub_padroes/identidade_visual/GUIA_OPERACIONAL.md`. Para autoria, consulte `hub_snippets/visual/theme_lab/README.md`. Para um consumidor específico, o README local continua sendo a fonte de uso daquele objeto.

"""


def patch_manual(text: str) -> str:
    pattern = r"^## Sistema de Temas —.*?(?=^## )"
    return regex_once(text, pattern, MANUAL_SECTION, "manual live theme section")


def main() -> int:
    transforms = {
        "README.md": patch_assistant_readme,
        "skills/README.md": patch_skills_readme,
        "skills/hub-ml-concierge/SKILL.md": patch_concierge,
        "skills/hub-ml-criar-objeto/SKILL.md": patch_create_object,
        "skills/hub-ml-eda-profissional/SKILL.md": patch_eda_skill,
        "skills/hub-ml-eda-profissional/templates/estilo_visual_eda.md": new_eda_visual_template,
        "skills/hub-ml-baseline-ml/SKILL.md": patch_baseline,
        "skills/hub-ml-analise-safra/SKILL.md": patch_vintage,
        "skills/hub-ml-monitoramento-modelo/SKILL.md": patch_monitoring,
        "skills/hub-ml-explainability/SKILL.md": patch_explainability,
        "hub_padroes/README.md": patch_patterns_index,
        "hub_padroes/identidade_visual/README.md": patch_identity_readme,
        "hub_padroes/identidade_visual/GUIA_OPERACIONAL.md": patch_operational_guide,
        "MANUAL_TECNICO.md": patch_manual,
    }
    for relative, transform in transforms.items():
        patch_pair(relative, transform)
        print(f"V08_UPDATED={relative}")

    canonical = (SOURCE / "MANUAL_TECNICO.md").read_bytes()
    ROOT.joinpath("MANUAL_TECNICO.md").write_bytes(canonical)
    if (MIRROR / "MANUAL_TECNICO.md").read_bytes() != canonical:
        raise SystemExit("manual simulated copy diverged after patch")
    print("V08_MANUAL_ROOT_SYNC=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
