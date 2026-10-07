# MT24 — mapa de campos da ponte AI/BI

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt24-bridge-field-map"></a>
<a id="mt-mod-mt24-bridge-field-map-h-mt24-mapa-de-campos-da-ponte-aibi"></a>
### MT24 — mapa de campos da ponte AI/BI

Consulta técnica complementar ao capítulo MT24. A matriz e os objetos de projeção são **formatos do Hub**. Este documento não representa nem supõe um schema JSON nativo Databricks. A fonte da matriz é `ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/aibi_mapping.json` (SHA-256 `98dba3149203a174c7ef76f5aac5636e9c3ab34fcd37ae120200347da831996f`); a implementação fica em `_aibi_theme_impl.py`. O binding só pode ser preenchido depois de export real e revisão de JSON Pointers existentes.

| Artefato | Caminho | Tipo | Significado e condição | Fonte/consumidor |
|---|---|---|---|---|
| Matriz | $.contract_version | int | Versão da matriz local; o loader exige 1. | aibi_mapping.json; _load_mapping |
| Matriz | $.source_context | str | Contexto de origem; o loader exige notebook. | aibi_mapping.json; _load_mapping |
| Matriz | $.target_product | str | Nome do produto alvo da projeção. | aibi_mapping.json |
| Matriz | $.native_theme_json_schema_status | str | Registro do estado de conhecimento do formato nativo. | aibi_mapping.json |
| Matriz | $.native_import_ready_by_default | bool | Declara que a projeção não nasce importável. | aibi_mapping.json |
| Matriz | $.classifications[*] | str | Classes declaradas translated/approximated/unsupported. | aibi_mapping.json; metadado declarativo, não lido por _load_mapping; as classes aceitas de mappings vêm da constante Python _ALLOWED_CLASSES |
| Matriz | $.binding_strategies[*] | str | Estratégias declaradas direct/manual/none. | aibi_mapping.json; metadado declarativo, não lido por _load_mapping; as estratégias aceitas de mappings vêm da constante Python _ALLOWED_BINDING |
| Matriz | $.capabilities.<id>.scope | str | Escopo declarado da capacidade alvo. | aibi_mapping.json; descrição não lida por _load_mapping; integridade por hash não constitui interpretação deste subcampo |
| Matriz | $.capabilities.<id>.official_status | str | Status documentado da capacidade na fonte oficial estudada. | aibi_mapping.json |
| Matriz | $.mappings[*].hub_token | str | Nome de token do notebook; as 48 linhas devem cobrir todos exatamente uma vez. | aibi_mapping.json; _load_mapping; project_theme |
| Matriz | $.mappings[*].classification | str | Classe de correspondência; controla automação. | aibi_mapping.json; _load_mapping |
| Matriz | $.mappings[*].target_capability | str\|null | Capacidade alvo existente no catálogo; nulo para unsupported. | aibi_mapping.json; _load_mapping |
| Matriz | $.mappings[*].binding_strategy | str | direct só se translated; none para unsupported. | aibi_mapping.json; _load_mapping |
| Matriz | $.mappings[*].note | str | Justificativa/limite semântico da linha. | aibi_mapping.json |
| Matriz | $.official_sources[*].title | str | Título da fonte oficial estudada. | aibi_mapping.json |
| Matriz | $.official_sources[*].url | str | URL da fonte oficial. | aibi_mapping.json |
| Matriz | $.official_sources[*].verified_on | str | Data de verificação registrada pela V11. | aibi_mapping.json |
| Projeção | $.format | str | Formato próprio hub-aibi-theme-projection, não formato Databricks. | AibiThemeProjection.to_dict |
| Projeção | $.version | int | Versão 1 da exportação do Hub. | AibiThemeProjection.to_dict |
| Projeção | $.source.theme_id | str | ID da configuração Hub que originou a projeção. | AibiThemeProjection.to_dict |
| Projeção | $.source.theme_version | str | Revisão do tema de origem. | AibiThemeProjection.to_dict |
| Projeção | $.source.fingerprint | str | Fingerprint do ResolvedTheme revalidado. | AibiThemeProjection.to_dict |
| Projeção | $.source.content_sha256 | str | Hash do conteúdo canônico do tema. | AibiThemeProjection.to_dict |
| Projeção | $.source.context | str | notebook; origem exigida. | AibiThemeProjection.to_dict |
| Projeção | $.source.mode | str | Modo do tema de origem. | AibiThemeProjection.to_dict |
| Projeção | $.target.product | str | Produto de destino declarado. | AibiThemeProjection.to_dict |
| Projeção | $.target.native_schema_status | str | unverified no resultado local. | AibiThemeProjection.to_dict |
| Projeção | $.target.native_import_ready | bool | false; não promete importação nativa. | AibiThemeProjection.to_dict |
| Projeção | $.mapping_sha256 | str | Hash da matriz local fixada. | AibiThemeProjection.to_dict |
| Projeção | $.summary.translated | int | Contagem das traduções diretas. | AibiThemeProjection.to_dict |
| Projeção | $.summary.approximated | int | Contagem de aproximações que requerem revisão. | AibiThemeProjection.to_dict |
| Projeção | $.summary.unsupported | int | Contagem sem equivalência segura. | AibiThemeProjection.to_dict |
| Projeção | $.mappings[*].source_value | JSON | Valor do token proveniente do tema verificado, adicionado à linha da matriz. | project_theme |
| Projeção | $.mappings[*].hub_token | str | Token Hub original da linha; uma linha por token da matriz, sem duplicata. | project_theme; AibiThemeProjection.to_dict |
| Projeção | $.mappings[*].classification | str | Classe translated/approximated/unsupported herdada da matriz; determina se a projeção é direta, manual ou sem equivalente. | project_theme; AibiThemeProjection.to_dict |
| Projeção | $.mappings[*].target_capability | str\|null | Capacidade alvo registrada na matriz; null quando classification=unsupported. | project_theme; AibiThemeProjection.to_dict |
| Projeção | $.mappings[*].binding_strategy | str | Estratégia herdada: direct apenas para translated; none para unsupported; manual requer revisão. | project_theme; AibiThemeProjection.to_dict |
| Projeção | $.mappings[*].note | str | Justificativa ou limite semântico original da correspondência na matriz. | project_theme; AibiThemeProjection.to_dict |
| Projeção | $.warnings[*] | str | Avisos sobre schema nativo, mutação e aproximação. | AibiThemeProjection.to_dict |
| Binding | $.binding_version | int | Versão 1 exigida para descrever a ligação ao template exportado. | bind_native_template |
| Binding | $.template_sha256 | str | SHA-256 dos bytes exatos do export nativo; divergência recusa. | bind_native_template |
| Binding | $.paths.<target_capability> | JSON Pointer | Aponta campo já existente no template para uma das 3 capacidades translated/direct. | bind_native_template; _set_existing_pointer |
| Candidato | content | bytes | Bytes UTF-8 canônicos do template modificado localmente; não comprovam aceitação ou renderização Databricks. | AibiNativeCandidate; bind_native_template |
| Candidato | template_sha256 | str | Hash do export usado como base. | AibiNativeCandidate |
| Candidato | candidate_sha256 | str | Hash dos bytes canônicos gerados localmente. | AibiNativeCandidate |
| Candidato | applied_capabilities[*] | str | Capacidades diretas efetivamente vinculadas. | AibiNativeCandidate |
| Candidato | omitted_capabilities[*] | str | Capacidades diretas não incluídas no binding. | AibiNativeCandidate |
| Candidato | validation_status | str | locally_bound_not_databricks_validated. | AibiNativeCandidate |

