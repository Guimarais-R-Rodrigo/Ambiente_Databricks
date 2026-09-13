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

Preencha o briefing com um caso real equivalente ao cenário demonstrado no notebook, mantendo recursos, público e objetivo explícitos.

## 7. O que você precisa antes de usar?

Tenha notebook/células, modo, público, profundidade, objetivo, convenções e restrições. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Entrega um pedido estruturado. O contrato do briefing lista os artefatos esperados; confira separadamente o que foi proposto, executado ou validado.

## 9. Como usar este recurso no Hub?

Abra [comentar_notebook.md](comentar_notebook.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_comentar_notebook.py) demonstra o preenchimento. O exemplo apenas lê `exemplo_pit_join.py`; o estado atual já exige saída colada nos notebooks de exemplo.

## 10. Decisões e configurações que mais importam

REVISÃO/EDIÇÃO/DOCUMENTAÇÃO, público, profundidade, partes imutáveis e PII.

## 11. Limitações, riscos e armadilhas

Refatorar sem autorização, repetir literalmente o código ou afirmar reexecução inexistente. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Para aprender código use `tutor_explicar`; para auditar output use `auditoria_skills`.

## 13. Como saber se o resultado faz sentido?

Compare código e ordem de células, confira referências e separe comentário factual de recomendação. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](comentar_notebook.md), o [notebook](exemplo_comentar_notebook.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

A descrição foi confrontada com [comentar_notebook.md](comentar_notebook.md) e [exemplo_comentar_notebook.py](exemplo_comentar_notebook.py) na base R11. Para comportamento atual de Genie Code, Agent Skills e instruções, consulte a documentação oficial do Databricks antes de operar em produção.
