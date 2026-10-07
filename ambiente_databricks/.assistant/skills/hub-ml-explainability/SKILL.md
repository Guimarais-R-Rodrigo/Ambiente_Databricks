---
name: hub-ml-explainability
description: Explica modelos no Databricks para públicos técnico e executivo com SHAP, importância por permutação, coeficientes, PDP/ALE e exemplos locais, registrando metodologia e limitações no MLflow. Usar quando pedirem interpretabilidade, explicabilidade, SHAP, feature importance, motivos de score, drivers, análise global/local, comparação por cohort, model card ou investigação de leakage/bias do modelo.
---

# Explicar modelos com rigor

## Perfil sintético de regressão linear

O perfil `LINEAR_REGRESSION_SYNTHETIC_V1` aceita somente regressão linear escalar `sklearn.LinearRegression` com dados sintéticos, features numéricas finitas em ordem explícita, IDs únicos, amostra explícita e uma linha de referência. Prepare [input.schema.json](input.schema.json) e use `scripts/preflight.py::preflight(request)`. Com PASS, chame `scripts/run.py::run(request, model=model, X=X, background=background, run_id=...)`; modelo e arrays devem vir da mesma fonte independente do pedido e manter os parâmetros e valores declarados. Defina `model.hub_model_id` com a identidade externa que deve coincidir com `request.model.model_id`.

O runner chama `hub_snippets.ml.shap_explainer.compute_shap` com `model_type="linear"`, `task="regression"` e `background` explícito. Para afirmar valores verificados, chame `scripts/verify.py::verify(payload, expected_request=..., expected_model=..., expected_X=..., expected_background=..., expected_run_id=...)` com entradas confiáveis preservadas fora do payload. Exija `valid=true`. Um Receipt sozinho não prova a correção dos valores. Neste perfil, `valid=true` autoriza apenas afirmar que os valores passaram no escopo do verificador. O retorno mantém `completion_authorized=false` e `promotion_authorized=false` mesmo quando `valid=true`: esses campos não são condições adicionais para a afirmação limitada de valores verificados, nem autorizam homologação ou conclusão da entrega. Ao descrever a rota sem executá-la, não afirme verificação realizada.

O runner copia as matrizes aceitas para `float64`; inteiros sem conversão exata são bloqueados. Se o estimador tiver `feature_names_in_`, a ordem deve coincidir com `feature_names`.

A referência de uma linha fixa a base. O resultado conserva todas as linhas na ordem de `row_ids`; `sample_ids` marca exemplos pedidos para leitura local. SHAP é contribuição em unidades da saída bruta do modelo, não causalidade. O perfil não faz inferência, recomendação automática, persistência, publicação, homologação Genie ou promoção de policy. Se preflight, execução ou verificação bloquear, reporte a causa sem afirmar conclusão.


## Quando esta skill se aplica

- Pedem **interpretabilidade, SHAP, feature importance, motivos de score,
  drivers, model card** ou investigação de leakage/viés.
- Existe um **modelo treinado** a explicar — global, local ou por cohort.

**Não cobre:** treinar ou comparar modelos (`hub-ml-baseline-ml`) nem detectar
drift em produção (`hub-ml-monitoramento-modelo`).

## Definir o objeto

Confirmar modelo/versão, target, unidade, população, período, conjunto avaliado, preprocessing, classe explicada e escala do output (margem, log-odds, probabilidade ou valor previsto).

Executar explicações sobre validação/teste ou amostra representativa, não sobre treino sem justificativa. Preservar a mesma transformação usada na inferência.

## Escolher o método

- Usar TreeSHAP para árvores compatíveis.
- Usar explicadores lineares para modelos lineares com transformação conhecida.
- Usar permutation importance como diagnóstico agnóstico, com métrica e conjunto declarados.
- Usar PDP com cautela quando features são correlacionadas; preferir ALE quando disponível e adequado.
- Usar KernelSHAP ou métodos aproximados somente com amostra explícita, orçamento e limitação documentada.
- Não usar attention weights como explicação causal.

