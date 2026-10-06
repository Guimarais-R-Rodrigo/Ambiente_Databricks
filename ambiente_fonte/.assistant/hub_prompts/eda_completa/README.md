# `eda_completa` — estruturar uma EDA profunda sem confundir exploração com aprovação

<!-- readme-objeto: 1.0.0 -->

Este recurso é um briefing para pedir uma análise exploratória completa, reprodutível e orientada a uma decisão. Ele organiza contexto de negócio, grão, chave, tempo, target, período, volume, foco, restrições e formato de entrega. O prompt não executa a EDA sozinho.

**Antes de executar o preparo:** ele sobrescreve `workspace.default.hub_exemplo_clientes` com `mode("overwrite")`. Esse destino também é usado por EDA, Baseline, Explainability, Novo Projeto, Pipeline e Stat Check: executar um exemplo pode substituir a base de outro. Use o briefing sem executar o preparo quando só precisar do texto.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um prompt preenchível para EDA completa. |
| Para que serve? | Pedir análise estrutural, de qualidade, distribuições, relações e riscos de modelagem. |
| Use quando... | A fonte já está definida e a análise precisa ir além de um primeiro perfil. |
| Evite quando... | A pergunta ainda é preliminar ou a fonte está mudando rapidamente. |
| Precisa de... | Recurso, contexto, grão, chave, tempo, período, foco e restrições. |
| Entrega... | Uma solicitação estruturada de diagnóstico, evidências, código e backlog. |

Comece pelo [briefing original](eda_completa.md). O [notebook de exemplo](exemplo_eda_completa.py) prepara uma tabela sintética com escrita persistente; leia a seção 9 antes de executar.

## 1. O que é?

`eda_completa` é um prompt personalizado que organiza uma EDA mais profunda do que `eda_rapida`. Ele pede estrutura, qualidade, análise univariada e multivariada, relações com target quando aplicável e riscos como leakage, desbalanceamento e representatividade.

## 2. Que problema este recurso resolve?

Pedidos como “faça uma EDA” deixam em aberto população, período, unidade de análise e finalidade. O briefing explicita essas decisões para tornar a investigação reproduzível e relacionada ao uso pretendido.

## 3. Quando faz sentido usar?

Use quando a fonte e o objetivo já são conhecidos e você precisa de uma análise que sustente decisões de modelagem, segmentação ou investigação. É apropriado depois de um perfil inicial ou quando o target e o entregável precisam orientar a profundidade.

## 4. Quando não usar?

Não use apenas para conhecer rapidamente uma tabela nova; nesse caso, `eda_rapida` é mais proporcional. Um contraexemplo é pedir uma EDA completa sobre um schema ainda instável: o resultado pode envelhecer antes de ser usado.

## 5. Como funciona, intuitivamente?

Você declara o universo da análise e o formato esperado. O prompt orienta verificação de schema, volume, chaves e granularidade; depois qualidade, distribuições, relações relevantes e riscos. Conclusões devem apontar para evidências e listar o que não foi verificado.

## 6. Exemplo de situação

Uma equipe quer avaliar uma base de clientes para um modelo de propensão. O briefing define uma linha por cliente-mês, target de resposta em 30 dias, período, foco em qualidade e relação com o alvo, além do formato notebook. A resposta deve investigar esses pontos sem tratar correlação como causalidade.

## 7. O que você precisa antes de usar?

Preencha [eda_completa.md](eda_completa.md) com recurso, contexto, granularidade, chave, coluna temporal, target quando houver, período/filtros, volume, foco, restrições e entregável. Campos desconhecidos devem ficar como não informados, não ser inventados.

## 8. O que este recurso entrega?

Confira a entrega solicitada: inventário de qualidade com evidência e severidade; código parametrizado e organização reproduzível; cada gráfico com base, unidade e período; achados referenciados; limitações e pendências. A execução deve sustentar cada número. Notebook extenso ou visualmente cuidado não autoriza conclusão sem finalização canônica.

## 9. Como usar este recurso no Hub?

Preencha [eda_completa.md](eda_completa.md), selecione a fonte e leia o [exemplo](exemplo_eda_completa.py). Quando `hub-ml-eda-profissional` for selecionada para executar a EDA protegida, siga a [rota canônica](../../skills/hub-ml-eda-profissional/SKILL.md): `run_enforced` coleta evidência e emite Receipt; depois o handoff deve ser finalizado por `finalize_or_raise`. Exija Postflight `PASS` e `completion.authorized=true` antes de declarar conclusão. `PENDING_POSTFLIGHT` é transitório, não sucesso. Rapidez reduz profundidade opcional; não dispensa gates nem autoriza helper/SQL manual como bypass. Campos essenciais ausentes permanecem pendentes, sem inventar chave ou dados. Consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json). O preparo sintético sobrescreve `workspace.default.hub_exemplo_clientes`; a Parte 3 permanece **NÃO EXECUTADO**, mesmo que existam runners no produto.

## 10. Decisões e configurações que mais importam

Granularidade e chave definem contagens e duplicidade. Período e filtros definem a população. Target muda quais relações são relevantes. Volume influencia estratégia de execução. `FOCO` e `NOTEBOOK_RELATORIO_OU_CODIGO` evitam uma entrega extensa, mas pouco útil.

## 11. Limitações, riscos e armadilhas

EDA não demonstra causalidade, não garante ausência de leakage e não substitui validação de negócio. Amostras e agregações podem esconder padrões raros. Uma resposta organizada também pode estar errada se o recurso, período ou grão usado não coincidir com o briefing.

## 12. Quais são as alternativas?

Para primeiro diagnóstico, use [eda_rapida](../eda_rapida/README.md). Para qualidade formal, use [data_quality](../data_quality/README.md). Para combinar várias fontes antes de modelar, use [cross_eda](../cross_eda/README.md).

## 13. Como saber se o resultado faz sentido?

Confira recurso, período, filtros, contagens e granularidade. Verifique pelo menos alguns cálculos materiais e se gráficos informam base, unidade e período. Separe achados observados de hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](eda_completa.md) contém o formulário; o [notebook](exemplo_eda_completa.py) mostra um cenário sintético; o [catálogo](../README.md) reúne os prompts. Achados importantes podem seguir para regras de qualidade, Cross-EDA ou feature engineering.

## 15. Referências

O [briefing](eda_completa.md) define os campos e a entrega; o [notebook](exemplo_eda_completa.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.

Para anexos e seleção de recursos, consulte [Navigate Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code). O contrato de execução protegido continua sendo o da skill vinculada acima.
