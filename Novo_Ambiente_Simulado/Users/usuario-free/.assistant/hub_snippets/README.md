# `hub_snippets/` — biblioteca Python reutilizável

> **HUB · IMPORT MANUAL.** Esta pasta não é uma Agent Skill, não é instalada
> pelo Genie Code e nenhum módulo entra automaticamente no chat ou no runtime.

Use um snippet quando precisar de uma função para compor seu notebook, teste ou
pipeline. Para diagnóstico que recebe nome de tabela/notebook e devolve um
veredito, veja [`hub_scripts`](../hub_scripts/README.md).

## Encontre antes de importar

O [catálogo de helpers](../CATALOGO_HELPERS.md) é o documento dono do mapa:

```text
demanda → módulo → API pública → dependência → restrição de runtime
```

Não mantenha uma segunda lista completa aqui. Este README explica a forma e o
uso; o catálogo responde “qual helper resolve meu problema?”.

| Pacote | Finalidade | Cuidado principal |
|---|---|---|
| `constants` | formato brasileiro, cores e estilos | convenções locais, não identidade oficial Databricks |
| `visual` | tema Plotly, seções, badges e KPIs | escape de texto e compatibilidade de render |
| `spark` | joins temporais, qualidade, amostra e display | ações distribuídas, custo e Spark Connect |
| `display` | gráficos e tabelas de exploração | coleta no driver sempre limitada |
| `ml` | validação, modelos, explicabilidade e monitoramento | dependências opcionais e leakage |
| `testing` | dados sintéticos determinísticos | apenas teste/exemplo |
| `tests` | regressão local de helpers driver-side | não é pasta de objeto nem produto importável |

## Primeiro uso

Adicione a pasta `.assistant` ao path:

```python
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if not assistant_root.is_dir():
    raise FileNotFoundError(f"Defina o caminho correto: {assistant_root}")

sys.path.insert(0, str(assistant_root))

from hub_snippets.spark.null_summary import null_summary
from hub_snippets.visual.theme_plotly import aplicar_tema
```

Se o pacote estiver dentro do projeto, derive o caminho a partir da raiz do
projeto em vez de fixar um usuário.

Teste barato, sem ação Spark:

```python
from hub_snippets.constants.format_br import fmt_brl, fmt_pct

assert fmt_brl(1.999) == "R$ 2,00"
assert fmt_pct(0.928) == "92,8%"
```

Silêncio no import significa apenas que o módulo foi localizado. Não prova que a
função executará no runtime nem que a lógica está correta para seus dados.

## Forma de cada objeto

```text
hub_snippets/<pacote>/<objeto>/
├── __init__.py              # API pública
├── <objeto>.py              # implementação importável
└── exemplo_<objeto>.py      # notebook didático
```

Abra `exemplo_<objeto>` antes de usar a função. Ele apresenta:

1. problema e erro típico;
2. ambiente e dependências;
3. exemplo executável com dado sintético;
4. saída real e interpretação;
5. situações em que o helper é a escolha errada.

No workspace, `exemplo_*` aparece como notebook sem a extensão `.py`. A
implementação ao lado precisa permanecer arquivo Python comum para que o import
funcione.

## Dependências opcionais

O arquivo [`requirements-optional.txt`](requirements-optional.txt) é inventário,
não lockfile universal.

1. Escolha o helper no catálogo.
2. Instale apenas a dependência marcada para ele.
3. Fixe a versão no projeto consumidor.
4. Reinicie o Python quando o notebook exigir.
5. Reexecute no runtime de destino.

Ambiente gerenciado muda. Uma biblioteca que funcionou numa data pode deixar de
funcionar — ou o inverso — após atualização do runtime.

## Diagnóstico de import e execução

| Sintoma | Causa provável | Ação |
|---|---|---|
| `No module named 'hub_snippets'` | path aponta para `hub_snippets`, não para o pai | adicione `.assistant` |
| dependência como `lightgbm` ausente | opcional exigida no import | instale versão fixada ou escolha outro helper |
| import passa, chamada falha | dependência é carregada tardiamente | confira catálogo e notebook de exemplo |
| `NOT_SUPPORTED_WITH_SERVERLESS` | API não aceita nesse compute/runtime | use alternativa documentada e teste no destino |
| `NameError: spark` dentro do módulo | código contou com global de notebook | resolva `SparkSession` explicitamente |
| `Py4JError` em API de ML | superfície clássica não exposta por Spark Connect | use API compatível ou compute apropriado |

Esses padrões são diagnósticos, não garantias universais. Preserve a mensagem
completa, runtime e data ao registrar uma falha nova.

## Contrato de segurança

- Não use `toPandas()` ou coleta no driver sem limite verificável.
- Declare grão, chave, tempo e classe positiva quando aplicável.
- Ajuste preprocessamento somente no treino.
- Respeite disponibilidade point-in-time e atraso de publicação.
- Trate PSI e thresholds como heurísticas calibráveis.
- Não esconda falha com sentinela arbitrária; retorne diagnóstico ou lance erro.
- Helper não substitui expectativa de pipeline, monitoramento de produção ou
  política do Unity Catalog.

## Onde continuar

- [Catálogo demanda → helper](../CATALOGO_HELPERS.md)
- [Diagnósticos em `hub_scripts`](../hub_scripts/README.md)
- [Template para novo snippet](../hub_padroes/snippet/template.md)
- [Guia do ecossistema](../README.md)
