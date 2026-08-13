---
name: rodrigo-cross-eda-ml
description: Consolida múltiplos EDAs e fontes para avaliar viabilidade de joins, resolução de entidade, alinhamento temporal, cobertura, complementaridade de sinal e prontidão para ML no Databricks. Usar quando pedirem cross-EDA, cruzamento de bases, integração de fontes, readiness para modelagem, análise de cobertura entre tabelas, definição de âncora ou riscos antes de feature engineering.
---

# Avaliar múltiplas fontes para ML

## Receber o contexto

Exigir ou inferir explicitamente:

- pergunta e target;
- unidade de predição;
- instante de decisão e horizonte do target;
- fonte âncora;
- chaves de entidade e temporais;
- snapshots/filtros de cada EDA;
- restrições de uso e sensibilidade.

Sem instante de decisão, não aprovar prontidão para modelagem.

## Executar o fluxo

1. **Inventariar EDAs:** registrar fonte, granularidade, período, chave, qualidade e limitações.
2. **Resolver entidade:** medir unicidade, overlap e conflitos; documentar tabela de correspondência quando necessária.
3. **Alinhar tempo:** definir join point-in-time e garantir que cada atributo existia antes da decisão.
4. **Simular joins:** medir cobertura à esquerda, não match, multiplicidade e fator de expansão.
5. **Diagnosticar ausência:** distinguir ausência estrutural, indisponibilidade temporal e falha operacional; não declarar MCAR/MAR/MNAR sem evidência suficiente.
6. **Medir complementaridade:** comparar sinal incremental com validação adequada, não apenas correlação marginal.
7. **Avaliar qualidade combinada:** verificar duplicidade, conflito semântico, unidade e domínios após o join.
8. **Decidir readiness:** registrar bloqueadores, mitigação, owner e critério de aceite.

## Proteger contra leakage

Para cada feature candidata, registrar:

- `event_time` ou período de validade;
- momento de disponibilidade real;
- regra de lookback;
- atraso de publicação;
- fonte e transformação;
- relação com a data de decisão.

Usar join point-in-time quando houver histórico. Não usar o registro “mais recente” se ele puder ter sido conhecido somente depois do target.

## Interpretar métricas corretamente

- **Coverage:** calcular no denominador da fonte âncora e por janela/segmento.
- **Overlap/Jaccard:** usar para conjuntos, sem concluir qualidade do join.
- **Cramér's V/mutual information:** tratar como associação, não causalidade.
- **PSI:** calcular com bins/categorias fixados na referência, incluindo missing; definir limiares pela política e pelo histórico.
- **Sinal incremental:** preferir comparação out-of-time com e sem a fonte e mesma população.

## Produzir scorecard sem falsa precisão

Usar dimensões explicáveis — entidade, temporalidade, cobertura, qualidade, leakage, sinal incremental e governança — e registrar a evidência de cada nota. Não converter uma média em `GO` se houver veto de leakage, chave indefinida ou população sem representatividade.

Decidir:

- **GO:** contrato completo e riscos controlados;
- **CONDICIONAL:** lacunas mitigáveis com owners e critérios;
- **NO-GO:** ausência de chave/tempo, leakage material ou cobertura incompatível.

## Usar recursos

- [templates/inventario_edas.md](templates/inventario_edas.md)
- [templates/join_feasibility.md](templates/join_feasibility.md)
- [templates/coverage_matrix.md](templates/coverage_matrix.md)
- [templates/readiness_scorecard.md](templates/readiness_scorecard.md)
- [templates/notebook_output_cross_eda.md](templates/notebook_output_cross_eda.md)
- [templates/relatorio_executivo_cross_eda.md](templates/relatorio_executivo_cross_eda.md)

Adaptar thresholds e imports à implementação atual; templates são customizados e não recursos nativos do Genie Code.

## Entregar o handoff

Fornecer mapa de fontes, contrato de join point-in-time, matriz de cobertura, riscos, decisão e backlog para `rodrigo-feature-engineering`. Incluir consultas de validação reproduzíveis e data dos snapshots.
