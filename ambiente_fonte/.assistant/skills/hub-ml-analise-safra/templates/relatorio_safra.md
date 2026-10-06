# Template: Relatório de Análise de Safras

> **[N safras]** analisadas | **[N contratos]** total | **[Ever-bad]** taxa média | **[MOB maturação]** meses


Preencher somente com evidência da análise. Sem execução, usar NÃO EXECUTADO;
sem dado ou critério informado, usar NÃO INFORMADO. Gráficos e alertas dependem
da rota efetivamente executada; o relatório não autoriza intervenção.

## Contrato de comparação

- Unidade e roster de origem: [fonte, versão, N por safra]
- Numerador/target: [EVENT ou CUMULATIVE e definição]
- Denominador: [regra e valor por safra; no perfil de roster fixo, não substituir N pelo número observado]
- Data de corte: [data comprovada ou NÃO INFORMADO]
- Por célula safra × MOB: [maturidade, N observado, cobertura e fonte]
- Taxa em célula imatura, incompleta ou sem observações: AUSENTE, nunca zero nem taxa provisória sobre o subconjunto observado.
- Sem corte: maturidade/status formal pendentes; cobertura parcial relatada não comprova imaturidade nem maturidade.
- Comparar apenas MOBs de maturidade e cobertura compatíveis; declarar ponderação da média e incerteza.

## Resumo executivo

| Aspecto | Valor |
|---|---|
| Produto/Carteira | [nome] |
| Período analisado | [safra inicial] a [safra final] |
| N safras | [X] |
| N contratos total | [X] |
| Ever-bad rate médio | [X]% |
| Safra com melhor performance | [safra] ([X]%) |
| Safra com pior performance | [safra] ([X]%) |
| MOB de maturação | [X] meses |

## Curvas de maturação (vintage curves)

[Inserir gráfico de linhas: X=MOB, Y=taxa acumulada, cor=safra]

### Observações:
- [obs 1: comportamento geral]
- [obs 2: safras outliers]
- [obs 3: tendência temporal]

## Heatmap de safras

[Inserir heatmap: linhas=safras, colunas=MOB, cor=taxa]

## Comparação entre safras

| Safra | N | Taxa MOB-6 | Taxa MOB-12 | Ever-bad | vs. Média | Status |
|---|---|---|---|---|---|---|
| [safra] | [N] | [X]% | [X]% | [X]% | [±X]pp | [🟢/🟡/🔴] |

## Alertas

| Alerta | Safra | Detalhe | Severidade |
|---|---|---|---|
| [tipo] | [safra] | [descrição] | [🟡/🔴] |

## Interpretação e recomendações

### Padrões observados e hipóteses
- **Safra**: [padrão observado; hipótese sobre originação a testar]
- **Calendário**: [padrão observado; hipótese macroeconômica a testar]
- **Maturação**: [padrão observado em MOBs comparáveis; hipótese a testar]

Diferenças descritivas não identificam efeitos causais: mix, calendário e idade
podem se confundir. Registrar a evidência necessária antes de recomendar ação.

### Recomendações:
1. [ação 1]
2. [ação 2]
3. [ação 3]
