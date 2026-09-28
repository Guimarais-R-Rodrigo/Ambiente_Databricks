# 03 — Ciclo de vida, gates, falhas e retomada

## 3.1 Estados não são um único semáforo

Preservar eixos separados: prontidão de autoria, resultado local, revisão, capacidade externa, autorização, promoção, integração e publicação. Exemplo legítimo: `LOCAL=PASS`, `AUDIT=PASS`, `FREE=BLOCKED_CAPABILITY`, `PROMOTION=NOT_AUTHORIZED`. Não colapsar isso em “skill concluída”.

Fases de campanha: `AUTHORING_DIAGNOSTIC`, `LOCAL_CERTIFICATION`, `EXTERNAL_VALIDATION`, `POST_POLICY_CERTIFICATION`, `INTEGRATION_CHECK`. O campo `phase` é enum, não texto livre. Um caso é `PASS`, `FAIL`, `ERROR`, `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE` ou `NOT_OBSERVABLE`, conforme contrato. `SKIP` do framework de testes é traduzido com sua causa; não é automaticamente `NOT_APPLICABLE`.

## 3.2 Gates de uma frente

| Gate | Entrada | Ação autorizada | Saída exigida | Quem decide |
|---|---|---|---|---|
| G0 — Escopo | Dossiê e fontes | Leitura, inventário e desenho repo-side | Operações/superfícies/hosts/efeitos fechados; exclusões explícitas | Autor; usuário apenas em decisão material |
| G1 — Autoria pronta | Código/testes/fixtures/perfil completos | Checagens baratas e revisão estática aqui | Sem defeito conhecido; catálogo de APIs conferido; bloqueios resolvidos | Autor + revisão |
| G2 — Qualificação local | Pacote imutável G1 | Diagnósticos aprovados e inventário do host | Ambiente compatível; permissões comprovadas; cobertura coletada | Launcher + auditores |
| G3 — Freeze | Diagnóstico resolvido; preparação aprovada | Render/snapshot mecânicos, commit de preparação | SHA/tree limpos; manifestos e digests fechados | Integrador |
| G4 — Certificação local | G3 e autorização da campanha | Uma execução dos gates e casos liberados | Outputs, efeitos e evidência coerentes; verifier válido | Launcher/verificador |
| G5 — Auditoria | Artefatos G4 | Revisões independentes e probes read-only aprovados | Sem finding material aberto; cobertura demonstrada | Auditores; adjudicação por autor/usuário |
| G6 — Externo | Pacote auditado e capacidade/efeitos autorizados | Publicação única, probes e chats definidos | Evidência real Free/Genie por superfície aplicável | Integrador + usuário |
| G7 — Proposta de promoção | G4–G6 e escopo provado | Preparar proposta nominal e rollback | Before/after e riscos apresentados; autorização específica | Usuário |
| G8 — Pós-policy | G7 autorizado | Alteração mínima de policy aqui; preparação mecânica local | Novo SHA; certificação final e auditoria do vetor aprovado | Autor/integrador/verificador |
| G9 — Integração | Candidata final certificada | Reconfirmação remota e merge específico | Pais/tree conferidos; identidade integrada registrada | Usuário autoriza; integrador executa |
| G10 — Publicação vigente | Pacote integrado e autorização de destino | Publicar/verificar, quando solicitado | Package digest remoto correspondente; status separado de merge | Integrador + usuário |

Não há obrigação de pedir autorização humana a cada comando read-only se a campanha aprovada já os listar. Também não há autorização implícita de escrita porque a fase anterior passou.

## 3.3 G1: checklist de autoria para evitar retorno previsível

Antes de enviar ao laboratório: parse de todos os `.py` novos com `ast.parse`; JSON/TOML válidos; fixture pequena com encoding explícito; assinaturas públicas reais; testes de policy em fixtures quando se destinarem a níveis históricos; ausência de autoimport recursivo do test runner; manifest hashes; paths/links locais; testes positivos e negativos; erros e skips estruturados; esquema de summary e verificação independente; placeholders bloqueados no perfil executável.

O autor não declara runtime local ou Windows se não o executou. Checagens estáticas aqui reduzem defeitos triviais; a qualificação G2 cobre o que depende da máquina do usuário. Qualificação não é oportunidade para o **executor determinístico da campanha** criar implementação faltante. Após a rodada encerrar, o root controller pode abrir repair A1 causal em novo SHA quando o envelope permitir.

## 3.4 Diagnóstico sem retry-until-green

`diagnose` recebe um DAG diagnóstico fixo. Pode rodar syntax, schemas, coleta, fixtures puras e validação de configuração em paralelo, mesmo se outro diagnóstico independente falhar. Interrompe descendentes de uma falha e qualquer operação com efeito. Preserva todas as falhas numa lista ordenada; `first_failure` é imutável.

É proibido instalar uma nova biblioteca, editar o teste, trocar seed, aumentar timeout ou repetir só o teste que falhou durante a mesma rodada. Um problema ambiental causa uma rodada causalmente nova após a alteração autorizada do ambiente. Um problema de código encerra a rodada determinística e retorna à autoria; em Autonomous Controller Mode essa autoria pode ser executada pelo A1 Authoring Executor dentro dos write roots, sempre produzindo novo SHA antes de nova certificação.

O diagnóstico pode revelar erro novo que a análise aqui não alcançou. O compromisso é não encaminhar erro conhecido, não prometer ausência de qualquer defeito futuro.

## 3.5 Certificação single-shot com paralelismo

Uma certificação contém várias tarefas independentes; cada tarefa/gate tem no máximo uma tentativa material na rodada. Falha local interrompe seus descendentes. Tarefas independentes já autorizadas podem terminar; seus resultados permanecem componentes válidos para o SHA testado, mas o agregado exigindo a tarefa falha não recebe PASS.

