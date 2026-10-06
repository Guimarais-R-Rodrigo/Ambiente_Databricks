# Prompt: explicabilidade de modelo

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe modelo/run, dataset de avaliação e
> documentação com **Add context**/`@`. Skill: `@hub-ml-explainability`.

Antes de executar, siga a [skill selecionada](../../skills/hub-ml-explainability/SKILL.md),
a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) e o contrato
da rota suportada. Helpers são componentes dessa rota, não um bypass. O
[Manual Técnico](../../MANUAL_TECNICO.md#catalogo-helpers) é o catálogo integrado.

## Pré-requisitos

Informe população, split, target/evento e público. Se o modelo ou os dados usados na
explicação não puderem ser identificados, peça somente um plano.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{MODELO}}` | Anexe modelo, URI ou run exato. | Evita explicar versão diferente. | `models:/main.ml.propensao/7` |
| `{{DATASET_E_SPLIT}}` | Anexe dados e nomeie o split/período. | Define população explicada. | teste out-of-time 2026-Q1 |
| `{{TARGET_E_EVENTO}}` | Defina target e classe positiva. | Alinha sinal da explicação. | 1=contratou |
| `{{VALIDACAO_GLOBAL_CASO_INDIVIDUAL_COMUNICACAO}}` | Escolha a pergunta explicativa. | Muda método e entrega. | validação global |
| `{{PUBLICO}}` | Informe público e nível técnico. | Calibra linguagem e detalhe. | Risco de Modelo; técnico |
| `{{SHAP_PDP_COEFICIENTES_OU_PROPOR}}` | Escolha métodos ou peça proposta. | Evita técnica incompatível com modelo. | SHAP global e local |
| `{{AMOSTRA_SEGMENTOS_PERIODO}}` | Defina N, segmentos e janela. | Torna custo e cobertura explícitos. | 10 mil; canal; 2026-Q1 |
| `{{RESTRICOES}}` | Liste PII, features proibidas e divulgação. | Evita explicação identificável ou indevida. | sem valores individuais de renda |
| `{{PLANO_CODIGO_OU_EXECUCAO_AUTORIZADA}}` | Escolha plano, código ou execução. | Separa artefato proposto de evidência. | código sem executar |

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

## O que conferir na resposta

- O recurso, o período e o grão usados coincidem com o que foi anexado e preenchido.
- Evidência observada está separada de hipótese, default e recomendação.
- Código, execução e escrita estão rotulados sem apresentar proposta como ação realizada.
- Limitações, validações não executadas e decisões pendentes aparecem explicitamente.

## Limites

- Este formulário não concede acesso, permissão de escrita, execução ou deploy.
- Campo ausente deve permanecer `NÃO INFORMADO`; não invente schema ou regra de negócio.
- Resultado material precisa de validação proporcional ao risco e, quando aplicável,
  revisão humana de negócio, Risco, Compliance ou operação.

## Follow-ups úteis

- “Teste a estabilidade das importâncias por mês e segmento.”
- “Explique este caso sem revelar atributos identificáveis.”
- “Transforme os achados em hipóteses testáveis, não em conclusões causais.”
