# `feature_engineering` — especificar features com fronteiras temporais explícitas

<!-- readme-objeto: 1.0.0 -->

Este recurso é um briefing para desenhar features de forma reprodutível, com atenção a entidade, janelas, cutoff, horizonte e disponibilidade temporal. Ele ajuda a separar plano, código e implementação autorizada. O prompt não cria nem publica features sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um prompt preenchível para especificação de feature engineering. |
| Para que serve? | Definir atributos, fontes, janelas, cutoff, testes e riscos de leakage. |
| Use quando... | Target, entidade e ponto no tempo já estiverem definidos. |
| Evite quando... | A pergunta ainda estiver em EDA ou faltar instante de predição. |
| Precisa de... | Entidade, chave, target, janela de observação, cutoff, horizonte, fontes e frequência. |
| Entrega... | Uma solicitação estruturada de especificação, código opcional e testes. |

Comece pelo [briefing original](feature_engineering.md). O [notebook de exemplo](exemplo_feature_engineering.py) cria duas tabelas sintéticas com escrita persistente; confira a seção 9 antes de executar.

## 1. O que é?

`feature_engineering` é um prompt personalizado que organiza o desenho de atributos para modelos. O foco é tornar cada feature rastreável por fonte, janela, cutoff, fórmula, tratamento de nulos e testes, mantendo a fronteira entre informação disponível e informação futura.

## 2. Que problema este recurso resolve?

Uma feature pode parecer válida e ainda conter leakage porque usa dados publicados depois do instante de predição. O briefing exige janela de observação, ponto no tempo e horizonte para reduzir esse risco e para evitar atributos com significado variável entre execuções.

## 3. Quando faz sentido usar?

Use depois de EDA e Cross-EDA, quando entidade, target, fontes e temporalidade já estiverem suficientemente definidos. É adequado para desenhar famílias de features, revisar atributos existentes ou preparar código para treino e inferência.

## 4. Quando não usar?

Não use para “inventar features” quando o cutoff ainda é desconhecido. Um contraexemplo é calcular “média de transações” sem janela e sem atraso de publicação: o número muda de significado e pode incluir informação que não existia na decisão.

## 5. Como funciona, intuitivamente?

Você declara o que será previsto, quando a previsão acontece e qual passado pode ser observado. O prompt pede uma especificação por feature, valida joins e cardinalidade, diferencia plano de execução e exige testes de cutoff, cobertura, estabilidade e parity treino/inferência.

## 6. Exemplo de situação

Uma equipe quer prever resposta em 30 dias. O scoring acontece diariamente, mas uma fonte de transações é atualizada semanalmente. O briefing define janela de 90 dias e atraso real da fonte; a especificação precisa impedir que uma feature use registros que só chegaram depois da decisão.

## 7. O que você precisa antes de usar?

Preencha [feature_engineering.md](feature_engineering.md) com entidade/granularidade, chave, target, janela de observação, ponto no tempo, horizonte, fontes/joins, frequência, features existentes, restrições e modo desejado. Sem janela e cutoff, peça apenas um plano.

## 8. O que este recurso entrega?

São três entregas distintas: **especificação** (fontes, event_time, available_at, cutoff, fronteira e testes); **código proposto**, quando solicitado; e **materialização**, somente sob rota e autorização específicas. A especificação prioriza risco/custo, registra hipóteses, rejeições e testes de unicidade, cobertura, janela e parity. Nenhuma dessas etapas é inferida da anterior.

## 9. Como usar este recurso no Hub?

Preencha [feature_engineering.md](feature_engineering.md). Siga a [skill correspondente](../../skills/hub-ml-feature-engineering/SKILL.md) e consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json): `current_level` descreve a capacidade vigente; `target_level` não autoriza promoção. A materialização sintética `FREE_SYNTHETIC_PIT_FEATURE_MATERIALIZATION_V1` exige composição PIT verificada, destino e autorização de efeito explícitos; não é autorização genérica para qualquer feature table. O perfil implementado tem escopo e evidência próprios; não equivale a homologação de todo pedido deste briefing.

O [exemplo](exemplo_feature_engineering.py) sobrescreve `workspace.default.hub_exemplo_fatos` e `workspace.default.hub_exemplo_features`, os mesmos nomes de Cross-EDA. As duas fixtures não certificam produção nem execução da feature. Parte 3: **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

`JANELA_OBSERVACAO`, `PONTO_NO_TEMPO` e `HORIZONTE` definem a fronteira temporal. `FONTES_E_JOINS` precisa incluir chaves, timestamps e atraso de disponibilidade. `FREQUENCIA` influencia janelas e materialização. O modo separa plano, código e implementação.

## 11. Limitações, riscos e armadilhas

Data de referência no passado não garante que o dado estava disponível naquele momento. Joins podem multiplicar linhas. Features aparentemente neutras podem atuar como proxies indesejados. Ganho hipotético não deve ser descrito como ganho medido sem experimento ou validação apropriada.

## 12. Quais são as alternativas?

Se a compatibilidade entre fontes ainda não foi demonstrada, use [cross_eda](../cross_eda/README.md). Para explorar uma única fonte, use [eda_completa](../eda_completa/README.md). Para validação estatística de hipóteses, use [stat_check](../stat_check/README.md).

## 13. Como saber se o resultado faz sentido?

Teste um evento exatamente no cutoff conforme a fronteira `<` ou `<=` declarada. Se `available_at` for posterior à decisão, ele deve ser excluído mesmo com event_time no passado. Após **cada** join, confira chave, contagem e cardinalidade esperada/observada. Registre que testes foram executados e quais ficaram pendentes; não declare disponibilidade temporal sem evidência.

## 14. Arquivos relacionados e próximos passos

O [briefing](feature_engineering.md) é o ponto de uso; o [notebook](exemplo_feature_engineering.py) demonstra leakage sintético; o [catálogo](../README.md) organiza prompts relacionados. Uma especificação aprovada pode depois virar código ou feature table em uma etapa separada.

## 15. Referências

O [briefing](feature_engineering.md) define os campos e a entrega; o [notebook](exemplo_feature_engineering.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.

Referências de plataforma: [Databricks Feature Store](https://docs.databricks.com/aws/en/machine-learning/feature-store) e [Point-in-time feature joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series). Consulte-as para os recursos nativos pertinentes; a disponibilidade e a execução do caso ainda precisam de evidência.
