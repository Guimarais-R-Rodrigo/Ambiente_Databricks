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

Uma pessoa intermediária em SQL e iniciante em Spark quer entender por que `pit_join` considera atraso de publicação antes de adaptá-lo. A explicação deve distinguir data do evento, disponibilidade e decisão, sem executar o módulo ou modificar o notebook.

## 7. O que você precisa antes de usar?

Forneça objeto/pergunta, nível, profundidade, objetivo e ambiente/versão. Anexe o módulo inteiro quando pedir explicação integral: o preparo lê o arquivo local e **imprime só as 20 primeiras linhas**; isso não comprova que o chat recebeu o conteúdo completo.

## 8. O que este recurso entrega?

Solicita resposta direta conceitual, explicação em camadas, exemplo mínimo, armadilhas/checklist, duas perguntas de autoavaliação e referências pertinentes à versão. No exercício, a resposta direta não deve entregar a adaptação pronta antes de explicar o raciocínio; ensino e solução completa são entregas diferentes.

## 9. Como usar este recurso no Hub?

Preencha [tutor_explicar.md](tutor_explicar.md) e siga a [skill Tutor](../../skills/hub-ml-tutor-databricks/SKILL.md). A orientação não exige runner de outra skill; consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) se o fluxo mudar. O [preparo](exemplo_tutor_explicar.py) lê `pit_join.py` sem criar tabela; sua impressão parcial não prova contexto integral. Parte 3: **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

Nível, granularidade, ambiente/versão, objetivo prático e permissão para experimento.

## 11. Limitações, riscos e armadilhas

Explicar código não lido, usar API obsoleta ou confundir tutoria com revisão. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use [Comentar Notebook](../comentar_notebook/README.md) para documentação e [Auditoria](../auditoria_skills/README.md) para aderência/correção sob contrato. Aprender um conceito não equivale a auditar execução.

## 13. Como saber se o resultado faz sentido?

Cheque se exemplos usam o objeto real, termos estão definidos e claims de plataforma têm versão/referência. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](tutor_explicar.md), o [notebook](exemplo_tutor_explicar.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](tutor_explicar.md) define os campos e a entrega; o [notebook](exemplo_tutor_explicar.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
