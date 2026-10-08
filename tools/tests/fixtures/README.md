# Entradas sintéticas dos testes

Fixtures são exemplos controlados para casos positivos e negativos; não são
configuração de produção nem dados do trabalho.

| Entrada | Uso |
|---|---|
| [ci_recipe_contract.json](ci_recipe_contract.json) | Contrato de receitas usado nas regressões do compilador de CI |
| [micromodelos_mm01/](micromodelos_mm01/) | Especificação válida e casos inválidos dos Micromodelos |
| [micromodelos_mm03/](micromodelos_mm03/) | Catálogo sintético para os contratos de metadados |

Mantenha fixtures pequenas e determinísticas. Para alterar uma expectativa,
confira qual teste a consome e por que o negativo precisa falhar; não atualize
entrada e expectativa em conjunto para mascarar um defeito. Nunca inclua PII,
credenciais ou extração corporativa. [Voltar às suítes](../README.md).
