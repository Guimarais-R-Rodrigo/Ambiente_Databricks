# 07 — Paralelismo, recursos, Git e integração

## 7.1 Unidade de concorrência

Há oito frentes lógicas, não oito processos pesados obrigatoriamente simultâneos. O scheduler escolhe tarefas READY cujas dependências e recursos estejam livres. O coordenador solicita a execução, mas não altera a regra do scheduler.

No B0 V3, `max_parallel` é o **total de tasks simultâneas**, inclusive auditorias. `max_auditors` é um teto dentro desse mesmo pool, não slots adicionais. O piloto parte de `max_parallel=2` e `max_auditors=1`; `3/2` é somente candidata pós-piloto e exige headroom medido, sandbox qualificado e ausência de finding material. Se o host suportar menos, usar o limite menor. Não aumentar durante rodada para “ganhar tempo”.

O B0 também usa um lease de SO host-wide que autoriza **um launcher de campanha por host**. Assim, exclusivity/resource limits não são vendidos como globais entre múltiplos launchers independentes: múltiplas campanhas locais simultâneas permanecem não autorizadas. O paralelismo ocorre dentro da campanha única. Uma coordenação multi-launcher futura só pode substituir esse conservadorismo depois de prova própria de leases/quotas.

A etapa cara normalmente é processo analítico/IO, não conversa da IA. O agente não precisa permanecer gerando texto enquanto um comando determinístico roda. Eventos started/finished/failure são suficientes, com heartbeat de liveness sem suposições de progresso.

## 7.2 Pools de recursos

As classes executáveis do B0 são `light`, `cpu`, `spark`, `tracking`, `external_effect` e `audit`, exatamente como no contrato/runtime. Rótulos conceituais históricos como `LIGHT_READ` ou `CPU_ANALYTIC` podem aparecer em material de planejamento, mas não constituem outra taxonomia operacional.

Antes de liberar, medir recursos do host em diagnóstico e congelar budgets. Um Spark pesado pode reservar todos os slots analíticos sem impedir auditoria leve. Caches de dependência preparados e read-only podem ser compartilhados; instalações e mutações do cache não ocorrem em concorrência. Não compartilhar run MLflow, porta, temporary root ou fixture mutável entre tarefas.

A raiz sugerida no Windows é curta e externa ao clone; o valor real é resolvido localmente e não versionado com nome pessoal. Não impor path inexistente. `core.longpaths` por ambiente, se comprovadamente necessário e suportado; nenhuma alteração global por conveniência.

## 7.3 Clones e permissões

Um clone limpo por campanha de componente, com SHA/tree fixos; processo Python separado por execução. Worktree pode servir a leitura/preparação, mas não é sandbox de segurança e compartilha metadados Git. O runner histórico possui estado global de processo; não executar múltiplas campanhas no mesmo interpretador importando esse módulo.

Modelo mínimo de defesa: fonte/tests/scripts protegidos contra escrita pelo papel; evidence/scratch exclusivos; rede negada ao worker que não precisa dela; credenciais ausentes do contexto e ambiente do executor; commands allowlist; fingerprints antes/depois; probes de permissão negativa. Fingerprint sozinho detecta algumas mudanças, mas não impede alteração temporária seguida de restauração: prevenção/observação de acesso é gate próprio.

Se o sandbox local não permitir fonte read-only + scratch/evidence write por escopo, separar o launcher de execução do agente. O agente lê/solicita IDs de tarefas; um processo controlado executa os comandos autorizados. Não lançar o pai com permissões amplas e presumir que um TOML de auditor as reduzirá efetivamente.

## 7.4 Escritores exclusivos

| Alvo | Escritor permitido |
|---|---|
| Código da skill, testes e perfis | Autoria repo-side |
| Schema compartilhado, contrato temporal, verificador comum | Autoria repo-side com revisão transversal |
| Policy, Manual, índices e mudanças funcionais | Autoria repo-side |
| Render e atualização mecânica de snapshot | Integrador, com script/instrução aprovado |
| CHANGELOG consolidado | Integrador aplica fragmento de autoria, sem reescrever histórico |
| Evidência de task | Launcher daquela task; auditor só leitura |
| Relatório de auditoria | Auditor respectivo, fora de RAW da execução |
| Workspace `.assistant` | Único publicador do lote/destino autorizado |
| Merge GitHub | Operação explícita após aceite humano do SHA |

