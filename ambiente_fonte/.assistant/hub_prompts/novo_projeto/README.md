# `novo_projeto` — iniciar projeto analítico com contexto reutilizável

<!-- readme-objeto: 1.0.0 -->

Briefing para charter, árvore de projeto, contexto local e backlog antes de criar recursos. O prompt organiza o pedido, mas não executa a tarefa sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para charter, árvore de projeto, contexto local e backlog antes de criar recursos. |
| Para que serve? | Evitar arquitetura prematura e tornar objetivo, owners, métricas e ambientes verificáveis. |
| Use quando... | Há problema/decisão e stakeholders a organizar. |
| Evite quando... | É usado como substituto da descoberta com negócio ou sem owner/prazo. |
| Precisa de... | Nome, objetivo, donos, métricas, fontes, entidade/target, entregáveis, ambientes, repo e modo. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](novo_projeto.md) e leia o [notebook de exemplo](exemplo_novo_projeto.py).

## 1. O que é?

Briefing para charter, árvore de projeto, contexto local e backlog antes de criar recursos. O arquivo `novo_projeto.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Projetos começam mal quando solução é escolhida antes de problema, governança e definition of done.

## 3. Quando faz sentido usar?

Use quando há problema/decisão e stakeholders a organizar. Evitar arquitetura prematura e tornar objetivo, owners, métricas e ambientes verificáveis.

## 4. Quando não usar?

Evite quando é usado como substituto da descoberta com negócio ou sem owner/prazo. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Defina charter e limites, proponha estrutura simples e use `AGENTS.md` apenas no diretório correto; separe plano de criação/deploy.

## 6. Exemplo de situação

Preencha o briefing com um caso real equivalente ao cenário demonstrado no notebook, mantendo recursos, público e objetivo explícitos.

## 7. O que você precisa antes de usar?

Tenha nome, objetivo, donos, métricas, fontes, entidade/target, entregáveis, ambientes, repo e modo. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Entrega um pedido estruturado. O contrato do briefing lista os artefatos esperados; confira separadamente o que foi proposto, executado ou validado.

## 9. Como usar este recurso no Hub?

Abra [novo_projeto.md](novo_projeto.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_novo_projeto.py) demonstra o preenchimento. O exemplo cria `workspace.default.hub_exemplo_clientes` só como contexto sintético; o modo pedido é somente plano.

## 10. Decisões e configurações que mais importam

Objetivo mensurável, owner/aprovador, guardrails, diretório ancestral, ambientes e modo.

## 11. Limitações, riscos e armadilhas

Duplicar instruções globais, incluir segredos, criar recursos cedo ou confundir convenção local com recurso oficial. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Para pipeline definido use `pipeline`; para baseline use `baseline_orchestration`.

## 13. Como saber se o resultado faz sentido?

Confirme local do `AGENTS.md`, ausência de segredos/placeholders e aceite de cada entregável. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](novo_projeto.md), o [notebook](exemplo_novo_projeto.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

A descrição foi confrontada com [novo_projeto.md](novo_projeto.md) e [exemplo_novo_projeto.py](exemplo_novo_projeto.py) na base R11. Para comportamento atual de Genie Code, Agent Skills e instruções, consulte a documentação oficial do Databricks antes de operar em produção.
