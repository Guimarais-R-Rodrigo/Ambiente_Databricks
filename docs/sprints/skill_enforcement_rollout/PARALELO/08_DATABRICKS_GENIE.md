# 08 — Capacidade externa, publicação e coleta controlada

## 8.1 Objetivo do canal externo

Provar aquilo que a campanha local não prova: dependências e runtime reais no Free, pacote remoto correspondente à fonte, integração com Spark/MLflow/serviço permitido, efeitos no destino autorizado e comportamento do Genie. Não confundir essa prova com a identidade de commit ou com autorização corporativa.

Este plano não verificou capacidades atuais do workspace nem executou probes novos. A qualificação externa será read-only primeiro. Uma credencial válida prova identidade/login, não permissão de escrever ou existência de API específica.

## 8.2 Descoberta de capacidade antes de escrever o roteiro definitivo

O pacote de autoria inclui inventário mínimo: profile/host esperado, usuário do workspace redigido no SHARE, runtime/linguagem, versões de dependências, Spark, MLflow, acesso ao namespace pessoal, operações aceitas e limites observados. Consultas só de leitura são aprovadas em lote; não usar credential scan nem imprimir tokens.

Se uma capacidade indispensável não existir, marcar o nó afetado BLOCKED_CAPABILITY e manter sua claim fora da promoção. Não preparar dezenas de testes de deploy baseados numa API cuja disponibilidade não foi observada. Pipeline/materialização/tracking só liberam positivos de efeito depois desse inventário e do destino autorizado.

## 8.3 Um publicador e um pacote por vez

Publicação usa o entrypoint existente `tools/publicar_free.py`, após conferir suas opções reais. Não substituir pelo engine interno do Hub. Preservar dry-run, execute, verify de presença e verify por conteúdo como etapas diferentes. O número de arquivos é medido para a candidata; não fixar 574 eternamente.

O publicador possui lock exclusivo por workspace/raiz `.assistant`. Probes das várias skills podem ter nomes distintos, mas todos referenciam o mesmo deployment manifesto congelado do lote. Ninguém publica outra versão enquanto a coleta desse lote estiver aberta.

Publicar antes da promoção mantém current antigo; testar disponibilidade de primitives não promove policy. Depois de autorização, mudança de policy/metadata aplicável exige nova verificação do pacote final. Comportamento deve ser reavaliado proporcionalmente à mudança; não alegar comportamento L3/L4 a partir de um pacote L0/L2 sem explicitar a diferença.

## 8.4 Protocolo de side effects e anomalia de transporte

Antes de import/publicação: registrar request fingerprint sem segredo, path alvo, conteúdo esperado, estado existente e semântica de sobrescrita autorizada. Depois: preservar exit/erro, estado remoto, timestamps/IDs e conteúdo exportado quando pertinente.

Se o comando falhar com possibilidade de efeito no servidor, parar novas escritas. Permitir somente reconciliação read-only declarada: get-status, export, list/readback. A tentativa falha continua falha. Se o objeto existe e corresponde ao conteúdo, uma tarefa nova pode usar o objeto existente sem novo import, mediante transição autorizada do runbook. Nunca repetir cegamente a escrita para “conseguir exit 0”.

## 8.5 Roteiro de coleta controlada

O coletor prepara uma fila com case_id, notebook/chat alvo, instrução literal, deployment digest, output que deve ser preservado e proibições. A execução pode ser humana ou feita pelo controller somente quando a superfície/capability correspondente estiver qualificada e a classe A2 estiver ativa para aquele efeito. O usuário não precisa inventar nome, preencher schema nem resumir resultados. A primeira tarefa piloto valida que o canal consegue transportar o JSON/eventos necessários antes das demais.

Para notebook: abrir o alvo previamente materializado e verificado, executar uma vez, preservar output literal completo e ID/timestamp de execução quando exposto. O JSON é validado mecanicamente pelo coletor. Se parte foi omitida, usar export/readback permitido antes de pedir novo Run all. Não converter um resumo humano em JSON “equivalente”.

A coleta não recebe como evidência a afirmação “tudo passou”. Aceita output literal ou arquivo exportado, com vínculo à versão e ao caso. JSON truncado ou marcador ausente recebe EVIDENCE_INCOMPLETE, sem dizer que o código necessariamente falhou.

