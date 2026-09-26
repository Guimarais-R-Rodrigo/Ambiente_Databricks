# `taxa_resposta_campanha` — uma taxa acompanhada de sua incerteza

<!-- readme-objeto: 1.0.0 -->

Este exemplar mostra como apresentar a proporção de respostas de uma campanha
junto da precisão da estimativa, em vez de decidir olhando apenas a maior taxa.
É **material dos padrões do Hub**, não um novo helper operacional nem uma
implementação homologada para produção.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Exemplar de snippet que resume respostas por segmento. |
| Para que serve? | Mostrar taxa, tamanho da base e intervalo de Wilson juntos. |
| Use quando... | Quiser estudar o padrão e medir uma resposta binária por grupo. |
| Evite quando... | Precisar provar causalidade ou decidir apenas pelo maior percentual. |
| Precisa de... | DataFrame PySpark, um contato por linha, segmento e resposta 0/1. |
| Entrega... | DataFrame agregado, com percentuais, intervalo e marca de base mínima. |

Comece pela [implementação](taxa_resposta_campanha.py) ou pelo
[notebook](exemplo_taxa_resposta_campanha.py). **O notebook sobrescreve uma tabela
sintética persistente; o helper não escreve tabelas.** Confira a seção 9 antes
de executar o exemplo.

## 1. O que é?

Uma taxa de resposta é a quantidade de contatos que responderam dividida pela
quantidade de contatos avaliados. Ela resume o que aconteceu, mas não mostra
sozinha quanta informação sustenta a estimativa.

Este snippet é uma função reutilizável que calcula essa taxa por segmento e
acrescenta um intervalo de confiança de Wilson. O intervalo ajuda a representar
incerteza sob um modelo de respostas binárias; não é garantia de que a próxima
campanha ficará dentro daqueles limites. A função desta pasta também inclui
uma regra local de tamanho mínimo de grupo, separada do cálculo estatístico.

## 2. Que problema este recurso resolve?

A pergunta é: “Estes segmentos têm taxas parecidas, mas a precisão das estimativas
também é parecida?”. A tabela apoia a revisão de resultados antes de priorizar
uma investigação ou planejar outra campanha. Ela não distribui orçamento,
não estima receita e não escolhe automaticamente quem contatar.

## 3. Quando faz sentido usar?

Faz sentido em uma campanha encerrada, com definição consistente de resposta e
um contato por linha: assim, numerador e denominador se referem ao mesmo evento.
Também ajuda a perceber a diferença entre grupos grandes e pequenos, porque
exibe quantidade observada e incerteza ao lado do percentual.

Como exemplar, é útil a quem está aprendendo a organizar uma pasta do Hub:
fachada, cálculo, notebook e guia humano têm responsabilidades diferentes.

## 4. Quando não usar?

Não use esta tabela para atribuir um aumento de respostas à oferta ou ao canal.
A função não recebe grupo de controle nem identifica efeitos causais. Também
não a use diretamente quando uma pessoa aparece em várias linhas dependentes:
a contagem por contato pode não representar a unidade da decisão, e o cálculo
não ajusta essa dependência.

Uma campanha ainda aberta é outro contraexemplo: comparar grupos com tempos de
exposição diferentes pode confundir atraso de resposta com menor interesse.
Resolver essa definição vem antes de chamar a função.

## 5. Como funciona, intuitivamente?

Primeiro, a função verifica as colunas, os parâmetros básicos e se a resposta
contém nulos ou valores fora de 0/1. Encontrando resposta inválida, ela interrompe
com `ValueError`, sem decidir silenciosamente que nulo significa não resposta.

Depois, agrupa os contatos, conta linhas e soma respostas. Calcula a proporção,
os limites de Wilson e a largura do intervalo; converte as medidas em percentual
e ordena os grupos pela taxa. Por fim, `decidivel` compara apenas a quantidade
de contatos com o mínimo informado. Essa marca não mede viés, independência ou
significância de uma diferença entre grupos.

## 6. Exemplo de situação

Considere uma campanha fictícia. Um segmento teve 20 respostas em 500 contatos;
outro teve duas em 50. Ambos mostram 4%. O primeiro tem mais observações, embora
isso não elimine eventual viés de seleção.

Com o mínimo padrão de 100 contatos, a marca `decidivel` seria verdadeira no
primeiro grupo e falsa no segundo. Esse é um exemplo aritmético e uma leitura
da condição implementada, **não uma transcrição de execução PySpark nesta
sprint**. O próximo passo é examinar os intervalos e o contexto, não transferir
a decisão inteira para a marca booleana.

## 7. O que você precisa antes de usar?

O argumento `dados` deve ser um DataFrame PySpark. Informe `coluna_segmento` e
uma coluna de resposta numérica com 0 para não resposta e 1 para resposta; o
nome padrão desta última é `respondeu`. Defina o período e o que conta como
resposta antes de montar a base.

O grão esperado é um contato por linha. A função não recebe chave de cliente,
não remove duplicatas, não verifica maturação da campanha e não valida a
independência dos contatos. Essas condições pertencem à preparação e à revisão
do analista. É necessária uma sessão Spark compatível com as operações usadas;
esta R01 não certificou runtime Databricks.

