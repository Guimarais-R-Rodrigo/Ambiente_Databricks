# Plano Mestre — Skill Enforcement Rollout

## Estado efetivo em 2026-09-26

O cabeçalho SER00 e partes sequenciais abaixo são histórico do desenho original.
A execução vigente é regida por ADR-0023/0024/0025 e pelo state source da frente.

```text
SER00 = INTEGRATED
SER01 = INTEGRATED
B0 = INTEGRATED_CLOSED / PR #113
B1 = ACTIVE / PR #115 / G6 PARTIAL RECOVERY
AUTONOMOUS_CONTROLLER = AC-R1
A0/A1 = ACTIVE_SCOPED
A2 = PENDING_EXPLICIT_ACTIVATION_AND_CONTRACT
A3 = HUMAN_ONLY
```

Para estado corrente de B1:
`PARALELO/B1/AUTHORING_STATE.json`.


**Versão candidata SER00 reconciliada em 2026-09-23.** Baseline histórica `11851e137dd7793b351ac08fc211c0be90005dee`; main atual `73d7659dcf11509a7fba392221c4810d10401c35`, após as manutenções A07 #102/#105 e a integração MM01. A01–A03 estão aceitas. Falta apenas certificar a candidata documental final da SER00 no SHA exato. Não constitui autorização de SER01.

## 1. Objetivo e limites

Levar nove skills hoje abaixo do target ao nível correto e comprovado por superfície. SEF é infraestrutura; SER é rollout. Não reabrir SE01–SE08 nem criar SE09. Cinco skills no target entram apenas em regressões e integração transversal. `ambiente_fonte/` é fonte; `Novo_Ambiente_Simulado/` é gerado. Nenhuma promoção corporativa.

## 2. Gate de entrada

SER00 entrega inventário, matrizes e desenho. Em 2026-09-22 houve aceite humano do encaminhamento A01–A03: certificação SER prospectiva e aditiva; evolução declarativa de condições sem sobrecarregar o schema 0.1; target L3 de criar-objeto mantido com escopo stage-specific a ser provado por matriz operação×tipo×host×efeito. As corretivas A07 foram certificadas nas PRs #102 e #105 e integradas; a #105 provou diretamente delete sharing com child vivo e sustentou stress 30/30, CI 10/10 e FULL 21/21. A SER00 precisa agora apenas repetir os gates canônicos sobre sua própria HEAD final limpa. Não começar SER01 antes da integração da SER00 e de autorização humana separada.

## 3. Regime local-first

```text
EXECUTION_REGIME = LOCAL_FIRST
GITHUB_ACTIONS = DEFERRED_NO_CREDITS
SER-ACTIONS-RECERTIFICATION = NOT_BLOCKING
PROMOCAO_TRABALHO = BLOQUEADA
```

Não exigir Actions para candidata tecnicamente pronta, não disparar/reexecutar workflows deliberadamente, não alterar workflows por falta de créditos e não relaxar proteção/required checks. Observar execuções incidentais e conservar seus resultados; ausência de passos não prova FAIL funcional nem permite inventar causa de billing. Se proteção impedir integração, registrar MERGE_BLOCKED_BY_ACTIONS_CREDITS e decidir humanamente, sem bypass.

## 4. Contrato de promoção

Target é hipótese revisada; current é capacidade realmente implementada. Nunca promover porque helper existe, teste isolado passou ou o agente disse que usou a função. Exigir contrato, gates, testes adversariais, Receipt/Postflight pertinentes, evidência SHA-bound, Free/Genie aplicáveis e aceite.

Antes de policy, implementar/testar mantendo current antigo e obter autorização da proposta de promoção. Alteração de current é o último ato funcional autorizado; a candidata final exige recertificação no novo SHA e aceite antes de integração. A PR deve identificar BEFORE_CURRENT_LEVEL, AFTER_CURRENT_LEVEL, TARGET_LEVEL, superfície, rollout e evidências. Gate falho mantém promoção não efetivada. Nenhuma alteração de target ou scope por conveniência.

Rollout é dimensão distinta. Preservar EDA/enforce; novas L3 ficam inicialmente audit (warn somente aprovado), pois o validator recusa enforce abaixo de L4. Novas L4 podem permanecer audit até prova discriminante e ativação humana. Não confundir esse rollout com execution_contract.mode=audit do schema 0.1.

## 5. Arquitetura

LLM preserva metodologia e decisões não determinísticas; helpers implementam cálculos reutilizáveis; SEF fornece gates e evidências; policy declara a verdade do produto. Cada skill tem orquestração fina e domínio explícito, não cópia de helpers ou runner universal. Leitura/importação/chamada/conclusão são estados separados. Autorização não é execução. Hash não é identidade humana autenticada.

