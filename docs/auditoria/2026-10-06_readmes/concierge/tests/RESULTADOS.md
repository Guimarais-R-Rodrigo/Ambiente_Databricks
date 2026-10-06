# Resultados — Concierge Hub 0.2.0

Data: 2026-09-12. Base de integração:
`f748c144dbb6909c7437b53498b25dd4f4854ab7`.
Ambiente local: Python 3.13.5, Linux. Sem credenciais ou chamadas Databricks.

## Verificações executadas

Validador estático do pacote:

```text
PASS: estrutura, frontmatter, links locais, sintaxe e matriz de aceite.
NAO VALIDADO: roteamento, recomendacoes reais, Databricks e permissoes.
```

Regressões do verificador: 14 testes, zero falhas, zero skips.
Incluem as 12 regressões do protótipo e dois casos novos: raiz simbólica
recusada antes de resolver o path e divergência entre categoria/ativação da matriz.
A cópia histórica e seus resultados não foram reescritos.

Integração canônica: 12 testes, zero falhas, zero skips, executados pelo arquivo
`tools/tests/test_concierge_integracao.py` no checkout. Conferem política,
frontmatter, rota opcional nas instruções, inventário/cópia do Manual, caminhos
de helpers, símbolos públicos, matriz pendente, fonte/espelho e estágios do CI.
Não importam os helpers nem testam sua execução no workspace.

## Matriz conversacional

26 casos preparados: 7 positivos, 4 negativos, 2 menções e 13 casos de borda.
Todos continuam PENDENTE como expectativas; não são resultados de uso do Genie.
O caso E13 explicita comando de execução embutido em documento recuperado, sem
confundi-lo com uma autorização nova dada pelo usuário.

Os casos básicos 14P/14N/14M foram acrescentados ao roteiro do repositório.
O 39/39 antigo permanece histórico; não representa aprovação da nova skill nem
do conjunto ampliado. Regressões das vizinhas e do mapa de instruções no destino
permanecem pendentes.

## Limites

Integração Git, não instalação ou homologação. Não houve publicação no Free ou
no trabalho, alteração de ACL, consultas, treinamento ou chamadas remotas.
O relatório de integração do repositório registra o CI completo separadamente
em `docs/testes/2026-09-12_concierge-integracao.md`. A presença de um arquivo,
a correção estática e a execução conversacional continuam evidências distintas.