Workers determinísticos de campanha não fazem commits de correção. Falha produz finding/diagnóstico e encerra a rodada pertinente; no modo autônomo, o root pode então despachar repair causal ao A1 Authoring Executor dentro dos write roots. Mudanças mecânicas não são licença para decidir conflitos semânticos.

## 7.5 DAG funcional

Depois de B0 qualificado, as três frentes L3 e os cinco contratos L2 podem ser liberados conforme a autoria individual fique pronta. Explainability usa fixture pré-treinada, não depende da promoção de baseline. Safra e estatística não dependem de pipeline. Cross e features compartilham contrato PIT, não copiam implementations uma da outra.

SER06 depende da L2 SER05 aceita; SER08 da L2 SER07; SER10 da L2 SER09; SER12 da L2 SER11; SER14 da L2 SER13. Dependências de efeito externo são nós adicionais: capacidades, destino e autorização. A fila não impõe que toda L3 termine antes de iniciar L2 independente.

O arquivo `catalogos/DAG.json` contém o grafo de planejamento histórico e não é state source vivo. Nós de autoria não são tarefas do executor determinístico local; podem ser despachados ao A1 Authoring Executor quando o envelope corrente os autoriza. Nós de execução só recebem SHA/perfil depois de G1/G2. Faltas de schema/contrato comum bloqueiam consumidores; falha independente não cancela todos os demais.

## 7.6 Modelo de branches e composição

Recomendação: branch de infraestrutura comum; candidatas de componente com owners exclusivos e baseline comum; branch de integração serializada para um lote pequeno. Todos os branch names são resolvidos/reconfirmados antes da criação para evitar colisão.

O contrato de componente contém a lista de paths e dependências. Conflito entre paths permitidos é identificado no planejamento, não descoberto pelo merge. Se duas skills exigirem a mesma mudança compartilhada, criar tarefa de autoria comum, testar uma vez e fixar seu digest; não aplicar duas correções concorrentes.

O integrador combina apenas commits autorizados e previamente inspecionados. O resultado composto ganha SHA próprio, renderer/snapshot medidos e certificação CI-I. Integração preservadora, sem rebase/amend/force sobre evidências congeladas. Não declarar que a árvore final é a mesma porque os arquivos de uma skill parecem iguais.

## 7.7 Movimento da main

Uma campanha não faz fetch repetidamente no meio do teste para perseguir a main. Usa base fixada; reconfirma remoto em pontos explícitos antes do freeze/publicação/merge.

Se main avançar, calcular delta e fecho de dependências. Mudança em policy, schema, engine, instruções globais, publicador ou cardinalidade é impacto transversal. Mudança documental não executável pode permitir reuso de provas de componente como suporte, mas o novo SHA composto ainda precisa de CI-I pertinente. O classificador de impacto é um instrumento revisável, não autorização para descartar testes arbitrariamente.

Antes de uma integração, acordar janela operacional curta com MM/PSEF, sem bloquear o desenvolvimento dessas frentes. Ausência de acordo não autoriza force. Se proteção/required checks impedir merge, registrar bloqueio e solicitar decisão; não relaxar configuração por falta de créditos.

## 7.8 Pacotes de integração e estado por skill

O lote não é indivisível por conveniência. Uma skill bloqueada pode ficar fora de um lote, desde que o manifesto de integração seja regenerado e revisado antes do freeze e que nenhuma outra dependa dela. Não remover silenciosamente membro depois de um FAIL para apresentar o mesmo lote verde.

L2 e L4 da mesma skill têm marcos e aceites explícitos. É possível preparar código L4 enquanto L2 está em revisão, mas não publicar claim de L4 nem pular o checkpoint aceito de L2. A aprovação humana pode agrupar marcos nominalmente e por evidência; nunca transformar uma autorização ampla de paralelismo em aceite de promoção.

## 7.9 Rollback

Plano de rollback é parte do lote antes de efeitos/merge: versão anterior de produto/policy, pacote remoto e destinos, ações necessárias e autoridade. Reverter a policy sem reconciliar produto/manifestos não é recuperação completa. Rollback remoto pode ser impossível de maneira total; nesse caso limitar efeitos iniciais e registrar resíduos.

Cleanup e rollback não são passos automáticos escondidos após falha. São tarefas de efeito autorizadas e verificadas, com seus próprios IDs e logs. Nunca apagar a prova necessária ao contraditório.
