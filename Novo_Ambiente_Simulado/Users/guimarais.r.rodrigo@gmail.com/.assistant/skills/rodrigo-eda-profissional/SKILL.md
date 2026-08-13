---
name: rodrigo-eda-profissional
description: Produz EDA profissional e escalável no Databricks com PySpark/Spark SQL, cobrindo granularidade, chaves, qualidade, distribuições, relações, visualizações agregadas e recomendações. Usar quando pedirem exploração, perfil, diagnóstico de base, qualidade inicial, análise uni/bivariada, notebook de EDA ou relatório executivo de uma fonte de dados.
---

# Produzir EDA profissional

## Definir escopo

Confirmar a pergunta, unidade de análise, data de corte, tabela, filtros, chave candidata e target. Se algo crítico estiver ausente, continuar com hipóteses explícitas e listar o que precisa ser confirmado.

## Executar em nove etapas

1. **Contextualizar:** registrar objetivo, fontes, snapshot, filtros e limitações.
2. **Inventariar:** obter schema, tipos, estimativa/contagem necessária, partições e período coberto.
3. **Validar granularidade:** medir unicidade, duplicidades, cardinalidade e consistência das chaves.
4. **Medir qualidade:** nulos, vazios, domínios, ranges, datas inválidas e regras de negócio.
5. **Analisar numerais:** percentis robustos, assimetria, zeros, sinal, caudas e outliers contextualizados.
6. **Analisar categorias:** frequência, cobertura acumulada, raridade, valores inesperados e cardinalidade.
7. **Analisar relações:** target, tempo, segmentos e redundância; escolher método compatível com os tipos.
8. **Visualizar:** agregar no Spark, limitar categorias e coletar somente o resultado pequeno para Plotly.
9. **Concluir:** separar fatos, hipóteses, impacto e ações priorizadas.

## Trabalhar de forma escalável

- Preferir agregações PySpark/Spark SQL.
- Evitar `toPandas()` sobre a base completa. Registrar limite, estratégia de amostragem e seed.
- Evitar múltiplos `count()` sem necessidade; persistir apenas quando houver reutilização comprovada e liberar cache.
- Usar `approxQuantile`/`percentile_approx` quando a precisão aproximada for adequada.
- Não exibir todas as categorias ou linhas. Mostrar top-N, cauda e “outros”.
- Mascarar ou agregar PII e dados sensíveis.

## Escolher testes e gráficos pelo dado

Não impor uma matriz fixa. Exemplos:

- numérica: histograma amostrado/agregado, ECDF ou box plot por grupo;
- categórica: barras ordenadas com denominador explícito;
- temporal: série com frequência regular e cobertura;
- target binário: distribuição por classe, AUC apenas se houver score, taxas com volume;
- correlação: Pearson para relação linear, Spearman para monotonicidade, associação apropriada para categóricas.

Rotular unidade, janela e denominador. Não confundir correlação com causalidade.

## Entregar recomendações acionáveis

Para cada achado relevante, informar:

- evidência e população afetada;
- possível impacto em análise/modelo/processo;
- hipótese de causa;
- ação recomendada;
- validação de aceite.

Usar [templates/roteiro_eda.md](templates/roteiro_eda.md) para estruturar o notebook, [templates/matriz_graficos_eda.md](templates/matriz_graficos_eda.md) para selecionar visualizações e [templates/relatorio_executivo_eda.md](templates/relatorio_executivo_eda.md) para o resumo. Consultar [templates/estilo_visual_eda.md](templates/estilo_visual_eda.md) apenas para orientação visual customizada, não como API nativa Databricks.

## Handoff

Entregar um contrato com:

- fontes e snapshot;
- unidade, chaves e target;
- principais riscos de qualidade;
- features candidatas e suspeitas de leakage;
- filtros e amostra usados;
- perguntas ainda abertas.

Acionar `rodrigo-cross-eda-ml` para múltiplas fontes, `rodrigo-feature-engineering` para projetar features e `rodrigo-validacao-estatistica` quando a decisão exigir inferência.