<a id="mt-mod-mt24-bridge-field-map-h-matriz-completa-de-48-tokens"></a>
#### Matriz completa de 48 tokens

A coluna alvo vazia corresponde a `null` para tokens `unsupported`. `direct` só aparece nas três linhas traduzidas. A nota original fica no JSON de origem; esta tabela resume para localização e conferência.

| Token Hub | Classe | Capacidade alvo | Estratégia |
|---|---|---|---|
| `brand.primary` | approximated | `widget.selection_color` | manual |
| `brand.accent` | unsupported | null | none |
| `text.primary` | approximated | `typography.category.color` | manual |
| `text.plot` | approximated | `typography.category.color` | manual |
| `text.secondary` | approximated | `typography.category.color` | manual |
| `surface.section` | approximated | `canvas.background` | manual |
| `surface.card` | translated | `widget.background` | direct |
| `table.header_text` | approximated | `typography.category.color` | manual |
| `divider.light` | approximated | `visualization.grid_color` | manual |
| `divider.medium` | approximated | `widget.border` | manual |
| `status.ok_bg` | unsupported | null | none |
| `status.ok_text` | unsupported | null | none |
| `status.warn_bg` | unsupported | null | none |
| `status.warn_text` | unsupported | null | none |
| `status.fail_bg` | unsupported | null | none |
| `status.fail_text` | unsupported | null | none |
| `semantic.positive` | approximated | `dashboard.color_mappings` | manual |
| `semantic.negative` | approximated | `dashboard.color_mappings` | manual |
| `semantic.neutral` | approximated | `dashboard.color_mappings` | manual |
| `semantic.warning` | approximated | `dashboard.color_mappings` | manual |
| `palette.categorical` | translated | `visualization.categorical_palette` | direct |
| `palette.curves_legacy` | unsupported | null | none |
| `palette.sequential` | approximated | `visualization.continuous_gradient` | manual |
| `palette.diverging` | approximated | `visualization.continuous_gradient` | manual |
| `font.family` | approximated | `typography.font_family` | manual |
| `chart.font_px` | approximated | `typography.category.size` | manual |
| `chart.title_px` | approximated | `typography.category.size` | manual |
| `chart.footer_px` | approximated | `typography.category.size` | manual |
| `chart.height_px` | unsupported | null | none |
| `chart.width_px` | unsupported | null | none |
| `chart.margin_left_px` | unsupported | null | none |
| `chart.margin_right_px` | unsupported | null | none |
| `chart.margin_top_px` | unsupported | null | none |
| `chart.margin_bottom_px` | unsupported | null | none |
| `section.title_px` | approximated | `typography.category.size` | manual |
| `section.description_px` | approximated | `typography.category.size` | manual |
| `section.radius_px` | unsupported | null | none |
| `section.padding_y_px` | unsupported | null | none |
| `section.padding_x_px` | unsupported | null | none |
| `section.border_px` | approximated | `widget.border` | manual |
| `card.font_px` | unsupported | null | none |
| `card.radius_px` | translated | `widget.corner_radius` | direct |
| `card.padding_y_px` | approximated | `widget.padding` | manual |
| `card.padding_x_px` | approximated | `widget.padding` | manual |
| `badge.font_px` | unsupported | null | none |
| `badge.radius_px` | unsupported | null | none |
| `badge.padding_y_px` | unsupported | null | none |
| `badge.padding_x_px` | unsupported | null | none |

