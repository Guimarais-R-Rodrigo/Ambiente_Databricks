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

Escolha IMPLEMENTAÇÃO ou OUTPUT, fixe o contrato e percorra frontmatter, recursos, segurança e testes antes do veredito.

## 6. Exemplo de situação

Preencha o briefing com um caso real equivalente ao cenário demonstrado no notebook, mantendo recursos, público e objetivo explícitos.

## 7. O que você precisa antes de usar?

Tenha modo, skill alvo, output/pedido quando aplicáveis, casos de uso, prompts de teste e dependências. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Entrega um pedido estruturado. O contrato do briefing lista os artefatos esperados; confira separadamente o que foi proposto, executado ou validado.

## 9. Como usar este recurso no Hub?

Abra [auditoria_skills.md](auditoria_skills.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_auditoria_skills.py) demonstra o preenchimento. O exemplo apenas lê um `SKILL.md`; não cria tabela.

## 10. Decisões e configurações que mais importam

Modo, contrato produtor, escopo user/workspace, dependências, severidade e autorização para corrigir.

## 11. Limitações, riscos e armadilhas

Confundir palavra-chave com descobribilidade, editar description sem reteste ou aprovar script não executado. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Para explicar uma skill use `tutor_explicar`; para documentação use `comentar_notebook`.

## 13. Como saber se o resultado faz sentido?

Monte matriz requisito→evidência, valide caminhos/scripts e registre o que não foi executado. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](auditoria_skills.md), o [notebook](exemplo_auditoria_skills.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

A descrição foi confrontada com [auditoria_skills.md](auditoria_skills.md) e [exemplo_auditoria_skills.py](exemplo_auditoria_skills.py) na base R11. Para comportamento atual de Genie Code, Agent Skills e instruções, consulte a documentação oficial do Databricks antes de operar em produção.
