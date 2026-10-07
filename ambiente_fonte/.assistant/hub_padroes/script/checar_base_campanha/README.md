# `checar_base_campanha` — verificar a base antes de medir a campanha

<!-- readme-objeto: 1.0.0 -->

Este exemplar mostra como transformar problemas de uma tabela em um diagnóstico
legível, sem tentar corrigir os dados automaticamente. É **referência dos
padrões do Hub**, não um script de produção homologado.


Antes de confiar em `pass`, confira `linhas > 0`: base vazia pode passar. `pct_nulo_alerta` é inativo; qualquer resposta nula gera `fail`, que é retorno, não exceção. A função lê; o preparo do notebook pode sobrescrever tabela persistente. O check de grão compara linhas e chaves distintas, sem separar duplicidade de chave nula. Exemplo interpretativo: `status="fail"` pede inspeção dos checks, não corrige dados nem bloqueia sozinho o código seguinte.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Exemplar de script que recebe o nome de uma tabela. |
| Para que serve? | Apontar problemas de chave, resposta e tamanho de grupos. |
| Use quando... | Quiser estudar um diagnóstico anterior à medição. |
| Evite quando... | Precisar de certificação completa ou bloqueio automático. |
| Precisa de... | Sessão Spark, acesso à tabela e colunas definidas. |
| Entrega... | Dicionário com status, contagens, limites e alertas. |

A [implementação](checar_base_campanha.py) apenas lê. O
[notebook](exemplo_checar_base_campanha.py) **sobrescreve e depois remove uma
tabela persistente de demonstração**. Confira seus efeitos antes de executar.

## 1. O que é?

Um diagnóstico de qualidade verifica condições explícitas e relata onde elas
não foram atendidas. Não significa que o programa conheça todas as regras de
negócio. Este script compara linhas com chaves distintas, inspeciona o domínio
da resposta e procura segmentos menores que um limite configurado.

Ele recebe o endereço de um recurso já existente, em vez de um DataFrame pronto.
Essa é a diferença didática que este exemplar ilustra em relação ao snippet
de taxa de resposta.

## 2. Que problema este recurso resolve?

A pergunta é: “Há algum problema básico nesta base que eu precise decidir antes
de confiar na taxa de resposta?”. Uma chave repetida pode fazer algumas pessoas
pesarem mais que outras. Uma resposta nula pode representar informação ausente,
e não ausência de resposta. O diagnóstico torna essas questões visíveis antes
do cálculo, sem remover linhas nem alterar a tabela.

## 3. Quando faz sentido usar?

Use como referência de forma ao criar um script de diagnóstico: ele mostra a
separação entre configuração, contagens e mensagens. No cenário analítico do
exemplar, ele é pertinente quando a unidade pretendida é um contato por chave,
a resposta deveria ser 0/1 e os grupos precisam ter seus tamanhos examinados.

Depois de um cruzamento de tabelas, a comparação entre linhas e chaves pode
ajudar a encontrar expansão inesperada. A conclusão ainda depende de verificar
se a chave escolhida representa realmente a unidade do estudo.

## 4. Quando não usar?

Não o trate como certificado geral da base: ele não valida todas as colunas,
regras temporais, cobertura da campanha ou viés de seleção. Uma base que passa
nessas verificações pode continuar inadequada ao objetivo.

Também não use `id_cliente` como chave única quando várias campanhas foram
misturadas e cada cliente pode aparecer legitimamente uma vez por campanha.
Nesse caso, a pergunta e a preparação da base precisam mudar; o exemplar não
recebe uma lista de colunas para formar chave composta.

## 5. Como funciona, intuitivamente?

A função mescla os limites recebidos com os padrões, obtém uma sessão Spark e
lê a tabela. Verifica a presença das três colunas solicitadas. Em seguida,
calcula um resumo global e lista os segmentos pequenos.

Os alertas de grão ou de resposta têm severidade `fail`; base pequena produz
`warn`. O status geral prioriza `fail`, depois `warn` e, sem alertas, `pass`.
Esse status é um valor devolvido, não uma ordem de correção ou cancelamento de
um job. Coluna ausente, por outro lado, gera `ValueError`; falha de acesso pode
interromper a chamada antes de existir diagnóstico.

## 6. Exemplo de situação

Imagine uma tabela fictícia de uma única campanha com 1.000 linhas e 980
identificadores distintos. A diferença pede investigação: pode haver duplicatas
ou chaves ausentes, e não se deve concluir apenas pelo total qual é a causa.

O script gera alerta de grão quando as contagens diferem. O analista investiga
a chave e o processo de preparação antes de calcular taxas. Estes números são
ilustrativos, não resultados de uma execução observada. Confirme versão,
ambiente e resultados na execução real.

## 7. O que você precisa antes de usar?

Informe `tabela`, preferencialmente com catálogo, schema e nome confirmados no
ambiente. Os nomes padrão são `segmento`, `respondeu` e `id_cliente`; podem ser
substituídos pelos parâmetros correspondentes. Para uma view temporária, a
sessão que a contém precisa ser a mesma utilizada pela função.

