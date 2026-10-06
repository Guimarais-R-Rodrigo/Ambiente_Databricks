# Referência de uso dos tokens

> Referência gerada a partir do schema e da cobertura dos consumidores. Não editar separadamente.

Consulte esta página para escolher um campo e verificar onde ele produz efeito. O [schema](theme.schema.json) define nomes, tipos, defaults declarativos e restrições; os adaptadores definem o suporte efetivo. Um campo válido não é um controle disponível em toda interface.

Os defaults abaixo são referências, não valores injetados pelo validador. A configuração deve ser completa para seu contexto. Carregar/validar um tema não o aplica, não o aprova e não o publica. A edição de proposta indicada por papel é metadado de contrato, não autenticação nem concessão de permissão.

Comece pelo [guia operacional](GUIA_OPERACIONAL.md). Passe um ResolvedTheme explicitamente às APIs resolvidas; as APIs legadas e constantes compartilhadas não são alteradas. O adaptador Plotly e a galeria completa aceitam notebook/light. SHAP/Matplotlib e Kaplan–Meier não recebem tema por essa rota.

O campo de consumo identifica leituras diretas; componentes e wrappers podem herdar o layout/CSS desses adaptadores. O CSS de styles alimenta seção, cartões, badges, divisores, índice e tabela nas respectivas APIs resolvidas. Nem toda propriedade é usada por todo componente, e parâmetros explícitos de uma figura podem prevalecer.

O [Visual Lab](../../hub_snippets/visual/theme_lab/README.md) e o [App de autoria](databricks_app/README.md) compartilham a disponibilidade de prévia indicada por token. O tipo de controle declarado no schema é uma intenção de edição; cada interface pode usar outro widget. Prévia sintética, validação e persistência não comprovam acessibilidade, ACL ou homologação do ambiente.

Em AI/BI, a classificação vem da [matriz do Hub](aibi/aibi_mapping.json): translated indica correspondência conceitual, approximated exige decisão de mapeamento e unsupported não possui binding. Nenhuma classificação equivale a importação nativa pronta. É necessário export real, binding revisado e autorização específica para importar/publicar; consulte o [guia AI/BI](aibi/GUIA_PRIMEIRO_USO.md).

Cores e status não criam regras analíticas. Conferir contraste de uma combinação não certifica toda a interface; o par de alerta de referência requer avaliação. A paleta divergente exige quantidade ímpar também na validação semântica do núcleo.

## Notebook

### `brand.primary`

Cor de títulos, bordas de seção e cabeçalhos de tabela; não recolore categorias automaticamente.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#005CA9"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Cor de títulos, bordas de seção e cabeçalhos de tabela; não recolore categorias automaticamente.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md); [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md); [PerformanceMonitor.plot_timeline_resolvido](../../hub_snippets/ml/performance_monitor/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `widget.selection_color`. Cor de marca pode aproximar a cor de seleção; não é equivalência semântica universal.

### `brand.accent`

Destaque institucional secundário nos consumidores que já usam LARANJA.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#F7941D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Destaque institucional secundário nos consumidores que já usam LARANJA.
**Consumo atual:** Sem leitura visual direta nas APIs notebook atuais; valor validado e preservado, sem propagação automática. As curvas com tema usam a segunda cor de palette.curves_legacy, não brand.accent.
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. AI/BI não expõe no contrato público um segundo token institucional genérico equivalente.

### `text.primary`

Texto dos cartões de indicadores.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#1A1A1A"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Texto dos cartões de indicadores.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.color`. AI/BI configura cor por categoria de texto; um único text.primary não cobre todas as categorias.

### `text.plot`

Texto geral dos gráficos.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#333333"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Texto geral dos gráficos.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md); [curves_plotly (com theme explícito)](../../hub_snippets/ml/curves_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.color`. Pode orientar categorias de eixo/legenda, mas exige escolha explícita da categoria nativa.

### `text.secondary`

