# Triagem após as 37 primeiras rodadas SD — 2026-09-29

(Codex) A revisão de suficiência reduziu a fila manual. Esta triagem confere
as cinco respostas materiais citadas na [reconciliação](RECONCILIACAO_SD_FG_2026-09-29.md)
contra as instruções publicadas. Ela não altera as respostas originais nem
transforma comportamento observado em defeito comprovado de código.

| Achado | Regra já existente | Decisão |
|---|---|---|
| SD-CE-P e SD-FE-N: Cross-EDA ausente; no segundo, fontes inferidas | Cross-EDA exige confirmar fontes/chave; instrução global publicada depois restringe dispensa de skill quando há notebook/execução e impede prosseguir após pergunta material pendente | Reteste espontâneo dirigido após a mudança já publicada; não repetir duas vezes o mesmo objetivo |
| SD-PB-DELTA: estado remoto presumido e limpeza repetida | Pipeline Builder já define `UNKNOWN` e inspeção do destino sem repetir escrita | Falha da resposta; prompt conceitual não nomeou pipeline e a instrução global permite dispensar skill em dúvida curta. Não editar description por este caso isolado; um reteste com skill selecionada separaria seleção de aderência |
| SD-BL-B/P: holdout oferecido para seleção e planejamento virou execução | Baseline já reserva holdout para avaliação final; reforço plano versus execução foi publicado após SD-BL-P | Preservar ambas as falhas; reteste só se a aderência comportamental for gate, com pedido autocontido e sem criar dados |
| SD-FE-MAT: finalizador/campo inventados para materialização | FE nomeia `effect_request` e `execute`, e o registro de efeito é separado da prova PIT upstream; o script não tem `finalize`/`verify` próprios | Falha de orientação; não foi defeito demonstrado do executor. Reteste focal se persistir depois de fornecer contexto fechado |
| SD-VF-A: `NO_OBSERVATIONS` citado com uma observação | Safra define zero observações para esse estado e distingue cobertura de maturidade por data de corte | Núcleo do pedido passou; ressalva permanece. Reteste somente com fixture/corte que exija classificar formalmente os estados |

Os [relatórios Free R2](CONTINUACAO_LOCAL_FREE_2026-09-28.md) já exercitam
os perfis sintéticos no runtime, inclusive SER12, MLflow, Delta e FE.
Perguntas conceituais sem execução no Genie não apagam essas provas. Nenhum
novo teste local ou publicação é necessário antes da próxima coleta de
roteamento. Alteração de produto fica condicionada à causa reproduzida;
reteste só terá valor se diferenciar hipóteses ou verificar correção.

**Próximo caso humano:** positivo espontâneo de Concierge (`14P` do
[roteiro forward](../../testes/forward/roteiro.md)), primeiro caso sem
histórico Genie. A primeira mensagem mede roteamento; o Codex registra a
resposta externamente, dispensando a segunda mensagem de registro no mesmo
chat. O prompt exato está no
[roteiro guiado](GENIE_RODADAS_GUIADAS_2026-09-29.md).
