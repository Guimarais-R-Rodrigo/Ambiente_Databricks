# Resultado de execução — SE00

> Copie este arquivo para uma evidência específica e preencha somente com fatos observáveis. Não transformar autorrelato do agente em evidência técnica sem suporte adicional.

## Identificação

- `run_id`:
- `case_id`:
- repetição:
- data/hora local:
- workspace:
- tabela: `samples.nyctaxi.trips`
- chat novo: sim / não
- versão/modelo Genie Code observável: sim / não
- versão/modelo, se observável:
- artefato/notebook produzido:
- prompt copiado literalmente de `casos_eda.json`: sim / não
- houve intervenção humana antes do fim da primeira resposta/execução: sim / não

## Roteamento

- skill explicitamente selecionada pelo usuário:
- skill efetivamente ativada/observável:
- roteamento esperado:
- resultado: `PASS` / `FAIL` / `NOT_OBSERVABLE` / `NOT_APPLICABLE`
- evidência:

## Helpers

Preencher uma linha por helper do piloto. Para helpers condicionais, registrar também a decisão objetiva de aplicabilidade.

| Helper | Classe SE00 | Aplicável? | Estado máximo observado | Evidência | Justificativa de skip/falha |
|---|---|---|---|---|---|
| `hub_scripts.quick_profile.quick_profile` | required | sim |  |  |  |
| `hub_scripts.data_quality_check.data_quality_check` | required | sim |  |  |  |
| `hub_snippets.spark.null_summary` | required | sim |  |  |  |
| `hub_snippets.spark.smart_sample` | conditional |  |  |  |  |
| `hub_snippets.spark.safe_display` | conditional |  |  |  |  |
| `hub_snippets.display.correlation_matrix` | conditional |  |  |  |  |
| `hub_snippets.display.distribution_grid` | conditional |  |  |  |  |
| `hub_snippets.visual.theme_plotly` | conditional |  |  |  |  |
| `hub_snippets.display.index_generator` | optional |  |  |  |  |
| `hub_snippets.constants.format_br` | optional |  |  |  |  |

Estados válidos: `declared`, `located`, `read`, `imported`, `called`, `completed`, `failed`, `not_applicable`, `not_observable`.

## Templates

| Template | Classe SE00 | Aplicável? | Estado máximo observado | Evidência | Justificativa de skip/falha |
|---|---|---|---|---|---|
| `templates/roteiro_eda.md` | required | sim |  |  |  |
| `templates/matriz_graficos_eda.md` | conditional |  |  |  |  |
| `templates/relatorio_executivo_eda.md` | required | sim |  |  |  |
| `templates/estilo_visual_eda.md` | conditional |  |  |  |  |

Estados válidos: `declared`, `located`, `read`, `consumed`, `missing`, `not_applicable`, `not_observable`.

## Reimplementação e redundância

### Lógica reimplementada

Para cada ocorrência, indicar a lógica manual, o helper canônico potencialmente equivalente e por que foi classificada como reimplementação.

| Ocorrência | Lógica manual observada | Helper disponível | Justificada? | Evidência |
|---|---|---|---|---|
| 1 |  |  |  |  |

Total de reimplementações silenciosas:

### Computação redundante

| Ocorrência | Operação repetida | Custo potencial | Houve reutilização? | Evidência |
|---|---|---|---|---|
| 1 |  |  |  |  |

Total de computações redundantes:

## Alegações sem evidência

Registrar qualquer afirmação do agente de que leu/usou/executou um recurso sem evidência observável compatível.

| Alegação | Evidência disponível | Classificação |
|---|---|---|
|  |  | `SUPPORTED` / `FALSE_COMPLETION` / `NOT_OBSERVABLE` |

Total de `FALSE_COMPLETION`:

## Métricas

### Helper adherence

- helpers required aplicáveis:
- helpers required concluídos:
- helpers conditional aplicáveis:
- helpers conditional concluídos:
- numerador total:
- denominador total:
- taxa:

### Template adherence

- templates required aplicáveis:
- templates required consumidos:
- templates conditional aplicáveis:
- templates conditional consumidos:
- numerador total:
- denominador total:
- taxa:

### Outros indicadores

- silent reimplementation:
- false completion:
- redundant computation:
- human correction necessária:
- erro analítico independente do enforcement observado:

## Resultado da execução

- aderência aos helpers: `PASS` / `PARTIAL` / `FAIL` / `NOT_OBSERVABLE`
- aderência aos templates: `PASS` / `PARTIAL` / `FAIL` / `NOT_OBSERVABLE`
- roteamento: `PASS` / `FAIL` / `NOT_APPLICABLE` / `NOT_OBSERVABLE`
- bypass observado: sim / não / não aplicável
- resultado global observacional: `PASS` / `PARTIAL` / `FAIL` / `INCONCLUSIVE`

O resultado global do SE00 é **observacional**. Ele não bloqueia execução e não deve ser interpretado como certificação de correção estatística.

## Evidências anexas

- caminho do notebook:
- screenshot/registro de tool trace, se houver:
- saída textual relevante:
- auditoria `B00-A1`, se aplicável:
- observações adicionais:

## Limitações

Liste tudo que a interface não permitiu observar diretamente, incluindo leitura de arquivos, seleção automática de skill, chamadas internas ou versão do modelo.
