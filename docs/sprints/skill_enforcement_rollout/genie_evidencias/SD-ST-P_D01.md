# SD-ST-P-D01 — KS sintético com verificador explícito — 2026-09-29

(Codex) Resposta literal e notebook exportado preservados somente em
`.artifacts/skills-delivery-evidence/genie-20260929-st-p-d01/`, pois o notebook
contém caminho pessoal. SHA256 da resposta:
`815a7aaab73736d47556192b138a4523289e44dda2e9745181b6b662381847ba`;
SHA256 do notebook:
`8103ffe33ad7a417ba4abbf08cfe64e0611e69d16609f8357dfa0de04fea5f24`.
Release Free conferida antes da coleta: 657/657 arquivos, zero problemas, hash
normalizado `7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O usuário confirmou chat novo sem @ e indicador separado de **Validação Estatística**.

## Vereditos separados

- Roteamento: **PASS observado por confirmação humana**.
- Cálculo e decisão: **PASS**. Para as duas amostras de quatro valores sem
  empates, `D=1`, `p=0.028571428571428577=1/35`; rejeitar H0 a alfa 0,05.
  Oráculo independente: duas de `C(8,4)=70` rotulações têm separação máxima.
  Independência/i.i.d. permanecem pressupostos declarados, não comprovados
  pelo código.
- Execução: **PASS na evidência exportada**. O notebook contém chamadas
  explícitas a `preflight.py` e `run.py`, ambas com stdout `status=PASS`.
  O runner gerou Receipt V1 `er1:b99fb5cd4b1b5ca141c27234d51dc616ba6821b13f4232bc634b99eade1bc118`
  com manifesto `727bc6acf816af812f8560244ff2ce69ab88a65335215446e41ed74d58742820`.
- Verificação: **PASS na evidência exportada**. A célula salva o JSON exato do
  runner em `/tmp/ks_run.json` e chama `verify.py --payload` com esse arquivo,
  `--request`, `--run-id SER04-DEMO-001` e oráculo independente `D=1`, `p=1/35`.
  O output mostra `status=VALID`, `valid=true`, `issues=[]` e exit code 0.
  Auditoria local reextraiu request/payload do notebook e executou novamente
  apenas o verificador da release atual: `VALID`, sem issues; hash do manifesto
  coincidiu com o Receipt.
- Escopo: `completion_authorized=false` e `promotion_authorized=false` foram
  preservados. O PASS cobre esta fixture e execução exportada, não homologação
  geral nem leitura remota posterior de `/tmp`. A célula imprime o exit code
  do verificador sem `assert`, mas o valor efetivamente exportado é zero.

**Veredito D01: PASS.** T01 continua FAIL histórico por falsa alegação de
verificação na release antiga; D01 não o reclassifica. Nenhuma mudança de
produto ou nova publicação foi feita por esta coleta.
