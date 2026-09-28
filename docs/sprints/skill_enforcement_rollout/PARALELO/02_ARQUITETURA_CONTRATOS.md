# 02 — Arquitetura, contratos e interfaces a implementar

## 2.1 Camadas e limites

1. **Plano e dossiês:** arquivos versionados que declaram requisitos, decisão de domínio e testes. Esta entrega pertence a essa camada.
2. **Pacote executável:** implementação, testes, fixtures, perfis e registro de comandos. A autoria repo-side o produz antes de liberar qualquer worker.
3. **Launcher determinístico:** valida manifesto/autorizações, reserva diretórios e recursos, lança processos isolados, captura evidência e bloqueia ações fora do contrato. Não delega decisão de segurança ao LLM.
4. **Agentes de campanha determinística:** coordenador, executores e auditores recebem escopos fechados. Podem diagnosticar, mas não alterar a candidata congelada, resultados ou critérios. O A1 Authoring Executor do ADR-0024/0025 é outro papel: ele pode alterar somente `repo_scope.write_roots` entre rodadas causais, nunca durante a certificação.
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
