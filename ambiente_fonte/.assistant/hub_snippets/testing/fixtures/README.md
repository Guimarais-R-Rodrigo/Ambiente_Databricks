# `fixtures` — dados sintéticos com propósito de teste

<!-- readme-objeto: 1.0.0 -->

> Uma fixture é uma entrada preparada para exercitar um comportamento. Estes geradores criam pequenos DataFrames Spark fictícios; não estimam a realidade da carteira.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Quatro geradores de bases fictícias. |
| Para que serve? | Demonstrar contratos, casos conhecidos e testes. |
| Use quando... | Você precisa de dados controlados para aprender ou conferir um helper. |
| Evite quando... | A finalidade é provar desempenho de um modelo ou representar clientes reais. |
| Precisa de... | PySpark e sessão Spark compatível; dimensões pequenas. |
| Entrega... | DataFrames em memória, ou par de DataFrames; sem gravação de tabela. |

**Acesso direto:** [exemplo](exemplo_fixtures.py) · [implementação](fixtures.py) · [API pública](__init__.py) · [coleção](../../README.md).

## 1. O que é?

Uma **fixture** é uma preparação de teste: dados com características conhecidas para observar se um recurso responde como esperado. Por exemplo, uma base pode incluir identificadores repetidos intencionalmente para testar um diagnóstico de duplicatas.

[Este módulo](fixtures.py) gera quatro famílias de dados sintéticos. Usa números pseudoaleatórios — produzidos por um gerador com regra definida — e uma **semente** (`seed`) para repetir sorteios sob as mesmas condições. Não é uma amostra da carteira nem um modelo gerador calibrado com clientes.

## 2. Que problema este recurso resolve?

“Como demonstrar um helper sem depender de uma tabela real, e como distinguir erro de mudança dos dados de exemplo?” As fixtures dão uma entrada reproduzível e com casos planejados.

Isso permite verificar contratos e algumas propriedades. Passar nesses casos não prova que o recurso esteja correto para toda entrada, nem que um modelo tenha utilidade de negócio.

## 3. Quando faz sentido usar?

Use `base_tabular` para exercitar qualidade, tipos e chaves; `serie_temporal` para operações por entidade e mês; `fatos_e_features` para uma junção temporal com versões elegíveis e futuras; e `safras` para painéis de contratos por idade.

Cada família foi desenhada para um problema específico. Uma chave duplicada proposital ajuda um teste de join, mas não deve ser esquecida quando o mesmo dado é reutilizado para outro objetivo.

## 4. Quando não usar?

Não use a base para estimar risco, resposta comercial ou qualidade preditiva. Em `base_tabular`, o alvo é sorteado; as rendas e os estados não foram calibrados para produzir uma relação de negócio.

Também não aumente `n` para milhões supondo geração distribuída: o Python monta uma lista local antes de criar o DataFrame Spark. O retorno ser Spark não torna a etapa de geração distribuída.

## 5. Como funciona, intuitivamente?

Cada chamada cria uma instância de `random.Random(seed)`, monta linhas em uma lista e chama `createDataFrame` com esquema declarado. O gerador não precisa mudar a semente global do Python.

Em `fatos_e_features`, cada decisão recebe cliente próprio, duas versões anteriores e, por sorteio, uma versão futura. A coluna `eh_futura` é um gabarito de teste, não um preditor real. Em `safras`, quando um contrato vira inadimplente ele permanece nesse estado: a proporção resultante é acumulada, não a taxa de novos casos do mês.

## 6. Exemplo de situação

Para demonstrar duplicidade, prepare 20 linhas com `n_entidades=5`. Os identificadores são construídos de modo que os cinco clientes fictícios se repitam. A pergunta é: “O diagnóstico encontra mais linhas que entidades?”

Para demonstrar uma junção temporal, gere fatos e atributos com versões futuras e confira se o resultado exclui as versões marcadas. Não conclua que toda forma de vazamento foi eliminada: esse cenário não cobre, por exemplo, todas as possibilidades de atraso ou revisão histórica de uma fonte real.

## 7. O que você precisa antes de usar?

O módulo importa PySpark no topo. É necessária uma sessão Spark compatível: `_sessao()` procura uma sessão ativa e, se não encontrar, tenta criar uma. Essa tentativa pode exigir configuração no ambiente local. No Databricks, confirme o ambiente existente; não instale PySpark indiscriminadamente no runtime gerenciado.

Use inteiros positivos para dimensões, probabilidades nos intervalos aceitos e tamanhos pequenos. Em `base_tabular`, `pct_nulos_renda` pertence a `[0, 1)` e `prevalencia_alvo` a `(0, 1)`. Nem todos os argumentos têm validação equivalente: `n_entidades=0` cai no padrão `n`, porque a implementação usa `n_entidades or n`. Prefira `None` para o padrão e não interprete zero como teste recusado.

O notebook consulta o usuário via Spark, exibe amostras limitadas e coleta alguns resumos; não lê ou sobrescreve tabelas persistentes.

## 8. O que este recurso entrega?

Os retornos possuem estes grãos — o que uma linha representa — e campos:

