# PR #117 — ficha de revisão e aceite parcial B1

(Codex) Retrato em 2026-09-30 do produto no PR #117 em rascunho, commit `9b845549`,
empilhado sobre o branch do PR #115 em `d6cd9fd3`. O PR #116 de
Micromodelos está em `3b9ea68c` e permanece paralelo. Esta ficha consolida
o estado **atual**; relatórios anteriores preservam a versão e a tentativa
que examinaram. Nenhum gate histórico G6 R7 foi reclassificado como PASS.

## Identidade e validação do candidato

| Gate de revisão parcial | Evidência no HEAD | Estado |
|---|---|---|
| Fonte e derivado | Árvore Git `ambiente_fonte/.assistant` e derivado `.assistant`: `fa5bd390cb3273fe91077d9d9d90f125cbae892f`; 657/657 arquivos gerenciados iguais byte a byte. `ambiente_fonte/README.md` fica fora do renderer. | PASS local |
| Integridade de release | 11 manifestos, 159/159 artefatos com hash Git blob atual. | PASS local |
| Validador | `python -B tools/validate_assistant.py --conferir-readme`: 0 falhas e 0 avisos. | PASS local |
| Mudança Delta/FE | Teste SER14 9/9, incluindo ACK de `DROP` perdido antes/depois do efeito e no fallback; regressão FE 7/7. FakeSpark testa efeito incerto; Spark local cobre cálculo/projeção. | PASS no escopo local |
| Databricks Free | Correção Delta/FE: [readback dos três arquivos](DELTA_ACK_FREE_PUBLICACAO_2026-09-30.md). Orientação PB pós-`UNKNOWN`: [ACK e segundo readback](PB_RECOVERY_SKILL_FREE_2026-09-30.md). Probes anteriores permanecem vinculados a suas versões. | Conteúdo publicado; novo efeito Delta **NOT_RUN** |
| Genie | [Cross-EDA T03](genie_evidencias/RQ-TRUST-FOCAL_T03.md) PASS focal de proveniência; [Pipeline T02](genie_evidencias/RQ-PB-RECOVERY_T02.md) PASS focal de no-retry com ressalvas materiais. Ambos têm @/indicador relatados, sem execução canônica. Outros [FAILs permanecem](REVISAO_FAILS_REMANESCENTES_B1_2026-09-30.md). | Parcial, não homologado integralmente |
| CI GitHub | No commit `9b845549`, 14 jobs falharam antes de iniciar; `validar` teve zero steps e anotação de pagamento/limite de gastos da conta. `se02` foi SKIPPED. Commits anteriores tiveram CI verde, mas não esse commit. | Externo indisponível; não é falha de teste do produto |

O diff de #117 contra #115 tem 326 arquivos. O pacote inclui oito skills de
execução B1, regressões proporcionais nas outras seis e o contexto MM04
incorporado por escolha do usuário. As alterações mais recentes de produto
ficaram em Cross-EDA/Pipeline SKILL, runner Delta compartilhado e manifestos
Pipeline/FE; policy, controller e runtime paralelo de micromodelos não foram
alterados por essas correções.

## Decisão de revisão

**Candidato parcial revisável: SIM. Ready/merge: NÃO. Homologação integral das
14 skills: NÃO.** Nenhum prompt Genie adicional é obrigatório para manter
essa posição. Indicador de skill não prova bytes carregados ou execução;
readback Free não prova comportamento Genie; teste local de ACK perdido não
é probe de efeito no Free. Os anexos e relatórios `.artifacts/` que não estão
versionados limitam a reverificação remota integral.

O PR #117 é `MERGEABLE` isoladamente, mas seu merge alteraria o branch
compartilhado do PR #115, que segue Draft. A simulação read-only entre os
heads #117 e #116 encontra 12 arquivos conflitantes e 27 caminhos tocados
pelas duas frentes. `MERGEABLE` dos PRs individuais não resolve essa
integração. Os objetos remotos adicionais de MM permanecem sob ownership
paralelo; os readbacks B1 dirigidos não são inventário remoto integral.

## Gates futuros por fronteira

| Fronteira | Evidência reutilizável | Prova ainda necessária **se** entrar no aceite integral |
|---|---|---|
| Safra e Cross-EDA | Free SER03/SER05; evento, estático e T03 focal | Denominador/ausência Safra e contexto Cross sem inventar campos; execução Genie só se exigida como gate próprio. |
| Explainability e Validação Estatística | EX-D01; KS verificado após correção CLI | SHAP/Receipt Genie, potência/multiplicidade somente se essas respostas forem exigidas; definir oráculo antes de novo chat. |
| Feature Engineering e Baseline | PIT e regressões locais; planejamento temporal dirigido | Extrapolação de schema/causa, roteamento FE distinto; holdout, maturidade e tracking nos casos ainda falhos. |
| Monitoramento | Cálculos/outputs sintéticos anteriores | Interpretação de smoothing, potência e labels maduros, sem repetir cálculo só por erro textual. |
| Pipeline Builder | T02 no-retry; Delta/FE local e conteúdo Free atual | Um reteste focal da **nova** orientação para aceitar recuperação completa; PB-P de especificação é fronteira distinta. Novo probe Free normal do runner é automatizável, se efeito remoto atualizado for gate. |
| Seis skills de regressão | Concierge/Comentar e SER01 A4 em seus escopos; fichas EDA/Tutor/Auditoria | EDA sem schema, Tutor com contexto real esclarecido e payload SE07 somente se incluídos no aceite; não reabrir os demais por rotina. |

Antes de Ready ou merge: resolver o bloqueio externo de CI para obter checks
do HEAD, definir a ordem de integração #115/#117/#116 e reconciliar conflitos
com ownership preservado, e obter a autorização humana específica para os
gates de promoção e integração. O estado G6 histórico de #115 e os gates
G7/G9 não são promovidos por esta ficha. Não alterar policy, controller ou
workspace corporativo para satisfazer o aceite parcial.
