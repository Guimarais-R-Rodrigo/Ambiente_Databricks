# `x_snippets` — biblioteca Python customizada

> **EXTENSÃO CUSTOMIZADA (`x_`) — não auto-descoberta nem instalada pela Genie Code.**

Esta pasta preserva helpers reutilizáveis de notebook. Ela não é uma Agent Skill e
nenhum módulo é carregado automaticamente. Importe somente o que o notebook usa.

Para localizar o módulo a partir da demanda ("preciso calcular PSI", "preciso de
split temporal"), consulte o [catálogo de helpers](../x_docs/catalogo_helpers.md),
que cobre `x_snippets` e `x_scripts` e marca as dependências opcionais.

## Uso no Databricks

Se `.assistant` estiver no diretório do projeto/repositório:

```python
from pathlib import Path
import sys

project_root = Path.cwd()  # ajuste se o notebook estiver em uma subpasta
assistant_root = project_root / ".assistant"
if not assistant_root.is_dir():
    raise FileNotFoundError("Defina assistant_root para a pasta .assistant deste projeto")
sys.path.insert(0, str(assistant_root))

from x_snippets.visual.theme_plotly import aplicar_tema
from x_snippets.spark.null_summary import null_summary
from x_snippets.spark.safe_display import safe_display
```

Para uma instalação no diretório do usuário, use o caminho parametrizado
`/Workspace/Users/<username>/.assistant`; nunca copie um e-mail pessoal de um
exemplo. Em serverless, confirme as regras atuais para dependências e reinicie o
Python quando a instalação do notebook exigir.

## Onde procurar um módulo

O mapa completo — organizado por demanda, com função pública e dependências
marcadas — está em
[x_docs/catalogo_helpers.md](../x_docs/catalogo_helpers.md).

O catálogo é a lista mantida para **demanda → módulo**. A tabela de inventário
logo abaixo responde outra pergunta — "o que existe?" — e pode ficar para trás
quando a biblioteca mudar. Havendo divergência entre as duas, vale o catálogo.

### O que cada módulo faz

Visão de inventário — o que existe. Para o caminho inverso ("preciso fazer X,
qual módulo uso?"), o catálogo é a referência.

| Módulo | Em uma linha |
|---|---|
| `spark.pit_join` | junta histórico à decisão usando só o que já estava disponível |
| `spark.join_diagnostics` | mede cobertura, multiplicidade e expansão antes do join |
| `spark.psi_calculator` | PSI e CSI comparando formas de distribuição, bins da referência |
| `spark.null_summary` | nulos por coluna com semáforo |
| `spark.smart_sample` | amostra reprodutível, estratificada quando pedido |
| `spark.safe_display` | exibe DataFrame grande sem varredura completa |
| `spark.date_features` | features de calendário, com feriados do projeto |
| `ml.split_temporal` | separa treino e teste por período, não por sorteio |
| `ml.walk_forward` | validação que avança no tempo, retreinando a cada janela |
| `ml.metrics_report` | métricas de classificação e regressão padronizadas |
| `ml.curves_plotly` | curvas ROC, PR, lift e KS |
| `ml.train_lgbm`, `.train_xgboost`, `.train_catboost` | baselines tabulares com MLflow opcional |
| `ml.optuna_lgbm` | busca de hiperparâmetros |
| `ml.lgbm_ranker` | ranking com LambdaRank e NDCG |
| `ml.mlflow_run` | registro que exige dataset, split, assinatura e limitações |
| `ml.scorecard_builder` | converte modelo logístico em pontos |
| `ml.score_bands` | bandas de score com direção declarada |
| `ml.woe_iv_calculator` | WOE e Information Value |
| `ml.shap_explainer` | SHAP: cálculo, importância e gráficos |
| `ml.explainability_report` | relatório executivo e técnico de explicabilidade |
| `ml.drift_detection` | PSI, KS e CSI driver-side, sobre amostra |
| `ml.performance_monitor` | acompanha métricas contra política calibrada |
| `ml.vintage_analysis` | safras: tabela, curvas de maturação e heatmap |
| `ml.survival_cox`, `.kaplan_meier` | sobrevivência e teste log-rank |
| `ml.prophet_wrapper`, `.arima_wrapper` | séries temporais |
| `ml.clustering_suite`, `.cluster_profiling` | seleção de k, pipeline e profiling |
| `ml.isolation_forest`, `.autoencoder_anomaly` | detecção de anomalia |
| `ml.umap_viz` | projeção 2D para visualizar grupos |
| `ml.mlp_embeddings`, `.tabnet_wrapper` | redes para dados tabulares |
| `ml.lgbm_temporal` | lags e janelas móveis por entidade |
| `display.correlation_matrix`, `.distribution_grid`, `.dataframe_styled` | gráficos e tabelas de exploração |
| `visual.theme_plotly`, `.kpi_card`, `.badge`, `.section_header`, `.divider`, `.index_generator` | identidade visual do notebook |
| `constants.format_br`, `.colors`, `.emojis`, `.styles` | formatação brasileira, paleta e estilos |
| `testing.fixtures` | bases sintéticas determinísticas para teste e exemplo |

### Material didático

Quatro notebooks executáveis explicam, sobre fixtures sintéticas, os conceitos
onde o erro custa mais caro. Cada um mostra o problema acontecendo antes de
apresentar a solução:

Todos ficam em `x_docs/notebooks/`. **No workspace do Databricks eles aparecem
como notebook e sem a extensão `.py`** — abra pelo navegador de arquivos, não
pelo link, se estiver lendo este documento dentro do Databricks.

| Notebook | Cobre |
|---|---|
| `01_vazamento_temporal` | `pit_join` e `split_temporal`: como dado do futuro entra no treino |
| `02_drift_e_estabilidade` | `psi_calculator`: o que o PSI mede, e por que comparar médias não é PSI |
| `03_qualidade_de_juncao` | `join_diagnostics`: quando o join infla, encolhe ou perde linhas |
| `04_armadilhas_de_credito` | `vintage_analysis` e `woe_iv_calculator`: somar taxas de safra e celebrar IV alto |

Para explicação linha a linha de qualquer outro módulo, use
`@rodrigo-tutor-databricks` com o arquivo anexado — ela lê a versão atual, então
não fica defasada.

### Como se localizar

| Sua pergunta | Onde responder |
|---|---|
| "o que existe nesta biblioteca?" | a tabela de módulos acima |
| "preciso fazer X, qual módulo uso?" | [catálogo de helpers](../x_docs/catalogo_helpers.md) |
| "por que este helper existe e o que dá errado sem ele?" | os quatro notebooks |
| "o que esta linha do código faz?" | `@rodrigo-tutor-databricks` com o módulo anexado |
| "o que significa este termo?" | [glossário](../x_docs/glossario.md) |

### Agrupamento por pacote

| Pacote | Finalidade | Cuidados |
|---|---|---|
| `constants` | cores, estilos, emojis e formatação BR | a paleta é customizada, não Databricks |
| `visual` | tema Plotly, cabeçalhos, badges, KPIs e índice | o HTML gerado escapa o texto recebido |
| `spark` | nulos, amostragem, display, datas e PSI | ações Spark têm custo; declare amostra e referência |
| `display` | correlação, distribuições e tabela estilizada | conversão ao driver é sempre limitada |
| `ml` | baselines, validação, drift, SHAP, séries, survival e monitoramento | dependências opcionais; valide versão e runtime |
| `testing` | fixtures sintéticas determinísticas | só para teste e exemplo; nunca imita base real |

Use `requirements-optional.txt` como inventário, não como lockfile universal. Instale
somente o subconjunto necessário e registre versões no projeto consumidor.

## Quando o import falha

| Mensagem | Causa | Correção |
|---|---|---|
| `ModuleNotFoundError: No module named 'x_snippets'` | foi adicionada ao `sys.path` a pasta `x_snippets` | adicione a `.assistant`, que a contém |
| `ModuleNotFoundError: No module named 'lightgbm'` (ou `xgboost`, `catboost`, `optuna`, `torch`) | dependência opcional exigida já no import | instale com versão fixada, ou use outro módulo do catálogo |
| Import passa e o erro só aparece ao chamar a função | dependência opcional resolvida na chamada — caso de SHAP, lifelines, Prophet, UMAP, TabNet e ARIMA | mesma correção; o catálogo marca esses casos |
| `NOT_SUPPORTED_WITH_SERVERLESS: PERSIST TABLE` | código novo chamando `cache()` em compute serverless | remova o cache; os helpers já operam sem ele |
| `NameError: name 'spark' is not defined` | código novo contando com a variável global de notebook dentro de um módulo | resolva a sessão com `SparkSession.getActiveSession()` |

As três últimas linhas vieram de falhas reais encontradas ao executar a
biblioteca no runtime, não de suposição.

## Contrato de segurança

- Não use `toPandas()` sem limite verificável.
- Em dados temporais, ajuste preprocessamento apenas no treino e respeite o instante
  de decisão.
- Em dados por entidade, informe a chave para lags/janelas.
- Defina explicitamente classe positiva e direção do score.
- PSI e thresholds de alerta são heurísticas calibráveis.
- Não silencie exceções com sentinelas como `-1`; retorne diagnóstico ou falhe.

## Verificação rápida

```python
from x_snippets.constants.format_br import fmt_brl, fmt_pct

assert fmt_brl(1.999) == "R$ 2,00"
assert fmt_pct(1.0) == "100,0%"              # escala ratio
assert fmt_pct(1.0, input_scale="percent") == "1,0%"
```

Após alterar os módulos, execute os testes locais e a compilação sintática. O fato de
um arquivo importar não comprova compatibilidade com o runtime Spark do workspace.
