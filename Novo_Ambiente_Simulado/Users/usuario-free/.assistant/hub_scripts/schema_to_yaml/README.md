# `schema_to_yaml` — transformar schema em texto revisável sem confundir fotografia com contrato

<!-- readme-objeto: 1.0.0 -->

Um schema pode ser inspecionado no Spark, mas muitas revisões precisam de uma representação textual versionável. `schema_to_yaml` transforma nomes, tipos, nulabilidade e comentários disponíveis em dicionário ou texto seguro; estatísticas básicas podem ser incluídas opcionalmente. O resultado é uma fotografia técnica, não um catálogo de dados nem um contrato automaticamente governado.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um script PySpark que serializa o schema de uma tabela/view para dicionário e YAML/JSON. |
| Para que serve? | Produzir uma representação revisável e serializável da estrutura observada. |
| Use quando... | Precisar comparar, versionar ou revisar schema fora da visualização interativa. |
| Evite quando... | Esperar documentação semântica, monitoramento automático de schema ou garantia de compatibilidade. |
| Precisa de... | Objeto legível por Spark; PyYAML é opcional. |
| Entrega... | Dicionário Python ou string YAML; sem PyYAML, JSON válido em YAML 1.2. |

Consulte a [implementação](schema_to_yaml.py), a [fachada](__init__.py) e o [notebook de exemplo](exemplo_schema_to_yaml.py). O exemplo cria/substitui a view temporária `vw_exemplo_schema`; o helper não grava arquivo.

## 1. O que é?

`schema_to_dict` lê `df.schema.fields` e cria uma estrutura serializável com nome, `simpleString()` do tipo e `nullable`. Quando disponível no metadata Spark e solicitado, inclui `comment`.

`schema_to_yaml` usa essa estrutura e tenta serializá-la com `yaml.safe_dump`. Se PyYAML não estiver instalado, devolve JSON indentado. Isso é deliberado: JSON é subconjunto oficial de YAML 1.2, então um consumidor compatível com YAML 1.2 pode ler os dois.

## 2. Que problema este recurso resolve?

Ele responde: “Como registrar de forma legível e comparável a estrutura que o Spark vê agora?”. Isso reduz cópia manual de nomes/tipos e ajuda code review, documentação técnica ou comparação entre snapshots.

O script não responde “o que cada coluna significa?”, “quem é o dono?” ou “esta mudança é breaking?”. Essas perguntas pertencem à governança e à análise de compatibilidade.

## 3. Quando faz sentido usar?

Use para produzir snapshot de schema antes/depois de uma mudança, anexar uma estrutura técnica a uma revisão ou alimentar outra ferramenta que aceite dicionário/YAML.

Sem `include_stats`, o foco é metadata/schema. Com `include_stats=True`, o recurso acrescenta contagens que podem ajudar uma revisão manual, desde que o custo de varrer a tabela seja aceitável.

## 4. Quando não usar?

Não use o YAML gerado como substituto do catálogo governado. Um arquivo pode envelhecer assim que a tabela muda, enquanto o Unity Catalog continua sendo a fonte operacional do objeto.

Não ligue `include_stats=True` por padrão em tabela muito grande apenas para “deixar o schema mais completo”. O parâmetro muda o custo: passa de inspeção de estrutura para agregação sobre os dados.

## 5. Como funciona, intuitivamente?

Primeiro o Spark resolve `table_name`. Sem estatísticas, a função percorre os campos do schema e monta a lista de colunas.

Com estatísticas, cria uma única agregação larga: conta linhas e, para cada coluna, calcula `approx_count_distinct` e quantidade de `NULL`. Depois combina essas métricas com a descrição de cada campo e calcula `null_pct`.

A serialização é etapa separada. PyYAML presente produz YAML com unicode e ordem preservada; ausente produz JSON com os mesmos dados lógicos.

## 6. Exemplo de situação

O [notebook](exemplo_schema_to_yaml.py) cria uma view tabular sintética e primeiro imprime `schema_to_dict`. Em seguida, gera texto e mostra o mesmo conteúdo em YAML quando PyYAML está presente.

Por fim ativa estatísticas e inspeciona uma coluna com cardinalidade aproximada e nulos. O cenário evidencia a diferença entre “descrever estrutura” e “varrer dados para enriquecer a fotografia”.

## 7. O que você precisa antes de usar?

`table_name` deve ser resolvível e legível por `spark.table`. Não há parâmetro de seleção de colunas: todas entram no payload.

`include_comments=True` inclui comentários somente quando a informação aparece em `field.metadata["comment"]`. Ausência no retorno não prova que nenhuma documentação exista em outra camada de governança.

`include_stats=True` requer que as expressões Spark sejam válidas para os tipos presentes. A agregação cresce com duas expressões por coluna, além da contagem total; tabelas muito largas merecem avaliação de custo.

PyYAML não é dependência obrigatória. Consumidores que exigem **estilo textual YAML específico**, em vez de dados YAML 1.2, devem tratar a diferença de formatação explicitamente.

