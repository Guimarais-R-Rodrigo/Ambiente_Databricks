# Ponte de temas para AI/BI

## O que é

Esta pasta contém a ponte entre o Sistema de Temas do Hub e os temas nativos de dashboards Databricks AI/BI.

A fonte de verdade **continua sendo `ResolvedTheme`**. A ponte não cria um segundo tema canônico, não transforma `context="aibi"` em contexto suportado pelo schema central e não altera o núcleo de resolução. Em vez disso, uma configuração `notebook` íntegra é projetada para uma matriz explícita de capacidades AI/BI.

Percurso: `ResolvedTheme` notebook validado → projeção e cobertura de 48 tokens (3 traduzidos, 23 aproximados, 22 não suportados) → export nativo real → binding revisado por responsável técnico → bytes do candidato local. Gerar bytes não importa nem publica. Siga o [guia de primeiro uso](GUIA_PRIMEIRO_USO.md).

## Por que a ponte é conservadora

A documentação oficial do Databricks descreve as capacidades de temas do workspace/dashboard e oferece **Export theme** / **Import theme**, mas não publica um schema estável e completo para o JSON exportado. Por isso:

- `aibi_mapping.json` registra o que é `translated`, `approximated` ou `unsupported`;
- `aibi_theme.py` exporta uma **projeção do Hub**, não um JSON nativo fingindo ser importável;
- um candidato nativo só pode ser materializado a partir de um **template realmente exportado**, fixado por SHA-256, acompanhado de um binding revisado para os campos existentes;
- apenas as três correspondências `translated` com `binding_strategy="direct"` podem ser automatizadas;
- aproximações exigem revisão humana e itens não suportados nunca são aplicados silenciosamente.

## Capacidades documentadas consideradas

A matriz considera as capacidades documentadas nas fontes que acompanham o contrato no AI/BI: fontes por categoria de texto, fundo do canvas, fundo/borda/seleção/raio/padding de widget, cor de grade/eixos, paleta categórica, gradiente contínuo e `Color mappings` locais ao dashboard.

O tema do workspace e o tema local do dashboard têm escopos diferentes. Um dashboard existente recebe um **snapshot** ao aplicar o tema do workspace; alterações posteriores do tema do workspace não se propagam automaticamente. A reaplicação é manual.

## Arquivos

- [`aibi_theme.py`](aibi_theme.py): fachada pública de projeção, políticas locais e binder fail-closed;
- [`_aibi_theme_impl.py`](_aibi_theme_impl.py): implementação interna, não API alternativa;
- `aibi_mapping.json`: matriz canônica de correspondência dos 48 tokens `notebook`;
- `dashboard_sintetico.json`: fixture de dashboard para testes de semântica; **não é formato Databricks e não pode ser importado no Databricks**;
- `GUIA_PRIMEIRO_USO.md`: procedimento operacional para usuário não técnico.

## Limites

A ponte não:
- chama Databricks SDK/REST/CLI;
- cria dashboard;
- altera tema do workspace;
- importa arquivo de tema;
- publica dashboard;
- muda queries, filtros ou métricas;
- promete propagação universal;
- certifica o formato de JSON nativo sem um export real do ambiente.

Antes de aplicar um candidato, confirme export original, SHA-256, binding revisado, autorização e teste do destino. O ensaio histórico de importação aprovado para um dashboard draft não autoriza repetição, alteração de workspace theme ou Publish. Consulte a [evidência administrativa delimitada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/docs/sprints/sistema_temas/README.md).