A certificação SER será aditiva e terá identidade própria, conforme ADR-0022 aceito. Preservar semântica histórica de perfis se01–se08, inclusive resultados vermelhos. A implementação prospectiva deve separar assertions históricas temporalmente fixas de invariantes atuais; perfil novo sozinho não resolve testes históricos presos a números da árvore atual.

## 6. Ordem de integração candidata

SER01 criar-objeto; SER02 explainability; SER03 safra; SER04 estatística; SER05/06 cross-EDA; SER07/08 features; SER09/10 baseline; SER11/12 monitoramento; SER13/14 pipeline; SER15 reconciliação; SER16 fechamento. As cinco L4 são divididas em L0→L2 e L2→L4. Não pular contrato/preflight nem fazer um salto L0→L4.

Explicabilidade pode usar fixture pré-treinada, sem ciclo artificial com SER10. As dependências funcionais e PSEF/MM constam na matriz própria. A frase histórica de que cada sprint parte da main após integração da anterior foi substituída pelo DAG do ADR-0023; frentes independentes podem avançar contra base identificada. O aceite de uma sprint continua sem autorizar automaticamente a seguinte.

## 7. Especificação por sprint

### SER01 — criar-objeto L2 → L3

**Objetivo:** Fechar operação×tipo×host×efeito; separar geração, validação e escrita. Generalizar apenas superfície aprovada, sem converter piloto Windows em prova global.

**Artefatos/rota:** Contrato atual e preflight; validate_create_readme repo-side; validators/moldes por tipo; runner e Receipt com bytes, destino e autorização.

**Casos discriminantes mínimos:** Tipo inválido, conversão, destino ocupado, traversal/junction, autorização ausente, falha parcial, replay, clone/host incompatível. Não sobrescrever nem remover resíduo para forçar PASS.

**Evidência/limite:** Local real por host e prova Free do que for publicado; se o host não suportar a superfície, manter current L2 e registrar escopo não promovido.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER02 — explainability L0 → L3

**Objetivo:** Vincular modelo, versão/run, dataset, população, features, método, classe/output e amostragem; interpretação permanece metodológica.

**Artefatos/rota:** L1 contrato, L2 binding/preflight, L3 compute_shap ou API pública realmente adequada, Receipt.

**Casos discriminantes mínimos:** Modelo/método incompatível, dependência ausente, output_index ambíguo, sample/output sem binding, chamada omitida/incompleta, Receipt adulterado.

**Evidência/limite:** Fixture sintética de modelo/dataset; local e Free; probes de rota/mention/bypass; não apresentar importância como causalidade/fairness.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER03 — análise-safra L0 → L3

**Objetivo:** Resolver coorte, tempo, periodicidade, MOB, denominadores, maturidade e safras incompletas.

**Artefatos/rota:** Contrato/preflight; build_vintage_table no domínio suportado; tabela safra×MOB, incidência e Receipt.

**Casos discriminantes mínimos:** Target não binário, MOB inconsistente, cumulativo decrescente, cobertura incompleta, zero indevido, denominador alterado e replay.

**Evidência/limite:** Fixtures pandas/sintéticas no Free; provar saída e limites; regra de negócio não entra como default silencioso.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER04 — validação-estatística L0 → L3

**Objetivo:** Congelar pergunta, hipótese, unidade, desenho, pressupostos, multiplicidade e catálogo de cálculos suportados.

**Artefatos/rota:** Contrato/preflight; APIs canônicas encontradas; efeitos/incerteza/p-values/correções quando aplicáveis; Receipt.

**Casos discriminantes mínimos:** Método não suportado, população vazia/ambígua, pares quebrados, multiplicidade ignorada, assinatura inexistente, falha de helper.

**Evidência/limite:** Casos sintéticos com resultados conferíveis; não promover escopo genérico a partir de um teste KS nem automatizar decisão causal/econômica.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER05 — cross-EDA L0 → L2

**Objetivo:** Resolver A/B, grão, chaves, relação, período, objetivo e disponibilidade/cardinalidade/PIT aplicável.

**Artefatos/rota:** Contrato e preflight read-only; condições aprovadas.

**Casos discriminantes mínimos:** Chave ausente, fontes ambíguas, grain incompatível, tempo/latência desconhecidos, condição falsa/verdadeira/indeterminada.

**Evidência/limite:** Probes de contexto e bloqueio no Free; sem joins substantivos para alegar L3/L4; máximo L2.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER06 — cross-EDA L2 → L4

