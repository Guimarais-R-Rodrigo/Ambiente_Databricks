# SD-BL-P/T01 — baseline temporal sintético e feature derivada do alvo — 2026-09-29

> **Errata de auditoria transversal (Codex, 2026-09-29):** a classificação
> abaixo de `X` gerado condicionalmente a `Y` como leakage automático foi
> incorreta. Em uma simulação sintética, amostrar `X|Y` pode definir uma
> distribuição conjunta legítima; a ordem do gerador não demonstra que o
> valor de `Y` estaria disponível como feature na decisão real. O notebook
> continua demonstrando apenas o resultado da fixture criada pelo Genie,
> não generalização ou ausência de leakage operacional. Mantêm-se como
> achados o desvio de “planeje” para execução, entradas inventadas para a
> demonstração e a inferência de pior calibração a partir de 3 observações
> no holdout. Veredito revisado: **PASS técnico do request sintético gerado,
> FAIL parcial de aderência ao pedido e interpretação**, sem afirmar target
> leakage comprovado. O texto original é preservado abaixo como histórico
> da primeira análise, agora supersedida neste ponto.

(Codex) Resposta literal e notebook exportado preservados somente em
`.artifacts/skills-delivery-evidence/genie-20260929-bl-p/`, pois o notebook
contém caminho pessoal. SHA256 da resposta:
`1bad01f21606d3793f4ba8148e816366b687b359d5678f76411bf0158f9c8831`;
SHA256 do notebook:
`7bce29ad10eaf5c91b26548ec50581dc3c72658af69126f41a091e8e3f8cc9b5`.
Versão Free esperada: 657/657 arquivos conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O usuário informou indicador de `hub-ml-baseline-ml` carregada.

## Vereditos separados

- Roteamento: **PASS por relato humano**.
- Split e processamento: **PASS no request gerado**. O código criou 12
  meses, partições cronológicas de 6/3/3 observações, ambas as classes em
  cada partição, e chamou `preflight`, `run` e `verify` da skill. Os outputs
  exportados mostram preflight/run `PASS`, `Verify: VALID (valid=True)`,
  scaler e métricas. O contrato `BINARY_TEMPORAL_LOCAL_V1` confere os
  bindings do split, do scaler treino-only e do Receipt para **esse request**.
- Proveniência de entrada: **FAIL material**. O prompt pediu planejar com
  doze meses sintéticos rotulados, mas não forneceu linhas, features nem
  rótulos. O Genie os gerou e, no notebook, criou cada feature com
  `mu = 1.0 if target == 1 else -1.0`, isto é, condicionou o preditor ao
  próprio alvo. Esse mecanismo de geração introduz informação do rótulo
  na feature. O AUC 1,0 do holdout é uma propriedade da fixture fabricada,
  não evidência de generalização sem leakage para um baseline de decisão.
- Escopo da execução: **OBSERVED no notebook exportado para o request
  construído pelo Genie**, não para dados fornecidos pelo usuário. O output
  do verificador foi `VALID`, mas o notebook não serializou o payload nem
  imprimiu `run_id`/Receipt completos para auditoria independente posterior.
  O status atesta apenas o escopo do verificador, não aprovação da
  construção da feature ou prontidão do modelo.
- Interpretação: **FAIL parcial**. A resposta afirmou split “sem leakage”,
  ignorando o alvo usado na geração da feature. A elevação de Brier de
  treino para holdout, com apenas 6/3 observações e feature alvo-condicionada,
  não prova pior calibração nem que tal padrão era esperado.
- Desvio do pedido: o verbo era “planeje”; o Genie executou um experimento
  sintético adicional. A execução é observável, mas não substitui o plano
  solicitado nem autoriza aplicar os números a uma base real.

**Veredito T01: FAIL analítico/de aderência**, embora a rota local tenha
retornado `VALID` para a fixture criada. A skill já exclui construção de
features do escopo do baseline e orienta split sem leakage; nenhum ajuste de
produto/publicação foi feito por esta coleta. O achado deve orientar reteste
ou correção comportamental preservando T01.
