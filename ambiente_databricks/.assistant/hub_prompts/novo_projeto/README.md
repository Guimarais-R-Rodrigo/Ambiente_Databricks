# `novo_projeto` — iniciar projeto analítico com contexto reutilizável

<!-- readme-objeto: 1.0.0 -->

Briefing para charter, árvore de projeto, contexto local e backlog antes de criar recursos. O prompt organiza o pedido, mas não executa a tarefa sozinho.

**Antes de executar o preparo:** ele sobrescreve `workspace.default.hub_exemplo_clientes` com `mode("overwrite")`. Esse destino também é usado por EDA, Baseline, Explainability, Novo Projeto, Pipeline e Stat Check: executar um exemplo pode substituir a base de outro. Use o briefing sem executar o preparo quando só precisar do texto.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para charter, árvore de projeto, contexto local e backlog antes de criar recursos. |
| Para que serve? | Evitar arquitetura prematura e tornar objetivo, owners, métricas e ambientes verificáveis. |
| Use quando... | Há problema/decisão e stakeholders a organizar. |
| Evite quando... | É usado para assumir decisões/compromissos sem descoberta ou responsável. |
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

Não use para substituir a descoberta com negócio nem assumir compromisso sem responsável. Owner, aprovador ou prazo ausentes são lacunas úteis ao plano condicionado; bloqueiam apenas compromissos e execução que dependam dessas decisões.

## 5. Como funciona, intuitivamente?

Defina charter e limites, proponha estrutura simples e use `AGENTS.md` apenas no diretório correto; separe plano de criação/deploy.

## 6. Exemplo de situação

Estruturar um projeto fictício de propensão a resposta, com fonte sintética conhecida e backlog de EDA. Time e consumidor são propostos; dono e aprovador efetivos, ambiente e repositório continuam pendentes. Os marcos pedidos são estimativas para revisão, não compromissos assumidos ou arquitetura aprovada.

## 7. O que você precisa antes de usar?

Tenha nome, objetivo, donos, métricas, fontes, entidade/target, entregáveis, ambientes, repo e modo. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Solicita charter mensurável, árvore justificada, `AGENTS.md` para revisão, backlog com dependências, critérios de aceite e lista de ações que exigem autorização. Gerar texto ou arquivos não significa deploy, publicação nem criação automática de recursos.

## 9. Como usar este recurso no Hub?

O [briefing](novo_projeto.md) pode ser usado sem executar a Parte 1. O [preparo](exemplo_novo_projeto.py) **sobrescreve** `workspace.default.hub_exemplo_clientes` com `mode("overwrite")`; pedir “somente plano” no chat não impede essa escrita preparatória. A Parte 3 permanece **NÃO EXECUTADO**. Não há associação obrigatória 1:1 a uma skill: escolha a rota depois de definir o resultado.

## 10. Decisões e configurações que mais importam

Objetivo mensurável, owner/aprovador, guardrails, diretório ancestral, ambientes e modo.

## 11. Limitações, riscos e armadilhas

Duplicar instruções globais, incluir segredos, criar recursos cedo ou confundir convenção local com recurso oficial. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use [Pipeline](../pipeline/README.md), [Baseline](../baseline_orchestration/README.md) ou [Micromodelo Novo](../micromodelo_novo/README.md) conforme o objetivo. O [Concierge](../../skills/hub-ml-concierge/SKILL.md) ajuda a descobrir recursos sem inventar acesso.

## 13. Como saber se o resultado faz sentido?

Confirme local do `AGENTS.md`, ausência de segredos/placeholders e aceite de cada entregável. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](novo_projeto.md), o [notebook](exemplo_novo_projeto.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](novo_projeto.md) define os campos e a entrega; o [notebook](exemplo_novo_projeto.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