Falha de mecanismo compartilhado, integridade do clone, quebra de isolamento, segredo exposto ou corrupção de evidência dispara parada global. O coordenador não cancela processos arbitrariamente sem registrar motivo e estado de efeito. Um cancelamento é `INTERRUPTED`, não FAIL de domínio nem PASS incompleto.

Não executar novamente toda a suíte como “conferência” depois do PASS. O verifier externo pode ler artefatos e executar probes de verificação previamente aprovados; isso é tarefa de auditoria distinta, não segunda certificação disfarçada.

## 3.6 Transições permitidas e saídas do fluxo

`PLANNED → AUTHORING → AUTHORING_READY → DIAGNOSTIC_RUNNING → DIAGNOSTIC_PASS → FROZEN → LOCAL_RUNNING → LOCAL_PASS → AUDIT_PASS → EXTERNAL_PENDING/EXTERNAL_PASS → PROMOTION_PROPOSED → AUTHORIZED → POST_POLICY_CERTIFIED → WAITING_MERGE → MERGED`.

Essas transições só acontecem com os artefatos exigidos. `FAIL`, `BLOCKED_*`, `NOT_OBSERVABLE` e `PARTIAL_CAPABILITY` são estados de saída explícitos. Uma nova rodada referencia a anterior por `supersedes_attempt_for_current_candidate`, sem mudar o registro anterior. Não usar `SUPERSEDED` para apagar o fato de que uma tentativa falhou.

A lista acima descreve um caminho, não uma obrigação de serializar skills independentes. Uma L4 pode ser preparada enquanto outra L3 está em Free; sua própria L2 deve estar aceita antes de alegar a promoção L4.

## 3.7 Efeito e comando têm estados independentes

`exit_code=1` pode coexistir com `remote_effect=CREATED`. Um timeout pode coexistir com `effect=UNKNOWN`. A campanha precisa de `process_status`, `effect_status` e `verification_status` separados.

Ações de reconciliação read-only podem ocorrer após falha se declaradas antes: get-status, export, leitura do destino, listagem do run. Não incluem retry de POST/PUT, cleanup, overwrite ou replay. O resultado da tentativa original continua falho; uma execução subsequente sobre objeto existente requer uma nova tarefa autorizada e identidade própria.

Cleanup é efeito mutável com autorização, precondições e evidência próprias. Não apagar resíduos antes de capturar bytes/estado necessários à auditoria. Não usar “limpeza concluída” se não houve observação suficiente.

## 3.8 Condições de PASS agregado

PASS exige: todos os casos obrigatórios com outcomes esperados; condições resolvidas; collection manifest igual ao aprovado; nenhum erro/skip inesperado; domínio e autoridades respeitados; outputs e records presentes e consistentes; nenhum drift não autorizado; evidência íntegra; todas as suites da cobertura aplicável contabilizadas; verificação externa válida.

Algumas suites contêm testes negativos que esperam erro. Nesses casos, PASS é do oráculo do teste, não da operação rejeitada. Canal histórico temporal não é relabelado PASS; é observação separada e só deixa de bloquear o agregado novo quando há invariante sucessor explicitamente implementado e verificado.

## 3.9 Falha do próprio mecanismo de evidência

Se a reserva de evidence root falhar, o launcher registra a tentativa em seu ledger externo e devolve erro estruturado. Se o disco parar de aceitar escrita, não prometer summary persistido em qualquer circunstância. Preservar stdout/stderr e estado parcial recuperável; marcar `REPORTING_FAILURE` e impedir certificado.

Exceção de serialização, schema inválido, verifier que levanta exceção e falha na auto-verificação resultam em certificado ausente/inválido, nunca num PASS. O status de processo final e o de evidência devem concordar. Proibir sobrescrita do primeiro erro por erro de cleanup/finalização.

## 3.10 Retomada sem duplicar efeitos

Após interrupção, executar apenas a inspeção autorizada de ledger, locks, processos e destinos. Se estado mutável desconhecido persistir, não retomar a ação. Tarefa puramente read-only pode ganhar nova rodada explicitamente registrada; ela não é continuação invisível de um PASS parcial.

Nenhum agente decide sozinho que uma falha é “flaky”. A hipótese precisa de causa, reprodução controlada e correção da infraestrutura ou mudança de ambiente autorizada. Stress test é conjunto de repetições predefinido com denominador e critério antes da execução; não é rodar até acertar.


## 3.11 Autonomous Controller Mode

O ADR-0024 muda a **granularidade da coordenação**, não os gates.

Um envelope ativo pode delegar ao Codex controller transições técnicas entre gates
sem nova pergunta humana:

- A0: read-only, diagnóstico, auditoria e reconciliação permitida;
- A1: autoria repo-side, testes, commits/push normal e manutenção da draft PR;
- A2: efeitos pessoais/reversíveis somente após ativação humana explícita e dentro
  de host/namespace/effect/budget fechados;
- A3: promoção, Ready, merge, corporativo, dados reais e mudanças materiais de
  escopo permanecem Human Gates.

A nova unidade delegada ao controller é uma **frente fechada**, não um comando
isolado. O controller continua despachando tasks fechadas para seus subagentes.

`retry-until-green` permanece proibido. O controller pode abrir nova rodada
somente após registrar `causal_delta`. Mesmo SHA + mesmo estado + mesmo comando
tem budget de retry igual a zero.

Antes de qualquer nova mutação após possível write, `UNKNOWN` exige
reconciliação read-only. Se o efeito continuar irresolvido, parar em Human Gate.

A transição G6→G7 continua exigindo todos os subgates externos obrigatórios; PASS
de um subgate não promove o agregado.
