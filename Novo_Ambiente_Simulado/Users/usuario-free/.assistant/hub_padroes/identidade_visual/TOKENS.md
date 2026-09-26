# Referência dos tokens — derivada do schema

> GERADO por `tools/temas_v01_contract.py --print-dictionary`. Não editar esta tabela separadamente.

Os defaults são amostras declarativas, não valores injetados pelo validador. O produto legado permanece independente até os adaptadores serem integrados. Nenhum controle abaixo está instalado pela V01.

## Notebook

### `brand.primary`

Cor de títulos, bordas de seção e cabeçalhos de tabela; não recolore categorias automaticamente.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#005CA9"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`; `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`; `ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/dataframe_styled.py`.
**Efeito previsto:** Cor de títulos, bordas de seção e cabeçalhos de tabela; não recolore categorias automaticamente..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:AZUL_CAIXA`.

### `brand.accent`

Destaque institucional secundário nos consumidores que já usam LARANJA.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#F7941D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/curves_plotly.py`.
**Efeito previsto:** Destaque institucional secundário nos consumidores que já usam LARANJA..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:LARANJA`.

### `text.primary`

Texto dos cartões de indicadores.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#1A1A1A"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.
**Efeito previsto:** Texto dos cartões de indicadores..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:TEXTO_PRINCIPAL`.

### `text.plot`

Texto geral dos gráficos.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#333333"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`; `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/curves_plotly.py`.
**Efeito previsto:** Texto geral dos gráficos..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:CINZA_ESCURO`.

### `text.secondary`

Descrição das seções e notas dos gráficos.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#6C757D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`; `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.
**Efeito previsto:** Descrição das seções e notas dos gráficos..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:TEXTO_SECUNDARIO`.

### `surface.section`

Fundo de cabeçalhos de seção e itens de índice.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#F8F9FA"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`; `ambiente_fonte/.assistant/hub_snippets/visual/index_generator/index_generator.py`.
**Efeito previsto:** Fundo de cabeçalhos de seção e itens de índice..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:BG_SECTION`.

### `surface.card`

Fundo de cartões e badges informativos.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#E8F4FD"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`; `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Fundo de cartões e badges informativos..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:BG_HEADER`.

### `table.header_text`

Cor de texto dos títulos de coluna.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FFFFFF"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/dataframe_styled.py`.
**Efeito previsto:** Cor de texto dos títulos de coluna..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/dataframe_styled.py:white`.

### `divider.light`

Cor do separador fino.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#D9DEE3"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/divider/divider.py`.
**Efeito previsto:** Cor do separador fino..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/divider/divider.py:divider_light`.

### `divider.medium`

Cor do separador médio.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#BFC7D1"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/divider/divider.py`.
**Efeito previsto:** Cor do separador médio..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/divider/divider.py:divider_medium`.

### `status.ok_bg`

Fundo do estado ok; não define a regra que atribui esse estado.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#EAF7EC"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Fundo do estado ok; não define a regra que atribui esse estado..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py:badge_status`.

### `status.ok_text`

Texto do estado ok.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#2E7D32"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Texto do estado ok..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py:badge_status`.

### `status.warn_bg`

Fundo do estado de alerta.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FFF8E1"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Fundo do estado de alerta..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py:badge_status`.

### `status.warn_text`

Texto do estado de alerta; legado exige avaliação de contraste.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#B26A00"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Texto do estado de alerta; legado exige avaliação de contraste..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py:badge_status`.

### `status.fail_bg`

Fundo do estado de falha.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FDECEC"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Fundo do estado de falha..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py:badge_status`.

### `status.fail_text`

Texto do estado de falha.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#B71C1C"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Texto do estado de falha..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py:badge_status`.

### `semantic.positive`