**Objetivo:** Executar diagnóstico e PIT somente quando aplicável, preservando contrato SER05.

**Artefatos/rota:** diagnosticar_join L3; pit_join L4; Receipt; Postflight e finalizer.

**Casos discriminantes mínimos:** Multiplicidade inesperada, perda de linhas, latência variável não suportada, timezone/empate/limite de janela, invalid Receipt e finalizer omitido.

**Evidência/limite:** Dados isolados no Free, disponibilidade <= decisão verificável e probes adversariais; join simples não é forçado a PIT.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER07 — feature-engineering L0 → L2

**Objetivo:** Resolver entidade/grão/cutoff/horizonte/janelas/disponibilidade/chaves/origem e intenção de materialização.

**Artefatos/rota:** Contrato e preflight temporal/read-only; autorização de escrita ainda separada.

**Casos discriminantes mínimos:** Cutoff ausente, availability desconhecida, janela vazando futuro, contexto conflitante, destino não autorizado.

**Evidência/limite:** L2 não materializa nem prova L4; Free/Genie valida decisões e bloqueios, não criatividade de features.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER08 — feature-engineering L2 → L4

**Objetivo:** Proteger PIT e materialização sem tornar toda hipótese de feature uma função fixa.

**Artefatos/rota:** Estágio L3 explícito para cálculo autorizado; primitives temporais; provenance, output binding, Receipt e Postflight.

**Casos discriminantes mínimos:** Fit fora do treino, fronteira de janela, fonte tardia, materialização sem autorização, saída adulterada e rollback/cleanup incompletos.

**Evidência/limite:** Objeto sintético/isolado, efeitos autorizados, inspeção do destino; falta de materializer comprovado impede L4 dessa superfície.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER09 — baseline-ML L0 → L2

**Objetivo:** Resolver problema/target/classe/unidade/cutoff/horizonte/split/holdout/leakage/grupos/métricas/tracking.

**Artefatos/rota:** Contrato e preflight; treinamento não integra prova L2.

**Casos discriminantes mínimos:** Holdout reutilizado, classe ambígua, grupo cruzado, tracking sem destino, dataset/split textuais inconsistentes.

**Evidência/limite:** Free/Genie sobre fixture e contexto; nenhuma promoção de modelo implícita.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER10 — baseline-ML L2 → L4

**Objetivo:** Proteger processo de split/treino/tracking sem impor algoritmo universal.

**Artefatos/rota:** temporal_split ou alternativa pública adequada; adapters por tarefa; run_governado quando aplicável; Receipt/Postflight.

**Casos discriminantes mínimos:** Preprocessing treinado no teste, parâmetro de treino não ligado ao Receipt, log falho, run/artefato divergente, ausência de assinatura e promoção automática.

**Evidência/limite:** Testar dependências/MLflow no ambiente pessoal antes de declarar capacidade; efeito externo e resíduo registrados; unsupported não vira PASS.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER11 — monitoramento L0 → L2

**Objetivo:** Resolver modelo/versão, referência/atual, janela, métricas/thresholds, maturidade do target, decisão e ações autorizadas.

**Artefatos/rota:** Contrato e preflight read-only.

**Casos discriminantes mínimos:** Modelo ausente, bins/referência mutáveis, janela inválida, label imaturo tratado como performance, autorização inferida.

**Evidência/limite:** Sem retreino/promoção para provar L2; probes de bloqueio/contexto no Free.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER12 — monitoramento L2 → L4

**Objetivo:** Executar métricas e controlar fronteira de recomendação/ação de retrain ou promotion.

**Artefatos/rota:** PSI/CSI/drift/performance pelas APIs aprovadas; Receipt; autorização separada e Postflight.

**Casos discriminantes mínimos:** Drift usado como prova de perda, threshold default indevido, target imaturo, action sem autoridade, replay e falso completion.

**Evidência/limite:** Não aceitar um dry-run como retreino/deploy real; efetuar somente ações pessoais sintéticas explicitamente autorizadas; incapacidade mantém bloqueio.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER13 — pipeline-builder L0 → L2

**Objetivo:** Resolver ambiente/objeto/origem/destino/incremental/idempotência/write mode/permissões/jobs/schedule/intent/rollback.

**Artefatos/rota:** Contrato, pipeline_spec e preflight read-only.

**Casos discriminantes mínimos:** Destino produtivo, permissões não observadas, overwrite ambíguo, schedule presumido, rollback ausente.

**Evidência/limite:** Não executar deploy/run para provar preflight; máximo L2.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER14 — pipeline-builder L2 → L4

