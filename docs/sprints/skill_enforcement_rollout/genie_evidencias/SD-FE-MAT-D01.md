# SD-FE-MAT-D01 — efeito Delta `UNKNOWN` — 2026-09-30

(Codex) Prompt e primeira resposta preservados em
`.artifacts/skills-delivery-evidence/genie-20260930-fe-d01/response-original.txt`;
SHA-256 `ac24a00233748b77773485f87b1873f70bedaf22366903e7929fe2ad54cba501`.
O usuário informou chat novo sem @. Informou que o Genie leu Feature
Engineering, mas confirmou que o único indicador separado exibiu
**Baseline ML**; Feature Engineering não apareceu. O
[T01](SD-FE-MAT_T01.md) permanece como tentativa histórica distinta.

## Versão e efeito observado

A versão remota efetiva após publicação paralela de micromodelos não foi
conferida nesta coleta. O registro de efeito, o readback e a prova PIT são
premissas do prompt, não outputs anexados. Não há chamada de ferramenta,
notebook executado, Receipt ou inspeção do catálogo na transcrição:
**execução NOT_RUN nesta rodada**.

## Vereditos separados

- Roteamento: **FAIL para Feature Engineering** pelo indicador apenas de
  Baseline ML em chat sem @. O texto do Genie diz que consultaria Feature
  Engineering e conhece os entrypoints; isso não prova carregamento da skill
  na interface.
- Fronteira de efeito: **PASS no núcleo**. Separou a prova PIT upstream do
  efeito Delta, recusou concluir materialização com `status=UNKNOWN` e
  `table_absent_after_cleanup=null`, pediu inspeção humana do destino e
  ownership sem retry automático.
- Entrypoints: **PASS**. Citou `scripts/run_pit_materialization.py::effect_request`
  e `::execute`; não inventou `verify`, finalizador nem
  `completion.authorized` para essa rota. A rota de composição PIT upstream
  tem verificação própria, distinta do efeito de materialização.
- Precisão da evidência: **FAIL parcial**. O cenário informa readback de três
  linhas, mas não schema/colunas; a resposta afirmou que as cinco colunas
  esperadas foram observadas. Também chamou a escrita de “parcial” sem saber
  seu alcance. `BLOCKED_OWNERSHIP_OR_DROP_UNKNOWN` é disjuntivo: não prova que
  a checagem de ownership especificamente falhou. O destino
  `workspace.default.skills_delivery_<32 hex>` é padrão contratual, não nome
  efetivo fornecido neste caso.

**Veredito D01: PASS da decisão central e correção do finalizador inventado em
T01; FAIL parcial de precisão e FAIL de roteamento espontâneo FE.** Não homologa
materialização nem prova o estado remoto da tabela. Não houve edição de
produto, execução remota ou publicação por esta coleta.
