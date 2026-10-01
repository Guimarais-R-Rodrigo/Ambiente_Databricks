# B1 — revisão dos FAILs e limites remanescentes

(Codex) Revisão em 2026-09-30, por escolha do usuário de manter o [PR #117](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/pull/117)
como **candidato parcial**. Base de produto desta revisão: árvore Git
`ambiente_fonte/.assistant` `5d9024df92da0edb9f0fbc8762c63bdbccbda3ee`
após a correção Cross-EDA; a [ficha atual do PR](ACEITE_PARCIAL_PR117_2026-09-30.md)
registra as mudanças posteriores. Fontes principais: [consolidação das 14
skills](CONSOLIDACAO_GENIE_B1_2026-09-30.md),
[triagem de UI](TRIAGEM_POS_UI_2026-09-30.md),
[requalificação atual de Safra/Cross](G6_REQUALIFICACAO_B1_ATUAL_2026-09-30.md)
e fichas de cada caso. Esta revisão não executou novos prompts Genie, jobs,
escritas Free ou alterações de produto/policy.

## Regra de leitura

Um FAIL registrado continua verdadeiro **naquela tentativa**; ele não é
automaticamente um defeito reproduzido na versão mais nova. Um PASS local ou
Free comprova o perfil executado, não o comportamento da Genie naquele chat.
Indicador de skill confirma apenas carregamento relatado, e texto sobre
preflight/Receipt sem payload não comprova execução. Use quatro estados:

1. **Histórico com reteste positivo:** manter o FAIL e usar o PASS posterior
   somente para o mesmo objetivo e versão efetivamente testados.
2. **Histórico pré-correção sem reteste específico:** contrato foi ajustado;
   comportamento da Genie na versão corrigida permanece desconhecido.
3. **Falha contra guarda já existente:** erro de resposta material, sem defeito
   de runner ou lacuna de contrato demonstrada. Repetir frase na skill ou chat
   idêntico não é reparo causal.
4. **Reproduzida pós-correção/readback:** risco atual forte, que bloqueia
   homologação conversacional daquela fronteira.

## Oito skills de execução B1

| Skill | Estado da evidência Genie | Limite/ação mínima |
|---|---|---|
| Safra | [STATUS-D01](genie_evidencias/SD-VF-STATUS-D01.md) acertou maturity/coverage, mas sugeriu taxa parcial com denominador 1 contra roster 2: **FAIL material contra guarda existente**. [RQ-VF-EVENT](genie_evidencias/RQ-VF-EVENT_T01.md) passou em fixture de evento diferente. | Estimando de MOB2 segue risco aberto; não converter PASS da nova fixture em correção do erro de denominador. Reteste só após intervenção causal identificada. |
| Explainability | [EX-A T01/D01](genie_evidencias/SD-EX-A_D01.md): a fronteira `valid=true` falhou antes e passou no diagnóstico dirigido após correção. | Reutilizar D01 no objetivo conceitual; SHAP/Receipt novo não foi observado nesse chat. Nenhum prompt só para apagar T01. |
| Validação Estatística | KS [ST-P-D01](genie_evidencias/SD-ST-P_D01.md) tem execução/verificação observadas depois da correção de CLI. [ST-A](genie_evidencias/SD-ST-A_T01.md) e [ST-B](genie_evidencias/SD-ST-B_T01.md) têm erros de potência/multiplicidade anteriores ao reforço transversal publicado. | ST-A/B são **históricos pré-correção, sem reteste específico**; não alegar reincidência atual nem PASS posterior desses estímulos. Procedência SciPy ausente na resposta antiga continua limite daquele caso. |
| Cross-EDA | [SD-CE-P-D01](genie_evidencias/SD-CE-P-D01.md) inventou campos e narrou execução sem outputs; [RQ-TRUST T01](genie_evidencias/RQ-TRUST-COMBINED_T01.md) e [T02](genie_evidencias/RQ-TRUST-COMBINED_T02.md) elevaram `valid=true` alegado a prova. T02 falhou **após** correção pontual e [readback Free](CROSS_EDA_TRUST_CORRECAO_FREE_2026-09-30.md). O [focal T03](genie_evidencias/RQ-TRUST-FOCAL_T03.md) depois passou na fronteira isolada, com ressalvas de precisão. | T01/T02 seguem FAILs históricos; T03 não homologa o conjunto nem prova bytes consumidos/execução. O SKILL já exige output verificável. Probes Free 5/5 continuam válidos no escopo dos runners, que não mudaram. |
| Feature Engineering | [FE-MAT-D01](genie_evidencias/SD-FE-MAT-D01.md) preservou `UNKNOWN` e entrypoints, mas inventou colunas de readback, escrita parcial e causa específica. Indicador espontâneo mostrou só Baseline; [FE-PIT](genie_evidencias/SD-FE-PIT_T01.md) também ampliou a conclusão sobre a view. | Separar FAIL de roteamento do FAIL de evidência. A skill já guarda `UNKNOWN`; não alterar gatilho por um D01 isolado nem repetir materialização para corrigir texto. |
| Baseline ML | [BL-P-D01](genie_evidencias/SD-BL-P-D01.md) respeitou planejamento, validação e holdout em cenário dirigido, mas presumiu convenção de maturidade/fim do mês. [BL-P/T01](genie_evidencias/SD-BL-P_T01.md) e [BL-B/T01](genie_evidencias/SD-BL-B_T01.md) conservam falhas próprias: converter planejamento em execução e oferecer holdout para seleção de hiperparâmetro, respectivamente. [MLFLOW](genie_evidencias/SD-BL-MLFLOW_T01.md) mantém limites de tracking. | PASS de planejamento dirigido com ressalva; não demonstra cura dos estímulos BL-P/T01 e BL-B/T01. Nenhum treino/MLflow novo nesse diagnóstico. Guardas de split e tracking já existem; investigar causalmente antes de outro chat. |
| Monitoramento | [MO-P](genie_evidencias/SD-MO-P_T01.md) teve métrica sintética/outputs, porém inferiu potência/smoothing incorretamente **após** reforço de contrato; [MO-LABEL](genie_evidencias/SD-MO-LABEL_T01.md) e [MO-B](genie_evidencias/SD-MO-B_T01.md) têm limites temporais/roteamento. [D04](genie_evidencias/SD-VF-N_D04.md) passou em análise exploratória diferente. | Manter interpretação inferencial como risco aberto; não refazer PSI/KS somente por falha textual nem usar D04 para apagar MO-P. |
| Pipeline Builder | [PB-A](genie_evidencias/SD-PB-A_T01.md) recomendou retry com efeito pendente: **FAIL histórico material**. O [focal T02](genie_evidencias/RQ-PB-RECOVERY_T02.md) recusou conclusão/retry, mas omitiu o primeiro passo de localizar destino/registro e sugeriu `DROP_OWNED` sem exigir autoridade de limpeza específica. [DELTA-D02](genie_evidencias/SD-PB-DELTA-D02.md) preservou `UNKNOWN`, mas presumiu tipo/arquivos. [PB-P](genie_evidencias/SD-PB-P_T01.md) trocou `MERGE` por CDC/SCD e tratou `DROP TABLE` como rollback sem impacto pelo nome sintético. | PASS focal de no-retry, reconciliação completa ainda parcial. A [correção do runner](TRIAGEM_CAUSAL_POS_FAILS_B1_2026-09-30.md) passou localmente e teve [readback Free](DELTA_ACK_FREE_PUBLICACAO_2026-09-30.md), sem novo probe de efeito; não cura automaticamente orientação Genie. PB-P mantém falha própria. |

## Seis skills de regressão e roteamento

| Skill | Estado e limite de versão | Ação mínima |
|---|---|---|
| EDA Profissional | [FG-EDA-A](genie_evidencias/FG-EDA-A_T01.md): @/indicador PASS; tipos e grão inferidos sem schema, **FAIL material**. SKILL já veda preencher entradas ausentes. | Preservar FAIL, sem instrução duplicada. Se o comportamento for gate futuro, separar descrição sem schema de schema confirmado. |
| Tutor Databricks | [FG-TU-A](genie_evidencias/FG-TU-A_T01.md): @/indicador PASS; afirmou execução/estado de tabela sem prova, **FAIL material de proveniência**. | Primeiro apurar contexto efetivamente injetado pelo notebook; não atribuir ao runner nem publicar regra textual repetida. |
| Comentar Notebook | [FG-CN-A](genie_evidencias/FG-CN-A_T01.md): deixou `df.count()` pendente, **PASS de núcleo**; “não houve execução” amplia ausência de output além da sessão. | Corrigir formulação na avaliação futura para “não observada nesta rodada”; sem reteste isolado. |
| Auditoria Skills | [FG-AU-A](genie_evidencias/FG-AU-A_T01.md): rejeitou `42` sem prova, mas score `0,6` contradiz total `0,80`; preflight/Receipt apenas narrados, **NOT_OBSERVABLE**, não “executados”. | FAIL parcial material de relatório; checar aritmética local. Se SE07 conversacional virar gate explícito, exigir payload/output, não mais narração. |
| Criar Objeto | Forward 13P/N/M pertence à versão `8187fac`; descrição e enforcement mudaram desde então. Sem novo FAIL B1 demonstrado. O [checkpoint SER01](SER01/CHECKPOINT.md) já registra A4 Free/Genie PASS em sua trilha própria. | Não presumir identidade da versão atual com forward antigo nem reabrir A4 por esta revisão B1. Respeitar gate próprio de SER01. |
| Concierge | [FG-CC-P](genie_evidencias/FG-CC-P_T01.md) e [A](genie_evidencias/FG-CC-A_T01.md): descoberta/seleção/recomendação PASS no escopo; leitura remota de arquivo não observada. | Nenhum novo chat automático; não transformar símbolo confirmado localmente em leitura remota comprovada. |

Roteamentos cruzados são por estímulo: FE-MAT-D01 mostrou Baseline no indicador;
ST-N mostrou Tutor onde o oráculo preferia Explainability, mas “quero entender”
também cabe ao Tutor; ausência de @ naquele caso não foi confirmada. Esses
eventos não justificam uma mudança global de `description` sem hipótese
reproduzível. As fichas históricas continuam com seus vereditos originais.

## Qualidade da prova e posição do PR

As transcrições brutas antigas de EDA, Tutor e Concierge-P não estão neste
worktree de revisão; os anexos originais fornecidos pelo usuário foram
localizados e seus SHA-256 conferem com as fichas. Um revisor remoto recebe
resumos e hashes, não esses anexos nem todos os relatórios `.artifacts/`
ignorados. Esse limite impede reverificação remota integral da campanha.

O PR #117 permanece Draft e empilhado sobre o PR #115. O G6 R7 congelado
continua incompleto; a [requalificação da versão atual](G6_REQUALIFICACAO_B1_ATUAL_2026-09-30.md)
é separada. O inventário Free adicional de micromodelos pertence à frente
paralela e foi preservado. Os 14 checks recentes falharam **antes de iniciar**
por bloqueio de cobrança/limite da conta GitHub (anotações dos jobs), com
`se02` configurado como SKIPPED; não são resultado de teste do produto.
O validador e 24 testes SE05 locais passaram após a correção Cross-EDA que
esta revisão examinou. Testes e readbacks das correções Delta/Pipeline
posteriores pertencem à [ficha atual](ACEITE_PARCIAL_PR117_2026-09-30.md).
Policy, Ready, merge e workspace corporativo não foram alterados.

## Adendo de auditoria causal — 2026-10-01

(Codex) A tabela acima retrata a revisão de 30/set; os FAILs nela descritos
não foram apagados. A versão atual passou nos retestes focais de
[denominador Safra](genie_evidencias/RQ-VF-DENOM-D02.md) e de
[recuperação Pipeline Builder](genie_evidencias/RQ-PB-RECOVERY_T03.md), ambos
conceituais, com indicador da skill relatado pelo usuário e sem runner
observado. Este adendo verifica se os demais FAILs justificam nova edição
de produto ou rodada Genie agora:

| Frente | Contrato atual versus resposta observada | Decisão proporcional |
|---|---|---|
| Cross-EDA | [T02](genie_evidencias/RQ-TRUST-COMBINED_T02.md) atribuiu checagens a `valid=true` apenas alegado após correção Free; o [T03 focal](genie_evidencias/RQ-TRUST-FOCAL_T03.md) tratou isso como alegação, sem prover execução. O `SKILL.md` atual já exige output, inputs independentes e não completar chave/grão/corte ausentes; [CE-P-D01](genie_evidencias/SD-CE-P-D01.md) violou esta última guarda. | Conservar T02 e CE-P-D01 como FAILs de suas tentativas; T03 passa somente na alegação isolada. Sem lacuna nova de contrato demonstrada, não repetir prompt idêntico nem declarar SER05 homologada. |
| Feature Engineering | [FE-MAT-D01](genie_evidencias/SD-FE-MAT-D01.md) preservou `UNKNOWN`, mas inferiu schema/causa sem readback suficiente; a skill já separa view PIT de materialização e exige inspeção humana sem retry. O indicador espontâneo foi Baseline, enquanto [FE-PIT](genie_evidencias/SD-FE-PIT_T01.md) mostrou FE em outro estímulo. | Falha de evidência e de roteamento nesse caso, sem base para mudar `description` global ou reexecutar efeito Delta. |
| Baseline ML | [BL-B/T01](genie_evidencias/SD-BL-B_T01.md) recusou alegações falsas, mas sugeriu holdout para tuning; o contrato atual reserva hiperparâmetros à validação/CV e teste à avaliação final. O planejamento [BL-P/T01](genie_evidencias/SD-BL-P_T01.md) extrapolou para execução; a skill atual já veda criar linhas ou treinar por um pedido de plano. | Preservar FAILs históricos. Repetir a regra no contrato sem causa demonstrada não é reparo; nenhuma métrica nova é necessária. |
| Monitoramento | [MO-P/T01](genie_evidencias/SD-MO-P_T01.md) errou a interpretação de smoothing/potência, mas [D04](genie_evidencias/SD-VF-N_D04.md) acertou a fronteira exploratória; a instrução contraditória sobre bins retornados pelo helper foi esclarecida e publicada. | Sem reteste adicional para esta questão; D04 não certifica SER11 inteiro. |

**Próxima decisão:** manter o B1 como candidato parcial, com os dois novos
PASSes focais documentados. Nenhum prompt Genie adicional tem oráculo novo
proporcional neste checkpoint. Um pedido futuro de homologação integral
exigirá definir antes quais rotas executáveis e fronteiras ainda são gates,
com evidência observável própria; os casos antigos não viram PASS por analogia.
O PR #121 de Safra segue em rascunho; a evidência de Pipeline Builder está
consolidada apenas no branch local de aceite. Policy e merge continuam gates
separados.

**Decisão:** candidato parcial, nenhuma das 14 skills homologada integralmente
por esta campanha. Não há prompt Genie adicional proporcional programado.
Prioridade de investigação causal após T03: (1) cobertura restante de Cross-EDA, sem repetir a fronteira focal que passou; (2)
recuperação segura e extrapolação de efeito Pipeline/FE; (3) denominador Safra;
(4) interpretação Monitoramento e corte temporal Baseline; (5) EDA, Tutor e
Auditoria. Investigar um item não autoriza retriar efeitos nem promover policy.
Depois de hipótese e mudança concreta, retestar **só** o comportamento afetado
em versão vinculada. Para CI voltar a fornecer gate externo, o proprietário da
conta GitHub precisa resolver o bloqueio de cobrança/limite; até lá, o estado
do PR continua candidato parcial com validação local declarada.
