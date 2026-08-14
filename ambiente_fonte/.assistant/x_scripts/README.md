# `x_scripts` — utilitários executados explicitamente

> **EXTENSÃO CUSTOMIZADA (`x_`) — não auto-descoberta nem executada pela Genie Code.**

Os scripts desta pasta são helpers de diagnóstico. Importe-os ou execute-os de forma
explícita depois de adicionar `.assistant` ao `sys.path`. Para produção, incorpore o
código ao projeto versionado, adicione testes e implante com um Declarative
Automation Bundle.

O mapa demanda → módulo, incluindo `x_snippets`, está no
[catálogo de helpers](../x_docs/catalogo_helpers.md).

```python
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
sys.path.insert(0, str(assistant_root))

from x_scripts.quick_profile import quick_profile
profile = quick_profile("catalog.schema.table", sample_fraction=0.05, seed=42)
```

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
from x_scripts.data_quality_check import data_quality_check

quality = data_quality_check(
    "catalog.schema.table",
    pk_columns=["entity_id", "reference_date"],
    date_column="reference_date",
    thresholds={"null_warn": 2.0, "null_fail": 10.0, "freshness_days": 2},
)
assert quality["status"] != "fail", quality["alerts"]
```

```python
from x_scripts.drift_detector import drift_detector

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
- `spark` deve existir no ambiente para os scripts que leem tabelas.
- Leituras e ações podem ter custo. Revise o plano e as permissões antes de rodar em
  tabelas grandes.
- `doc_coverage` mede adjacência de Markdown, não a qualidade da explicação.
