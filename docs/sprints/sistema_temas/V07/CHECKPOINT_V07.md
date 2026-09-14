# Checkpoint V07 — demais consumidores e formatos de saída

## Estado

**CANDIDATA EM EXECUÇÃO; SEM ACEITE, SEM PR DE INTEGRAÇÃO, SEM MERGE E SEM PUBLICAÇÃO DATABRICKS.**

A V07 foi iniciada em 14/09/2026 a partir da `main` em `0c0c71bce4bbc09130ec51eec8245057be4f3d81`, depois do fechamento documental da V06. A branch isolada é `codex/temas-v07-consumidores-formatos-20260914`.

Este checkpoint não antecipa aceite. O próximo gate é concluir documentação/métricas, obter um head final verde, revisar o diff, abrir PR draft e repetir os checks no SHA exato da candidata.

## Objetivo e decisão arquitetural

A V07 não cria novo catálogo de temas nem uma segunda resolução de configuração. `ResolvedTheme` continua sendo a fonte de verdade e `theme_plotly` continua sendo o adaptador Plotly central.

A mudança adiciona `get_tokens_plotly(theme)`, que passa pelas mesmas guardas fail-closed V02/V03 e devolve cópia dos tokens já revalidados. Consumidores com semântica própria podem então usar tokens como `palette.curves_legacy`, `palette.sequential`, `semantic.warning` e `semantic.negative` sem ler JSON, campos privados ou fixtures diretamente.

As rotas novas são opt-in e usam sufixo `_resolvido`. As APIs legadas permanecem disponíveis por padrão.

## Consumidores classificados

O registro estruturado está em [`CONSUMIDORES.json`](CONSUMIDORES.json).

### Suporte V07

- `display.correlation_matrix`: `plot_correlation_resolvido` / `plot_correlation_matrix_resolvido`;
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

As exceções possuem motivo, responsável e efeito visível no registro estruturado. Elas não são tratadas como suporte parcial implícito.

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

Os arquivos de implementação/fachada modificados foram sincronizados reutilizando os mesmos blobs Git entre `ambiente_fonte` e `Novo_Ambiente_Simulado`.

Sete READMEs operacionais também receberam notas V07 idênticas nos dois lados. `tools/tests/test_temas_v07_mirror.py` verifica byte a byte os arquivos de código/fachada e esses READMEs.

A migração dos READMEs longos foi feita por um script/workflow transitório para evitar reconstrução manual ou truncamento. Depois da escrita, o workflow V07 foi restaurado para `contents: read`, `persist-credentials: false`, e o script transitório foi removido da árvore permanente.

## Evidências até este checkpoint

### `34858836840` — FAILURE documental

Antes da validação documental:

- V07: **18/18 PASS**;
- regressões V01–V07: **382/382 PASS**;
- V00: **12/12 PASS**.

O run reprovou porque quatro fachadas `__init__.py` ainda não coincidiam com a saída canônica de `tools/api_publica.py` e porque o README raiz trazia métricas anteriores. As fachadas foram corrigidas conforme o contrato, sem filtrar testes nem relaxar o validador.

### `34859769442` — FAILURE documental preservado

A rodada transitória atualizou sete READMEs fonte/simulado e voltou a obter:

- V07: **18/18 PASS**;
- regressões V01–V07: **382/382 PASS**;
- V00: **12/12 PASS**.

O validador reprovou apenas a saída colada do README raiz. Naquele checkout mediu **1345 arquivos** na identidade do repositório e **1841 links fora da raiz**, contra 1339/1840 ainda registrados. A execução permanece `failure`; o mecanismo de escrita transitório foi removido depois da migração.

## Pendências para formar a candidata final

1. reconciliar os índices vivos com o estado **V07 candidata**, sem dizer que foi aceita ou integrada;
2. registrar V07 no changelog como candidata, preservando failures;
3. medir as métricas finais do README raiz depois de todos os documentos estáveis;
4. executar novamente V07, regressões V01–V07, V00 e validação documental;
5. executar o CI agregado no head final;
6. revisar diff e confirmar ausência de mecanismos transitórios;
7. confirmar que a `main` não avançou ou reconciliar a branch se necessário;
8. abrir PR draft e validar todos os checks no SHA exato;
9. parar para aceite explícito de Rodrigo antes de qualquer merge.

## Limites

Nenhuma publicação ou escrita remota no Databricks foi executada. Não houve alteração de ACL, compute, Spark/SQL/MLflow remoto, promoção visual, homologação de browser, acessibilidade ou UAT humano.

A V08 **não foi iniciada**.