Cor de estado favorável declarado pelo consumidor, não de aumento numérico.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#8DC63F"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `avancado_amostra_sem_promessa_de_propagacao`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py`; `ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py`.
**Efeito previsto:** Cor de estado favorável declarado pelo consumidor, não de aumento numérico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:COR_POSITIVO`.

### `semantic.negative`

Cor de estado desfavorável ou destaque negativo já definido pelo consumidor.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#C4262E"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py`; `ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/dataframe_styled.py`.
**Efeito previsto:** Cor de estado desfavorável ou destaque negativo já definido pelo consumidor..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:COR_NEGATIVO`.

### `semantic.neutral`

Cor do estado neutro.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#6C757D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `avancado_amostra_sem_promessa_de_propagacao`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py`; `ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py`.
**Efeito previsto:** Cor do estado neutro..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:COR_NEUTRO`.

### `semantic.warning`

Cor de atenção; a condição analítica continua fora do tema.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FFB800"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `avancado_amostra_sem_promessa_de_propagacao`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py`; `ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py`.
**Efeito previsto:** Cor de atenção; a condição analítica continua fora do tema..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:COR_ALERTA`.

### `palette.categorical`

Paleta categórica; o mapa estável categoria/cor pertence ao consumidor.

**Unidade:** paleta. **Tipo:** array. **Default de referência:** `["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E", "#7B2D8B", "#00A79D", "#F15A29", "#A7A9AC"]`.
**Limites:** `{"minItems": 2, "maxItems": 20}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `editor_paleta_avancado`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py`; `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Paleta categórica; o mapa estável categoria/cor pertence ao consumidor..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:PALETA_CATEGORICA`.

### `palette.curves_legacy`

Paleta distinta das curvas de ML; não expandir silenciosamente para dez cores.

**Unidade:** paleta. **Tipo:** array. **Default de referência:** `["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E"]`.
**Limites:** `{"minItems": 2, "maxItems": 20}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `editor_paleta_avancado`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/curves_plotly.py`.
**Efeito previsto:** Paleta distinta das curvas de ML; não expandir silenciosamente para dez cores..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/curves_plotly.py:PALETA_CATEGORICA`.

### `palette.sequential`

Cores sequenciais, em ordem de intensidade; não altera domínio dos valores.

**Unidade:** paleta. **Tipo:** array. **Default de referência:** `["#E6F0FA", "#99C2E8", "#4D94D6", "#005CA9", "#003D73"]`.
**Limites:** `{"minItems": 2, "maxItems": 11}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `editor_paleta_avancado`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py`; `ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/vintage_analysis.py`.
**Efeito previsto:** Cores sequenciais, em ordem de intensidade; não altera domínio dos valores..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:PALETA_SEQUENCIAL`.

### `palette.diverging`

Cores divergentes; quantidade ímpar e cor central, sem definir ponto zero dos dados.

**Unidade:** paleta. **Tipo:** array. **Default de referência:** `["#C4262E", "#F7941D", "#FFB800", "#8DC63F", "#005CA9"]`.
**Limites:** `{"minItems": 3, "maxItems": 11}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `avancado_amostra_sem_promessa_de_propagacao`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py`; `ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py`.
**Efeito previsto:** Cores divergentes; quantidade ímpar e cor central, sem definir ponto zero dos dados..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py:PALETA_DIVERGENTE`.

### `font.family`

Família tipográfica por identificador permitido, sem CSS livre.

