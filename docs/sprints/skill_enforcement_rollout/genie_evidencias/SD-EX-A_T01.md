# SD-EX-A/T01 — verificação de Explainability — 2026-09-29

(Codex) [Resposta literal](SD-EX-A_T01.txt), SHA256
`616d3bfc8f85c86636bb321887b9d007ddba75c8bc197ef2de0bacde05e81ac0`;
cópia privada em `.artifacts/skills-delivery-evidence/genie-20260929-explainability-a/`.
Versão Free esperada:
`1ac2e49e2411ccd448dd050b9b2d8afb646489e81ecc665d4f33ea028404fabc`.
O usuário confirmou escolha de `hub-ml-explainability` na lista do menu @ e
indicador separado de carregamento. Bytes internos carregados não foram
inspecionados; o prefixo textual sozinho não provaria o evento da interface.

## Vereditos separados

- Roteamento: **PASS observado na interface** por confirmação humana da
  seleção real no menu @ e do indicador separado.
- Oráculo simbólico: **PASS**. O prompt não fornece intercepto/coeficientes
  numéricos neste chat; a resposta preservou símbolos. Para fundo `(0,0)` e
  observação `(2,1)`, base `β₀`, contribuições `(2β₁,β₂)` e predição
  `β₀+2β₁+β₂` estão corretas.
- Descrição da rota: preflight, vinculação de pedido/modelo/arrays, oráculo
  analítico e Receipt foram descritos em essência. A comparação numérica do
  verificador usa tolerâncias relativa e absoluta de `1e-10`; “igualar
  exatamente” é impreciso se lido como igualdade de ponto flutuante.
- Orientação de conclusão: **FAIL**. A resposta disse que só com `valid=true`
  **e** `completion_authorized` poderia afirmar valores verificados. O
  `scripts/verify.py` retorna `completion_authorized=false` incondicionalmente,
  inclusive com `valid=true`. A skill exige apenas `valid=true` para afirmar
  valores verificados no escopo restrito; a conclusão da entrega e promoção
  continuam não autorizadas.
- Execução: **NOT_RUN**. O Genie descreveu o procedimento, sem payload,
  chamada, saída do verificador ou Receipt observado. O pedido “Como checar”
  não exigia execução; ausência dela não é falha por si.
- Veredito T01: **FAIL parcial de orientação canônica**; matemática PASS.
  O PASS de roteamento não corrige a falha na orientação canônica.

Auditoria independente confirmou o retorno do verificador e a correção
matemática. A instrução de Explainability foi esclarecida para distinguir
`valid=true` do campo de autorização de conclusão; scripts e helper não foram
alterados. Reteste pertence a nova versão após publicação conferida; este
resultado histórico permanece FAIL. Nove regressões de Explainability PASS;
renderer e validador PASS. Pré-checagem remota encontrou só a diferença
prevista em `SKILL.md`; plano → publicação → readback integral PASS em 657/657
arquivos, zero erros, hash normalizado
`afdb7bfa5a391acf04d762677a3b41bb6417af475dd4d3563f60945b5a227529`.
Evidência `.artifacts/skills-delivery-evidence/genie-20260929-explainability-a/publish-verify.json`.
