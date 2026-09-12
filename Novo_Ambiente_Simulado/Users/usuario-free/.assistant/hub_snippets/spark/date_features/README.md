# `date_features` — transformar uma data em atributos de calendário explícitos

<!-- readme-objeto: 1.0.0 -->

Datas carregam informação de calendário que pode ser útil em análise e modelagem, mas nomes, convenções e feriados precisam ser explícitos para que treino e uso posterior façam a mesma transformação. Este helper acrescenta atributos de calendário a um DataFrame Spark sem alterar o número de linhas.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Transformador PySpark que deriva nove atributos de calendário de uma coluna de data. |
| Para que serve? | Padronizar dia da semana, fim de semana, mês, trimestre, ano e dois indicadores de feriado. |
| Use quando... | O instante da linha já está definido e esses atributos fazem sentido para a pergunta analítica. |
| Evite quando... | Você precisa de hora/fuso, dia útil bancário ou um calendário completo que ainda não foi definido. |
| Precisa de... | DataFrame Spark, nome da coluna de data e, se necessário, lista explícita de datas de feriado do projeto. |
| Entrega... | O DataFrame original acrescido de nove colunas, opcionalmente prefixadas. |

Leia a [implementação](date_features.py), a [fachada](__init__.py) e o [notebook](exemplo_date_features.py). O exemplo usa somente dados sintéticos e não persiste tabela.

## 1. O que é?

`date_features` é um pequeno transformador de calendário. Ele recebe uma coluna, a converte com `to_date` e deriva atributos como mês, trimestre e dia da semana ISO. “ISO” aqui significa segunda-feira igual a 1 e domingo igual a 7; o helper calcula essa convenção a partir de `dayofweek` do Spark.

A implementação desta pasta também contém **nove feriados nacionais brasileiros de data fixa** em `FIXED_NATIONAL_HOLIDAYS_BR`. Eles alimentam `is_feriado_nacional_fixo`. Isso não é um calendário nacional completo: feriados móveis, estaduais, municipais, bancários ou regras próprias do projeto precisam ser fornecidos separadamente em `holiday_dates`, que alimenta `is_feriado_calendario`.

A função pública principal é `extrair_features_data`; `add_date_features` é um alias da mesma função.

## 2. Que problema este recurso resolve?

A pergunta prática é: “Como transformar a data de referência em atributos consistentes sem cada notebook inventar nomes e calendários diferentes?”. O helper centraliza a transformação e torna a origem de cada indicador explícita.

Ele não decide se mês, dia da semana ou feriado melhoram um modelo. Também não transforma uma data em “dia útil”, “fechamento bancário” ou qualquer calendário operacional que não tenha sido codificado.

## 3. Quando faz sentido usar?

Use quando cada linha possui uma data conhecida no instante da análise e você quer testar efeitos de calendário: sazonalidade mensal, diferença entre semana e fim de semana, trimestre ou datas previamente classificadas como feriado.

Também faz sentido quando há mais de uma coluna de data e você precisa manter nomes distinguíveis. Nesse caso, use `prefixo`, por exemplo `prefixo="contrato"`, para gerar `contrato_mes`, `contrato_ano` e assim por diante.

A recomendação é adequada quando a data realmente representa o evento cuja sazonalidade se quer medir. Derivar `mes` de uma data de carga técnica para explicar comportamento do cliente pode produzir um atributo perfeitamente calculado e conceitualmente errado.

## 4. Quando não usar?

Não use esperando um calendário completo. O conjunto embutido cobre somente datas fixas nacionais; “é feriado?” pode depender de ano, localidade, categoria profissional, calendário de compensação ou regra interna.

Também não use para componentes intradiários. `to_date` descarta a parte de horário; se a pergunta depende de hora, minuto ou fuso, outro tratamento é necessário.

Contraexemplo: uma tabela tem `dt_processamento` e a pergunta é sobre a data em que o cliente tomou uma decisão. O helper roda sem erro sobre `dt_processamento`, mas produz sazonalidade do processamento, não do comportamento que se queria estudar.

## 5. Como funciona, intuitivamente?

Primeiro, `F.to_date` cria uma expressão de data a partir de `col_data`. Em seguida, o helper acrescenta:

- `dia_semana_iso`: 1 a 7, de segunda a domingo;
- `is_fim_semana`: verdadeiro para 6 e 7;
- `dia_mes`, `semana_ano`, `mes`, `trimestre` e `ano`;
- `is_feriado_nacional_fixo`: comparação de `MM-dd` com as nove datas fixas embutidas;
- `is_feriado_calendario`: comparação da data completa com `holiday_dates`.

Se houver `prefixo`, ele é anteposto aos nove nomes. As transformações são expressões Spark e permanecem lazy até uma ação posterior.

## 6. Exemplo de situação

Imagine uma base sintética de interações diárias. A equipe suspeita que a resposta muda no fim de semana e em determinados feriados do projeto. A coluna `dt_referencia` já representa a data da interação.

`extrair_features_data(base, "dt_referencia", holiday_dates=["2026-02-17"])` acrescenta atributos de calendário e marca a data explicitamente fornecida no indicador de calendário. O exemplo serve para estudar o recorte; não demonstra que feriado causa aumento ou queda de resposta.

## 7. O que você precisa antes de usar?

