# `comentar_notebook` — documentar notebook sem alterar lógica por acidente

<!-- readme-objeto: 1.0.0 -->

Briefing para revisar, editar documentação ou criar narrativa de notebook. O prompt organiza o pedido, mas não executa a tarefa sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para revisar, editar documentação ou criar narrativa de notebook. |
| Para que serve? | Calibrar documentação ao público e preservar comportamento quando exigido. |
| Use quando... | Notebook/células alvo e público estão definidos. |
| Evite quando... | O notebook ainda muda muito ou documentação é usada como refatoração implícita. |
| Precisa de... | Notebook/células, modo, público, profundidade, objetivo, convenções e restrições. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](comentar_notebook.md) e leia o [notebook de exemplo](exemplo_comentar_notebook.py).

## 1. O que é?

Briefing para revisar, editar documentação ou criar narrativa de notebook. O arquivo `comentar_notebook.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Comentários podem ficar obsoletos ou mascarar código pouco claro. O formulário separa revisão, edição e documentação.

## 3. Quando faz sentido usar?

Use quando notebook/células alvo e público estão definidos. Calibrar documentação ao público e preservar comportamento quando exigido.

## 4. Quando não usar?

Evite quando o notebook ainda muda muito ou documentação é usada como refatoração implícita. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Mapeie entradas, saídas e efeitos; depois altere somente a camada documental permitida e liste o que foi preservado.

## 6. Exemplo de situação

Revisar `exemplo_pit_join.py` para uma pessoa experiente em SQL e iniciante em Spark, tornando explícitos o propósito do join e o risco temporal. No modo REVISÃO, entregar sugestões; editar Markdown exige modo autorizado, preservando lógica e ordem das células.

## 7. O que você precisa antes de usar?

Tenha notebook/células, modo, público, profundidade, objetivo, convenções e restrições. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Solicita resumo das sugestões ou mudanças, inputs/outputs, dependências e execução segura, riscos, elementos preservados e validações não realizadas. No modo REVISÃO, não promete notebook reescrito. Output não observado deve ficar pendente, nunca inventado para preencher um template.

## 9. Como usar este recurso no Hub?

Preencha [comentar_notebook.md](comentar_notebook.md) e siga a [skill de documentação](../../skills/hub-ml-comentar-notebook/SKILL.md). O [exemplo](exemplo_comentar_notebook.py) lê `exemplo_pit_join.py` e pede sugestões. A presença de dados sensíveis e a permissão para sugerir células Markdown são campos distintos: classifique PII com evidência e mantenha `NÃO INFORMADO` quando não houver. Não execute o notebook alvo para obter outputs sem autorização.

## 10. Decisões e configurações que mais importam

REVISÃO/EDIÇÃO/DOCUMENTAÇÃO, público, profundidade, partes imutáveis e PII.

## 11. Limitações, riscos e armadilhas

Refatorar sem autorização, repetir literalmente o código ou afirmar reexecução inexistente. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use [Tutor](../tutor_explicar/README.md) para aprender código e [Auditoria](../auditoria_skills/README.md) para conferir aderência. [doc_coverage](../../hub_scripts/doc_coverage/README.md) mede somente adjacência de Markdown, não qualidade da explicação.

## 13. Como saber se o resultado faz sentido?

Compare código e ordem de células, confira referências e separe comentário factual de recomendação. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](comentar_notebook.md), o [notebook](exemplo_comentar_notebook.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](comentar_notebook.md) define os campos e a entrega; o [notebook](exemplo_comentar_notebook.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
