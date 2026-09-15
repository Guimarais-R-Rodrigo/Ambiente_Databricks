# V12 — fontes oficiais verificadas

Consulta realizada em **14/09/2026**. Fontes externas sustentam comportamento Databricks; o escopo V12 vem do próprio repositório.

## Databricks AI/BI — dashboard settings

https://docs.databricks.com/aws/en/dashboards/manage/settings

Verificado em 14/09/2026:

- settings são acessíveis em dashboard draft;
- `Export theme` baixa JSON de tema separado do dashboard JSON;
- `Import theme` torna o tema importado o tema atual do dashboard;
- tema inválido é recusado e o dashboard permanece inalterado;
- light/dark podem ser pré-visualizados;
- `Color mappings` são locais ao dashboard.

A página não publica um schema completo e versionado do JSON exportado. A decisão V11 de não inventar esse schema permanece.

## Databricks AI/BI — workspace themes

https://docs.databricks.com/aws/en/ai-bi/admin/themes

Verificado em 14/09/2026:

- somente workspace admins criam/atualizam/apagam workspace theme;
- dashboards novos herdam o tema configurado;
- dashboard existente recebe snapshot quando aplica workspace theme;
- atualização posterior não se propaga automaticamente;
- reaplicação é manual;
- apagar workspace theme não muda dashboards existentes;
- a Settings API suporta get/update/delete de workspace themes.

A disponibilidade de API **não autoriza automação V12**. Qualquer escrita remota continua gate operacional separado.

## Custom visualizations

https://docs.databricks.com/aws/en/dashboards/manage/visualizations/custom-visualizations

Verificado em 14/09/2026: visualizações Vega-Lite podem herdar valores resolvidos do tema e expõem sinais como `colors`, `mode` e `dashboardTheme`. Isso não é tratado como schema do arquivo `Export theme`.

## Databricks Apps — autorização

https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth

Verificado em 14/09/2026: App authorization usa service principal dedicado; user authorization usa a identidade/permissões do usuário e scopes. A V12 não grava credenciais e não presume que identidade do navegador seja autorização suficiente.

## Databricks Apps — permissões

https://docs.databricks.com/aws/en/dev-tools/databricks-apps/permissions

Verificado em 14/09/2026: `CAN USE` e `CAN MANAGE` controlam acesso ao App; `CAN MANAGE` inclui gestão de permissões. Isso é distinto da autorização a dados/recursos.

## Limite de evidência

A documentação oficial descreve capacidades da plataforma, mas não prova que o workspace de teste possui feature, permissão ou comportamento efetivo. Isso só recebe `PASS` de ambiente depois de observação real autorizada.