Descrição das seções e notas dos gráficos.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#6C757D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Descrição das seções e notas dos gráficos.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md); [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md); [PerformanceMonitor.plot_timeline_resolvido](../../hub_snippets/ml/performance_monitor/README.md); [plot_umap_clusters_resolvido](../../hub_snippets/ml/umap_viz/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.color`. Pode orientar subtítulos/notas, mas a correspondência depende da categoria nativa.

### `surface.section`

Fundo de cabeçalhos de seção e itens de índice.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#F8F9FA"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Fundo de cabeçalhos de seção e itens de índice.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `canvas.background`. Fundo de seção de notebook não equivale necessariamente ao canvas inteiro do dashboard.

### `surface.card`

Fundo de cartões e badges informativos.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#E8F4FD"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Fundo de cartões e badges informativos.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md); [curves_plotly (com theme explícito)](../../hub_snippets/ml/curves_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `translated`; binding `direct`. Destino conceitual: `widget.background`. Fundo de cartão é semanticamente compatível com fundo de widget.

### `table.header_text`

Cor de texto dos títulos de coluna.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FFFFFF"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Cor de texto dos títulos de coluna.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.color`. Cabeçalho de tabela depende da categoria de texto suportada pelo dashboard.

### `divider.light`

Cor do separador fino.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#D9DEE3"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Cor do separador fino.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `visualization.grid_color`. Separador leve pode orientar linhas de grade, mas os elementos têm funções distintas.

### `divider.medium`

Cor do separador médio.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#BFC7D1"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Cor do separador médio.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `widget.border`. Separador médio pode orientar borda de widget, sem equivalência de espessura/estado.

### `status.ok_bg`

Fundo do estado ok; não define a regra que atribui esse estado.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#EAF7EC"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Fundo do estado ok; não define a regra que atribui esse estado.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Tema nativo não publica um token genérico de fundo de status equivalente.

### `status.ok_text`

Texto do estado ok.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#2E7D32"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Texto do estado ok.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Tema nativo não publica um token genérico de texto de status equivalente.

### `status.warn_bg`

Fundo do estado de alerta.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FFF8E1"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Fundo do estado de alerta.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Tema nativo não publica um token genérico de fundo de alerta equivalente.

### `status.warn_text`

Texto do estado de alerta; legado exige avaliação de contraste.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#B26A00"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Texto do estado de alerta; legado exige avaliação de contraste.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Tema nativo não publica um token genérico de texto de alerta equivalente.

### `status.fail_bg`

Fundo do estado de falha.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FDECEC"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Fundo do estado de falha.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Tema nativo não publica um token genérico de fundo de falha equivalente.

### `status.fail_text`

Texto do estado de falha.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#B71C1C"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Texto do estado de falha.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Tema nativo não publica um token genérico de texto de falha equivalente.

### `semantic.positive`

Cor de estado favorável declarado pelo consumidor, não de aumento numérico.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#8DC63F"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `avancado_amostra_sem_promessa_de_propagacao`. **Contextos:** notebook.
**Efeito definido:** Cor de estado favorável declarado pelo consumidor, não de aumento numérico.
**Consumo atual:** Sem leitura visual direta nas APIs notebook atuais; valor validado e preservado, sem propagação automática.
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `dashboard.color_mappings`. Color mappings são locais ao dashboard e exigem nomes de valores; não são semântica positiva global.

### `semantic.negative`

