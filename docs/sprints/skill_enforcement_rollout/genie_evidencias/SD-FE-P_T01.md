# SD-FE-P/T01 — lag_1 sintético com janela inclusiva — 2026-09-29

(Codex) Resposta literal preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-fe-p/response-original.txt`;
SHA256 `1ad7ddf9c4134e706f3fd865378eb9590ba495a5db2b57a5182dbe5498343e82`.
Versão Free esperada: 657/657 arquivos conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O usuário informou que **não apareceu indicador de carregamento de skill**.
O texto do Genie considerou a pergunta simples e respondeu sem carregar
Feature Engineering. O roteiro previa chat novo sem @.

## Vereditos separados

- Roteamento: **FAIL no oráculo de carregamento espontâneo**. A skill
  esperada para lag e elegibilidade temporal era Feature Engineering; não
  houve indicador segundo o usuário. A regra geral permite responder a
  dúvidas simples sem skill, o que torna plausível a escolha do Genie,
  mas ela não satisfaz o teste de skill enforcement congelado.
- Oráculo: **PASS conceitual**. `lag_1` de 8/jan usa valor `1` de 7/jan;
  disponibilidade em 8/jan é anterior à decisão de 10/jan. A resposta
  identificou a janela inclusiva `[7/jan,10/jan]` para quatro dias e não
  usou evento futuro/indisponível.
- Execução: **NOT_RUN**. A resposta não alegou execução de
  `FIXED_LAG_L1_V1`, payload, runner, Receipt ou verificador. Não há notebook
  exportado nesta coleta. O cálculo textual correto não certifica o perfil.

**Veredito T01: PASS do cálculo conceitual, FAIL de roteamento pelo oráculo.**
Sem edição de produto/publicação por esta coleta; a instrução geral sobre
dúvidas simples explica a ambiguidade de roteamento e T01 fica preservado.
