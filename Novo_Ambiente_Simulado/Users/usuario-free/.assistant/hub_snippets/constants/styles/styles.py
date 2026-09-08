"""Estilos CSS compartilhados para displayHTML em notebooks Databricks.

**Nenhum módulo da biblioteca importa este arquivo.** Uma auditoria da Sprint 9
mediu: as constantes daqui são cópia byte a byte de CSS que vive inline em
`visual/badge`, `visual/divider`, `visual/kpi_card`, `visual/section_header` e
`visual/index_generator`. Editar `STYLE_SECTION_HEADER` **não muda cabeçalho
nenhum** — e um notebook chegou a afirmar o contrário.

O que mudou em 2026-08-18: as cores institucionais deixaram de ser literais e
passam a derivar de `constants.colors`, que é a fonte única. O CSS continua
duplicado, porque unificá-lo mexeria na saída de cinco módulos e é decisão de
produto, não higiene — está registrado em `PLANO_HUB.md` §12.2.

Use este módulo quando quiser o CSS pronto num notebook seu. Não presuma que ele
governa o que a biblioteca renderiza.
"""

from hub_snippets.constants import colors

FONT_FAMILY = "Segoe UI, Roboto, sans-serif"

STYLE_SECTION_HEADER = (
    f"background:{colors.BG_SECTION}; border-left:4px solid {colors.AZUL_CAIXA}; padding:12px 16px; "
    "margin:8px 0 12px 0; border-radius:4px; font-family:Segoe UI, Roboto, sans-serif;"
)

STYLE_KPI_CARD = (
    f"display:inline-block; background:{colors.BG_HEADER}; padding:4px 10px; border-radius:12px; "
    f"font-size:12px; margin-right:8px; color:{colors.TEXTO_PRINCIPAL}; font-family:Segoe UI, Roboto, sans-serif;"
)

# `#D9DEE3`, `#BFC7D1` e as seis cores de badge abaixo **não existem** em
# `constants.colors`: são uma paleta de estado inventada aqui e em `visual/badge`,
# e promovê-las a constante oficial é decisão de produto, não unificação.
STYLE_DIVIDER_LIGHT = "border:none; border-top:1px solid #D9DEE3; margin:10px 0;"
STYLE_DIVIDER_HEAVY = f"border:none; border-top:2px solid {colors.AZUL_CAIXA}; margin:18px 0;"
STYLE_BADGE_OK = "display:inline-block; background:#EAF7EC; color:#2E7D32; padding:2px 8px; border-radius:10px; font-size:11px;"
STYLE_BADGE_WARN = "display:inline-block; background:#FFF8E1; color:#B26A00; padding:2px 8px; border-radius:10px; font-size:11px;"
STYLE_BADGE_FAIL = "display:inline-block; background:#FDECEC; color:#B71C1C; padding:2px 8px; border-radius:10px; font-size:11px;"
STYLE_INDEX_ITEM = f"margin:6px 0; padding:6px 10px; background:{colors.BG_SECTION}; border-radius:6px;"
