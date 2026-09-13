# `safra` — comparar safras na mesma maturidade

<!-- readme-objeto: 1.0.0 -->

Briefing para safra/vintage com coorte, idade, numerador, denominador e censura. O prompt organiza o pedido, mas não executa a tarefa sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para safra/vintage com coorte, idade, numerador, denominador e censura. |
| Para que serve? | Evitar comparar coortes com maturidade diferente. |
| Use quando... | Coorte, maturidade e evento estão claros. |
| Evite quando... | Célula imatura é tratada como zero ou regra normativa não tem fonte. |
| Precisa de... | Dataset, entidade/chave, safra, idade, evento, denominador, métrica e censura. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](safra.md) e leia o [notebook de exemplo](exemplo_safra.py).

## 1. O que é?

Briefing para safra/vintage com coorte, idade, numerador, denominador e censura. O arquivo `safra.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Safras recentes parecem melhores quando tiveram menos tempo para maturar. Sem denominador e censura a curva pode enganar.

## 3. Quando faz sentido usar?

Use quando coorte, maturidade e evento estão claros. Evitar comparar coortes com maturidade diferente.

## 4. Quando não usar?

Evite quando célula imatura é tratada como zero ou regra normativa não tem fonte. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Crie grade safra×idade, preserve células não observáveis e compare idades equivalentes.

## 6. Exemplo de situação

Preencha o briefing com um caso real equivalente ao cenário demonstrado no notebook, mantendo recursos, período e unidade de análise explícitos.

## 7. O que você precisa antes de usar?

Tenha dataset, entidade/chave, safra, idade, evento, denominador, métrica e censura. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Entrega um pedido estruturado. O contrato do briefing lista os artefatos esperados; confira separadamente o que foi apenas proposto, executado ou validado.

## 9. Como usar este recurso no Hub?

Abra [safra.md](safra.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_safra.py) demonstra o preenchimento. O exemplo sobrescreve `workspace.default.hub_exemplo_safras`; base sintética não cria regra regulatória.

## 10. Decisões e configurações que mais importam

Entrada na coorte, MOB, evento cumulativo, denominador, censura e maturidade comum.

## 11. Limitações, riscos e armadilhas

Somar taxas cumulativas, dupla contagem e atribuir causa a mix/maturação. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use `vintage_analysis` para cálculo reutilizável; survival para censura mais formal.

## 13. Como saber se o resultado faz sentido?

Reconcilie entidades, numerador, denominador, células imaturas e maturidade comum. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](safra.md), o [notebook](exemplo_safra.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

A descrição foi confrontada com [safra.md](safra.md) e [exemplo_safra.py](exemplo_safra.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
