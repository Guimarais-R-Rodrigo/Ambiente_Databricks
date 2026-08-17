# Prompt: explicabilidade de modelo

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe modelo/run, dataset de avaliação e
> documentação com **Add context**/`@`. Skill: `@hub-ml-explainability`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Pré-requisitos

Informe população, split, target/evento e público. Se o modelo ou os dados usados na
explicação não puderem ser identificados, peça somente um plano.

## Prompt pronto para colar

```text
Use @hub-ml-explainability para explicar o modelo anexado com rigor, respeitando o
objetivo, o público e as limitações do método.

CONTEXTO
- Modelo/MLflow run/URI: {{MODELO}}
- Dataset e split: {{DATASET_E_SPLIT}}
- Target/evento positivo: {{TARGET_E_EVENTO}}
- Objetivo da explicação: {{VALIDACAO_GLOBAL_CASO_INDIVIDUAL_COMUNICACAO}}
- Público e nível técnico: {{PUBLICO}}
- Métodos desejados: {{SHAP_PDP_COEFICIENTES_OU_PROPOR}}
- Amostra/segmentos/período: {{AMOSTRA_SEGMENTOS_PERIODO}}
- Features proibidas/PII: {{RESTRICOES}}
- Modo: {{PLANO_CODIGO_OU_EXECUCAO_AUTORIZADA}}

FLUXO
1. Confirme versão do modelo, transformação, ordem/schema das features e split.
2. Diferencie performance de explicabilidade: AUC não é percentual de casos corretos.
3. Para SHAP, declare o explainer, background, espaço da saída (log-odds, score ou
   probabilidade quando suportado) e tratamento multiclasse. Valores SHAP são
   contribuições relativas ao baseline, não percentuais causais.
4. Produza visão global e local somente no nível solicitado. Não conclua causalidade,
   fairness ou conformidade a partir de importância de variável isolada.
5. Faça sanity checks: estabilidade por amostra/tempo/segmento, sinal esperado,
   correlação entre features e sensibilidade do background.
6. Não exponha registros individuais ou atributos sensíveis. Não publique artefatos
   nem altere o modelo sem autorização explícita.

CONTRATO DE SAÍDA
- Resumo executivo e definição correta de cada visual/métrica.
- Achados globais e locais separados, com evidência e incerteza.
- Limitações, riscos de interpretação e validações pendentes.
- Código reprodutível, se solicitado, com amostragem e seed declaradas.
- Recomendações que não extrapolem o método.

VALIDAÇÃO FINAL
- Confirme modelo, dataset, split, população e espaço da saída.
- Verifique que classes e sinais estão rotulados corretamente.
- Diferencie associação, contribuição do modelo e efeito causal.
```

## Exemplo mínimo

Modelo = `models:/churn/7`; dataset = `@main.ml.churn_holdout`; objetivo = explicar
drivers globais no holdout temporal; método = SHAP em amostra estratificada de 20 mil.

## Follow-ups úteis

- “Teste a estabilidade das importâncias por mês e segmento.”
- “Explique este caso sem revelar atributos identificáveis.”
- “Transforme os achados em hipóteses testáveis, não em conclusões causais.”
