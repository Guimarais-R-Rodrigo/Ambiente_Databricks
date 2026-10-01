# RQ-PB-RECOVERY/T03 — reconciliação de efeito Delta incerto

(Codex) Resposta recebida em 2026-10-01 após o esclarecimento de recuperação
do Pipeline Builder publicado no Free. [Texto integral colado pelo usuário](RQ-PB-RECOVERY_T03_resposta.txt),
SHA-256 `af8c13eb46ca14412719106b932faefed2f0149c2a33bd7ac9af76c23101e7d7`.
O usuário confirmou seleção de `hub-ml-pipeline-builder` no menu `@` e
**indicador separado de carregamento**. O texto menciona leitura de skill,
contrato e script, mas não inclui outputs de chamadas de ferramenta. O
indicador não identifica os bytes exatos lidos nem prova execução do runner.

## Oráculo e resultado

O mesmo cenário de [T02](RQ-PB-RECOVERY_T02.md) relata sucesso de MERGE
sem destino exato, effect record, readback, posse ou estado de limpeza.
O oráculo separa relato não verificado, efeito persistido `UNKNOWN` e
limpeza `UNKNOWN`; recusa retry como prova retroativa. A primeira sequência
segura recupera destino, registro de efeito e autorização do run original,
mantém `UNKNOWN` se não houver como recuperá-los, e só então faz inspeção
somente leitura de existência, conteúdo, posse e limpeza. Marcadores de
posse não autorizam novo `DROP`.

A resposta recusou conclusão e retry, apresentou os três estados
separadamente e ordenou a recuperação de destino/registro/autorização antes
da inspeção. Condicionou qualquer limpeza futura à autoridade explícita
aplicável ao destino e efeito. Não afirmou que o MERGE ou o DROP foram
observados nesta rodada, nem presumiu estado físico atual.

| Dimensão | Veredito | Evidência e limite |
|---|---|---|
| Roteamento @ | PASS por relato humano | Seleção no menu e indicador separados confirmados pelo usuário |
| Relato e estados | PASS conceitual | Sucesso não verificado; persistência e limpeza `UNKNOWN` |
| Retry e reconciliação | PASS focal | Novo `run_delta.py` não comprova efeito anterior; recuperar identidade e autoridade antes de inspecionar ou decidir |
| Autoridade de limpeza | PASS focal | Posse isolada não autoriza `DROP`; exige autoridade específica recuperada e conferida |
| Precisão de escopo | RESSALVA | O exemplo `workspace.default.skills_delivery_<32hex>` é o padrão do probe contratado, mas o relato inicial não prova que o efeito veio desse perfil; tratá-lo como padrão esperado, não destino observado |
| Execução/efeito nesta rodada | NOT_RUN | Pedido era conceitual; nenhum effect record, readback, Receipt ou output de executor foi fornecido |

**Resultado:** PASS conceitual focal da sequência de recuperação na versão
posterior à correção. O [FAIL material anterior](SD-PB-A_T01.md) e as
ressalvas de [T02](RQ-PB-RECOVERY_T02.md) continuam históricos. O reteste
não homologa a rota executável Delta, a especificação PB-P ou a skill inteira;
não autoriza promoção de policy, Ready, merge ou escrita remota.