## 8.6 Probes determinísticos por skill

Cada probe tem fonte versionada, hash local e export remoto conferido. Não incluir notebook de teste dentro do pacote de produto sem decisão arquitetural. No Free, respeitar distinção entre arquivo importável e notebook; usar o publicador existente para evitar regressão desse mecanismo.

Probes positivos computacionais devem executar a primitive real, não apenas verificar fixture sintética de Receipt. Um probe de verifier pode usar fixture rotulada INTEGRITY_ONLY, mas não substitui o positivo numérico da skill. Probes de L4 precisam observar Postflight e os efeitos realmente incluídos no escopo.

Após o lote, verify por conteúdo confirma que o produto continua esperado. Estado do target de materialização/tracking/deploy é verificado separadamente; package integrity não prova ausência de alteração em tabelas/runs.

## 8.7 Roteiro Genie antes da execução

Cada skill possui oito famílias no catálogo (auto-route, mention, negativo, incompletude, bypass, Receipt inválido, autoridade fraca e efeito versus explicação). O autor transforma essas famílias em prompts literais, com variantes e oráculos observáveis, antes do freeze externo. Pelo menos dois negativos vizinhos discriminantes são definidos, não escolhidos a posteriori.

No teste de auto-route positivo, usar prompt sem nome/@ da skill alvo. No teste de mention, preservar a menção conforme a UI realmente a enviou. Caso negativo não deve simplesmente repetir “não use esta skill” como única prova de precisão de roteamento. Usar também uma tarefa vizinha cuja skill correta seja outra ou nenhuma.

Chat novo por caso/variante; sem dicas corretivas no mesmo chat. Primeiro resultado preservado. Uma falha comportamental não é apagada tentando outro prompt até acertar; gerar nova revisão/caso com razão e manter o denominador original. Os prompts do teste não devem instruir a produzir o veredito esperado de forma tão detalhada que tornem a medição tautológica.

## 8.8 Observabilidade e critérios humanos

Campos: case_id/variant_id, deployment_id, chat/notebook/run_id quando observável, prompt literal, resposta literal, tool/UI events, skill/load indicator, effects attempted/observed, outputs, ambiente/data, evidence_grade e verdicts separados.

Task correctness, agent adherence e canonical compliance são eixos distintos. Uma resposta adequada sem prova da chamada não certifica execução. Uma skill carregada sem cálculo correto não certifica domínio. Ausência de indicador é NOT_OBSERVABLE; não pedir histórico de pensamento privado como compensação.

A suficiência probatória por caso é congelada antes da coleta. Se a UI não expuser um evento obrigatório, a autoria deve propor observação alternativa efetiva ou limitar a claim antes do teste. Não relaxar depois do FAIL. Um caso de explicação pode exigir só comportamento textual; um caso que declara “helper chamado” precisa de execução observada.

## 8.9 Contrato de autorização externa por lote

Uma autorização delimita workspace pessoal, identidade da candidata/deployment, lista de operações e destinos temporários, write/overwrite permitido, limites e cleanup/rollback. Referenciar o aceite do usuário; não colocar credencial no manifesto. Troca de host, tabela, modelo, schedule, payload material ou candidato revoga o vínculo para a ação alterada.

Reautenticar profile após expiração é ação do usuário ou procedimento explicitamente autorizado pelo contrato ativo; A0 não inclui remediação de credencial. Uma autenticação renovada não reclassifica rodada antiga. O local nunca presume DEFAULT ou um profile corporativo para contornar FREE indisponível.

## 8.10 Encerramento e publicação pós-merge

Um lote externo termina quando outputs, post-verifies, effects e revisões estão completos para as claims previstas. Exceções ficam por skill/superfície. Não exigir que pipeline L4 improvável bloqueie o fechamento legítimo de safra L3 independente; tampouco chamar o plano inteiro concluído se pipeline ficou parcial.

Merge integra código. Publicação coloca bytes no Free. Homologação comportamental mede uma versão operacional. Replicação no trabalho permanece BLOQUEADA e fora desta autorização. Essas três datas/identidades são registradas separadamente.