Confirmar a forma de retorno da versão instalada do SHAP, especialmente em classificação multiclasses. Não assumir que `shap_values` é sempre uma lista ou matriz 2D.

## Produzir camada técnica

1. Validar performance do modelo no mesmo conjunto.
2. Calcular explicação global: distribuição e média de `|SHAP|` ou método escolhido.
3. Examinar direção e não linearidade para features prioritárias.
4. Explicar casos locais representativos, fronteiriços e de erro; não selecionar apenas exemplos convenientes.
5. Comparar cohorts com volume e incerteza.
6. Investigar features suspeitas de leakage ou proxies sensíveis.
7. Testar estabilidade por período e segmento quando necessário.
8. Registrar seed, amostra, background, classe e escala.

SHAP decompõe a saída do modelo em relação a um valor base. Não significa causalidade, percentual de decisão, relevância normativa ou justificativa humana verdadeira. Se converter log-odds para probabilidade, explicar que contribuições deixam de ser aditivas na escala transformada.

## Produzir camada executiva

Traduzir somente depois da análise técnica:

- o que mais influenciou as previsões na população;
- como o efeito variou e em quais segmentos;
- exemplos concretos de score, sem expor PII;
- confiabilidade, cobertura e limitações;
- ações investigativas e controles.

Não dizer que AUC de 0,82 significa “82% dos casos corretos”. Não chamar associação de causa. Não usar cor/linguagem para sugerir aprovação regulatória.

## Registrar e governar

No MLflow, registrar gráficos, ranking tabular, configuração do explicador, amostra/background e versão do pacote. Conectar ao modelo correto em Unity Catalog sem promover ou alterar alias sem autorização.

Revisar dados sensíveis: explicações locais podem revelar atributos. Agregar, mascarar e controlar acesso.

## O que nunca fazer

- **Ler importância como causalidade.** SHAP explica o modelo, não o mundo.
- **Explicar modelo que não foi validado.** Explicabilidade sobre modelo com
  leakage produz uma narrativa convincente e errada.
- **Publicar importância global sem a distribuição.** A média esconde o cohort em
  que o modelo se comporta de outro jeito.
- **Omitir a limitação do método.** PDP assume independência entre features;
  quando elas são correlacionadas, a curva descreve um ponto que não existe.
- **Instalar `shap` sem fixar versão** — o inventário exige `shap==0.44.1`.

## Usar recursos

- Usar [templates/shap_analysis_technical.md](templates/shap_analysis_technical.md) para a camada técnica.
- Usar [templates/relatorio_executivo_explainability.md](templates/relatorio_executivo_explainability.md) para a camada executiva.

Substituir thresholds fixos dos templates por critérios do modelo, população e política aprovada.

## Usar helpers da biblioteca

Importar de `hub_snippets` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO_V2.md#catalogo-helpers](../../MANUAL_TECNICO_V2.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Cálculo SHAP, importância e plots global/local | `hub_snippets.ml.shap_explainer` |
| Relatório dual-layer (executivo e técnico) | `hub_snippets.ml.explainability_report` |
| Curvas diagnósticas de apoio | `hub_snippets.ml.curves_plotly` |

Para curvas diagnósticas Plotly auxiliares, um tema notebook validado pode ser aplicado pelas rotas como `plot_roc_curve_resolvido`. **SHAP/Matplotlib é uma exceção explícita:** o Sistema de Temas atual não controla o estilo interno dos plots SHAP nem o PNG salvo por `shap_explainer`. Não prometa recoloração/consistência temática dessas figuras apenas porque o notebook usa `ResolvedTheme` em outros gráficos.

`shap` é dependência opcional resolvida na chamada: o import do módulo passa mesmo sem a biblioteca instalada. Os textos gerados evitam tratar importância SHAP como causalidade ou como percentual de poder preditivo; preservar essa formulação ao adaptar.

## Entregar

Entregar método, conjunto, classe/escala, gráficos, tabela de drivers, exemplos locais, estabilidade, limitações e próximos testes. Separar claramente explicação do comportamento do modelo de explicação causal do fenômeno.
