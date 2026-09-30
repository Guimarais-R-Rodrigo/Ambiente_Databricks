# Reconciliação de cobertura SD × FG — 2026-09-29

(Codex) **Revisão de suficiência após questionamento do usuário:** não há
justificativa para iniciar automaticamente 18 a 42 novas interações Genie.
A primeira análise abaixo mapeou apenas SD versus FG e omitiu o histórico
forward e o critério de reabertura por mudança. A estimativa anterior fica
superada por esta análise por objetivo, com duas auditorias somente leitura.

As 37 primeiras tentativas SD foram coletadas. A matriz FG mede roteamento;
SD também mede qualidade/aderência e, quando aplicável, execução. Um objetivo
pode ser coberto por evidência de outra ficha sem alegar que o prompt FG
literal foi enviado. Fichas não executadas continuam NOT_RUN; cobertura
reutilizada deve declarar fonte, condição de seleção, versão e limites.

| Skill FG | P — SD análogo | N — SD análogo | A — SD análogo | Lacuna de cobertura |
|---|---|---|---|---|
| EDA | — | — | — | 3 sem análogo SD |
| Cross-EDA | SD-CE-P | SD-CE-N | SD-CE-A | Prompts FG distintos; SD-P sem indicador |
| Feature Engineering | SD-FE-P; SD-FE-PIT/MAT | SD-FE-N | SD-FE-A | Prompt FG distinto; SD-FE-P sem indicador |
| Validação Estatística | SD-ST-P | SD-ST-N | SD-ST-A | Prompts FG distintos; SD-ST-N roteou Tutor |
| Baseline ML | SD-BL-P; SD-BL-MLFLOW | SD-BL-N | SD-BL-A | Prompts FG distintos; MLflow sem indicador claro |
| Explainability | SD-EX-P | SD-EX-N | SD-EX-A | Prompts FG distintos |
| Monitoramento | SD-MO-P; SD-MO-LABEL | SD-MO-N | SD-MO-A | Prompts FG distintos; SD-MO-LABEL roteou ST |
| Pipeline Builder | SD-PB-P; SD-PB-DELTA | SD-PB-N | SD-PB-A | Prompts FG distintos; PB-P/DELTA sem roteamento provado |
| Safra | SD-VF-P | SD-VF-N | SD-VF-A | Prompts FG distintos; SD-VF-P sem indicador |
| Comentar Notebook | — | — | — | 3 sem análogo SD |
| Tutor Databricks | — | — | — | 3 sem análogo SD; ocorrência como desvio em SD-ST-N não é teste TU |
| Auditoria Skills | — | — | — | 3 sem análogo SD |
| Criar Objeto | — | — | — | 3 sem análogo SD |
| Concierge | — | — | — | 3 sem análogo SD |

Há 24 entradas com análogo SD e 18 sem análogo **SD**. Isso não significa
18 objetivos sem qualquer evidência. Não atribuímos 42/42 PASS nem
homologação geral. O estado das tentativas está no
[registro consolidado](GENIE_SKILLS_RESULTADOS_2026-09-28.md).

## Evidência omitida na primeira estimativa

- O [README forward](../../testes/forward/README.md) registra **39/39 PASS
  históricos** para 13 skills, inclusive EDA, Comentar, Tutor, Auditoria e
  Criar Objeto. Concierge é a única dessas seis sem homologação conversacional
  histórica. O mesmo README manda reabrir conforme name/description, fronteira,
  vocabulário ou path alterados; edição apenas no corpo não invalida tudo.
- A [correção transversal](CORRECOES_TRANSVERSAIS_2026-09-29.md) preservou
  frontmatter/descriptions. No diff atual das seis skills, EDA e Tutor têm
  mudanças no corpo; Comentar, Auditoria, Criar Objeto e Concierge não têm
  diff contra HEAD. Isso não prova identidade com a publicação histórica,
  mas afasta repetir automaticamente P/N/@ por mudanças desta entrega.
- O [ADR-0006](../../decisions/ADR-0006-identidade-hub.md) preserva o
  roteamento automático na renomeação e pede repetir menções. SD já observou
  @ para as oito skills prioritárias; ainda não localizamos prova atual
  equivalente para EDA, Tutor, Comentar e Auditoria. Criar Objeto teve
  [13M PASS no nome atual](../../testes/forward/resultados/2026-09-09_rodada3.md).
