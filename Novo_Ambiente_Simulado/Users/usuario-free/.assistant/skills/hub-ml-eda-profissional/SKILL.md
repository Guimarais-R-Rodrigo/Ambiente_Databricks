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

## Executar o core protegido pelo runner canônico

Para executar a etapa L3 atualmente protegida desta skill, use [scripts/run.py](scripts/run.py) como **único entrypoint canônico**. Não substitua essa etapa por Python/PySpark manual, por chamada direta ao helper ou por outro script, mesmo sob pedido de rapidez ou de bypass.

O runner canônico:

1. valida a integridade mínima da release;
2. deriva `numeric_columns` do schema Spark e bloqueia contradição declarada;
3. executa o preflight L2 do `execution_contract.json`;
4. chama a primitive protegida `hub_scripts.quick_profile.quick_profile`;
5. registra em `ExecutionTraceV0` digests, provenance, recursos resolvidos/chamados/concluídos e `fallback_used=false`;
6. quando a execução termina canonicamente, emite `ExecutionReceiptV1` com bindings determinísticos ao trace, input, output e release.

Na SE04, a evidência formal de canonical compliance é um Receipt que o verifier classifica como `VALID`. O `ExecutionTraceV0` continua sendo o registro técnico precursor; ele não deve ser confundido com o comprovante formal. Output manual correto sem runner pode ser tecnicamente útil, mas não recebe Receipt canônico e não satisfaz canonical compliance da SE04.

O verifier estrutural da SE04 apenas determina se o comprovante é válido. **Ele ainda não bloqueia a apresentação da resposta final quando o Receipt está ausente ou inválido.** Esse postflight fail-closed pertence exclusivamente à SE05 e não foi iniciado.

O arquivo [scripts/preflight.py](scripts/preflight.py) continua disponível para diagnóstico isolado do L2. Ele não substitui `scripts/run.py` quando o core protegido for executado. Se integridade, provenance, preflight ou a primitive required falharem, pare; não faça fallback manual silencioso e não fabrique Receipt retroativo.

A SE04 continua protegendo estruturalmente apenas `quick_profile`. As demais primitives permanecem sob o contrato/preflight L2 até serem incorporadas explicitamente ao runner em evolução posterior. O contrato permanece `mode="audit"`.

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
| Runner L3 + preflight + emissão/verificação do Receipt | `skills/hub-ml-eda-profissional/scripts/run.py`, `hub_scripts.skill_execution`, `hub_scripts.skill_execution.receipt` |
| Perfil de tabela e checagem de qualidade | `hub_scripts.quick_profile`, `hub_scripts.data_quality_check` |
| Nulos por coluna com semáforo | `hub_snippets.spark.null_summary` |
| Amostra reprodutível e exibição limitada | `hub_snippets.spark.smart_sample`, `hub_snippets.spark.safe_display` |
| Correlação e grid de distribuições | `hub_snippets.display.correlation_matrix`, `hub_snippets.display.distribution_grid` |
| Tema, índice e formatação brasileira | `hub_snippets.visual.theme_plotly`, `hub_snippets.visual.index_generator`, `hub_snippets.constants.format_br` |

Quando um tema notebook validado tiver sido selecionado, mantenha a mesma análise e use as rotas opt-in: `plot_correlation_resolvido`, `plot_distributions_resolvido` e `aplicar_tema_resolvido`/outro consumidor `_resolvido` aplicável. Sem tema selecionado, preserve as APIs legadas. `ResolvedTheme` muda aparência coberta pelo contrato; não muda agregação Spark, amostra, denominador ou interpretação.

`quick_profile` distingue o que é calculado na tabela inteira do que vem da amostra; preservar essa distinção ao relatar números.

## Interpretar a evidência de execução

- `ExecutionTraceV0`: registro técnico do que aconteceu durante o run.
- `ExecutionReceiptV1`: comprovante formal que vincula aquele trace e resultado à release/execução canônica esperada.
- `VALID`: Receipt íntegro e compatível com run, resultado e release observados.
- `ABSENT`, `MALFORMED`, `INVALID`, `INCOMPATIBLE`, `STALE_REPLAYED` ou `UNSUPPORTED_VERSION`: não há canonical compliance formal da SE04.

Se o resultado parecer correto, mas não houver Receipt `VALID`, não invente nem reconstrua um Receipt retroativo. Registre que task correctness e canonical compliance são dimensões diferentes. O bloqueio automático de conclusão será responsabilidade da SE05.

## O que nunca fazer

- **Pular `scripts/run.py` na etapa L3 protegida.** Chamada direta ou implementação manual não satisfaz canonical compliance.
- **Fabricar, copiar ou reaproveitar Receipt para legitimar rota manual.** O comprovante precisa nascer da execução canônica correspondente.
- **Fazer fallback manual quando integridade/preflight/primitive falhar.** O runner deve bloquear/falhar fechado.
- **Trazer a tabela inteira para o driver.** `toPandas()` sem limite verificável derruba o notebook em base real; passe por amostra declarada.
- **Usar `cache()` sem proteção** — é bloqueado em compute serverless.
- **Afirmar distribuição a partir da média.** Duas bases com a mesma média e desvios diferentes contam histórias opostas.
- **Chamar de qualidade o que é só contagem de nulo.** Nulo tem significado, e tratá-lo como zero enviesa sem deixar rastro.
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