# `cross_eda` — avaliar se várias fontes podem sustentar uma base de modelagem

<!-- readme-objeto: 1.0.0 -->

Este recurso é um briefing para analisar, em conjunto, fontes já conhecidas. Ele organiza entidade, granularidade, target, ponto no tempo, horizonte, chaves, períodos e restrições antes de pedir uma avaliação de compatibilidade. O prompt não executa joins nem comprova prontidão de modelagem sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um prompt preenchível de Cross-EDA. |
| Para que serve? | Examinar compatibilidade, joins, cobertura temporal e risco de leakage entre fontes. |
| Use quando... | Já houver EDAs ou conhecimento suficiente das fontes e um target definido. |
| Evite quando... | Uma fonte ainda for desconhecida ou o ponto no tempo não estiver definido. |
| Precisa de... | Recursos, entidade/grão, target, cutoff, horizonte, chaves e períodos. |
| Entrega... | Uma solicitação estruturada de mapa de fontes, riscos, evidências e condicionantes. |

Comece pelo [briefing original](cross_eda.md). O [notebook de exemplo](exemplo_cross_eda.py) cria dados sintéticos e sobrescreve duas tabelas em `workspace.default`; confira a seção 9 antes de executar.

## 1. O que é?

Cross-EDA é a exploração entre fontes, não apenas dentro de cada fonte. O objetivo é verificar se tabelas, EDAs e definições podem ser combinados sem quebrar grão, população, tempo ou significado. Nesta pasta, `cross_eda.md` é o formulário textual que organiza essa análise.

## 2. Que problema este recurso resolve?

Fontes individualmente adequadas podem formar uma base incorreta quando ligadas. Um join pode multiplicar linhas, períodos podem não se sobrepor e uma variável pode só estar disponível depois da decisão. O briefing ajuda a tornar esses riscos explícitos antes de feature engineering ou treino.

## 3. Quando faz sentido usar?

Use depois de EDAs individuais, quando já existir entidade âncora, target e fontes candidatas. É especialmente útil para avaliar cardinalidade de joins, cobertura entre tabelas, fonte de verdade e disponibilidade temporal dos atributos.

## 4. Quando não usar?

Não use como substituto da EDA de uma fonte desconhecida. Um contraexemplo é juntar dados por `id_cliente` usando o registro mais recente sem declarar o ponto de predição: o código pode rodar e ainda usar informação futura, produzindo leakage.

## 5. Como funciona, intuitivamente?

Você informa quais recursos existem, o que uma linha representa e quando a decisão acontece. O prompt pede inventário das fontes, comparação de grão e períodos, proposta de joins, verificação de cardinalidade e análise ponto-no-tempo. A recomendação final deve separar observação, hipótese e lacuna.

## 6. Exemplo de situação

Uma equipe quer combinar cadastro mensal e eventos transacionais para prever churn. O cadastro tem uma linha por cliente-mês, enquanto eventos têm várias linhas por cliente e atraso de publicação. O Cross-EDA deve verificar como agregar e ligar essas fontes sem usar eventos que ainda não existiam no cutoff.

## 7. O que você precisa antes de usar?

Preencha os campos do [briefing](cross_eda.md): recursos, entidade/granularidade, target, ponto no tempo, horizonte, chaves, períodos, fonte autoritativa quando conhecida, foco e restrições. Se o ponto no tempo estiver ausente, limite a entrega a um plano e não conclua que não há leakage.

## 8. O que este recurso entrega?

Solicita mapa de fontes e joins, cardinalidade esperada versus observada por join, matriz de compatibilidade, scorecard de readiness com critérios e itens não observáveis, riscos e recomendação condicionada à evidência. Vetos não são neutralizados por uma média. Sem ponto no tempo, entregue plano; não conclua “sem leakage”.

## 9. Como usar este recurso no Hub?

Preencha [cross_eda.md](cross_eda.md) e siga a [skill correspondente](../../skills/hub-ml-cross-eda-ml/SKILL.md) para selecionar a superfície suportada e seus inputs. Perfis sintéticos de contexto e PIT têm escopos separados; sua existência não amplia a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) nem comprova todo Cross-EDA.

O [notebook](exemplo_cross_eda.py) sobrescreve `workspace.default.hub_exemplo_fatos` e `workspace.default.hub_exemplo_features` com `mode("overwrite")`. Feature Engineering usa os mesmos destinos. O preparo planta risco temporal; não executa a análise. Parte 3: **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

`ENTIDADE_E_GRANULARIDADE` define a unidade de contagem. `TARGET_E_DEFINICAO`, `PONTO_NO_TEMPO` e `HORIZONTE` delimitam o problema temporal. `CHAVES` e `PERIODOS` definem se as fontes podem ser ligadas de forma defensável. Campos desconhecidos devem permanecer explicitamente não informados.

## 11. Limitações, riscos e armadilhas

Cobertura alta de join não prova ausência de viés nem ganho preditivo. Timestamp antigo também não garante disponibilidade antiga quando existe atraso de publicação. Exija contagens antes/depois dos joins e não trate um helper sugerido como se tivesse sido executado sem evidência.

## 12. Quais são as alternativas?

Para uma fonte, use [eda_rapida](../eda_rapida/README.md) ou [eda_completa](../eda_completa/README.md). Para duas versões da mesma informação, use [comparar_tabelas](../comparar_tabelas/README.md). Quando a compatibilidade já estiver resolvida e a tarefa for especificar atributos, use [feature_engineering](../feature_engineering/README.md).

## 13. Como saber se o resultado faz sentido?

Confira cardinalidade esperada e observada, contagens antes/depois, taxa de matches e cobertura por período. Para temporalidade, escolha casos concretos e confirme que a feature usada estava disponível antes do cutoff considerando o atraso real da fonte.

## 14. Arquivos relacionados e próximos passos

O [briefing](cross_eda.md) é o ponto de uso; o [notebook](exemplo_cross_eda.py) ilustra o risco temporal; o [catálogo de Hub Prompts](../README.md) organiza as alternativas. Depois de um Cross-EDA satisfatório, transforme as condições aprovadas em uma especificação de features e testes.

## 15. Referências

O [briefing](cross_eda.md) define os campos e a entrega; o [notebook](exemplo_cross_eda.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
