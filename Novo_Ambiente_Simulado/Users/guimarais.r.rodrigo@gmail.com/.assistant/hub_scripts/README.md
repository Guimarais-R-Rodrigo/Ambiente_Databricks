# `hub_scripts` — utilitários executados explicitamente

> **EXTENSÃO DO HUB (`hub_`) — não auto-descoberta nem executada pelo Genie Code.**

Os scripts desta pasta são helpers de diagnóstico. Importe-os ou execute-os de forma
explícita depois de adicionar `.assistant` ao `sys.path`. Para produção, incorpore o
código ao projeto versionado, adicione testes e implante com um Declarative
Automation Bundle.

O mapa demanda → módulo, incluindo `hub_snippets`, está no
[catálogo de helpers](../CATALOGO_HELPERS.md).

```python
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
sys.path.insert(0, str(assistant_root))

from hub_scripts.quick_profile import quick_profile
profile = quick_profile("catalog.schema.table", sample_fraction=1.0, seed=42)
```

## O que volta de verdade

Saída real de `data_quality_check` sobre uma tabela sintética de 500 linhas,
executada em compute serverless. Trecho, com a estrutura preservada:

```json
{
  "status": "fail",
  "score": 75,
  "thresholds": { "null_warn": 5.0, "null_fail": 20.0, "freshness_days": 2.0 },
  "checks": {
    "row_count": 500,
    "pk_uniqueness": { "columns": ["id_cliente"], "duplicate_rows": 0, "status": "pass" },
    "nulls": {
      "renda": { "count": 20, "pct": 4.0, "status": "pass" },
      "uf":    { "count": 0,  "pct": 0.0, "status": "pass" }
    },
    "freshness": {
      "column": "dt_referencia", "max_value": "2026-07-20",
      "days_old": 25, "status": "fail"
    }
  },
  "alerts": [
    { "check": "freshness", "severity": "fail",
      "message": "Latest dt_referencia is 25 days old; limit is 2.0." }
  ]
}
```

Este retorno ilustra bem o ponto mais importante do helper: **`status: "fail"`
não significa dado ruim**. Aqui, chave sem duplicata e nulos dentro do limite —
a reprovação veio do prazo de atualização, comparado contra um limite de dois
dias que é política padrão do script, não exigência da plataforma. Uma tabela
mensal reprovaria todo dia sob esse limite. Ajuste `thresholds` ao ritmo real da
fonte antes de tratar o resultado como alerta.

`quick_profile` sobre a mesma tabela, também executado em serverless:

```json
{
  "table": "vw_doc_clientes",
  "total_rows": 500,
  "total_columns": 5,
  "sample_fraction": 1.0,
  "sample_seed": 42,
  "sample_rows": 500,
  "null_summary_full_table": [
    { "column": "renda", "null_count": 20, "null_pct": 4.0 },
    { "column": "id_cliente", "null_count": 0, "null_pct": 0.0 }
  ],
  "cardinality_sample": { "doc": 300, "uf": 4 },
  "date_range_sample": {
    "dt_referencia": { "min": "2026-01-01", "max": "2026-07-20" }
  }
}
```

Os sufixos das chaves são deliberados e carregam a informação mais importante do
retorno: `_full_table` foi calculado sobre a tabela inteira, `_sample` saiu da
amostra. Neste exemplo `sample_fraction` é 1.0, então os dois coincidem — com
fração menor, não coincidiriam. Relatar uma cardinalidade de amostra como se
fosse da tabela inteira é exatamente o erro que essa nomenclatura existe para
evitar. As demais chaves do dicionário são `dtypes`, `top_values_sample` e
`numeric_summary_sample`, omitidas aqui por extensão.

> Saídas capturadas em 14 ago 2026, em compute serverless com Spark 4.1, sobre
> tabela sintética de 500 linhas.

| Script | Contrato atual |
|---|---|
| `quick_profile.py` | nulos/contagem na tabela completa; demais estatísticas em amostra declarada |
| `data_quality_check.py` | unicidade, nulos e freshness; thresholds são política local |
| `drift_detector.py` | PSI numérico real com bins derivados da referência e bucket de ausentes |
| `rfv_calculator.py` | RFV somente até a data de referência, sem scores inventados |
| `schema_to_yaml.py` | YAML seguro; JSON é fallback válido de YAML 1.2 quando PyYAML não existe |
| `naming_checker.py` | snake_case/prefixos configuráveis e identificados como política customizada |
| `doc_coverage.py` | heurística para `.ipynb` e source notebooks exportados; não busca URLs do workspace |

## Exemplos

```python
from hub_scripts.data_quality_check import data_quality_check

quality = data_quality_check(
    "catalog.schema.table",
    pk_columns=["entity_id", "reference_date"],
    date_column="reference_date",
    thresholds={"null_warn": 2.0, "null_fail": 10.0, "freshness_days": 2},
)
assert quality["status"] != "fail", quality["alerts"]
```

```python
from hub_scripts.drift_detector import drift_detector

drift = drift_detector(
    "catalog.schema.scored_population",
    date_col="reference_period",
    date_ref="2026-06",
    date_comp="2026-07",
    cols=["score", "income"],
    num_bins=10,
)
```

## Limites

- Esses helpers não substituem Lakeflow expectations, o event log, MLflow, Model
  Serving observability, monitoramento Lakehouse ou políticas do Unity Catalog.
- Os scripts resolvem a sessão Spark sozinhos
  (`SparkSession.getActiveSession() or ...getOrCreate()`); precisam apenas de uma
  sessão ativa no runtime. Não conte com o global `spark` de notebook dentro de
  um módulo importado — ele não existe lá, e foi a causa da primeira leva de
  falhas no runtime real.
- Leituras e ações podem ter custo. Revise o plano e as permissões antes de rodar em
  tabelas grandes.
- `doc_coverage` mede adjacência de Markdown, não a qualidade da explicação.
