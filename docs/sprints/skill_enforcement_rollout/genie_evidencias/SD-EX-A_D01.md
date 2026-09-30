# SD-EX-A-D01 — reteste do verificador de Explainability — 2026-09-29

(Codex) [Resposta literal](SD-EX-A_D01.txt), SHA256
`c84fef36b5ae7b94f663592609ba028acfea33b7280c5a9a34e9fa1d79f68712`;
cópia privada em `.artifacts/skills-delivery-evidence/genie-20260929-explainability-a-d01/`.
Versão Free esperada:
`afdb7bfa5a391acf04d762677a3b41bb6417af475dd4d3563f60945b5a227529`
(657/657 arquivos conferidos antes desta coleta). O usuário confirmou chamada
com @ e carregamento da skill; bytes internos não foram inspecionados.

## Vereditos separados

- Roteamento: **PASS observado por confirmação humana** da seleção @ e do
  carregamento da skill.
- Oráculo e procedência: **PASS**. A resposta identificou o fixture
  `tests/linear_fixture.json`, que contém intercepto 3, coeficientes `(2,-1)`,
  fundo `(0,0)` e amostra `(2,1)`. Esses números vêm do fixture consultado,
  não do texto literal do prompt D01. Base 3, contribuições `(4,-1)` e
  predição 6 conferem. A fórmula simbólica para o fundo de uma linha também
  está correta.
- Semântica do verificador: **PASS** no achado que motivou D01.
  `valid=true` permite afirmar valores verificados somente no escopo do
  verificador; `completion_authorized=false` e `promotion_authorized=false`
  permanecem distintos e não homologam a entrega. A resposta já não exige
  `completion_authorized=true` como condição impossível.
- Descrição de checks: essencialmente correta. A lista resumida não cita a
  checagem explícita `PREFLIGHT_BINDING_MISMATCH` do `verify.py`, embora a
  explicação anterior mencione preflight. Não afeta o oráculo nem a conclusão.
- Execução: **NOT_RUN**. A resposta descreve como chamar preflight, runner e
  verificador e oferece executar depois; não mostra chamada, payload, Receipt
  ou resultado `valid=true` observado nesta rodada.
- Veredito D01: **PASS do diagnóstico conceitual de verificação**, com
  execução canônica NOT_RUN. T01 conserva FAIL histórico. D01 está fora dos 37
  casos SD e não certifica o perfil executável nem homologação geral.

Nenhuma edição de produto ou publicação decorre deste reteste. Próximo caso
guiado: `SD-EX-N`, para checar a fronteira com Validação Estatística.
