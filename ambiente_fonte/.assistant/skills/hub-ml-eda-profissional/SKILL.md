---
name: hub-ml-eda-profissional
description: Produz EDA profissional e escalável no Databricks com PySpark/Spark SQL, cobrindo granularidade, chaves, qualidade, distribuições, relações, visualizações agregadas e recomendações. Usar quando pedirem exploração, perfil, diagnóstico de base, qualidade inicial, análise uni/bivariada, notebook de EDA ou relatório executivo de uma fonte de dados.
---

# Produzir EDA profissional

## Quando esta skill se aplica

- Pedem **exploração, perfil, diagnóstico ou qualidade inicial** de uma fonte de
  dados, ou um notebook de EDA.
- A pergunta é sobre **uma** tabela ou uma base já consolidada.

**Não cobre:** cruzar múltiplas fontes (`hub-ml-cross-eda-ml`) nem executar
testes de hipótese com p-valor e effect size (`hub-ml-validacao-estatistica`).

## Definir escopo

Confirmar a pergunta, unidade de análise, data de corte, tabela, filtros, chave candidata e target. Se algo crítico estiver ausente, continuar com hipóteses explícitas e listar o que precisa ser confirmado.

## Executar o preflight antes do core

Antes de escrever ou executar lógica analítica protegida, execute [scripts/preflight.py](scripts/preflight.py) com contexto explícito para as condições do `execution_contract.json`. O contexto deve registrar, sem assumir silêncio como `false`, se há necessidade de amostra local, preview tabular, distribuições numéricas, tema resolvido, diagnósticos visuais e quantas colunas numéricas estão disponíveis após a inspeção de schema.

- `PASS`: os requisitos obrigatórios/aplicáveis estão resolvidos e o fluxo pode seguir para as nove etapas abaixo.
- `BLOCKED`: pare a execução canônica, preserve as issues estruturadas e informe o requisito ausente ou a condição não resolvida. Não substitua silenciosamente o helper/template por implementação manual.

O preflight é somente L2: ele não executa a EDA, não chama o core, não produz Execution Receipt e não autoriza alegar enforcement completo. O contrato continua `mode="audit"` nesta sprint.

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

Usar [templates/roteiro_eda.md](templates/roteiro_eda.md) para estruturar o notebook, [templates/matriz_graficos_eda.md](templates/matriz_graficos_eda.md) para selecionar visualizações e [templates/relatorio_executivo_eda.md](templates/relatorio_executivo_eda.md) para o resumo. Consultar [templates/estilo_visual_eda.md](templates/estilo_visual_eda.md) para composição e leitura da EDA. Paleta/tokens configuráveis vêm de `ResolvedTheme` e do padrão `hub_padroes/identidade_visual`; o template não é uma segunda fonte de tema.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Preflight do contrato antes do core | `hub_scripts.skill_execution` |
| Perfil de tabela e checagem de qualidade | `hub_scripts.quick_profile`, `hub_scripts.data_quality_check` |
| Nulos por coluna com semáforo | `hub_snippets.spark.null_summary` |
| Amostra reprodutível e exibição limitada | `hub_snippets.spark.smart_sample`, `hub_snippets.spark.safe_display` |
| Correlação e grid de distribuições | `hub_snippets.display.correlation_matrix`, `hub_snippets.display.distribution_grid` |
| Tema, índice e formatação brasileira | `hub_snippets.visual.theme_plotly`, `hub_snippets.visual.index_generator`, `hub_snippets.constants.format_br` |

Quando um tema notebook validado tiver sido selecionado, mantenha a mesma análise e use as rotas opt-in: `plot_correlation_resolvido`, `plot_distributions_resolvido` e `aplicar_tema_resolvido`/outro consumidor `_resolvido` aplicável. Sem tema selecionado, preserve as APIs legadas. `ResolvedTheme` muda aparência coberta pelo contrato; não muda agregação Spark, amostra, denominador ou interpretação.

`quick_profile` distingue o que é calculado na tabela inteira do que vem da amostra; preservar essa distinção ao relatar números.

## O que nunca fazer

- **Trazer a tabela inteira para o driver.** `toPandas()` sem limite verificável
  derruba o notebook em base real; passe por amostra declarada.
- **Usar `cache()` sem proteção** — é bloqueado em compute serverless.
- **Afirmar distribuição a partir da média.** Duas bases com a mesma média e
  desvios diferentes contam histórias opostas.
- **Chamar de qualidade o que é só contagem de nulo.** Nulo tem significado, e
  tratá-lo como zero enviesa sem deixar rastro.
- **Fechar a EDA sem dizer o que ela não olhou.**

## Handoff

Entregar um contrato com:

- fontes e snapshot;
- unidade, chaves e target;
- principais riscos de qualidade;
- features candidatas e suspeitas de leakage;
- filtros e amostra usados;
- perguntas ainda abertas.

Acionar `hub-ml-cross-eda-ml` para múltiplas fontes, `hub-ml-feature-engineering` para projetar features e `hub-ml-validacao-estatistica` quando a decisão exigir inferência.
