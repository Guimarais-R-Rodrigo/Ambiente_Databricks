# Template: Decisão de Pressupostos

## Como usar
Selecionar diagnóstico por pergunta, estimando, desenho e método. As alternativas
abaixo são candidatas de planejamento; não são sequência automática de execução.
Códigos R/T/M/D/I identificam testes de diagnóstico, não capacidade do runner.
Confirmar rota disponível na [skill](../SKILL.md). O piloto KS não executa as
outras suites por aproximação. Sem evidência, registrar NÃO AVALIADO.

Antes de agir, registrar alfa pré-especificado, efeito mínimo relevante, família
de hipóteses, critério aprovado, população/N e dependência. Teste isolado não
comprova pressuposto, leakage ou causalidade; não escolher remediação por p-valor
sem examinar consequências para o estimando.

## Regressão e econometria

| Diagnóstico | Código | Evidência a avaliar | Alternativas a justificar |
|---|---|---|---|
| Normalidade dos resíduos | R1/R2 | Resíduos, N, caudas e sensibilidade da inferência | Inferência robusta/reamostragem compatível; transformação só se preservar objetivo |
| Multicolinearidade | R3 | VIF, estrutura das features e estabilidade | Regularização, revisão da especificação; sem remover por VIF fixo |
| Autocorrelação | R4 | Dependência residual, tempo e desenho | Lags/erros robustos HAC/modelagem da dependência, conforme objetivo |
| Heterocedasticidade | R5/R6 | Padrão dos resíduos, teste e magnitude | Erros robustos ou WLS com hipótese de variância justificada |
| Forma funcional | R7 | Resíduos e teste RESET com especificação declarada | Termos adicionais/GAM/modelo alternativo com validação |
| Estabilidade numérica | R8 | Escala, condition number e sensibilidade | Padronização/reparametrização/regularização justificadas |

Não exigir normalidade dos preditores. Transformar a resposta pode alterar
estimando, interpretação e retransformation; não é correção automática.

## Séries temporais

| Diagnóstico | Código | Evidência a avaliar | Alternativas a justificar |
|---|---|---|---|
| Estacionariedade | T1/T2 | ADF/KPSS, componentes determinísticos, lags e quebras | Diferenciação/detrend apenas com especificação; verificar excesso de diferenciação |
| Ruído residual | T3 | Ljung-Box, lags e multiplicidade | Rever estrutura temporal e validar fora da amostra |
| Dependência de primeira ordem | T4 | Resíduos e desenho temporal | Modelar dependência compatível, sem corte universal de DW |
| Sazonalidade | T5 | Período, histórico e estabilidade do padrão | Termos sazonais/decomposição quando suportados |
| Normalidade residual | T6 | Caudas e impacto nos intervalos | Intervalos robustos/reamostragem que preserve dependência |
| Variância condicional | T7 | ARCH-LM, magnitude e contexto | Modelo de volatilidade ou intervalo adequado à finalidade |

ADF/KPSS não aprovam forecast. Comparar baseline, horizonte e desempenho OOT.

## ML tabular

| Diagnóstico | Código | Evidência a avaliar | Alternativas a justificar |
|---|---|---|---|
| Leakage | M7 | Proveniência, disponibilidade até decisão, split e fit no treino | Corrigir fonte/split/transformação quando violação comprovada; correlação alta isolada não prova leakage |
| Drift | M4/M5 | Referência/bins, volume, segmentos e critério aprovado | Investigar dados/população; challenger só com escopo e autoridade próprios |
| Sinal incremental | M1/M2/M6 | Comparação justa fora da amostra e incerteza | Revisar features ou objetivo; ausência de significância univariada não prova ausência de sinal |
| Imbalance | C6 | Eventos, métrica, capacidade e custo do erro | Pesos/threshold/reamostragem só no treino, quando justificados |
| Suficiência amostral | M9 | Alternativa, desenho, alfa e cálculo de potência ou precisão | Coleta adicional ou escopo limitado; sem corte universal de power |

## Deep learning

| Diagnóstico | Código | Evidência a avaliar | Alternativas a justificar |
|---|---|---|---|
| Overlap de entidade | D3 | Política de independência e duplicação cross-split | Reparticionar quando o contrato exigir entidades disjuntas |
| Qualidade de labels | D2 | Método de avaliação e erros verificados | Revisão de anotação/robustez; não limpar por taxa arbitrária |
| Escala | D5 | Sensibilidade do algoritmo e pipeline | Scaling ajustado só no treino, se necessário |
| Distribuição entre splits | D8 | Shift, tempo e mecanismo amostral | Investigar e preservar desenho de uso; não estratificar apagando OOT |

## Inferência entre grupos

| Diagnóstico | Código | Evidência a avaliar | Alternativas a justificar |
|---|---|---|---|
| Distribuição relevante ao estimando | I1 | Forma, N e robustez do método | Transformação, bootstrap ou teste alternativo; testes não paramétricos podem mudar a hipótese |
| Variâncias | I2 | Desenho, tamanhos e heterogeneidade | Welch ou modelo apropriado, sem preteste automático como único seletor |
| Dependência/pareamento | — | Unidade e desenho de coleta | Teste pareado/modelo hierárquico apropriado |
| Contagens categóricas | I7 | Contagens esperadas, dimensão e independência | Método exato/simulação compatível; agregação de categorias só com sentido substantivo |
| Multiplicidade | I9 | Família definida antes de olhar resultados e controle de erro pretendido | Holm/Bonferroni/FDR conforme objetivo e pressupostos; não esperar “mais de 3 testes” |

## Decisão documentada
- Achado e evidência: [fonte ou NÃO AVALIADO]
- Consequência para estimando/decisão: [magnitude, incerteza e limite]
- Mitigação proposta e critério de reavaliação: [justificativa]
- Autoridade e escopo: [aprovação necessária antes de alterar dados/método/execução]
- Estado: [pendente/condicional/bloqueado ou decisão fundamentada]

Risco crítico interrompe a etapa dependente. Mitigação proposta não é mitigação
executada, e um reteste não apaga seleção pós-hoc, falha anterior ou risco residual.
