# `null_summary` — resumir ausência por coluna com limiares explícitos

<!-- readme-objeto: 1.0.0 -->

Nulos são fáceis de contar e fáceis de interpretar mal. Este helper calcula, para cada coluna de um DataFrame Spark, quantidade e percentual de `NULL` e associa um semáforo aos limiares informados.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Perfil simples de `NULL` por coluna, devolvido como DataFrame Spark. |
| Para que serve? | Tornar ausência visível antes de análise, join ou modelagem. |
| Use quando... | Você já possui um DataFrame e quer comparar nulidade com uma política explícita. |
| Evite quando... | Precisa de diagnóstico completo de qualidade, regras de domínio ou recência. |
| Precisa de... | DataFrame Spark e limiares percentuais coerentes. |
| Entrega... | `coluna`, `count_null`, `pct_null` e `status` (`🟢`, `🟡`, `🔴`). |

Leia a [implementação](null_summary.py), a [fachada](__init__.py) e o [notebook](exemplo_null_summary.py). A função dispara ações Spark e imprime uma mensagem de sucesso; ela não persiste os dados.

## 1. O que é?

`null_summary` é um resumo de nulidade. Para cada coluna, conta valores que o Spark considera `NULL`, calcula o percentual sobre o total de linhas e aplica uma classificação local por limiar.

Ele não detecta automaticamente string vazia, valor sentinela como `-999`, categoria “desconhecido” ou `NaN` como regra de negócio. “Ausente” no contrato desta função é especificamente `isNull()`.

## 2. Que problema este recurso resolve?

A pergunta é: “Quais colunas têm valores nulos, em que quantidade e quais ultrapassam os limiares que definimos?”. Isso ajuda a não descobrir a ausência apenas depois que uma transformação ou modelo falha.

O helper não responde se o nulo é defeito. Uma data de cancelamento nula pode significar “não cancelou”; interpretar a ausência requer semântica de domínio.

## 3. Quando faz sentido usar?

Use no início de uma exploração ou antes de uma etapa sensível a nulos, quando o DataFrame já está disponível e você quer uma visão compacta por coluna.

Também é útil para comparar a mesma política ao longo de execuções, desde que os limiares estejam registrados junto com o resultado. A tabela pode ser filtrada pelos emojis para destacar somente colunas fora da faixa verde.

## 4. Quando não usar?

Não use como score geral de qualidade. A função não verifica unicidade, domínio, consistência entre colunas, recência, duplicidade ou valores impossíveis.

Não use sobre um recorte filtrado se a pergunta é a nulidade da população original: o cálculo será correto para o recorte e errado para a população pretendida.

Contraexemplo: uma coluna tem zero `NULL`, mas 30% dos registros usam `"N/A"`. O helper devolve verde, embora a ausência semântica seja alta.

## 5. Como funciona, intuitivamente?

A função primeiro executa `df.count()` para obter o total. Depois monta uma expressão `sum(isNull())` para cada coluna e coleta essa **linha agregada** para o processo Python.

Para cada coluna, calcula `100 × count_null / total`. Valores maiores ou iguais a `threshold_fail` ficam 🔴; senão, maiores ou iguais a `threshold_warn` ficam 🟡; os demais ficam 🟢. Por fim, cria um novo DataFrame Spark com uma linha por coluna e ordena por percentual decrescente.

## 6. Exemplo de situação

Uma base sintética tem 500 linhas e 13 nulos em `renda`: 2,6%. Com os defaults `threshold_warn=5` e `threshold_fail=20`, a coluna fica verde. Mantendo os mesmos dados e reduzindo o alerta para 1%, ela fica amarela.

Nada mudou na base; mudou a política. O semáforo só pode ser interpretado junto com os limiares usados.

## 7. O que você precisa antes de usar?

Você precisa de um DataFrame PySpark. Os limiares são percentuais na escala 0–100 por convenção de uso, mas **a implementação não valida faixa nem relação entre eles**. Para interpretação consistente, forneça `0 <= threshold_warn <= threshold_fail <= 100`.

O código assume que há ao menos uma coluna. Em DataFrame vazio, `total` vira zero, mas agregações de `sum` podem produzir `None`; a implementação atual não normaliza todos esses valores antes de `int()`. Trate base vazia como caso a validar explicitamente.

## 8. O que este recurso entrega?

Retorna um DataFrame Spark ordenado por `pct_null` decrescente:

| Coluna | Significado |
|---|---|
| `coluna` | nome da coluna avaliada |
| `count_null` | número de valores `NULL` |
| `pct_null` | percentual de `NULL` sobre o total de linhas |
| `status` | 🟢 abaixo do alerta; 🟡 entre alerta e falha; 🔴 a partir da falha |

