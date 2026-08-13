---
name: rodrigo-explainability
description: Explica modelos no Databricks para públicos técnico e executivo com SHAP, importância por permutação, coeficientes, PDP/ALE e exemplos locais, registrando metodologia e limitações no MLflow. Usar quando pedirem interpretabilidade, explicabilidade, SHAP, feature importance, motivos de score, drivers, análise global/local, comparação por cohort, model card ou investigação de leakage/bias do modelo.
---

# Explicar modelos com rigor

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

## Usar recursos

- Usar [templates/shap_analysis_technical.md](templates/shap_analysis_technical.md) para a camada técnica.
- Usar [templates/relatorio_executivo_explainability.md](templates/relatorio_executivo_explainability.md) para a camada executiva.

Substituir thresholds fixos dos templates por critérios do modelo, população e política aprovada.

## Entregar

Entregar método, conjunto, classe/escala, gráficos, tabela de drivers, exemplos locais, estabilidade, limitações e próximos testes. Separar claramente explicação do comportamento do modelo de explicação causal do fenômeno.
