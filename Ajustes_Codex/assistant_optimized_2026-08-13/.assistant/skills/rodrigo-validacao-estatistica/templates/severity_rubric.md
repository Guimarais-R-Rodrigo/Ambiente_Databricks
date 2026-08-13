# Template: Rubrica de severidade estatística

> Recurso customizado. Calibrar ao estimando, desenho, efeito mínimo relevante, risco e política aprovada. Um p-valor ou PSI isolado não define severidade.

## Níveis

| Nível | Definição | Resposta |
|---|---|---|
| ✅ OK | Evidência e incerteza compatíveis com o uso declarado | Prosseguir e monitorar |
| ℹ️ Informativo | Resultado descritivo sem impacto decisório imediato | Interpretar e registrar |
| 🟡 Atenção | Pode alterar magnitude, estabilidade ou generalização | Mitigar e repetir a validação |
| 🔴 Crítico | Invalida o estimando, introduz leakage/erro material ou torna a decisão insegura | Interromper a etapa dependente e corrigir |

## Calibração de cada achado

Responder:

1. Qual pressuposto, estimando ou contrato foi afetado?
2. Qual a magnitude e o intervalo de incerteza?
3. Quantas unidades/períodos/segmentos foram afetados?
4. O resultado persiste em análise de sensibilidade?
5. Qual decisão mudaria e qual é o custo do erro?
6. Existe mitigação verificável e critério de aceite?

## Orientação por família

| Família | Atenção quando | Crítico quando |
|---|---|---|
| Chave/granularidade | duplicidade explicável e tratável | unidade de análise ou join incorreto |
| Missing | padrão muda população/estimativa | informação futura, viés material ou perda sem rastreio |
| Redundância/VIF | aumenta instabilidade | inviabiliza inferência/identificação no uso declarado |
| Normalidade/resíduos | afeta IC/teste em amostra limitada | conclusão depende de pressuposto não mitigado |
| Heterocedasticidade/dependência | erros padrão ou forecast mudam | inferência/validação permanece inválida após mitigação |
| Estacionariedade | especificação temporal instável | validação fora da amostra não representa o uso |
| Drift/PSI/KS | excede variabilidade histórica aprovada | população/contrato mudou e desempenho não é confiável |
| Imbalance | métricas/threshold instáveis | não há eventos/volume para a decisão pretendida |
| Leakage | suspeita exige teste | informação pós-decisão ou overlap contamina a avaliação |
| Múltiplos testes | família mal definida | conclusão se apoia em seleção pós-hoc sem correção |

## Card de achado

| Campo | Conteúdo |
|---|---|
| Achado | [descrição] |
| Evidência | [estimativa, IC, teste, N] |
| Severidade | [nível + justificativa] |
| Impacto | [decisão/métrica/população] |
| Mitigação | [ação] |
| Aceite | [teste/limite aprovado] |
| Risco residual | [descrição] |