## 8. O que este recurso entrega?

| Campo | Significado |
|---|---|
| `segmento` | Grupo, renomeado a partir da coluna informada. |
| `contatados` / `respostas` | Número de linhas e soma da resposta binária. |
| `taxa_pct` | Proporção multiplicada por 100, arredondada a duas casas. |
| `ic_inferior_pct` / `ic_superior_pct` | Limites de Wilson na mesma escala percentual. |
| `largura_ic_pp` | Largura do intervalo em pontos percentuais. |
| `decidivel` | Verdadeiro quando o tamanho do grupo atinge o mínimo configurado. |

Um intervalo de confiança não é previsão do número de respostas futuras.
Seu limite superior tampouco é um teto absoluto de respostas possíveis. Se a
base estiver vazia, não há segmento a resumir: não interprete ausência de linhas
como taxa igual a zero.

## 9. Como usar este recurso no Hub?

Leia a [fachada pública](__init__.py) e acompanhe o
[notebook de demonstração](exemplo_taxa_resposta_campanha.py), começando pelos
requisitos e pela preparação. O exemplo usa o import
`from hub_padroes.snippet.taxa_resposta_campanha import taxa_resposta_campanha`.
Esse caminho é de material didático; não substitui a escolha de um helper
operacional apropriado no catálogo.

A função lê o DataFrame e retorna uma transformação, sem persistir tabela.
Há uma ação de contagem na validação; retornar um DataFrame não significa que
toda a chamada seja sem execução ou custo.

O notebook usa `mode("overwrite").saveAsTable` em
`workspace.default.hub_exemplo_campanha`. Isso pode substituir uma tabela
existente com o mesmo nome. Confira destino e autorização antes da preparação.
Nenhum notebook foi executado no Databricks nesta revisão documental.

## 10. Decisões e configurações que mais importam

`z=1.96` corresponde aproximadamente ao nível nominal bilateral de 95% na
construção utilizada. A função aceita `0 < z <= 5`; escolher outro valor muda
os limites, não a contagem observada. O nível nominal não corrige amostragem
inadequada nem dependência entre observações.

`minimo_para_decisao=100` é política local calibrável, não número universal de
suficiência estatística. `coluna_segmento` define quais pessoas são resumidas
juntas; mudar essa divisão muda a pergunta. A coluna de resposta precisa manter
a mesma semântica em todos os grupos.

## 11. Limitações, riscos e armadilhas

Mesmo em uma aplicação adequada, ordenar pela maior taxa não equivale a testar
diferenças, corrigir comparações múltiplas ou otimizar resultado financeiro.
A função não calcula ajuste por seleção, custo de contato ou potencial de
resposta incremental.

Ela também não fornece um ajuste para populações finitas ou contatos
correlacionados. Os requisitos sobre dados devem ser revistos antes de usar o
intervalo para generalizar resultados. No notebook histórico há interpretações
mais fortes que o retorno sustenta; a nota R01 delimita esse problema sem
alterar o código ou fabricar uma nova execução.

## 12. Quais são as alternativas?

Para uma descrição apenas do conjunto observado, uma agregação de contagens e
taxas pode bastar, desde que o denominador apareça. Para escolher uma intervenção
ou comparar grupos formalmente, é necessário um desenho e uma análise próprios,
que este exemplar não implementa.

Para verificar problemas básicos antes da medição, estude o
[exemplar de checagem](../../script/checar_base_campanha/README.md). Ele é
complementar, não substituto do cálculo ou de uma validação estatística.

## 13. Como saber se o resultado faz sentido?

Reconte contatos e respostas em um grupo pequeno conhecido. Confira que a taxa
é `100 × respostas / contatados`, que as unidades são percentuais e que a marca
`decidivel` muda apenas ao cruzar o mínimo configurado. Verifique se os limites
estão entre 0% e 100%, admitida a precisão numérica da apresentação.

Depois, faça a revisão que o código não realiza: duplicidade, definição de
resposta, maturação, seleção e dependência. Um cálculo conferido não resolve
automaticamente essas questões.

## 14. Arquivos relacionados e próximos passos

| Arquivo | Papel |
|---|---|
| [Implementação](taxa_resposta_campanha.py) | Fórmula, parâmetros e validações reais. |
| [Fachada](__init__.py) | Função e constante exportadas. |
| [Notebook](exemplo_taxa_resposta_campanha.py) | Demonstração com preparo que escreve tabela. |
| [Molde de snippet](../template.md) | Estrutura do objeto a construir. |
| [Molde deste guia](../../readme/template_objeto.md) | Contrato editorial comum. |

## 15. Referências

A [implementação local](taxa_resposta_campanha.py) sustenta as afirmações sobre
contrato e comportamento. A expressão de Wilson foi conferida na documentação
primária do [NIST sobre limites para proporções binomiais](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/agcoulci.htm),
consultada em 12/09/2026; a página apresenta a expressão usada neste código.

Revisão R01: leitura estática do módulo, fachada e notebook; revisão do próprio
autor, sem auditor independente. Fórmula ilustrativa não é execução do helper.
Teste Spark/Databricks e aceite humano permanecem separados e pendentes.
