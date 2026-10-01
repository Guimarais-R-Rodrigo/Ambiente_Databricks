# RQ-VF-DENOM-D02 — Safra, denominador em célula incompleta

(Codex) Resposta recebida em 2026-10-01. [Texto integral colado pelo usuário](RQ-VF-DENOM-D02_resposta.txt), SHA-256
`0ecad99cc5cb77afab1fc928cf4bfc57cb2202814c9f353666cf1aa1c6e37c10`.
O texto colado reproduz o prompt e a resposta da Genie; não é export da
interface, log de ferramentas nem prova dos bytes de skill efetivamente lidos.
O usuário informou que houve **indicador separado de chamada de Safra**.
A seleção efetiva no menu `@` não foi confirmada separadamente nesta rodada.

## Oráculo e observação

O prompt repete o cenário de
[SD-VF-STATUS-D01](SD-VF-STATUS-D01.md): safra janeiro/2026, roster fixo
`{a,b}`, corte 31/mar/2026, MOB0 2/2, MOB1 0/2, MOB2 1/2 e MOB3 ainda
imatura. O alvo binário cumulativo foi descrito sem valores 0/1. O oráculo
é `MATURE/COMPLETE`, `MATURE/NO_OBSERVATIONS`, `MATURE/INCOMPLETE` e
`IMMATURE/IMMATURE`, respectivamente. Só MOB0 é estruturalmente elegível
à taxa final; sem alvo, nenhuma taxa numérica pode ser calculada.

A resposta correspondeu aos quatro pares de status, manteve o denominador
fixo 2 e deixou todas as taxas indefinidas. Em MOB2, explicou que `1/2`
descreve cobertura e que nem mesmo um valor conhecido para `a` permitiria
taxa sobre o subconjunto observado. Não ofereceu taxa provisória com
denominador 1, não inventou alvo nem causa para a falta em MOB1.

## Vereditos separados

| Dimensão | Estado | Evidência e limite |
|---|---|---|
| Carregamento | OBSERVADO por relato humano | Indicador separado informado pelo usuário; o prefixo textual, sozinho, não provaria carregamento |
| Maturidade e cobertura | PASS conceitual | Quatro pares de status e contagens observadas coincidem com o oráculo |
| Denominador e taxa | PASS focal | Roster 2 preservado; MOB2 1/2 é cobertura, sem taxa final ou provisória; MOB0 carece de alvo |
| Execução canônica | NOT_RUN | Resposta diz ser conceitual; não há outputs de preflight, runner, Receipt ou verificador |
| Identidade de bytes consumidos | NOT_OBSERVABLE | Readback Free prova conteúdo remoto publicado, não o conteúdo lido pela Genie nesta sessão |

A frase sobre o helper deixar `taxa_acumulada` ausente em MOB0 sem valores
0/1 é uma descrição contratual, não output do helper. Entrada sem alvo não
foi submetida ao preflight, portanto não se registra uma linha executada
para MOB0. Isso não altera o acerto do oráculo conceitual.

**Resultado:** o FAIL parcial de denominador no D01 foi corrigido neste
reteste focal, depois da mudança de `SKILL.md` e readback no Free. O D01
permanece histórico. Este PASS não homologa a execução da rota de Safra,
não promove policy e não atesta as demais skills.