Você precisa de um DataFrame PySpark e de `col_data` presente em `df.columns`. A função verifica apenas a existência do nome; a qualidade da conversão para data continua sendo responsabilidade de quem usa. **Não há contrato de tolerância a texto malformado.** Com ANSI habilitado, `to_date` pode levantar `CAST_INVALID_INPUT`; com ANSI desabilitado, a mesma conversão pode produzir `NULL`. Se o fluxo precisa tolerar valores inválidos, normalize a coluna antes deste helper e use uma conversão tolerante (`try_cast` para `DATE`) de forma explícita.

`holiday_dates` recebe uma sequência de strings de datas. O código remove duplicidades com `set` e não valida previamente formato, calendário ou procedência. Use datas ISO (`AAAA-MM-DD`) e mantenha a fonte do calendário documentada.

Se as colunas de destino já existirem, `withColumn` as substitui silenciosamente. Por isso, confira os nomes ou use um `prefixo` que não colida com o schema existente.

## 8. O que este recurso entrega?

Retorna um DataFrame Spark com as colunas originais e nove colunas adicionais. Não retorna métricas, logs ou dicionário de diagnóstico.

`is_feriado_nacional_fixo` e `is_feriado_calendario` respondem perguntas diferentes. A primeira usa a lista local de datas fixas; a segunda usa somente as datas completas fornecidas em `holiday_dates`. Uma linha pode ser verdadeira em uma, em ambas ou em nenhuma.

Uma feature preenchida corretamente não prova utilidade preditiva, causalidade nem ausência de vazamento em outras variáveis.

## 9. Como usar este recurso no Hub?

A importação pública é:

```python
from hub_snippets.spark.date_features import extrair_features_data

saida = extrair_features_data(
    df,
    "dt_referencia",
    prefixo="evento",
    holiday_dates=["2026-02-17", "2026-04-03"],
)
```

O [notebook de exemplo](exemplo_date_features.py) usa fixtures sintéticas, exibe as nove colunas e discute a diferença entre feriado fixo e calendário de projeto. Ele não grava dados persistentes.

## 10. Decisões e configurações que mais importam

`col_data` define **qual relógio do negócio** será transformado; escolher a coluna errada é mais grave que escolher um nome ruim. `prefixo=None` mantém os nomes curtos, mas pode sobrescrever colunas existentes ou colidir quando várias datas são transformadas.

`holiday_dates=None` faz `is_feriado_calendario` ser sempre falso. Isso não desativa `is_feriado_nacional_fixo`, que continua usando `FIXED_NATIONAL_HOLIDAYS_BR`.

A lista fixa é parte do código e sua existência deve ser tratada como convenção local versionada, não como serviço oficial de calendário.

## 11. Limitações, riscos e armadilhas

O helper reduz timestamps a datas; horário e fuso não são preservados na transformação. Ele não verifica se `holiday_dates` está no formato esperado nem se o calendário é válido para todas as localidades da população.

Datas inválidas ou não conversíveis **não têm comportamento único garantido por este helper**: em modo ANSI podem interromper a ação com `CAST_INVALID_INPUT`; em configurações permissivas podem resultar em `NULL` e propagar nulos às features. Nomes de saída existentes podem ser sobrescritos. `weekofyear` segue a função do Spark e precisa ser interpretada com a convenção adotada pelo projeto, principalmente em viradas de ano.

A lista fixa pode ficar desatualizada se a legislação mudar. Por isso, o README não a apresenta como fonte normativa.

## 12. Quais são as alternativas?

Para uma transformação única e muito simples, usar diretamente `pyspark.sql.functions` pode ser mais transparente. Para calendário de negócio complexo, prepare uma dimensão de calendário governada e faça uma junção com os atributos necessários.

Se a questão é disponibilidade temporal de features históricas, use [`pit_join`](../pit_join/README.md); ele resolve uma pergunta diferente: qual informação estava disponível no momento da decisão.

## 13. Como saber se o resultado faz sentido?

Escolha datas conhecidas: uma segunda-feira, um domingo, 1º de janeiro e uma data presente somente em `holiday_dates`. Confira `dia_semana_iso`, `is_fim_semana` e os dois indicadores de feriado.

Antes de aplicar o helper em produção, valide uma amostra representativa da coluna como data e decida explicitamente a política para valores malformados. Se a política for tolerá-los, faça essa conversão antes do helper e conte os valores que viraram `NULL`; se a política for falhar, teste o erro esperado. Se usar `prefixo`, confirme que nenhuma coluna anterior foi sobrescrita. Para treino e scoring, compare também os nomes e a lógica de preparação nos dois fluxos.

## 14. Arquivos relacionados e próximos passos

- [Implementação](date_features.py): regras e lista fixa local.
- [Fachada](__init__.py): exporta `FIXED_NATIONAL_HOLIDAYS_BR`, `extrair_features_data` e `add_date_features`.
- [Notebook](exemplo_date_features.py): demonstração sintética e leitura didática.
- [Coleção Spark](../../README.md): catálogo local dos snippets.
- [`pit_join`](../pit_join/README.md): quando o problema é disponibilidade histórica, não calendário.

## 15. Referências

O comportamento descrito foi conferido em `date_features.py`, `__init__.py` e no notebook desta pasta, sobre a base integrada da R04-A. As funções de calendário são APIs PySpark; o contrato local, os nomes e a lista fixa são definidos pelo Hub. A documentação atual do Databricks para `to_date` registra que entrada malformada levanta erro com ANSI habilitado e recomenda `try_cast(... AS DATE)` quando a intenção é retornar `NULL` em vez de falhar.

Nesta revisão houve leitura estática e testes sintéticos próprios da sprint. Teste local sem PySpark e teste de runtime Spark são registrados separadamente no relatório R04-A; não há publicação Databricks nem auditoria independente implícita.