| Gerador | Unidade e saída |
|---|---|
| `base_tabular` | Registro fictício com `id_cliente`, `uf`, `renda`, `dt_referencia`, `alvo`. A chave pode repetir. |
| `serie_temporal` | Entidade × mês, com `id_entidade`, `dt_referencia`, `valor`. |
| `fatos_e_features` | Par `(fatos, features)`: decisão por cliente e versões de `score_bureau`, com `dt_referencia` e `eh_futura`. |
| `safras` | Contrato × MOB, com `id_contrato`, `safra`, `mob`, `inadimplente`. MOB é a idade em meses no painel. |

`serie_temporal` inicia em janeiro de 2025; as datas dos demais geradores também partem de referências fixas. Não são datas automaticamente atualizadas. `safras` produz `n_contratos * mob_maximo` linhas, sem censura por data corrente.

## 9. Como usar este recurso no Hub?

Comece pelo [exemplo de fixtures](exemplo_fixtures.py), após preparar o pacote conforme a [coleção](../../README.md). Para uma sessão Spark já disponível:

```python
from hub_snippets.testing.fixtures import base_tabular
clientes = base_tabular(n=20, n_entidades=5, seed=42)
print(clientes.count(), clientes.select("id_cliente").distinct().count())
```

O caso tem 20 linhas e cinco identificadores distintos pela construção do gerador. As contagens são ações Spark. O trecho não persiste uma tabela; execução local com Spark, quando registrada nas evidências, não equivale a homologação no Databricks.

## 10. Decisões e configurações que mais importam

Mantenha `seed`, parâmetros e versões registrados ao comparar execuções. A semente fixa não transforma probabilidades em quotas exatas: 4% de probabilidade de nulo pode produzir outra fração observada numa base pequena.

`pct_feature_futura=0.2` é a chance de acrescentar uma versão futura **por decisão**, não 20% de todas as linhas de atributos. Cada decisão já possui duas versões anteriores. `atraso_real_dias` desloca essas datas anteriores; não gera uma coluna separada de publicação. Use valor não negativo no cenário previsto, pois ele não é validado e valores negativos podem violar a intenção do teste.

Em `serie_temporal`, `tendencia` altera o termo esperado por período, mas o ruído pode fazer um valor mensal cair. Em `safras`, o crescimento é construção do gerador; não é estimativa de probabilidade real.

## 11. Limitações, riscos e armadilhas

Há validações incompletas: `fatos_e_features` não recusa explicitamente quantidades não positivas de decisões, e strings de safra não são validadas como datas. Testes de entrada precisam distinguir comportamento observado de requisito recomendado.

As listas são construídas na memória do processo Python. Não existe limite de memória garantido pelo helper. As condições de reprodutibilidade abrangem também versão do Python, argumentos e ordem de consumo dos números; a documentação de [random](https://docs.python.org/3/library/random.html#notes-on-reproducibility) delimita garantias entre versões. Ordene por chaves antes de comparar DataFrames; não dependa da ordem incidental de uma coleta.

O indicador `eh_futura` vale para o desenho com cliente exclusivo por decisão. Reutilizar o mesmo cliente em decisões distintas exige outro critério temporal. O painel de safras não simula recuperação nem observações censuradas.

## 12. Quais são as alternativas?

Para um caso de borda específico, uma pequena tabela criada explicitamente pode ser melhor que um gerador probabilístico. Para desenho amostral de dados reais autorizados, examine [smart_sample](../../spark/smart_sample/smart_sample.py): amostragem real é outra tarefa e exige cuidados de acesso e representatividade.

Uma simulação de carteira para estimar risco precisaria de premissas e validação próprias; não é uma extensão presumida destas fixtures.

## 13. Como saber se o resultado faz sentido?

Confira contagem de linhas, grão, chaves, tipos e propriedades que motivaram o teste. No caso de 20 linhas/cinco entidades, confirme ambas as contagens. Para séries, ordene por entidade/data; para safras, confira que `inadimplente` não regride dentro do contrato. Para o par temporal, confira os dois candidatos anteriores, o marcador futuro e a seleção da versão elegível mais recente.

Repita com os mesmos parâmetros e compare linhas ordenadas; teste também outra semente. Se surgir diferença, investigue parâmetros e versões antes de atribuí-la ao helper consumidor. Uma fixture que gera não substitui assertions — verificações explícitas — sobre o comportamento que você quer testar.

## 14. Arquivos relacionados e próximos passos

[fixtures.py](fixtures.py) contém os geradores; [__init__.py](__init__.py), a API pública; [exemplo_fixtures.py](exemplo_fixtures.py), a demonstração. O [README de pit_join](../../spark/pit_join/README.md) explica o caso temporal; a [coleção](../../README.md) e o [Manual](../../../MANUAL_TECNICO.md#catalogo-helpers) orientam a continuação.

## 15. Referências

A [implementação](fixtures.py) sustenta esquema, parâmetros e limites descritos. [Python — random](https://docs.python.org/3/library/random.html#notes-on-reproducibility) delimita reprodutibilidade. [Spark — createDataFrame](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.createDataFrame.html) explica a criação do DataFrame a partir das entradas aceitas. Fontes consultadas em 12/09/2026; “latest” não identifica a versão do runtime testado.

Revisão R03-A: leitura completa do módulo, fachada e notebook. Os testes da sprint distinguem geração em Spark real de inspeção estática; versões e resultados ficam nas evidências. Não foi executado o notebook no Databricks nem validada uma carteira real.
