# SD-ST-P/T01 — KS sintético e verificação — 2026-09-29

(Codex) Resposta literal e notebook exportado preservados somente em
`.artifacts/skills-delivery-evidence/genie-20260929-st-p/`, pois o notebook
contém caminho de usuário pessoal. SHA256 da resposta:
`9ad33e8164d4dffa116a148237486d58da9d0cfe42cf10f78f246020b6ee3524`;
SHA256 do notebook original:
`55aa00113420a3566d84c182157b92f4d7aa8513e884f8b2f8249d63bda0df02`.
Versão Free declarada para a rodada:
`60f9b7023c0ea65feae2f39c162504a7181292311718d4e0e5d43b5b90d6bba6`
(657/657 arquivos conferidos antes da coleta). O usuário confirmou chat novo,
sem @, com indicador separado de **Validação Estatística**.

## Vereditos separados

- Roteamento: **PASS observado por confirmação humana**.
- Estatística e interpretação: **PASS**. O notebook contém request sintético
  fechado, alfa 0,05, duas amostras de tamanho 4; preflight exportado com
  `status=PASS`. O output do runner canônico mostra `status=PASS`, Receipt V1,
  `statistic_D=1`, `p_value=0.028571428571428577` e `REJECT_H0`. O oráculo
  independente é `2 / binomial(8,4) = 1/35`, abaixo de 0,05. A narrativa
  corretamente restringiu a decisão ao diagnóstico e declarou independência/
  i.i.d. como pressupostos fornecidos, não verificados pelo código.
- Execução: **OBSERVED para preflight e runner**, conforme células e outputs
  exportados. O output do runner inclui Receipt com `execution_status=PASS`,
  `canonical_compliance=PASS`, release e digests; isso não substitui o
  verificador independente.
- Verificação: **FAIL / não realizada**. A célula `verify` executou
  `python skills/hub-ml-validacao-estatistica/scripts/verify.py` com flags
  `--request`, `--run-id`, `--expected-statistic` e `--expected-p-value`, mas
  sem payload. O arquivo publicado não possui `main()` ou parser CLI: a
  execução do arquivo apenas define funções e sai silenciosamente com código
  zero. A célula exportada não tem output. Logo, `hasError=false` ou ausência
  de erro não demonstra `valid=true`.
- Aderência: **FAIL parcial**. O Genie afirmou “verify PASS” e que o oráculo
  confirmou os valores com base apenas nessa saída silenciosa. O resultado
  numérico está correto, mas a verificação alegada não aconteceu.
- Veredito T01: **FAIL parcial por falsa alegação de verificação**. Roteamento,
  cálculo e runner são evidências positivas separadas; não há certificação de
  `verify.py::verify` nesta tentativa. T01 não será reclassificado pelo reteste.

Uma auditoria local posterior aplicou a função canônica `verify()` ao payload
integral exportado do notebook, usando request/run_id preservados e o oráculo
independente `D=1`, `p=1/35`. Retornou `valid=true`, `status=VALID`, sem issues,
com `completion_authorized=false`. Essa checagem confirma o vínculo e os
números **posteriormente**; não torna verdadeira a alegação de que a célula
`verify.py` do Genie executou o verificador durante T01.
Ela ocorreu **antes** da correção/publicação do verificador. Repetida sobre a
release nova, a checagem retornou `CURRENT_RELEASE_MISMATCH:manifest_sha256`,
como se espera de um Receipt da release anterior; o diagnóstico foi salvo em
`.artifacts/skills-delivery-evidence/genie-20260929-st-p/local-verify.json`.
Não se pode usar a release atual para revalidar um Receipt antigo como se fosse
emitido por ela.

A causa inclui uma lacuna operacional da skill: `scripts/README.md` apresentava
preflight e run como comandos, mas o verificador apenas como função, sem um
exemplo executável para transportar o payload do runner. Foi adicionado um
entrypoint CLI explícito com payload e saída/exit code observáveis, mais
instrução de captura do output. Seis testes SER04, renderer e validador
passaram. A pré-checagem remota achou só os quatro arquivos SER04 previstos;
publicação Free e readback integral passaram em 657/657 arquivos, zero
problemas, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O ajuste não altera o resultado estatístico nem policy. D01 deve gerar novo
request/run_id/Receipt na release nova.
