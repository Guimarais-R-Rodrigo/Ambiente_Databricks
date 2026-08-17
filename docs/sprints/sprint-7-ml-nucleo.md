# Sprint 7 — `hub_snippets/ml`, os 16 módulos de núcleo

Data: 2026-08-17 · Executor: Claude · Escopo:
`ambiente_fonte/.assistant/hub_snippets/ml/`, limitado aos módulos que importam
sem dependência opcional. Os 14 restantes são a Sprint 8.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 0 aviso(s)
                        33 pastas de objeto · 33 pares módulo/notebook
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
smoke test (job real)   109 verificações | 102 PASS | 0 FAIL | 7 opcionais ausentes
```

Os 16 notebooks executaram como job no laboratório:

```text
exemplo_split_temporal      SUCCESS    exemplo_metrics_report      SUCCESS
exemplo_walk_forward        SUCCESS    exemplo_curves_plotly       SUCCESS
exemplo_scorecard_builder   SUCCESS    exemplo_score_bands         SUCCESS
exemplo_woe_iv_calculator   SUCCESS    exemplo_mlflow_run          SUCCESS
exemplo_drift_detection     SUCCESS    exemplo_performance_monitor SUCCESS
exemplo_vintage_analysis    SUCCESS    exemplo_explainability_report SUCCESS
exemplo_clustering_suite    SUCCESS    exemplo_cluster_profiling   SUCCESS
exemplo_isolation_forest    SUCCESS    exemplo_lgbm_temporal       SUCCESS
```

## O achado da sprint: uma dependência que nenhum portão enxerga

`explainability_report` está na lista de "núcleo, sem dependência opcional" — e a
lista está certa quanto ao critério que a produziu. O módulo não tem
`import tabulate` em lugar nenhum. O smoke test o importa com `PASS`. A validação
o aprova. E o notebook falha:

```text
ImportError: Missing optional dependency 'tabulate'.
```

A dependência entra por uma linha só, no meio do módulo:

```python
report += shap_importance.to_markdown(index=False) + "\n\n"
```

`DataFrame.to_markdown()` é do pandas, mas o pandas delega a formatação ao
`tabulate` **no momento da chamada**. Nenhuma análise estática de import de topo
encontra isso, e nenhum teste que só importa o módulo também.

A consequência prática é que a divisão 16/14 herdada de
`docs/testes/spark/README.md` é exata sobre **importabilidade** e não sobre
**executabilidade**. São coisas diferentes, e até esta sprint o projeto tratava
como se fossem a mesma.

Duas correções, nenhuma delas na assinatura do módulo:

| Onde | O que |
|---|---|
| `exemplo_explainability_report.py` | a célula do resumo técnico usa o BLOCO CANÔNICO de não executado, com o motivo verificado; a célula do relatório executivo continua executando, porque `generate_executive_report` monta o texto à mão |
| `requirements-optional.txt` | `tabulate==0.9.0` registrado numa seção própria, marcada como dependência **escondida**, com a explicação de por que a classificação por import não a encontra |

Trocar `to_markdown()` por formatação própria muda a saída do módulo, e por isso
é etapa 2 — a etapa 1 não altera comportamento.

## Seis notebooks escritos contra API imaginada

Escrevi os dezesseis notebooks a partir das docstrings e das assinaturas. Seis
falharam na primeira execução, e os seis erros são meus, não dos módulos:

| Notebook | O que eu supus | O que a API é |
|---|---|---|
| `scorecard_builder` | coeficientes em dicionário; tabela WOE com coluna `bin` | coeficientes em array; a coluna chama-se `faixa` |
| `walk_forward` | `model_fn` devolve o modelo | `model_fn` devolve um dicionário de métricas |
| `performance_monitor` | construtor com `thresholds` | `baseline_metrics` + `policy`; o método é `add_period` |
| `explainability_report` | importância SHAP com `importance` | exige a coluna `pct_importance` |
| `drift_detection` | `calculate_ks` devolve um número | devolve uma tupla |
| `drift_detection` | `feature_cols` opcional | é posicional e obrigatório: declara o universo, e as duas listas seguintes dizem como tratar cada coluna dele |

Nenhum deles foi pego pela validação, porque nenhum é erro de forma. Um deles —
o `pct_importance` — teria sido pego pelo `check_contrato_de_dados` se a coluna
viesse de um dicionário do módulo em vez de ser exigida na entrada. A guarda
cobre o que o módulo **produz**; estes seis são sobre o que ele **recebe**.

**A lição operacional é a mesma da Sprint 6, agora quantificada:** escrever
notebook a partir de docstring acerta em dez de dezesseis. A execução real não é
conferência final, é parte da escrita.

## A pasta de trânsito acabou

`_notebooks_a_migrar/` foi criada na Sprint 2 para que a renomeação não apagasse
o insumo das Sprints 6 e 7. Esta sprint desmembrou os dois últimos:

| Notebook original | Virou |
|---|---|
| `01_vazamento_temporal` (segunda metade) | `ml/split_temporal/exemplo_split_temporal.py` |
| `04_armadilhas_de_credito` | `ml/vintage_analysis/` e `ml/woe_iv_calculator/` |

A pasta foi removida da fonte e do workspace. Três documentos vivos ainda a
descreviam e foram corrigidos — o README de `hub_snippets` (que tinha uma tabela
de inventário sem nenhuma linha), o checklist de replicação e o guia temporário,
os dois últimos mandando abrir um arquivo que não existe mais.

Os relatórios das Sprints 2 e 6 e o ADR-0006 continuam citando a pasta, e assim
devem ficar: são registro datado do que era verdade quando foram escritos.

## Limpeza remota

Como em toda sprint de conversão, `import-dir --overwrite` não apaga: os 16
arquivos planos e a pasta de trânsito continuariam no workspace convivendo com as
pastas novas. Foram removidos explicitamente antes do `--verify`, que fechou com
0 obsoletos.

## O que fica para depois

| Item | Por quê |
|---|---|
| `to_markdown()` em `explainability_report` | trocar muda a saída; é etapa 2 |
| `PALETA_CATEGORICA` com 6 cores em `curves_plotly` e 10 em `constants.colors` | registrado no notebook de `curves_plotly`, conforme o template manda; unificar é decisão de produto |
| Bateria funcional de `ml` no smoke test | fora do escopo do plano (§10); hoje só `spark` e `hub_scripts` têm casos funcionais nominais |
