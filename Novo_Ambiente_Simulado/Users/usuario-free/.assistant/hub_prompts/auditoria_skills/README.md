# `auditoria_skills` — auditar uma skill ou o output produzido por ela

<!-- readme-objeto: 1.0.0 -->

Briefing para auditar implementação de agent skill ou artefato contra o contrato produtor. O prompt organiza o pedido, mas não executa a tarefa sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para auditar implementação de agent skill ou artefato contra o contrato produtor. |
| Para que serve? | Separar descobribilidade, estrutura, segurança, execução e aderência. |
| Use quando... | Skill/output e pedido original podem ser anexados conforme o modo. |
| Evite quando... | A auditoria seria feita de memória ou correção foi autorizada sem diagnóstico. |
| Precisa de... | Modo, skill alvo, output/pedido quando aplicáveis, casos de uso, prompts de teste e dependências. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](auditoria_skills.md) e leia o [notebook de exemplo](exemplo_auditoria_skills.py).

## 1. O que é?

Briefing para auditar implementação de agent skill ou artefato contra o contrato produtor. O arquivo `auditoria_skills.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Um Markdown bem formado pode apontar para recurso inexistente ou rotear mal. Auditoria exige evidência além de abrir o arquivo.

## 3. Quando faz sentido usar?

Use quando skill/output e pedido original podem ser anexados conforme o modo. Separar descobribilidade, estrutura, segurança, execução e aderência.

## 4. Quando não usar?

Evite quando a auditoria seria feita de memória ou correção foi autorizada sem diagnóstico. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Escolha dois eixos independentes: **objeto** `IMPLEMENTAÇÃO` ou `OUTPUT`; **ação** `AUDITORIA`, `PLANO DE CORREÇÃO` ou `CORRIGIR AUTORIZADO`. Fixe o contrato e percorra estrutura, recursos, segurança e evidência. Escolher OUTPUT não autoriza editar o artefato.

## 6. Exemplo de situação

Auditar [hub-ml-criar-objeto](../../skills/hub-ml-criar-objeto/SKILL.md), anexando o `SKILL.md` e suas dependências, sem alterar `description`. Conferir criação de snippet e possível colisão com um pedido de cálculo de PSI. O preparo do notebook lê o arquivo publicado; essa leitura não executa o runner de auditoria.

## 7. O que você precisa antes de usar?

Informe o objeto da auditoria e a ação permitida separadamente. Anexe skill alvo, dependências e casos positivos/negativos de descoberta. Em OUTPUT, inclua ainda pedido original e contrato da skill produtora. Campos ausentes ficam `NÃO INFORMADO`; testes e arquivos não acessados não podem ser presumidos.

## 8. O que este recurso entrega?

A entrega solicitada contém inventário; achados P0–P3 com caminho, evidência e impacto; matriz requisito→evidência→status; e plano de testes de descoberta. Diff e validações após correção só cabem quando a correção tiver sido autorizada. Um veredito editorial não substitui o verificador da skill produtora.

## 9. Como usar este recurso no Hub?

Preencha [auditoria_skills.md](auditoria_skills.md) e siga a [skill Auditoria](../../skills/hub-ml-auditoria-skills/SKILL.md), incluindo preflight, runner e consulta da [policy vigente](../../hub_padroes/skill_enforcement/policy.json). O [notebook](exemplo_auditoria_skills.py) apenas lê um `SKILL.md`, sem criar tabela. Registre separadamente `citado → localizado → lido → importado → chamado → concluído`; um degrau não prova o seguinte. PASS persistido é estado observado; só a execução do verificador canônico sobre o artefato atual sustenta reverificação.

## 10. Decisões e configurações que mais importam

Objeto auditado, ação autorizada, contrato produtor, escopo user/workspace, dependências e severidade. Alterar `description` exige retestar descoberta; não é consequência de pedir auditoria.

## 11. Limitações, riscos e armadilhas

Confundir palavra-chave com descobribilidade, editar description sem reteste ou aprovar script não executado. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use [Tutor](../tutor_explicar/README.md) para aprender e [Comentar Notebook](../comentar_notebook/README.md) para revisar documentação. Para OUTPUT, a [skill produtora](../../skills/README.md) é dona do contrato técnico.

## 13. Como saber se o resultado faz sentido?

Monte matriz requisito→evidência, valide caminhos/scripts e registre o que não foi executado. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](auditoria_skills.md), o [notebook](exemplo_auditoria_skills.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](auditoria_skills.md) define os campos e a entrega; o [notebook](exemplo_auditoria_skills.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
