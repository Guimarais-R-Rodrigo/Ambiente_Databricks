# Template: Relatório Executivo de Explicabilidade

## Uso
Camada executiva para gestores; a camada editorial não indica ambiente de
execução ou homologação. Traduzir somente resultados efetivamente
observados da [skill](../SKILL.md); sem eles, entregar plano/NÃO EXECUTADO.

## Objeto explicado
- Modelo/versão e origem: [identificação comprovada]
- Target, classe, população e período: [definições]
- Método, conjunto/background e N: [fonte]
- Escala explicada: [saída bruta, log-odds, probabilidade ou valor previsto]
- Performance: [métrica realmente calculada, valor, benchmark e incerteza; ou NÃO AVALIADA]

## O que influencia as previsões

Os principais fatores que influenciam as previsões do modelo no recorte são:

| Fator | Descrição | Importância na escala declarada | Direção/padrão observado | Limitação |
|---|---|---|---|---|
| [nome] | [significado] | [valor, método e normalização ou NÃO CALCULADO] | [contribuição para a previsão] | [variação por segmento/correlação] |

Importância explica o comportamento do modelo. Não determina o target real,
não mede percentual de decisões e não comprova causa, proteção ou benefício
por intervir no fator. Só usar porcentagem com denominador matemático declarado.

## Exemplos locais, se produzidos

| Caso agregado/mascarado | Predição e unidade | Contribuições observadas | Evidência |
|---|---|---|---|
| [caso representativo] | [valor; probabilidade só quando essa for a escala] | [fatores e valores] | [artefato ou NÃO EXECUTADO] |

Não converter contribuição SHAP bruta em probabilidade aditiva. Não divulgar
atributos pessoais em exemplos locais.

## Confiança e limites
- AUC-ROC mede ordenação de pares, não percentual de casos corretos. Informar
  acurácia apenas se calculada separadamente, com threshold/população.
- Escopo de validade: [período, segmentos, cobertura e incerteza observados]
- O que o método não captura: [limitações, proxies, dependências entre features]
- Verificação: [fonte/estado e escopo; não inferir aprovação por Receipt isolado]

## Recomendações
1. Investigação: [padrão a verificar e evidência necessária]
2. Hipótese de intervenção: [se pertinente, desenho causal/experimento necessário antes de afirmar efeito]
3. Controle/monitoramento: [owner e critério definidos]

Recomendação técnica não autoriza intervenção, retreino, publicação ou promoção.
