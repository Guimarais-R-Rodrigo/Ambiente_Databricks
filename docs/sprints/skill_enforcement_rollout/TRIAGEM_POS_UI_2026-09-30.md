# Triagem das seis checagens dirigidas de UI — 2026-09-30

(Codex) O lote proporcional previsto na
[reconciliação](RECONCILIACAO_SD_FG_2026-09-29.md) foi coletado:
Concierge espontâneo e @, EDA @, Tutor @, Comentar Notebook @ e
Auditoria Skills @. A seleção/carregamento relatada pelo usuário passou
em seis casos; isso valida apenas a observação de UI desses chats. O
hash B1 anteriormente verificado é histórico: a versão remota efetiva
depois da publicação paralela de micromodelos não foi lida nesta triagem.

| Caso | Observação material | Regra local vigente | Decisão |
|---|---|---|---|
| [FG-CC-P](genie_evidencias/FG-CC-P_T01.md) / [FG-CC-A](genie_evidencias/FG-CC-A_T01.md) | Descoberta e função `fmt_brl` adequadas; leitura remota não provada na transcrição | Concierge pede fonte consultada e separação da recomendação | Nenhum reteste imediato; não afirmar que arquivos específicos foram lidos remotamente |
| [FG-EDA-A](genie_evidencias/FG-EDA-A_T01.md) | Presumiu tipos/grão sem schema | EDA já restringe hipóteses a planejamento e não preenche chave/grão ausentes | Preservar FAIL parcial; não duplicar regra nem publicar sem causa nova |
| [FG-TU-A](genie_evidencias/FG-TU-A_T01.md) | Declarou execução anterior ausente, `df` inexistente e estado da tabela sem prova suficiente | Tutor já exige marcar resultado/status não informado sem output ou histórico | Preservar FAIL material; próximo reteste só com hipótese que separe contexto real do notebook do exemplo hipotético |
| [FG-CN-A](genie_evidencias/FG-CN-A_T01.md) | Markdown correto com resultado pendente; frase amplia ausência de execução para além da sessão | Skill já manda usar apenas valores observados e adaptar templates | PASS de núcleo com ressalva; sem reteste isolado |
| [FG-AU-A](genie_evidencias/FG-AU-A_T01.md) | Detectou número e execução sem prova, mas score incoerente e preflight/Receipt apenas alegados | Auditoria já exige preflight/runner e escada de evidência; score subordinado aos vetos, templates adaptáveis | Preservar FAIL parcial e estado mecânico NOT_OBSERVABLE; não homologar SE07 com texto narrativo |

Não há causa demonstrada de defeito dos scripts/contratos locais pelas três
falhas de precisão: a resposta conversacional divergiu de regras já
presentes. Repetir frase no `SKILL.md` ou publicar sobre trabalho paralelo
sem verificar bytes remotos não é correção causal. Nenhuma alteração em
`ambiente_fonte/`, policy ou workspace Free foi feita nesta triagem.

## Próxima coleta humana proporcional

O [SD-CE-P/T01](genie_evidencias/SD-CE-P_T01.md) executou Spark
exploratório sem carregar Cross-EDA nem usar Receipt/verificador. A
instrução global de roteamento foi ajustada depois daquela coleta.
Um único reteste espontâneo em chat novo pode verificar essa mudança e
separar: skill indicada na UI, cálculo da fixture, rota canônica e
alegações de conclusão. O prompt está no
[roteiro guiado](GENIE_RODADAS_GUIADAS_2026-09-29.md). O caso original
permanece FAIL; não contar a nova resposta como substituição. Os demais
retestes ficam condicionados aos resultados e a hipóteses concretas.

O [D01](genie_evidencias/SD-CE-P-D01.md) foi coletado: Cross-EDA apareceu
sem @ e a conta dos IDs passou, mas o Genie preencheu contexto ausente
para alegar execução canônica sem output verificável. O roteamento mudou
de FAIL para PASS neste diagnóstico; SER05 conversacional não foi
homologado. O próximo reteste proporcional examina `UNKNOWN` de Pipeline
Builder após limpeza remota incerta, com prompt no roteiro guiado.

