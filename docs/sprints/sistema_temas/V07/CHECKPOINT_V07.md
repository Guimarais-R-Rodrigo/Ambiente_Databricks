# Checkpoint V07 — demais consumidores e formatos de saída

## Estado final

**ACEITA E INTEGRADA NO GIT EM 14/09/2026. SEM PUBLICAÇÃO DATABRICKS.**

Rodrigo autorizou explicitamente a aprovação e integração da V07. A PR #40 foi integrada com o head final `6b50151738a311eff8530c3191e24693af3fb036`; o merge efetivo na `main` é `67114605c7345a01c1144e5d6c6d24e9c24e2491`. A árvore do merge é `5438288bda2326e96372c7464b3aef0cb8375102`, idêntica à árvore do head final validado.

A V07 havia sido iniciada a partir da `main` em `0c0c71bce4bbc09130ec51eec8245057be4f3d81`, na branch `codex/temas-v07-consumidores-formatos-20260914`.

## Objetivo e decisão arquitetural

A V07 não cria novo catálogo de temas nem uma segunda resolução de configuração. `ResolvedTheme` continua sendo a fonte de verdade e `theme_plotly` continua sendo o adaptador Plotly central.

A mudança adiciona `get_tokens_plotly(theme)`, que passa pelas mesmas guardas fail-closed V02/V03 e devolve cópia dos tokens já revalidados. Consumidores com semântica própria podem usar tokens como `palette.curves_legacy`, `palette.diverging`, `palette.sequential`, `semantic.warning` e `semantic.negative` sem ler JSON, campos privados ou fixtures diretamente.

As rotas novas são opt-in e usam sufixo `_resolvido`. As APIs legadas permanecem disponíveis por padrão.

## Consumidores classificados

O registro estruturado está em [`CONSUMIDORES.json`](CONSUMIDORES.json).

### Suporte V07

- `display.correlation_matrix`: `plot_correlation_resolvido` / `plot_correlation_matrix_resolvido`, com `palette.diverging`;
- `display.distribution_grid`: `plot_distributions_resolvido` / `plot_distribution_grid_resolvido`;
- `ml.curves_plotly`: ROC, Precision–Recall, Lift e KS com rotas `_resolvido`;
- `ml.performance_monitor`: `PerformanceMonitor.plot_timeline_resolvido`;
- `ml.umap_viz`: `plot_umap_clusters_resolvido`;
- `ml.vintage_analysis`: curvas e heatmap `_resolvido`.

### Já coberto antes da V07

- `display.dataframe_styled`: integração por `display_styled_resolvido` pertence à V04 e não foi duplicada.

### Exceções explícitas

- `ml.kaplan_meier`: permanece legado porque sua ordem histórica própria de oito cores não possui hoje um token que a represente sem remapeamento silencioso de grupos;
- `ml.shap_explainer`: permanece legado porque SHAP/Matplotlib controla aparência própria e o contrato vigente não define colormap/estilo SHAP nem exportação estática tematizada.

## Invariantes analíticas

A V07 separa aparência de cálculo:

- correlação Spark, método e pares fortes permanecem no mesmo caminho;
- `smart_sample` continua sendo a única amostragem da grade de distribuições;
- AUC, AP, Lift e KS usam a mesma lógica das rotas legadas;
- política, thresholds, histórico e decisão do `PerformanceMonitor` não mudam;
- `compute_umap` continua sendo a única rotina de embedding;
- `build_vintage_table` e `compare_safras` não recebem lógica de tema;
- rotas resolvidas de vintage reutilizam os mesmos pontos/matriz das rotas legadas.

## Formatos de saída

Suporte exercitado na V07:

- figura Plotly em memória/notebook;
- arquivo HTML local gerado da própria figura Plotly, com JS embutido no teste.

Já coberto em outra sprint:

- HTML de `pandas.Styler` pela V04.

Permanecem fora do aceite V07:

- PNG estático Plotly/Kaleido;
- PDF;
- PPTX;
- render real no navegador Databricks;
- acessibilidade do render final;
- PNG/tela SHAP tematizados.

## Fonte e ambiente simulado

Os arquivos de implementação/fachada modificados foram sincronizados entre `ambiente_fonte` e `Novo_Ambiente_Simulado`. Sete READMEs operacionais receberam notas V07 idênticas nos dois lados, e `tools/tests/test_temas_v07_mirror.py` verifica os arquivos cobertos byte a byte.

Mecanismos de escrita utilizados apenas durante migrações controladas foram removidos antes da candidata final. O workflow permanente V07 está com `contents: read` e `persist-credentials: false`.

## Evidências finais

Failures históricos permanecem failures e não foram reclassificados: `34858836840`, `34859769442` e `34860697409`. Eles registram problemas documentais reais encontrados e corrigidos durante a sprint.

Após a correção semântica da correlação, os sucessos permanentes culminaram no head final `6b50151738a311eff8530c3191e24693af3fb036`:

- run V07 pré-PR `34862446870`: 19/19 V07, 383/383 regressões V01–V07, 12/12 V00, validador 0 falhas/0 avisos;
- os sete checks de `pull_request` no mesmo head concluíram com `success`;
- PR #40 integrada sem mover o head da candidata;
- merge commit `67114605c7345a01c1144e5d6c6d24e9c24e2491` preserva a mesma árvore da candidata.

### Pós-merge na `main`

O push do merge disparou nove workflows/checks, todos com `success`:

- V00: `34863452273`;
- V01: `34863452340`;
- V02: `34863452364`;
- V03: `34863452332`;
- V04: `34863452339`;
- V05: `34863452252`;
- V06: `34863452347`;
- V07: `34863452328`;
- CI geral: `34863452363`.

## Limites

Nenhuma publicação ou escrita remota no Databricks foi executada. Não houve alteração de ACL, compute, Spark/SQL/MLflow remoto, promoção visual, homologação de browser, acessibilidade ou UAT humano.

O encerramento da V07 autoriza apenas a continuidade do plano de sprints já aprovado. A V08 começa em branch própria a partir da `main` estabilizada; ela não deve reinterpretar o aceite V07 como homologação operacional no Databricks.
