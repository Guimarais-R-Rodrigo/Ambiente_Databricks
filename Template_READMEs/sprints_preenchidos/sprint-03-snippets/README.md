![CRM — Missão Modelos Analíticos CRM](../hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Hub Snippets

> A biblioteca matemática e algorítmica central do ecossistema `.assistant`: funções e classes reutilizáveis, revisadas e testadas para fluxos de Machine Learning e Big Data no Databricks.

> **CONTEÚDO CUSTOMIZADO PELO HUB.** `hub_snippets` não é uma biblioteca institucional da Databricks nem é carregada automaticamente pela Genie Code. O notebook precisa tornar o pacote visível ao Python e importar explicitamente a função desejada.

> **Rascunho de sprint 3 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/hub_snippets/README.md`.

---

## 🧭 Neste Guia

**Pacote** é a árvore `hub_snippets`. **Módulo** é o arquivo `.py` da pasta do objeto. **Função/classe** é o que o `__init__.py` reexporta. Ver uma linha `from ... import ...` não ensina o contrato.

| Para entender... | Vá para... |
|---|---|
| o conceito e a estrutura de um snippet | [O que é um Snippet](#-o-que-é-um-snippet-neste-ecossistema) |
| as categorias da biblioteca | [Mapa de Categorias](#-mapa-de-categorias-do-hub-snippets) |
| quais objetos estão disponíveis | [Catálogo Detalhado](#-catálogo-detalhado-por-categoria) |
| como importar e executar | [Passo a Passo Operacional](#️-passo-a-passo-operacional-como-usar-um-snippet) |
| runtime, dependências e custo | [Onde o Código Executa](#️-onde-o-código-executa-e-quanto-pode-custar) |
| dúvidas e limitações | [Perguntas Frequentes](#-perguntas-frequentes-faq) |

**Percurso de quem nunca reutilizou módulo:** conceito → pasta de objeto → passo a passo com `fmt_int` (conta à mão) → catálogo da família que você precisa.

---

## 🧩 O que é um Snippet neste Ecossistema?

Na internet, “snippet” costuma ser trecho copiado. **Aqui, é peça de engenharia analítica com contrato:** API pública, implementação, exemplo e limites.

Copiar código espalha versões. Importar um módulo mantido concentra a correção. A responsabilidade de validar assinatura, volume e significado de negócio continua sua.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                            O QUE DEFINE UM SNIPPET                          │
│                                                                             │
│   Efeito declarado · Lógica revisável · Execução adequada ao volume         │
│   Evidência delimitada nos testes e no notebook de exemplo                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

Na campanha fictícia: em vez de reimplementar split por linha (que vaza futuro), você chama `temporal_split` com períodos de calendário.

---

## 🏛️ Arquitetura e o Padrão "Pasta de Objeto"

![Anatomia da pasta de um snippet](../hub_readmes_visual_assets/readmes/snippets/png/01_anatomia_pasta.png)

*Leitura da figura: `__init__.py` é o ponto estável de import; o `.py` homônimo é o motor; `exemplo_*.py` demonstra a chamada — não é o módulo importado.*

### O que cada arquivo faz

1. **`__init__.py` (fachada).** Reexporta a API. Você lê para saber o nome público; não executa análise ao abrir.
2. **`nome_do_snippet.py` (motor).** Implementação, validações, docstring. Fonte da assinatura real.
3. **`exemplo_nome_do_snippet.py` (guia).** Dados sintéticos e saída observada. Ensina o contrato exercitado; não promete qualquer runtime.

Leitura guiada — `split_temporal/`:

- Comece pelo exemplo para ver `temporal_split(...)`.
- Confira parâmetros no motor (`train_pct`, `val_pct`, `gap_periods`, `period_unit`, `group_col`).
- Importe de `hub_snippets.ml.split_temporal`, não rode o exemplo como se fosse a biblioteca.

O [Catálogo de Helpers](../CATALOGO_HELPERS.md) é o índice canônico demanda → caminho.

---

## 🗺️ Mapa de Categorias do Hub Snippets

![Mapa das categorias funcionais do Hub Snippets](../hub_readmes_visual_assets/readmes/snippets/png/02_mapa_categorias.png)

*Leitura da figura: as seis categorias agrupam pelo tipo de problema, não por “importância”.*

| Categoria | Pergunta cotidiana | Não confundir com |
|---|---|---|
| `ml` | Como parto no tempo / meço / treino? | script de qualidade da tabela |
| `spark` | Como faço isso em DataFrame Spark? | pandas no driver |
| `display` | Como mostro tabela no notebook? | tema Plotly (`visual`) |
| `visual` | Como mantenho identidade gráfica? | cálculo de métrica (`ml`) |
| `constants` | Como formato número em pt-BR? | regra de negócio |
| `testing` | Como gero dado sintético? | dado real da campanha |

---

## 📚 Catálogo Detalhado por Categoria

Cada item: problema, quando usar / não usar, import. Detalhe extensivo no `exemplo_*.py`. Um exemplo completo por família crítica aparece no passo a passo e abaixo em `constants` e `ml` temporal.

### 1. Categoria: `ml`

Família de modelagem, tempo, risco, métricas e monitoramento. Dependências opcionais (LightGBM, SHAP, CatBoost, Prophet, etc.) falham no import se ausentes — isso não é defeito silencioso do Hub.

#### Engenharia temporal e séries

| Objeto | Problema | Quando usar | Quando não usar |
|---|---|---|---|
| `lgbm_temporal` | lags/rolling + treino LightGBM | série com data já válida; LightGBM instalado | data textual ambígua sem `date_format` |
| `split_temporal` | treino/val/teste por **período de calendário** | avaliação temporal | split aleatório por linha |
| `walk_forward` | janelas sucessivas | estabilidade ao longo de cortes | um único holdout |
| `vintage_analysis` | curvas de safra / MOB | evento, denominador e censura definidos | taxa “do mês” sem coorte |

**Exemplo completo — `temporal_split`.** Evita vazar o futuro ao cortar pelas linhas mais recentes misturadas no meio.

```python
import pandas as pd
from hub_snippets.ml.split_temporal import temporal_split

df = pd.DataFrame({
    "dt_evento": pd.date_range("2025-01-01", periods=12, freq="MS"),
    "respondeu": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
})
treino, val, teste = temporal_split(
    df, date_col="dt_evento", train_pct=0.50, val_pct=0.25, gap_periods=1, period_unit="M"
)
```

São 12 meses. A função exige períodos suficientes para treino, gaps e teste. **Não** existem parâmetros `train_end`/`val_end`. `group_col` torna o split disjunto por entidade; omita-o se a mesma entidade deve aparecer nas janelas (previsão em painel).

**Interpretação.** Cada partição contém meses completos. O gap é mês deixado de fora entre partições, de propósito.

**Se não funcionou.** `at least N periods are required`: a série é curta demais para os gaps pedidos.

#### Risco de crédito e scorecards

`woe_iv_calculator` — WOE/IV nos tipos suportados; binning e target são seus.  
`scorecard_builder` — logístico compatível → pontos; transparência ≠ aprovação regulatória.  
`score_bands` — faixas de score; política de corte é externa. Recusa score constante.

#### Avaliação e visualização

`metrics_report` — AUC, Gini, KS (`ks_pct` em 0–100), F1, LogLoss, Brier quando couber.  
`curves_plotly` — ROC/PR/ganho/KS; Plotly opcional.  
`explainability_report` — importância e explicações; não é causalidade.

#### Monitoramento e MLOps

`performance_monitor` — compara métricas a limiares quando **chamado**. Não agenda, não alerta, não retreina. Use `selecionar_metricas_do_relatorio` para mapear `auc_roc` → `auc`.  
`drift_detection` — mudança de distribuição.  
`mlflow_run` — wrapper de run; efeito externo intencional. No Free serverless a abertura de run pode estar bloqueada (evidência de laboratório, não lei da plataforma).

#### Não supervisionado e demais `ml`

`clustering_suite`, `cluster_profiling`, `isolation_forest` — agrupamento/anomalia; anomalia ≠ fraude.  
Também no inventário: `arima_wrapper`, `autoencoder_anomaly`, `kaplan_meier`, `lgbm_ranker`, `mlp_embeddings`, `optuna_lgbm`, `prophet_wrapper`, `shap_explainer`, `survival_cox`, `tabnet_wrapper`, `train_catboost`, `train_lgbm`, `train_xgboost`, `umap_viz`. Cada um tem pasta, exemplo e dependência própria — confirme no catálogo antes de importar.

### 2. Categoria: `spark`

Operações em PySpark. Agregados podem ser coletados no driver; a tabela inteira não deve ser.

| Objeto | Problema | Nota de contrato |
|---|---|---|
| `pit_join` | feature disponível até o instante de decisão | chaves, duplicidade e atraso de publicação são seus |
| `psi_calculator` | PSI numérico / CSI categórico | CSI limita cardinalidade antes do `collect` |
| `null_summary` | nulos Spark | tabela larga custa |
| `smart_sample` | amostra simples ou estratificada | amostra ≠ representatividade automática |
| `date_features` | atributos de calendário | timezone e disponibilidade |
| `join_diagnostics` | cobertura/duplicidade/expansão | API: `diagnosticar_join` |
| `safe_display` | limitar exibição | não torna o scan anterior barato |

### 3–6. `display`, `visual`, `constants`, `testing`

`dataframe_styled`, `distribution_grid`, `correlation_matrix` — pandas no driver.  
`theme_plotly`, `section_header`, `badge`, `divider`, `index_generator`, `kpi_card` — identidade; tema global é efeito de sessão.  
`colors`, `styles`, `emojis`, `format_br` — paleta e formatação.  
`fixtures` — sintético para teste; não é a campanha real.

**Exemplo completo — `fmt_int` / `fmt_pct` (conta à mão).**

```python
from hub_snippets.constants.format_br import fmt_int, fmt_pct, fmt_brl

fmt_int(3375674)   # "3.375.674"
fmt_pct(0.928)     # "92,8%"
fmt_brl(12345.67)  # "R$ 12.345,67"
```

`fmt_pct` assume razão 0–1 por padrão (`input_scale="ratio"`). Passar `92.8` sem `input_scale="percent"` formata errado. `fmt_int` não acrescenta unidade.

### Inventário completo

```text
hub_snippets/
├── constants/   colors emojis format_br styles
├── display/     correlation_matrix dataframe_styled distribution_grid
├── ml/          (objetos listados acima)
├── spark/       date_features join_diagnostics null_summary pit_join
│                psi_calculator safe_display smart_sample
├── testing/     fixtures
└── visual/      badge divider index_generator kpi_card section_header theme_plotly
```

---

## 🔐 O Contrato de Reuso

![Contrato de reuso dos snippets](../hub_readmes_visual_assets/readmes/snippets/png/04_contrato_de_reuso.png)

*Leitura da figura: interface previsível, execução consciente e evidência conferida. Faltar um dos três não é “reuso” — é cópia opaca.*

---

## 🛠️ Passo a Passo Operacional: Como Usar um Snippet

![Fluxo operacional para usar um snippet](../hub_readmes_visual_assets/readmes/snippets/png/03_fluxo_operacional.png)

*Leitura da figura: consultar o exemplo, tornar o pacote visível, importar a API real e validar o retorno.*

### Passo 1 — Inspecione o notebook modelo

Abra `exemplo_<snippet>.py`. Confira função, dados sintéticos e forma da saída.

### Passo 2 — Path

```python
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))
```

A pasta `.assistant` não entra no `sys.path` só por existir. Em serverless, o Environment/Git folder pode declarar dependências; isso **não** substitui o path do Hub.

### Passo 3 — Import e chamada reais

```python
from hub_snippets.ml.split_temporal import temporal_split
from hub_snippets.spark.psi_calculator import calcular_psi
```

### Passo 4 — Interprete

Confira tipo, unidade e schema. Threshold é política analítica, não constante universal. Registre versão e população quando houver decisão.

**Se não funcionou.** `ModuleNotFoundError: hub_snippets` → path. `ImportError` de biblioteca opcional → instale só ela. Assinatura diferente da memória → leia o `.py`, não o README antigo.

---

## ⚙️ Onde o Código Executa e Quanto Pode Custar

| Família | Onde roda | Atenção |
|---|---|---|
| pandas / sklearn | driver | memória, conversão Spark→pandas |
| PySpark | cluster + agregados no driver | shuffle, cardinalidade, `collect` |
| Plotly / HTML | driver + navegador | tamanho da figura |
| MLflow | serviço configurado | runs persistentes |
| opcionais | compute | versão e política de instalação |

Não existe helper universalmente rápido.

---

## ❓ Perguntas Frequentes (FAQ)

### 1. Os snippets alteram o DataFrame original?

A maior parte devolve objeto novo. Tema Plotly de sessão, MLflow e treinadores têm efeito. Leia a docstring.

### 2. Funcionam em serverless?

Depende do snippet e das bibliotecas. Serverless não torna `.assistant` importável automaticamente.

### 3. Faltou LightGBM ou Tabulate?

O módulo falha no import da dependência, em geral com `ImportError` orientado. Consulte o catálogo.

### 4. Como o Spark lida com tabela grande?

Prioriza operação distribuída; coleta **agregados** ou amostras. Controle cardinalidade.

### 5. A Genie Code executa snippets sozinha?

Não. Skill pode recomendar o caminho; o notebook importa.

### 6. Posso propor um snippet novo?

Sim: [`hub_padroes`](../hub_padroes/README.md) e `@hub-ml-criar-objeto`.

---

## 🔗 Continue Explorando

- [Catálogo de Helpers](../CATALOGO_HELPERS.md)
- [Hub Scripts](../hub_scripts/README.md)
- [Agent Skills](../skills/README.md)
- [Hub Prompts](../hub_prompts/README.md)
- [Dependências serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies)
- [Arquivos no workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace)