**Objetivo:** Separar geração/validação de spec L3, se adequada, da operação de efeito L4.

**Artefatos/rota:** Executor canônico aprovado, autorização/destino, Receipt, Postflight, verificação remota e cleanup.

**Casos discriminantes mínimos:** Spec válida sem execução, destino trocado, autorização stale, deploy parcial, run sem retorno verificável, cleanup falho.

**Evidência/limite:** Somente ambiente pessoal/Free, objeto isolado e autorização explícita; se operação não existir no Free, não promover artificialmente L4.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER15 — reconciliação transversal

**Objetivo:** Conferir catálogo, policy, artefatos, protected surfaces, prompts, handoffs, bypass e documentação vigente.

**Artefatos/rota:** Atualizações necessárias em policy/skills README/instructions/Manual/PSEF; renderer canônico e validadores; referências MM somente.

**Casos discriminantes mínimos:** Entrada ausente/extra, níveis incompatíveis, links quebrados, adapter que finge verificação, policy hardcoded em prompt, drift do derivado.

**Evidência/limite:** 14/14 continua baseline; mudança de cardinalidade externa exige decisão explícita. Não inventar README individual por uniformidade.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

### SER16 — certificação integrada e fechamento

**Objetivo:** Consolidar árvore final e provas proporcionais já obtidas por skill; não adiar toda observação comportamental para esta sprint.

**Artefatos/rota:** Local SHA-bound; publicar_free dry-run/publicação/verify completo e conteúdo; campanha Genie nova; relatório consolidado e rollback.

**Casos discriminantes mínimos:** Rota manual, @mention sem carregamento, helper ausente, blocked preflight, invalid Receipt, Postflight FAIL/omisso, handoff incorreto e stale evidence.

**Evidência/limite:** Separar task correctness, agent adherence e canonical compliance; SER_FULLY_CERTIFIED só após gates e aceite, mantendo Actions DEFERRED_NO_CREDITS.

**Gate:** README, TESTES, RESULTADOS e CHECKPOINT atualizados; PR própria; validação local e externa proporcional; revisão e aceite explícito. Parar antes de merge e antes da próxima sprint.

## 8. Testes mínimos cumulativos

L1: contrato válido, required/conditional/optional, export e template reais, traversal e referência fantasma recusados. L2: positivo, obrigatório ausente, conflito/ambiguidade, condição aplicável/inaplicável/indeterminada, read-only e fail-closed. L3: entrypoint e primitive correta, Receipt válido/adulterado/stale, helper omitido/chamado mas não concluído, input/output binding e erro propagado. L4: PASS/FAIL/BLOCKED/REVIEW aplicável; completion.authorized somente PASS; bypass e finalizer omitido recusados; artifact adulterado, autorização ausente, conditional e rollback/cleanup para efeitos.

Testes unitários usam fixtures sintéticas; mocks não provam Databricks real. Não duplicar a implementação esperada no teste nem fabricar Receipt para substituir chamada não realizada. O gate negativo deve discriminar caminho canônico e caminho manual com resultado numericamente correto.

## 9. Certificação local e evidências

Conferir interfaces atuais com --help antes de executar. Comandos de referência existentes: validate_contracts.py, se07_policy.py, certify_local.py --profile se08, validate_assistant.py, render_simulado.py --write, validate_assistant.py --conferir-readme e ci_local.py --verbose. O perfil SE08 é referência histórica. Pelo ADR-0022, a certificação operacional SER terá identidade própria e composição explícita; qualquer execução do perfil histórico na árvore nova continua registrada como canal separado. Não retirar sua falha do relatório nem reclassificar resultados antigos.

Certificação final exige SHA/tree/main/merge-base, worktree pré/pós, diretório probatório externo novo, comandos e códigos de saída, versões/host, logs, hashes, renderer/diff e bundle verificável. Nenhum PASS de candidata anterior é transportado para novo SHA. Falha preservada; correção gera candidata/rodada nova, não retry-until-green. A indisponibilidade de rede/checkout impede uma alegação de full local, mas não deve ser mascarada como Actions failure.

## 10. Free, Genie e canonical compliance por promoção

Local PASS da candidata primeiro; depois publicação pessoal autorizada e verify por conteúdo, com source_commit, hashes, file counts, missing, obsolete e skills count. Usar tools/publicar_free.py; confirmar CLI, dry-run, publicação, verify completo e conteúdo. Não usar workspace do trabalho, credenciais corporativas ou dados bancários reais.

