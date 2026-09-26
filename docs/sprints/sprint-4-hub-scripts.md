# Sprint 4 — `hub_scripts`, o portão de formato

Data: 2026-08-16 · Executor: Claude · Escopo: `ambiente_fonte/.assistant/hub_scripts/`.

É a sprint que valida o formato inteiro num volume revisável, antes de ele ser
replicado para 51 snippets. Sete objetos, com código que executa.

## O que mudou

Cada script deixou de ser um `.py` solto e virou uma pasta com três arquivos:

```text
hub_scripts/<nome>/
├── __init__.py              # gerado por tools/api_publica.py
├── <nome>.py                # movido, não reescrito
└── exemplo_<nome>.py        # notebook novo
```

Sete pastas, sete notebooks, mais o README da seção no template novo.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 0 aviso(s) — 10 pastas de objeto conferidas
render_simulado.py      OK: 201 arquivos
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
smoke test (job real)   84 verificações | 77 PASS | 0 FAIL | 7 opcionais ausentes

exemplo_data_quality_check   SUCCESS
exemplo_quick_profile        SUCCESS
exemplo_drift_detector       SUCCESS
exemplo_rfv_calculator       SUCCESS
exemplo_schema_to_yaml       SUCCESS
exemplo_naming_checker       SUCCESS
exemplo_doc_coverage         SUCCESS
```

Os sete notebooks foram executados como job serverless. O smoke test subiu de 77
para 84 verificações — os sete pacotes novos —, com **zero notebooks de exemplo
importados**: o filtro da Sprint 0 continua valendo com sete notebooks a mais
dentro de pacotes.

## A regra de conversão foi seguida à risca

Converter é **mover**. Nenhuma assinatura, nome de coluna devolvida ou
comportamento em caso de borda foi alterado. Nenhum identificador traduzido —
`threshold_warn` continua `threshold_warn`, com docstring em português.

A prova está no smoke test: os cinco casos funcionais de `hub_scripts` importam
por caminho nominal (`from hub_scripts.quick_profile import quick_profile`) e
continuam passando sem nenhuma edição. O `__init__.py` reexporta, e o caminho de
import documentado sobreviveu intacto nos sete.

**Melhorias que os módulos pedem — validação de entrada em `doc_coverage`,
constante de política em `drift_detector` — não entraram.** São etapa 2, por
objeto, com registro. Misturá-las à conversão tornaria impossível saber se uma
falha futura veio do movimento ou da mudança.

## As guardas novas provaram o valor

Ao validar com três notebooks escritos e quatro faltando:

```text
FAIL .assistant\hub_scripts\doc_coverage: falta o notebook 'exemplo_doc_coverage.py'
FAIL .assistant\hub_scripts\naming_checker: falta o notebook 'exemplo_naming_checker.py'
FAIL .assistant\hub_scripts\rfv_calculator: falta o notebook 'exemplo_rfv_calculator.py'
FAIL .assistant\hub_scripts\schema_to_yaml: falta o notebook 'exemplo_schema_to_yaml.py'
```

O `check_pastas_de_objeto`, acrescentado pela auditoria da Sprint 1, nomeou
exatamente os quatro que faltavam. Sem ele, a sprint poderia ter fechado com
pastas incompletas e ninguém notaria até a auditoria.

A conferência também acusou os sete `.py` no caminho antigo sobrevivendo no
workspace — o mesmo padrão da Sprint 2, agora esperado e tratado.

## O que cada notebook ensina

Todos seguem os quatro movimentos e fecham com "quando **não** usar". O que os
diferencia é a armadilha que cada um foi construído para mostrar:

| Notebook | O erro que ele faz acontecer |
|---|---|
| `data_quality_check` | tratar `status: fail` como dado ruim, quando a reprovação veio de uma política de atualidade que não cabe naquela fonte |
| `quick_profile` | copiar a cardinalidade da amostra para um relatório como se fosse da tabela inteira |
| `drift_detector` | comparar médias entre dois períodos com a **mesma média** e formas completamente diferentes |
| `rfv_calculator` | agregar a base inteira e incluir transações posteriores à data de decisão |
| `schema_to_yaml` | ligar `include_stats` por hábito e atribuir a lentidão ao Spark |
| `naming_checker` | ler política da casa como exigência do Unity Catalog |
| `doc_coverage` | tratar cobertura alta como notebook bem documentado |

O de `drift_detector` constrói duas safras com médias praticamente idênticas e
distribuições opostas — o caso em que a comparação natural não vê nada. O de
`rfv_calculator` compara o resultado do helper com uma contagem filtrada à mão e
prova que zero transações posteriores entraram.

O de `doc_coverage` faz algo incomum: demonstra o **limite** da ferramenta,
mostrando que um markdown com um ponto final pontua igual a uma explicação boa.
Não é defeito a corrigir — qualquer medida automática de qualidade de texto
erraria com aparência de autoridade —, e declarar isso é a informação mais útil
que aquele script tem a dar.

## O que fica para a auditoria

Esta é a sprint em que o formato é aprovado ou refeito. Pontos onde uma sessão
sem contexto deve olhar primeiro:

- Se algum notebook tem saída colada que não confere com a execução real.
- Se a regra "converter é mover" foi de fato respeitada — comparar cada módulo
  com a versão anterior e confirmar que nada mudou além do caminho.
- Se a profundidade da explicação é comparável entre os sete, ou se dá para
  perceber quais foram escritos primeiro.
- Se o README da seção lista o que existe, sem sobrar nem faltar, e se a
  distinção script × snippet está clara para quem chega.
- Se algum dos sete deveria ter recebido a etapa 2 (melhoria) imediatamente, por
  o defeito ser grave o bastante para não esperar.
