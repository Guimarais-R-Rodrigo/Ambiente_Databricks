# `explainability` — explicar previsões sem transformar contribuição em causalidade

<!-- readme-objeto: 1.0.0 -->

Briefing para explicabilidade global/local de modelo. O prompt organiza o pedido, mas não executa a tarefa sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para explicabilidade global/local de modelo. |
| Para que serve? | Alinhar modelo, população, método e público. |
| Use quando... | Modelo e split podem ser identificados. |
| Evite quando... | Versão do modelo ou população não estão confirmadas. |
| Precisa de... | Modelo/run, dataset/split, target, objetivo, público, método e amostra. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](explainability.md) e leia o [notebook de exemplo](exemplo_explainability.py).

## 1. O que é?

Briefing para explicabilidade global/local de modelo. O arquivo `explainability.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Explicações são fáceis de superinterpretar. O formulário separa performance, contribuição do modelo, associação e efeito causal.

## 3. Quando faz sentido usar?

Use quando modelo e split podem ser identificados. Alinhar modelo, população, método e público.

## 4. Quando não usar?

Evite quando versão do modelo ou população não estão confirmadas. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Fixe modelo e população, escolha a pergunta explicativa e o método, então aplique sanity checks.

## 6. Exemplo de situação

Preencha o briefing com um caso real equivalente ao cenário demonstrado no notebook, mantendo recursos, período e unidade de análise explícitos.

## 7. O que você precisa antes de usar?

Tenha modelo/run, dataset/split, target, objetivo, público, método e amostra. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Entrega um pedido estruturado. O contrato do briefing lista os artefatos esperados; confira separadamente o que foi apenas proposto, executado ou validado.

## 9. Como usar este recurso no Hub?

Abra [explainability.md](explainability.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_explainability.py) demonstra o preenchimento. O exemplo sobrescreve `workspace.default.hub_exemplo_clientes`; SHAP é dependência opcional.

## 10. Decisões e configurações que mais importam

Versão do modelo, split, espaço da saída, explainer/background, amostra e público.

## 11. Limitações, riscos e armadilhas

Explicar versão errada, tratar SHAP como efeito causal ou expor PII. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Para performance use baseline/monitoramento; para hipótese estatística use `stat_check`.

## 13. Como saber se o resultado faz sentido?

Confirme modelo, schema, split, classes, sinal e estabilidade quando aplicável. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](explainability.md), o [notebook](exemplo_explainability.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

A descrição foi confrontada com [explainability.md](explainability.md) e [exemplo_explainability.py](exemplo_explainability.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
