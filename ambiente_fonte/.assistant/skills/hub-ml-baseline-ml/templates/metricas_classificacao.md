# Template: Métricas de classificação

> Preencher com resultados observados e critérios aprovados. Não existem faixas universais de “bom” AUC, KS, Gini ou F1.

## Contexto

| Campo | Valor |
|---|---|
| População/período | [valor] |
| N / eventos / prevalência | [valores] |
| Custo de falso positivo/negativo | [descrição] |
| Baseline trivial/histórico | [valor] |
| Métrica primária | [métrica + justificativa] |
| Threshold | [valor + regra de escolha] |
| Critério de aceite | [benchmark/política] |

## Discriminação e ranking

| Métrica | Treino | Validação | Teste OOT | IC/variabilidade | Benchmark | Status |
|---|---:|---:|---:|---|---:|---|
| AUC-ROC | [X] | [X] | [X] | [lo–hi] | [X] | [status] |
| AUC-PR | [X] | [X] | [X] | [lo–hi] | [prevalência/baseline] | [status] |
| KS | [X] | [X] | [X] | [lo–hi] | [X] | [status] |
| Lift@k | [X] | [X] | [X] | [lo–hi] | [X] | [status] |

AUC-ROC estima a probabilidade de um positivo sorteado receber score maior que um negativo sorteado. Não é percentual de casos corretos. Em evento raro, ler AUC-PR e precision/recall junto com prevalência.

## Probabilidade e calibração

| Métrica/diagnóstico | Resultado | Benchmark | Status |
|---|---:|---:|---|
| Log loss | [X] | [X] | [status] |
| Brier score | [X] | [X] | [status] |
| Calibration intercept/slope | [X]/[X] | [X]/[X] | [status] |
| Curva de calibração por faixa | [artefato] | [critério] | [status] |

## Operação no threshold escolhido

| Métrica | Valor | Limite operacional | Status |
|---|---:|---:|---|
| Precision | [X] | [X] | [status] |
| Recall | [X] | [X] | [status] |
| F1/F-beta | [X] | [X] | [status] |
| Especificidade | [X] | [X] | [status] |
| Volume sinalizado | [N/%] | [capacidade] | [status] |
| Custo/benefício esperado | [valor] | [critério] | [status] |

## Robustez

Reportar os mesmos indicadores por período e segmentos materiais, incluindo volume. Investigar gap treino–teste, uma única classe, mudança de prevalência, leakage, calibração e sensibilidade ao threshold.

## Texto executivo

> No período [X], o modelo [superou/não superou] o baseline em [métrica], com [incerteza]. No threshold [regra], identifica [recall] dos eventos com [precision], sinalizando [volume]. A decisão é [ação], condicionada a [limitação/guardrail].
