# SD-BL-N/T01 — queda de AUC em modelo implantado — 2026-09-29

(Codex) Resposta literal preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-bl-n/response-original.txt`;
SHA256 `4c911030582c70c1fe4bb3b9de39ac7c605ad833e202462a4049a7401fa55ac3`.
Versão Free esperada: 657/657 arquivos conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O usuário informou indicador de `hub-ml-monitoramento-modelo` carregada.
O roteiro previa chat novo sem @; isso não foi confirmado separadamente.

## Vereditos separados

- Roteamento: **PASS por relato humano**. Monitoramento, não Baseline ML,
  foi escolhido para verificar desempenho de modelo já implantado.
- Coleta de requisitos: **PASS parcial**. A resposta pediu origem, colunas
  de score/label, duas janelas disjuntas, maturidade de labels, modelo/versão
  e política de severidade. Não inventou AUC, delta, queda, execução ou
  Receipt. Disse corretamente que sem limiar aprovado pode reportar delta
  sem classificar severidade.
- Limite do perfil: **FAIL parcial de orientação**. SER12
  `BINARY_MATURE_PERFORMANCE_V1` é uma rota **sintética local**. O usuário
  descreveu modelo implantado e não declarou que as linhas fossem
  sintéticas. A resposta pediu tabela/view de previsões e labels e prometeu
  montar o request e executar a rota, sem separar dados reais da fixture
  permitida nem confirmar origem sintética antes de `synthetic: true`.
  Dados de produção não podem ser reclassificados para caber nesse piloto.
- Escopo do finalizador: a resposta descreveu preflight → run → verify e
  Receipt, mas omitiu `finalize`/`verify_finalized`, exigidos pela SKILL para
  encerrar o diagnóstico local SER12. Nenhuma etapa foi executada aqui.
- Execução: **NOT_RUN**; não há dados, cálculo, notebook, payload ou
  verificação nesta rodada.

**Veredito T01: PASS de roteamento e recusa de inventar métricas, FAIL
parcial de orientação do perfil sintético/finalizador.** A skill já nomeia
o perfil sintético e o finalizador obrigatório. Nenhuma edição de
produto/publicação foi feita por esta coleta.
