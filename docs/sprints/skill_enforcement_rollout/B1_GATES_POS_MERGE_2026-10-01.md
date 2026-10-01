# B1 — gates proporcionais após o merge do PR #121

(Codex) Proposta técnica em 2026-10-01, baseada no `main` `e86ff0ff`.
O [PR #118](PR_B1_SKILLS_SEM_CONTROLLER_2026-09-30.md) integrou as skills
executáveis e o [PR #121](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/pull/121)
integrou a correção de Safra e os retestes focais. O gate central e SE01/SE02
passaram no merge #121. Isso é **entrega integrada com aceite parcial**;
não promove policy nem equivale a homologação ampla das 14 skills.

## Definir o objeto do aceite antes de pedir outro chat

| Escopo | O que poderia ser aceito | Limite |
|---|---|---|
| **A — perfis sintéticos suportados (recomendado)** | As rotas fechadas já implementadas, com dados sintéticos, inputs externos, preflight/runner/verificador, efeitos e limpeza quando aplicáveis | Não cobre toda tarefa descrita em cada `SKILL.md`, roteamento Genie universal, domínio corporativo ou target da policy |
| **B — orquestração Genie dos perfis** | Além de A, a Genie deve selecionar a skill certa e produzir outputs observáveis da rota canônica por perfil exigido | As respostas conceituais atuais não substituem runner/Receipt; exige novos chats focais somente onde falta essa prova |
| **C — promoção dos níveis da policy** | Alterar `current_level` por superfície até o target, após evidência e aceite específicos | Human Gate separado; um probe sintético ou status `valid=true` não autoriza L3/L4 amplo |

O [G6 R7 congelado](G6_RECONCILIACAO_ATUAL_2026-09-30.md) mantém suas 20
variantes literais `NOT_RUN` e produto R7 diferente. A escolha humana de
requalificar a versão atual permite reutilizar provas sem executar os 20
prompts antigos, mas não converte o G6 legado em PASS. MM04 tem owner e gates
próprios; seus objetos Free adicionais não são erro a limpar nesta frente.
A policy vigente mantém as oito skills B1 em `current_level=L0`: Safra,
Explainability e Validação Estatística têm target L3; Cross-EDA, FE,
Baseline, Monitoramento e Pipeline Builder têm target L4. Aceitar A ou B
não altera esses níveis.

## Evidência reaproveitável e diferença residual

| Skill B1 | Prova já disponível | Para fechar A no HEAD atual | Se B for exigido |
|---|---|---|---|
| Safra | [Free SER03 5/5](G6_RECONCILIACAO_ATUAL_2026-09-30.md); [denominador D02](genie_evidencias/RQ-VF-DENOM-D02.md) PASS conceitual | Conferir vínculo de versões e manter oráculo de célula incompleta; runner não mudou no D02 | Um output Genie de rota canônica com Receipt/verificador, se execução pela interface for gate |
| Explainability | [R2 runtime](CONTINUACAO_LOCAL_FREE_2026-09-28.md) e [EX-D01](genie_evidencias/SD-EX-A_D01.md) | Reusar SHAP linear escalar com fundo e oráculo independente; outros modelos fora do perfil | Output SHAP/Receipt observável, ainda ausente nos chats conceituais |
| Validação Estatística | [KS D01](genie_evidencias/SD-ST-P_D01.md) com execução/verificação observadas e R2 | Reusar somente KS bilateral do perfil; multiplicidade/potência de outras perguntas não viram aprovação | O KS positivo já cobre a rota observada; só abrir novo chat para gate diferente e pré-definido |
| Cross-EDA | [Free SER05 5/5](G6_RECONCILIACAO_ATUAL_2026-09-30.md), PIT R2 e [T03](genie_evidencias/RQ-TRUST-FOCAL_T03.md) focal | Vincular contexto, oráculo e Postflight às versões; [CE-P-D01](genie_evidencias/SD-CE-P-D01.md) segue FAIL de resposta | Output Genie de preflight/diagnóstico/PIT se a interface, e não o Free, tiver de provar a chamada |
| Feature Engineering | [R2 materialização](CONTINUACAO_LOCAL_FREE_2026-09-28.md) e composição PIT; [FE-MAT-D01](genie_evidencias/SD-FE-MAT-D01.md) preservou `UNKNOWN` | Efeito Delta na versão corrigida, readback e cleanup: **PASS no lote abaixo**; resta consolidação do aceite por perfil | Prova de seleção/execução FE na interface, se necessária; D01 mostrou indicador de Baseline |
| Baseline ML | [R2 MLflow](CONTINUACAO_LOCAL_FREE_2026-09-28.md) e treino sintético Genie observado em [BL-P/T01](genie_evidencias/SD-BL-P_T01.md) | Manter treino/tracking e holdout no escopo do request; não inferir ausência de leakage operacional | Se a Genie for gate, pedir linhas sintéticas fornecidas pelo usuário e preservar request, run_id, Receipt e output de verify para reverificação independente; T01 não os exportou integralmente e não prova tracking pela Genie |
| Monitoramento | R2 de drift SER11 e performance com labels maduros SER12; [D04](genie_evidencias/SD-VF-N_D04.md) corrigiu interpretação PSI/KS | Reusar métricas e política de labels maduros, sem ação automática | Output SER12 na Genie somente se for exigido além do Free; D04 exploratório não o substitui |
| Pipeline Builder | [R2 Delta](CONTINUACAO_LOCAL_FREE_2026-09-28.md) e [T03](genie_evidencias/RQ-PB-RECOVERY_T03.md) PASS conceitual | Efeito Delta na versão corrigida, identidade, MERGE/replay, readback e cleanup: **PASS no retry isolado abaixo**; resta consolidação do aceite por perfil | Output da rota de spec/execução na Genie somente se seleção e chamada forem gates |

O [adendo causal](REVISAO_FAILS_REMANESCENTES_B1_2026-09-30.md) não encontrou
lacuna nova de contrato em Cross-EDA, FE, Baseline ou Monitoramento que
justifique repetir prompts por rotina. Os FAILs de suas tentativas antigas
permanecem nos registros. As outras seis skills da campanha B1 usam
regressões proporcionais por sua superfície vigente; MM04 é a 15ª skill e
permanece fora deste aceite.

As seis regressões têm gates distintos dos oito perfis novos:

| Skill de regressão | Nível vigente | Gate proporcional nesta frente |
|---|---|---|
| EDA Profissional | L4 / enforce | Validador e regressões do piloto EDA, sem inferir schema/grão do chat que não os forneceu |
| Auditoria Skills | L3 / audit | Testes locais do contrato de evidência; o score incoerente e o runner apenas narrado em [FG-AU-A](genie_evidencias/FG-AU-A_T01.md) não viram PASS Genie |
| Criar Objeto | L3 / audit | Reusar o [checkpoint SER01](SER01/CHECKPOINT.md) e sua regressão, sem reabrir seus gates próprios |
| Concierge | L1 / audit | Preservar seleção/recomendação sem atribuir execução da skill descoberta |
| Comentar Notebook | L1 / audit | Preservar código e marcar saída não observada como pendente |
| Tutor Databricks | L0 / guidance | Conferir explicação e proveniência sem runner artificial |

O fechamento A exige que estas regressões não quebrem no HEAD aceito;
não as promove nem converte os FAILs Genie históricos em PASS.

## Ordem mínima recomendada para A

1. Fixar HEAD, hashes de fonte/derivado e identidade remota dos arquivos
   alterados. Nesta leitura, os SHA-256 normalizados atuais de Safra
   `SKILL.md`, Pipeline `SKILL.md` e `run_delta.py`, e dos manifests Pipeline/FE
   coincidem com os readbacks Free registrados nas fichas de publicação.
   Isto não prova os bytes consumidos pela Genie em chats passados.
2. Reusar testes locais, [R2 Free](CONTINUACAO_LOCAL_FREE_2026-09-28.md),
   Free SER03/SER05 e checks do PR #121 somente nas rotas/versões que cobrem.
   Registrar explicitamente qualquer mudança posterior em runner ou contrato.
3. Fazer **um lote Free dirigido com dois casos**, Pipeline Delta e
   materialização FE, na versão de `run_delta.py` posterior à R2, com
   autorizações sintéticas vinculadas, destinos pessoais novos e limpezas
   conferidas separadamente. O caso FE também deve vincular Postflight PIT
   upstream, projeção e identidade da view; o motor Delta compartilhado
   sozinho não comprova essa composição. O
   [readback da correção](DELTA_ACK_FREE_PUBLICACAO_2026-09-30.md) prova
   conteúdo remoto, não execução desse novo efeito. Se o probe falhar ou
   perder ACK, reconciliar o efeito antes de qualquer retry; não repetir
   escrita para fabricar prova.
4. Auditar o resultado por perfil e declarar apenas os perfis realmente
   fechados. Não usar um PASS numérico para apagar FAIL de proveniência,
   autorizar retreino/deploy ou declarar toda a skill homologada.

## Lote Free dirigido em 2026-10-01

Os probes publicados de Pipeline e FE foram conferidos contra os arquivos
locais por SHA-256. Também houve readback idêntico dos runners, contratos e
manifests relevantes. O lote usou apenas fixtures sintéticas e dois destinos
novos em `workspace.default` da área pessoal.
[O extrato estruturado dos outputs e readbacks](B1_FREE_EFFECTS_2026-10-01.json)
preserva os valores completos, sem parâmetros de autorização nem credenciais.

| Caso | Evidência da execução | Resultado e limite |
|---|---|---|
| [FE materialização](https://dbc-72c8503a-bc27.cloud.databricks.com/?o=1656741970497299#job/1016633106927465/run/902427072158930) | `PASS`; Receipt upstream `er1:c8519fa9...`, Postflight `pf1:2f9d01d8...`, view `54bc418e...`; hashes esperado, primeiro MERGE e replay iguais a `69bfe597...`; manifests FE `625a7ca5...` e Delta `c02e8a8f...` | Escrita persistente sintética, readback, replay e cleanup `PASS`; `table_absent_after_cleanup=true`. `promotion_authorized=false`, `business_readiness=NOT_EVALUATED`. |
| [Pipeline, primeira tentativa](https://dbc-72c8503a-bc27.cloud.databricks.com/?o=1656741970497299#job/1016633106927465/run/990221941458934) | `BLOCKED` em `AUTH_VALIDATED`, antes da criação, por `SPEC_PREFLIGHT_BLOCKED` | Diagnóstico somente de leitura no mesmo ambiente: `ModuleNotFoundError: No module named 'jsonschema'`. A API de tabelas confirmou destino ausente. |
| [Pipeline, retry isolado](https://dbc-72c8503a-bc27.cloud.databricks.com/?o=1656741970497299#job/421176563087172/run/678992559773330) | Novo destino, run_id e nonce; ambiente serverless v2 com `jsonschema==4.25.1`; `PASS`, Receipt `er1:1e32ad19...`; hashes esperado, primeiro MERGE e replay iguais a `3ac1a366...`; manifest `c02e8a8f...` | Criação reconhecida, escrita persistente, readback, replay e cleanup `PASS`; `table_absent_after_cleanup=true`. |

Após cada execução, `databricks tables get` retornou `Table ... does not
exist` para os três destinos; essa leitura é independente dos flags do runner.
O notebook temporário de diagnóstico foi excluído e sua ausência confirmada.
O job `SUCCESS` externo não é usado como substituto do `status` interno: a
primeira tarefa Pipeline terminou como job `SUCCESS` mas seu efeito foi
`BLOCKED`. Os resultados FE/Pipeline fecham **somente** o déficit de efeito
Delta da etapa A, na versão publicada aferida. Não demonstram seleção Genie,
uso corporativo, prontidão de negócio ou promoção de policy. Auditoria
independente de leitura recalculou os oráculos sintéticos e conferiu os
outputs brutos e as três ausências; não foi injetada perda real de ACK remoto.

**Genie adicional imediato: zero prompts.** Em B, os novos chats devem ser
especificados por rota ainda sem output observável, nunca pela contagem FG
42/42. O número final depende de quais superfícies Genie entram no aceite;
uma resposta narrativa ou indicador de carregamento não substitui execução.

**Próximo marco:** consolidar o aceite A por perfil com as provas existentes e
as regressões proporcionais. Se a orquestração Genie for exigida para esse
aceite, definir as rotas B específicas antes de abrir novos chats. Promoção
de policy (C), Ready, merge e workspace corporativo continuam em gates
separados.