O [SD-PB-DELTA-D01](genie_evidencias/SD-PB-DELTA-D01.md) passou na
classificação do estado `UNKNOWN`, mas nenhuma skill apareceu e a
resposta acrescentou sem prova semântica de tabela gerenciada/UC e
probabilidades de conclusão. Um único reteste com @ e o mesmo cenário
separa aderência da skill do acerto conceitual sem roteamento. Prompt no
roteiro guiado; nenhuma edição de produto/publicação foi feita.

No [D02 com @](genie_evidencias/SD-PB-DELTA-D02.md), Pipeline Builder
apareceu na UI e a resposta preservou `UNKNOWN`, mas continuou a
preencher detalhes de tabela gerenciada/arquivos e omitiu o vínculo
inicial com effect record/ownership. O próximo teste material é Baseline:
separar plano de treino, seleção em validação e holdout final, sem fit
nem tracking inventados. Prompt no roteiro guiado.

O [SD-BL-P-D01](genie_evidencias/SD-BL-P-D01.md) preservou o holdout e
não executou treino/tracking, corrigindo a falha principal de T01 neste
cenário. Restou a suposição de maturidade no fim do mês seguinte sem
convenção declarada; indicador separado de Baseline confirmado posteriormente.
O próximo
reteste focal é Feature Engineering, para não inventar finalizador da
materialização e separar PIT upstream de efeito Delta `UNKNOWN`.

O [SD-FE-MAT-D01](genie_evidencias/SD-FE-MAT-D01.md) separou corretamente
PIT upstream de efeito `UNKNOWN` e nomeou os dois entrypoints reais de
materialização, sem finalizador inventado. A resposta extrapolou colunas do
readback e a causa de `BLOCKED_OWNERSHIP_OR_DROP_UNKNOWN`. O usuário viu
somente Baseline ML no indicador, embora a resposta diga ter consultado
Feature Engineering; o roteamento espontâneo FE falhou nesta rodada.
Não houve execução remota nesta rodada. O último reteste proporcional
planejado é Safra com corte informado e quatro estados de cobertura; prompt
no roteiro guiado.

O [SD-VF-STATUS-D01](genie_evidencias/SD-VF-STATUS-D01.md) acertou os
quatro pares maturity/coverage_status e recusou taxa final sem valores
binários. Introduziu, porém, a ideia de taxa provisória MOB2 com
denominador 1 apesar do roster fixo 2; nenhum cálculo foi executado.
A chamada @ e o indicador separado de Safra foram confirmados pelo usuário.
Com isso, as rodadas manuais proporcionais planejadas foram coletadas.
Resta resolver observabilidade pendente, revisar os FAILs materiais e
reconciliar versão remota com a publicação paralela de micromodelos.

## Conferência remota somente leitura após as rodadas

Em 2026-09-30, `python -B tools/publicar_free.py --verify --conteudo
--profile FREE` comparou **657/657** arquivos gerenciados, sem diferenças
de conteúdo, e confirmou **15/15** diretórios de skills. Hash normalizado
local `7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O verificador retornou **FAIL de inventário**, com 30 objetos extras;
todos estão sob `.assistant/hub_micromodelos/` e pertencem à frente paralela
informada pelo usuário. Foram preservados. Não há evidência, neste
readback, de versão divergente nos 657 arquivos B1 gerenciados. Isso não
prova que os extras não influenciam roteamento ou que a Genie executou
scripts canônicos. Relatório bruto:
`.artifacts/skills-delivery-evidence/genie-20260930-final-remote-verify.json`,
SHA-256 `45844d944d741c24556f7a7ea0331def4b55c60a0e080e16a6a98faaa887d674`.
Nenhuma escrita remota, limpeza ou publicação foi feita.

Próximo trabalho local: consolidar os FAILs materiais por causa demonstrada
e decidir correção focal apenas quando o contrato vigente não cobrir o
comportamento. Roteamento espontâneo FE falhou nesta rodada, enquanto Safra
por @ carregou. O indicador de Baseline em SD-BL-P-D01 foi confirmado.
Não exigir os 41 prompts FG históricos sem nova hipótese.

A [consolidação da campanha](CONSOLIDACAO_GENIE_B1_2026-09-30.md) apresenta
o estado por skill, separa provas locais/Free de respostas Genie e prioriza
a fila sem presumir homologação integral.