Cor de estado desfavorável ou destaque negativo já definido pelo consumidor.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#C4262E"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** notebook.
**Efeito definido:** Cor de estado desfavorável ou destaque negativo já definido pelo consumidor.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md); [PerformanceMonitor.plot_timeline_resolvido](../../hub_snippets/ml/performance_monitor/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `dashboard.color_mappings`. Color mappings são locais ao dashboard e exigem nomes de valores; não são semântica negativa global.

### `semantic.neutral`

Cor do estado neutro.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#6C757D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `avancado_amostra_sem_promessa_de_propagacao`. **Contextos:** notebook.
**Efeito definido:** Cor do estado neutro.
**Consumo atual:** Sem leitura visual direta nas APIs notebook atuais; valor validado e preservado, sem propagação automática.
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `dashboard.color_mappings`. Color mappings são locais ao dashboard e exigem nomes de valores; não são semântica neutra global.

### `semantic.warning`

Cor de atenção; a condição analítica continua fora do tema.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FFB800"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `avancado_amostra_sem_promessa_de_propagacao`. **Contextos:** notebook.
**Efeito definido:** Cor de atenção; a condição analítica continua fora do tema.
**Consumo atual:** [PerformanceMonitor.plot_timeline_resolvido](../../hub_snippets/ml/performance_monitor/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `dashboard.color_mappings`. Color mappings são locais ao dashboard e exigem nomes de valores; não são semântica de alerta global.

### `palette.categorical`

Paleta categórica; o mapa estável categoria/cor pertence ao consumidor.

**Unidade:** paleta. **Tipo:** array. **Default de referência:** `["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E", "#7B2D8B", "#00A79D", "#F15A29", "#A7A9AC"]`.
**Limites:** `{"items": {"type": "string", "pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}, "minItems": 2, "maxItems": 20, "uniqueItems": true}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `editor_paleta_avancado`. **Contextos:** notebook.
**Efeito definido:** Paleta categórica; o mapa estável categoria/cor pertence ao consumidor.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md); [plot_umap_clusters_resolvido](../../hub_snippets/ml/umap_viz/README.md); [vintage_analysis (curvas/heatmap resolvidos)](../../hub_snippets/ml/vintage_analysis/README.md). Cores explícitas dos traces e a paleta própria das curvas podem prevalecer.
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `translated`; binding `direct`. Destino conceitual: `visualization.categorical_palette`. Paleta categórica corresponde à capacidade nativa de cores categóricas.

### `palette.curves_legacy`

Paleta distinta das curvas de ML; não expandir silenciosamente para dez cores.

**Unidade:** paleta. **Tipo:** array. **Default de referência:** `["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E"]`.
**Limites:** `{"items": {"type": "string", "pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}, "minItems": 2, "maxItems": 20, "uniqueItems": true}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `editor_paleta_avancado`. **Contextos:** notebook.
**Efeito definido:** Paleta distinta das curvas de ML; não expandir silenciosamente para dez cores.
**Consumo atual:** [curves_plotly (com theme explícito)](../../hub_snippets/ml/curves_plotly/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Paleta legada de curvas é específica do Hub e não deve substituir silenciosamente a paleta categórica nativa.

### `palette.sequential`

Cores sequenciais, em ordem de intensidade; não altera domínio dos valores.

**Unidade:** paleta. **Tipo:** array. **Default de referência:** `["#E6F0FA", "#99C2E8", "#4D94D6", "#005CA9", "#003D73"]`.
**Limites:** `{"items": {"type": "string", "pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}, "minItems": 2, "maxItems": 11, "uniqueItems": true}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `editor_paleta_avancado`. **Contextos:** notebook.
**Efeito definido:** Cores sequenciais, em ordem de intensidade; não altera domínio dos valores.
**Consumo atual:** [vintage_analysis (curvas/heatmap resolvidos)](../../hub_snippets/ml/vintage_analysis/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `visualization.continuous_gradient`. Pode orientar gradiente contínuo, mas a forma nativa e a interpolação precisam ser confirmadas.

### `palette.diverging`

Cores divergentes; quantidade ímpar e cor central, sem definir ponto zero dos dados.

**Unidade:** paleta. **Tipo:** array. **Default de referência:** `["#C4262E", "#F7941D", "#FFB800", "#8DC63F", "#005CA9"]`.
**Limites:** `{"items": {"type": "string", "pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}, "minItems": 3, "maxItems": 11, "uniqueItems": true}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `avancado_amostra_sem_promessa_de_propagacao`. **Contextos:** notebook.
**Efeito definido:** Cores divergentes; quantidade ímpar e cor central, sem definir ponto zero dos dados.
**Consumo atual:** [plot_correlation_resolvido](../../hub_snippets/display/correlation_matrix/README.md); [theme_lab.build_preview (heatmap sintético)](../../hub_snippets/visual/theme_lab/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `visualization.continuous_gradient`. Pode orientar gradiente contínuo, mas não há contrato público de gradiente divergente equivalente.

### `font.family`

Família tipográfica por identificador permitido, sem CSS livre.

**Unidade:** id-fonte. **Tipo:** string. **Default de referência:** `"system_sans"`.
**Limites:** `{"enum": ["system_sans", "system_arial"]}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_fonte`. **Contextos:** notebook.
**Efeito definido:** Família tipográfica por identificador permitido, sem CSS livre.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md); [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md). A tabela pandas mantém a família fixa Segoe UI; este token não altera table.font_family.
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.font_family`. O Hub usa aliases de fontes; a opção nativa disponível precisa ser resolvida no ambiente.

### `chart.font_px`

Tamanho do texto do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `12`.
**Limites:** `{"minimum": 8, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Tamanho do texto do gráfico.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.size`. Tamanho geral do gráfico deve ser distribuído por categorias de texto nativas.

### `chart.title_px`

Tamanho do título do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `16`.
**Limites:** `{"minimum": 12, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Tamanho do título do gráfico.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.size`. Pode orientar a categoria de título, mas não é aplicado automaticamente sem binding revisado.

### `chart.footer_px`

Tamanho das notas de gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `10`.
**Limites:** `{"minimum": 8, "maximum": 24}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Tamanho das notas de gráfico.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md); [plot_umap_clusters_resolvido](../../hub_snippets/ml/umap_viz/README.md). No adaptador geral, só há efeito quando a chamada cria uma nota/rodapé.
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.size`. Pode orientar texto pequeno/nota, mas depende da categoria nativa.

### `chart.height_px`

Altura do gráfico, sem alterar seus dados.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `450`.
**Limites:** `{"minimum": 240, "maximum": 1600}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Altura do gráfico, sem alterar seus dados.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md); [vintage_analysis (curvas/heatmap resolvidos)](../../hub_snippets/ml/vintage_analysis/README.md). O heatmap de safras usa o máximo entre este valor e 25 px por safra.
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Tema AI/BI não é contrato de dimensão individual de gráfico.

### `chart.width_px`

Largura nominal do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `900`.
**Limites:** `{"minimum": 320, "maximum": 2400}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Largura nominal do gráfico.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Tema AI/BI não é contrato de dimensão individual de gráfico.

### `chart.margin_left_px`

Margem esquerda do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `60`.
**Limites:** `{"minimum": 0, "maximum": 240}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Margem esquerda do gráfico.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Margens do gráfico não pertencem ao tema nativo documentado.

### `chart.margin_right_px`

Margem direita do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `30`.
**Limites:** `{"minimum": 0, "maximum": 240}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Margem direita do gráfico.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Margens do gráfico não pertencem ao tema nativo documentado.

### `chart.margin_top_px`

Margem superior do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `70`.
**Limites:** `{"minimum": 0, "maximum": 240}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Margem superior do gráfico.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Margens do gráfico não pertencem ao tema nativo documentado.

### `chart.margin_bottom_px`

Margem inferior do gráfico.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `60`.
**Limites:** `{"minimum": 0, "maximum": 240}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Margem inferior do gráfico.
**Consumo atual:** [theme_plotly (layout e rodapé nas APIs resolvidas)](../../hub_snippets/visual/theme_plotly/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Margens do gráfico não pertencem ao tema nativo documentado.

### `section.title_px`

Tamanho do título da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `18`.
**Limites:** `{"minimum": 12, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Tamanho do título da seção.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.size`. Título de seção pode orientar categoria de título, mas conflita com outros títulos se aplicado globalmente.

### `section.description_px`

Tamanho da descrição da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `13`.
**Limites:** `{"minimum": 10, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Tamanho da descrição da seção.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `typography.category.size`. Descrição de seção pode orientar categoria secundária de texto.

### `section.radius_px`

Raio dos cantos da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `4`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Raio dos cantos da seção.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Raio de seção não tem consumidor nativo separado do widget.

### `section.padding_y_px`

Espaçamento vertical interno da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `12`.
**Limites:** `{"minimum": 0, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Espaçamento vertical interno da seção.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Padding de seção do notebook não é um token nativo de dashboard separado.

### `section.padding_x_px`

Espaçamento horizontal interno da seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `16`.
**Limites:** `{"minimum": 0, "maximum": 64}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Espaçamento horizontal interno da seção.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Padding de seção do notebook não é um token nativo de dashboard separado.

### `section.border_px`

Espessura da borda lateral de seção.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `4`.
**Limites:** `{"minimum": 0, "maximum": 12}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Espessura da borda lateral de seção.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `widget.border`. Espessura de borda de seção pode orientar borda de widget, sem binding automático.

### `card.font_px`

Tamanho do texto de cartão.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `12`.
**Limites:** `{"minimum": 10, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Tamanho do texto de cartão.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. O tamanho de fonte de cartão não tem categoria nativa própria garantida.

### `card.radius_px`

Raio dos cantos de cartão.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `12`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Raio dos cantos de cartão.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `translated`; binding `direct`. Destino conceitual: `widget.corner_radius`. Raio de cartão corresponde à capacidade nativa de raio de canto do widget.

### `card.padding_y_px`

Espaçamento vertical do cartão.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `4`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Espaçamento vertical do cartão.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `widget.padding`. AI/BI possui padding de widget, mas o contrato público não garante eixos separados.

### `card.padding_x_px`

Espaçamento horizontal do cartão.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `10`.
**Limites:** `{"minimum": 0, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Espaçamento horizontal do cartão.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Controle habilitado na galeria sintética notebook/light; resultado depende do componente.
**AI/BI (matriz do Hub):** `approximated`; binding `manual`. Destino conceitual: `widget.padding`. AI/BI possui padding de widget, mas o contrato público não garante eixos separados.

### `badge.font_px`

Tamanho do texto do badge.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `11`.
**Limites:** `{"minimum": 10, "maximum": 24}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Tamanho do texto do badge.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Badge do Hub não possui consumidor nativo equivalente documentado.

### `badge.radius_px`

Raio dos cantos de badge.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `10`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Raio dos cantos de badge.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Badge do Hub não possui consumidor nativo equivalente documentado.

### `badge.padding_y_px`

Espaçamento vertical de badge.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `2`.
**Limites:** `{"minimum": 0, "maximum": 24}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Espaçamento vertical de badge.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Badge do Hub não possui consumidor nativo equivalente documentado.

### `badge.padding_x_px`

Espaçamento horizontal de badge.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `8`.
**Limites:** `{"minimum": 0, "maximum": 32}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** notebook.
**Efeito definido:** Espaçamento horizontal de badge.
**Consumo atual:** [styles.get_styles_resolvidos (CSS para componentes HTML)](../../hub_snippets/constants/styles/README.md).
**Visual Lab / App:** Sem componente na galeria; controle desabilitado e valor preservado.
**AI/BI (matriz do Hub):** `unsupported`; binding `none`. Badge do Hub não possui consumidor nativo equivalente documentado.

## README e apresentação

Estes campos pertencem aos contextos readme e presentation, não à galeria notebook nem ao App de autoria. A rota de variantes editoriais disponível seleciona readme; aceitar presentation no núcleo não garante um renderer de apresentações. O suporte abaixo descreve o compositor de variantes, que produz candidatos para revisão e preserva os assets congelados. O Markdown e as imagens já publicadas não são recoloridos ao carregar um tema. Consulte o [guia de recursos visuais](../../hub_readmes_visual_assets/README.md).

### `editorial.background`

Fundo do material editorial.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#06101D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Fundo do material editorial.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.background_elevated`

Superfície elevada.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#0B182A"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Superfície elevada.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.panel`

Fundo de painéis.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#102238"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Fundo de painéis.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.panel_high`

Painel em destaque.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#16304A"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Painel em destaque.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.line`

Linhas e conectores.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#34516D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Linhas e conectores.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.text`

Texto principal.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#F7FAFC"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Texto principal.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.muted`

Texto secundário.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#B8C9DA"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Texto secundário.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.quiet`

Texto de apoio discreto.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#8196AA"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Texto de apoio discreto.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.hub_custom`

Identificação de conteúdo customizado do Hub.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FF6598"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Identificação de conteúdo customizado do Hub.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.gradient_end`

Extremo do gradiente de fundo.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#102139"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Extremo do gradiente de fundo.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.atlas_core`

Núcleo da composição Atlas.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#0D2034"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Núcleo da composição Atlas.
**Consumo atual e limite:** Cor encaminhada ao compositor, usada na autoria de assinaturas. Na rota de variantes, essas assinaturas são congeladas e copiadas sem recoloração; alterar o token não modifica seus bytes.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.dossier_back`

Camada traseira do dossiê.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#0B1B2D"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Camada traseira do dossiê.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.dossier_middle`

Camada intermediária do dossiê.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#112740"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Camada intermediária do dossiê.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.dossier_fold`

Dobra do dossiê.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#1B3751"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Dobra do dossiê.
**Consumo atual e limite:** Cor encaminhada ao compositor, usada na autoria de assinaturas. Na rota de variantes, essas assinaturas são congeladas e copiadas sem recoloração; alterar o token não modifica seus bytes.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.databricks_native`

Identificação de recurso nativo Databricks.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#5DD6FF"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Identificação de recurso nativo Databricks.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.human_decision`

Identificação de decisão humana.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FFC966"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Identificação de decisão humana.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.result_evidence`

Identificação de resultado ou evidência.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#66E3C4"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Identificação de resultado ou evidência.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.supporting_method`

Identificação de método de apoio.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#A992FF"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Identificação de método de apoio.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `editorial.danger`

Identificação visual de risco, sem criar critério analítico.

**Unidade:** hex. **Tipo:** string. **Default de referência:** `"#FF7A7A"`.
**Limites:** `{"pattern": "^#[0-9A-F]{6}(?![\\s\\S])", "minLength": 7, "maxLength": 7}`. **Edição de proposta:** mantenedor.
**Controle declarado:** `seletor_cor_e_hex`. **Contextos:** readme, presentation.
**Efeito definido:** Identificação visual de risco, sem criar critério analítico.
**Consumo atual e limite:** Cor consumida pelo compositor nas figuras paramétricas que usam este papel. Assinaturas e assets congelados preservam os bytes; gerar uma variante não a aprova nem a publica.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `font.family`

Família editorial por ID; não distribui nem baixa fontes.

**Unidade:** id-fonte. **Tipo:** string. **Default de referência:** `"editorial_inter"`.
**Limites:** `{"enum": ["editorial_inter", "system_arial"]}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `seletor_fonte`. **Contextos:** readme, presentation.
**Efeito definido:** Família editorial por ID; não distribui nem baixa fontes.
**Consumo atual e limite:** O compositor de variantes aceita somente editorial_inter e recusa system_arial, embora ambos sejam válidos no schema. Não baixa fontes nem muda a fonte do Markdown.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `typography.presentation_title_px`

Título de apresentação no canvas original.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `52`.
**Limites:** `{"minimum": 24, "maximum": 96}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Título de apresentação no canvas original.
**Consumo atual e limite:** Valor encaminhado à configuração do compositor de variantes, mas sem leitura nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam valores próprios das composições. Não há propagação visual garantida.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `typography.readme_heading_px`

Cabeçalho de README no canvas original.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `34`.
**Limites:** `{"minimum": 20, "maximum": 72}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Cabeçalho de README no canvas original.
**Consumo atual e limite:** Valor encaminhado à configuração do compositor de variantes, mas sem leitura nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam valores próprios das composições. Não há propagação visual garantida.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `typography.module_title_px`

Título interno de módulo.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `30`.
**Limites:** `{"minimum": 18, "maximum": 64}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Título interno de módulo.
**Consumo atual e limite:** Valor encaminhado à configuração do compositor de variantes, mas sem leitura nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam valores próprios das composições. Não há propagação visual garantida.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `typography.body_px`

Texto de corpo no canvas original.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `32`.
**Limites:** `{"minimum": 18, "maximum": 64}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Texto de corpo no canvas original.
**Consumo atual e limite:** Default de tamanho dos helpers de texto/medição do compositor; chamadas com size explícito prevalecem. Não altera automaticamente todo texto das figuras.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `typography.small_px`

Texto menor no canvas original.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `24`.
**Limites:** `{"minimum": 14, "maximum": 48}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Texto menor no canvas original.
**Consumo atual e limite:** Valor encaminhado à configuração do compositor de variantes, mas sem leitura nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam valores próprios das composições. Não há propagação visual garantida.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `geometry.corner_radius`

Raio de cantos editoriais.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `22`.
**Limites:** `{"minimum": 0, "maximum": 64}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Raio de cantos editoriais.
**Consumo atual e limite:** Default de raio do helper de painéis do compositor; chamadas com radius explícito prevalecem. Não altera cantos de todos os elementos.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `geometry.connector_width`

Espessura dos conectores.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `5`.
**Limites:** `{"minimum": 1, "maximum": 12}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Espessura dos conectores.
**Consumo atual e limite:** Valor encaminhado à configuração do compositor de variantes, mas sem leitura nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam valores próprios das composições. Não há propagação visual garantida.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `geometry.border_width`

Espessura das bordas.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `3`.
**Limites:** `{"minimum": 1, "maximum": 12}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Espessura das bordas.
**Consumo atual e limite:** Valor encaminhado à configuração do compositor de variantes, mas sem leitura nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam valores próprios das composições. Não há propagação visual garantida.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `geometry.safe_margin`

Margem de segurança.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `56`.
**Limites:** `{"minimum": 16, "maximum": 160}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Margem de segurança.
**Consumo atual e limite:** Valor encaminhado à configuração do compositor de variantes, mas sem leitura nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam valores próprios das composições. Não há propagação visual garantida.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `geometry.glow_opacity`

Opacidade do brilho decorativo; não substitui contraste.

**Unidade:** proporcao. **Tipo:** number. **Default de referência:** `0.16`.
**Limites:** `{"minimum": 0, "maximum": 0.3}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Opacidade do brilho decorativo; não substitui contraste.
**Consumo atual e limite:** Valor encaminhado à configuração do compositor de variantes, mas sem leitura nos renderers atuais dessa rota; tamanhos, espessuras, margens e brilho usam valores próprios das composições. Não há propagação visual garantida.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `canvas.width_px`

Largura original do material; o tamanho efetivo é verificado na publicação.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `1400`.
**Limites:** `{"minimum": 720, "maximum": 3200}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Largura original do material; o tamanho efetivo é verificado na publicação.
**Consumo atual e limite:** Metadado preservado no tema; não redimensiona figuras. O compositor de variantes usa as dimensões do preset de cada contrato visual.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.

### `canvas.height_px`

Altura original do material editorial.

**Unidade:** px. **Tipo:** integer. **Default de referência:** `900`.
**Limites:** `{"minimum": 480, "maximum": 1800}`. **Edição de proposta:** proponente, mantenedor.
**Controle declarado:** `controle_numerico`. **Contextos:** readme, presentation.
**Efeito definido:** Altura original do material editorial.
**Consumo atual e limite:** Metadado preservado no tema; não redimensiona figuras. O compositor de variantes usa as dimensões do preset de cada contrato visual.
**Visual Lab / App / AI/BI:** Fora do contexto notebook dessas rotas; sem controle ou tradução editorial.
