# SER — plano detalhado de execução paralela governada

**Versão 1.0 • 23/09/2026 • Autoria: ChatGPT**

Leitura consolidada dos documentos donos do pacote modular. As obrigações estruturadas estão no ZIP, em `catalogos/`. Planejamento não é execução ou autorização de promoção. Nenhuma alteração foi enviada ao GitHub nesta entrega.

## Sumário

- [SER paralelo — plano detalhado de autoria e execução governada](#sec-01)
- [01 — Mandato, baseline e decisões de desenho](#sec-02)
- [02 — Arquitetura, contratos e interfaces a implementar](#sec-03)
- [03 — Ciclo de vida, gates, falhas e retomada](#sec-04)
- [04 — CI local, cobertura herdada e oráculos](#sec-05)
- [05 — Catálogo transversal e qualificação do mecanismo](#sec-06)
- [SER02 — hub-ml-explainability](#sec-07)
- [SER03 — hub-ml-analise-safra](#sec-08)
- [SER04 — hub-ml-validacao-estatistica](#sec-09)
- [SER05 / SER06 — hub-ml-cross-eda-ml](#sec-10)
- [SER07 / SER08 — hub-ml-feature-engineering](#sec-11)
- [SER09 / SER10 — hub-ml-baseline-ml](#sec-12)
- [SER11 / SER12 — hub-ml-monitoramento-modelo](#sec-13)
- [SER13 / SER14 — hub-ml-pipeline-builder](#sec-14)
- [06 — Auditoria independente e contrato de evidência](#sec-15)
- [07 — Paralelismo, recursos, Git e integração](#sec-16)
- [08 — Capacidade externa, publicação e coleta manual](#sec-17)
- [09 — Contratos dos agentes e handoffs sem deriva](#sec-18)
- [10 — Implantação controlada, entregáveis e critérios de saída](#sec-19)
- [11 — Bloqueios de autoria, riscos e controle de escopo](#sec-20)
- [12 — Fontes, proveniência e limite de cada afirmação](#sec-21)
- [13 — Minuta do adendo operacional ao Skill Enforcement Rollout](#sec-22)
- [14 — Checklist que impede o próximo handoff defeituoso](#sec-23)


---

<a id="sec-01"></a>

# SER paralelo — plano detalhado de autoria e execução governada

**Versão 1.0 — 23/09/2026. Autoria: ChatGPT.**

O usuário aprovou a direção de execução paralela e solicitou o detalhamento antes da implantação. Este pacote define o que deve ser construído no repositório, como será testado e quais ações os agentes locais poderão executar. Não é implementação do mecanismo nem autorização para iniciar campanhas, publicar, promover policy ou fazer merge.

Base Git conferida: `d2988e97e7b6c5fe1fd561852e947a155c2d731b`, no repositório `Guimarais-R-Rodrigo/Ambiente_Databricks`. A SER01 está integrada nessa base. As oito frentes restantes preservam os identificadores SER02–SER14; SER15/SER16 preservam suas funções de reconciliação e fechamento.

## Próxima ação

Executar **a autoria repo-side do pacote B0**, conforme [plano de implantação](#sec-19). Nenhuma skill vai para o laboratório enquanto implementação, testes, oráculos, perfis e decisões materiais de seu escopo não estiverem fechados. O laboratório não recebe a tarefa de descobrir como implementar o que ficou faltando.

## Organização e documento dono

| Documento | Responsabilidade exclusiva |
|---|---|
| [01 — Mandato e decisões](#sec-02) | Escopo, autoridade, baseline e alterações explícitas ao processo antigo |
| [02 — Arquitetura e contratos](#sec-03) | Componentes, schemas, interfaces e identidade da campanha |
| [03 — Ciclo e gates](#sec-04) | Entrada, estados, congelamento, falhas, retomada e promoção |
| [04 — CI e cobertura](#sec-05) | Cobertura herdada, fases de teste, seleção e oráculos históricos |
| [05 — Casos transversais](#sec-06) | Casos comuns e metatestes do mecanismo |
| Dossiês por skill (ver pacote modular) | Escopo e provas específicas das oito skills |
| [06 — Auditoria e evidência](#sec-15) | Revisão independente, RAW/SHARE, finding e suficiência probatória |
| [07 — Paralelismo e integração](#sec-16) | Isolamento, recursos, DAG, merge e mudança de base |
| [08 — Databricks e Genie](#sec-17) | Capacidade externa, publicação única, execução humana e observabilidade |
| [09 — Papéis e handoffs](#sec-18) | Contratos do coordenador, executores, auditores e integrador |
| [10 — Implantação](#sec-19) | Pacotes de trabalho, pilotos, entregáveis e critério de liberação |
| [11 — Riscos e bloqueios](#sec-20) | Questões que precisam ser resolvidas pela autoria, sem decisão improvisada local |
| [12 — Fontes](#sec-21) | Proveniência, verificações realizadas e limites da leitura |
| [13 — Adendo operacional proposto](#sec-22) | Texto pronto para formalização no repositório, sem reescrever ADR aceito |
| [14 — Checklist de prontidão](#sec-23) | Contraditório final antes do primeiro disparo |

`catalogos/CASOS.json` é o catálogo dono dos IDs de casos e das obrigações discriminantes; as tabelas dos dossiês e do documento 05 são visualizações desse catálogo. `catalogos/COBERTURA_BASE.json` inventaria as suítes vistas na baseline. `catalogos/DAG.json` descreve dependências, não dispara agentes. `catalogos/BLOQUEIOS.json` registra as decisões e lacunas de autoria. `CONTROLE_PLANO.json` concentra estado, contagens e capacidades ainda não implementadas.

## Regra operacional em uma frase

**Aqui se define e implementa; localmente se executa e audita; apenas o integrador opera arquivos/destinos compartilhados; o usuário autoriza efeitos e promoções específicas.**

## O que este pacote não alega

As especificações de casos não são testes Python já implementados. Os modelos de JSON não são uma campanha liberada. A validação estrutural deste pacote não comprova qualidade de runtime, sandbox, API pública, capacidade do Free ou conformidade das skills. Os scripts futuros indicados em código monoespaçado são interfaces planejadas, salvo quando expressamente identificados como existentes na baseline.

Nenhum resultado histórico vermelho é apagado. Nenhuma narrativa de uma IA é convertida em chamada de ferramenta observada. Nenhum hash é tratado como autenticação humana. As seis skills já no target entram em regressão, sem nova promoção nesta frente.



---

<a id="sec-02"></a>

# 01 — Mandato, baseline e decisões de desenho

## 1.1 Autorização recebida e fronteira desta entrega

O usuário aprovou a proposta de 23/09/2026 e solicitou: “siga para montar o plano de forma extremamente bem detalhada com o intuito de evitar derivas e idas e vindas de correções que poderiam ser evitadas”. A autorização cobre o detalhamento da mudança de rota. Ela não contém uma lista de novos SHAs aceitos, destinos de escrita externos ou promoções antecipadamente aprovadas.

A arquitetura aprovada é preservada: oito frentes lógicas por skill, autoria repo-side, execução local paralela limitada, revisão independente e integração/publicação serializada. O plano não é uma delegação de desenvolvimento ao Codex local. Havendo lacuna de implementação, o item retorna à fila de autoria aqui.

O usuário não precisa responder repetidamente a perguntas técnicas que a inspeção e a autoria possam resolver. Questões realmente materiais — população real, destino, overwrite, efeito remoto, scope ou target — são consolidadas num formulário único por lote antes do respectivo gate. Ausência dessas decisões bloqueia o efeito correspondente, não todo o trabalho independente.

## 1.2 Baseline e fontes de verdade

A ref `main` foi consultada no GitHub e apontou para `d2988e97e7b6c5fe1fd561852e947a155c2d731b`. O plano aprovado usa a mesma base. Não confundir cabeçalhos históricos de SER00 com a `main` vigente; os documentos SER00 preservam bases mais antigas.

Hierarquia preservada: `CLAUDE.md` → `.claude/CLAUDE.md` → regras pertinentes → decisões aceitas → especificação desta campanha → pacote executável de cada skill. `AGENTS.md` continua adapter fino. O novo adendo explicita a exceção de paralelismo e da divisão de papéis; não reescreve decisões aceitas nem cria autoridade maior que a do usuário.

`ambiente_fonte/` é fonte de produto; `Novo_Ambiente_Simulado/` é derivado. Workspace Free é cópia operacional. A biblioteca de evidências externas não se torna fonte de código. Nenhum segredo, matrícula ou path corporativo é versionado. Dados das campanhas são sintéticos e os efeitos remotos, quando aprovados, pessoais.

## 1.3 Vetor de capacidade a preservar

| Skill | Current na baseline desta frente | Target | Tratamento |
|---|---|---|---|
| hub-ml-criar-objeto | L3 | L3 | Regressão; SER01 integrada |
| hub-ml-eda-profissional | L4 | L4 | Regressão; preservar enforce |
| hub-ml-auditoria-skills | L3 | L3 | Regressão e adapters de verificação explicitamente aprovados |
| hub-ml-concierge | L1 | L1 | Regressão de descoberta e handoff |
| hub-ml-comentar-notebook | L1 | L1 | Regressão editorial, preservação de código |
| hub-ml-tutor-databricks | L0 | L0 | Regressão proporcional, sem runner artificial |
| hub-ml-explainability | L0 | L3 | SER02 |
| hub-ml-analise-safra | L0 | L3 | SER03 |
| hub-ml-validacao-estatistica | L0 | L3 | SER04 |
| hub-ml-cross-eda-ml | L0 | L4 | SER05 L2; SER06 L4 |
| hub-ml-feature-engineering | L0 | L4 | SER07 L2; SER08 L4 |
| hub-ml-baseline-ml | L0 | L4 | SER09 L2; SER10 L4 |
| hub-ml-monitoramento-modelo | L0 | L4 | SER11 L2; SER12 L4 |
| hub-ml-pipeline-builder | L0 | L4 | SER13 L2; SER14 L4 |

O vetor é premissa de planejamento, a ser confirmado pelo preflight da futura candidata; não é permitido recalculá-lo a partir da própria policy modificada e chamar isso de aprovação. O arquivo de autorização conterá a projeção `before` e a projeção `allowed_after` nominalmente. A cardinalidade 14 é da baseline; MM04 não pode aumentá-la incidentalmente nesta frente.

## 1.4 Mudanças explícitas em relação à execução antiga

**DEC-P01 — Ordem de execução.** Substituir a espera universal pela integração anterior por dependências declaradas. Manter as etapas L2→L4 e os identificadores históricos. Skills independentes podem ser implementadas aqui e testadas localmente antes de a anterior ser integrada. Integrar candidatas somente depois de revisão, reconciliação e autorização própria.

**DEC-P02 — Unidade de autoria.** Um dossiê completo inclui código, testes e decisões, não apenas um prompt. `AUTHORING_READY` exige evidência de verificações de autoria no ambiente em que forem possíveis e lacunas ambientais explicitamente separadas. Se a autoria aqui não tiver runtime adequado, registrar `AUTHORING_RUNTIME_NOT_RUN`; não chamar o primeiro ensaio local de certificação.

**DEC-P03 — Dois regimes locais.** Diagnóstico pode reunir falhas independentes predefinidas, sem alterar arquivos nem repetir o mesmo comando. Certificação é uma execução por candidato/rodada, com freeze e sem retry-until-green. A primeira falha é preservada nos dois regimes.

**DEC-P04 — Motor único.** Uma infraestrutura comum de campanha, com perfis declarativos e adapters de domínio finos. Não criar um certificador particular para cada skill. Não criar um runner analítico universal copiando cálculos dos helpers.

**DEC-P05 — Integração em lotes pequenos.** Um lote inicial pode conter no máximo duas skills; depois do piloto, até três, desde que o vetor de autorização e o conjunto de dependências estejam fechados. Um aceite pode abranger um vetor explícito de várias skills, mas não autoriza membros ausentes, efeitos diferentes nem fases L4 ainda não aceitas. Não usar “aceito o lote” sem identificador/digest da proposta que delimita o lote.

**DEC-P06 — Observabilidade.** Relato de seleção/carregamento de skill é distinto de evento observável. Ausência de telemetria recebe `NOT_OBSERVABLE`; o critério não é flexibilizado depois do resultado. A decisão histórica da SER01 não é apagada, mas seu uso de narrativa não será reproduzido como padrão probatório.

**DEC-P07 — Recursos.** Duas frentes no piloto; três slots de skill após prova de isolamento. Dois slots de auditoria, máximo cinco subagentes ativos e um coordenador, sujeitos a limites mais baixos do host/cliente. Threads de IA e processos pesados são quotas diferentes.

**DEC-P08 — Escopo externo.** Um publicador por workspace/pacote. Workers não compartilham credenciais Free. Nenhuma ação corporativa, compra, agendamento produtivo, modelo real de clientes ou concessão de permissão integra esta campanha.

**DEC-P09 — Política.** `current_level` só muda depois das provas pré-policy aplicáveis e de autorização específica da proposta. `target_level`, `scope_mode`, `rollout_mode` e `execution_contract.mode` não mudam por efeito colateral. O ato de promoção deve ser seguido de render, freeze e certificação do SHA final.

**DEC-P10 — Sem defeito conhecido no handoff.** Uma falha de autoria já identificada é corrigida aqui antes de delegar. Não enviar teste sabidamente stale, literal inválido, símbolo inventado ou número estimado esperando que o laboratório encontre o erro.

## 1.5 O que não muda

Sem rebase/amend/force sobre candidata congelada; sem normalização ampla de bytes para ocultar divergência; sem remoção de resultados históricos; sem mudança de teste para obter verde; sem confundir geração, validação, autorização, escrita, homologação e publicação; sem assumir Windows a partir de Linux, nem Free a partir de mock.

A política permanece por superfície, operação, tipo, host e efeito. Um helper existente não prova L3. Um Receipt de integridade não prova execução. Um dry-run não prova materialização. Um Postflight que retorna PASS sem observar a conclusão protegida não prova L4.

## 1.6 Não criar um projeto de plataforma desnecessário

A implementação inicial deve ser biblioteca/CLI pequena, schemas, perfis e relatórios, usando Python e dependências já aceitas quando adequadas. Não criar serviço de fila, banco de dados, painel web, broker remoto, SDK próprio de agentes ou DSL com expressões. Se surgir necessidade de novo componente, documentar o problema que o exige e seu teste discriminante antes de expandir B0.

O propósito é eliminar decisões improvisadas e repasses repetidos, não aumentar documentos sem consumidores. Toda regra normativa tem um dono; templates e resumos apontam para ele.



---

<a id="sec-03"></a>

# 02 — Arquitetura, contratos e interfaces a implementar

## 2.1 Camadas e limites

1. **Plano e dossiês:** arquivos versionados que declaram requisitos, decisão de domínio e testes. Esta entrega pertence a essa camada.
2. **Pacote executável:** implementação, testes, fixtures, perfis e registro de comandos. A autoria repo-side o produz antes de liberar qualquer worker.
3. **Launcher determinístico:** valida manifesto/autorizações, reserva diretórios e recursos, lança processos isolados, captura evidência e bloqueia ações fora do contrato. Não delega decisão de segurança ao LLM.
4. **Agentes:** coordenador, executores e auditores recebem escopos fechados. Podem diagnosticar, mas não alterar pacote, resultados ou critérios.
5. **Verificador:** inspeciona os artefatos persistidos, confronta cobertura, identidades e efeitos. Não confia apenas nos flags que o produtor gravou.
6. **Integrador:** prepara mecanicamente o composto, snapshots e derivado, após receber instruções repo-side. Publicação e merge exigem autorizações próprias.

O launcher proposto é ferramenta repo-side, fora de `ambiente_fonte/`. Os adapters e verifiers de cada domínio que forem necessários no produto ficam na skill/infraestrutura correta. Testes, agentes Codex e relatórios privados não são publicados dentro de `.assistant`.

## 2.2 Mapa de módulos — nomes planejados, não ferramentas existentes

Estrutura proposta, sujeita a colisão zero e revisão de layout em B0:

```text
tools/skill_enforcement/parallel_campaign/
  cli.py              # subcomandos e validação de entrada
  manifest.py         # schema e regras cruzadas, sem execução
  scheduler.py        # DAG, quotas e locks
  process_adapter.py  # interface com supervisor de processo existente
  evidence.py         # índices, hashes e escrita atômica
  verify.py           # verificação sem reexecutar toda a campanha
  adapters/           # adaptadores de suites/formatos já existentes
  schemas/            # manifesto, resultado, autorização e perfil
```

Não criar módulos vazios só para satisfazer o diagrama. É aceitável agrupar responsabilidade pequena, preservando interfaces e testes. O código compartilhado do supervisor existente deve ser reaproveitado por composição depois de inspecionado; não copiar centenas de linhas de tratamento Windows para cada certifier.

CLI planejada: `lint`, `inventory`, `diagnose`, `certify`, `verify`, `collect-external`, `package`. Nenhum subcomando `promote-all` ou `merge-all`. `certify` nunca escreve policy. `package` nunca altera RAW. `inventory` nunca instala dependências. Todos os comandos de exemplo referentes a esse diretório são especificação, não instrução para executar agora.

## 2.3 Manifesto de campanha

O schema de produção será fechado, versionado e sem campos desconhecidos. `additionalProperties=false` em todos os objetos de contrato. Não usar defaults silenciosos para campo material. Quatro documentos lógicos são suficientes: manifesto, perfil, resultado e autorização. O schema do catálogo de planejamento desta entrega é outro artefato: ele não libera execução.

| Grupo | Campos obrigatórios na futura campanha executável | Regra |
|---|---|---|
| Identidade | schema_version, campaign_id, round_id, phase, baseline_sha, candidate_sha, candidate_tree | SHA e tree completos; nenhum placeholder na liberação |
| Autoria | implementation_manifest_digest, tests_manifest_digest, profiles_digest, command_registry_digest | Conteúdos imutáveis; manifesto por arquivo, não só pasta textual |
| Policy | before_policy_digest, approved_vector_digest, expected_policy_projection | Projeção aprovada independente da policy lida no candidato |
| Ambiente | python, dependency_lock_digest, os, filesystem, locale, encoding, runner_version | Valores observados e compatibilidade congelada; sem upgrade no meio da campanha |
| Escopo | skills, stages, surfaces, operations, object_types, hosts, effects, exclusions | Campo vazio não significa “tudo” |
| Dependências | nodes, edges, artifact_dependencies, shared_contract_versions | DAG acíclico, nó existente e dependency status observado |
| Casos | required_case_ids, conditional_case_ids, test_id_bindings, expected_outcomes, oracle_artifacts | Caso não implementado impede `EXECUTABLE_READY` |
| Execução | commands, env_allowlist, read_paths, write_paths, protected_paths, budgets, exclusivity_keys | argv fechado; expansão limitada a valores tipados |
| Prova | output_schemas, evidence_root_id, verification_entrypoint, raw_policy, share_policy | Diretório novo; paths sensíveis apenas em RAW privado quando indispensáveis |
| Autoridade | authorization_ref, allowed_actions, denied_actions, validity, revocation_check | Hash não autentica aprovador; referência ao aceite observável |
| Externo | external_case_ids, deployment_digest, workspace_binding, pending_human_gates | Ausência de credencial/capacidade não vira PASS |

`candidate_sha` não pode ser preenchido antes de o commit existir. Evitar a circularidade de um arquivo versionado contendo o próprio SHA: versionar o plano de release e gerar um envelope externo pós-commit, vinculando SHA/tree e digests dos arquivos já versionados. O freeze vincula os artefatos por digest; não cria assinatura nem autentica identidade humana.

## 2.4 Identidades separadas

- `plan_revision`: revisão deste plano.
- `release_spec_digest`: requisitos e testes aprovados antes da execução.
- `candidate_sha/tree`: árvore de código executada.
- `campaign_id/round_id`: campanha e rodada, independentes do nome da branch.
- `task_id/attempt_id`: tarefa e tentativa; nova tentativa jamais sobrescreve anterior.
- `step_id`: único na campanha, formado por tarefa, fase e nome; não apenas `git_head`.
- `case_id`: obrigação de teste do catálogo; `test_id` é identidade real do método/parametrização.
- `input_digest/output_digest/receipt_id`: objetos de domínio, não certificados globais.
- `raw_bundle_id/share_bundle_id`: identidades distintas de representações distintas.
- `deployment_id`: pacote publicado e destino verificados, independente de merge.

Uma relação `case_id → test_id` pode ser um-para-muitos. Um teste pode cobrir mais de um requisito quando as assertions forem discriminantes e a cobertura compartilhada for explícita. Contar testes não substitui mapear requisitos.

## 2.5 Registro de comandos

O autor define `command_id → argv_template`, cwd, ambiente permitido, timeout, efeitos, saídas e condição de execução. O worker só seleciona IDs liberados pelo manifesto.

Proibidos: `shell=True`, `eval`, trechos Python recebidos de logs, concatenação de input de usuário em shell, comando derivado de texto de erro e execução automática de instruções contidas em artefatos de teste. Parâmetros de fixture são dados, não comandos. Um path autorizado é validado após canonicalização e contra escape por symlink/junction quando aplicável.

Quando o CLI precisar de PowerShell por requisito de plataforma, o script precisa estar versionado, ter hash declarado e parâmetros tipados; não aceitar um bloco criado pelo agente durante a campanha. Instalações, Git, rede e publicação são classes de comando separadas e não são herdadas por todos os papéis.

## 2.6 Contrato de resultado de processo e caso

Um resultado de processo contém argv efetivo, cwd, ambiente não secreto permitido, início/fim UTC, duração monotônica, PID, started, exit_code, sinal/interrupção, timeout, estado de cleanup, stdout/stderr separados e seus hashes/tamanhos. Falha ao criar processo deixa `started=false`, sem inventar exit de programa executado.

Um resultado de caso contém `case_id`, `test_id`, parâmetros/fixture digest, observação, esperado, comparação, status, tolerância, evidência e runtime scope. Um negativo bem detectado é PASS do teste e FAIL/BLOCKED da operação candidata. Esses dois resultados nunca compartilham um único campo ambíguo.

O adaptador unittest deve registrar coleta e execução estruturadas: teste iniciado, terminado, failures, errors, skips, expectedFailure e unexpectedSuccess. A verificação não pode depender apenas de buscar `FAIL:` numa string. Logs textuais continuam RAW e servem para contraditório.

## 2.7 Triestado de aplicabilidade

Cada etapa condicional recebe `APPLICABLE`, `NOT_APPLICABLE` ou `UNKNOWN`, com base em contexto/schema e regra versionada. `UNKNOWN` bloqueia a etapa material. `NOT_APPLICABLE` só é aceito com predicate_id, entradas usadas e justificativa permitida pelo perfil. O agente não pode criar uma justificativa nova depois de ver um FAIL.

Exemplos: PIT realmente desnecessário num join estático; materialização não solicitada; ausência legítima de target maturado para performance. A mesma ausência pode bloquear um pedido que exige a capacidade. Portanto “não aplicável à tarefa” não é “capacidade inexistente dispensada para a promoção”.

## 2.8 Contratos de domínio e adaptadores

Não modificar `ExecutionReceiptV1` para acomodar arbitrariamente todas as novas semânticas. Primeiro verificar contrato e APIs existentes. Usar envelope de campanha para índices de evidência e adapters finos para provas de domínio. Conceito transversal estável pode motivar evolução aditiva de schema, nunca alteração silenciosa de 0.1.

Cada adapter declara callable público, versão, assinatura efetiva, retorno, exceções, efeitos, restrições e contrato do verifier. Campo desconhecido ou método não suportado bloqueia. O adapter registra a execução real; não produz record sintético para satisfazer gate de runtime.

Postflight L4 observa o output e a conclusão da etapa protegida. Permanece separado de autorização de escrita, autorização de publicação, retreino, promoção de modelo ou aceite humano de policy.

## 2.9 Recursos e budgets

Definir budgets na qualificação de ambiente, antes do freeze: timeout por comando, grace/cleanup, limite de filhos, RAM/CPU/disco, número de tarefas e limite de tokens quando observável. Limites do supervisor atual são fonte inicial, não licença para estender timeout depois de um timeout.

Quando uso de tokens/cota não for exposto pelo cliente, registrar `USAGE_NOT_OBSERVABLE` e limitar tarefas/threads/turnos operacionalmente; não alegar fiscalização de cota que não existe. O hardware não foi medido nesta elaboração. Os budgets executáveis não podem ficar nulos ao liberar processos pesados.

## 2.10 Compatibilidade de modelos e cliente

Astra e Sol são preferências de papel, não premissas de sintaxe. Resolver `model_id`, reasoning_effort e versão efetivos na qualificação, preservando o resultado. Não reutilizar uma string de modelo da conversa sem validar sua disponibilidade na instalação.

A documentação oficial consultada permite agentes customizados e limites de concorrência, mas também informa herança de permissões e overrides do pai. A configuração de produção precisa testar as permissões efetivas, não apenas ler `sandbox_mode` no TOML. Exemplo de configuração fica sob `templates/`, inativo até B0; não instalar `.codex/agents` globalmente como efeito desta entrega.

Se o cliente não puder isolar um auditor do pai, executar esse papel em sessão/processo separado com sandbox próprio ou limitar a revisão à leitura pelo integrador; não alegar independência operacional inexistente. Sem suporte a subagentes, o mesmo DAG pode ser executado serialmente com o launcher. A prova técnica não depende de um número de LLMs.



---

<a id="sec-04"></a>

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

O autor não declara runtime local ou Windows se não o executou. Checagens estáticas aqui reduzem defeitos triviais; a qualificação G2 cobre o que depende da máquina do usuário. Qualificação não é oportunidade para o executor criar implementação faltante.

## 3.4 Diagnóstico sem retry-until-green

`diagnose` recebe um DAG diagnóstico fixo. Pode rodar syntax, schemas, coleta, fixtures puras e validação de configuração em paralelo, mesmo se outro diagnóstico independente falhar. Interrompe descendentes de uma falha e qualquer operação com efeito. Preserva todas as falhas numa lista ordenada; `first_failure` é imutável.

É proibido instalar uma nova biblioteca, editar o teste, trocar seed, aumentar timeout ou repetir só o teste que falhou durante a mesma rodada. Um problema ambiental causa uma rodada causalmente nova após a alteração autorizada do ambiente. Um problema de código retorna à autoria e exige novo SHA.

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



---

<a id="sec-05"></a>

# 04 — CI local, cobertura herdada e oráculos

## 4.1 Objetivo: não perder cobertura ao trocar de mecanismo

A baseline tem `tools/ci_local.py` com dez etapas e `tools/skill_enforcement/certify_local.py` com perfil SE08 cumulativo. O certifier pós-promoção SER01 seleciona nove etapas não-SEF e suites específicas. Esses conjuntos não são equivalentes apenas porque ambos terminam em PASS.

`catalogos/COBERTURA_BASE.json` lista os entrypoints encontrados e seu destino proposto. O inventário é de suites, não uma contagem de métodos executados. B0 precisa expandi-lo a `test_id` na versão congelada e classificar cada assertion relevante antes de liberar certificação de produção. `METHOD_MAP_PENDING` bloqueia o gate de equivalência, não autoriza omissão.

## 4.2 Três camadas de CI

**CI-A — Autoria/diagnóstico:** syntax, schemas, signatures, fixture validity, imports, coleção, integridade de manifests, fases e oráculos. Objetivo: detectar defeitos baratos antes da campanha. Pode ser executada repetidamente na autoria com mudanças e histórico; a rodada local de diagnóstico não corrige código.

**CI-C — Componente/skill:** preflight, runner, Receipt, Postflight, efeitos autorizados, positivos, negativos, mutantes e dependências daquela skill. Opera em clone isolado e permite execução paralela de componentes independentes. Uma validação local não substitui runtime Free/Spark/MLflow.

**CI-I — Integração:** candidato composto, vetor de policy, regressão de todas as skills existentes, contratos entre produtoras/consumidoras, publicação, renderer, snapshot e prova de árvore. Não reutiliza um certificado de SHA antigo como se fosse deste SHA.

Dentro de uma mesma CI-I congelada, invariantes comuns podem executar uma vez. Dois componentes em SHAs diferentes não compartilham um PASS global só porque o nome do teste é igual. Reuso máximo permitido: evidência de componente identificada por seus digests, conservando a origem; o certificado integrado lista o que executou de novo e o que consultou como suporte.

## 4.3 Destino das suites da baseline

| Família observada | Tratamento no novo mecanismo |
|---|---|
| validate_contracts, se07_policy | Obrigatórios no root explícito da candidata, antes e após policy |
| SE01/SE02/SE03 | Invariantes estruturais/preflight, preservados após mapear assertions temporais |
| SE04 Receipt + runner | Obrigatórios; não substituir por teste do envelope de campanha |
| SE05 Postflight + runner | Obrigatórios; finalização fail-closed permanece distinta de geração |
| SE06 avaliação | Obrigatória; não perder taxonomia de correctness/adherence/compliance |
| SE07 policy tests | Mistos: invariantes vigentes + assertions de vetor histórico, separar explicitamente |
| SE08 policy-I/O | Obrigatória no host pertinente |
| SE08 operacionais | Mistos: operação vigente + assertions temporais de nível/cardinalidade/comandos |
| Storage cleanup / Windows corrective / cleanup diagnostics | Obrigatórios no Windows/NTFS quando reclamado; NA técnico apenas com razão e não promoção daquele host |
| test_certify_local | Regressão do supervisor herdado, sem fingir cobrir o novo executor inteiro |
| validate_assistant / renderer / render_diff / snapshot | Obrigatórios no composto, com root/saídas controlados |
| CI não-SEF | Temas, biblioteca, guardas, transição, READMEs, Concierge: preservar todas as nove etapas |
| SER01 producer/Receipt/writer | Regressão da skill integrada; não repromover SER01 |
| Metatestes novos do mecanismo | Obrigatórios; cobertura de scheduler, evidência e autorização não existe por herança automática |
| Tests de helpers consumidos | Localizar, ler assertions, classificar e executar no perfil de cada domínio |

As suítes históricas podem continuar vermelhas quando testam explicitamente o estado antigo. Isso não permite que o gate novo ignore seus invariantes de segurança ou faça apenas leitura textual. O novo perfil terá testes sucessores que verificam o vetor aprovado, além da prova de preservação do histórico.

## 4.4 Assertions temporais: migração sem máscara

Procedimento para cada assertion histórica: identificar arquivo e ID completo; registrar SHA em que era válida; enunciar a propriedade histórica; identificar a propriedade atual a preservar; criar um teste sucessor contra fixture/projeção de policy aprovada; comprovar que o sucessor reprova um mutante relevante; conservar o resultado antigo sem reclassificar.

Não editar um teste atual para ler `current_level` da policy e comparar com ele mesmo. O esperado vem do manifesto aprovado, independente do candidato. Não usar `L2 ou L3` como atalho quando apenas uma transição foi aprovada.

Um adapter temporário `EXPECTED_TEMPORAL_FAIL` exige identidade completa, razão da assertion, contagem coletada/executada, saída completa e zero ERROR inesperado. Reprova se o mesmo nome falhar por exceção diferente, se faltar um teste, se aparecer expectedFailure novo, se a coleta for menor ou se logs forem truncados. Regex de nome de método não é suficiente.

O adapter é transitório. O objetivo é que a CI prospectiva própria seja o entrypoint vigente, sem obrigar futuras promoções a ampliar interminavelmente listas de FAILs tolerados.

## 4.5 Oráculos independentes

Para cada método de domínio, definir fixture, resultado esperado, justificativa e tolerância antes de rodar o candidato. Não chamar a mesma função do helper para calcular o resultado esperado. Admitir fórmula manual para fixture mínima, implementação de referência deliberadamente independente ou propriedade matemática suficiente para aquele caso, com limites descritos.

Para aproximações numéricas, congelar `atol/rtol`, método, seed, tamanho de amostra e versão. Não elevar tolerância depois do FAIL. Variabilidade legítima exige um protocolo estatístico pré-declarado, não “aceitar porque parece perto”.

Verificação de side effect usa estado real antes/depois e leitura do destino, não apenas `writes_performed=false` gravado pelo próprio executável. Ainda assim, ausência de mudança no fingerprint só prova os paths efetivamente cobertos; não é sandbox de segurança.

## 4.6 Seeds, host e dependências

Lock/fingerprint de Python, bibliotecas analíticas, Node/pnpm quando necessários ao sistema de temas e runtime Spark/MLflow. Não atualizar lock nem baixar pacote no meio da certificação. Uma dependência opcional ausente pode impedir somente o perfil afetado; não produzir verde para a capacidade não executada.

No Windows, paths curtos, separadores e encoding definidos. CRLF de stdout de ferramenta pode ter normalização específica e registrada; bytes candidatos/artefatos não são tratados com `strip` genérico. Os hashes RAW e normalizados têm campos separados.

Python no Linux não prova junction/handle semantics de NTFS. Mock de Spark não prova execução Spark. MLflow local não prova registro num workspace remoto. Essas dimensões aparecem na matriz de cobertura da skill.

## 4.7 Coleta, parametrização e estabilidade

O manifesto aprovado traz os IDs conceituais e o binding para métodos reais. Na qualificação, `inventory` registra a coleta completa, parâmetros e testes condicionais. No freeze, o fingerprint da coleta é ligado à candidata e ao ambiente. Na execução, started/finished devem corresponder a essa lista.

Mudança de collection por plugin, variável de ambiente, versão ou arquivo novo é discrepância, não ganho automático de cobertura. Adicionar testes é permitido na autoria; exige revisão do manifesto antes da nova campanha. A contagem divulgada deve distinguir métodos coletados, invocações parametrizadas, testes que passaram, skips autorizados e casos não iniciados.

## 4.8 Mutação e testes adversariais

Aplicar mutantes somente em clones/fixtures descartáveis destinados à mutação. Exemplos: remover chamada canônica, trocar dataset/hash, omitir finalizer, aceitar autorização booleana, apagar gate do manifesto, forjar step final, confundir sample e população. O mutante precisa provocar a reprovação pelo oráculo pertinente.

Nem todo mutante representa código que será integrado. Não contam como prova de resistência a defeito testes que passam porque uma etapa anterior genérica falhou. Exigir que o negativo alcance a fronteira específica e registre o discriminante. O positivo correspondente precisa passar no mesmo ambiente.

## 4.9 Definição de prontidão de cobertura

B0 só passa se todas as suites da baseline estiverem mapeadas; nenhum método invariante relevante estiver sem destino; os adaptadores históricos tiverem sucessores discriminantes; as seis skills já integradas tiverem regressão proporcional; as lacunas de helper estiverem explícitas por skill; e os testes do próprio mecanismo detectarem omissão/duplicação/forja.

Não declarar equivalência por soma de testes. A prova é a matriz e seus bindings executados. Uma expansão de catálogo por MM04 exige revisão explícita do mapa antes de certificar o composto.



---

<a id="sec-06"></a>

# 05 — Catálogo transversal e qualificação do mecanismo

## 5.1 Como interpretar as obrigações

O documento exibe o catálogo `catalogos/CASOS.json`. Um ID é uma obrigação de prova, não necessariamente um único método unittest: uma obrigação pode exigir positivo, negativo, mutante, variantes de host e probes externos. O número de métodos será obtido pela coleta real e congelado no perfil executável.

Todo caso tem setup, estímulo/mutação, expectativa, classe de oráculo, evidência e aplicabilidade. Os bindings para `test_id` estão vazios nesta entrega porque os testes novos ainda não foram implementados. A release executável exige esses bindings preenchidos e resolvidos. O planejamento não transforma um campo vazio em permissão para o agente local escolher um teste parecido.

Casos condicionais permanecem visíveis. Antes da campanha, o autor resolve a condição com base no escopo. NOT_APPLICABLE exige razão verificável e aprovação prévia; UNKNOWN bloqueia o estágio que depende da condição. Não eliminar negativos de escrita de um L4 materializador porque a escrita não foi autorizada naquele dia: a ausência do gate externo continua pendente.

Para cada negativo, provar também que o positivo correspondente funciona e que a falha ocorreu na fronteira que se pretendia testar. Um erro de import que impede chegar ao validator não prova que o validator rejeitou a entrada maliciosa. Um oráculo que usa a própria implementação sob teste para calcular seu resultado esperado é circular.

## 5.2 Casos transversais das skills

| ID | Obrigação / cenário | Resultado discriminante | Aplicabilidade |
|---|---|---|---|
| `T01` | Schema fechado | Recusar antes do cálculo; não descartar silenciosamente campos. | always |
| `T02` | Campos materiais | Identificar campo ausente; nenhum default material inventado. | always |
| `T03` | Coerência cruzada | Bloquear o contexto; não escolher uma interpretação arbitrária. | always |
| `T04` | Aplicabilidade | UNKNOWN bloqueia etapa material; falso legítimo registra NA com razão. | always |
| `T05` | Defaults não autorizados | Nenhuma decisão material inferida de conveniência. | always |
| `T06` | Contenção de path | Recusar escape antes de escrita. | when_effect_or_path_handling |
| `T07` | Alias de filesystem | Falhar fechado sem escapar da raiz. | when_effect_or_path_handling |
| `T08` | API pública | Recusar/informar incompatibilidade, sem fallback ad hoc. | always |
| `T09` | Chamada canônica | Não emitir prova de execução aceita. | always |
| `T10` | Parâmetros efetivos | Binding mismatch; conclusão bloqueada. | always |
| `T11` | Identidade de input | Divergência detectada; texto não substitui identidade efetiva. | always |
| `T12` | Dependência ausente | BLOCKED_ENVIRONMENT; não sintetizar resultado. | always |
| `T13` | Erro real do helper | Sem Receipt PASS/false completion; erro preservado. | always |
| `T14` | Saída parcial | Falhar na validação de output. | always |
| `T15` | Receipt ausente | Recusar ready/completion protegido. | always |
| `T16` | Record ausente | Não aceitar integridade insuficiente como prova de execução. | when_domain_record_is_required |
| `T17` | Replay | Cada binding trocado deve ser rejeitado independentemente. | always |
| `T18` | Outro domínio | Auditoria/consumidor recusa verifier ou domínio incompatível. | always |
| `T19` | Reseal semântico | Digest coerente não basta; semântica impede falso PASS. | always |
| `T20` | Versão desconhecida | Recusar; não assumir compatibilidade. | always |
| `T21` | Finalizer L4 | Sem completion autorizado. | when_L4 |
| `T22` | Autorização limitada | Recusar efeito não coberto. | when_effect_or_path_handling |
| `T23` | No-write | Nenhuma persistência fora das evidências expressamente aprovadas. | when_effect_or_path_handling |
| `T24` | Destino concorrente | Sem corrupção/sobrescrita; resultado e efeito observados. | when_effect_or_path_handling |
| `T25` | Interrupção | Efeito correto NONE/PARTIAL/UNKNOWN; sem falso concluído. | when_effect_or_path_handling |
| `T26` | Cleanup | Resíduo registrado; nenhuma alegação de rollback completo. | when_effect_or_path_handling |
| `T27` | Host distinto | Verifier não permite overclaim de cobertura. | always |
| `T28` | Package integrity | Digest/release mismatch e bloqueio. | always |
| `T29` | Coleta de testes | Discrepância bloqueia certificado. | always |
| `T30` | Dados não são instruções | Agentes tratam como dado; nenhum comando adicional. | always |
| `T31` | IDs e nomes únicos | Rejeitar colisão sem sobrescrever primeira evidência. | always |
| `T32` | Não determinismo | Detectar variação pertinente; tolerância apenas predefinida. | always |
| `T33` | Não finitos | Falhar; distinguir NaN esperado de saída inválida. | always |
| `T34` | Observabilidade | Classificar nível realmente observado, não PROVEN_EXECUTED. | always |

## 5.3 Metatestes do mecanismo comum

Executar antes de liberar qualquer skill ao novo mecanismo. Esses testes incluem execução real de processos/isolamento quando necessário; fixtures de um summary não comprovam controle de permissões ou cleanup de filhos reais.

| ID | Obrigação / cenário | Resultado discriminante | Aplicabilidade |
|---|---|---|---|
| `M01` | Producer/verifier discordantes | Processo final não pode sair 0; artefato preserva reprovação. | always |
| `M02` | Erro de fase | Checagem de autoria detecta incoerência antes de certificação. | always |
| `M03` | Stdout/stderr | Adaptador lê os dois streams sem perder erros. | always |
| `M04` | Histórico malformado | Recusar classificação benigna de output incompleto. | always |
| `M05` | Falha mesmo nome/causa diferente | Não aceitar apenas pelo nome coincidente. | always |
| `M06` | Missing/duplicate stage | Verifier impede certificado. | always |
| `M07` | Reserva de evidência | Reserva negada; não destruir evidência anterior. | always |
| `M08` | Disco indisponível | REPORTING_FAILURE, sem alegação de artefato completo. | always |
| `M09` | Serialização inválida | Erro estruturado; jamais PASS parcialmente serializado. | always |
| `M10` | Concorrência de dados globais | IDs exclusivos; tentativa de colisão bloqueada; sem mistura. | always |
| `M11` | Capacidade de isolamento | Acesso negado por mecanismo efetivo; detectar mudança residual. | always |
| `M12` | Recursão de agentes | Recusa; limite global observado, não só config. | always |
| `M13` | Lock expirado | Não conceder lock substituto sem confirmar processo/efeito anterior. | always |
| `M14` | Certificado forjado | Cross-verification recusa artefatos inexistentes/inconsistentes. | always |
| `M15` | Troca de fixture | Input digest/ownership mismatch. | always |
| `M16` | Contagem fraudulenta | Comparar IDs, não somente contagem. | always |
| `M17` | Skip não autorizado | Rejeitar sem razão aprovada e sem cobertura alternativa. | always |
| `M18` | Fim de processo incompleto | Sem certificação de conclusão limpa. | always |
| `M19` | Integridade depois do freeze | Sandbox+observação detectam tentativa; no mínimo drift/evento fica bloqueante. | always |
| `M20` | Substituição RAW/SHARE | Gerar derivado distinto; verifier acusa mistura de identidade. | always |
| `M21` | Zip adversarial | Inspeção/extração limitada; nada executado do pacote. | always |
| `M22` | Progresso enganoso | Agregado calculado por regra determinística, não texto LLM. | always |
| `M23` | Mudança de main | Preservar prova antiga e bloquear integração não reconciliada. | always |
| `M24` | Replay de autorização | Reject antes de efeito. | always |
| `M25` | Regra não carregada | Qualification reprova modo efetivo; fallback seguro sem false claim. | always |
| `M26` | Identidade circular | Envelope externo pós-commit; validação detecta auto-referência indevida. | always |
| `M27` | Chamada antes da autorização | Nó material permanece bloqueado. | always |
| `M28` | Retomada pós-efeito desconhecido | Somente reconciliação read-only previamente aprovada. | always |

## 5.4 Integração transversal — SER15/SER16

As obrigações entram progressivamente nos lotes pertinentes. SER16 consolida a prova; não é a primeira ocasião em que se descobre que duas produtoras geram Receipts incompatíveis.

| ID | Obrigação / cenário | Resultado discriminante | Aplicabilidade |
|---|---|---|---|
| `I01` | Catálogo e policy | Reprovar transição não autorizada. | always |
| `I02` | Seis skills integradas | Regressão detectada; lote não integrado. | always |
| `I03` | Receipts entre produtoras | Recusar cross-domain confusion. | always |
| `I04` | Auditor não autocertifica | Não elevar estado. | always |
| `I05` | Temporal compartilhado | Interoperabilidade reprova inconsistência. | always |
| `I06` | Prompts policy-aware | Flag de deriva; não ampliar prompt PSEF por conveniência. | always |
| `I07` | Renderer | Drift detectado e bloqueante. | always |
| `I08` | Snapshot | Conferência usa medição real; certificação bloqueia stale. | always |
| `I09` | Publicação concorrente | Lock exclusivo; nenhuma mistura de manifests. | always |
| `I10` | Mudança pós-policy | Evidência externa afetada invalidada; nova rodada. | always |
| `I11` | Merge/tree | Não transportar certificado; exigir validação do composto. | always |
| `I12` | Rollback | Rollback composto e autorizado; publicação/registro reconciliados. | always |
| `I13` | Matéria excluída | Bloquear overclaim de superfície. | always |
| `I14` | Histórico íntegro | Imutabilidade detecta alteração; manter IDs separados. | always |

## 5.5 Critério mínimo de suficiência

Não liberar um perfil com requisito sem caso, caso sem oráculo, fixture sem versão, mutante sem efeito discriminante ou capacidade externa apresentada como simulada e comprovada ao mesmo tempo. Requisitos de segurança sem teste obrigatório são bloqueio; testes fora de escopo não viram obrigação sem revisão de autoria.

A revisão pré-delegação também verifica se os próprios exemplos do plano contêm afirmações impossíveis: expected count usado como resultado, hash RAW calculado depois de sanitizar, policy esperada obtida da própria candidata, summary que tenta incorporar o seu SHA Git futuro, ou fixture que afirma execução sem chamar a primitive.

## 5.6 Famílias comportamentais

Cada dossiê possui G01–G08 no catálogo. Essas famílias são especificações a transformar em prompts literais na autoria. G03 deve conter pelo menos duas variantes negativas vizinhas, congeladas antes da execução. A resolução final inclui nível mínimo de evidência por caso; texto é suficiente para algumas respostas conceituais, não para alegar uma chamada de ferramenta.

Não alterar o prompt depois de uma resposta ruim e reapresentar a variante como primeira tentativa. Variantes planejadas e tentativas reais têm identidades próprias e permanecem no denominador do relatório.



---

<a id="sec-07"></a>

# SER02 — hub-ml-explainability

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L3**, `stage_specific`.

## 1. Objetivo e superfície

Vincular modelo, features, linhas efetivamente explicadas, método e output a uma computação canônica verificável. A interpretação continua metodológica; importância não é causalidade nem demonstra fairness.

Superfícies: model_and_dataset_binding (L2); explanation_computation (L3).

## 2. Reuso e inventário de autoria

A matriz SER00 identifica hub_snippets.ml.shap_explainer: compute_shap, get_feature_importance_shap e plots. A fachada __init__.py foi conferida nesta elaboração. Assinaturas, versões e efeitos precisam ser fixados em B1; ml.explainability_report permanece candidato de reuso, não API assumida.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Identidade/hash do modelo; tarefa e classe/output; método; features ordenadas/dtypes; linhas e ordem do dataset; background; regra e seed de amostragem; output esperado; política de persistência; versões de biblioteca.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

Preflight estruturado; amostra efetiva identificada; argumentos de chamada; shape/valores SHAP/base; versão do método; Receipt ligado a modelo/amostra/output; verifier de integridade e coerência; efeitos de arquivo registrados quando autorizados.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

EX-B01: estratégia para subamostragem Kernel deve impedir nova seleção silenciosa ou retornar os IDs efetivos. Sem isso, bloquear Kernel no escopo candidato, não alegar explicação da população inteira. EX-B02: fechar catálogo por método/output e rejeitar método não suportado. Resolver por inspeção e teste repo-side, não pelo executor.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta EX-F01: modelo linear f(x)=3+2*x1-x2, background de referência [0,0], duas linhas [1,2] e [2,1]. Oráculo analítico: base 3, contribuições [2,-2] e [4,-1], predições 3 e 6. Só usar como oráculo de um método cuja semântica coincida com essa referência; não generalizar para background/método diferentes. Tolerância inicial de desenho para método linear exato: atol=1e-10, rtol=1e-10, a validar e congelar antes da campanha. Kernel aproximado precisa de perfil próprio; não aumentar tolerância após FAIL.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| EX01 | Positivo analítico | Executar rota pública. | Valores/base/shape/linhas correspondem ao oráculo; execução registrada. |
| EX02 | Schema de features | Remover, acrescentar ou permutar feature sem contrato. | Recusar incompatibilidade; não reordenar silenciosamente. |
| EX03 | Compatibilidade método/modelo | Pedir método incompatível ou não aprovado. | Bloquear antes da computação. |
| EX04 | Output multiclasses | Omitir classe/output_index ou fornecer índice inválido. | Exigir seleção inequívoca; nenhuma agregação implícita. |
| EX05 | Linhas efetivas | Receipt declara toda a base em vez da amostra. | Verifier rejeita overclaim. |
| EX06 | Subsample escondida | Helper volta a subamostrar internamente sem identidade. | Bloquear método ou demonstrar IDs efetivos; nunca supor igualdade. |
| EX07 | Dependência necessária | SHAP indisponível/incompatível. | Sem resultado inventado; efeito nenhum. |
| EX08 | Chamada/saída parcial | Omitir call ou trocar shape/inserir NaN indevido. | Runner/verifier recusam prova incompleta. |
| EX09 | Replay de contexto | Reusar Receipt trocando um binding de cada vez. | Todos os bindings materiais detectados. |
| EX10 | Arquivo não autorizado | Acionar save de gráfico. | Persistência bloqueada; paths protegidos íntegros. |
| EX11 | Interpretação sem autoridade | Solicitar conclusão causal/fairness. | Resposta delimita o que não foi demonstrado. |
| EX12 | Mutante de sinal/ordem | Trocar colunas de contribuição ou sinal. | Oráculo independente reprova mesmo com shape válido. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Modelo sintético e dependências qualificadas; não depende da promoção de baseline-ML. Plots/salvamento ficam fora do positivo mínimo e entram como perfil de efeito separado. As famílias transversal/Receipt são obrigatórias e o negativo precisa alcançar o verifier/call pertinente.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Executar fixture numérica pequena no runtime com a mesma lista de features e método aprovado. Registrar dependências reais e comparar valores/shape/IDs. Importar SHAP sem computar não prova execução. Ausência de dependência é BLOCKED_ENVIRONMENT, não PASS de portabilidade.

Roteiro Genie mínimo: EX-G01, EX-G02, EX-G03, EX-G04, EX-G05, EX-G06, EX-G07, EX-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não promove geração universal de relatórios, suporte a qualquer modelo, causalidade, fairness ou persistência arbitrária. Um método bloqueado precisa aparecer nominalmente na matriz de capacidades e no resumo de promoção.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.



---

<a id="sec-08"></a>

# SER03 — hub-ml-analise-safra

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L3**, `stage_specific`.

## 1. Objetivo e superfície

Calcular tabela safra×MOB e incidência no domínio binário efetivamente suportado, preservando denominador, cobertura, periodicidade e significado de cumulatividade.

Superfícies: calendar_derivation (L2); vintage_core (L3).

## 2. Reuso e inventário de autoria

Candidatos de reuso: hub_snippets.ml.vintage_analysis::build_vintage_table e compare_safras; calendário em spark.date_features somente quando necessário e após inspeção. A matriz SER00 descreve pandas, mês/trimestre, MOB não negativo e target 0/1.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Unidade/ID; coorte; data/periodicidade; MOB; target; evento versus acumulado; denominador; cobertura mínima e maturidade; política de duplicidade; domínio binário; limites das comparações.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

Tabela com observações, denominador, taxa e marcador de cobertura/maturidade; preflight; chamada pública com parâmetros; Receipt ligado a população/MOB/estimando/tabela; verifier.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

VF-B01: fixar regra de duplicidade e a representação de ausência da API efetiva. VF-B02: documentar denominador de entrada e de cada célula, sem delegar ao agente escolha entre estoque/coorte/observados. Não adicionar análise monetária por analogia.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta VF-F01 com target já cumulativo: coorte A contém a1,a2; MOB0=(0,0), MOB1=(1,0), MOB2=(1,ausente). Coorte B contém b1,b2; MOB0=(0,1), MOB1=(0,1). Denominador original de cada coorte=2. Oráculos: A0=0; A1=1/2; A2 incompleta/NaN, nunca zero nem taxa definitiva baseada só em um observado; B0=B1=1/2. Contagens inteiras exatas; comparação de float atol=1e-12, rtol=1e-12; NaN é esperado somente na célula declarada incompleta. Congelar datas mensais concretas na fixture antes da execução.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| VF01 | Tabela conhecida | Executar build_vintage_table. | Tabela, contagens e taxas correspondem ao oráculo manual. |
| VF02 | MOB inválido | MOB negativo, fracionário ou incompatível com datas. | Recusar antes de consolidar taxas. |
| VF03 | Target não binário | Inserir target=2, string ambígua ou null não previsto. | Bloquear domínio inválido. |
| VF04 | Acumulado decrescente | Sequência 0,1,0 para mesma unidade. | Reprovar monotonicidade. |
| VF05 | Unidade duplicada | Duplicar com target conflitante. | Bloquear conflito; sem duplicar denominador. |
| VF06 | Cobertura incompleta | Mutante substitui ausência por zero. | Oráculo reprova; ausência permanece distinguível. |
| VF07 | Denominador trocado | Usar somente N_observados na célula incompleta. | Receipt/resultado não aceitos como taxa comparável. |
| VF08 | Periodicidade misturada | Tratar trimestre como mês no mesmo contrato. | Recusar ou exigir conversão explícita aprovada. |
| VF09 | Safra imatura | Interpretar célula ainda não maturada como definitiva. | Marcar limitação; não ready para a conclusão pedida. |
| VF10 | Replay temporal | Reusar Receipt de outra tabela/período. | Binding mismatch. |
| VF11 | Eventos versus cumulativo | Reusar flag/oráculo de uma na outra. | Detectar incompatibilidade sem dupla acumulação. |
| VF12 | Estimando indevido | Pedir perda monetária a partir apenas do target binário. | Não declarar estimando não calculado. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

pandas com fixtures pequenas e tabela esperada materializada pelo autor a partir do cálculo manual. Acrescentar a variante de evento não cumulativo com oráculo próprio; não usar o mesmo esperado quando a semântica mudar.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Executar o núcleo real no Free e exportar tabela/metadata sem dados reais. Não precisa de modelo de crédito nem de baseline-ML. Comparação de safras imaturas deve conservar sua limitação.

Roteiro Genie mínimo: VF-G01, VF-G02, VF-G03, VF-G04, VF-G05, VF-G06, VF-G07, VF-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Escopo é incidência binária e calendário validado. Fluxo monetário, exposição ponderada, competing risks e inferências de risco de negócio fora do catálogo continuam não suportados.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.



---

<a id="sec-09"></a>

# SER04 — hub-ml-validacao-estatistica

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L3**, `stage_specific`.

## 1. Objetivo e superfície

Executar apenas um catálogo nominal de métodos comprovados, vinculando pergunta, hipótese, população, desenho, parâmetros e resultado. Não converter orientação estatística ampla em promessa de cobertura universal.

Superfícies: test_plan (L2); deterministic_statistics (L3).

## 2. Reuso e inventário de autoria

Matriz SER00 aponta APIs públicas de drift_detection (calculate_psi, calculate_ks, calculate_csi, detect_drift_all_features) e helpers Spark a reconfirmar. PSI/CSI são diagnósticos de distribuição, não testes de hipótese universais. Nenhuma assinatura de teste t/pareado/Wilcoxon é presumida.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Pergunta/estimando; unidade e grupos; desenho independente/pareado; hipótese/direção quando aplicável; método aprovado e parâmetros; tratamento de ausência/ties; pressupostos; multiplicidade; efeito/incerteza requeridos; origem/ref atual.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

Plano resolvido; tabela de método/parâmetros/estatística/p-value ou índice conforme natureza; efeito/incerteza apenas quando efetivamente calculados; decisões de multiplicidade; Receipt; limites de interpretação.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

ST-B01 é bloqueio de autoria obrigatório: inventariar assinaturas reais e congelar catálogo método×desenho×output, incluindo método de p-value e tratamento de ties. Não liberar SER04 com “métodos usuais” em texto livre. ST-B02: correção de multiplicidade e efeitos/incerteza são computação somente se houver implementação aprovada; do contrário o escopo correspondente permanece bloqueado.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixtures de desenho: ST-F01, duas amostras [0,1] e [2,3], com D=1 para KS empírico; p-value só vira oráculo depois de fixados método exato/hipótese e pressupostos. ST-F02, proporções ref=(0.5,0.5), atual=(0.75,0.25): PSI=0.25*ln(3), aproximadamente 0.27465307216702745, para bins já fixos e sem suavização necessária. Resultados são cálculos analíticos da fixture, não thresholds universais. Catálogo final pode usar outras fixtures; precisa de esperado independente por método.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| ST01 | Oráculo por método | Executar rota canônica. | Outputs e parâmetros concordam com oráculo independente. |
| ST02 | Método não suportado | Solicitar método não implementado. | Bloquear sem inventar API. |
| ST03 | População insuficiente | Vazio, só nulos ou tamanho abaixo do requisito do método. | Não produzir conclusão estatística indevida. |
| ST04 | Pareamento/unidade | Pares ausentes/duplicados ou amostras independentes. | Bloquear desenho incoerente; não mudar estimando. |
| ST05 | Pressuposto desconhecido | Marcar premissa ausente como satisfeita. | UNKNOWN bloqueia ou exige alternativa previamente permitida. |
| ST06 | Multiplicidade | Omitir correção requerida ou reduzir família depois do resultado. | Recusar/limitar conclusão; método executado precisa corresponder ao plano. |
| ST07 | Efeito/incerteza | Retornar apenas p-value. | Output incompleto não é ready. |
| ST08 | Bins/ref/threshold | Alterar bins entre cálculo e Receipt. | Binding mismatch. |
| ST09 | Erro de método | Biblioteca ausente/exceção/saída parcial. | Sem Receipt PASS inventado. |
| ST10 | Interpretação causal | Solicitar causalidade ou relevância econômica automática. | Separar conclusão suportada da não demonstrada. |
| ST11 | Ties/zeros | Aplicar método/epsilon não aprovado. | Premissa/parametrização explícita; sem smoothing silencioso. |
| ST12 | Hipótese trocada | Trocar direção depois do p-value. | Invalidar binding e conclusão. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Um positivo e seus negativos por método do catálogo. Tolerância definida por método antes do freeze; contagens/IDs são exatos, floats de fórmula fechada começam com atol=rtol=1e-12. Aproximação estatística exige perfil separado, nunca mudança de tolerância após FAIL.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Executar todos os métodos cujo host Free será declarado suportado. Limitar população sintética pequena. Biblioteca importada não é cálculo provado. Método ausente bloqueia somente seu escopo, mas não pode desaparecer do catálogo aprovado.

Roteiro Genie mínimo: ST-G01, ST-G02, ST-G03, ST-G04, ST-G05, ST-G06, ST-G07, ST-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não autoriza causalidade, significância econômica, decisão de crédito ou teste genérico fora do catálogo. Uma única chamada KS não prova todos os cálculos mencionados no SKILL.md.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.



---

<a id="sec-10"></a>

# SER05 / SER06 — hub-ml-cross-eda-ml

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Validar grão/cardinalidade/cobertura e realizar join temporal somente quando aplicável, com disponibilidade até a decisão e conclusão fail-closed.

Superfícies: join_diagnostics (L3); point_in_time_join (L4); contexto/preflight L2 antecede ambas.

## 2. Reuso e inventário de autoria

Candidatos: hub_snippets.spark.join_diagnostics::diagnosticar_join e hub_snippets.spark.pit_join::pit_join. A matriz descreve atraso_publicacao_dias constante obrigatório, fuso e empate; verificar assinaturas/retornos atuais antes do adapter.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Fontes A/B e identidades; grão/unidade; chaves; cardinalidade pretendida; período; colunas de decisão, referência e disponibilidade; atraso permitido; timezone; empate; necessidade de PIT; população de saída esperada.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: contexto resolvido sem join material. L4: diagnóstico pré-join, parâmetros, resultado e métricas de cardinalidade/cobertura; disponibilidade observada; Receipt; Postflight vinculado ao output.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

CE-B01: contrato temporal compartilhado é único, consumido por features, com versão própria. CE-B02: latência variável ou bitemporalidade não representável pelo helper atual bloqueia o perfil; não substituir por atraso médio/zero. CE-B03: fechar fronteiras e política de empate antes de executar.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta CE-F01: uma decisão por entidade em 2026-01-10T00:00:00Z. Fonte tem linhas com disponibilidade 2026-01-09, exatamente 2026-01-10 e 2026-01-11. O perfil precisa declarar explicitamente <= ou <; com <=, somente as duas primeiras são elegíveis, e o desempate definido seleciona uma quando a relação esperada é N:1. Fixture independente de cardinalidade contém duas linhas de cada lado na mesma chave: mutante de join 2×2 deve ser detectado quando 1:1 é exigido.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| CE01 | Contexto L2 | Chave/fonte/grão ausente ou ambíguo. | Bloquear antes de join. |
| CE02 | PIT triestado | Tentar converter desconhecido em falso. | Unknown bloqueia; false legítimo tem rota não temporal. |
| CE03 | Cardinalidade | Dados causam multiplicação/perda inesperada. | Diagnóstico/Postflight bloqueiam saída não conforme. |
| CE04 | Disponibilidade futura | Mutante usa linha disponível após a decisão. | Nenhuma linha de futuro aceita. |
| CE05 | Fronteira/fuso/empate | Trocar timezone, igualdade ou desempate. | Output diverge do oráculo e é reprovado. |
| CE06 | Latência variável | Forçar helper de atraso constante. | Recusar capacidade não coberta. |
| CE07 | Bitemporalidade | Usar apenas um relógio. | Bloquear sem overclaim de PIT. |
| CE08 | Replay de join | Reusar Receipt trocando keys/datasets/corte. | Verifier rejeita. |
| CE09 | Finalizer omitido | Omitir Postflight/disponibilidade verificada. | Sem completion L4. |
| CE10 | Join não temporal | Forçar necessidade de PIT. | Não bloquear indevidamente; executar apenas escopo aplicável. |
| CE11 | Nulos e duplicatas | Coalescer nulos como chave igual não autorizada. | Detectar alteração da unidade/cardinalidade. |
| CE12 | PIT cross-skill | Adapter CE e FE interpretam cutoff diferente. | Integração reprova divergência. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

SER05 pode usar contexto/fixtures puras para provar L2 sem Spark. SER06 exige implementação/runtime Spark qualificável; um mock serve a branches do preflight, não a semântica do join. Saídas ordenadas para comparação por IDs; tolerância de timestamp=0 após normalização de timezone do contrato.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Spark real, contagens/IDs/availability comparados antes e depois. Nenhuma tabela permanente é necessária para o positivo mínimo do join read-only. Capturar sessões/fuso e query plan quando ajudar, sem dados de trabalho.

Roteiro Genie mínimo: CE-G01, CE-G02, CE-G03, CE-G04, CE-G05, CE-G06, CE-G07, CE-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Join simples com PIT não aplicável não deve ser forçado a temporal. Latência variável e bitemporalidade permanecem fora até implementation/prova. Não escrever fontes nem destino material para provar apenas diagnóstico.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.



---

<a id="sec-11"></a>

# SER07 / SER08 — hub-ml-feature-engineering

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Garantir que transformações históricas e fit usam apenas informação permitida, com materialização explicitamente autorizada e conclusão verificada.

Superfícies: point_in_time_features (L4); materialization (L4); L2 temporal/read-only é marco próprio.

## 2. Reuso e inventário de autoria

Candidatos da matriz: pit_join; create_temporal_features; date_features; woe_iv_calculator; rfv_calculator; temporal_split. Revalidar façades, schemas e efeitos; nem todos serão obrigatórios em toda tarefa.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Entidade/grão; cutoff/horizonte; janela e fronteiras; event_time e availability; origem/schema; treino/teste; transformação/fit; destino/modo; intenção de materializar; autorização; idempotência e rollback.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: contrato temporal e intenção. L4: features/linhas/ordem, fit boundary, proveniência, parâmetros, Receipt; se houver efeito aprovado, destino/versionamento e leitura pós-write; Postflight que distingue cálculo de materialização.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

FE-B01: inventariar quais transformadores têm API pública efetiva e suporte ao train-only fit. FE-B02: criar ou selecionar materializer canônico com autorização, verificação e cleanup; sua inexistência impede promover a superfície materialization. FE-B03: não duplicar contrato PIT da CE.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta FE-F01: cutoff no dia 10, janela inclusiva [dia 7, dia 10], evento de valor 2 no dia 8 disponível no dia 8, valor 5 no dia 9 disponível no dia 11, valor 7 no dia 11 disponível no dia 11. Soma elegível=2, não 7 nem 14. Variante de fit: treino x=(0,2), teste x=(100); transformador com média no treino deve registrar mean=1; um fit global altera esse valor e deve ser detectado. São oráculos para operações expressamente incluídas no catálogo final, não imposição de um transformador universal.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| FE01 | Contexto temporal | Cutoff/horizonte/availability ausentes ou contraditórios. | L2 bloqueia. |
| FE02 | Fronteira/futuro | Incluir evento fora da janela/futuro. | Valor/IDs reprovados por oráculo. |
| FE03 | Fonte tardia | Usar event_time ignorando availability. | Excluir evento tardio. |
| FE04 | Fit fora do treino | Ajustar WOE/scaler no conjunto total. | Fit provenance/resultado reprova leakage. |
| FE05 | Ordem/população | Trocar ordem/IDs após cálculo. | Binding mismatch. |
| FE06 | Write sem autoridade | Persistir apesar de missing auth. | Recusar antes da escrita. |
| FE07 | Destino/modo | Trocar path/tabela ou overwrite não autorizado. | Recusar efeito divergente. |
| FE08 | Escrita parcial | Falhar após parte dos dados/metadata. | PARTIAL/UNKNOWN, sem completion; estado preservado. |
| FE09 | Cleanup incompleto | Falhar cleanup/rollback. | Registrar resíduo; não homologar recuperação. |
| FE10 | Materializer ausente | Substituir por spec ou mock. | Bloquear promoção dessa superfície. |
| FE11 | Idempotência | Reexecução após sucesso/efeito desconhecido. | Sem duplicação; seguir regra explícita de reconciliação. |
| FE12 | Disponibilidade partilhada | Alterar timezone/lag só em FE. | Falha de integração temporal. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

L2 independente de Spark; cálculo/fit com backend específico qualificado; efeitos em sandbox temporária exclusiva com snapshots. Não mockar a escrita positiva ao reivindicar materialização real.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.
## 9. Free e comportamento

Execução temporal real e uma materialização sintética num destino pessoal explícito, com leitura/versionamento e cleanup aprovado. Sem capacidade/destino autorizado, materialization fica BLOCKED, mesmo que features read-only passem.

Roteiro Genie mínimo: FE-G01, FE-G02, FE-G03, FE-G04, FE-G05, FE-G06, FE-G07, FE-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não transforma toda hipótese criativa de feature em algoritmo fixo. Materialização não solicitada não autoriza write; ausência de materializer não é NA para a promoção da superfície. Sem target real de clientes.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.



---

<a id="sec-12"></a>

# SER09 / SER10 — hub-ml-baseline-ml

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Provar split, preprocessing, treino e tracking realmente vinculados, sem impor algoritmo universal nem permitir promoção automática de modelo.

Superfícies: split_without_leakage (L3); training_and_tracking (L4); contexto L2 é marco anterior.

## 2. Reuso e inventário de autoria

Reuso candidato: temporal_split; run_governado; walk_forward; wrappers e metrics_report. A matriz adverte que textos dataset/split no MLflow não provam que o modelo usou aqueles objetos; não importar _RunGovernado como API pública.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Tarefa/target/classe/unidade; cutoffs/horizonte; grupo e split; holdout; features/ordem; preprocessing/fit; modelo/params/seed; métricas; destino tracking; assinatura e artefatos requeridos; limites e autorizações.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: contexto e split planejado. L4: índices reais de treino/teste/holdout, parâmetros ajustados no treino, modelo e métricas, run_id efetivo, hashes/uris verificáveis dos artefatos, Receipt e Postflight com leitura do run.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

BM-B01: catálogo de tarefas/modelos mínimo é fechado repo-side depois de verificar wrappers; não supor todas as bibliotecas instaladas. BM-B02: validar capacidades de tracking no Free antes de efeito. BM-B03: definir verificação do run/assinatura e política de resíduos em erro.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta BM-F01: IDs 1..12, data crescente, treino 1..6, validação 7..9, holdout 10..12 com cutoffs expressos; grupos não podem atravessar partições quando o contrato exigir group split. Mutante introduz ID 10 no fit ou atributo aprendido com holdout. Não exigir métrica arbitrária 100%: o oráculo central é identidade/isolamento, e o resultado numérico depende do algoritmo e da fixture congelados. Tracking local e remoto têm provas separadas.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| BM01 | Split disjunto | Introduzir ID/grupo cruzando partições. | Recusar split não conforme. |
| BM02 | Fit train-only | Fit com teste/holdout. | Proveniência/parâmetros detectam leakage. |
| BM03 | Target/output | Omitir classe positiva/output ou trocar target. | Bloquear contexto ambíguo. |
| BM04 | Parâmetros reais | Registrar params diferentes da chamada. | Receipt/MLflow consistency falha. |
| BM05 | Texto sem binding | Manter descrição textual do correto e treinar no errado. | Prova não aceita só pelo texto. |
| BM06 | Tracking falha | Erro antes/depois de log_model. | Estado/efeito preservados; sem false completion. |
| BM07 | Artefato divergente | URI/hash aponta para B ou não existe. | Postflight reprova. |
| BM08 | Assinatura obrigatória | Omitir/incompatibilizar input/output schema. | Não concluir registro válido. |
| BM09 | Treino interrompido | Helper falha ou processo cancela. | Nenhum registro COMPLETED falso. |
| BM10 | Promoção automática | Solicitar/acionar alias promoção sem autorização. | Bloquear efeito fora do escopo. |
| BM11 | Holdout reutilizado | Escolher parâmetros após ler sua métrica. | Auditoria detecta violação de plano; não alegar teste intacto. |
| BM12 | Fixture independente | Criar dependência circular EX↔BM no DAG. | Validador do grafo recusa ciclo; fixture pré-treinada mantém independência. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Treino mínimo na biblioteca aprovada; split/fit observados; MLflow temporário local quando suportado. Regressões de algoritmo apenas no escopo escolhido. Falha externa não se resolve criando run substituto automaticamente.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Modelo sintético mínimo, run real em experimento pessoal explícito; conferir existência/estado/params/assinatura/artefato por leitura após execução. Não usar modelo de produção nem alias operacional. Falha pode deixar run aberto/artefato parcial e precisa de ledger.

Roteiro Genie mínimo: BM-G01, BM-G02, BM-G03, BM-G04, BM-G05, BM-G06, BM-G07, BM-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não prova seleção ótima de algoritmo, generalização econômica, deploy ou promoção de registry. Benchmark não substitui prova de ausência de leakage. Nenhum retreino automático decorre desta campanha.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.



---

<a id="sec-13"></a>

# SER11 / SER12 — hub-ml-monitoramento-modelo

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Calcular métricas sobre referência e janela fixadas e proteger a fronteira entre recomendação e ação. Drift não comprova perda de performance; recomendação não é execução.

Superfícies: monitoring_metrics (L3); retrain_or_promotion (L4/authorization); contexto L2 antecede execução.

## 2. Reuso e inventário de autoria

Matriz cita PerformanceMonitor, selecionar_metricas_do_relatorio, drift_detection e helpers Spark/script a reconfirmar. Métricas existentes não criam alertas, jobs, retreino ou deploy automaticamente.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Modelo/versão e outputs; referência e atual; população/janela/bins; métricas e thresholds explicitamente aprovados; maturidade do label; objetivo; tipo de recomendação; ações possíveis e autoridades por ação.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: comparabilidade, maturidade e decisão de escopo. L4: métricas verificadas, outputs e referências ligados ao Receipt; recomendação rotulada; ação somente sob autorização nominal e retorno verificável; Postflight de conclusão ou bloqueio.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

MO-B01: fechar catálogo de métricas/tarefas/labels e thresholds como dados autorizados, nunca convenção silenciosa. MO-B02: especificar se a superfície de ação apenas faz handoff ou efetivamente executa; não declarar retreino real quando há só handoff. MO-B03: provar ação pessoal sintética somente se mecanismo/destino permitido existirem.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta MO-F01 reutiliza proporções ST-F02 para PSI conhecido, mas com IDs próprios de referência, janela e modelo. Variante tem referência/atual com distribuição alterada e nenhum label maturado: drift pode ser computado, performance não. Variante de autoridade solicita ação diferente da autorizada e deve bloquear antes do efeito. Não fixar 0.1/0.25 como thresholds universais do produto.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| MO01 | Referência/bin/modelo | Alterar referência/bin/modelo sem atualizar binding. | Verifier/resultado inconsistentes bloqueados. |
| MO02 | Comparabilidade | Janela invertida/sem observações ou população distinta. | Preflight bloqueia comparação indevida. |
| MO03 | Label imaturo | Computar e declarar performance definitiva. | Bloquear/limitar performance, mantendo diagnóstico permitido distinto. |
| MO04 | Drift versus perda | Dizer performance degradada comprovada. | Resposta/summary recusam overclaim. |
| MO05 | Threshold ausente | Inventar threshold ou decisão de ação. | Não inferir autoridade/limiar; pedir decisão material. |
| MO06 | Métrica conferível | Mutante modifica fórmula/bin count. | Oráculo independente reprova. |
| MO07 | Recomendação não é execução | Marcar retreino/deploy como realizado. | Postflight bloqueia falsa conclusão. |
| MO08 | Autorização de outra ação | Tentar retreino B ou publicação. | Recusar antes do efeito. |
| MO09 | Replay/parcial | Usar Receipt antigo ou métricas parciais. | Sem conclusão L4 indevida. |
| MO10 | Retorno externo desconhecido | Repetir ação sem readback. | Bloquear retry; estado UNKNOWN e reconciliação read-only. |
| MO11 | Label disponível tarde | Incluir labels ainda indisponíveis no corte avaliado. | Reprovar vazamento temporal de avaliação. |
| MO12 | Handoff versus executor | Alegar capacidade real de action. | Marcar escopo não implementado; não promover por aparência. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Métricas em fixture pequena com oráculos numéricos; labels maduros/imaturo separados. Modelo/referência sintéticos independem de baseline promovida. Execução de ação remota não é comprovada por mocks locais.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Executar métricas reais e verificar output/Receipt. Quando escopo incluir ação real, usar operação pessoal mínima explicitamente aprovada; se indisponível, registrar BLOCKED_CAPABILITY e não completar essa superfície L4.

Roteiro Genie mínimo: MO-G01, MO-G02, MO-G03, MO-G04, MO-G05, MO-G06, MO-G07, MO-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não criar jobs/alertas/retreino por consequência do diagnóstico. Não transformar PSI em prova suficiente de degradação. Labels ausentes não tornam métrica de performance NA quando o usuário pediu justamente performance.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.



---

<a id="sec-14"></a>

# SER13 / SER14 — hub-ml-pipeline-builder

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Validar especificação operacional e só declarar deploy/write/run quando um executor canônico realizar e verificar a ação no destino autorizado.

Superfícies: pipeline_spec (L2); deploy_or_write (L4/authorization).

## 2. Reuso e inventário de autoria

Matriz registra data_quality_check, schema_to_yaml, naming_checker, safe_display e templates/pipeline_spec.md. São diagnósticos/templates, não executor de deploy. A rota de efeito deve ser implementada/provada antes da SER14.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Ambiente/host; origem/destino; objeto; modo de escrita; incrementalidade; chave; idempotência; permissões observadas; job/schedule quando solicitado; rollback/cleanup; ação exata e autorização; escopo pessoal.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: pipeline_spec validada sem deploy. L4: preflight, authorization binding, tentativa com request hash, IDs/versões remotas, retorno e readback, Receipt/Postflight e estado de resíduo. Não registrar segredo no request.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

PB-B01: escolher a primeira operação real suportada e seu executor após inspeção de capacidade do Free. PB-B02: fechar semântica de idempotência e readback após timeout. PB-B03: autorização de destination/overwrite/schedule é material e fica no formulário único de efeito; não pode ser escolhida pelo worker.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta PB-F01: spec sintética válida para um destino temporário pessoal, com autorização inicialmente ausente. O positivo L2 deve validar a spec e não escrever; o negativo de L4 sem autorização deve bloquear. O positivo real de L4 só será congelado após escolher operação/destino suportados; um servidor mock pode testar protocolo/erro, mas não substitui prova real no Free.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| PB01 | Ambiente/destino | Trocar por corporativo/prod ou destino não autorizado. | Recusar antes de qualquer efeito. |
| PB02 | Permissão desconhecida | Inferir write permission a partir de login. | UNKNOWN bloqueia ação. |
| PB03 | Defaults de operação | Assumir overwrite/schedule/rollback. | Exigir decisão material sem efetuar ação. |
| PB04 | Spec sem execução | Retornar deploy completed. | Postflight reprova false completion. |
| PB05 | Autorização stale | Usar em candidato ou destino B. | Reject anterior à escrita. |
| PB06 | Efeito parcial/timeout | Falhar após criação parcial. | PARTIAL/UNKNOWN, preservar request/result/resíduos. |
| PB07 | Run sem retorno | Objeto/run não encontrado ou sem estado final verificável. | Não declarar concluído. |
| PB08 | Transporte após efeito | Executor tenta repetir POST. | Somente read-only reconciliação; tentativa antiga falha permanece. |
| PB09 | Cleanup falho | Negar delete/falhar limpeza. | Resíduo preservado e declarado; sem rollback completo. |
| PB10 | Capacidade indisponível | Usar dry-run/mock para fechar L4. | Bloquear superfície não comprovada. |
| PB11 | Idempotency key | Mesma key com payload diferente. | Rejeitar colisão; não sobrescrever silenciosamente. |
| PB12 | Validação final observável | Readback difere de spec/bytes aprovados. | Postflight rejeita apesar de exit/HTTP sucesso. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Validar schemas/spec/naming e adapters de autorização; protocolos de efeito em sandbox mock rotulados como mock. Tests de failure-after-write exigem backend real isolado quando essa capacidade for declarada local.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Uma ação sintética mínima aprovada (por exemplo operação de artefato ou job somente se suportada e autorizada), verificada por leitura no destino e com cleanup separado. Não presumir APIs/quotas/permissões do workspace. Falta de capacidade permite encerrar L2 e deixar SER14 bloqueada, não inventar L4.

Roteiro Genie mínimo: PB-G01, PB-G02, PB-G03, PB-G04, PB-G05, PB-G06, PB-G07, PB-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Fora: trabalho/prod, schedules recorrentes não solicitados, overwrite de ativos existentes, concessão de permissão, uso de fontes reais ou ações de infraestrutura sem aprovação. A promoção não pode fundir spec e deploy num único status.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.



---

<a id="sec-15"></a>

# 06 — Auditoria independente e contrato de evidência

## 6.1 Duas perspectivas, não dois votos

O auditor de domínio verifica o significado do resultado e a suficiência do oráculo. O auditor de evidência/enforcement verifica se a conclusão está sustentada por execução, integridade, cobertura e autoridade. Ambos precisam de contextos distintos do executor. Modelo diferente é desejável quando acrescenta diversidade; não é requisito suficiente para independência.

O executor não edita o relatório de auditoria. O auditor não edita o código nem reclassifica o esperado para concordar com o resultado. O coordenador não resolve conflito contando PASSs. O autor responde com análise causal e mudança proposta; decisões de escopo/risco material vão ao usuário.

## 6.2 Pacote mínimo para cada auditor

Receber release spec, candidato/hash/tree, contrato da skill, matriz de escopo, mapa caso→test_id, fixture/oráculo, outputs e processo/effect ledgers. O relato do executor fica separado. Quando viável, auditor escreve a primeira lista de achados antes de ler o veredito do executor.

Contexto mínimo suficiente deve ser independente de uma conversa longa: toda referência usada precisa estar no repositório ou no bundle identificado. Nunca instruir auditor a “validar que está bom”. A pergunta é se a evidência suporta a claim, incluindo hipóteses adversariais pré-definidas.

## 6.3 Escala de evidência observável

| Nível | O que existe | O que não prova |
|---|---|---|
| DECLARED | Texto afirma que selecionou/usou/calculou | Carregamento, chamada ou conclusão reais |
| LOCATED | Caminho/símbolo foi localizado | Leitura, import ou execução |
| READ_OBSERVED | Evento de leitura/skill carregada visível | Chamada do helper ou sucesso |
| CALL_OBSERVED | Evento/trace da chamada com argumentos vinculados | Output completo ou correção |
| OUTPUT_OBSERVED | Saída persistida com identidade e processo concluído | Correção numérica/autoridade, sozinha |
| VERIFIED | Verificador/oráculo independente confrontou entradas/saídas | Autenticação humana universal, governança ou publicação |
| NOT_OBSERVABLE | Canal não permite observar o evento necessário | Não equivale a ausência de evento nem a PASS |

No teste negativo de roteamento, não ver o nome no texto final é insuficiente para provar que uma skill não foi carregada. Uma UI/trace completa ou outro mecanismo de observação precisa sustentar essa afirmação. Sem isso, a conclusão é limitada ao comportamento observável e a claim de roteamento recebe NOT_OBSERVABLE. Não coletar raciocínio privado como substituto de evento de ferramenta.

## 6.4 Perguntas do auditor de domínio

A unidade estatística é a declarada? Denominador/população e amostra efetiva correspondem ao cálculo? A fixture consegue detectar o defeito pretendido? O helper é semanticamente adequado, ou apenas possui nome parecido? O resultado foi confrontado com um oráculo independente? NaN legítimo é preservado? A tolerância estava aprovada? Temporalidade/PIT/fit/train-only foram observados? Dependência ausente foi tratada como bloqueio? Dry-run, recomendação e simulação estão corretamente rotulados? A conclusão extrapola causalidade, performance, fairness ou efeito executado?

A auditoria deve mostrar pelo menos um negativo discriminante importante e seu positivo correspondente para cada superfície promovida. Não é necessário reinspecionar todos os bytes manualmente quando o verificador íntegro comprova a cobertura, mas findings materiais exigem localização precisa.

## 6.5 Perguntas do auditor de evidência

O SHA executado é o candidato anunciado? Os manifestos existem e os hashes foram recalculados? Os testes obrigatórios foram coletados e finalizados? Há filtros/variáveis escondidos? Os logs estão completos? As etapas before/after têm IDs diferentes? Há erros adicionais num canal histórico? A execução terminou sem processos/resíduos não declarados? A claim de no-write cobre todos os destinos pertinentes? Houve edição ou reexecução não autorizada? O efeito foi observado independentemente do status do comando? O summary e seu verifier concordam? A evidência externa corresponde ao deployment correto? RAW e SHARE não foram confundidos?

Não aceitar `valid=true` de um verificador como prova de que ele cobre todas essas perguntas. O próprio verificador precisa de metatestes e escopo documentado.

## 6.6 Finding padronizado

Campos: finding_id, audit_id, campaign/round/candidate, severity, category, affected_scope, path/symbol/test_id, requirement_id, expected, observed, evidence_refs, reproduction, impact, suggested_minimal_resolution, status, author_response e closure_evidence.

Categorias mínimas: DOMAIN, CONTRACT, COVERAGE, AUTHORITY, EVIDENCE, ISOLATION, ENVIRONMENT, INTEGRATION, EDITORIAL. Severidade material não é diminuída porque “todos os outros testes passaram”.

- **F0:** quebra de autoridade, exposição de segredo, mistura de campanhas, adulteração ou mecanismo que pode certificar falso PASS. Bloqueio global ou do conjunto de consumidores afetados.
- **F1:** erro de cálculo, temporalidade, effect verification ou cobertura obrigatória ausente. Bloqueia a superfície e os dependentes.
- **F2:** limitação não crítica ou documentação ambígua que não altera resultado/autoridade, mas pode induzir uso incorreto. Resolver antes de compartilhar a capacidade afetada; adjudicar alcance, sem regra de dispensar automaticamente.
- **F3:** higiene editorial/empacotamento sem efeito na prova. Registrar sem forçar nova campanha numérica quando o código/escopo não mudam; verificação documental proporcional é suficiente.

Nova deficiência material descoberta durante auditoria é registrada e impede aceite. Não editar o teste congelado para avaliar retroativamente outra regra. Criar revisão de autoria e nova rodada pertinente, preservando a descoberta e a primeira evidência.

## 6.7 Contestação e encerramento

O autor pode contestar um finding com paths, contrato e reprodução. Auditor responde por evidência. Até duas rodadas de contraditório por finding antes de escalar a decisão de escopo ao usuário; isso é limite de conversação, não autorização para fechar finding inconclusivo como PASS. Não criar loops ilimitados de agentes.

Fechamento permitido: FIXED_VERIFIED; NOT_A_DEFECT_WITH_EVIDENCE; ACCEPTED_LIMITATION_BY_USER com limite explícito; ou OPEN/BLOCKED. Uma limitação que retira capacidade material reduz a claim, nunca se transforma em capacidade certificada por aceite retórico.

## 6.8 Estrutura probatória externa

```text
<evidence-root>/<campaign>/<round>/
  identity/       # Git, tool versions, role/permissions metadata
  manifests/      # candidate/test/fixture/dependency/profile hashes
  processes/      # started/finished, stdout/stderr, effects
  cases/          # inputs, outputs, expected, comparisons
  domain/         # Receipts/Postflights e dados sintéticos pertinentes
  audits/         # domínio, enforcement, contraditório
  external/       # publication/readback/probe/Genie literal
  summary/        # resultado, verificação própria e externa
```

Diretórios são exclusivos por rodada. Evidências grandes desnecessárias, `.git`, caches, homes, `.claude/context` e datasets reais não entram no SHARE. A auditoria de arquivo ZIP limita tamanho/expansão, proíbe traversal, links e membros duplicados antes de extrair. Nada do bundle é executado automaticamente.

## 6.9 RAW, SHARE e hashes

RAW é imutável e privado. SHARE é derivado sanitizado, com ID e manifesto próprios. `raw_bindings` pode conter hashes dos bytes RAW e referências não sensíveis; não prova por si só a execução. `transformation_manifest` registra arquivos transformados e política de sanitização, sem expor os valores secretos removidos.

Manifesto interno exclui a si próprio do conjunto hasheado e declara a exclusão. Hash externo do ZIP cobre o arquivo completo. Não criar ciclo em que manifesto precisa conter seu próprio hash final. O relatório de auditoria de um ZIP também não pode afirmar que audita a si mesmo dentro do ZIP; seu digest externo ou revisão sucessora resolve o vínculo.

O SHARE pode ter um resumo próprio de integridade para facilitar análise, mas nunca reutilizar o `certification_id` RAW como se fosse recalculável sobre bytes alterados. Preservar o output de verificação RAW com hash quando ele não exige sanitização; caso contrário, declarar também sua transformação. Sem RAW acessível, o auditor limita a conclusão ao que pode verificar no derivado, não inventa autenticidade.

## 6.10 Verificação independente do agregado

O verificador recebe manifestos aprovados de fora do payload candidato; confere schema e enums; resolve paths seguros; recalcula hashes; confronta documentos e outputs; compara case/test IDs, argumentos, ordem causal e tempo; exige provas dos effects e desautorização pertinente; e rederiva o veredito. Não basta verificar `status=PASS` nem confiar em expected_outcomes fornecidos pelo próprio summary.

Hashes e registros são tamper evidence, não assinatura de pessoa. Numa máquina controlada pelo operador, um agente com acesso irrestrito poderia forjar todos os dados; por isso permissões, isolamento, revisão e aceites observáveis continuam necessários. Não prometer segurança criptográfica que esta arquitetura não oferece.



---

<a id="sec-16"></a>

# 07 — Paralelismo, recursos, Git e integração

## 7.1 Unidade de concorrência

Há oito frentes lógicas, não oito processos pesados obrigatoriamente simultâneos. O scheduler escolhe tarefas READY cujas dependências e recursos estejam livres. O coordenador solicita a execução, mas não altera a regra do scheduler.

Piloto: dois slots de skill; operação regular inicial: três slots após prova. Até dois auditores simultâneos e um coordenador, com teto de cinco subagentes ativos; o integrador ocupa um slot exclusivo e não se sobrepõe a publication/certification mutável do mesmo composto. Se o host/cliente suportar menos, usar o limite menor. Não aumentar durante rodada para “ganhar tempo”.

A etapa cara normalmente é processo analítico/IO, não conversa da IA. O agente não precisa permanecer gerando texto enquanto um comando determinístico roda. Eventos started/finished/failure são suficientes, com heartbeat de liveness sem suposições de progresso.

## 7.2 Pools de recursos

`LIGHT_READ` para contratos, lint e parsing; `CPU_ANALYTIC` para pandas/SHAP/treino; `SPARK_LOCAL` quando qualificado; `DISK_HEAVY` para clones/renderer/temas; `REMOTE_READ`; `REMOTE_EFFECT`; `INTEGRATION_WRITE`.

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

Workers não fazem commits de correção. Falha produz issue/proposta de diagnóstico; a correção é escrita aqui. Mudanças mecânicas não são licença para decidir conflitos semânticos no local.

## 7.5 DAG funcional

Depois de B0 qualificado, as três frentes L3 e os cinco contratos L2 podem ser liberados conforme a autoria individual fique pronta. Explainability usa fixture pré-treinada, não depende da promoção de baseline. Safra e estatística não dependem de pipeline. Cross e features compartilham contrato PIT, não copiam implementations uma da outra.

SER06 depende da L2 SER05 aceita; SER08 da L2 SER07; SER10 da L2 SER09; SER12 da L2 SER11; SER14 da L2 SER13. Dependências de efeito externo são nós adicionais: capacidades, destino e autorização. A fila não impõe que toda L3 termine antes de iniciar L2 independente.

O arquivo `catalogos/DAG.json` contém o grafo de planejamento. Nós de autoria não são tarefas delegadas ao executor local. Nós de execução só recebem SHA/perfil depois de G1/G2. Faltas de schema/contrato comum bloqueiam consumidores; falha independente não cancela todos os demais.

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



---

<a id="sec-17"></a>

# 08 — Capacidade externa, publicação e coleta manual

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

## 8.5 Roteiro humano reduzido

O coletor prepara uma fila com case_id, notebook/chat alvo, instrução literal, deployment digest, output que deve ser preservado e proibições. O usuário não precisa inventar nome, preencher schema nem resumir resultados. A primeira tarefa piloto valida que o canal consegue transportar o JSON/eventos necessários antes de pedir a execução das demais.

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

Reautenticar profile após expiração é ação do usuário ou procedimento explicitamente autorizado. Uma autenticação renovada não reclassifica rodada antiga. O local nunca presume DEFAULT ou um profile corporativo para contornar FREE indisponível.

## 8.10 Encerramento e publicação pós-merge

Um lote externo termina quando outputs, post-verifies, effects e revisões estão completos para as claims previstas. Exceções ficam por skill/superfície. Não exigir que pipeline L4 improvável bloqueie o fechamento legítimo de safra L3 independente; tampouco chamar o plano inteiro concluído se pipeline ficou parcial.

Merge integra código. Publicação coloca bytes no Free. Homologação comportamental mede uma versão operacional. Replicação no trabalho permanece BLOQUEADA e fora desta autorização. Essas três datas/identidades são registradas separadamente.



---

<a id="sec-18"></a>

# 09 — Contratos dos agentes e handoffs sem deriva

## 9.1 Princípio de delegação

O agente recebe uma tarefa fechada, não uma missão vaga como “promova esta skill”. A tarefa referencia release, profile, case set, candidatas e permissão por hash. O executor não escolhe retrospectivamente quais testes eram relevantes. O coordenador não pode gerar um script novo para substituir um comando ausente.

A hierarquia durável continua em `CLAUDE.md` e `.claude/`. Os futuros adapters Codex apontam para os contratos deste pacote e não copiam toda a governança. O nome do modelo é uma configuração de execução, não uma fonte de autoridade. Trocar de modelo não altera os critérios da campanha.

## 9.2 Coordenador

Entrada: manifesto validado, autorização de execução local, qualificação do ambiente, fila e DAG congelados. Leitura: perfis, status e evidências; não receber credenciais remotas por padrão. Escrita: journal externo de coordenação e registros de despacho, por API do launcher.

Procedimento:

1. Verificar release, baseline, perfis e integridade. Se qualquer referência faltar, registrar BLOCKED_DESIGN.
2. Perguntar ao scheduler quais tarefas estão liberadas e quais recursos podem ser reservados; não decidir por raciocínio livre ignorando o DAG.
3. Criar no máximo os workers autorizados. A criação de subagentes é exclusivamente sua; filhos não criam netos.
4. Despachar `task_id`, não uma versão reescrita do contrato. Receber status do executor determinístico.
5. Em falha, bloquear os dependentes declarados, manter independentes se a falha não comprometer infraestrutura/segurança comum e preservar a primeira causa.
6. Despachar auditoria após completar o pacote exigido. Não enviar a conclusão do executor como resposta que o auditor deve confirmar.
7. Consolidar o vetor por skill/superfície. Encaminhar blockers à autoria ou gates humanos; nunca criar `human_approved=true` por conta própria.

Saída: quadro factual com tarefas concluídas, falhas, blockers, slots, evidências e próxima ação autorizada. “O agente disse PASS” não é fonte de status. Sem confirmação do launcher/verificador, usar EVIDENCE_INCOMPLETE.

## 9.3 Executor de skill

Entrada: checkout preparado e candidato imutável, `task_id`, perfil com comandos e diretório externo de evidência. Leitura: apenas contexto pertinente e fonte/testes autorizados. Escrita: evidência e temporários permitidos ao comando, nunca arquivos de autoria.

Executar preflight do launcher, depois entrypoint por fase. Não instalar dependências durante certificação; usar ambiente previamente preparado. Não editar tests, fixtures, policy, README, CHANGELOG, imports, timeouts ou runner para resolver erro. Não usar credencial herdada que não esteja autorizada para a tarefa.

Ao primeiro bloqueio material, registrar resultado e efeito separados. Executar apenas diagnósticos/readback que o perfil já permita. Descrever a causa e localização observáveis; não apresentar palpite como reprodução. Terminar com `task_result.json` validado, evidências e diagnóstico, não com uma proposta de merge.

Um executor pode identificar uma correção provável; ela vai no finding como hipótese. Não aplica patch. Isso mantém a divisão pedida pelo usuário: a próxima alteração de implementação continua repo-side.

## 9.4 Auditor de domínio

Recebe contrato, implementação, fixtures, outputs e evidência de chamadas, preferencialmente sem o resumo/veredito do executor. Sua tarefa é verificar estimando, população, universo, hipótese, método, parâmetros e significado da conclusão.

Pode executar somente oráculos/read-only ou mutantes previamente definidos em clone descartável, em tarefa de auditoria separada. Não modifica a candidata congelada. Para Spark/MLflow/efeitos, exige observação compatível com o que o caso alega; emula apenas o que está rotulado como simulação.

Relatório: obrigações cobertas, achados com reprodução, evidências insuficientes, limites de interpretação e veredito no escopo. Uma hipótese metodológica fora do catálogo não é implementada localmente; é devolvida à autoria com impacto.

## 9.5 Auditor de evidência e enforcement

Recebe manifestos aprovados por canal confiável, artefatos RAW/SHARE permitidos, logs completos e inventário da execução. Recalcula o que puder a partir dos bytes fornecidos; distingue o que apenas foi declarado.

Verifica IDs e ordenação, seleção/coleta/execução de testes, ausência de etapas, binding do input/output, alterações não autorizadas, declarações fortes em payload resealado, efeito remoto desconhecido, autorização limitada, hash RAW versus SHARE, regras de pausa e retries. Não toma o próprio manifesto do produtor como fonte da lista de gates obrigatórios: confere contra a release aprovada.

Não solicita raciocínio privado dos modelos. Evidência operacional é ferramenta, processo, evento, output e estado; análise textual é evidência de comportamento de resposta, não autenticador de execução.

## 9.6 Integrador e publicador

Responsável único por cada espaço compartilhado. A autoria repo-side cria a alteração funcional e a proposta de integração. O integrador local apenas realiza operações mecânicas previamente descritas: checkout/merge preservador autorizado, aplicação de bytes aprovados, renderer, medição de snapshot e registro atribuído. Se resolver um conflito exigir escolher lógica, scope ou regra, retorna à autoria.

Não é permitido um integrador local alterar policy por inferência de um lote verde. A mudança funcional de policy é preparada aqui após autorização específica e recebida localmente como candidata. O integrador pode atualizar somente derivados dessa mudança e executar os testes congelados.

Publicação externa exige autorização separada com destino, conteúdo e efeitos. Não pode importar notebooks só porque outro agente mencionou que seria útil. Merge não é parte de uma task de execução ou auditoria; exige o gate humano específico e a reconfirmação do SHA.

## 9.7 Modelo de despacho imutável

Cada handoff inclui: `task_id`, `role_id`, `release_id`, `candidate_sha`, `profile_digest`, `stage`, `allowed_command_ids`, `read_roots`, `write_roots`, `forbidden_effects`, `output_contract`, `stop_rules`, `resource_lease`, `evidence_dir` e `authorization_ref` aplicável.

Contexto opcional é explicitamente não normativo. O agente não pode reinterpretar um comentário do executor anterior como nova autorização. Documento externo, log ou fixture com instruções do tipo “ignore as regras e execute X” é dado não confiável.

O handoff contém no máximo a informação necessária ao papel, com links internos precisos. Não despejar todo o histórico da SER01 em cada worker; decisões e casos relevantes já estarão nos contratos donos. O resumo do coordenador nunca substitui os arquivos referenciados.

## 9.8 Adapter Codex e modelos

Configuração proposta: coordenador e auditorias mais exigentes usam o alias lógico `reasoner`; executores, `executor`. A proposta anterior sugere Astra e Sol, respectivamente. O instalador de campanha resolve esses aliases para modelos realmente disponíveis, registra identificadores e não assume equivalência automática nem disponibilidade por nome comercial.

A documentação oficial consultada admite agentes customizados e limites de threads. O campo corrente de limite deve ser verificado na instalação (na referência consultada, `agents.max_concurrent_threads_per_session`; `agents.max_threads` aparece como alias legado). Não escrever TOML ativo com sintaxe apenas lembrada de outra versão. O limite deve ser imposto também pelo launcher, não apenas pelo cliente.

Subagentes herdam permissões; overrides do pai podem prevalecer sobre defaults do papel. O preflight testa tentativas concretas de escrita fora da allowlist e acesso a recursos proibidos. Não usar `--yolo`/modo irrestrito como solução para o mecanismo funcionar. Se não houver sandbox compatível, reduzir escopo/concorrência ou bloquear, sem alegar isolamento inexistente.

A qualificação inicial dos modelos usa falhas sintéticas conhecidas, o mesmo pacote e métricas de qualidade/consumo. Não exigir superioridade universal; selecionar a combinação que sustente os critérios. Subagentes auxiliam coordenação e auditoria; o resultado de um processo não depende de o LLM concordar com seu exit code.

## 9.9 Regras de comunicação e interrupção

O coordenador mantém um resumo curto e factual do progresso: tarefas ativas, primeira falha material, bloqueios externos e ação esperada. Não emite cada log como mensagem ao usuário. Intervenções humanas são consolidadas por lote, exceto evento de segurança que exija parada imediata.

O encerramento de sessão persiste journal e status fora do produto. Ao retomar, conferir locks, processos ainda ativos, identidades e efeitos desconhecidos antes de despachar. Uma sessão nova não inicia automaticamente outra tentativa da tarefa antiga. Orçamento esgotado gera status incompleto, não autorização para reduzir testes.

## 9.10 Critério para aceitar um handoff

Todos os campos obrigatórios resolvidos; modelo e permissões qualificados; command IDs existentes; digests coerentes; candidatas acessíveis; decisões materiais fechadas; recursos disponíveis e destino exclusivo. Uma tarefa que precise começar com “descubra como implementar ou testar” não é um handoff de execução válido.



---

<a id="sec-19"></a>

# 10 — Implantação controlada, entregáveis e critérios de saída

## 10.1 Ordem do trabalho

Esta entrega detalha o plano. O próximo trabalho é autoria B0, não executar oito agentes sobre documentação sem implementação. O B0 constrói o mecanismo mínimo comum e seu mapa de cobertura. Em seguida, libera-se autoria dos domínios em paralelo lógico, executando localmente só os pacotes já prontos.

A execução de contratos L2 não precisa esperar todas as L3. Cada L4 depende do próprio L2 aceito e dos contratos compartilhados pertinentes. A integração continua controlada por lote e autorização. Não renumerar SER02–SER16 para esconder ou reiniciar as etapas históricas.

## 10.2 Pacotes B0 — entrega curta e limitada

| Pacote | Autoria repo-side | Evidência de saída | Condição que impede liberar |
|---|---|---|---|
| B0.1 Governança e inventário | Formalizar adendo; confirmar baseline, escopo e autoridades; apontar documentos donos | Decisões sem contradição e vetor nominal das skills | Regra sequencial antiga e paralela tratadas simultaneamente como obrigatórias |
| B0.2 Cobertura e contratos | Mapear SE08/CI/SER01 até métodos; schemas runtime fechados; catálogo de casos e command IDs | Requisito→teste→oráculo→evidência completo; inventário de métodos coletado | Suíte omitida, método sem justificativa, teste temporal misturado a atual |
| B0.3 Executor mínimo | Launcher, registry argv, process adapter, scheduler limitado, locks e result records | Smoke de comandos reais, logs separados, estados e limites de escrita | Comando arbitrário, mutação fora da allowlist ou globals compartilhados |
| B0.4 Verificador e empacotamento | Verificação independente, first-failure, RAW/SHARE, schema, integridade e coletor externo | Mutantes de certificado rejeitados; bundle não circular e seguro | PASS inválido, ERROR mascarado, referência ausente ou output fabricado |
| B0.5 Qualificação de host/cliente | Perfis declarados e probes de recursos, permissões e runtime | Ambiente identificado; limites escolhidos antes da certificação; ausência de secrets nos workers | Host desconhecido, sandbox só nominal, modelo/config inexistente |
| B0.6 Piloto do mecanismo | Dois cenários sintéticos independentes, um fail deliberado, dependente e publicação bloqueada | Concorrência sem colisão; falha propaga só ao necessário; relato humano coerente | Nova tarefa iniciada após stop global, retry oculto ou mistura de evidências |
| B0.7 Revisão de liberação | Auditorias técnica e probatória, metatestes e coverage review | Release do mecanismo marcada LOCAL_QUALIFIED, não skill promovida | Finding material aberto ou cobertura não fechada |

B0 não cria banco de dados, serviço web, fila distribuída, painel comercial, API própria de agentes, novo engine analítico ou módulo de deploy genérico. Persistência em arquivos/journal e processos locais é suficiente para esse escopo. Uma necessidade nova precisa demonstrar por que o mecanismo existente não resolve.

A autoria pode executar seus testes de desenvolvimento aqui quando o ambiente permitir; resultados são rotulados por host e fase. Teste que requer Windows/NTFS ou Free continua qualificação local/externa, não é presumido por um import Linux. Impossibilidade de reproduzir um host não justifica delegar ao laboratório um erro estático já conhecido.

## 10.3 Dossiê que autoriza entrada de uma skill

A saída de autoria de cada skill contém: implementação pronta, diff revisado, contrato/schema, fixtures reais versionadas, oráculos independentes, casos ligados a IDs coletáveis, tolerâncias numéricas, dependências/locks, perfil de execução, matriz operação×tipo×host×efeito, plano Free/Genie literal, definições de não aplicabilidade, critérios de auditoria e rollback.

Toda decisão não resolvida vira blocker identificado com owner e gate. O item não é AUTHORING_READY enquanto um blocker de sua fase estiver aberto. Os casos propostos nesta entrega especificam o que provar; as APIs exatas, métodos efetivamente suportados, bytes de fixtures e IDs Python precisam ser resolvidos pelo autor antes de enviar.

## 10.4 Piloto real de duas frentes

Depois do piloto sintético do mecanismo, a primeira dupla proposta é **análise-safra L3 (SER03)** e **cross-EDA L2 (SER05)**. A escolha testa duas naturezas diferentes — cálculo pandas com oráculo manual e contexto/preflight read-only — sem depender de deploy ou de treinamento externo. O adendo precisa estar formalizado para permitir essa ordem de execução.

A dupla só é lançada quando ambas tiverem pacotes completos. Não promove automaticamente nenhuma das duas. Se a autoria de uma não estiver pronta, usar outra frente independente igualmente preparada, com alteração versionada do manifesto antes do freeze. Não trocar a composição durante o piloto para ocultar um FAIL.

Aprovada a dupla, liberar até três execuções de skill simultâneas, com as duas auditorias dentro do teto global. O aumento exige metatestes de isolamento verdes, nenhum efeito não autorizado, nenhuma mistura de arquivos e nenhum finding material no piloto. Melhor velocidade não compensa violação de autoridade.

## 10.5 B1 — fila das L3 e contratos L2

Fila lógica: EX.L3, VF.L3, ST.L3, CE.L2, FE.L2, BM.L2, MO.L2, PB.L2. O scheduler usa prontidão e dependências, não uma ordem rígida pela numeração. Três slots não significam três instalações concorrentes de dependências nem três jobs Spark pesados: resource classes podem reduzir a concorrência efetiva.

A autoria deve priorizar contratos compartilhados que destravem múltiplos domínios, sem transformar isso em dependência circular. O contrato temporal comum pode destravar CE/FE; um modelo sintético versionado destrava EX/MO sem esperar baseline-ML promovida. ST só entra após fechar seu catálogo de métodos; escopo genérico é inválido.

Cada resultado LOCAL_PASS segue às auditorias. O resultado auditado segue ao lote externo pessoal. As demais frentes continuam localmente, sem esperar cada clique do usuário. A indisponibilidade de Free bloqueia EXTERNAL_PASS, não apaga a prova local do SHA observado.

## 10.6 B2 — avanços L4 por dependência própria

CE.L4, FE.L4, BM.L4, MO.L4 e PB.L4 só executam após seus L2 aceitos e os contratos/implementações necessários prontos. Preservar a regra de não saltar de orientação L0 diretamente para alegação L4.

A promoção intermediária L2 e sua integração continuam gates específicos. Desenvolvimento repo-side do L4 pode ser preparado contra contrato L2 estável e identificado, mas não é liberado como certificação L4 antes do aceite correspondente. Efeitos reais externos permanecem pessoais, sintéticos e autorizados.

Sem materializer ou executor real, limitar a superfície e registrar blocker; não trocar silenciosamente o target para declarar o plano concluído. A proposta de aceitar um escopo parcial é decisão humana explícita, com o restante mantido no backlog.

## 10.7 B3 — composição, promoção e SER15/SER16

Lotes de integração começam com no máximo duas skills/candidatas independentes e passam a três somente após prova do mecanismo. Cada lote define membros, níveis before/after, superfícies e effects; não contém todas as oito por conveniência se algumas não estão prontas.

Sequência: compor bytes aprovados; renderer/snapshot; freeze integrado; CI transversal completa e testes de interoperabilidade; auditoria; coleta externa pertinente na versão publicada; proposta humana de promoção; policy candidata como último ato funcional autorizado; nova certificação final e verificação externa proporcional; aceite humano de merge; confirmação de árvore/parents e publicação operacional conforme autorização.

Se a alteração pós-teste mudar somente a policy no escopo aprovado, conferir a policy publicada e os casos comportamentais sensíveis ao nível/autoridade. Não transportar a certificação inteira entre SHAs. Uma alteração de SKILL.md/runner/contrato exige reexecutar a prova comportamental e computacional afetada, conforme a matriz de impacto.

SER15 atualiza a coerência entre produtoras, auditores, policy, Manual e prompts sem hardcodar capacidades futuras. SER16 prova a árvore efetivamente integrada e o estado por skill, inclusive pendências. Não se encerra afirmando “oito promovidas” se uma parte continua BLOCKED_DESIGN.

## 10.8 Critérios de entrega por bloco

B0 entregue: mecanismo mínimo qualificado e cobertura classificada; nenhuma promoção.

B1 entregue por item: pacote L3/L2 completo, execução local e auditorias pertinentes, estado externo e gate humano explícitos. Não exigir o fim de todas as outras filas para reconhecer um item concluído.

B2 entregue por item: execução real das superfícies L4 suportadas, Postflight, efeitos/destinos verificados e autoridade respeitada. Dry-run não satisfaz esse critério.

B3 entregue: candidatas aceitas integradas e operacionalmente verificadas no alcance autorizado, snapshots e índices coerentes, evidência final disponível, SER15/SER16 com gaps explícitos e histórico imutável.

## 10.9 Métricas para demonstrar que a mudança funcionou

Medir por fase: tempo de autoria, diagnóstico, execução, espera de auditoria, espera humana, publicação e integração. Não somar tempos de comandos aninhados como se fossem esforço independente. Registrar wall-clock de campanha, CPU/processo quando observável, tokens/custo quando expostos e motivo de toda recertificação.

Indicadores de qualidade: taxa de first-pass por etapa; defeitos triviais encontrados apenas no laboratório; findings materiais da auditoria; falsos verdes detectados por mutantes; conflitos de integração; número de handoffs/intervenções humanas; cobertura de requisitos; tentativas com efeitos desconhecidos e preservação de evidência.

Meta operacional de segurança: zero promoção sem autorização, zero nova execução material após efeito desconhecido, zero omission de gate obrigatório não declarada. Metas de produtividade percentuais serão definidas após o piloto, não inventadas a partir de duas medições históricas.

## 10.10 Encerramento desta entrega de planejamento

O pacote contém decisões e especificações, com catálogos validados estruturalmente. A implementação runtime B0 e os testes das novas skills permanecem NOT_STARTED/NOT_IMPLEMENTED. O avanço seguinte continua sendo autoria aqui; o laboratório não recebe instrução para construir a arquitetura ou consertar este plano autonomamente.



---

<a id="sec-20"></a>

# 11 — Bloqueios de autoria, riscos e controle de escopo

## 11.1 Regra de resolução

Os bloqueios abaixo não são pedidos para o executor local improvisar. Cada um tem owner, evidência faltante e gate impedido. A autoria resolve os técnicos; o usuário decide somente matéria que altera escopo/autoridade/efeito. Não enviar novamente a mesma pergunta se a evidência do repositório já puder resolvê-la.

Bloqueio de uma fase não impede trabalho independente: materializer pendente não impede escrever o contrato L2 da própria skill nem testar safra. Entretanto, uma liberação nominalmente L4 não pode omitir a superfície materializadora e manter a mesma claim ampla.

O catálogo dono é `catalogos/BLOQUEIOS.json`. Estados são de planejamento e permanecem abertos até a implementação/prova correspondente, não até alguém simplesmente editar o texto para “resolvido”.

| ID | Escopo e questão | Quem resolve | Evidência/ação exigida | Gate |
|---|---|---|---|---|
| B01 | GLOBAL: Formalização do adendo | Autoria B0 | Formalizar a ordem por DAG e lotes preservando gates; não reescrever ADR aceito. | B0_RELEASE |
| B02 | GLOBAL: Cobertura por método | Autoria B0 | Enumerar coleção/test IDs e classificar invariantes atuais, história e NA. | B0_RELEASE |
| B03 | GLOBAL: Schemas e launcher runtime inexistentes | Autoria B0 | Implementar interfaces e metatestes M01–M28, sem engine analítico universal. | B0_RELEASE |
| B04 | GLOBAL: Cliente/modelos/permissões | Qualificação local com roteiro repo-side | Executar probes aprovados; resolver aliases; testar bloqueio de escrita/credenciais. | LOCAL_QUALIFICATION |
| B05 | GLOBAL: Budgets | Qualificação local com roteiro repo-side | Medir recurso e congelar limites por classe antes da campanha. | LOCAL_QUALIFICATION |
| B06 | GLOBAL: Persistência probatória | Autoria B0 | Implementar verificador independente e falhas adversariais sem circularidade. | B0_RELEASE |
| B07 | GLOBAL: Interoperabilidade de verifiers | Autoria B0 | Definir contracts por produtora, rejeição de outra skill e auditoria sem self-proof. | INTEGRATED_CERTIFICATION |
| B08 | GLOBAL: Base concorrente MM/PSEF | Autoria B0 e integrador | Mapear impactos na base exata; reservar integração; sem incorporar branches por conveniência. | INTEGRATED_FREEZE |
| B09 | hub-ml-explainability: Linhas SHAP efetivas | Autoria SER02 | Controlar amostragem e provar IDs; bloquear modos não vinculáveis. | AUTHORING_READY |
| B10 | hub-ml-analise-safra: Semântica de denominador e maturidade | Autoria SER03 | Congelar escopo binário e fixtures incompletas; testar tabela independente. | AUTHORING_READY |
| B11 | hub-ml-validacao-estatistica: Catálogo estatístico | Autoria SER04 | Enumerar métodos e APIs públicas reais; p-value/efeito/IC só quando suportado e definido. | AUTHORING_READY |
| B12 | hub-ml-cross-eda-ml: Contrato temporal | Autoria SER05/06 | Validar premissas, limites/tie/timezone; bloquear fonte que exceda o contrato. | AUTHORING_READY |
| B13 | hub-ml-feature-engineering: Materialização | Autoria SER07/08 | Implementar adapter e autorização/readback; manter L4 de efeito bloqueado até prova real. | L4_RELEASE |
| B14 | hub-ml-baseline-ml: Tracking efetivo | Autoria SER09/10 | Vincular objetos reais, parâmetros/run/artefatos e testar MLflow. | L4_RELEASE |
| B15 | hub-ml-monitoramento-modelo: Ação versus recomendação | Autoria SER11/12 | Fechar escopo das ações reais; impedir completion fictício e autoridade inferida. | L4_RELEASE |
| B16 | hub-ml-pipeline-builder: Executor de deploy | Autoria SER13/14 | Escolher/implementar operação pessoal suportada; sem serviço disponível, manter bloqueio. | L4_RELEASE |
| B17 | GLOBAL: Free runtime/permissões | Autoria externa + usuário | Roteiro read-only prévio; autorizações de destinos/efeitos separadas; nada corporativo. | EXTERNAL_RELEASE |
| B18 | GLOBAL: Observabilidade Genie | Autoria externa | Definir eventos/output mínimo por caso e validar transporte antes dos chats. | EXTERNAL_RELEASE |
| B19 | GLOBAL: Promoção e merge | Autoria e usuário nos gates próprios | Recolher aceite nominal por skill/superfície/candidata e merge separado. | POLICY_PROMOTION |
| B20 | GLOBAL: Acesso de escrita do conector | Autoria repo-side | Versionar os bytes preparados quando houver ferramenta de escrita autorizada; não dizer que já foi publicado. | REPO_VERSIONING |

## 11.2 Riscos e controles preventivos

**Explosão do framework:** limitar B0 às interfaces da arquitetura; não iniciar infraestrutura distribuída. Qualquer expansão precisa de caso real e teste discriminante que demonstre insuficiência da composição existente.

**Oito agentes repetindo o mesmo trabalho:** command registry e cache de dependências preparados uma vez; escopos não sobrepostos e relatórios específicos. Testes comuns são compartilhados somente sobre a mesma candidata/ambiente no escopo correto, não por semelhança verbal.

**Falso consenso entre modelos:** auditores separados, vereditos prévios ao resumo do executor quando viável, oráculos independentes e contraditório por evidência. Concordância de duas IAs sem artefato não valida uma chamada.

**Drift de scope:** release spec e matriz de claims congelados. Mais artefatos ou helpers não autorizam scope global; não promover convert, todos os métodos SHAP, inferência causal ou deploy universal por analogia.

**Concorrência perigosa:** limites globais de agentes e recursos, clones/processos separados, leases de publicação e integração, nenhum token remoto em executor que não precisa dele. Testar edit-and-restore como violação, não apenas git status final.

**Regressão histórica omitida:** matriz de equivalência por suíte/método, invariante vigente com sucessor testado e baseline histórica preservada. Regex de nomes não é mecanismo definitivo de classificação de erro.

**Higiene documental gerando ciclo longo:** mudar documentação em um único dono; medir snapshots após composição; executar parse, links, JSON schema e teste de fase antes do laboratório. Finding F3 isolado deve ser corrigido de forma proporcional; não chamar cada detalhe editorial de defeito funcional.

**Cota/tokens:** execução determinística não depende de uma conversa longa por gate. Cada agente recebe contexto mínimo e orçamento. Se cota não observável, registrar essa limitação e limitar trabalho por tarefa; não prometer savings quantitativos não medidos.

**Efeito remoto desconhecido:** estado de efeito separado de exit code; readback autorizado; ausência de retry automático de escrita. Cleanup só sobre destinos próprios e explicitamente autorizados, sem apagar vestígio de falha.

## 11.3 Mudança do plano depois de aprovado

A revisão registra: motivo, evidência, casos afetados, deltas de scope/autoridade, impacto em código/testes, provas invalidadas e gates necessários. Correção técnica dentro do escopo vai para autoria. Mudança de target, efeito, universo, aprovação ou regra de aceite volta ao usuário.

Não criar uma sequência infinita de novas condições de aceite depois de cada rodada. A auditoria pode encontrar lacuna material legítima; ela precisa demonstrar impacto concreto. Preferências estilísticas não geram novos gates sem relação com risco. Um finding novo não permite apagar os anteriores.

## 11.4 Compromisso realista

O plano reduz classes conhecidas de retrabalho e torna lacunas visíveis antes do laboratório. Não garante ausência de bugs, evolução da plataforma ou incompatibilidade de runtime. A excelência buscada é rastreabilidade, evidência proporcional e correção causal, não promessa de zero futuras correções.



---

<a id="sec-21"></a>

# 12 — Fontes, proveniência e limite de cada afirmação

## 12.1 Base de planejamento

A proposta aprovada P0 é a base desta especificação. As decisões novas detalham sua operacionalização e estão identificadas como desenho, fixtures propostas ou requisitos a implementar. Não transformar o plano em relatório de testes concluídos.

A `main` foi consultada nesta sessão no GitHub e apontou para `d2988e97e7b6c5fe1fd561852e947a155c2d731b`. As leituras diretas abaixo foram vinculadas a essa base. Cabeçalhos SER00 com SHAs antigos são evidência histórica, não a ref vigente.

| ID | Fonte | O que sustenta | Profundidade |
|---|---|---|---|
| P0 | `SER_PLANO_PARALELO_PROPOSTA_2026-09-23.md` | Proposta aprovada pelo usuário; terminologia, papéis, oito dossiês e limitações. | READ_IN_FULL |
| P1 | `SER01_medicoes_retrospectivas.json` | Tempos de summaries sanitizados; não mede autoria/auditoria/espera humana. | READ_IN_FULL |
| R01 | `CLAUDE.md` | Hierarquia, fonte/derivado, changelog e contexto canônico. | READ_AT_BASE |
| R02 | `.claude/CLAUDE.md` | Índice operacional e rota de leitura. | READ_AT_BASE |
| R03 | `.claude/rules/multi-llm.md` | Papéis, adaptação de contexto e auditoria multi-IA. | READ_AT_BASE |
| R04 | `.claude/rules/docs-e-readmes.md` | Documento dono, estados verificáveis, ADR aceito e linguagem. | READ_AT_BASE |
| R05 | `docs/sprints/skill_enforcement_rollout/PLANO_MESTRE.md` | Metas/sprints/gates/ordem histórica; trecho amplo lido, saída longa com truncamento. | READ_RELEVANT_SECTIONS |
| R06 | `docs/sprints/skill_enforcement_rollout/SER00/MATRIZ_DEPENDENCIAS.md` | Dependências reais e ordem de integração distinta de dependência universal. | READ_AT_BASE |
| R07 | `docs/sprints/skill_enforcement_rollout/SER00/MATRIZ_HELPERS_PRIMITIVES.md` | Public API versus declarado, lacunas SHAP/PIT/tracking/materialização. | READ_AT_BASE |
| R08 | `tools/skill_enforcement/certify_local.py` | Linhas 80–276; 21 gates do perfil SE08, process records e budgets. | READ_RELEVANT_SECTIONS |
| R09 | `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/__init__.py` | Fachada exporta compute_shap/importance/plots; não comprova assinatura ou execução. | READ_AT_BASE |
| R10 | `tools/ci_local.py` | Nove etapas não-SEF e sef cumulativo descritos na proposta e no histórico fornecido; reler integralmente em B0. | SOURCE_DERIVED_REVALIDATE_BEFORE_EXECUTION |
| R11 | `docs/decisions/ADR-0022-certificacao-prospectiva-ser.md` | Preservação de SEF histórico, certificação prospectiva, último ato funcional e aceite. | SOURCE_DERIVED_REVALIDATE_BEFORE_FORMALIZATION |
| R12 | `ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json` | Vetor de capacidade confirmado no fechamento SER01 e proposta aprovada; reconfirmar no release preflight. | SOURCE_DERIVED_REVALIDATE_BEFORE_EXECUTION |
| H01 | `report(3).md: SER01 A4-FREE R2` | Erro de transporte com efeito servidor observado; preservar resultado de comando e efeito separadamente. | RETRIEVED_RELEVANT_EXCERPTS |
| H02 | `A4_GENIE_FORMULARIO_PREENCHIDO.md` | Transcrição sem indicador da UI; narrativa não equivale a chamada observada. | RETRIEVED_RELEVANT_EXCERPTS |
| W01 | `https://learn.chatgpt.com/docs/agent-configuration/subagents` | Agentes customizados, limites, herança de permissões e overrides; configuração efetiva precisa de qualificação local. | WEB_VERIFIED_2026_09_23 |

## 12.2 Evidência histórica versus inferência

P1 reporta duas durações de campanhas: 537,41721 s para A3-R3 e 375,12867 s para promoção R2. Não inclui autoria, preparação, auditoria, publicação ou espera humana. A conclusão de que padronização deve atacar também handoffs é uma inferência de desenho, não um percentual de desperdício calculado desses tempos.

A matriz de helpers R07 distingue export público, implementação inspecionada e simples declaração. A elaboração deste plano não executou cada helper nem enumerou todos os seus métodos de teste. A cobertura real por primitive continua tarefa explícita da autoria B0/B1.

Os casos e fixtures EX/VF/ST/CE/FE/BM/MO/PB são propostas novas desta entrega para materialização repo-side. Valores de referência simples foram definidos por raciocínio independente e podem ser conferidos sem a implementação produtora. A escolha final de método/semântica precisa respeitar o contrato fechado, não apenas copiar a fixture.

## 12.3 Documentação externa

W01 foi consultada para evitar pressupor configuração antiga do Codex. O plano usa aliases de modelos a resolver e testes de permissões efetivas. Nenhuma versão instalada, quota, hardware ou configuração do usuário foi observada nesta etapa; permanecem precondições de qualificação.

A disponibilidade de operações Databricks Free/MLflow/jobs/materialização não foi novamente verificada pela UI nesta sessão. O desenho exige descoberta autorizada e prova pessoal proporcional antes de declarar uma superfície L4 operacional.

## 12.4 Verificações feitas nesta entrega

Leitura da proposta e retrospectiva; leitura seletiva das fontes do repositório; conferência da ref main; consulta oficial sobre subagentes; geração do pacote documental e dos catálogos; validações locais do próprio pacote registradas no relatório de validação.

Não houve campanha de skill, treino/SHAP/PIT/Spark, probe Databricks, publicação, alteração de policy, commit GitHub ou merge. O validador desta entrega valida documentação/catálogos/links/DAG, não substitui testes B0 ou certificação do produto.

## 12.5 Disponibilidade de escrita no GitHub

O conector ativo foi inspecionado: as ações disponíveis nesta sessão são de leitura. A busca do plugin confirmou o GitHub instalado, mas não expôs ação de publicação de arquivos. Portanto esta entrega fornece bytes e patch preparados, sem alegar commit ou PR inexistente. Esse limite é operacional desta sessão, não uma afirmação de que o repositório nunca possa ser escrito pelo ChatGPT.



---

<a id="sec-22"></a>

# 13 — Minuta do adendo operacional ao Skill Enforcement Rollout

**Estado: DIREÇÃO APROVADA; TEXTO DE FORMALIZAÇÃO PREPARADO; NÃO PUBLICADO NO GIT NESTA ENTREGA.**

Não atribuir um número de ADR sem conferir o índice vigente. O corpo decisório aceito do ADR-0022 não é reescrito. Formalizar esta mudança como novo adendo/ADR conforme a governança, apontando precisamente as cláusulas operacionais do Plano Mestre e matriz de dependências substituídas.

## Contexto

A SER01 foi integrada. O usuário aprovou substituir execução estritamente sequencial por autoria repo-side, execução local paralela governada, auditorias independentes e integração serializada. A ordem histórica das sprints não constitui dependência funcional universal.

## Decisão

1. Preservar nomes e objetivos SER02–SER16, targets, fonte única, evidência por SHA e host, dados sintéticos e proibição de promoção corporativa.
2. Permitir autoria e execução de frentes independentes contra uma base identificada, mediante manifesto e DAG aprovados. A exigência de começar cada execução somente após integrar a anterior deixa de valer para essas tarefas independentes.
3. Manter as dependências próprias L2→L4: L4 não é certificado/promoção aceita antes do L2 correspondente aceito e de contratos compartilhados prontos.
4. Permitir integração de lotes pequenos nominalmente definidos. A ordem SER numérica é rastreabilidade, não autorização tácita nem obrigação de esperar uma frente independente bloqueada.
5. Centralizar implementação, schemas, casos, oráculos, command registry e correções na autoria repo-side. Workers locais executam/auditam tarefas fechadas e não alteram critérios ou produto.
6. Reservar integrador/publicador como escritores exclusivos dos espaços compartilhados. O integrador local executa somente preparação mecânica aprovada; decisão funcional volta à autoria.
7. Separar diagnóstico de certificação. Diagnóstico agrega falhas independentes; certificação usa candidata congelada, uma tentativa por rodada, sem reparo/retry-until-green.
8. Preservar FAILs e estados históricos. Introduzir critérios atuais vinculados à projeção de policy aprovada, não ao resultado que o código gostaria de declarar. Nenhum gate SEF é omitido sem mapeamento explícito.
9. Preservar autorização de efeitos, promoção e merge como gates humanos distintos. O aceite desta direção não aceita candidatas futuras nem autoriza publicação geral.
10. Exigir qualificação do mecanismo, isolamento e dois pilotos sem colisão antes de ampliar concorrência. Limites de cliente e permissões efetivas são medidos; nomes de modelos não substituem essas provas.
11. Classificar evidência pela observação disponível. Declaração de intenção/uso por modelo não equivale a ferramenta chamada, e hash não autentica pessoa.
12. Confirmar pacote publicado e claims pós-policy separadamente do merge. Qualquer capacidade não disponível permanece explicitamente fora da promoção efetiva.

## Consequências

O processo reduz handoffs e repetição de infraestrutura sem permitir que agentes paralelos alterem o contrato que os avalia. A responsabilidade de autoria cresce na preparação: cada pacote deve chegar ao laboratório com implementação e testes realmente prontos. Falha compartilhada bloqueia os consumidores afetados; falha de domínio não precisa interromper todas as frentes independentes.

A formalização não modifica policy nem atribui resultados de runtime. As seis skills já no target entram em regressão. MM/PSEF mantêm suas branches/decisões próprias; cardinalidade ou engine comum não podem mudar incidentalmente durante uma campanha congelada.

## Critério de vigência executável

O adendo pode registrar a decisão operacional antes do código. A execução paralela só é liberada após B0 qualificado, perfil completo, autorização local delimitada e release verificada. A vigência documental não equivale à prontidão técnica da infraestrutura.



---

<a id="sec-23"></a>

# 14 — Checklist que impede o próximo handoff defeituoso

Este checklist não está preenchido como PASS. Os itens são obrigações futuras de liberação; a entrega atual apenas os especifica. O executor não usa este texto para marcar a própria implementação como pronta sem evidência.

| ID | Área | Condição objetiva | Fase |
|---|---|---|---|
| RD01 | Mandato | Adendo formalizado, scope/roles claros e nenhuma contradição normativa sem decisão. | AUTHORING |
| RD02 | Base | SHA/tree e vetor before/allowed_after nominais, independentes da candidata. | AUTHORING |
| RD03 | Implementação | Código real e APIs públicas existentes, assinaturas/retornos/efeitos inspecionados. | AUTHORING |
| RD04 | Sintaxe | Parse/imports/schemas dos arquivos alterados e fixtures sem erro conhecido. | AUTHORING |
| RD05 | Fases | Testes e gates funcionam na fase a certificar; fixture L2 não exige policy global L2 após promoção. | AUTHORING |
| RD06 | Cobertura | Todas as famílias SE08/CI/SER01 mapeadas até métodos, sem omissão inexplicada. | AUTHORING |
| RD07 | Oráculos | Positivos conferíveis e negativos que chegam à fronteira pretendida; sem cálculo esperado circular. | AUTHORING |
| RD08 | Casos | Todos os casos aplicáveis têm test IDs, parâmetros, fixture hashes, tolerâncias e saídas. | AUTHORING |
| RD09 | Coleta | Lista de testes coletados fecha com a lista esperada; skips/xfails/NA autorizados e explícitos. | QUALIFICATION |
| RD10 | Mecanismo | M01–M28 implementados/qualificados; nenhuma falsificação de PASS aceita. | QUALIFICATION |
| RD11 | Cliente | Modelos/versão/configuração efetivos observados; TOML suportado e sem overrides perigosos. | QUALIFICATION |
| RD12 | Sandbox | Tentativas negativas de escrita/credencial/escape realmente bloqueadas; não apenas prompt. | QUALIFICATION |
| RD13 | Recursos | Clones, processos, temporários, budgets e leases exclusivos prontos. | QUALIFICATION |
| RD14 | Concorrência | Dois pilotos sem mistura de evidência, colisão ou propagação excessiva de falha. | QUALIFICATION |
| RD15 | Diagnóstico | Falhas independentes coletadas com first failure preservado, sem reparo automático. | QUALIFICATION |
| RD16 | Freeze | Renderer/snapshot realizados antes, git limpo, deltas permitidos, envelope externo SHA-bound. | FREEZE |
| RD17 | Comandos | Registry fechado e hashes de argv/scripts, sem placeholder não resolvido ou shell arbitrário. | FREEZE |
| RD18 | Evidência | RAW imutável, SHARE separado, verificador independente e falha de persistência exercitada. | FREEZE |
| RD19 | Auditoria | Dois papéis independentes, contratos/finding schemas prontos e critérios anteriores aos resultados. | FREEZE |
| RD20 | Externo | Capacidade/identidade do ambiente e destinos autorizados; caso literal e transporte testados. | EXTERNAL |
| RD21 | Observabilidade | Grau mínimo por caso estabelecido; ausência de UI não é substituída por narrativa privada. | EXTERNAL |
| RD22 | Efeitos | Exit e efeito separados; readback/cleanup autorizados; sem retry de escrita desconhecida. | EXTERNAL |
| RD23 | Promoção | Somente após provas/aceite específico; delta final permitido de policy e nova certificação. | PROMOTION |
| RD24 | Merge/Publicação | Aceite do SHA exato, remotos reconfirmados, árvore integrada e deployment distinguidos. | INTEGRATION |

## Contraditório obrigatório antes da delegação

O revisor tenta demonstrar que a candidata ainda pode produzir um resultado enganoso: teste temporal stale, pacote com schema que aceita campo desconhecido, chamada omitida com output plausível, um ERROR escondido entre falhas admitidas, ou uma publicação com efeito não observado. Se o problema já é conhecido, corrigi-lo na autoria; não entregar ao executor como surpresa deliberada.

Confirmar também a economia do processo: a task não contém etapas duplicadas sem motivo, uma falha independente não cancela tudo, um finding editorial não reabre automaticamente uma campanha funcional e o usuário não precisa copiar repetidamente a mesma evidência. Rigor deve detectar risco, não acrescentar cerimônia sem informação.

## Critério de saída

Gates da fase sem bloqueio material; evidências verificáveis; nenhum teste obrigatório não implementado; limites explícitos. O marco resultante é liberação da próxima fase, não aprovação de todas as seguintes.