**Unidade:** id-fonte. **Tipo:** string. **Default de referência:** `"system_sans"`.
**Limites:** `{"enum": ["system_sans", "system_arial"]}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_fonte`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`; `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`; `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.
**Efeito previsto:** Família tipográfica por identificador permitido, sem CSS livre..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py:font.family`.

### `chart.font_px`

Tamanho do texto do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `12`.
**Limites:** `{"minimum": 8, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Tamanho do texto do gráfico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `chart.title_px`

Tamanho do título do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `16`.
**Limites:** `{"minimum": 12, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Tamanho do título do gráfico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `chart.footer_px`

Tamanho das notas de gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `10`.
**Limites:** `{"minimum": 8, "maximum": 24}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Tamanho das notas de gráfico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `chart.height_px`

Altura do gráfico, sem alterar seus dados.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `450`.
**Limites:** `{"minimum": 240, "maximum": 1600}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Altura do gráfico, sem alterar seus dados..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `chart.width_px`

Largura nominal do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `900`.
**Limites:** `{"minimum": 320, "maximum": 2400}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Largura nominal do gráfico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `chart.margin_left_px`

Margem esquerda do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `60`.
**Limites:** `{"minimum": 0, "maximum": 240}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Margem esquerda do gráfico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `chart.margin_right_px`

Margem direita do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `30`.
**Limites:** `{"minimum": 0, "maximum": 240}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Margem direita do gráfico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `chart.margin_top_px`

Margem superior do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `70`.
**Limites:** `{"minimum": 0, "maximum": 240}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Margem superior do gráfico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `chart.margin_bottom_px`

Margem inferior do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `60`.
**Limites:** `{"minimum": 0, "maximum": 240}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.
**Efeito previsto:** Margem inferior do gráfico..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py`.

### `section.title_px`

Tamanho do título da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `18`.
**Limites:** `{"minimum": 12, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.
**Efeito previsto:** Tamanho do título da seção..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.

### `section.description_px`

Tamanho da descrição da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `13`.
**Limites:** `{"minimum": 10, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.
**Efeito previsto:** Tamanho da descrição da seção..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.

### `section.radius_px`

Raio dos cantos da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `4`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.
**Efeito previsto:** Raio dos cantos da seção..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.

### `section.padding_y_px`

Espaçamento vertical interno da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `12`.
**Limites:** `{"minimum": 0, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.
**Efeito previsto:** Espaçamento vertical interno da seção..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.

### `section.padding_x_px`

Espaçamento horizontal interno da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `16`.
**Limites:** `{"minimum": 0, "maximum": 64}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.
**Efeito previsto:** Espaçamento horizontal interno da seção..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.

### `section.border_px`

Espessura da borda lateral de seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `4`.
**Limites:** `{"minimum": 0, "maximum": 12}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.
**Efeito previsto:** Espessura da borda lateral de seção..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py`.

### `card.font_px`

Tamanho do texto de cartão.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `12`.
**Limites:** `{"minimum": 10, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.
**Efeito previsto:** Tamanho do texto de cartão..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.

### `card.radius_px`

Raio dos cantos de cartão.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `12`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.
**Efeito previsto:** Raio dos cantos de cartão..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.

### `card.padding_y_px`

Espaçamento vertical do cartão.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `4`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.
**Efeito previsto:** Espaçamento vertical do cartão..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.

### `card.padding_x_px`

Espaçamento horizontal do cartão.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `10`.
**Limites:** `{"minimum": 0, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.
**Efeito previsto:** Espaçamento horizontal do cartão..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py`.

### `badge.font_px`

Tamanho do texto do badge.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `11`.
**Limites:** `{"minimum": 10, "maximum": 24}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Tamanho do texto do badge..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.

### `badge.radius_px`

Raio dos cantos de badge.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `10`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Raio dos cantos de badge..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.

### `badge.padding_y_px`

Espaçamento vertical de badge.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `2`.
**Limites:** `{"minimum": 0, "maximum": 24}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Espaçamento vertical de badge..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.

### `badge.padding_x_px`

Espaçamento horizontal de badge.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `8`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V03_V04`. **Contextos:** notebook.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.
**Efeito previsto:** Espaçamento horizontal de badge..
**Origem do default:** `ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py`.

## README e apresentação

### `editorial.background`

Fundo do material editorial.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#06101D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Fundo do material editorial..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.background`.

### `editorial.background_elevated`

Superfície elevada.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#0B182A"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Superfície elevada..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.background_elevated`.

### `editorial.panel`

Fundo de painéis.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#102238"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Fundo de painéis..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.panel`.

### `editorial.panel_high`

Painel em destaque.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#16304A"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Painel em destaque..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.panel_high`.

### `editorial.line`

Linhas e conectores.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#34516D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Linhas e conectores..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.line`.

### `editorial.text`

Texto principal.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#F7FAFC"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Texto principal..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.text`.

### `editorial.muted`

Texto secundário.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#B8C9DA"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Texto secundário..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.muted`.

### `editorial.quiet`

Texto de apoio discreto.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#8196AA"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Texto de apoio discreto..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.quiet`.

### `editorial.hub_custom`

Identificação de conteúdo customizado do Hub.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FF6598"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Identificação de conteúdo customizado do Hub..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.hub_custom`.

### `editorial.gradient_end`

Extremo do gradiente de fundo.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#102139"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Extremo do gradiente de fundo..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.gradient_end`.

### `editorial.atlas_core`

Núcleo da composição Atlas.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#0D2034"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Núcleo da composição Atlas..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.atlas_core`.

### `editorial.dossier_back`

Camada traseira do dossiê.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#0B1B2D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Camada traseira do dossiê..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.dossier_back`.

### `editorial.dossier_middle`

Camada intermediária do dossiê.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#112740"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Camada intermediária do dossiê..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.dossier_middle`.

### `editorial.dossier_fold`

Dobra do dossiê.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#1B3751"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Dobra do dossiê..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.dossier_fold`.

### `editorial.databricks_native`

Identificação de recurso nativo Databricks.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#5DD6FF"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Identificação de recurso nativo Databricks..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.databricks_native`.

### `editorial.human_decision`

Identificação de decisão humana.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FFC966"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Identificação de decisão humana..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.human_decision`.

### `editorial.result_evidence`

Identificação de resultado ou evidência.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#66E3C4"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Identificação de resultado ou evidência..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.result_evidence`.

### `editorial.supporting_method`

Identificação de método de apoio.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#A992FF"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Identificação de método de apoio..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.supporting_method`.

### `editorial.danger`

Identificação visual de risco, sem criar critério analítico.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FF7A7A"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])"}`. **Edição de proposta:** mantenedor.
**Controle projetado:** `seletor_cor_e_hex`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Identificação visual de risco, sem criar critério analítico..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:colors.danger`.

### `font.family`

Família editorial por ID; não distribui nem baixa fontes.

**Unidade:** id-fonte. **Tipo:** string. **Default de referência:** `"editorial_inter"`.
**Limites:** `{"enum": ["editorial_inter", "system_arial"]}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `seletor_fonte`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Família editorial por ID; não distribui nem baixa fontes..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:typography.family`.

### `typography.presentation_title_px`

Título de apresentação no canvas original.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `52`.
**Limites:** `{"minimum": 24, "maximum": 96}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Título de apresentação no canvas original..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:typography.presentation_title_px`.

### `typography.readme_heading_px`

Cabeçalho de README no canvas original.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `34`.
**Limites:** `{"minimum": 20, "maximum": 72}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Cabeçalho de README no canvas original..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:typography.readme_heading_px`.

### `typography.module_title_px`

Título interno de módulo.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `30`.
**Limites:** `{"minimum": 18, "maximum": 64}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Título interno de módulo..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:typography.module_title_px`.

### `typography.body_px`

Texto de corpo no canvas original.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `32`.
**Limites:** `{"minimum": 18, "maximum": 64}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Texto de corpo no canvas original..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:typography.body_px`.

### `typography.small_px`

Texto menor no canvas original.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `24`.
**Limites:** `{"minimum": 14, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Texto menor no canvas original..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:typography.small_px`.

### `geometry.corner_radius`

Raio de cantos editoriais.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `22`.
**Limites:** `{"minimum": 0, "maximum": 64}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Raio de cantos editoriais..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:geometry.corner_radius`.

### `geometry.connector_width`

Espessura dos conectores.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `5`.
**Limites:** `{"minimum": 1, "maximum": 12}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Espessura dos conectores..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:geometry.connector_width`.

### `geometry.border_width`

Espessura das bordas.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `3`.
**Limites:** `{"minimum": 1, "maximum": 12}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Espessura das bordas..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:geometry.border_width`.

### `geometry.safe_margin`

Margem de segurança.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `56`.
**Limites:** `{"minimum": 16, "maximum": 160}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Margem de segurança..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:geometry.safe_margin`.

### `geometry.glow_opacity`

Opacidade do brilho decorativo; não substitui contraste.

**Unidade:** proporcao. **Tipo:** number. **Default de referência:** `0.16`.
**Limites:** `{"minimum": 0, "maximum": 0.3}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Opacidade do brilho decorativo; não substitui contraste..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:geometry.glow_opacity`.

### `canvas.width_px`

Largura original do material; o tamanho efetivo é verificado na publicação.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `1400`.
**Limites:** `{"minimum": 720, "maximum": 3200}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Largura original do material; o tamanho efetivo é verificado na publicação..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:presets.readme_standard`.

### `canvas.height_px`

Altura original do material editorial.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `900`.
**Limites:** `{"minimum": 480, "maximum": 1800}`. **Edição de proposta:** proponente, mantenedor.
**Controle projetado:** `controle_numerico`. **Entrega:** `PLANEJADO_V06`. **Contextos:** readme, presentation.
**Pontos de integração:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml`; `tools/readme_visuals/lib.mjs`; `tools/readme_visuals/production.mjs`.
**Efeito previsto:** Altura original do material editorial..
**Origem do default:** `ambiente_fonte/.assistant/hub_readmes_visual_assets/visual_system/tokens.yaml:presets.readme_standard`.
