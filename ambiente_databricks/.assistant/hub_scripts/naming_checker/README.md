# `naming_checker` — conferir convenções sem chamar política local de regra do Databricks

<!-- readme-objeto: 1.0.0 -->

Convenções de nomes ajudam pessoas a reconhecer objetos e reduzir ambiguidade, mas precisam ter origem clara. `naming_checker` aponta diferenças em relação a três tipos de regra — contexto recomendado pela plataforma, convenção do projeto e política opcional da organização — sem apresentar `snake_case`, `dim_` ou `fato_` como exigência universal do Unity Catalog.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um script PySpark que lê o schema de uma tabela/view e devolve avisos de nomenclatura. |
| Para que serve? | Tornar explícitas diferenças entre nomes existentes e convenções declaradas. |
| Use quando... | A equipe já tem uma convenção e quer revisar objetos antes de compartilhar/promover. |
| Evite quando... | Esperar um gate normativo da plataforma, renomeação automática ou validação semântica do schema. |
| Precisa de... | Nome legível por Spark e, se exigir prefixo, uma lista explícita de prefixos aceitos. |
| Entrega... | Lista de violações, todas com `severity="warning"` e campo `policy`. |

Consulte a [implementação](naming_checker.py), a [fachada](__init__.py) e o [exemplo](exemplo_naming_checker.py). O exemplo cria/substitui uma view temporária deliberadamente irregular.

## 1. O que é?

O script é um verificador de convenções, não um validador de legalidade de identificadores. Ele abre o objeto com `spark.table`, lê seus nomes de coluna e produz mensagens quando detecta quatro situações: nome da tabela sem três partes; prefixo organizacional ausente quando a checagem foi ativada; coluna fora da regex minúscula `snake_case`; ou coluna acima do limite configurado.

Cada aviso registra a origem da regra em `policy`, justamente para que recomendação da plataforma e preferência local não sejam misturadas.

## 2. Que problema este recurso resolve?

Ele responde: “Quais nomes deste objeto divergem da convenção que decidimos usar, e de onde vem cada regra?”. Isso ajuda revisões de schema e conversas de governança, especialmente quando regras costumeiras passam a circular sem documentação.

A lista não decide se a divergência deve ser corrigida. Um nome legado, integração externa ou contrato publicado pode justificar manter uma exceção.

## 3. Quando faz sentido usar?

Use antes de publicar ou compartilhar uma tabela, durante revisão de um schema novo ou ao inventariar dívida de nomenclatura. É adequado quando o objetivo é produzir **avisos explicáveis**, não alterar objetos.

O check de prefixo faz sentido somente quando a organização realmente adotou uma lista. Nesse caso, forneça `allowed_table_prefixes` explicitamente.

## 4. Quando não usar?

Não use como prova de que um objeto é inválido no Unity Catalog. A regex de colunas e o limite de tamanho são convenções do projeto; o Unity Catalog suporta identificadores além desse subconjunto.

Não use para renomear automaticamente objetos em produção. Renomear coluna/tabela pode quebrar consumidores e exige análise de dependências, contratos e compatibilidade.

## 5. Como funciona, intuitivamente?

A função valida apenas os parâmetros locais, resolve uma sessão Spark e abre `table_name`. Se o texto do nome não possui exatamente três segmentos separados por `.`, adiciona um aviso de contexto recomendado.

Quando `enforce_prefix=True`, compara o último segmento do nome da tabela com os prefixos informados. Depois percorre `df.columns`: aplica a regex `[a-z][a-z0-9_]*` e mede o comprimento de cada nome.

Nenhuma linha da tabela é agregada ou coletada; o objetivo é trabalhar com nomes/schema, embora abrir o objeto ainda exija resolução e permissão adequadas no catálogo/sessão.

## 6. Exemplo de situação

O [notebook de exemplo](exemplo_naming_checker.py) cria uma view com `ValorTotal`, `dataDeReferencia` e uma coluna longa. O script devolve avisos `project-custom` para camelCase/maiúsculas e para o limite de comprimento.

A própria view também gera `databricks-recommended-context` porque seu nome é de sessão e não tem `catalog.schema.table`. O exemplo mostra por que isso é aviso, não erro: uma view temporária legítima não tem nome de três partes.

## 7. O que você precisa antes de usar?

Forneça `allowed_table_prefixes` como sequência de strings **não vazias**. O código não rejeita o prefixo `""`, que casa com qualquer nome e faz o check de prefixo passar; isso é uma limitação, não configuração recomendada.

`table_name` precisa ser resolvível por `spark.table`. `max_col_length` deve ser positivo. Se `enforce_prefix=True`, `allowed_table_prefixes` não pode ficar vazio.

A função não valida a política fornecida além disso. Prefixos sobrepostos, vazios ou semanticamente inadequados são responsabilidade do consumidor.