- A [prova Free R2](CONTINUACAO_LOCAL_FREE_2026-09-28.md) já registra runtime
  12/12, incluindo `monitor_performance`, e provas separadas de MLflow,
  Delta e materialização FE. Os artefatos locais confirmam esses resultados.
  `SER12 NOT_RUN` em um chat conceitual não significa que o runner nunca
  rodou no Free. Mudanças posteriores exigem regressão do componente afetado,
  não toda a prova executada outra vez pela interface.

## Corrigir a unidade de cobertura

| Objetivo | Evidência aproveitável | Consequência |
|---|---|---|
| Seleção explícita das oito skills prioritárias | SD-*-A com seleção/indicador relatados | Não repetir @ apenas para preencher FG |
| Seleção espontânea | P e outros chats sem @ que carregaram a mesma skill (ex.: FE-PIT, VF-B-D01) | Reutilização limitada ao estímulo e versão; não apaga P que falhou |
| Exclusão em tarefa vizinha | N cujo alvo ficou ausente | A skill ideal não aparecer não é FAIL do critério N básico |
| Qualidade/aderência | Resultado da resposta e contrato aplicável | Falha semântica não invalida retroativamente um roteamento observado |
| Execução do runner/efeito | Testes locais e provas Free com outputs/readback | CLI/Jobs adequados; UI só se o objetivo for o Genie escolher e chamar a rota |

Exemplos: SD-ST-N observou Tutor e não Estatística; isso cobre o negativo
básico de Estatística, mesmo que o oráculo SD preferisse Explainability.
SD-FE-N não exibiu nenhuma skill, portanto não invadiu a tarefa com FE;
persistem a falha de escolha das fontes e a ausência de Cross-EDA. Não
reclassificar esses casos como PASS integral. Em SD-ST-N a ausência de @
não foi confirmada separadamente; não usar esse caso sozinho como positivo
espontâneo certificado do Tutor.

## Próxima etapa proporcional — estimativa de 6 a 11 chats

Esta é uma **estimativa de lote dirigido**, não um teto garantido para
homologação integral. Nenhum novo prompt deve ser pedido só para completar
as 42 fichas. Reavaliar a estimativa se surgirem novos defeitos materiais.

| Grupo | Quantidade planejada | Objetivo e condição |
|---|---:|---|
| EDA, Tutor, Comentar e Auditoria por @ | 4 | Fechar menção no nome atual; combinar EDA/Tutor com as regressões de dados ausentes e intenção versus execução |
| Concierge positivo e @ | 2 | Lacuna de descoberta/seleção sem prova histórica; negativo aproveitar demanda especializada já observada sem Concierge, documentando limite e versão |
| Cross-EDA | até 1 | Retestar confirmação de fonte e uso da rota após correção já publicada; preservar SD-CE-P/FE-N |
| Pipeline Builder | até 1 | Estado UNKNOWN e recuperação sem repetir efeito às cegas; após investigar causa/orientação |
| Baseline | até 1 | Plano versus execução, holdout e alegação de tracking; após triagem/correção |
| Feature Engineering | até 1 | Não inventar finalizador próprio da materialização; separar prova upstream do efeito |
| Safra | até 1 | Maturidade, cobertura e NO_OBSERVATIONS coerentes; fixture autocontida com data de corte |

Os cinco retestes comportamentais não devem repetir o mesmo erro sem hipótese
de correção ou objetivo diagnóstico. O caso negativo Concierge só é dispensado
como novo envio se a ficha de cobertura identificar a observação aplicável;
se a ausência de Concierge não for sustentada, acrescentar um N explícito.
Prompts novos devem ser autocontidos e podem avaliar mais de uma propriedade
coerente na mesma tarefa, sem misturar teste espontâneo com @.

## Limites e gates separados

As falhas materiais não são dispensadas para reduzir custo. Falhas de dados
inventados, uso indevido do holdout, Receipt/finalizador inexistente ou
recuperação destrutiva sem estado conhecido continuam abertas até resolução.
Ressalvas editoriais e falta de execução em pergunta conceitual não geram
automaticamente outro chat.

A campanha congelada VF/CE não foi alterada. A4 de Criar Objeto e a matriz
completa do Concierge têm gates comportamentais próprios; este lote não os
declara concluídos nem os soma à regressão proporcional B1 sem delimitar o
escopo. Se a entrega pretendida passar a ser a certificação integral desses
gates, a estimativa deve incluir seus casos realmente pendentes.

**Triagem local concluída:** [cinco achados e decisões](TRIAGEM_POS_SD_2026-09-29.md).
O prompt FG-EDA-P anterior fica fora da fila automática; pode ser absorvido
por uma regressão EDA com seleção explícita, sem contar isso como teste
espontâneo. O próximo caso é o positivo espontâneo de Concierge 14P.
