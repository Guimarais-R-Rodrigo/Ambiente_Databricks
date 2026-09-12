# `join_diagnostics` — medir cobertura e expansão antes de juntar

<!-- readme-objeto: 1.0.0 -->

Uma junção pode duplicar, descartar ou deixar linhas sem correspondência sem produzir erro de execução. Este helper mede esses efeitos sobre dois DataFrames Spark antes de o join de negócio ser materializado.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Diagnóstico pré-join de cobertura, chaves nulas, multiplicidade e expansão prevista. |
| Para que serve? | Descobrir se um join tende a preservar, inflar ou descartar linhas da esquerda. |
| Use quando... | A unidade da tabela da esquerda importa e a cardinalidade da direita precisa ser conhecida. |
| Evite quando... | Você quer executar o join ou decidir automaticamente qual tipo de join é correto. |
| Precisa de... | Dois DataFrames Spark e a chave completa, simples ou composta. |
| Entrega... | Dicionário de contagens, expansão, relação e pequenas amostras de chaves problemáticas. |

Leia a [implementação](join_diagnostics.py), a [fachada](__init__.py) e o [notebook](exemplo_join_diagnostics.py). O helper não escreve tabela, mas dispara várias ações Spark e pode movimentar dados para agregações e joins de diagnóstico.

## 1. O que é?

`diagnosticar_join` é um helper customizado para responder “o que aconteceria com a cardinalidade da esquerda?”. **Cardinalidade**, aqui, é a quantidade de linhas e a relação entre ocorrências de uma mesma chave nos dois lados.

Ele separa chaves nulas, mede correspondência entre linhas válidas da esquerda e chaves da direita, calcula multiplicidade do lado direito apenas para chaves que existem à esquerda e estima os tamanhos de um `left join` e de um `inner join`.

Não é otimizador do Spark, não escolhe estratégia física de join e não materializa as colunas do join real.

## 2. Que problema este recurso resolve?

A pergunta prática é: “Se eu cruzar estas duas bases pela chave informada, vou duplicar ou perder a unidade de análise?”. Isso é especialmente importante antes de construir uma base de treino, um painel ou uma tabela de fatos.

O helper torna visíveis três causas distintas: chave nula, chave válida sem correspondência e multiplicidade maior que um do lado direito. Essas causas pedem correções diferentes.

## 3. Quando faz sentido usar?

Use antes de joins em que o número de linhas da esquerda precisa permanecer interpretável: cliente × cadastro, evento × dimensão, operação × atributos ou fato × conjunto de features.

É útil para validar uma chave composta e para entender se a direita é única por chave. Também ajuda a estimar a diferença entre preservar órfãs (`left`) e descartá-las (`inner`) antes de tomar a decisão de negócio.

## 4. Quando não usar?

Não use como substituto do join; o retorno é um dicionário de diagnóstico, não uma tabela combinada. Também não use passando somente parte de uma chave composta: os números podem ser calculados e ainda assim descrever uma relação diferente da pretendida.

Contraexemplo: contratos são a unidade desejada, mas a esquerda está no grão cliente. Um fator de expansão 2,0 pode ser correto para converter o grão para contrato; “expansão” não significa automaticamente “erro”. O helper informa o efeito, não a intenção do projeto.

## 5. Como funciona, intuitivamente?

A função conta linhas e chaves nulas em cada lado. Depois remove linhas com qualquer componente nulo da chave e reduz a direita às chaves que aparecem na esquerda. Nessa população relevante, conta quantas linhas da direita existem por chave.

Cada linha válida da esquerda que encontra uma chave recebe essa multiplicidade. Somando as multiplicidades, a função estima quantas linhas o join produziria. Linhas sem match e chaves nulas entram no tamanho previsto do `left`, mas não no `inner`.

A cobertura usa **linhas válidas da esquerda** como denominador, não todas as linhas e não chaves distintas.

## 6. Exemplo de situação

Uma base sintética tem 500 clientes e um cadastro com uma linha por cliente. O diagnóstico prevê expansão `1,0`. Se o lado direito passar a ter dois contratos por cliente, a expansão prevista sobe para `2,0`.

Se metade das chaves válidas não estiver no cadastro, `cobertura_pct_chaves_validas` fica em 50%. Chaves nulas são reportadas à parte e não reduzem esse percentual, justamente para não misturar ausência de identificador com falta de correspondência.

## 7. O que você precisa antes de usar?

`esquerda` e `direita` devem ser DataFrames PySpark. `chave` pode ser uma string ou uma sequência não vazia e precisa existir nos dois lados. `amostra_orfas` deve ser inteiro não negativo; o código valida apenas o sinal, não o tipo formalmente.

Confirme o **grão** de cada lado: o que uma linha representa. O código não sabe se multiplicidade 3 é esperada ou defeito. Para chave composta, forneça todos os componentes na mesma semântica e tipos compatíveis.

## 8. O que este recurso entrega?