A convenção de coluna aceita somente ASCII minúsculo começando por letra, seguido de letras, números ou `_`. Nomes com acento, maiúscula, espaço, hífen ou `_` inicial recebem aviso de projeto, ainda que possam existir na plataforma.

## 8. O que este recurso entrega?

O retorno é uma lista de dicionários. Cada violação contém:

| Campo | Significado |
|---|---|
| `object` | Nome da tabela ou coluna observada. |
| `severity` | Sempre `warning` nesta implementação. |
| `message` | Descrição humana da divergência. |
| `policy` | Origem da regra: `databricks-recommended-context`, `project-custom` ou `organization-custom`. |

Lista vazia significa apenas que nenhuma das regras implementadas encontrou divergência. Não certifica significado, tipos, comentários, ownership ou contratos.

## 9. Como usar este recurso no Hub?

Antes do import, confira a [preparação comum](../README.md#preparacao-comum): raiz `.assistant` no `sys.path`, Python e, para este helper, PySpark/Spark e acesso ao recurso.

Exemplo ilustrativo de violação: `{"object": "NomeLegado", "severity": "warning", "message": "Column is outside the configured lowercase snake_case convention.", "policy": "project-custom"}`.

```python
from hub_scripts.naming_checker import naming_checker

violacoes = naming_checker(
    "catalogo.crm.dim_cliente",
    enforce_prefix=True,
    allowed_table_prefixes=("dim_", "fato_"),
    max_col_length=80,
)
```

Abra o [exemplo](exemplo_naming_checker.py) para ver a separação entre origem das políticas e a recusa de `enforce_prefix=True` sem uma lista explícita.

## 10. Decisões e configurações que mais importam

`enforce_prefix=False` é o default. Ativar a regra muda o contrato porque introduz política organizacional; a função deliberadamente não embute `dim_`, `fato_` ou qualquer lista “padrão”.

`max_col_length=255` é convenção configurável do projeto. Reduzir esse valor pode gerar novos avisos sem que o schema tenha mudado.

A recomendação de nome completo se baseia na clareza de contexto do namespace. A documentação Databricks recomenda identificadores totalmente qualificados quando workloads interagem com objetos em múltiplos schemas/catálogos; isso não significa que todo nome parcialmente qualificado seja inválido.

## 11. Limitações, riscos e armadilhas

Erro de acesso/resolução da tabela interrompe a função; violação de convenção devolve uma lista. `max_col_length<=0` e `enforce_prefix=True` sem lista causam `ValueError`, não warnings. Uma exceção governada pode manter coluna legada por compatibilidade, desde que dono, justificativa e consumidores sejam registrados; não há renomeação automática.

A função não valida nome de catálogo/schema nem aplica regex ao nome curto da tabela; o prefixo é a única convenção de tabela além da checagem de três segmentos.

Dividir `table_name` por ponto é uma aproximação textual: identificadores escapados/complexos não são analisados por um parser SQL. O objeto precisa ser resolvido pelo próprio `spark.table`.

Todos os resultados são warning. Transformá-los em bloqueio de CI é uma decisão externa e deve prever exceções e ownership da política.

## 12. Quais são as alternativas?

Para verificar estrutura e conteúdo, use ferramentas de schema/qualidade, como [schema_to_yaml](../schema_to_yaml/README.md) ou [data_quality_check](../data_quality_check/README.md). Elas respondem perguntas diferentes.

Para governança formal, registre convenções em documentação organizacional e aplique controles no processo de criação/revisão. Um linter local é mais transparente quando a regra ainda está em discussão.

## 13. Como saber se o resultado faz sentido?

Crie uma view pequena com uma coluna `nome_ok`, outra `NomeRuim` e limite curto. Confira se somente as divergências esperadas aparecem.

Ative prefixo com uma lista que contenha o nome curto e confirme que não aparece `organization-custom`; troque para uma lista incompatível e confirme o aviso.

Leia sempre `policy` junto com `message`. Se uma regra não tem dono claro, o problema é de governança, não de regex.

## 14. Arquivos relacionados e próximos passos

A [implementação](naming_checker.py) define as convenções; a [fachada](__init__.py) expõe a função; o [exemplo](exemplo_naming_checker.py) demonstra avisos e política explícita. O [catálogo de Hub Scripts](../README.md) oferece os demais utilitários.

Depois da revisão, documente exceções e dependências antes de qualquer renomeação. O script não possui etapa automática de correção.

## 15. Referências

Contrato: [implementação](naming_checker.py), [fachada](__init__.py) e [exemplo](exemplo_naming_checker.py). A referência Databricks de [consulta a tabelas](https://docs.databricks.com/aws/en/query), consultada em 12/09/2026, contextualiza nomes qualificados. `snake_case`, comprimento e prefixos são política local, não regra universal do Unity Catalog.
