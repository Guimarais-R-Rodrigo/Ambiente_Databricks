# `pit_join` — preservação de linha e escolha da versão · 08/09/2026

Evidência do pacote T2 do plano consolidado. Não substitui a rodada no runtime de
destino; ela mede o comportamento do código, não o ambiente.

## O limite que motivou o teste

O `pit_join` já reconciliava as quatro categorias do diagnóstico:

```python
if sem_chave + com_feature + entidade_sem_historico + sem_disponivel != total:
    raise AssertionError("categorias do diagnóstico pit_join não reconciliam")
```

`total` é `sum(categorias.values())`, e as categorias vêm do próprio
`linhas_diag`. A asserção é, portanto, uma checagem de **completude de rótulo**:
ela pega uma quinta categoria inesperada. Não é uma checagem de **preservação de
linha** — perder uma linha e duplicar outra mantém a soma e passa despercebido.

## O que o novo caso mede

`t_pit_join_preservacao`, em `tools/spark_smoke_test.py`, usa uma fixture pequena e
inteiramente conhecida — 6 linhas de fato, 4 de feature — em que cada linha existe
para exercitar uma categoria:

| Linha de fato | Situação | Categoria esperada | Valor esperado |
|---|---|---|---|
| `C1`, 2026-03-10 | 3 versões no histórico | `com_feature` | 20 |
| `C1`, 2026-03-10 | **linha de fato duplicada** | `com_feature` | 20 |
| `C2`, 2026-03-10 | histórico só com referência futura | `sem_feature_disponivel_na_data` | nulo |
| `C3`, 2026-03-10 | nenhum histórico | `entidade_sem_historico` | nulo |
| `NULL`, 2026-03-10 | chave nula | `sem_chave_ou_data` | nulo |
| `C4`, `NULL` | data de decisão nula | `sem_chave_ou_data` | nulo |

Com `atraso_publicacao_dias=3`, a versão de 2026-02-28 fica disponível em 03-03 e é
a escolhida; a de 2026-03-09 só em 03-12 e é proibida; a de 2026-01-31 é elegível
mas não é a mais recente.

Asserções, além das categorias:

1. `resultado.count() == fatos.count()` — comparação contra a **entrada**, não
   contra um total derivado da saída;
2. `diag["linhas_fato"] == fatos.count()`;
3. `C1` mantém **2** linhas — multiplicidade, não só contagem total;
4. o valor trazido para `C1` é 20, e nem 10 nem 99 aparecem em lugar nenhum;
5. `C2`, `C3`, `C4` e a linha de chave nula recebem feature nula.

## Execução

Executado localmente contra **PySpark 3.5.3** na VM da ponte de arquivos, e não no
Databricks. O runtime observado do laboratório é Spark 4.2.0; a VM só tem Java 11,
que não suporta Spark 4. As funções usadas (`to_date`, `join`, janelas) têm a mesma
semântica nas duas versões, mas **esta rodada não substitui o smoke no destino**.

| Rodada | Resultado |
|---|---|
| código real | **PASS** |
| mutante A — perde uma linha da saída | REPROVOU: `entrada=6, saída=5` |
| mutante B — troca uma linha de `C1` por cópia de `C3`, **total preservado (6→6)** | REPROVOU: `C1 deveria manter as 2 linhas de fato duplicadas, obtido 1` |
| mutante C — escolhe a versão antiga (10 no lugar de 20) | REPROVOU: `C1 deveria receber a versão de 2026-02-28 (20), obtido {10}` |
| mutante D — deixa a feature futura atravessar | REPROVOU: `C2 não deveria receber feature, obtido [77]` |

O **mutante B é o que importa**: ele preserva o total e passaria pela invariante
anterior. É reprovado pela asserção de multiplicidade.

## O que continua fora deste teste

- Comportamento em volume, particionamento e skew;
- `politica_empate` com instantes de disponibilidade idênticos;
- fuso horário de sessão diferente do padrão;
- ACLs, Unity Catalog e runtime do workspace corporativo.

O caso precisa ser reexecutado no Free (Spark 4.2.0) na próxima rodada de smoke, e
o resultado registrado em `docs/testes/spark/resultados/`.
