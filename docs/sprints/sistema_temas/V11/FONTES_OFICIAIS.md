# V11 — fontes oficiais Databricks verificadas

Consulta realizada em **14/09/2026**. Estas fontes fundamentam somente as capacidades e limites externos; não certificam a implementação do Hub.

## Manage AI/BI dashboard workspace themes

https://docs.databricks.com/aws/en/ai-bi/admin/themes

Pontos usados:
- somente administradores do workspace gerenciam o workspace theme;
- temas incluem tipografia, canvas, widget, eixos/grade e paletas;
- dashboards novos herdam o workspace theme;
- dashboard existente recebe snapshot ao aplicar workspace theme;
- atualização posterior não se propaga automaticamente;
- reaplicação é manual;
- exclusão do workspace theme não remove snapshots já aplicados.

## Dashboard settings

https://docs.databricks.com/aws/en/dashboards/manage/settings

Pontos usados:
- settings de tema são acessíveis em dashboard draft;
- workspace theme, presets e customização local coexistem;
- `Color mappings` são locais ao dashboard;
- `Export theme` e `Import theme` trabalham com JSON de tema separado do dashboard JSON;
- arquivo inválido de tema é recusado e o dashboard permanece inalterado;
- aplicar workspace theme a dashboard existente cria snapshot;
- publicar é uma ação separada.

## Custom visualizations in AI/BI dashboards

https://docs.databricks.com/aws/en/dashboards/manage/visualizations/custom-visualizations

Pontos usados:
- Vega-Lite herda fontes/grade/fundo do tema;
- sinais `colors`, `mode` e `dashboardTheme` expõem valores de tema em runtime;
- `dashboardTheme` inclui `resolvedFontSettings`, `visualizationColors` e campos por modo como `gridLineColor`;
- isso **não** é assumido como schema do arquivo Import theme.

## Manage dashboards with Workspace APIs

https://docs.databricks.com/aws/en/dashboards/tutorials/workspace-dashboard-api

Ponto usado:
- `.lvdash.json` é um artefato de dashboard e pode conter definição completa, queries e widgets;
- a V11 evita editar esse arquivo para transferir apenas aparência e usa a separação oficial de theme export/import.

## Decisão de evidência

Nenhuma dessas páginas publica um schema completo e versionado para o JSON produzido por `Export theme`. Por isso a V11 não codifica nomes de campos nativos de importação por inferência. Um binding só poderá ser construído a partir de export real, revisado e fixado por hash.
