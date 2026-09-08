# `hub_scripts/` — diagnósticos antes de confiar

> **HUB · EXECUÇÃO MANUAL.** Estes scripts não são auto-descobertos nem
> executados pelo Genie Code. Adicione `.assistant` ao `sys.path` e importe o
> diagnóstico explicitamente.

Use quando a pergunta for “posso confiar nesta tabela ou notebook?”. Se precisa
de uma função para compor uma transformação, use
[`hub_snippets`](../hub_snippets/README.md).

## Comece por aqui

```python
import sys
from pathlib import Path

assistant_root = Path("/Workspace/Users/<username>/.assistant")
sys.path.insert(0, str(assistant_root))

from hub_scripts.data_quality_check import data_quality_check

veredito = data_quality_check(
    "catalogo.crm.contatos",
    primary_keys=["id_cliente"],
    date_column="dt_referencia",
)

if veredito["status"] == "fail":
    raise ValueError(veredito["alerts"])
```

`status="fail"` significa que há uma decisão pendente antes da medição; não
significa automaticamente que o dado deve ser descartado.

## Catálogo

| Script | Responde | Use antes de |
|---|---|---|
| [`data_quality_check`](data_quality_check/) | chave é única, campos críticos estão completos e dado está atual? | medir tabela nova |
| [`quick_profile`](quick_profile/) | qual schema e perfil básico, com origem de cada número? | explorar em profundidade |
| [`drift_detector`](drift_detector/) | distribuição mudou entre referência e atual? | concluir estabilidade |
| [`rfv_calculator`](rfv_calculator/) | recência, frequência e valor no instante correto? | criar segmentação/feature |
| [`schema_to_yaml`](schema_to_yaml/) | como serializar e comparar a estrutura? | documentar contrato |
| [`naming_checker`](naming_checker/) | quais nomes violam a convenção informada? | publicar artefato |
| [`doc_coverage`](doc_coverage/) | quais blocos de código carecem de explicação? | revisar notebook |

O [catálogo de helpers](../CATALOGO_HELPERS.md) inclui também dependências,
API pública e mapa por demanda.

## Forma e aprendizado

```text
hub_scripts/<nome>/
├── __init__.py
├── <nome>.py
└── exemplo_<nome>.py
```

O notebook `exemplo_*` mostra dado sintético, falha típica, saída real,
interpretação e “quando não usar”. Abra-o antes de adotar um limiar ou campo da
saída.

## Escolha script ou snippet

| Característica | `hub_scripts` | `hub_snippets` |
|---|---|---|
| entrada típica | nome de tabela ou caminho de notebook | `DataFrame`/array/parâmetros |
| papel | diagnóstico autocontido | peça de cálculo reutilizável |
| saída | veredito + evidência | dado, métrica, figura ou modelo |
| uso comum | antes de confiar/publicar | dentro de notebook/pipeline |

## Limites

- Nenhum script corrige ou filtra dado sozinho.
- Limiares são política local e precisam aparecer na saída aplicada.
- Leituras agregadas têm custo; confira plano e volume.
- Sessão Spark é resolvida pelo módulo, sem depender do global `spark` do
  notebook.
- Resultado no Free não prova compatibilidade no workspace do trabalho.
- Estes diagnósticos não substituem expectations do Lakeflow, event log,
  monitoramento de produção ou políticas do Unity Catalog.

## Onde continuar

- [Guia do ecossistema](../README.md)
- [Catálogo de helpers](../CATALOGO_HELPERS.md)
- [Biblioteca `hub_snippets`](../hub_snippets/README.md)
- [Template para novo script](../hub_padroes/script/template.md)