## 8. O que este recurso entrega?

`schema_to_dict` retorna:

| Campo | Significado |
|---|---|
| `table` | Nome consultado. |
| `columns` | Lista de campos com `name`, `type`, `nullable` e comentário opcional. |
| `row_count` | Somente com `include_stats=True`. |
| `columns[].stats.approx_distinct` | Estimativa de cardinalidade. |
| `columns[].stats.null_count` | Quantidade de `NULL`. |
| `columns[].stats.null_pct` | Percentual de nulos de 0 a 100; zero em tabela vazia por convenção. |

`schema_to_yaml` retorna string. A cardinalidade é aproximada; não use `approx_distinct` para certificar unicidade.

`type` usa `DataType.simpleString()`: estruturas aninhadas podem aparecer de forma compacta, adequada a snapshot técnico, mas não equivalem a um contrato expandido de todos os subcampos.

## 9. Como usar este recurso no Hub?

```python
from hub_scripts.schema_to_yaml import schema_to_dict, schema_to_yaml

payload = schema_to_dict("catalogo.schema.tabela")
texto = schema_to_yaml("catalogo.schema.tabela", include_comments=True)
```

Para estatísticas, ative conscientemente:

```python
payload_com_stats = schema_to_dict(
    "catalogo.schema.tabela",
    include_stats=True,
)
```

Abra o [exemplo](exemplo_schema_to_yaml.py) para comparar dicionário, YAML e fallback. O helper devolve valores; salvar arquivo é responsabilidade do consumidor.

## 10. Decisões e configurações que mais importam

`include_comments` controla somente o campo de comentário disponível no metadata lido pelo Spark. `include_stats` é a decisão de maior impacto de custo.

`approx_count_distinct` usa o estimador padrão do Spark; a documentação da API registra erro relativo padrão e recomenda `count_distinct` quando se precisa de contagem exata. Este helper não expõe `rsd` para ajustar a aproximação.

A presença de PyYAML muda a representação textual, não o conteúdo lógico pretendido. Se diffs de arquivo forem usados em automação, normalize o formato antes de comparar execuções feitas em ambientes diferentes.

## 11. Limitações, riscos e armadilhas

Um snapshot pode ficar desatualizado. A função não registra timestamp, versão da tabela, commit ou lineage automaticamente.

Comentários dependem do que chega ao metadata do campo. Ownership, tags, descrições de tabela, constraints e permissões não são exportados.

`include_stats=True` faz leitura de dados e `collect()` de uma linha agregada no driver. Em schema muito largo, o plano/resultado também cresce. A cardinalidade aproximada pode diferir entre execuções e não deve ser tratada como contagem exata.

JSON ser válido em YAML 1.2 não significa que todo software rotulado “YAML” aceite igualmente todas as versões/configurações. Valide o consumidor real quando o texto atravessar outra ferramenta.

## 12. Quais são as alternativas?

Para inspecionar uma tabela de maneira exploratória, use [quick_profile](../quick_profile/README.md). Para convenções de nomes, use [naming_checker](../naming_checker/README.md). Para contrato governado, mantenha metadata e documentação no mecanismo institucional apropriado do Unity Catalog/processo de dados.

Para detectar schema drift automaticamente, use monitoramento/versionamento que compare snapshots e emita alertas; este script só produz a fotografia.

## 13. Como saber se o resultado faz sentido?

Compare `columns` com `spark.table(nome).schema`. Verifique tipos complexos e nulabilidade. Se comentários forem esperados e não aparecerem, investigue onde eles estão armazenados antes de concluir que foram perdidos.

Com estatísticas, confira `row_count` com `count()` em uma tabela pequena e `null_count` de uma coluna com agregação independente. Trate `approx_distinct` como estimativa.

Serialização deve poder ser lida de volta por um parser YAML 1.2 compatível; caracteres com acento, aspas e dois-pontos são bons casos de teste.

## 14. Arquivos relacionados e próximos passos

A [implementação](schema_to_yaml.py) define payload e fallback; a [fachada](__init__.py) expõe `schema_to_dict` e `schema_to_yaml`; o [exemplo](exemplo_schema_to_yaml.py) demonstra custo opcional e serialização. O [catálogo de scripts](../README.md) posiciona a ferramenta em governança técnica.

Depois de gerar o snapshot, escolha explicitamente onde versioná-lo e quem revisa mudanças. Nenhuma publicação acontece pelo helper.

## 15. Referências

O contrato local foi revisado na implementação e no notebook durante a R04-B em 12/09/2026. A documentação Apache Spark de [`approx_count_distinct`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.approx_count_distinct.html) sustenta o caráter aproximado da cardinalidade.

A especificação [YAML 1.2](https://yaml.org/spec/1.2.1/) registra JSON como subconjunto oficial, base do fallback implementado. Fontes consultadas em 12/09/2026.

A validação de runtime da R04-B é registrada após execução. Revisão do próprio autor não é auditoria independente nem publicação/homologação Databricks.