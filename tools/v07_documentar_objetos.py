"""Migração transitória dos READMEs tocados pela V07.

Insere uma nota operacional imediatamente após o marcador readme-objeto, sem
reescrever o histórico do documento. Fonte e ambiente simulado precisam estar
idênticos antes da mudança e recebem exatamente os mesmos bytes depois dela.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ambiente_fonte/.assistant"
MIRROR = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free/.assistant"
MARKER = "<!-- readme-objeto: 1.0.0 -->"
V07_MARKER = "<!-- sistema-temas-v07: consumidores -->"

BLOCKS = {
    "hub_snippets/visual/theme_plotly/README.md": """
<!-- sistema-temas-v07: consumidores -->
> **Atualização V07 — estado atual.** Além das rotas V03, `theme_plotly` agora
> expõe `get_tokens_plotly(theme)`: ele revalida o `ResolvedTheme` pelas mesmas
> guardas de `notebook/light` e devolve uma **cópia** dos tokens para consumidores
> que precisam de semânticas específicas, como `palette.curves_legacy`,
> `palette.sequential` ou `semantic.warning`. A função não registra template nem
> altera `pio.templates.default`. A V07 também migrou explicitamente
> `correlation_matrix` e `distribution_grid`; referências abaixo que os descrevem
> como consumidores apenas legados registram o estado histórico da V03.
""",
    "hub_snippets/display/correlation_matrix/README.md": """
<!-- sistema-temas-v07: consumidores -->
> **Atualização V07 — estado atual.** `plot_correlation` e
> `plot_correlation_matrix` continuam sendo as rotas legadas. Para aplicar um
> `ResolvedTheme` notebook/light de forma opt-in, use
> `plot_correlation_resolvido` ou `plot_correlation_matrix_resolvido`. A rota
> temática usa `palette.sequential` somente na escala de cor; seleção de colunas,
> descarte de faltantes, cálculo Spark, método e `strong_pairs` permanecem na
> mesma implementação. Um tema inválido falha antes do cálculo.
""",
    "hub_snippets/display/distribution_grid/README.md": """
<!-- sistema-temas-v07: consumidores -->
> **Atualização V07 — estado atual.** As rotas legadas `plot_distributions` e
> `plot_distribution_grid` permanecem disponíveis. Para aparência derivada de um
> `ResolvedTheme`, use `plot_distributions_resolvido` ou
> `plot_distribution_grid_resolvido`. O tema é validado antes da amostragem;
> `smart_sample`, conversão para pandas, colunas e valores dos histogramas não têm
> uma segunda implementação. A V07 não transforma a amostra em evidência da
> população inteira nem homologa a renderização no browser Databricks.
""",
    "hub_snippets/ml/curves_plotly/README.md": """
<!-- sistema-temas-v07: consumidores -->
> **Atualização V07 — estado atual.** Cada curva legada possui agora uma rota
> opt-in `*_resolvido`: ROC, Precision–Recall, Lift e KS. A aparência usa o token
> dedicado `palette.curves_legacy`, preservando a decisão do contrato V01 de
> manter a família histórica de seis cores separada da paleta categórica geral.
> AUC, AP, lift, KS, eixos e séries continuam calculados pela mesma lógica. A
> figura Plotly resolvida pode ser serializada localmente para HTML; PNG Plotly,
> PDF e PPTX não são formatos homologados pela V07.
""",
    "hub_snippets/ml/performance_monitor/README.md": """
<!-- sistema-temas-v07: consumidores -->
> **Atualização V07 — estado atual.** `PerformanceMonitor.plot_timeline(metric)`
> continua legado. `plot_timeline_resolvido(metric, theme)` reutiliza exatamente
> o mesmo histórico, baseline e thresholds e altera apenas aparência:
> `brand.primary` para a série, `text.secondary` para baseline,
> `semantic.warning` para warning e `semantic.negative` para critical. A rota
> temática não altera `should_retrain`, não recalibra a política e não autoriza
> retreino automático.
""",
    "hub_snippets/ml/umap_viz/README.md": """
<!-- sistema-temas-v07: consumidores -->
> **Atualização V07 — estado atual.** `plot_umap_clusters` permanece a rota
> legada. `plot_umap_clusters_resolvido(..., theme)` valida o tema antes do
> cálculo, chama o mesmo `compute_umap` e troca somente paleta/layout. Coordenadas,
> labels, opacidade e tamanho solicitado não são recalculados por uma segunda
> lógica. `umap-learn` continua importado de forma lazy; selecionar um tema não
> instala dependências nem prova estabilidade dos clusters.
""",
    "hub_snippets/ml/vintage_analysis/README.md": """
<!-- sistema-temas-v07: consumidores -->
> **Atualização V07 — estado atual.** `build_vintage_table` e `compare_safras`
> continuam sem lógica de tema. Para as figuras, V07 adiciona
> `plot_vintage_curves_resolvido` (usa `palette.categorical`) e
> `plot_vintage_heatmap_resolvido` (usa `palette.sequential`). As duas rotas
> reutilizam os mesmos pontos/matriz das funções legadas: MOB, maturidade,
> denominadores, taxas, cobertura e células `NaN` não são alterados pela
> aparência.
""",
}


def patch(text: str, block: str, relative: str) -> str:
    if V07_MARKER in text:
        return text
    if text.count(MARKER) != 1:
        raise SystemExit(f"{relative}: marcador readme-objeto count={text.count(MARKER)}")
    return text.replace(MARKER, MARKER + "\n" + block.strip("\n"), 1)


def main() -> int:
    changed = []
    for relative, block in BLOCKS.items():
        source = SOURCE / relative
        mirror = MIRROR / relative
        source_text = source.read_text(encoding="utf-8")
        mirror_text = mirror.read_text(encoding="utf-8")
        if source_text != mirror_text:
            raise SystemExit(f"{relative}: fonte e simulado divergiam antes da migração")
        updated = patch(source_text, block, relative)
        source.write_text(updated, encoding="utf-8")
        mirror.write_text(updated, encoding="utf-8")
        if updated != source_text:
            changed.append(relative)
    print(f"V07_READMES_UPDATED={len(changed)}")
    for item in changed:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
