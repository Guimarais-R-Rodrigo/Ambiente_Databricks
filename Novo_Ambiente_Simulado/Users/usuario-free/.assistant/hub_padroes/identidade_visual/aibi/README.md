# AI/BI theme bridge — V11

## O que é

Esta pasta contém a ponte V11 entre o Sistema de Temas do Hub e os temas nativos de dashboards Databricks AI/BI.

A fonte de verdade **continua sendo `ResolvedTheme`**. A V11 não cria um segundo tema canônico, não transforma `context="aibi"` em contexto suportado pelo schema V01/V02 e não altera o núcleo de resolução. Em vez disso, uma configuração `notebook` íntegra é projetada para uma matriz explícita de capacidades AI/BI.

## Por que a ponte é conservadora

A documentação oficial do Databricks descreve as capacidades de temas do workspace/dashboard e oferece **Export theme** / **Import theme**, mas não publica um schema estável e completo para o JSON exportado. Por isso:

- `aibi_mapping.json` registra o que é `translated`, `approximated` ou `unsupported`;
- `aibi_theme.py` exporta uma **projeção do Hub**, não um JSON nativo fingindo ser importável;
- um candidato nativo só pode ser materializado a partir de um **template realmente exportado**, fixado por SHA-256, acompanhado de um binding revisado para os campos existentes;
- apenas as três correspondências `translated` com `binding_strategy="direct"` podem ser automatizadas;
- aproximações exigem revisão humana e itens não suportados nunca são aplicados silenciosamente.

## Capacidades documentadas consideradas

A matriz V11 considera capacidades atualmente documentadas no AI/BI: fontes por categoria de texto, fundo do canvas, fundo/borda/seleção/raio/padding de widget, cor de grade/eixos, paleta categórica, gradiente contínuo e `Color mappings` locais ao dashboard.

O tema do workspace e o tema local do dashboard têm escopos diferentes. Um dashboard existente recebe um **snapshot** ao aplicar o tema do workspace; alterações posteriores do tema do workspace não se propagam automaticamente. A reaplicação é manual.

## Arquivos

- `aibi_theme.py`: projeção, políticas locais e binder fail-closed;
- `aibi_mapping.json`: matriz canônica de correspondência dos 48 tokens `notebook`;
- `dashboard_sintetico.json`: fixture de dashboard para testes de semântica; **não é formato Databricks e não pode ser importado no Databricks**;
- `GUIA_PRIMEIRO_USO.md`: procedimento operacional para usuário não técnico.

## Limites

V11 não:
- chama Databricks SDK/REST/CLI;
- cria dashboard;
- altera tema do workspace;
- importa arquivo de tema;
- publica dashboard;
- muda queries, filtros ou métricas;
- promete propagação universal;
- certifica o formato de JSON nativo sem um export real do ambiente.

A homologação em workspace, browser, permissões reais, acessibilidade e UAT permanecem gates posteriores.
