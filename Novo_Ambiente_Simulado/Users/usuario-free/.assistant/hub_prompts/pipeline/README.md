# `pipeline` — desenhar pipeline operável antes de fazer deploy

<!-- readme-objeto: 1.0.0 -->

Briefing para pipeline de dados com lakeflow quando apropriado. O prompt organiza o pedido, mas não executa a tarefa sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para pipeline de dados com lakeflow quando apropriado. |
| Para que serve? | Explicitar fontes, destino, modo, chaves, schema, qualidade, slo e ambientes. |
| Use quando... | Contratos e reprocessamento podem ser descritos. |
| Evite quando... | Origem ainda está incorreta ou ambiente alvo indefinido. |
| Precisa de... | Objetivo, fontes, destinos, modo, chaves, schema, regras, slo e ambientes. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](pipeline.md) e leia o [notebook de exemplo](exemplo_pipeline.py).

## 1. O que é?

Briefing para pipeline de dados com lakeflow quando apropriado. O arquivo `pipeline.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Automatizar transformação sem idempotência, schema e recuperação apenas repete erros com maior frequência.

## 3. Quando faz sentido usar?

Use quando contratos e reprocessamento podem ser descritos. Explicitar fontes, destino, modo, chaves, schema, qualidade, slo e ambientes.

## 4. Quando não usar?

Evite quando origem ainda está incorreta ou ambiente alvo indefinido. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Comece pelos contratos e chegada; desenhe estado, deduplicação, late data e qualidade antes de bundle/deploy.

## 6. Exemplo de situação

Preencha o briefing com um caso real equivalente ao cenário demonstrado no notebook, mantendo recursos, período e unidade de análise explícitos.

## 7. O que você precisa antes de usar?

Tenha objetivo, fontes, destinos, modo, chaves, schema, regras, SLO e ambientes. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Entrega um pedido estruturado. O contrato do briefing lista os artefatos esperados; confira separadamente o que foi apenas proposto, executado ou validado.

## 9. Como usar este recurso no Hub?

Abra [pipeline.md](pipeline.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_pipeline.py) demonstra o preenchimento. O exemplo sobrescreve `workspace.default.hub_exemplo_clientes`; ele não cria pipeline real.

## 10. Decisões e configurações que mais importam

Batch/streaming/CDC, chave/sequência, schema, expectations, checkpoint, ambientes e rollback.

## 11. Limitações, riscos e armadilhas

Streaming sem necessidade, deploy no catálogo errado e reprocessamento não idempotente. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Para qualidade use `data_quality`; para organizar projeto novo use `novo_projeto`.

## 13. Como saber se o resultado faz sentido?

Teste duplicata, atraso, reprocessamento, schema novo, falha parcial e parametrização por ambiente. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](pipeline.md), o [notebook](exemplo_pipeline.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

A descrição foi confrontada com [pipeline.md](pipeline.md) e [exemplo_pipeline.py](exemplo_pipeline.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
