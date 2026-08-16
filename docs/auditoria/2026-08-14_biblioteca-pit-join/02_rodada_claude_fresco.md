# Rodada 1 — Claude em sessão sem contexto

> **Nomenclatura da época.** Os nomes `x_*` e `rodrigo-*` neste registro são
> os que existiam na data. A correspondência com os nomes atuais está no ADR
> da reestruturação do Hub; este documento não é reescrito porque descreve o
> que foi observado, não o estado atual.

Data: 2026-08-14 · Auditor: Claude, janela nova, sem acesso ao repositório
Material: `pit_join.py` e `join_diagnostics.py`, colados no chat

## Nível real desta rodada

**Não é A2.** O desenho previa três modelos de origens diferentes, partindo de
que modelos distintos erram de formas distintas. Aqui o auditor é do mesmo
modelo do implementador, então pontos cegos comuns permanecem. O que se
preservou foi o contexto zerado: o auditor não viu justificativas, changelog nem
resultados de teste, e por isso não teve como racionalizar decisões.

Vale como **A1**, e o gate para levar o material ao trabalho continua exigindo
uma segunda origem quando houver disponibilidade.

## Resultado

15 achados, dos quais **13 procedentes**. Todos os de severidade Crítico e Alto
foram confirmados por leitura do código e, depois, por teste que reproduz o
cenário descrito.

| Achado | Veredito | Situação |
|---|---|---|
| C1 — `atraso=0` com comparação inclusiva vaza feature do mesmo dia | procede | corrigido: parâmetro obrigatório, sem default |
| A1 — `janela_maxima_dias` medida na disponibilidade, não na referência | procede | corrigido: janela real era `janela + atraso` |
| A2 — fuso da sessão altera o corte quando a feature é `DATE` | procede | mitigado: semântica documentada e fuso reportado no diagnóstico |
| A3 — três causas de ausência fundidas em um número | procede | corrigido: causas separadas |
| A4 — cobertura inclui chave nula no denominador, exemplos não | procede | corrigido: denominador de chaves válidas |
| A5 — junção materializa o produto antes de reduzir | procede | parcial: janela recomendada e documentada; hint de range-join não aplicado |
| M1 — multiplicidade medida sobre o lado direito inteiro | procede | corrigido: restrita às chaves presentes à esquerda |
| M2 — encadear duas chamadas quebra por coluna interna | procede | corrigido: coluna interna não é devolvida por padrão |
| M3 — expansão descreve só o `left` | procede | corrigido: `left` e `inner` reportados |
| M4 — `ts_feature` nulo desaparece sem contabilização | procede | corrigido: contagem no diagnóstico |
| M5 — múltiplas ações sobre fonte não determinística | procede | corrigido no `join_diagnostics`: contagem em passada única |
| M6 — desempate por valor ascendente enviesa para o menor | procede | corrigido: `politica_empate="erro"` por padrão |
| B1, B2, B3, B4 | procedem | corrigidos: tipo do parâmetro, backticks, expansão de base vazia, amostra ordenada |

## Achados não incorporados

- **A5 (hint de range-join)**: a recomendação de `hint("range_join", 86400)`
  depende de plano físico sobre volume representativo, que o laboratório não
  tem. Fica como pendência para o ambiente do trabalho, junto da verificação
  por `explain()`.
- **Auto-join ambíguo** (item "não consegui avaliar"): o auditor não podia
  saber, mas esse defeito ocorreu de fato durante a implementação e foi
  resolvido antes desta rodada, renomeando as chaves na volta. Os testes
  confirmam que não reincide no Spark 4.1.

## O que a rodada prova sobre o processo

Os módulos tinham passado em 13 verificações de runtime escritas pelo próprio
implementador. Elas cobriam corretude no caminho feliz e a invariante
anti-vazamento — e **não pegaram nenhum** dos treze achados. As categorias que
escaparam foram: ambiguidade semântica de tipo de data, interação entre dois
parâmetros que os testes nunca combinaram, diagnósticos que agregam causas
distintas, comportamento em escala, encadeamento de chamadas e política de
empate.

É o argumento a favor de manter a auditoria como gate: teste escrito por quem
implementou herda as suposições de quem implementou.

## Verificação das correções

Notebook `x_lab/verificar_auditoria`, com um teste por achado reproduzindo o
cenário do relatório: **10 aprovações, nenhuma falha**
(`resultado_correcoes.json`).

Duas falhas surgiram durante a correção e também foram resolvidas: o helper
passou a chamar `conf.get(chave, default)`, que no Spark Connect valida o
segundo argumento como valor de configuração e derruba a execução; e a fixture
`fatos_e_features` sorteava datas de referência que podiam coincidir, criando
empate acidental — a guarda nova funcionou e o denunciou, mas a fixture deve
testar empate de propósito, não por acaso.
