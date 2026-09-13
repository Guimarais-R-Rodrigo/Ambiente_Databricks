# `tutor_explicar` — explicar código e conceitos no nível certo

<!-- readme-objeto: 1.0.0 -->

Briefing de tutoria para código, tabela, erro ou pipeline anexado. O prompt organiza o pedido, mas não executa a tarefa sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing de tutoria para código, tabela, erro ou pipeline anexado. |
| Para que serve? | Adaptar profundidade e vocabulário ao nível e objetivo prático. |
| Use quando... | O objeto real está anexado e a dúvida é concreta. |
| Evite quando... | É usado como revisão de código ou fonte única para comportamento de plataforma. |
| Precisa de... | Objeto/pergunta, nível, profundidade, objetivo, ambiente, contexto e restrições. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](tutor_explicar.md) e leia o [notebook de exemplo](exemplo_tutor_explicar.py).

## 1. O que é?

Briefing de tutoria para código, tabela, erro ou pipeline anexado. O arquivo `tutor_explicar.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Explicação genérica pode estar correta e ainda não ensinar. O formulário ancora a resposta no objeto e na tarefa futura.

## 3. Quando faz sentido usar?

Use quando o objeto real está anexado e a dúvida é concreta. Adaptar profundidade e vocabulário ao nível e objetivo prático.

## 4. Quando não usar?

Evite quando é usado como revisão de código ou fonte única para comportamento de plataforma. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Comece com mapa mental, defina termos e avance ao detalhe; diferencie comportamento documentado, prática e opinião.

## 6. Exemplo de situação

Preencha o briefing com um caso real equivalente ao cenário demonstrado no notebook, mantendo recursos, público e objetivo explícitos.

## 7. O que você precisa antes de usar?

Tenha objeto/pergunta, nível, profundidade, objetivo, ambiente, contexto e restrições. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Entrega um pedido estruturado. O contrato do briefing lista os artefatos esperados; confira separadamente o que foi proposto, executado ou validado.

## 9. Como usar este recurso no Hub?

Abra [tutor_explicar.md](tutor_explicar.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_tutor_explicar.py) demonstra o preenchimento. O exemplo é somente leitura de `pit_join.py`; nenhuma tabela é criada.

## 10. Decisões e configurações que mais importam

Nível, granularidade, ambiente/versão, objetivo prático e permissão para experimento.

## 11. Limitações, riscos e armadilhas

Explicar código não lido, usar API obsoleta ou confundir tutoria com revisão. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Para editar documentação use `comentar_notebook`; para avaliar correção use auditoria/revisão.

## 13. Como saber se o resultado faz sentido?

Cheque se exemplos usam o objeto real, termos estão definidos e claims de plataforma têm versão/referência. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](tutor_explicar.md), o [notebook](exemplo_tutor_explicar.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

A descrição foi confrontada com [tutor_explicar.md](tutor_explicar.md) e [exemplo_tutor_explicar.py](exemplo_tutor_explicar.py) na base R11. Para comportamento atual de Genie Code, Agent Skills e instruções, consulte a documentação oficial do Databricks antes de operar em produção.