<a id="mt-mod-mt24-bridge-field-map-h-interpretação-e-limites"></a>
#### Interpretação e limites

O produtor da matriz é a frente V11 do Hub, com hash fixado no loader. `project_theme` consome uma configuração `notebook` integralmente revalidada; `export_projection` produz bytes do formato Hub. Um mantenedor produz o binding após inspecionar um **export nativo real**. `bind_native_template` confere o hash do export, os caminhos existentes, o tipo do valor, a classe direta e a ausência de colisão. O candidato gerado permanece local até o produto nativo aceitar e renderizar o arquivo no ambiente autorizado.

`dashboard_sintetico.json` é fixture do Hub e não serve como template nativo. A documentação oficial de [Dashboard settings](https://docs.databricks.com/aws/en/dashboards/manage/settings) foi registrada como reconfirmada em 01/10/2026, no fechamento histórico para os botões Export/Import e seus efeitos gerais; o formato interno do export não foi inferido desses recursos.

**Reconciliação de 07/10/2026.** Matriz e implementação permanecem idênticas aos bytes da autoria anterior: as 48 correspondências e seus limites foram preservados. O JSON irmão inclui agora as 48 linhas com a nota original, além dos campos da consulta. `content` explicita os bytes do candidato, antes ausentes da tabela. Esta revisão de fonte não reexecutou importação, binding nem consulta oficial de plataforma; as datas de `official_sources` continuam históricas.


<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
