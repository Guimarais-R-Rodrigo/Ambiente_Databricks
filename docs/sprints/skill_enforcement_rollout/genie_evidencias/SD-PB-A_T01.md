# SD-PB-A/T01 — MERGE relatado sem readback e cleanup — 2026-09-29

(Codex) Resposta original preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-pb-a/response-original.txt`;
SHA-256 `9d5d5aeac821056bd6999281ee4e778380e4b590484e0cfbf4a7c585a04ee439`.
Versão Free esperada: 657/657 conteúdos conferidos, hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O usuário confirmou seleção de `@hub-ml-pipeline-builder` e indicador
separado de carregamento da skill.
Nenhum notebook/export de execução foi fornecido nesta coleta; o cabeçalho
de notebook aparece somente no texto colado.

## Vereditos separados

- Roteamento: **PASS por seleção @ e indicador relatados pelo usuário**.
- Fronteira de efeito: **PASS na recusa**. A resposta disse corretamente que
  o sucesso relatado do MERGE não comprova linhas gravadas, replay
  idempotente ou remoção da tabela. Não declarou o efeito concluído.
- Contrato: **PASS parcial**. Identificou readback, replay e `DROP_OWNED`,
  mas não pediu explicitamente o effect record, o destino/owner verificado,
  nem o status de cleanup para classificar o estado já existente. O Receipt
  de cálculo não é prova de escrita Delta.
- Recuperação: **FAIL material de orientação**. A resposta recomendou
  “reexecutar pelo `run_delta.py`” caso o MERGE tenha ocorrido fora do
  runner. Com readback e cleanup desconhecidos, pode já haver estado remoto
  parcial; o [SKILL.md](../../../../ambiente_fonte/.assistant/skills/hub-ml-pipeline-builder/SKILL.md)
  exige inspecionar o destino em estado `UNKNOWN`, **sem repetir a escrita**.
  A orientação correta é localizar o destino/registro de efeito e verificar
  estado, ownership, linhas e cleanup antes de qualquer nova ação.
- Execução atual: **NOT_RUN/NOT_OBSERVABLE**. Nenhum run, Receipt, readback,
  effect record ou cleanup foi executado ou fornecido nesta rodada. O
  “sucesso” do MERGE é parte do cenário relatado, não prova independente.

**Veredito T01: PASS de roteamento e recusa de conclusão, FAIL de recuperação
segura.** A skill já contém
explicitamente a regra para `UNKNOWN`; preservar a falha histórica e fazer
reteste focal posterior se necessário. Nenhuma edição de produto/publicação
foi feita por esta coleta.
