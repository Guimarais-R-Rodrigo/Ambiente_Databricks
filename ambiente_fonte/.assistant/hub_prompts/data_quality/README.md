# `data_quality` — organizar um diagnóstico verificável de qualidade

<!-- readme-objeto: 1.0.0 -->

Este recurso é um briefing para declarar o que precisa ser verificado em uma fonte de dados. Ele organiza grão, chaves, tempo, uso downstream, regras existentes e limites antes de pedir análise. O arquivo não altera dados nem aplica regras sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um prompt preenchível para diagnóstico e desenho de checks de qualidade. |
| Para que serve? | Pedir evidências de completude, unicidade, validade, consistência, integridade, atualidade e volume. |
| Use quando... | A confiabilidade da fonte precisa ser medida ou formalizada. |
| Evite quando... | A intenção for apenas explorar a base ou corrigir dados automaticamente. |
| Precisa de... | Recurso, grão, chaves, tempo, consumidores, regras, período e limites. |
| Entrega... | Uma solicitação estruturada de scorecard, regras propostas e evidências. |

Comece pelo [briefing original](data_quality.md). O [notebook](exemplo_data_quality.py) prepara uma tabela sintética com duplicidade proposital e faz escrita persistente; leia a seção 9 antes de executar.

## 1. O que é?

`data_quality` é um prompt personalizado do Hub. Ele transforma “esta base é confiável?” em dimensões e verificações explícitas. O Markdown é somente o briefing; qualquer leitura ou cálculo depende da interação e do ambiente.

## 2. Que problema este recurso resolve?

Qualidade depende do uso. A mesma duplicidade pode ser esperada em eventos e inadequada em uma base que deveria ter uma linha por cliente. O briefing força a declarar grão, chaves e uso downstream para que a interpretação tenha contexto.

## 3. Quando faz sentido usar?

Use ao receber uma fonte relevante, antes de modelagem ou pipeline, ao formalizar controles recorrentes ou ao transformar achados de EDA em regras verificáveis.

## 4. Quando não usar?

Não use para aprovar automaticamente uma fonte nem para escolher limites universais. Por exemplo, uma taxa de nulos aceitável em um campo opcional pode ser bloqueadora em uma chave obrigatória.

## 5. Como funciona, intuitivamente?

Você informa o recurso, o que uma linha representa, suas chaves, tempo, consumidores e regras conhecidas. O prompt pede checks por dimensão e exige que cada resultado informe evidência, período e interpretação.

## 6. Exemplo de situação

Uma base de treino deveria ter uma linha por cliente e data, mas tem mais linhas do que chaves distintas. O briefing pede que a duplicidade seja medida e relacionada ao uso downstream, sem corrigir registros automaticamente.

## 7. O que você precisa antes de usar?

Preencha os campos de [data_quality.md](data_quality.md), especialmente granularidade, chaves, colunas temporais, uso downstream, regras vigentes e período. Informação desconhecida deve permanecer explicitamente não informada até ser verificada.

## 8. O que este recurso entrega?

Solicita quatro grupos verificáveis: scorecard por dimensão com resultado/limite/evidência/severidade; catálogo de regras com proprietário sugerido; código proposto em bloco separado; riscos, lacunas e plano de implantação. Distinga regra vigente de proposta e código proposto de executado. Dimensão não testada permanece não observada, nunca conforme.

## 9. Como usar este recurso no Hub?

Preencha [data_quality.md](data_quality.md) e selecione o recurso real. Quando `hub-ml-eda-profissional` for selecionada para executar a EDA protegida, siga a [rota canônica](../../skills/hub-ml-eda-profissional/SKILL.md): `run_enforced` coleta evidência e emite Receipt; depois o handoff deve ser finalizado por `finalize_or_raise`. Exija Postflight `PASS` e `completion.authorized=true` antes de declarar conclusão. `PENDING_POSTFLIGHT` é transitório, não sucesso. Rapidez reduz profundidade opcional; não dispensa gates nem autoriza helper/SQL manual como bypass. Campos essenciais ausentes permanecem pendentes, sem inventar chave ou dados. Consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json).

O [exemplo](exemplo_data_quality.py) sobrescreve `workspace.default.hub_exemplo_clientes_dup` com `mode("overwrite")`. A duplicidade é sintética e deve ser conferida na chave declarada. Parte 3: **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

Grão e chaves definem unicidade. Colunas de tempo e período definem atualidade. O uso downstream muda a severidade. Regras existentes precisam ser separadas de limites apenas propostos pelo assistente.

## 11. Limitações, riscos e armadilhas

Uma taxa pode usar o denominador errado, uma amostra pode esconder falhas raras e um limite sugerido pode parecer plausível sem ter base suficiente. Confira a procedência das regras antes de implantá-las.

## 12. Quais são as alternativas?

Para exploração, use [EDA rápida](../eda_rapida/README.md) ou [EDA completa](../eda_completa/README.md). Para versões de uma fonte, use [Comparar Tabelas](../comparar_tabelas/README.md). [data_quality_check](../../hub_scripts/data_quality_check/README.md) oferece diagnóstico determinístico isolado de nulos, chave e freshness; seu escopo é menor que o catálogo de regras deste prompt e não substitui uma EDA protegida selecionada.

## 13. Como saber se o resultado faz sentido?

Recalcule taxas críticas, confira numerador, denominador, período, timezone, grão e chaves. Verifique que uma dimensão não testada não foi apresentada como conforme.

## 14. Arquivos relacionados e próximos passos

O [briefing](data_quality.md) é o ponto de uso; o [notebook](exemplo_data_quality.py) demonstra a falha sintética; o [catálogo](../README.md) organiza prompts relacionados. Regras aprovadas podem depois ser convertidas em testes ou controles de pipeline em uma etapa separada.

## 15. Referências

O [briefing](data_quality.md) define os campos e a entrega; o [notebook](exemplo_data_quality.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