Para mudanças behavior-bearing: chat novo, positivo/negativo, seleção por @mention, pedido de bypass, helper ausente, preflight bloqueado, Receipt inválido, Postflight failure/omissão quando aplicável, rota canônica e handoff. Probes L2 não exigem Receipt/L4 inexistentes; registrar N/A justificado por superfície, não para esconder incapacidade de executar um gate exigido.

Separar task correctness, agent adherence e canonical compliance. Uma resposta aparentemente correta, um helper importado e o upload de arquivos não provam aderência. Conservar o artefato conversacional literal, não apenas resumo, para evitar repetir a perda de proveniência da SE06. SER16 consolida essas provas; não inaugura a observação.

## 11. Concorrência, documentação e rollback

Reconfirmar main, PRs e arquivos antes de cada sprint/certificação. A main avançou: candidata stale, evidências conservadas e nova rodada reconciliada. PSEF resolve policy após escolher a skill, sem levels hardcoded. MM01 fica intocada; MM04 e alteração de cardinalidade exigirão decisão própria. Não incorporar branches acumuladas PSEF à SER.

Cada sprint mantém README/TESTES/RESULTADOS/CHECKPOINT, desenho quando necessário e ADR prospectivo se houver decisão nova. Nunca editar ADR histórico aceito para recontar a decisão. Atualizar CHANGELOG e snapshots raiz por procedimento preservador e somente com resultado real de validator. Derivado apenas renderer. Não abrir READMEs individuais de skills por uniformidade.

Rollback de código/policy é proposto em PR própria para estado anteriormente certificado; não equivale a apagar efeito externo. Materialização, runs, deploys e jobs exigem inventário de resíduos e cleanup autorizado verificável. Não remover evidência de falha durante cleanup.

## 12. Métricas e fechamento

Derivar periodicamente total/no target/abaixo, distribuição current/target L0–L4, contratos válidos, preflights, runners promovidos versus pilotos, suporte a Receipt e Postflight. Reportar LOCAL/FREE/GENIE/ACTIONS separadamente, por SHA e superfície. Não inventar números nem chamar presença de arquivo de gate executado.

SER_FULLY_CERTIFIED somente com targets aceitos, promoções provadas, adversariais, policy verdadeira, renderer sem drift, Free verificado, comportamento/canonical compliance aplicáveis, PSEF reconciliada, documentação integrada, rollback e aceite final. Nenhuma promoção corporativa. Skills bloqueadas não são consideradas encerradas só por edição de current.

## 13. SER-ACTIONS-RECERTIFICATION

Futura e fora do caminho crítico, NOT_BLOCKING / DEFERRED_NO_CREDITS. Quando houver autorização e créditos, reconfirmar a HEAD integrada final da SER, executar campanha consolidada única, registrar todos os runs, preservar failures e corrigir em PR própria. Zero rerun-until-green. Não reclassificar retroativamente local/Free/Genie nem executar automaticamente cada SHA intermediário.


---

## Adendo operacional de 2026-09-24 — execução paralela governada

Após a integração da SER01, o usuário aprovou substituir a execução estritamente sequencial por um modelo paralelo governado. O ADR-0023 complementa este Plano Mestre sem apagar sua ordem histórica.

Regras vigentes:

1. os identificadores SER02–SER16 e seus targets permanecem;
2. a ordem listada neste Plano continua sendo ordem de integração e rastreabilidade, não dependência funcional universal;
3. componentes independentes podem ser preparados, executados e auditados em paralelo conforme o DAG aprovado;
4. autoria de implementação, testes, fixtures, oráculos e perfis continua repo-side;
5. executores locais recebem campanhas fechadas e não corrigem o candidato;
6. integração, publicação, alteração de policy e gates humanos continuam serializados;
7. cada L4 depende do L2 da própria skill e das dependências compartilhadas explicitamente declaradas;
8. nenhum PASS é transportado como certificado de SHA novo;
9. B0 precisa ser qualificado antes de liberar qualquer campanha real SER02–SER14.

Estado inicial do adendo:

```text
BASELINE_MAIN = d2988e97e7b6c5fe1fd561852e947a155c2d731b
SER01 = INTEGRATED
B0 = IMPLEMENTED_CANDIDATE_LOCAL_QUALIFICATION_PENDING
PARALLEL_REAL_SKILL_CAMPAIGNS = NOT_AUTHORIZED
POLICY_CHANGE_BY_B0 = NONE
```

Documentação operacional: [PARALELO/README.md](PARALELO/README.md). Decisão arquitetural: [ADR-0023](../../decisions/ADR-0023-execucao-paralela-governada-ser.md).