O retorno é um dicionário. Os campos principais são:

| Campo | Como interpretar |
|---|---|
| `linhas_esquerda`, `linhas_direita` | contagens de linhas de cada entrada |
| `chaves_nulas_*` | linhas com ao menos um componente nulo da chave |
| `linhas_com_match` | linhas válidas da esquerda que encontram chave na direita |
| `linhas_sem_match_chave_valida` | linhas válidas da esquerda sem correspondência |
| `cobertura_pct_chaves_validas` | match / linhas válidas da esquerda, em % |
| `multiplicidade_max_direita` | maior número de linhas da direita por chave relevante |
| `multiplicidade_media_direita` | média de multiplicidade ponderada pelas linhas casadas da esquerda |
| `linhas_apos_join_left` / `inner` | tamanho previsto por tipo de join |
| `expansao_prevista_left` / `inner` | tamanho previsto / linhas originais da esquerda |
| `relacao` | resumo textual da expansão entre linhas casadas |
| `exemplos_sem_match` | pequenas chaves órfãs ordenadas |
| `exemplos_chave_nula` | pequena amostra de chaves nulas |

`relacao` não é uma inferência completa de modelo entidade-relacionamento. O texto “1:1 ou N:1” apenas diz que, nas linhas casadas, cada linha da esquerda produz uma linha.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.spark.join_diagnostics import diagnosticar_join

diag = diagnosticar_join(fatos, cadastro, ["id_cliente", "safra"])
print(diag["expansao_prevista_left"])
print(diag["cobertura_pct_chaves_validas"])
```

O [notebook](exemplo_join_diagnostics.py) mostra preservação, expansão, falta de match e chave nula com dados sintéticos. Não há escrita persistente.

## 10. Decisões e configurações que mais importam

A escolha central é `chave`: ela define a relação que está sendo diagnosticada. `amostra_orfas=5` controla somente quantos exemplos serão coletados para o processo Python; usar `0` evita essa coleta de exemplos.

Compare `expansao_prevista_left` e `expansao_prevista_inner`. O primeiro inclui órfãs e chaves nulas como linhas preservadas; o segundo considera apenas correspondências.

O helper restringe a multiplicidade às chaves presentes na esquerda. Duplicidades de chaves que existem **somente** na direita não afetam a estimativa, porque não participariam daquele join.

## 11. Limitações, riscos e armadilhas

O diagnóstico executa contagens, agregações, `left_semi`, `inner`, `left_anti` e pequenas coletas. O custo depende de volume, distribuição das chaves, partições e plano; não assuma tempo fixo.

A amostra de chaves nulas não é ordenada, portanto sua composição pode variar. As chaves órfãs são ordenadas antes do limite. Tipos incompatíveis, skew e transformações complexas na linhagem podem produzir custo ou erro apenas na execução Spark.

Em esquerda vazia, as expansões retornam `1.0` por convenção do código; isso não significa uma relação saudável. Leia junto com `linhas_esquerda`.

## 12. Quais são as alternativas?

Para conferir uma tabela nomeada, chave primária candidata, nulidade e recência, [`data_quality_check`](../../../hub_scripts/data_quality_check/data_quality_check.py) responde outra pergunta. Para disponibilidade temporal, [`pit_join`](../pit_join/README.md) escolhe a versão histórica elegível.

Contagens manuais com `groupBy` e `left_anti` são adequadas quando você precisa de um diagnóstico específico que não cabe no contrato desta função.

## 13. Como saber se o resultado faz sentido?

Construa casos pequenos conhecidos: uma direita única, uma duplicada, uma chave ausente e uma nula. Confira se `linhas_apos_join_left` coincide com o `left join` real em uma amostra sintética e se `linhas_apos_join_inner` coincide com o `inner`.

Verifique a identidade `linhas_com_match + linhas_sem_match_chave_valida + chaves_nulas_esquerda == linhas_esquerda`. Para uma direita única nas chaves relevantes, a multiplicidade máxima deve ser 1.

## 14. Arquivos relacionados e próximos passos

- [Implementação](join_diagnostics.py): cálculo das métricas e amostras.
- [Fachada](__init__.py): exporta `diagnosticar_join`.
- [Notebook](exemplo_join_diagnostics.py): quatro cenários sintéticos.
- [`pit_join`](../pit_join/README.md): join com elegibilidade temporal.
- [`data_quality_check`](../../../hub_scripts/data_quality_check/data_quality_check.py): qualidade de tabela nomeada, não efeito de join.
- [Coleção](../../README.md): demais operações Spark do Hub.

## 15. Referências

A descrição foi confrontada com `join_diagnostics.py`, `__init__.py` e o notebook desta pasta. Relação, cobertura e expansão são definições do helper local, não conceitos universais com esses nomes exatos.

A R04-A registra testes sintéticos com Spark separadamente do gate estrutural. Não há benchmark de escala, publicação Databricks ou auditoria independente nesta entrega.
