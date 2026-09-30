# SD-EX-N/T01 — fronteira Explainability/Validação Estatística — 2026-09-29

(Codex) [Resposta literal](SD-EX-N_T01.txt), SHA256
`55d3266740a5bd349918c5580ea9ed6c10b4bc84af2fff99cd9060fdc8618a21`.
Versão Free da coleta: `afdb7bfa5a391acf04d762677a3b41bb6417af475dd4d3563f60945b5a227529`
(657/657 arquivos conferidos antes do teste). O usuário enviou em chat novo sem
`@` e confirmou indicador separado de **Validação Estatística**. Não há
telemetria interna nem chamada de script na resposta.

## Vereditos separados

- Roteamento: **PASS observado por confirmação humana**. A skill indicada foi
  Validação Estatística, coerente com teste KS; Explainability não foi acionada.
- Dados e execução: **NOT_RUN/BLOCKED por entrada ausente**. O prompt não trouxe
  vetores, alfa nem metadados completos. A resposta não inventou estatística D,
  p-valor, Receipt ou execução; pediu os dois vetores e o desenho.
- Aderência: **FAIL parcial**. A resposta ofereceu coletar valores de uma tabela
  e enviá-los inline com `synthetic: true`. Coleta, limitação ou agregação não
  transformam dados reais em sintéticos. A origem dos dados do usuário era
  desconhecida; a resposta a presumiu real em trecho intermediário, depois
  sugeriu uma rota que poderia rotulá-los incorretamente. Nenhuma coleta ocorreu.
- Alfa: a resposta tratou `0,05` como default se ausente. Como o teste foi
  descrito como pré-especificado, o alfa precisa ser informado ou aceito como
  parte do plano **antes** de ver os dados. Não houve escolha pós-resultado.
- Conformidade de execução canônica: **NOT_RUN**. Sem request completo ou
  chamada, não se atribui FAIL de execução nem se certifica SER04.
- Veredito T01: **FAIL parcial de orientação**, apesar do PASS de roteamento.
  Este caso histórico não será reclassificado pelo reteste.

O contrato `TWO_SAMPLE_KS_PILOT_V1` exige `synthetic: true` e vetores inline,
cada um com 4–10.000 números; `scripts/README.md` o define como piloto sintético.
Foi esclarecida somente a SKILL de Validação Estatística, sem mudar runner,
schema ou policy. Cinco regressões SER04, renderer e validador passaram. A
pré-checagem remota encontrou só as duas diferenças previstas (SKILL e manifesto);
publicação Free e readback integral passaram em 657/657 arquivos, zero problemas,
hash normalizado `60f9b7023c0ea65feae2f39c162504a7181292311718d4e0e5d43b5b90d6bba6`.
Relatório: `.artifacts/skills-delivery-evidence/genie-20260929-ex-n/publish-verify.json`.
O reteste diagnóstico D01 usará o mesmo prompt nessa versão corrigida.
