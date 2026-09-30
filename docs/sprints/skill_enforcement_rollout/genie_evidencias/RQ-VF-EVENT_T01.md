# RQ-VF-EVENT/T01 — Safra, eventos mensais

(Codex) Coleta recebida em 2026-09-30. [Texto integral colado pelo usuário](RQ-VF-EVENT_T01_resposta.txt), SHA-256
`d346b624ac07e31f46047cdcc7ab176aff1fb2ce7ee32554cc66145b7422fb9f`.
O arquivo contém o texto que o usuário colou, inclusive uma linha inicial de
interface `hub-ml-analise-safra se-safra` e a análise textual da Genie; não é
export da interface nem prova de quais bytes de SKILL.md foram carregados.
O usuário informou **indicador separado de carregamento de Safra**.

## Veredito por dimensão

| Dimensão | Estado | Evidência e limite |
|---|---|---|
| Seleção/carregamento | OBSERVADO por relato humano | Indicador separado de `hub-ml-analise-safra`; o prefixo colado isoladamente não provaria carregamento |
| Semântica EVENT | PASS conceitual | Máximo progressivo por contrato; fevereiro/MOB1 tem evento mensal 0/2 e incidência acumulada 1/2 |
| Denominador e ausência | PASS neste caso | Roster 2 fixo; janeiro/MOB2 tem a1 observado, a2 ausente e nenhuma taxa final; rejeita 1/1 e ausência=0 |
| Maturidade | PASS conceitual | Sem data de corte, status formal fica pendente; não chama MOB2 de maduro/INCOMPLETE |
| Execução/efeito | NOT_RUN | Resposta rotula contas como ilustrativas e não mostra runner, Receipt, verificador, escrita ou tabela |

A resposta usa `Calculada (2/2)` no resumo das células completas, mas enquadra
explicitamente essas contas como ilustrações, sem afirmar execução canônica.
Ela menciona um `input.schema.json` e `run_id` futuros; isso é orientação,
não evidência de que a rota tenha sido executada. O oráculo desta rodada é
conceitual, não exige output de runner.

**Resultado:** PASS da lacuna de alvo EVENT para esta fixture, com indicador
separado relatado; execução canônica permanece `NOT_RUN`. O [FAIL parcial de denominador no
SD-VF-STATUS-D01](SD-VF-STATUS-D01.md) e as falhas anteriores de Safra
continuam abertos, pois esta resposta não é reteste do mesmo estímulo nem
houve mudança de produto. Não promove G6 histórico, policy ou homologação
integral da skill.