Confirme permissões de leitura e a unidade de cada linha. O código não aplica
filtro de período nem recebe definição de campanha: a tabela fornecida precisa
representar o recorte pretendido. Ele exige PySpark e sessão disponível. Esta
revisão não certifica que todos os runtimes suportam o mesmo cenário.

## 8. O que este recurso entrega?

| Chave | Conteúdo |
|---|---|
| `tabela` | Recurso informado à função. |
| `status` | `pass`, `warn` ou `fail`, conforme os alertas implementados. |
| `limites` | Dicionário de padrões mesclados com as sobreposições recebidas. |
| `checagens` | Linhas, chaves distintas, respostas nulas/fora do domínio e grupos pequenos. |
| `alertas` | Lista de checagem, severidade e mensagem. |

`pass` significa somente ausência dos alertas implementados. `fail` no retorno
não lança uma exceção por si só. O chamador decide como tratar o diagnóstico,
com autorização apropriada para qualquer correção.

## 9. Como usar este recurso no Hub?

Leia a [fachada](__init__.py) e o
[notebook](exemplo_checar_base_campanha.py). O caminho mostrado é
`from hub_padroes.script.checar_base_campanha import checar_base_campanha`.
É import de exemplar, não recomendação de adotar este código em produção.

O helper não escreve nem registra MLflow. O notebook pressupõe a tabela do
[exemplo de snippet](../../snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha.py),
cria `workspace.default.hub_exemplo_campanha_dup` por `saveAsTable` com
`overwrite` e depois usa `DROP TABLE`. Apesar da palavra “temporária” no relato
histórico, a preparação usa tabela persistente. Confira recursos e autorização;
não execute todo o notebook indiscriminadamente.

## 10. Decisões e configurações que mais importam

`min_contatos_por_segmento=100` controla quais grupos geram alerta de base
pequena. Esse mínimo é uma política do exemplo, não uma garantia estatística.
A chave e a coluna de resposta definem o que se está diagnosticando.

pct_nulo_alerta não controla os alertas nesta implementação: qualquer resposta nula gera fail. O argumento limites não valida todas as chaves, tipos e intervalos.

## 11. Limitações, riscos e armadilhas

O código não reprova explicitamente uma tabela vazia. Assim, zero linhas pode
terminar em `pass`; confira `checagens["linhas"]` antes de interpretar o status.
Chaves nulas também podem causar diferença entre linhas e chaves distintas:
o alerta não separa esse caso de duplicidade real.

Há duas chamadas explícitas de `collect`: uma traz o resumo global e outra a
lista de grupos pequenos. A segunda pode ser grande com alta cardinalidade.
Não transforme a descrição antiga de “três varreduras” em medição garantida de
custo físico. O plano, o volume e o ambiente importam. Os blocos históricos do
notebook não foram reexecutados nem certificados nesta revisão.

## 12. Quais são as alternativas?

Para usar um recurso operacional do Hub, consulte
[`data_quality_check`](../../../hub_scripts/data_quality_check/data_quality_check.py)
e confira seu contrato próprio: ele não precisa retornar as mesmas chaves
que este exemplar. Para conhecer a tabela de maneira exploratória, consulte
[`quick_profile`](../../../hub_scripts/quick_profile/quick_profile.py).

Uma consulta específica pode ser mais apropriada quando a regra de negócio
não está entre as verificações implementadas. Não force este diagnóstico a
responder uma pergunta que ele não conhece.

## 13. Como saber se o resultado faz sentido?

Confira o nome do recurso e as colunas. Reconte um caso sintético pequeno com
chave duplicada, outro com resposta nula e outro com grupo abaixo do mínimo.
Verifique contagens e alertas, não apenas a palavra `status`.

Inclua um caso vazio na revisão, justamente porque o helper não o bloqueia.
Confirme também que mudar `pct_nulo_alerta` não está sendo apresentado como
tratamento de nulos. A saída ajuda a investigar; a decisão de uso exige
checagens adicionais do domínio.

## 14. Arquivos relacionados e próximos passos

| Arquivo | Papel |
|---|---|
| [Implementação](checar_base_campanha.py) | Condições e alertas realmente implementados. |
| [Fachada](__init__.py) | Função e limites exportados. |
| [Notebook](exemplo_checar_base_campanha.py) | Demonstração com escrita e remoção de tabela. |
| [Molde de script](../template.md) | Estrutura de um novo diagnóstico. |
| [Guia de taxa](../../snippet/taxa_resposta_campanha/README.md) | Exemplar complementar de medição. |

## 15. Referências

O contrato foi confrontado com a [implementação](checar_base_campanha.py) e a
[fachada](__init__.py). A semântica de contagem, incluindo valores distintos
não nulos, pode ser conferida na documentação oficial de
[funções SQL do Apache Spark](https://spark.apache.org/docs/latest/api/sql/index.html),
consultada em 12/09/2026. Isso não substitui teste no runtime de destino.

Antes de usar, confirme PySpark e sessão compatíveis no seu ambiente. Este exemplar não certifica a base nem substitui validação de negócio.