A função também imprime `Resumo de nulos calculado com sucesso.`. O status não carrega os limiares dentro do DataFrame; registre-os separadamente se o resultado for persistido ou apresentado.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.spark.null_summary import null_summary

df = spark.createDataFrame([(None,), (float("nan"),), (1.0,), (2.0,)], "valor double")
warn, fail = 25.0, 50.0  # política ilustrativa deste caso
assert 0 <= warn <= fail <= 100  # pré-validação externa
if not df.columns or not df.take(1):
    raise ValueError("Base vazia: definir tratamento antes do resumo")
resumo = null_summary(df, threshold_warn=warn, threshold_fail=fail)
linha = resumo.first()
assert linha["count_null"] == 1 and linha["pct_null"] == 25.0
assert linha["status"] == "🟡"
```

O [notebook](exemplo_null_summary.py) usa dados sintéticos, altera o limiar mantendo a base constante e mostra como filtrar `status != '🟢'`. Não grava tabela.

A guarda acima pertence ao consumidor e adiciona uma ação Spark. `NaN` não conta como `NULL`. No exemplo, 25% coincide com o alerta e fica amarelo; com `threshold_fail=25.0`, a mesma taxa fica vermelha porque falha é testada primeiro. Se persistir o resultado em uma operação autorizada, registre também população, período, total e ambos os limiares; esses dados não acompanham automaticamente o retorno.

## 10. Decisões e configurações que mais importam

`threshold_warn` e `threshold_fail` são política do consumidor, não defaults oficiais de qualidade. O código aplica primeiro a condição de falha e depois a de alerta. Se os limiares forem incoerentes, a função ainda roda e o resultado pode surpreender; o README recomenda validá-los antes da chamada.

O denominador é o `df` recebido. Qualquer filtro anterior muda a população e, portanto, os percentuais.

## 11. Limitações, riscos e armadilhas

Há pelo menos duas ações Spark: a contagem total e a agregação/coleta dos nulos. Em tabela muito larga, a expressão de agregação cresce com o número de colunas. O resultado agregado coletado é pequeno — uma linha —, mas o processamento distribuído ainda precisa ler os dados necessários.

`NULL` não equivale a toda forma de dado ausente. O helper não valida os thresholds e o caso de DataFrame vazio merece guarda externa. O emoji pode ser filtrado incorretamente se alguém procurar strings como `"ok"` ou `"pass"`.

## 12. Quais são as alternativas?

[`quick_profile`](../../../hub_scripts/quick_profile/README.md) produz um perfil mais amplo de uma tabela/view e distingue métricas da base completa e da amostra. [`data_quality_check`](../../../hub_scripts/data_quality_check/README.md) lê uma tabela nomeada e acrescenta nulidade, chave candidata e recência opcional, além de status e alertas.

Use `null_summary` quando você já tem o DataFrame e quer **somente** nulidade de forma simples. Não trate essas três APIs como equivalentes apenas porque todas mencionam nulos.

## 13. Como saber se o resultado faz sentido?

Em uma amostra pequena conhecida, conte manualmente os `NULL` de uma ou duas colunas e compare. Verifique que `pct_null == 100 * count_null / total` e teste exatamente os pontos de corte: valor igual ao alerta é amarelo; valor igual à falha é vermelho.

Confirme também se strings vazias ou sentinelas precisam de regras separadas. Se a base pode estar vazia, teste e trate esse cenário antes de automatizar o helper.

## 14. Arquivos relacionados e próximos passos

- [Implementação](null_summary.py): cálculo e semáforo.
- [Fachada](__init__.py): exporta `null_summary`.
- [Notebook](exemplo_null_summary.py): demonstração sintética e filtro correto por emoji.
- [`quick_profile`](../../../hub_scripts/quick_profile/README.md): perfil mais amplo.
- [`data_quality_check`](../../../hub_scripts/data_quality_check/README.md): diagnóstico de tabela nomeada com outras dimensões.
- [Coleção](../../README.md): demais operações Spark.

## 15. Referências

O contrato foi confrontado com `null_summary.py`, a fachada e o notebook desta pasta, além das implementações locais de `quick_profile` e `data_quality_check` para a comparação de alternativas.

Os defaults não são política de negócio. Pré-validar e conferir os cortes no seu recorte não implica aprovação geral de qualidade.

[Registro técnico de referência](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/docs/sprints/readmes_objetos/RELATORIO_R04A.md): consulte data, ambiente e alcance de cada teste; o registro não é homologação do destino.
