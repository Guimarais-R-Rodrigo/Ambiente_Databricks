# Changelog

## 2026-09-23 — SER00 A07-R2: corretiva test-only do oráculo de storage

### Corrigido

- (ChatGPT) `tools/tests/test_certify_storage_cleanup.py` deixa de recuperar o registro da invocação por `sys._getframe(1).f_locals` e passa a interceptar `TemporaryDirectory.cleanup()`, usando o `record` já pertencente ao wrapper concreto. O `certify_local.py` de produção permanece inalterado.
- (ChatGPT) A fixture registra `native_preemptions` quando o cleanup real falha antes da injeção sintética. Esse caminho continua reprovando explicitamente com `NATIVE_STORAGE_CLEANUP_PREEMPTED_FIXTURE`; não há retry, sleep, `ignore_errors` nem conversão de WinError32 real em PASS.
- (ChatGPT) `test_se08_windows_corrective.py` ganha guarda estática para impedir retorno à introspecção de stack e exigir o binding direto da fixture.

### Limites

- A correção parte da `main@11851e137dd7793b351ac08fc211c0be90005dee` em branch de manutenção separada; não reabre/reclassifica SE08 e não altera policy, skills, runtime do produto ou níveis.
- O A07-R1 da SER00 permanece FAIL preservado. A correção repo-side ainda requer uma única campanha Windows/NTFS sobre SHA congelado antes de qualquer integração; SER00 permanece `NOT_READY` e SER01 `NOT_STARTED`.


## 2026-09-22 — SE08: integração, gate Free e fechamento

### Integrado

- (ChatGPT) RC `ee1cf04b...` certificada com FULL SE08 Windows 21/21, CI Windows 10/10 e gate Databricks Free PASS com 573/573 arquivos comparados, zero ausentes/obsoletos e 14/14 skills.
- (ChatGPT) PR #90 integrada em `627bcc798...` após aceite humano. A primeira rodada pós-merge preservou um FAIL de portabilidade em Python 3.11: a suíte SE07 chamava `PosixPath.is_junction()` onde a API não existia.
- (ChatGPT) PR #92 corrigiu a detecção de junction e o filtro de dependências do workflow de transição. No SHA de integração `431c46fc...`, 17/17 workflows disparados concluíram em success, inclusive o workflow Python 3.11 que revelou o defeito.
- (ChatGPT) PR #93 realizou somente o fechamento documental e foi integrada em `85474968...`; sua rodada pós-merge concluiu 18/18 workflows em success, incluindo SE01 e SE02.

### Estado final

- `SE08_RC_FULLY_CERTIFIED=true` para a release candidate certificada;
- `SE08_INTEGRATED=true`;
- `SE08_POST_MERGE_ACTIONS=PASS`;
- `DATABRICKS_FREE=PASS`;
- `GENIE_BEHAVIORAL_SCREENING=NOT_APPLICABLE` ao delta SE08;
- SE06/SE07 permanecem com suas classificações históricas;
- WinError32 permanece intermitente, sem root cause estabelecida;
- `PROMOCAO_TRABALHO=BLOQUEADA`.


## 2026-09-22 — SE08 R5: amostra prioritária no instante pós-WinError32

### Incorporado

- (ChatGPT) Incorporada a campanha Windows R4: standalone storage/certifier verdes, CI FAIL apenas em SEF, com WinError32 no timeout pai-filho; Restart Manager e FileProcessIdsUsingFileInformation retornaram vazios após a falha.
- (ChatGPT) A observação nativa passa a consultar primeiro o recurso cujo unlink falhou, antes de Restart Manager, traceback e inspeções secundárias. Cada amostra registra timestamps monotônicos, duração e delta desde o instante em que o cleanup error foi capturado.
- (ChatGPT) O certifier registra que seus próprios objetos Python stdout/stderr já estão fechados imediatamente antes da saída do TemporaryDirectory, separando handle do processo pai de handles externos/herdados.

### Estado

- R4 Windows: `R4_WINDOWS_NOT_READY`.
- WinError32: intermitente, sem owner identificado.
- promoção ao trabalho: bloqueada.


## 2026-09-22 — SE08 R4: identificação diagnóstica de PIDs por arquivo

### Incorporado

- (ChatGPT) Incorporada a campanha Windows R3 em `3556f198...`: storage standalone 9/9, certifier standalone exit 0, CI 10/10 e FULL FAIL 20/21 por uma única ocorrência nativa WinError32 no storage. Na falha, Job Object estava vazio, launcher/child encerrados e Restart Manager não reportou processos.
- (ChatGPT) Adicionada consulta pós-falha `NtQueryInformationFile(FileProcessIdsUsingFileInformation)` por recurso para observar PIDs que usam o arquivo no exato boundary do WinError32. A consulta é read-only, single-shot e não altera cleanup/verdict.
- (ChatGPT) O PID do próprio observador é marcado como ambíguo porque o handle aberto para a consulta pode fazê-lo aparecer no resultado; somente PIDs adicionais são evidência discriminante de outro processo.

### Estado

- R3 Windows: `R3_WINDOWS_NOT_READY`.
- FULL R3: FAIL 20/21.
- owner do handle: ainda não identificado.
- promoção ao trabalho: bloqueada.


## 2026-09-22 — SE08 R3: observabilidade do WinError32 no boundary real

### Incorporado

- (ChatGPT) Incorporada a campanha Windows da R2 em `d3720f59...`: storage standalone FAIL 8/9 por WinError32 nativo preemptando uma injeção sintética; certifier standalone 46/46 PASS; CI Windows FAIL somente em `sef/certifier_regression`, com segunda ocorrência nativa no timeout pai-filho; FULL não executado. O antigo teste de resíduo passou e sustenta a correção do problema de finalizer da fixture, sem implicar correção do WinError32.
- (ChatGPT) O certifier passa a registrar, somente depois de um WinError32 já ocorrido, consulta read-only ao Restart Manager e estado instantâneo dos PIDs supervisionados. Também registra o Job Object após término e antes do fechamento. A telemetria não faz retry, sleep, remoção adicional, encerramento de aplicações ou mudança de verdict.
- (ChatGPT) `ci_local.py` deixa de truncar em 4.000 caracteres a saída de uma etapa reprovada; failures futuros permanecem integralmente auditáveis no log do comando.
- (ChatGPT) O loader do observador Restart Manager resolve explicitamente o arquivo irmão quando o certifier é carregado por `spec_from_file_location`; assim a regressão Windows do certifier não perde a observação por depender de `sys.path` incidental.

### Estado

- R2 Windows: `WINDOWS_NOT_READY`.
- FULL R2: `NOT_RUN_CONDITION_NOT_MET`.
- WinError32: causa ainda não estabelecida.
- promoção ao trabalho: bloqueada.


## 2026-09-22 — SE08 R2: hardening repo-side antes da nova campanha Windows

### Corrigido

- (ChatGPT) A fixture sintética de storage mantém viva a `TemporaryDirectory` defeituosa até o oráculo externo observar o resíduo; somente depois do snapshot ocorre teardown explícito via `TemporaryDirectory.cleanup()`, que desarma o finalizador pelo caminho normal. Isso remove o falso negativo causado por limpeza implícita do CPython sem alterar o certifier de produção, sem retry e sem converter falha de cleanup em PASS.
- (ChatGPT) O perfil FULL SE08 passa a incluir explicitamente as suítes de storage cleanup, guardrails da corretiva Windows e regressões do observador diagnóstico. Assim, um FULL futuro não pode ficar verde omitindo novamente o gate de storage.
- (ChatGPT) Adicionado observador opt-in de lifecycle/Job Object/Restart Manager. O probe nativo mira explicitamente `test_keyboard_interrupt_before_first_output`, que foi o caso real do WinError32; ausência de reprodução continua sem valor de certificado causal.

### Corrigido durante a auditoria S5

- (ChatGPT) A rodada seguinte do CI geral preservou um segundo FAIL repo-side no gate SEF: `test_skill_enforcement_se08.py` continha sequências literais `\\n` dentro do comentário da fixture de identidade, deixando o `if` da linha 128 sem corpo e produzindo `IndentationError`. A fixture foi reformatada em linhas Python reais e a corretiva ganhou um `ast.parse` explícito do módulo operacional SE08.

- (ChatGPT) A primeira rodada automática de Actions no SHA `089a5e7d...` preservou um FAIL em Skill Enforcement SE01 exclusivamente no snapshot README: o próprio `validate_assistant.py` importava um helper sob `ambiente_fonte/.assistant` sem suprimir bytecode, criava `__pycache__` e depois convertia essa sujeira criada por ele mesmo em warning. O validador passa a definir `sys.dont_write_bytecode=True` antes dos imports locais; a regra de warning e o snapshot não foram relaxados.

- (ChatGPT) O observador nativo agora falha fechado quando o teste-alvo não executa exatamente uma vez ou fica `skipped`; `unittest.wasSuccessful()` isoladamente não é mais suficiente para produzir exit 0. Isso impede que ausência de observação Windows seja tratada como resultado diagnóstico bem-sucedido.
- (ChatGPT) A fixture de storage passou a registrar ownership/finalizer no instante do oráculo e usa `TemporaryDirectory.cleanup()` somente depois do snapshot, em vez de desarmar o finalizador manualmente; o teardown continua exclusivamente test-only.

### Reconciliado

- (ChatGPT) Reaplicada à linha remota a correção local `3118e970`: a identidade corporativa sintética é construída em runtime para não ser capturada pela própria varredura estática.
- (ChatGPT) Reconstituída a materialização local `e3e67bce` copiando os quatro blobs canônicos exatos para `Novo_Ambiente_Simulado`. Nenhuma edição manual de conteúdo derivado foi inventada.

### Limites

- Esta R2 é repo-side e ainda NÃO certifica Windows/NTFS, WinError32, FULL, Free ou Genie.
- O SHA local histórico `5b2c1692` permanece evidência da campanha anterior; a R2 é uma nova linha remota e não reclassifica resultados históricos.
- Permanecem `S06-A1-R4=NOT_RUN`, `SE06_DOD=INCOMPLETE`, `SE07_FULLY_CERTIFIED=false`, L2 global para `hub-ml-criar-objeto` e promoção ao trabalho bloqueada.

## 2026-09-22 — SE08: integração local da corretiva Windows/CI (Codex)

- (Codex) Integrados por cherry-pick os 17 commits da corretiva remota `49860959`, preservando os commits locais `3118e970` e `e3e67bce` e os quatro arquivos derivados. Telemetria observacional e reparos de testes serão certificados serialmente no SHA congelado; não constituem correção causal de WinError32. Skips ambientais não comprovam guardrails. Dívidas SE06/SE07, storage FAIL 8/9, L2 global e promoção ao trabalho bloqueada permanecem. Resultados brutos em evidência externa exclusiva desta rodada; nenhuma publicação autorizada por este registro.

## 2026-09-22 — SE08: materialização local do derivado (Codex)

### Atualizado

- (Codex) Renderer canônico rematerializou os 574 arquivos do simulado; somente Manual Técnico, template de skill, README da policy e README de skills diferiram, refletindo mecanicamente a fonte consolidada. Snapshot do README conferido pela saída real, sem alteração de contagens. A certificação da nova candidata fica vinculada ao SHA congelado em evidência externa; este registro não presume PASS, publicação ou promoção.

## 2026-09-22 — SE08: fixture sintética compatível com a guarda de identidade

### Corrigido

- (Codex) O teste de recusa de identidade corporativa monta a fixture sintética em runtime, preservando o valor e a asserção de bloqueio antes da autenticação. A primeira validação local da base `25013c53` reprovou por detectar o literal no código do teste; o FAIL está preservado na evidência externa. Nenhuma regra de identidade, policy ou nível foi alterada.

## 2026-09-22 — SE08: consolidação repo-side para operação permanente

### Adicionado

- (ChatGPT) Perfil cumulativo `se08` no certifier, regressões operacionais e suíte dedicada de I/O da policy; o subgate SEF do `ci_local.py` usa o perfil SE08 em modo parcial/read-only, sem substituir a certificação FULL.
- (ChatGPT) Pasta `docs/sprints/skill_enforcement/SE08/` com objetivo, matriz de testes, resultados observados, checkpoint e runbook local.
- (ChatGPT) Gate de promoção SE08 e rollback incorporados ao runbook/checklist de transição para o trabalho.

### Corrigido

- (ChatGPT) `se07_policy.py`: validator e resumo usam o mesmo parse da policy, preservam `assistant_root` e retornam `POLICY_UNREADABLE` estruturado para arquivo ausente, ilegível, UTF-8 inválido ou JSON malformado, sem releitura contraditória.
- (ChatGPT) `validate_contracts.py`: `UnicodeDecodeError` é tratado como contrato ilegível.
- (ChatGPT) `validate_assistant.py`: contratos e registry SEF passam a integrar o validador geral contra a mesma raiz analisada.

### Documentado

- (ChatGPT) Template canônico de skill, guia de Agent Skills, policy README, Manual Técnico e ferramentas SEF passam a documentar `current_level`, `target_level`, rollout e os gates permanentes da SE08.
- (ChatGPT) `hub-ml-criar-objeto` não foi promovida: permanece L2 global. `hub-ml-auditoria-skills` já estava integrada à policy/Receipt/verifier e não recebeu mudança artificial.
- (ChatGPT) G2 continua limitado à transição SE06→SE07. Com `SE06_DOD=INCOMPLETE` e `S06-A1-R4=NOT_RUN`, a promoção corporativa da SE08 permanece bloqueada até nova decisão humana específica e evidência suficiente.

### Estado e limites

- (ChatGPT) Repo-side consolidado, porém ainda não release candidate: `Novo_Ambiente_Simulado/` deve ser rematerializado pelo renderer canônico; snapshot verificável do README, FULL SE08, CI local real, Windows/NTFS, Free/Genie e futura Actions/PR permanecem pendentes.
- (ChatGPT) Preservados `SE07_FULLY_CERTIFIED=false`, storage cleanup histórico FAIL 8/9 e a distinção `NATIVE_WINERROR32_NOT_REPRODUCED_IN_THIS_RECERTIFICATION` ≠ `WINERROR32_FIXED`. Nenhum residual foi convertido em PASS.


## 2026-09-21 — SE07: hotfix pós-merge para policy com UTF-8 inválido

### Corrigido

- (ChatGPT) `tools/skill_enforcement/se07_policy.py`: `UnicodeDecodeError` passa a ser tratado como `POLICY_UNREADABLE` tanto no validator quanto na leitura de resumo, preservando `FAIL` estruturado e evitando traceback no CLI `--json`.
- (ChatGPT) `tools/tests/test_skill_enforcement_se07.py`: o adversarial de policy ilegível passa a cobrir também arquivo existente com bytes UTF-8 inválidos.

### Proveniência

- Achado P2 tardio do review automatizado da PR #81, surgido após o merge `73cacdd44fbccc80da835d96388ca23b6a6fcefc`. O hotfix não altera `policy.json`, níveis, registry, runtime das skills nem as dívidas preservadas de SE06/SE07.


## 2026-09-21 — SE07: hotfix pós-merge para policy ilegível

### Corrigido

- (ChatGPT) `tools/skill_enforcement/se07_policy.py`: `summarize()` preserva o `POLICY_UNREADABLE` emitido pelo validator quando o arquivo de policy está ausente, ilegível ou com JSON malformado e retorna `FAIL` estruturado em vez de traceback.
- (ChatGPT) `tools/tests/test_skill_enforcement_se07.py`: cobertura adversarial para policy ausente e JSON malformado, incluindo execução CLI `--json`, exit 1, payload estruturado e ausência de traceback.

### Proveniência

- Achado P2 do review automatizado da PR #80, surgido após o merge da SE07. O hotfix não altera policy, níveis, registry, runtime das skills nem a dívida residual já aceita.


## 2026-09-21 — SE07: encerramento humano com residual conhecido

### Atualizado

- (ChatGPT) Registrado o aceite humano explícito da PG-01 apesar da falha do oráculo sintético de resíduo. O gate permanece FAIL, o FULL permanece 16/16 PASS e `SE07_FULLY_CERTIFIED=false`.
- (ChatGPT) SE07 encerrada com DoD de policy registry 14/14 satisfeito, dívida residual preservada e sem promoção global adicional de `hub-ml-criar-objeto`.
- (ChatGPT) A candidata testada local `4b8bb46d...` e a publicação remota `b5a4eb9d...` compartilham parent `8db4c984...` e a tree exata `c36e5015...`.


## 2026-09-21 — SE07: PG-01, prontidão da fixture de timeout

### Corrigido

- (Codex) `tools/tests/test_validate_create_readme.py`: integrada localmente a proposta PG-01 conferida por SHA-256; a fixture observa prontidão com prazo finito antes do timeout real de 1,5 s e exige o artefato de PIDs. Nenhum timeout ou algoritmo de produção mudou.

### Notas

- (Codex) `docs/sprints/skill_enforcement/SE07/TESTES.md`: documentados escopo, cobertura independente de startup e controles Windows (cinco aprovações, duas reprovações esperadas). Novo SHA requer a bateria final completa; os aceites anteriores não aprovam esta alteração nem autorizam push.


## 2026-09-21 — SE07: aceite humano da corretiva de cleanup

### Atualizado

- (ChatGPT) Registrado aceite humano explícito da corretiva `74f92f02...` em `CHECKPOINT.md` e no handoff correspondente. O aceite autoriza seguir à recertificação nativa Windows/NTFS, mas não equivale a PASS técnico, não elimina o WinError32 histórico e não promove canônica/current_level.


## 2026-09-21 — SE07: decisão humana sobre o piloto README

### Atualizado

- (Codex) `docs/sprints/skill_enforcement/SE07/CHECKPOINT.md`: registrado o aceite humano de `19328661`, separado do resultado técnico NAO_PRONTA e do FAIL WinError32 preservado. Próximo passo recomendado: corretiva focalizada e recertificação; nenhum código ou nível alterado.

## 2026-09-21 — SE07: corretiva de cleanup após auditoria (ChatGPT)

### Adicionado

- (ChatGPT) Suíte `tools/tests/test_certify_storage_cleanup.py`: oráculos externos de cancelamento, falha temporária/journal, resíduo, timeout e controles positivos.

### Corrigido

- (ChatGPT) `tools/skill_enforcement/certify_local.py`: separar término de processos da remoção temporária, registrar exceções completas e preservar cancelamento quando cleanup falha; nenhuma falha de limpeza vira PASS.
- (ChatGPT) `test_validate_create_readme.py`: exigir cleanup agregado FAILED no erro sintético, sem perder interrupção/130 nem a evidência da exceção.
- (ChatGPT) `README.md`: atualizar somente os dois censos medidos de arquivos/links alterados pela nova suíte e handoff; a validação histórica continua exigindo Git completo.

### Notas

- (ChatGPT) [Handoff da corretiva](docs/handoffs/2026-09-21_se07-auditoria-storage-cleanup.md): original NAO_APTA; causa nativa WinError32 não estabelecida; implementação local não equivale a certificação Windows, promoção ou aceite.

## 2026-09-21 — SE07: piloto estreito README L3 (Codex)

- (Codex, agente A) Runner generate/apply para create/readme/agregador, bytes determinísticos e bindings, criação exclusiva Windows/NTFS e evidência de efeitos/falhas sem homologação. Proteção ancestral foi refutada em v1 e corrigida com prova causal.
- (Codex, agente B) Suíte adversarial independente: autorização, topologia, concorrência, interrupção real, parciais, persistência, releitura e retry; vermelhos preservados antes das correções.
- (Codex, agente C) Gate em clone completo com overlay único e validator real, checks editoriais/links, binding base/path/bytes e regressões de cancelamento/cleanup. Reusa certifier aceito sem alterá-lo; erro intermediário de compartilhamento e limites de observação preservados.
- (Codex, coordenação) F-04 aceita promovida por fast-forward; integração isolada, SKILL/manifest/renderer, interface pré-dispatch, checkpoint/testes/handoff e evidência bruta selada. D2/D9 parcialmente aprovada somente para o piloto; policy/contrato L2, SE06 e históricos preservados. Gates do SHA documental serão medidos depois do freeze, com publicação exclusiva da review se segura.

Toda mudança relevante deste projeto é registrada aqui, em entradas curtas, sem
expor identificadores corporativos, PII ou segredos. Formato: seções por data,
subseções Adicionado/Atualizado/Corrigido/Removido, cada item com a IA autora
entre parênteses. Template: `.claude/templates/changelog-entry.md`.


## 2026-09-21 — SE07: corretiva SUP-F04-01/02/03 (Codex)

### Corrigido

- (Codex, agente A) Preservação da invocação, streams e exit observado quando o journal falha; início confirmado, ausente e desconhecido separados. Cancelamento durante campanha/finalização mantém saída não zero, sem alterar help/parsing.
- (Codex, agente B) Regressões adversariais de persistência e cancelamento externo; teste de interrupção usa ready após print/flush, com casos pré-output e never-ready e cleanup observado.

### Documentado

- (Codex, coordenação) Integração com procedência dos patches, handoff/checkpoint/testes versionados, prova bruta externa identificada por hash, F-03 remota aceita e review condicionada aos gates/workflows. FAILs históricos e WinError32 intermediário preservados; D2/D9 continua proposta não aprovada. Gates do SHA documental serão medidos após seu congelamento.

## 2026-09-21 — SE07: F-04/D10 e proposta D2/D9 (Codex)

### Adicionado

- (Codex, agente A) Suíte permanente do certifier com fault injection, controles externos, reserva concorrente de evidência e timeout real de árvore própria; preservados os gates e os consumidores existentes.
- (Codex, agente B) Proposta D2/D9 NÃO APROVADA com matriz de conversão, fronteira runtime/repositório e piloto futuro de README agregador. Doze probes API L2 somente leitura na base, sem writer ou mudança de policy.

### Corrigido

- (Codex, coordenação após revisão B) Metadata Windows ausente/malformada impede sucesso; gate executado permanece registrado mesmo quando seu log falha; falha de cleanup é distinta de falha observada do gate na contagem.

- (Codex, agente A) Certifier falha fechado em Git obrigatório não observável, reserva exclusiva de evidência, identidade final/cobertura e limites por processo. Saídas diagnósticas não certificam release limpa; falhas de persistência ou cleanup impedem sucesso.

### Notas

- (Codex, coordenação) Integração em clone e branch locais isolados, documentação operacional e snapshot README reconciliado com a medição final. Certificação do SHA exato e revisão interna B ficam no handoff externo; não equivalem a aceite humano, FULL multiplataforma ou homologação Free/Genie.

## 2026-09-21 — SE07: aceite F-03 e reconciliação E-01/E-02 (Codex)

### Corrigido

- (Codex, coordenação) Retificação aditiva das duas campanhas Linux FULL FAIL e da terceira interrompida, com paths/hashes dos bytes recuperados; relatórios e logs históricos preservados.
- (Codex, coordenação) Desambiguação textual de issues no contrato de auditoria: coleção vazia lista/tupla, normalizada para lista; fingerprint correspondente e espelho canônico, sem alteração do runner.

### Notas

- (Codex, coordenação) Aceite humano focalizado de F-03 registrado. Push do checkpoint bloqueado por credenciais Git; novo lote apenas local e sujeito à certificação própria. SE06, política D2 e níveis atuais preservados.

## 2026-09-21 — SE07 F-03/D6: adapter canônico da auditoria (Codex)

### Corrigido

- (Codex) O adapter L3 da auditoria agora distingue verifier localizado, importado, chamado, concluído, retorno bem formado e conclusão validada. Falha de importação retorna envelope `NOT_REVERIFIED`; falha de chamada e retorno malformado retornam `NOT_PASS_REVERIFIED` com diagnóstico estruturado.
- (Codex) `PASS_REVERIFIED` passa a exigir a forma canônica atual do verifier EDA, os quatro sinais positivos, `status="VALID"` e `issues` vazio. A suíte cobre import/call failure, não-mapping, mapeamentos incompletos, tipos inválidos, sucesso real sintético e retorno contraditório.

### Estado e limites

- (Codex) O aceite humano de `b6fb595...` é registrado como checkpoint L2 local publicado por fast-forward na branch SE07. A candidata F-03 é local e requer certificação/revisão próprias; não houve push dessa nova candidata, PR, Actions, Free/Genie, merge ou mudança de níveis.
- (Codex) F-02 permanece preservado. F-04/D10, D2/D9, criar-objeto L3, R2, SE08, Receipt/proveniência, policy, scorer e SE06 continuam fora desta rodada.

## 2026-09-20 — SE07 R1-C: confirmação residual do preflight L2 (Codex)

### Corrigido

- (Codex) P01: após fallback por ausência, o preflight volta a resolver estritamente o caminho efetivo. Um alias composto que normaliza para arquivo como ancestral agora bloqueia API/CLI, enquanto sufixo novo e dangling link interno simples continuam permitidos.

### Validado e preservado

- (Codex) P01 foi reproduzido primeiro em Linux/WSL Python 3.12.3, no blob R1-C hash-pinado; P02 (`missing/../cycle`) permaneceu bloqueado nesse runtime. A regressão POSIX é skip explícito no Windows, sem remover os vetores de junction Windows.
- (Codex) F-02, renderer, `.gitattributes`, certifier, contrato, policy, D2, SE06 e componentes L3 permanecem fora desta correção. A nova candidata requer certificação própria e revisão; a R1 auditada permanece NAO_APTA.

## 2026-09-20 — SE07 R1-C: correção pós-auditoria da R1 (Codex)

### Corrigido

- (Codex) F-01: resolução estrita antes da tolerância exclusiva a `FileNotFoundError`, bloqueando ciclos de junction Windows sem proibir destinos novos ou links internos resolvíveis. Regressões nativas de ciclos, origem/template, controles positivos e decisão D2 preservada.
- (Codex) F-02: marker do renderer emitido explicitamente com LF, conforme `.gitattributes`, com teste de bytes, cópia fiel e duas renderizações idempotentes. Derivado regenerado pela ferramenta canônica.

### Estado e limites

- (Codex) R1 auditada `2d25bd2...` permanece `NAO_APTA`. Esta candidata corretiva exige FULL em clones novos Windows/Linux do mesmo SHA; identidades e resultados definitivos ficam no handoff externo indicado no checkpoint, sem autorreferência no commit.
- (Codex) F-03 (adapter auditor L3) e F-04 (infraestrutura do certifier) continuam dívidas distintas; salvaguardas externas não corrigem esses componentes. Sem mudança de contrato, níveis, SE06, Receipt, política D2 ou autorização de escrita/publicação. R1-C é rótulo operacional, não nova sprint nem R2.

## 2026-09-20 — SE07 R1: estabilização delimitada de criar-objeto L2 (Codex)

### Corrigido

- (Codex) Preflight de criar-objeto: contenção física de origem/destino/template, recusa de traversal, drive-relative, UNC e componentes inseguros de seção; aliases do mesmo objeto não satisfazem “converter é mover”.
- (Codex) Entradas inadequadas na API/CLI retornam diagnóstico estruturado; falhas internas inesperadas não são disfarçadas de entrada inválida. Tipos, schema, níveis e permissões de escrita permanecem os do contrato vigente.

### Adicionado e atualizado

- (Codex) Regressões sintéticas na suíte SE07, incluindo seis tipos, links/junctions, hardlinks, template ausente e observação de ausência de escrita; prova dos defeitos originais preservada em bundle externo antes da correção.
- (Codex) Checkpoint, README, testes e runbook reconciliados para distinguir baseline intacta, candidata local e pacote Free histórico; exemplos antigos permanecem identificados como históricos. Derivado regenerado pela ferramenta canônica.
- (Codex) Reconciliação histórica, sem reivindicar autoria das implementações anteriores: a baseline herdada `a01d12ff4e0cb7cfd795ade164f9ce9daad372ba` passou os 15 gates do primeiro FULL_SE07_LOCAL da R1. O commit R1 exige evidência própria do SHA final no bundle externo indicado no checkpoint.

### Limites preservados

- (Codex) Por decisão explícita do usuário, origem `"."`, relações ancestral/descendente e destino existente em conversão mantêm a semântica herdada e ficam pendentes de política específica. PASS L2 não autoriza overwrite, merge ou conversão executada.
- (Codex) Auditoria L3 foi apenas diagnosticada em fixtures externas; certifier, schemas, policy e SE06 não foram alterados. SE06 continua 24/25 observados, A1-R4 NOT_RUN e DoD INCOMPLETE. Sem L3 de criar-objeto, publicação Free, push, PR, Actions ou merge nesta rodada.

## 2026-09-16 — SE02: preflight verificável do Skill Enforcement Framework (ChatGPT)

### Adicionado

- (ChatGPT) `hub_scripts.skill_execution` com API pública `run_preflight`, resultado estruturado `PASS`/`BLOCKED`, decisões por recurso/template e `writes_performed=false`.
- (ChatGPT) Script fino `hub-ml-eda-profissional/scripts/preflight.py`, suíte SE02 com 18 casos e workflow dedicado `Skill Enforcement SE02`.

### Atualizado

- (ChatGPT) `hub-ml-eda-profissional` passa a exigir preflight L2 antes do core analítico, mantendo `execution_contract` v0.1 em `mode="audit"`.
- (ChatGPT) Manual Técnico, catálogo de `hub_scripts`, Plano Mestre e ambiente simulado foram reconciliados; `Novo_Ambiente_Simulado` foi materializado exclusivamente pelo renderer canônico.
- (ChatGPT) Branch SE02 reconciliada com `main@ae9337204a7c769c0b28b33321c8b81afdff6bae` após correção transversal do guard V08, sem force-push.

### Evidências e limites

- (ChatGPT) A implementação preserva SE03 não iniciada: sem runner determinístico, Execution Receipt, postflight, `mode="enforce"` ou alteração de `.assistant_instructions.md`.
- (ChatGPT) Condições sem contexto explícito são fail-closed; a resistência do Genie Code a contexto falso/bypass permanece hipótese a medir no Databricks Free e não é tratada como enforcement comprovado.
- (ChatGPT) Failures intermediários de estrutura, derivado, snapshot, Manual Técnico e guard V08 permanecem históricos e não são reclassificados como PASS.

## 2026-09-16 — SE01: contrato verificável e capability experiment (ChatGPT)

### Adicionado

- (ChatGPT) `execution_contract.json` v0.1 adjacente à `hub-ml-eda-profissional`, com 10 recursos, 4 templates, políticas `required`/`conditional`/`optional`, evidências declarativas e `mode="audit"`.
- (ChatGPT) JSON Schema Draft 2020-12, validador estático somente stdlib, suíte SE01 e workflow dedicado; o validator resolve API pública por `__init__.py`/AST e recusa paths de template inseguros, condições fora do vocabulário e modos não suportados.
- (ChatGPT) ADR-0021 para registrar a decisão de contrato verificável antes de qualquer preflight/runner definitivo.

### Atualizado

- (ChatGPT) Branch `sef/SE01-contrato` reconciliada por merge normal com `main@79f53ba1a131d93cbb0fea7bd885da32b82a7588`, preservando integralmente V14 e sem force-push; após a reconciliação, `behind_by=0`.
- (ChatGPT) `Novo_Ambiente_Simulado` rematerializado a partir da saída real de `tools/render_simulado.py --write`; o probe temporário e sua seção foram retirados da fonte e do derivado, enquanto o contrato permanece.
- (ChatGPT) Snapshot verificável do README raiz novamente medido em 1501 arquivos e 1979 links; os demais campos do bloco permaneceram coerentes com a execução.
- (ChatGPT) `tools/publicar_free.py` compatibilizado com notebook já materializado e fallback SOURCE, com regressões específicas na suíte SE01.

### Evidências

- (ChatGPT) Capability probe histórico no Databricks Free: `SEF_CAPABILITY_PROBE_V0_1`, `assistant_root_resolved=true`, import público de `fmt_int`, `sample_result="1.234"`, `writes_performed=false` e `status="PASS"` no cenário testado.
- (ChatGPT) Regressão natural EDA histórica: PASS para ausência de degradação material atribuível ao contrato/probe; isso não constitui enforcement nem aprovação científica do notebook.
- (ChatGPT) Na reconciliação final, failures intermediários permaneceram failures: primeiro o renderer detectou o derivado defasado; depois o snapshot detectou 1490/1978 versus 1501/1979. Após as correções correspondentes, o workflow dedicado SE01 passou integralmente na árvore com snapshot reconciliado.

### Limites

- (ChatGPT) SE01 permanece audit-only: não implementa preflight, deterministic runner, Execution Receipt, postflight, fail-closed runtime ou `mode="enforce"`; SE02 não foi iniciada.
- (ChatGPT) A evidência do probe é histórica e não prova execução determinística universal pelo Genie Code. O script experimental foi aposentado do produto final, sem apagar os resultados observados.
- (ChatGPT) PR #69 permanece Draft e não pode ser integrada sem aceite humano explícito; a homologação desta sprint não autoriza iniciar SE02.

## 2026-09-14 — MM00: integração e fechamento documental do Framework de Micromodelos (ChatGPT)

### Adicionado

- (ChatGPT) Fundação documental MM00–MM13 do Framework de Micromodelos, com Plano Mestre, inventário, matrizes de reuso/riscos/dependências, pacote de auditoria A1 e checkpoint fail-closed.
- (ChatGPT) ADR-0014 a ADR-0020 para congelar as fronteiras arquiteturais: micromodelo como artefato de domínio, `micromodelo.yaml` canônico, MLflow para histórico de runs, governança externa de publicação, piloto greenfield antes dos legados, consumo do Sistema de Temas e fontes limitadas ao catálogo configurado.

### Atualizado

- (ChatGPT) PR #43 integrada após aceite humano explícito; head final validado `e3809b15b61f2bc1eeec06c9de6f38a329868e98` e merge `36e89515a46df24f41deea4791b109f5a1f938f2`.
- (ChatGPT) ADR-0014 a ADR-0020 ratificados como aceitos sem ressalvas; MM01 continua condicionada às decisões detalhadas previstas nas sprints seguintes, sem antecipação silenciosa de schema, fingerprint ou tracking rule-based.
- (ChatGPT) Q-01 da auditoria A1 é fechado por esta manutenção pós-merge, conforme exceção D1-B: a entrada da MM00 foi diferida para preservar o histórico do changelog e agora é registrada de forma aditiva.

### Evidências

- (ChatGPT) Auditoria A1 independente: `APTA_COM_CORRECOES`; M-01 corrigido, nenhum `DIVERGE` atribuível à MM00 e Q-01 tratado pela D1-B até este fechamento.
- (ChatGPT) Bateria final da candidata: CI geral `34893158270`, V00 `34893158453`, V01 `34893158339` e V02 `34893158265`, todos `success` no mesmo head final; nenhum validador foi relaxado.

### Limites

- (ChatGPT) MM00 não cria skill, prompt funcional, helper, template executável, micromodelo real, consulta de dados, run MLflow, publicação ou migração de legado. Esta entrada fecha somente a pendência documental Q-01 antes da MM01.

## 2026-09-14 — V08: integração transversal e fechamento técnico (ChatGPT)

### Adicionado

- (ChatGPT) Matriz transversal de integração entre Sistema de Temas, skills, Hub Padrões, entrada `.assistant` e Manual Técnico.
- (ChatGPT) Suíte V08 e workflow permanente read-only com guarda explícita que proíbe alterações runtime Python em `hub_snippets` e `hub_scripts`.

### Atualizado

- (ChatGPT) Concierge, criação de objeto, EDA, baseline, safra, monitoramento e explainability passam a apontar para `ResolvedTheme` e consumidores `_resolvido` sem redefinir paletas ou política visual.
- (ChatGPT) O template visual da EDA deixa de ser uma segunda fonte de tema e preserva composição, hierarquia, leitura, tabelas, KPIs, emojis, índice e demais convenções editoriais.
- (ChatGPT) Hub Padrões e Manual passam a descrever V02–V07 integradas, Visual Lab, geração editorial, consumidores V07 e limites atuais.
- (ChatGPT) O README raiz foi compactado para atuar como entrada operacional, mantendo o histórico detalhado no índice canônico de sprints e preservando o bloco verificável do gate local.
- (ChatGPT) PR #42 integrada após aceite explícito de Rodrigo; head final validado `9af5615d79b02cbd86f5a6d084444c83f203ae03` e merge `622d2c962a80998cf990b57036f7ae503bfc0458`, com árvore idêntica à candidata testada.

### Evidências

- (ChatGPT) Failures intermediários permanecem registrados com suas causas reais, incluindo migração, divergência temporária fonte/simulado e métricas documentais; nenhum foi reclassificado retroativamente.
- (ChatGPT) Gate final de push `34872178809`: V08 22/22, regressões V01–V08 405/405, V00 12/12, validador 0 falhas/0 avisos, `V08_RUNTIME_EDIT=0` e escopo verde.
- (ChatGPT) Todos os nove checks finais da PR #42 concluíram com `success` no mesmo head final.
- (ChatGPT) Pós-merge `622d2c962a80998cf990b57036f7ae503bfc0458`: dez workflows na `main` — CI geral e V00–V08 — concluíram com `success`.

### Limites

- (ChatGPT) Sem publicação Databricks, alteração de ACL/compute, execução remota Spark/SQL/MLflow, promoção visual, homologação de browser/acessibilidade/UAT ou prova de seleção determinística de skill pela Genie Code. A V09 não foi iniciada.

## 2026-09-14 — V07: candidata de consumidores e formatos de saída (ChatGPT)

### Adicionado

- (ChatGPT) Rotas opt-in `_resolvido` para matriz de correlação, grade de distribuições, curvas ROC/Precision–Recall/Lift/KS, timeline do `PerformanceMonitor`, UMAP e visualizações de safras.
- (ChatGPT) `get_tokens_plotly(theme)` centraliza o acesso a tokens já revalidados pelo núcleo V02/V03, sem leitura direta de JSON, fixture ou estado global.
- (ChatGPT) Registro estruturado classifica nove consumidores runtime e delimita formatos de saída efetivamente exercitados.

### Atualizado

- (ChatGPT) APIs legadas permanecem o default; cálculo, agregação, amostragem, embedding, métricas e políticas analíticas não são alterados pela seleção de tema.
- (ChatGPT) `dataframe_styled` permanece sob a integração V04; Kaplan–Meier e SHAP/Matplotlib ficam como exceções explícitas, sem suporte temático implícito.
- (ChatGPT) Fonte e `Novo_Ambiente_Simulado` mantêm equivalência byte a byte nos consumidores e READMEs alterados.

### Evidências

- (ChatGPT) Runs `34858836840`, `34859769442` e `34860697409` permanecem failures documentais. Em todos, a suíte V07 18/18, as regressões V01–V07 382/382 e V00 12/12 passaram antes da validação documental.
- (ChatGPT) O run `34860697409` mediu o estado documental estabilizado em 1345 arquivos de identidade e 1849 links fora da raiz; o README raiz é reconciliado com esses valores sem relaxar o validador.
- (ChatGPT) HTML Plotly local é exercitado; PNG Plotly/Kaleido, PDF, PPTX, browser Databricks e acessibilidade não são homologados nesta sprint.

### Limites

- (ChatGPT) V07 continua candidata: sem aceite, PR de integração, merge, publicação Databricks, alteração de ACL/compute, execução remota Spark/SQL/MLflow, promoção visual, UAT ou início da V08.

## 2026-09-14 — V06: integração Git e fechamento técnico (ChatGPT)

### Atualizado

- (ChatGPT) PR #38 integrada após aceite explícito de Rodrigo; head final validado `70499e1803ce0d61a148a0da975c4f52611046e0`, merge `418946de8d1e95e87cbfd9df528ddcced5075237` e árvore `68ddec3d691047e890ba2785e1e2e007039fa0e3` idêntica entre candidata testada e merge.
- (ChatGPT) V06 registra geração determinística por `ResolvedTheme`, bridge Python → compositor, 12 assets congelados protegidos por SHA-256, manifesto/fingerprints, detecção de adulteração e separação entre gerar, revisar, aprovar, promover e publicar.
- (ChatGPT) CI agregado, V04 e V05 passaram a preparar Node 22, `pnpm@10.34.5` e dependências do compositor antes da descoberta cumulativa V01–V06; nenhum teste foi removido ou filtrado.

### Evidências

- (ChatGPT) Head final da PR #38: CI geral, V00, V01, V02, V04, V05 e V06 concluíram com `success`; suíte V06 5/5, regressões V01–V06 364/364 e V00 12/12.
- (ChatGPT) Pós-merge da PR #38: oito workflows na `main` concluíram com `success` — CI geral e V00–V06, incluindo V03.
- (ChatGPT) Failures históricos da V06 permanecem failures, incluindo `34845378370`, `34845593931`, `34845754341`, `34845937711`, `34846291082`, `34847723861`, `34848445012`, `34848898532` e `34848898536`; suas causas e correções estão preservadas nos documentos V06.
- (ChatGPT) Durante a reconciliação documental pós-merge, os runs transitórios `34852055234`, `34852259063` e `34852831840` foram recusados antes da criação de jobs por YAML inválido; não alteraram produto nem changelog. Já `34853339999` (CI geral) e `34853335827` (V06) executaram os contratos, mas reprovaram na validação documental porque o README registrava `1837` links fora da raiz diante de `1840` medidos pelo validador. Essas execuções permanecem failures históricos.

### Limites

- (ChatGPT) Sem publicação Databricks, promoção automática de variante, ACL/compute/Spark/SQL/MLflow remoto, homologação de navegador/acessibilidade/UAT ou início da V07.

## 2026-09-14 — V05: fechamento técnico do Visual Lab em candidata (Codex)

### Adicionado

- (Codex) `hub_snippets.visual.theme_lab` entra no inventário do Manual com presets, edição atômica, comparação, sessão rastreável, reabertura e limites operacionais.
- (Codex) Entrada de primeiro uso no README do Hub para localizar o laboratório sem confundi-lo com publicação ou aprovação de tema.

### Atualizado

- (Codex) Candidata V05 reconciliada com a `main` pós-D05 `24ffce29`, preservando a documentação R13/D05 e mantendo a PR #26 como evidência histórica.
- (Codex) README do objeto migrado ao contrato `readme-objeto: 1.0.0`; checkpoint, testes e índices registram presets/linhagem/reabertura como contratos Python implementados, não homologação Databricks.
- (Codex) `CLAUDE.md` e Manual distinguem V04 integrada de V05 ainda candidata; a cobertura estrutural passa a incluir o novo 76º objeto fora do escopo histórico R00–R13.

### Notas

- (Codex) Runs reprovados continuam reprovados. `34797774791` falhou por contrato textual; `34798200237`, `34798497708` e `34798674298` mantiveram funções/regressões verdes e reprovaram o fechamento documental/métricas então desatualizadas.
- (Codex) Nas composições recentes foram observados 31/31 testes específicos V05, 14/14 de sessões, 359/359 regressões de temas e 12/12 V00; esses resultados são Python/GitHub Actions, não homologação de navegador/runtime Databricks.
- (Codex) As métricas finais do README foram medidas no run `34831939535`; depois da atualização numérica, o head limpo `efb9dd32` obteve `success` no workflow V05 `34832202757`, incluindo validação documental e escopo.
- (Codex) A PR #37 foi aberta em draft contra a `main` pós-D05; os checks iniciais da PR concluíram com `success` no CI geral `34832408423`, V00 `34832408496`, V01 `34832408407`, V02 `34832408460` e V05 `34832408426`. O registro final continua sem autorizar merge.
- (Codex) Sem aceite V05, merge, publicação Databricks, homologação operacional ou início da V06.

## 2026-09-13 — D05: reconciliação documental do Sistema de Temas (ChatGPT)

- Alinha documentação viva ao estado V00–V04 aceito e integrado no Git.
- Preserva notas históricas de candidatura e registra o fechamento por nova entrada, sem reescrever evidência.
- D05 é manutenção documental e não inicia a sprint funcional V05.
- Sem publicação Databricks, homologação visual/runtime, auditoria independente ou mudança de API.

## 2026-09-14 — pós-R13 D01–D04 (ChatGPT)

- Documentação viva reconciliada com R00–R13 encerrada.
- Sem alteração de implementação nem homologação Databricks.

## 2026-09-13 — R13: integração e encerramento da iniciativa de READMEs (ChatGPT)

- Integra o PR #33 no commit `b0e953cc`, após auditoria R13, mutantes negativos e CIs permanentes aprovados.
- Encerra a iniciativa R00–R13 em 75/75 READMEs operacionais, 3/3 exemplares e 0 pendências estruturais.
- Mantém explícitos os limites: revisão `A0_light`, sem auditoria independente, publicação ou homologação Databricks/Genie Code.

## 2026-09-13 — R13: auditoria final da iniciativa de READMEs (ChatGPT)

- Audita contrato, checklist, skill de criação, validador, Manual, 75 READMEs, três exemplares e seis índices de categoria.
- Adiciona inventário por SHA-256 e mutantes negativos para demonstrar sensibilidade do gate.
- Congela produto na base pós-R12; correções de produto não são feitas silenciosamente pela auditoria.
- Registra revisão `A0_light`: não é auditoria independente nem homologação Databricks/Genie Code.
- Sem publicação no workspace, merge antecipado ou início de outra iniciativa.

## 2026-09-13 — R12: índices de categoria e navegação (ChatGPT)

- Cria índices para as seis categorias funcionais de `hub_snippets`.
- Liga catálogo geral, entrada `.assistant` e Manual aos índices sem alterar objetos.
- Registra que a migração estrutural terminou na R11.
- Mantém `hub_snippets/tests/` como infraestrutura interna.
- Sem publicação, homologação runtime, auditoria independente, merge ou início da R13.

## 2026-09-13 — R11: fechamento da migração de READMEs (ChatGPT)

- Documenta os nove Hub Prompts restantes no contrato 1.0.0.
- Preserva os nove briefings e limita notebooks a backlinks/erratas Markdown declaradas.
- Fecha `pending` e muda o controle para `phase=complete`; meta estrutural 75/75 sujeita ao validador.
- Sem publicação, homologação Databricks/Genie Code, auditoria independente, merge antecipado ou encerramento das etapas posteriores.

## 2026-09-13 — R10: READMEs de Hub Prompts (ChatGPT)

- Documenta seis prompts no contrato 1.0.0: `comparar_tabelas`, `cross_eda`, `data_quality`, `eda_completa`, `feature_engineering` e `stat_check`.
- Preserva os seis briefings `.md`; notebooks recebem somente backlinks e três erratas Markdown sobre tabelas sintéticas já gravadas pelo código.
- Retira exatamente seis dispensas R10 do controle de migração; cobertura alvo 66/75, sujeita ao validador.
- Sem publicação Databricks, resposta Genie Code fabricada, auditoria independente, aceite editorial, merge ou início da R11.

## 2026-09-12 — R08: READMEs de clusters, anomalias e explicabilidade (ChatGPT)

- Documenta seis objetos no contrato 1.0.0: `autoencoder_anomaly`, `cluster_profiling`, `clustering_suite`, `explainability_report`, `shap_explainer` e `umap_viz`.
- Corrige somente prosa/backlinks dos notebooks: outputs históricos e código executável permanecem preservados.
- Registra limites de percentil de anomalia, métricas internas de clustering, ranking/SHAP, dependências ocultas e geometria UMAP.
- Retira exatamente seis dispensas R08 do controle de migração.
- Sem alteração de implementação/fachada, publicação Databricks, homologação de modelo/segmentação/explicabilidade, auditoria independente ou início da R09.

## 2026-09-13 — R08: fechamento de compatibilidade (ChatGPT)

### Corrigido

- (ChatGPT) Fixado scikit-learn 1.4.2 junto a UMAP 0.5.5 e NumPy 1.26.4 exclusivamente no runtime isolado de verificacao; helper e dependencias permanentes preservados.
- (ChatGPT) Coleta conjunta de stdout/stderr, contagem singular/plural e identidade Git automatizada explicita no workflow temporario. Nenhum teste removido, erro ignorado ou skip convertido em sucesso.

### Atualizado

- (ChatGPT) Relatorio, rubrica e matriz R08 registram o run e a compatibilidade; aceite editorial continua pendente. Sem merge, publicacao Databricks ou inicio da R09.

## 2026-09-12 — V04: componentes HTML e tabelas opt-in (Codex)

### Adicionado

- (Codex) `get_styles_resolvidos(theme)` materializa CSS de notebook a partir do `ResolvedTheme` revalidado, sem CSS livre ou estado global.
- (Codex) Variantes `_resolvido` para badges, divisores, KPI card HTML, cabeçalho de seção, índice EDA e tabela pandas.
- (Codex) Suíte V04 com 29 casos e workflow permanente somente leitura.

### Atualizado

- (Codex) Componentes cobertos usam `constants.styles` no caminho V04; APIs legadas, cortes de score, conteúdo, ordem e dados permanecem preservados.
- (Codex) Notebook/READMEs dos objetos, guia operacional, Manual e índices documentam o uso opt-in e os limites de `dark`/`high_contrast`.
- (Codex) Gate `temas` continua descobrindo todas as `test_temas*.py`, agora descrito até V04.

### Notas

- (Codex) Code-check `34726526972` permanece FAILURE: V04/temas/V00 passaram, mas checkout raso e notebook `styles` não exercitando a nova API reprovaram o validador.
- (Codex) Code-check corrigido `34726621227`: 29 V04, 298 temas V01–V04, 12 V00 e `validate_assistant` aprovados.
- (Codex) Reconciliação `34726990399` permanece FAILURE por fachadas V04 ainda não materializadas; nenhum commit combinado foi enviado.
- (Codex) Reconciliação corrigida `34727070003`: preservação V04/R04-B, regressões e 14/14 casos R04-B com Spark real aprovados; commit `c2b91c5e`.
- (Codex) Finalização `34727324137` permanece FAILURE por marcador textual impossível do `ci_local.py`; nenhum derivado/candidato final foi gravado.
- (Codex) Finalização `34727521220` permanece FAILURE porque a regressão V01 exigiu preservar `V01/README.md` e `V01/GUIA_PRIMEIRO_USO.md` no índice agregado; nenhum commit final foi criado.
- (Codex) V04 é candidata: sem aceite, merge, publicação Databricks, homologação visual/acessibilidade ou início da V05.
## 2026-09-12 — R07: READMEs de score, vintage e sobrevivência (ChatGPT)

- Documenta `kaplan_meier`, `score_bands`, `scorecard_builder`, `survival_cox`, `vintage_analysis` e `woe_iv_calculator` no contrato 1.0.0.
- Corrige somente prosa/backlinks dos seis notebooks; código, magics executáveis e outputs históricos permanecem protegidos.
- Explicita limites de censura, hazard, score/odds/PDO, maturidade de safra e WOE/IV, sem transformar heurísticas em normas.
- Retira exatamente seis dispensas R07 do controle de migração e registra achados, matriz, rubrica e testes.
- Sem alteração de implementação/fachada, dependência permanente, publicação Databricks, homologação de política/modelo, auditoria independente ou início da R08.

## 2026-09-12 — R06: READMEs de séries e validação temporal (ChatGPT)

- Documenta `arima_wrapper`, `lgbm_temporal`, `prophet_wrapper`, `split_temporal` e `walk_forward` no contrato 1.0.0.
- Corrige somente prosa/backlinks dos cinco notebooks; código, magics executáveis e outputs históricos permanecem protegidos.
- Corrige no catálogo o papel de `lgbm_temporal`: geração de features pandas, sem treino LightGBM.
- Retira exatamente cinco dispensas R06 do controle de migração e registra achados, matriz, rubrica e testes.
- Sem alteração de implementação/fachada, dependência permanente, publicação Databricks, auditoria independente ou início da R07.

## 2026-09-12 — R05: READMEs de modelos tabulares (ChatGPT)

- Documenta `lgbm_ranker`, `mlp_embeddings`, `optuna_lgbm`, `tabnet_wrapper`, `train_catboost` e `train_lgbm` no contrato 1.0.0.
- Corrige somente prosa/backlinks dos seis notebooks; código, magics executáveis e outputs históricos permanecem protegidos.
- Retira exatamente seis dispensas R05 do controle de migração.
- Registra limitações de API encontradas, relatório, matriz, rubrica e testes de runtime isolados.
- Sem alteração de implementação, dependência permanente, publicação Databricks, auditoria independente ou início da R06.

## 2026-09-12 — R04-B: READMEs dos seis Hub Scripts (ChatGPT)

- Documenta `data_quality_check`, `doc_coverage`, `drift_detector`, `naming_checker`, `rfv_calculator` e `schema_to_yaml` no contrato 1.0.0.
- Atualiza somente prosa/backlinks dos seis exemplos; implementações e fachadas permanecem protegidas.
- Retira exatamente seis dispensas do controle de migração; a cobertura final é calculada pelo validador.
- Registra relatório, matriz, achados, rubrica e testes específicos, incluindo Spark real.
- Sem publicação Databricks, auditoria independente ou início da R05.

## 2026-09-12 — V03: adaptador Plotly opt-in (Codex)

### Aceite e integração

- (Codex) Rodrigo concedeu aceite explícito à V03 com a instrução "pode integrar a V03". A integração Git pelo PR #16 fica autorizada após revalidação da árvore exata; o aceite não autoriza publicação Databricks, homologação operacional, migração automática de outros consumidores nem início da V04.

### Adicionado

- (Codex) `get_tema_plotly`, `aplicar_tema_resolvido` e `registrar_template_plotly_resolvido` sobre a API pública V02, sem alterar as três assinaturas legadas.
- (Codex) Suíte V03, workflow somente leitura e documentação de sprint para equivalência legada, mapeamento de tokens, integridade, efeitos de sessão e falhas adversariais.

### Atualizado

- (Codex) README/notebook de `theme_plotly`, Manual e índices passam a documentar a rota configurada como opt-in; consumidores atuais continuam no caminho legado.
- (Codex) Gate `temas` já descobre a suíte V03 pelo padrão `test_temas*.py`; descrição atualizada sem criar etapa paralela.

### Corrigido

- (Codex) Code review P2: o adaptador Plotly passa a consumir layout e rodapé somente dos tokens extraídos do JSON canônico revalidado; adulterar apenas `_values` de um `ResolvedTheme` não contamina a figura.
- (Codex) Bloco copiável V03 no README importa `plotly.graph_objects as go` localmente, sem depender da execução de células anteriores.
- (Codex) Code review P2 documental: README, notebook e Manual explicitam que a rota V03 revalida o tema e requer `jsonschema`/`referencing` conforme `hub_snippets/requirements-temas.txt`, sem instalação automática.
- (Codex) README do núcleo V02 deixa de afirmar que Plotly ainda não está integrado e passa a registrar a integração opt-in V03 sem sugerir migração automática ou aprovação.
- (Codex) Code review P2 final: `registrar_template_plotly_resolvido` recusa substituir um template que já participa do default ativo quando `ativar=False`, inclusive em defaults compostos; regressões cobrem recusa e ativação explícita.

### Notas

- (Codex) Primeiro run remoto V03 `34721929275`: 22 V03 + 12 V00 + 105 V02 + 138 V01 aprovados. Não somar reexecuções como novos casos.
- (Codex) `mode=dark` e `high_contrast` permanecem válidos no contrato, mas o adaptador Plotly V03 os recusa até existirem tokens de superfície suficientes.
- (Codex) Sem aceite/merge V03, publicação Databricks, migração de consumidores, V04/V05 ou homologação operacional.

## 2026-09-12 — R04-A: seis guias de operações Spark (ChatGPT)

### Adicionado

- (ChatGPT) READMEs de `date_features`, `join_diagnostics`, `null_summary`,
  `psi_calculator`, `safe_display` e `smart_sample`, com relatório, achados,
  rubrica, matriz e testes suplementares da R04-A.

### Atualizado

- (ChatGPT) Seis notebooks recebem backlinks e correções exclusivamente de
  prosa; implementações, fachadas, magics e saídas históricas são preservadas.
- (ChatGPT) Coleção, Manual e índices passam a oferecer rotas para os seis guias;
  controle de migração retira somente as seis dispensas correspondentes.
- (ChatGPT) Cobertura estrutural candidata passa a 26/75 operacionais, três
  exemplares e 49 pendências; isso não representa publicação ou aceite editorial.

### Corrigido

- (ChatGPT) Explicações sobre feriados fixos, cobertura de join, limiares de
  nulos, PSI/CSI, renderer de display e garantia de tamanho da amostra são
  alinhadas ao comportamento observado, sem mudança funcional silenciosa.

### Notas

- (ChatGPT) A R04-A foi produzida e validada inicialmente sobre `1be947b`; antes do PR final,
  foi reconciliada com a main `6085eab`, que já contém a V02 aceita. A composição final
  preserva a V02 e repete os gates; auditoria independente e homologação Databricks permanecem separadas.
- (ChatGPT) Pausa obrigatória antes da R04-B; nenhuma publicação ou merge é
  presumido por esta entrada.

## 2026-09-12 — V02: aceite e integração Git concluídos (Codex)

### Atualizado

- (Codex) Aceite explícito de Rodrigo registrado e PR #14 integrado na main no commit d4cabdca4ac68c0a2edbd7f9f621f68962c8f6b8; checkpoint, índices, contexto canônico e Manual passam a refletir o estado efetivo.
- (Codex) Manual fonte atualizado e cópias derivadas regeneradas pelo renderer, sem edição manual do espelho.

### Notas

- (Codex) A árvore do merge é idêntica à candidata final validada; CI geral, V00, V01 e V02 passaram novamente após o merge na main.
- (Codex) Sem publicação Databricks, mudança visual, homologação de Spark/widgets/Apps/AI-BI ou início da V03. Auditoria independente e teste com iniciante permanecem pendentes.

## 2026-09-12 — V02: alinhamento documental da candidata remota (Codex)

### Corrigido

- (Codex) Índices e checkpoint passaram a apresentar a V02 como etapa corrente no
  PR #14, preservando o guia de primeiro uso da V01 como referência histórica e
  mantendo separadas validação funcional, aceite, integração e publicação.
- (Codex) Saída reproduzível do README raiz sincronizada após os novos links
  documentais; o validador continua fail-closed e nenhuma guarda foi relaxada.

### Notas

- (Codex) Correção exclusivamente documental sobre o núcleo funcional já testado;
  sem mudança em API, schema, fixtures, assets, aparência ou consumidores legados.
- (Codex) Sem merge da V02, publicação Databricks, homologação de Spark/widgets/
  Apps/AI-BI ou início da V03. Auditoria independente e teste com iniciante seguem
  pendentes.

## 2026-09-12 — V02: conciliação com R03-A/R03-B integrada (Codex)

### Atualizado

- (Codex) Candidata V02 reconciliada com main `1be947b`, preservando os READMEs
  R03-A/R03-B e o contrato editorial 1.0.0. O novo objeto usa a versão vigente.
- (Codex) Conflitos do CHANGELOG e do README raiz resolvidos de forma aditiva;
  contagens recalculadas por execução. Manual raiz sincronizado e espelho gerado.

### Notas

- (Codex) Testes anteriores continuam vinculados à base `836f236`; a composição
  tem repetição própria de V01/V02, V00, publicador, nove gates e suplementos R03.
- (Codex) Candidata local em bundle/patch. A branch remota da preparação contém
  somente baseline; não confundir execução dos testes locais com push integral.
- (Codex) Sem merge, publicação Databricks, mudança funcional legada ou V03.

## 2026-09-12 — V02: núcleo de temas e contrato promovido (Codex)

### Adicionado

- (Codex) Objeto `visual.tema`: resolução explícita, cópias imutáveis, integridade,
  leitura local limitada, exportação em memória e erros seguros; nenhuma aplicação visual.
- (Codex) README de quinze seções, exemplo sintético, guia de primeiro uso/erros,
  registro do núcleo no Manual, testes positivos/adversariais e gate V02.

### Atualizado

- (Codex) Schema V01 movido sem alterar bytes para o padrão de identidade visual;
  verificador V01 reutiliza as funções do núcleo. Referências geradas e fixtures
  derivadas têm guardas contra divergência; políticas e relatos históricos preservados.
- (Codex) Entradas de navegação, dependências explícitas de validação e Manual raiz;
  espelho gerado pelo renderer, sem edição manual ou migração dos gráficos legados.

### Notas

- (Codex) Implementação candidata em branch; resultados pertencem ao commit/run
  identificado na PR e no pacote, não a rodadas antigas. Sem merge ou publicação.
- (Codex) Sem dados corporativos, alteração de modelos, permissões de escrita de
  workflows, painel, V03 ou homologação operacional presumida. Auditoria independente
  e teste com iniciante permanecem pendentes.

## 2026-09-12 — R03-I: reconciliação READMEs com V01 integrada (ChatGPT)

### Atualizado

- (ChatGPT) R03-A/R03-B reconciliadas com a `main` que já contém V01 e seu alinhamento documental; três conflitos textuais resolvidos sem descartar qualquer iniciativa.
- (ChatGPT) Estado agregado do README raiz recalculado pela execução real; índice de sprints registra simultaneamente a continuidade dos READMEs e o estado aceito/integrado de V00/V01.

### Notas

- (ChatGPT) Integração autorizada explicitamente por Rodrigo; árvore combinada revalidada antes do merge. Evidências anteriores permanecem vinculadas às árvores em que foram produzidas.
- (ChatGPT) Sem publicação Databricks, mudança funcional, V02 ou R04-A nesta reconciliação. Auditoria independente e homologações operacionais permanecem separadas.

## 2026-09-12 — R03-B: seis guias de display e navegação (ChatGPT)

### Adicionado

- (ChatGPT) READMEs de correlation_matrix, dataframe_styled, distribution_grid,
  index_generator, section_header e theme_plotly; relatório, matriz, achados,
  rubrica e testes suplementares em `docs/sprints/readmes_objetos/`.

### Atualizado

- (ChatGPT) Seis notebooks receberam backlinks e correções de prosa, sem mudar
  código executável ou saídas históricas. Coleção, Manual e índices oferecem rotas.
- (ChatGPT) Controle de migração remove exatamente seis dispensas: 19/74
  operacionais, três exemplares e 55 pendências; cobertura não é aceite editorial.
- (ChatGPT) Manual sincronizado, simulado pelo renderer e contagens da raiz
  reconciliadas com a execução. Contrato 1.0.0 e textos anteriores preservados.

### Corrigido

- (ChatGPT) Explicações sobre limiar/escala de correlação, custo e descarte de
  nulos, amostragem, índice declarado, CSS local e precedência do tema.
  Limites funcionais são documentados, não alterados silenciosamente.

### Notas

- (ChatGPT) Autorrevisão A0_light; evidências locais e remotas identificadas
  separadamente no relatório e no PR. Sem auditor independente ou homologação.
- (ChatGPT) Execução autorizada por “Siga”; branch R03-B depende da R03-A ainda
  em revisão. Nenhum merge, publicação Databricks ou avanço à R04-A.

## 2026-09-12 — R03-A: preservação da V00 integrada em paralelo (ChatGPT)

### Atualizado

- (ChatGPT) Reconciliação da branch R03-A com main `b88a9cc`, que integrou a instrumentação V00 durante a elaboração dos READMEs. Preservadas as entradas das duas iniciativas, o conteúdo da V00 e seus workflows; contagens recalculadas por execução.
- (ChatGPT) Registro complementar, matriz e verificador datado de preservação identificam a segunda base. Os sete textos, o contrato estável e o código dos oito gates não foram modificados nesta reconciliação.
- (ChatGPT) Aprovação do PR nº 7 não foi usada para integrar o novo PR nº 9. Sem mudança na main, publicação ou início da R03-B.

## 2026-09-12 — Aceite, versão 1.0.0 e lote R03-A (ChatGPT)

### Adicionado

- (ChatGPT) Sete READMEs: colors, emojis, styles, fixtures, badge, divider e
  kpi_card; relatório, matriz, achados, rubrica e testes suplementares da R03-A.
- (ChatGPT) Registro do aceite de Rodrigo e merge autorizado do PR nº 7
  (`5493f7d`); ratificação datada do ADR-0012, sem apagar o relato original.

### Atualizado

- (ChatGPT) Contrato 1.0.0 estabilizado sem mudar as quinze seções; nove READMEs
  anteriores mudam somente marcador de versão; checklist e regra editorial coerentes.
- (ChatGPT) Sete notebooks: backlinks e prosa corrigida, preservando execução e
  transcrições históricas. Coleção, Manual e índices oferecem rotas para os guias.
- (ChatGPT) Controle remove somente sete dispensas; cobertura estrutural 13/74,
  três exemplares e 61 pendências; os novos textos ainda aguardam aceite próprio.
- (ChatGPT) Cópia do Manual sincronizada, simulado pelo renderer e contagens da
  raiz reconciliadas com execução; nenhuma recertificação de publicação antiga.

### Notas

- (ChatGPT) Helpers, cores/CSS, APIs, blocos coláveis, Concierge e gates existentes
  preservados. Limitações funcionais/visuais caracterizadas, não corrigidas por efeito colateral.
- (ChatGPT) Autorrevisão A0_light; execução portátil e execução Spark registradas
  separadamente, sem presumir auditoria independente ou homologação Databricks.
- (ChatGPT) Branch R03-A separada da main aprovada. Parada antes da R03-B;
  nenhum novo merge automático ou publicação no workspace.

## 2026-09-12 — V01: alinhamento das entradas após integração (Codex)

### Corrigido

- (Codex) `docs/sprints/README.md`: V01 identificada como aceita e integrada no Git,
  sem instalação do seletor ou homologação operacional presumida.
- (Codex) `CLAUDE.md`: síntese do ADR-0013 aceito em Decisões ativas, com rota
  para o checkpoint vigente e distinção entre fixtures e temas operacionais.

### Notas

- (Codex) Correção dos dois apontamentos documentais da revisão do PR #10,
  autorizada por Rodrigo; corpo decisório e relatos históricos preservados.
- (Codex) Escopo restrito a estas duas entradas e ao changelog. Evidências e
  resultados pertencem à rodada e à PR corretiva, não a execuções antigas.
- (Codex) Sem mudança de produto, espelho, Manual, código, testes ou workflows
  permanentes; sem publicação Databricks e sem início da V02.

## 2026-09-12 — V01: aceite explícito e revalidação para integração (Codex)

### Atualizado

- (Codex) Aceite explícito de Rodrigo registrado no checkpoint V01, nas entradas da iniciativa e na ratificação do ADR-0013, preservando corpo decisório e relatórios históricos.
- (Codex) Integração Git pelo PR #10 condicionada aos checks da árvore exata; não altera produto, espelho, Manual, schema, fixtures, testes ou workflows permanentes.

### Notas

- (Codex) A rodada 34708693721 passou V01/V00/publicador, mas o CI reprovou a contagem de links do README raiz (765 documentados, 768 medidos). Contador reconciliado com a saída real e bateria repetida; o run anterior permanece reprovado, sem relaxar a guarda.
- (Codex) Revalidação identificada por base, candidata, árvore e run próprio. O artefato e o PR registram resultados reais; SKIPs não são PASS e rodadas anteriores não são reclassificadas.
- (Codex) Sem publicação Databricks, mudança visual, V02, force-push ou alteração de proteções. Auditoria independente, avaliação com iniciante e homologações operacionais permanecem pendentes.
- (Codex) Preparação transitória isolada em branch auxiliar, ausente da árvore candidata; só os documentos de aceite entram no commit submetido aos workflows permanentes.

## 2026-09-12 — V01: contrato e experiência sobre a V00 integrada (Codex)

### Adicionado

- (Codex) ADR-0013 proposto e contrato candidato em `docs/sprints/sistema_temas/V01/`, com schema, fixtures, política, guia de primeiro uso e manutenção, rastreabilidade e checkpoint.
- (Codex) Verificador `tools/temas_v01_contract.py`, regressões V01 e workflow separado com leitura apenas, sem modificar as oito etapas do CI ou o workflow V00.
- (Codex) Conferência de âncoras pelo parser Markdown existente, vínculo do registro de assets aos manifestos oficiais e evidências próprias da composição.

### Atualizado

- (Codex) Candidata local anterior reconciliada com `b88a9cc`, sem transportar a V00 alternativa. Índices e ferramentas apontam a rota única vigente; referência de tokens gerada pelo schema.
- (Codex) Contagens locais do README recalculadas pelo validador. Produto, espelho, Manual, decisões anteriores e históricos V00 preservados.

### Notas

- (Codex) A primeira cópia rasa foi recusada pelo gate de READMEs; recuperação refeita com histórico completo sem relaxar guardas. Preparação/transporte transitórios não compõem a árvore final.
- (Codex) Implementação candidata, não aceite do ADR nem homologação. Sem merge automático, publicação Databricks, mudança visual ou V02. Auditoria independente e leitura por iniciante continuam pendentes.

## 2026-09-12 — V00: reconciliação e aceite de integração Git (Codex)

### Atualizado

- (Codex) Reconciliação da candidata V00 com a main que incorpora READMEs e Concierge, preservando histórico, produto, espelho, Manual e as oito etapas do gate.
- (Codex) Autorização explícita de Rodrigo para aprovar e integrar registrada em `docs/sprints/sistema_temas/INTEGRACAO_V00.md`; limites e pendências não convertidos em homologação.
- (Codex) Contagens locais do README recalculadas pelo validador existente. Automação transitória de conciliação removida da árvore final, sem mudança das permissões do workflow permanente.

### Notas

- (Codex) Evidências anteriores permanecem vinculadas aos commits executados. A nova rodada identifica sua própria base e comandos. Sem publicação Databricks, alteração visual, force-push ou desativação de gates.
- (Codex) Preparação transitória corrigida após bloqueios por sintaxe YAML e localização incorreta da suíte visual; usa o comando já declarado no executor V00. Os runs reprovados permanecem no histórico, sem aprovação retroativa.

## 2026-09-12 — R02-I: composição candidata READMEs + Concierge (ChatGPT)

### Adicionado

- (ChatGPT) Candidata isolada, registro, checkpoint e matriz nominal em
  `docs/sprints/readmes_objetos/`, sem merge, R03 ou aceite editorial presumido.
- (ChatGPT) `tools/tests/test_readme_integracao.py`: regressões positivas e
  negativas para perda de etapas, colisão de ADR e navegação complementar.

### Atualizado

- (ChatGPT) `tools/ci_local.py` compõe as oito etapas; documentação de ferramentas,
  índices e instruções/Manual combinados preservam as duas iniciativas.
- (ChatGPT) Proposta dos READMEs renumerada de ADR-0011 para ADR-0012 com nota
  administrativa; ADR-0011 do Concierge e registros históricos preservados.
- (ChatGPT) Manual da raiz sincronizado e simulado pelo renderer; contagens
  do README raiz conferidas por execução da candidata, sem verify remoto.

### Corrigido

- (ChatGPT) Quatro conflitos da composição (CHANGELOG, CLAUDE, README raiz e
  gate) resolvidos sem descartar o Concierge nem a guarda dos READMEs.

### Notas

- (ChatGPT) A candidata parte de main `8744157` e incorpora o conteúdo R01/R02
  de `5996574`, com bases e hashes no registro. PRs originais não reescritos.
- (ChatGPT) Contrato `0.1.0-candidata`, seis pilotos, três exemplares e 68
  pendências mantidos. CI não substitui revisão independente ou aceite humano.
- (ChatGPT) Sem publicação Databricks, execução de dados ou novos testes
  conversacionais. Eventual transporte transitório não compõe a árvore final.

## 2026-09-12 — R02: fechamento editorial e diagnóstico de integração (ChatGPT)

### Adicionado

- (ChatGPT) Revisão, rubrica nominal, diagnóstico de integração e evidências em
  `docs/sprints/readmes_objetos/`; caracteriza a guarda binária e classes XGBoost.

### Atualizado

- (ChatGPT) Seis READMEs do piloto: termos, interpretação e procedência dos testes;
  checkpoint e índice da iniciativa; matriz nominal no relatório de fechamento.
- (ChatGPT) Markdown dos exemplos `pit_join`, `quick_profile` e `format_br`, sem
  alterar código, magics executáveis ou saídas; simulado pelo renderer.
- (ChatGPT) Contagens do README raiz reconciliadas após execução, sem recertificar
  o bloco histórico de publicação remota ou alterar os gates.

### Corrigido

- (ChatGPT) Descrição da checagem binária do XGBoost: exige ao menos duas classes,
  não garante exatamente 0/1. Restrição e falha posterior documentadas, sem mudar API.
- (ChatGPT) Distinção entre alvo futuro legítimo e atributo que vaza o desfecho;
  título sobre cardinalidade; promessa de compatibilidade irrestrita do exemplo.
- (ChatGPT) Textos que ainda apresentavam testes Spark/MLflow anteriores como
  futuros: evidência identificada e separada da reexecução local desta rodada.

### Notas

- (ChatGPT) Quatro conflitos textuais com a main e numeração ADR-0011 duplicada
  diagnosticados, não resolvidos por merge. Não substituir os gates do Concierge.
- (ChatGPT) Contrato `0.1.0-candidata`, cobertura 6/74 e 68 pendências preservados;
  revisão própria, sem aceite humano presumido, auditoria independente ou R03.
- (ChatGPT) Workflow transitório de recuperação de bases removido da árvore final;
  credenciais de checkout não persistidas, sem publicação Databricks.

## 2026-09-12 — R02: seis READMEs piloto e revisão documental (ChatGPT)

### Adicionado

- (ChatGPT) READMEs de `train_xgboost`, `isolation_forest`, `pit_join`,
  `format_br`, `quick_profile` e `eda_rapida`, seguindo `0.1.0-candidata`.
- (ChatGPT) Relatório, matriz nominal, achados, checkpoint e checks sintéticos
  em `docs/sprints/readmes_objetos/`, com evidências de alcance delimitado.

### Atualizado

- (ChatGPT) Navegação das três coleções, fichas do Manual e cópia da raiz,
  índices operacionais e de sprints; somente seis dispensas removidas do controle.
- (ChatGPT) Prosa e links dos seis notebooks, sem alterar código, magics
  executáveis ou blocos históricos; backlink no prompt fora do bloco colável.
- (ChatGPT) Simulado regenerado pelo renderer; contagens do README raiz
  reconciliadas com execução real. Relação de caminhos na matriz R02.

### Corrigido

- (ChatGPT) Afirmações documentais excessivas sobre equivalência entre modelos,
  contaminação exata, MLflow em serverless, cardinalidade e custo de amostragem.
- (ChatGPT) Explicação do fator cem entre escalas percentuais e alerta de perda
  de precisão de inteiros grandes em `fmt_int`/`fmt_n`; nenhum algoritmo alterado.
- (ChatGPT) Distinção entre leitura pedida pelo prompt e overwrite persistente
  de seu notebook; limite de evidência antiga sobre execução de Genie Code.

### Notas

- (ChatGPT) Revisão própria; nenhuma auditoria independente presumida. Template
  segue candidato até aceite do piloto. R03, merge e publicação não executados.
- (ChatGPT) Branch R02 depende da R01 ainda em revisão. Workflows transitórios
  de recuperação/integração têm escopo restrito e não compõem a árvore final.

## 2026-09-12 — R01: READMEs de objeto, fundação candidata (Codex)

### Adicionado

- (Codex) Template e checklist de README de objeto em
  `ambiente_fonte/.assistant/hub_padroes/readme/`; três READMEs de exemplares.
- (Codex) `docs/decisions/ADR-0011-readmes-de-objeto.md` proposto e registros em
  `docs/sprints/readmes_objetos/`, com controle explícito de legados pendentes.
- (Codex) `tools/readme_objeto_contract.py` e regressões adversariais: estrutura,
  navegação, versão, histórico e proibição de aumentar/reintroduzir dispensas.

### Atualizado

- (Codex) Templates de snippet/script/prompt/notebook, skill de criação e seu
  checklist, regras editoriais, instruções, Manual e entradas de navegação.
- (Codex) `tools/validate_assistant.py`, `tools/ci_local.py`, `tools/README.md` e
  checkouts de CI: nova guarda e histórico completo para conferir a migração.
- (Codex) Manual da raiz sincronizado e simulado regenerado a partir da fonte.
  Relação nominal, inclusive documentos não README, na matriz da R01.

### Corrigido

- (Codex) Contagens locais do README raiz reconciliadas com execução; baseline
  tinha duas divergências anteriores à R01. O bloco remoto não foi recertificado.
- (Codex) Notas de escopo nos exemplares: `decidivel`, parâmetro não usado,
  limites da evidência antiga e escrita de tabelas persistentes de demonstração.

### Notas

- (Codex) Nenhum helper analítico, API, imagem ou bloco colável foi modificado.
  R02 não iniciada; template candidato e ADR aguardam aceite humano.
- (Codex) Testes e revisão própria delimitados no relatório R01; sem agentes
  independentes, execução/publicação Databricks ou homologação de produção.

## 2026-09-12 — V00 candidata do Sistema de Temas (Codex)

### Corrigido nesta candidata

- (Codex) Descoberta de consumidores sem cor literal e agregação que distingue casos executados de texto citado, com testes adversariais.
- (Codex) Agregação dos skips, testada contra resumo duplicado; contagens locais do README reconciliadas com execução.
- (Codex) Falha global editorial anterior registrada com causa concreta; famílias validadas com alcance separado.

### Adicionado

- (Codex) Inventário visual somente leitura, runner comparativo e testes adversariais e de contratos legados.
- (Codex) Guia de V00 para leitores não técnicos, achados, matriz de ambientes e checkpoint.

### Limites

- (Codex) Resultados em `docs/testes/sistema_temas/V00/`; execução e aceite são distintos.
- (Codex) Produto, Manual e espelho preservados; sem render, publicação ou teste Databricks.
- (Codex) Revisão semântica independente, teste de leitura e aceite antes de V01 permanecem pendentes.

## 2026-09-12 — Concierge integrado ao produto (Codex)

### Adicionado

- (Codex) `hub-ml-concierge` na fonte canônica, com templates de recomendação,
  handoff e registro de busca, referências, documentação e testes locais.
- (Codex) ADR-0011: descoberta solicitada e progressiva, sem substituir helpers
  declarados nas skills especializadas nem criar outro agente ou catálogo.
- (Codex) Testes de integração em `tools/tests/test_concierge_integracao.py` e
  estágios Concierge incorporados ao gate `tools/ci_local.py`.

### Atualizado

- (Codex) Política de skills, mapa opcional nas instruções, READMEs e Manual;
  cópia do Manual sincronizada e simulado regenerado pelo renderer.
- (Codex) Roteiro/template de forward tests recebe 14P/14N/14M. O 39/39 anterior
  permanece evidência histórica, não homologação da skill nova.
- (Codex) Protótipo experimental preservado como histórico, com ponte para a
  versão mantida em `ambiente_fonte/`.

### Corrigido

- (Codex) Contagens do README reconferidas por execução: duas já estavam
  divergentes na base após a criação do pacote experimental.
- (Codex) Verificador do Concierge recusa raiz simbólica antes de resolver path
  e exige coerência entre categoria e ativação esperada na matriz de aceite.

### Notas

- (Codex) Resultados e limites em `docs/testes/2026-09-12_concierge-integracao.md`.
  Sem publicação no Free/trabalho, consulta de dados ou execução no Genie Code.
- (Codex) Aceite conversacional e revisão independente antes de compartilhamento
  permanecem pendentes. Skips de Spark local não são aprovação no Databricks.

## 2026-09-11 — Kit de transição e aceite gradual no trabalho (Codex)

### Adicionado

- (Codex) Kit offline de dois ZIPs, manifesto v2 com tipos de objeto e notebook
  IPYNB de aceite gerado a partir de núcleo testável, sem publicação remota.
- (Codex) Roteiro de 16 casos humanos para Genie e apresentação; testes de
  integridade, escopo, estado, notebook e contratos Spark sintéticos opcionais.

### Atualizado

- (Codex) Runbook/checklist e skill de replicação: backup Zip - Source, staging,
  promoção seletiva das cinco pastas Hub, instruções por último e reteste final.
- (Codex) MLflow e consultas corporativas desativados por padrão. Pulado não
  equivale a aprovado; arquivos, notebooks, runtime e experiência têm gates próprios.

### Notas

- (Codex) Instruções, Manual, READMEs do produto, imagens, helpers e simulado
  preservados. Nenhuma conexão, publicação ou teste no workspace corporativo.

## 2026-09-11 — Assistant Instructions integradas ao Hub (Codex)

### Atualizado

- (Codex) Instrucoes pessoais passam a fornecer mapa operacional, treze
  rotas de skills e treze modulos frequentes, com consulta seletiva,
  verificacao de contratos e separacao entre contexto e execucao.
- (Codex) Corrigida generalizacao de autologging; restricoes serverless,
  instalacao e efeitos de tracking passam a depender do ambiente/tarefa.
- (Codex) Mantidos limites de autorizacao, privacidade e proveniencia;
  sem leitura integral obrigatoria do manual e sem perguntas redundantes.
- (Codex) Espelho regenerado pelo renderer e contagens do README
  sincronizadas com a execucao do validador.

### Adicionado

- (Codex) Nota tecnica em `docs/handoffs/2026-09-11-assistant-instructions-otimizadas.md`,
  com fontes oficiais, tradeoffs, limites e dezesseis casos de aceite.

### Limites

- (Codex) Sem publicacao Databricks, alteracao de skills/helpers/imagens,
  teste conversacional ou medicao de custo/latencia/tokens da Genie.

## 2026-09-11 — Manual Técnico unificado; apresentação vigente preservada (Codex)

### Adicionado

- (Codex) Manual Técnico didático: APIs locais/Spark/REST, Python e imports,
  sys.path, contratos, dados, skills, modelos, métricas, segurança e publicação.
  Inclui inventário dos 58 helpers, métodos/briefings e índice de termos, com
  referências ao código examinado e à documentação oficial.
- (Codex) Uma redação de autoria no Hub e cópia de leitura idêntica na raiz Git;
  ADR-0010 e testes documentais de sincronização, inventário e exemplos locais.

### Atualizado

- (Codex) Referências ativas dos READMEs, skills, prompts e playbooks passam
  ao Manual Técnico. Layout, imagens, widgets e lógica analítica preservados.
- (Codex) Simulado regenerado exclusivamente por `tools/render_simulado.py`.
  Contagens do README raiz sincronizadas com a validação real.

### Removido

- (Codex) Catálogo de helpers e glossário independentes da raiz do Hub, na
  fonte e no derivado. Conteúdo útil consolidado e contratos reconferidos.

### Limites

- (Codex) Sem publicação Databricks, retirada remota de arquivos, alterações
  de ACL ou homologação conversacional. Os rascunhos descartados não retornam.


## 2026-09-11 — Limpeza de pastas acessórias; simulado eleito (OpenCode)

### Removido

- (OpenCode) `Template_READMEs/`, `READMEs_refeitos/`, `Ajustes_Codex/`,
  `GUIA_PENDENCIAS_E_CONFERENCIAS.md` e
  `PLANO_TRANSFERENCIA_E_TESTES_DATABRICKS_TRABALHO.md`.
- (OpenCode) Ferramentas e workflow que só existiam para revisar os rascunhos
  (`review_readmes.py`, testes e `.github/workflows/readme-examples.yml`).

### Atualizado

- (OpenCode) `CLAUDE.md`, `fonte-de-verdade.md` e `.gitattributes` deixam de
  tratar `Ajustes_Codex/` como camada viva. O estado escolhido permanece o
  `Novo_Ambiente_Simulado/` vigente (espelho de `ambiente_fonte/`).

## 2026-09-11 — Imagens nos rascunhos originais e paridade de disposição (Codex)

### Corrigido

- (Codex) A primeira entrega ficou apenas na branch de revisão, deixando os
  rascunhos da `main` com caminhos quebrados. As versões corrigidas passam a
  ocupar os próprios arquivos em `Template_READMEs/sprints_preenchidos/`.
- (Codex) Diagrama de contexto reinserido na seção correspondente do candidato
  da raiz; panorama de retornos dos scripts movido do catálogo para o passo
  a passo operacional, como nos READMEs atuais. PNGs aprovados preservados.

### Adicionado

- (Codex) Índice renderizado da pasta de candidatos e guarda que compara
  presença, sequência e seção das imagens com os READMEs de referência;
  quatro regressões para impedir novo falso positivo de validação visual.

### Limites

- (Codex) Sem promoção da redação candidata, edição de algoritmos, render do
  simulado ou publicação no Databricks. O README oficial da raiz recebe
  somente sincronização mecânica das contagens do gate.

## 2026-09-11 — Correção dos READMEs candidatos após auditoria (ChatGPT)

### Corrigido

- (ChatGPT) Dez rascunhos em `Template_READMEs/sprints_preenchidos/`, sem promoção
  da redação oficial: contratos DQ e taxa de resposta, freshness separado,
  schema sintético consistente, execução do agente, dependências e procedência.
- (ChatGPT) Fichas dos 51 snippets, sete scripts, treze skills e dezesseis prompts,
  com interfaces conferidas, preparação, exemplos, limites e referências específicas.
- (ChatGPT) Links de staging e destinos virtuais, âncoras explícitas e inserção
  dos 21 diagramas e dois banners existentes, sem alterar os PNGs aprovados.
- (ChatGPT) Validação ignora exemplos Markdown dentro de código, mas continua
  reprovando links reais quebrados. Quatro referências históricas locais foram
  identificadas como não versionadas, sem fabricar arquivos de Sprint 0.
- (ChatGPT) Somente os contadores de evidência do README raiz são atualizados;
  a redação candidata não foi promovida e o produto/simulado não foram alterados.

### Adicionado

- (ChatGPT) Mapping, exportação isolada de revisão, validação de PNG/hash,
  links/âncoras e chamadas por AST; testes de regressão e exemplos documentados.
- (ChatGPT) Workflow separado de PySpark local para dados sintéticos. Sem deploy,
  credenciais Databricks, alteração de ACL ou homologação conversacional presumida.
- (ChatGPT) Registro de escopo e evidências em
  `Template_READMEs/sprints_preenchidos/REVISAO.md`. Treinadores opcionais não
  são instalados nem homologados pelo gate básico.

## 2026-09-11 — Rascunhos dos READMEs a partir dos templates (OpenCode)

### Adicionado

- (OpenCode) `Template_READMEs/sprints_preenchidos/`: plano em dez sprints
  (um README cada) e rascunhos sem placeholders, com fio de campanha sintética.
  Destino canônico intocado; sem publicação Databricks.

## 2026-09-11 — Templates editoriais para aprofundar os READMEs (Codex)

### Adicionado

- (Codex) `Template_READMEs/`: guia comum de tom/didática e dez templates
  específicos, cobrindo os seis READMEs das cinco frentes e quatro guias
  auxiliares do produto, com títulos/subtítulos de referência preservados.
- (Codex) Orientações por seção, propostas aditivas de subdivisão, fichas de
  catálogo, exemplos acompanhados, interpretação de resultados e critérios
  editoriais; sem reescrever os READMEs atuais ou gerar novas figuras.

### Notas

- (Codex) Somente orientação local: sem publicação, criação de notebooks,
  alteração do produto, commit ou push. Mudanças anteriores preservadas.
- (Codex) Conferidos os hashes dos dez READMEs de origem, sem alterações;
  todos os títulos/subtítulos de referência preservados nos templates.
  Validador estrutural aprovado com zero falhas e zero avisos.

## 2026-09-11 — Conferência remota da camada visual e do produto (OpenCode)

### Atualizado

- (OpenCode) Recolhida a saída real do validador: `repo (links)` no README raiz
  passou de 456 para 469, alinhado à inclusão documental desta worktree.

### Validação

- (OpenCode) Publicação visual: `--verify` com 103/103 RAW e `status: verified`.
- (OpenCode) Produto Free: `--verify --conteudo` com 414/414, 0 ausentes/obsoletos,
  13/13 skills, 5/5 `hub_`.
- (OpenCode) QA visual local 8154/0; 29 testes do publicador visual; biblioteca e
  guardas do `ci_local` ok. Aceite de tela, commit e trabalho continuam humanos.

## 2026-09-11 — Guias de retomada, transferência e homologação (Codex)

### Adicionado

- (Codex) `GUIA_PENDENCIAS_E_CONFERENCIAS.md` na raiz: estado observado,
  retomada da publicação, conferências, versionamento e backlog documental.
- (Codex) `PLANO_TRANSFERENCIA_E_TESTES_DATABRICKS_TRABALHO.md` na raiz:
  transporte autorizado por e-mail/ZIP e UI, staging, backup, rollback e
  sprints para 12 notebooks principais e 14 opcionais, ainda não criados.
- (Codex) Plano de cobertura de scripts/snippets/moldes, 39 casos de roteamento
  e 48 casos conversacionais de prompts, com fixtures, oráculos, estados,
  evidências e gates de escrita; fundamentação em documentação oficial.

### Notas

- (Codex) Por mudança de escopo solicitada pelo usuário, a publicação em curso
  foi interrompida após log de 103/103 envios e conferências RAW individuais,
  durante a conferência final. O recibo permaneceu `started`; outra execução
  de verificação deve certificar o estado remoto, inclusive assets legados.
- (Codex) Nesta entrega, nenhuma criação de notebook, envio de e-mail, nova
  publicação, commit ou push. READMEs e código do produto preservados.
- (Codex) Validador estrutural aprovado, sem falhas/avisos. A atualização da
  contagem de links no bloco de saída do README raiz ficou como pendência
  editorial para `--conferir-readme`, pois foram acrescentados documentos.

## 2026-09-11 — Integração da evolução visual v2 (Codex)

### Adicionado

- (Codex) Cabeçalhos CRM/Squad incorporados à arquitetura canônica em
  `hub_readmes_visual_assets/headers/`, com original, texto editável, PNGs,
  proveniência, licenças e guia de uso compartilhado por README e notebook.
- (Codex) Compositor de produção para 21 diagramas, manifesto completo,
  transcrição das figuras, contratos semânticos e QA de imagens e consumidores.
- (Codex) Publicador visual de escopo fechado, com backup, detecção de conflito,
  comparação de bytes brutos, aposentadoria individual protegida e testes locais.

### Atualizado

- (Codex) Cinco sprints documentais integradas em seis READMEs físicos,
  preservando títulos, subtítulos, catálogos e exemplos de uso. Diagramas
  compartilhados têm 23 ocorrências; o único cabeçalho CRM atende os seis documentos.
- (Codex) Fontes e módulos de autoria organizados no pacote definitivo, sem
  dependência das pastas temporárias de avaliação para regeneração normal.

### Corrigido

- (Codex) Distinção entre contexto e runtime, procedência nativa e conteúdo Hub,
  política e diagnóstico, contratos heterogêneos dos scripts e seleção explícita.
- (Codex) Exemplo abreviado de retorno de `data_quality_check` alinhado ao código:
  `checks`, `score` e `thresholds` substituem o campo incorreto `metrics`.
  A exceção editorial é rastreada por hashes, sem alterar a implementação.
- (Codex) Rótulos cortados, setas invertidas/ocultas, margens, contraste, texto
  equivalente, alts canônicos e âncoras de integração, após revisão cruzada.

### Removido

- (Codex) Do pacote ativo, 12 arquivos SVG/PNG substituídos e sem referências.
  Permanecem recuperáveis no Git e no baseline congelado da Sprint 0.

### Notas

- (Codex) QA visual global: 8.154 verificações, zero falhas; dois renders
  independentes preservaram os 44 SVG/PNG ativos byte a byte. Os cinco PNGs
  assinatura e os dois cabeçalhos aprovados mantêm os hashes originais.
- (Codex) Biblioteca: 45 testes aprovados; ferramentas existentes: 35 testes
  aprovados. Dependências de desenvolvimento isoladas em `.venv/`, sem mudar runtime.
- (Codex) Publicação e conferência remota serão registradas após sua execução.

## 2026-09-10 — Propostas de cabeçalhos CRM e Squad (Codex)

### Adicionado

- (Codex) Dois PNGs de cabeçalho, CRM e Squad Modelos Analíticos e Preditivos,
  em `sprint_0/cabecalhos/`, compartilhando uma arte-base tecnológica. O mesmo
  PNG de CRM serve a README e notebook, sem duplicação de versões por destino.
- (Codex) Compositor isolado `tools/readme_visuals/headers.mjs`, texto exato
  declarativo, original raster preservado, origem da geração, manifesto,
  camadas tipográficas SVG e verificações de legibilidade em tamanho reduzido.

### Atualizado

- (Codex) Registrada a aprovação do usuário para as cinco assinaturas da Sprint 0.
  Os cabeçalhos são propostas adicionais locais, aguardando novo OK; nenhum
  README ativo, diagrama aprovado ou notebook existente foi substituído.

### Notas

- (Codex) Sem publicação no Databricks, commit ou push nesta rodada. A arte-base
  foi gerada pela ferramenta nativa de imagem; o texto é aplicado pelo compositor
  determinístico. As sprints seguintes continuam aguardando aprovação.
- (Codex) Validação dos cabeçalhos com 22 verificações, inspeção independente
  sem ajustes requeridos e duas exportações com hashes idênticos. O validador
  canônico do projeto passou sem falhas nem avisos.

## 2026-09-10 — Sprint 0 da evolução visual (Codex)

### Adicionado

1. (Codex) Contratos semânticos de 21 figuras, microcopy declarativa e sistema
   visual candidato v2 em `hub_readmes_visual_assets/`; cinco protótipos assinatura
   em SVG/PNG, com versões de leitura e apresentação, na galeria isolada `sprint_0/`.
2. (Codex) Renderer determinístico em `tools/readme_visuals/`, com fonte e ícones
   licenciados, dependências fixadas, baseline dos 22 ativos anteriores, comparação,
   transcrição acessível, QA geométrico e publicação/verificação isolada por CLI.

### Corrigido

1. (Codex) Falsos positivos de higiene em hashes SHA-256 e dependências locais:
   delimitado o token de identificação e excluído `node_modules` apenas da
   varredura de extras, mantendo inspeção de arquivos rastreados e testes de regressão.

### Notas

- (Codex) Preservados os seis READMEs físicos e os 22 ativos anteriores. As
  próximas sprints documentais dependem da avaliação visual do usuário. Tokens v2
  e protótipos são candidatos, não promoção automática do conjunto ativo.
- (Codex) O espelho `Novo_Ambiente_Simulado/` foi gerado pela ferramenta canônica;
  nenhum arquivo derivado foi editado manualmente.
- (Codex) Galeria enviada e conferida por CLI em pasta isolada; PNGs inspecionados
  no Databricks em leitura normal, com painel lateral e em split view. Corrigidos
  os links relativos do notebook visualizador, preservando os Markdown locais.

## 2026-09-10 — Variantes visuais dos READMEs para avaliação (Codex)

### Adicionado

- (Codex) Versionados em `READMEs_refeitos/` os rascunhos documentais
  conservadores e, na subpasta `readmes_viasual_melhorado/`, suas variantes para
  avaliação visual isolada no Databricks, sem substituir os READMEs ativos.
- (Codex) Criada a extensão editorial `hub_readmes_visual_assets/`, nomeada para
  deixar explícito que reúne apenas recursos visuais dos READMEs; ela contém 22
  fontes SVG editáveis, 22 PNGs publicados, manifesto com hashes e guia visual.
- (Codex) Adicionado `tools/render_readme_visuals.mjs` para reproduzir todo o
  conjunto em `1600 × 900` a partir de uma única definição versionada.
- (Codex) Registrado em `docs/sprints/2026-09-10-readmes-visuais.md` o plano das
  cinco sprints, incluindo o requisito de conciliar densidade informativa com
  acabamento bonito e estiloso para leitura e apresentação.

### Atualizado

- (Codex) As variantes visuais ganharam mapas de leitura, âncoras explícitas,
  tabelas mais estreitas, diagramas simplificados, inventário integral de
  snippets, matriz de seleção de prompts e legenda operacional de scripts.
- (Codex) Referências externas à cópia isolada passaram a ser exibidas como
  caminhos, preservando apenas links que podem ser navegados dentro do conjunto
  publicado para revisão.
- (Codex) Acrescentado o ensaio isolado
  `readmes_viasual_melhorado/readmes_visual_testes/` com três representações do
  README de snippets: Markdown com PNGs, notebook com Mermaid bruto e notebook
  com PNGs; fontes `.mmd`, texto equivalente e roteiro de comparação foram
  mantidos junto aos artefatos.
- (Codex) Promovidos os cinco READMEs principais — com os dois documentos de
  topo tratados como uma sprint editorial — e substituídos os blocos Mermaid
  por PNGs compatíveis com o workspace; cada figura recebeu texto alternativo,
  legenda interpretativa e equivalente semântico no corpo do documento.
- (Codex) Corrigidos os links que nos rascunhos apontavam para nomes isolados e
  recalculados os caminhos relativos para os destinos definitivos no Git e em
  `.assistant/`.
- (Codex) O inventário esperado de extensões `hub_` passou a incluir
  `hub_readmes_visual_assets`, permitindo que publicação e verificação remota
  tratem a nova pasta como parte explícita do pacote.
- (Codex) Restaurado no README raiz o bloco de estado verificável do gate local,
  preservando a conferência automática das contagens após a reformulação
  editorial.

## 2026-09-09 — Reformulação didática e promoção dos READMEs do ecossistema (Gemini)

- (Gemini) Reformulados os 5 READMEs principais do projeto com foco didático, humano e sem dicotomia de ambientes (Free x trabalho):
  - `README.md` (raiz do repositório) e `ambiente_fonte/.assistant/README.md` (guia do ecossistema): introdução didática, componentes modulares, arquitetura completa em Mermaid, fluxo de contexto para o Genie Code e FAQ abrangente.
  - `ambiente_fonte/.assistant/hub_snippets/README.md`: catálogo detalhado por categorias funcionais (`ml`, `spark`, `display`, `visual`, `constants`, `testing`), padrão Pasta de Objeto (ADR-0007), passo a passo operacional e FAQ.
  - `ambiente_fonte/.assistant/hub_scripts/README.md`: catálogo de diagnósticos de integridade e qualidade de dados (`data_quality_check`, `quick_profile`, `rfv_calculator`, `drift_detector`, `schema_to_yaml`, `naming_checker`, `doc_coverage`), fluxo sequencial e FAQ.
  - `ambiente_fonte/.assistant/skills/README.md`: guia metodológico aprofundado das Agent Skills, roteamento do Genie Code via `@`, sinergia com helpers, templates e catálogo funcional.
  - `ambiente_fonte/.assistant/hub_prompts/README.md`: especificação técnica de briefings estruturados para Genie Code, disciplina de metadados (`NÃO INFORMADO` / `NÃO APLICÁVEL`), catálogo por famílias e checklist de QA.
- (Gemini) Revisão editorial sistemática em todos os documentos promovidos: suavização de tom, eliminação de afirmações absolutas ("garante", "100%", "blindagem estrita") e remoção de contadores fixos de componentes.
- (Gemini) Espelho derivado `Novo_Ambiente_Simulado/` atualizado via `tools/render_simulado.py --write`.
- (Gemini) Validação local aprovada integralmente com `tools/validate_assistant.py` (0 falhas, 0 avisos).

## 2026-09-09 — Fechamento das inconsistências residuais (Codex)

- (Codex) `lgbm_temporal` agora recusa chaves de entidade nulas, parâmetros
  booleanos/duplicados e colisões com todas as features geradas, evitando perda
  de entidade e sobrescrita silenciosa.
- (Codex) `PerformanceMonitor` passou a rejeitar booleanos em métricas, limiares,
  contagens e períodos consecutivos; o CSI categórico separa ausência de uma
  categoria textual de mesmo nome.
- (Codex) Ampliados testes locais e smoke Spark para os casos acima; o gate local
  passou com 45 regressões da biblioteca e 33 guardas de ferramentas.
- (Codex) A proveniência de publicação passou a considerar apenas fonte e
  espelho publicáveis; a conferência do README inclui o status final e distingue
  a contagem volátil de extras locais.
- (Codex) Adicionado workflow de CI sem credenciais e atualizada a referência
  oficial do Genie Code para imagens, aprovações, MCP e conectores nativos Beta.
- (Codex) Espelho regenerado exclusivamente por `tools/render_simulado.py` e 13
  caches Python locais removidos do produto.
- (Codex) O primeiro smoke de fechamento revelou incompatibilidade do sentinela
  `format="ISO8601"` com o pandas do runtime Databricks e inferência impossível
  numa fixture Spark totalmente nula; ambos foram corrigidos antes da nova rodada.
- (Codex) O segundo smoke revelou um cenário legado que ignorava entidade com
  datas duplicadas sem optar por `on_duplicate_dates="keep"`; o teste passou a
  declarar essa escolha, preservando a proteção padrão do helper.
- (Codex) Publicado o produto `8187fac` no Free e conferidos 316/316 conteúdos,
  13/13 skills e 4/4 extensões, sem ausência ou obsoleto.
- (Codex) Smoke final `186787319038743` aprovado no Spark 4.2.0 com 146 casos,
  137 PASS, 0 FAIL, 8 opcionais e 1 bloqueio esperado; a skill 13 passou nos
  três forward tests e fechou o inventário em 39/39.

## 2026-09-09 — Correções da revisão e retomada no PC (Codex)

- (Codex) Implementados R01–R06 da revisão: métricas inválidas, colisões de nomes,
  inventário publicável, multiconjunto PIT, limite CSI e migração KS.
- (Codex) Separados inventário versionado/higiene local e conferência local/remota
  do README. Acrescentada evidência JSON opcional à verificação de conteúdo.
- (Codex) Atualizados exemplos e regenerado o espelho pelo renderer. Validação:
  40 testes da biblioteca e 32 de ferramentas aprovados; execução remota pendente.
- (Codex) Registrados plano de retomada e comandos em
  `docs/handoffs/2026-09-09_correcoes-codex.md` e fechamento local da auditoria.

## 2026-09-09 — Revisão da implantação do plano (Codex)

- (Codex) Registrados contexto, auditoria independente e plano corretivo em `docs/auditoria/2026-09-09_implantacao-plano/`.
- (Codex) Reexecutado o gate local sobre `9e9fa78`: 37 testes da biblioteca, 23 guardas e validação estrutural aprovados. Reproduzidos descarte de métrica inválida, colisão de coluna temporal e divergência entre filtro e operação de publicação simulada.
- (Codex) Acrescentada referência de continuidade ao handoff; nenhuma alteração funcional nem publicação Databricks nesta rodada.

## 2026-09-09 — Handoff da rodada registrado

### Adicionado

1. (Claude) `docs/handoffs/2026-09-09_plano-consolidado.md`: estado dos pacotes T0 a
   T6, o que continua bloqueado por acesso e as armadilhas de plataforma encontradas
   ao executá-los.

### Atualizado

1. (Claude) `docs/handoffs/README.md`: novo registro no índice, e o parágrafo de
   leitura passa a distinguir os dois handoffs em vez de falar de um só.

## 2026-09-08 — Plano consolidado, após contraditório de três LLMs

Rodada dos pacotes T0, T1, T2 e T5 do plano consolidado, mais o T6 e a parte
documental do T3. T4 (testes conversacionais) e T7 (replicação) seguem abertos.

### Adicionado

1. (Claude) `.gitattributes` com `* text=auto eol=lf` e exceção `-text` para
   `Ajustes_Codex/`, que é material congelado e fica preservado byte a byte.
2. (Claude) `tools/ci_local.py` e `tools/requirements-dev.txt`: gate local que
   roda validador, testes da biblioteca e guardas das ferramentas sem credencial
   do Databricks, e recusa rodar com dependência de teste ausente.
3. (Claude) `t_pit_join_preservacao` em `tools/spark_smoke_test.py`: fixture de
   seis linhas com contagem esperada por categoria, comparada contra
   `fatos.count()` e não contra o total derivado da própria saída.
4. (Claude) `conferir_fonte_espelho`, `comparar_conteudo` e a flag
   `--verify --conteudo` em `tools/publicar_free.py`, com hash bruto e hash
   normalizado registrados separadamente.
5. (Claude) `selecionar_metricas_do_relatorio` e `CHAVES_DO_RELATORIO` em
   `hub_snippets/ml/performance_monitor`: tradução explícita de `auc_roc` para
   `auc`, sem heurística de nome.
6. (Claude) `LIMITE_CATEGORIAS_CSI` e o parâmetro `max_categorias` em
   `hub_snippets/spark/psi_calculator`, com a contagem de categorias distintas
   feita antes da coleta no driver.
7. (Claude) Evidências datadas em `docs/testes/2026-09-08_diagnostico-eol.md` e
   `docs/testes/2026-09-08_pit-join-preservacao.md`.

### Atualizado

1. (Claude) `docs/playbooks/checklist-replicacao.md`: a ressalva de "auditoria de
   uma rodada" sobre `pit_join` e vizinhos deu lugar ao estado real — segunda
   origem em 20/08, smoke em 29/08, teste de preservação em 08/09. O risco que
   permanece é o ambiente corporativo, não a rodada única.
2. (Claude) `docs/playbooks/replicacao-trabalho.md`: passa a distinguir módulo da
   biblioteca (**arquivo**) de material didático `exemplo_*` (**notebook**), em
   vez de generalizar todos os `.py` como arquivo.
3. (Claude) `.claude/context/ambiente-free.md`: a cota de 01/09 vira fato datado e
   o estado passa a "pendente de revalidação".
4. (Claude) `tools/README.md`: declara o alcance de cada modo de verify e por que
   a normalização da comparação é deliberadamente mínima.
5. (Claude) `.gitignore`: `Claude outputs/`, pasta gerada pela ponte de arquivos
   que estava entrando na varredura de identidade do validador.

### Corrigido

1. (Claude) `hub_snippets/ml/lgbm_temporal`: a coluna de data era ordenada como
   veio. Em texto, a ordem era lexicográfica — `2026-1-10` antes de `2026-1-2` —
   e o lag trazia informação futura sem nenhum sinal de erro. A conversão passou
   a ocorrer antes de `sort_values` e independe de `calendar_features`.
2. (Claude) Contrato de data declarado no mesmo módulo: ano-mês-dia é aceito
   automaticamente por não ser ambíguo; qualquer outro formato exige
   `date_format`. Data nula, data inválida no calendário, coluna numérica e
   empate no grão entidade+data passaram a levantar `ValueError`.
3. (Claude) Árvore de trabalho normalizada de CRLF para LF em 648 arquivos, sem
   nenhuma diferença de conteúdo, em commit isolado das mudanças funcionais.
4. (Claude) `hub_snippets/ml/performance_monitor/__init__.py` regenerado por
   `tools/api_publica.py` em 09/09, depois que o validador acusou divergência da
   API pública: a ordem é a de definição no módulo, não alfabética.
5. (Claude) `tools/ci_local.py` lia a saída dos subprocessos como UTF-8 estrito.
   No Windows o filho escreve no code page do console, e o `UnicodeDecodeError`
   morria dentro da thread leitora: a etapa reprovava sem mostrar a causa. Agora
   o filho recebe `PYTHONUTF8` e a decodificação tem fallback de locale.
6. (Claude) `tools/tests/test_tool_guards.py`: o teste de representações
   equivalentes gravava a fixture em modo texto e casava o objeto remoto por
   `endswith`. No Windows a fixture saía em CRLF, o mock a convertia outra vez e
   produzia `CR CR LF`, reprovando os três arquivos. Passa a gravar bytes e a
   casar por mapa explícito de caminho remoto, e foi conferido nos dois cenários
   de fim de linha.

### Notas

- Validação local aprovada e espelho regenerado a cada pacote funcional.
- Testes: 37 em `hub_snippets/tests/test_core.py` (eram 21) e 23 em
  `tools/tests/test_tool_guards.py` (eram 14).
- `t_pit_join_preservacao` foi exercitado em PySpark 3.5.3 local, com quatro
  mutantes reprovando — inclusive o que preserva o total de linhas. Isso **não**
  substitui o smoke no Free em Spark 4.2.0, que precisa ser refeito.
- Continua aberto: escopo do `validate_assistant.py` por `git ls-files` (T3),
  recaptura do bloco de saídas de referência do `README.md`, T4 e T7.

## 2026-08-29 — Correções após auditoria externa dos READMEs

### Adicionado

1. (Codex) Registrados o parecer independente do Grok 4.6, o contraditório do
   Codex e a evidência datada da etapa 6 em `docs/auditoria/` e `docs/testes/`.

### Corrigido

1. (Codex) Unificado o estado vigente de publicação Free e separado esse estado
   da evidência histórica das etapas 1 a 5.
2. (Codex) Reordenado o ciclo canônico para validar, renderizar, publicar e
   verificar antes dos testes condicionais, do registro e da replicação; a
   matriz de impacto agora explicita quando cada gate é obrigatório.
3. (Codex) Corrigidas as referências ao glossário nos playbooks de replicação e
   distinguido `constants.styles` como espelho legado, sem efeito automático
   sobre módulos visuais.
4. (Codex) O catálogo de helpers passou a destacar o smoke vigente no Spark
   4.2.0 e a preservar os números de rodadas anteriores apenas como histórico;
   títulos ambíguos do histórico Spark receberam data explícita.
5. (Codex) O índice de skills operacionais passou a separar rotas ativas de uma
   rota apenas planejada. A documentação de instruções agora explicita as
   superfícies suportadas e a precedência geral das instruções de workspace.

### Validação

1. (Codex) Validação local aprovada com 737 arquivos inspecionados e 347 links
   externos à raiz do produto; o simulado foi regenerado com 317 arquivos.
2. (Codex) Publicação e verify no Databricks Free aprovados: 316 arquivos
   esperados, 317 remotos (um gerenciado pela plataforma), 0 ausentes, 0
   obsoletos, 13/13 skills e 4/4 diretórios `hub_`.

## 2026-08-29 — Redesenho editorial da etapa 6

### Adicionado

1. (Codex) Criados `docs/README.md`, `docs/playbooks/README.md` e
   `docs/sprints/README.md` para oferecer uma entrada única à governança,
   procedimentos e histórico de execução.
2. (Codex) Criado `ambiente_fonte/.assistant/GLOSSARIO.md`, separando vocabulário
   oficial da Databricks, conceitos de modelagem e convenções locais sem
   sobrecarregar o guia de uso.

### Atualizado

1. (Codex) Redesenhados os 20 READMEs ativos como um sistema de quatro níveis:
   repositório, governança, produto publicado e coleção. A regra
   `.claude/rules/docs-e-readmes.md` agora define propriedade do assunto,
   próxima ação, limites e prevenção de duplicação.
2. (Codex) O README raiz passou de manual linear para painel de manutenção; o
   README publicado do `.assistant` passou a conduzir instalação e uso por
   intenção; catálogos locais deixaram de repetir inventários mantidos em outro
   documento.
3. (Codex) Claims de Agent Skills foram reconciliados com a documentação oficial
   atual: `description` participa do carregamento relevante; o corpo e os
   recursos orientam a tarefa depois de carregados; skills podem referenciar
   documentação, templates e scripts. Os helpers externos do Hub continuam com
   import explícito.
4. (Codex) `Novo_Ambiente_Simulado/` foi regenerado exclusivamente por
   `tools/render_simulado.py` e o pacote documental foi republicado no Free.
   Verify aprovado com 316 arquivos esperados, 317 remotos (um gerenciado pela
   plataforma), 0 ausentes e 0 obsoletos.

### Validação

1. (Codex) `python tools/validate_assistant.py --conferir-readme` aprovado:
   22 linhas do README conferidas contra execução real, 107 Markdown ativos na
   fonte, 341 links externos à raiz analisada, 0 falhas e 0 avisos.
2. (Codex) A etapa 5 permanece pendente: 16 famílias de prompts e 3 casos de
   `hub-ml-criar-objeto` dependem da renovação da cota do Genie Code.

## 2026-08-29 — Checkpoint, publicação e smoke pós-auditoria

### Adicionado

1. (Codex) Criada a branch `codex/auditoria-a2-correcoes` e o checkpoint
   `02a5ad3`; gerado pacote limpo de 315 arquivos com manifesto SHA-256.
2. (Codex) Registrados o smoke integral em
   `docs/testes/spark/resultados/2026-08-29_smoke_a2.json` e a síntese das etapas
   em `docs/testes/2026-08-29_execucao-etapas-1-a-5.md`.

### Atualizado

1. (Codex) Publicação Free e verificação remota aprovadas: 315 arquivos
   esperados, 0 ausentes/obsoletos, 13/13 skills e 4/4 diretórios `hub_`.
2. (Codex) Smoke pós-correção aprovado no Spark 4.2.0: 145 verificações,
   136 PASS, 0 FAIL, 8 opcionais ausentes e 1 bloqueio MLflow esperado.

### Notas

- Os testes conversacionais não foram classificados: o Genie Code exibiu cota
  esgotada e envio desabilitado, com renovação em 01/09. Permanecem pendentes as
  16 famílias de prompts e os 3 casos de `hub-ml-criar-objeto`.

## 2026-08-20 — Auditoria de segunda origem com execução

### Adicionado

1. (Codex) `docs/auditoria/2026-08-20_segunda-origem-codex/01_rodada.md` —
   auditoria diagnóstica do baseline `9c17008`, executada em cinco frentes:
   biblioteca, ferramentas, produto/UX, documentação/decisões e
   segurança/replicação.

### Notas

- Os quatro gates foram reproduzidos antes dos probes: validação local e
  conferência do README aprovadas; verify remoto com zero problemas; smoke real
  com 145 verificações, 136 PASS, 0 FAIL, 8 dependências opcionais ausentes e um
  bloqueio esperado inspecionado.
- A rodada foi somente diagnóstica. Nenhum achado foi corrigido no produto,
  runbooks ou ADRs. A recomendação do relatório é não replicar no trabalho antes
  de conter os riscos externos e corrigir as três costuras analíticas prioritárias.

### Contraditório e correções pós-auditoria

1. (Codex) Adicionado
   `docs/auditoria/2026-08-20_segunda-origem-codex/02_treplica-e-execucao.md`:
   incorpora o contraditório independente do Claude, revisa severidades para
   2 críticas/16 relevantes/6 melhorias e registra a execução por F01–F24.
2. (Codex) Publicação/render/empacotamento endurecidos: perfil e host Free
   explícitos para escrita, inventário exato de skills, identidade neutra,
   proteção de path, falha em Git vazio, modos de auditoria e ZIP mínimo com
   manifesto SHA-256. ADR-0009 registra a decisão; a história Git anterior ainda
   exige reescrita coordenada antes de clone corporativo.
3. (Codex) Runbook e checklist deixaram de apagar `.mcp_servers.json` ou a pasta
   inteira de skills; substituem somente conteúdo Hub-owned e exigem pacote
   sanitizado/manifesto, smoke específico por ambiente e limpeza do run MLflow.
4. (Codex) Gates passaram a validar YAML real, nomes exatos, chamadas
   qualificadas, contratos de colunas, escopo Spark, coleta no driver,
   comportamento do detector e o contrato humano dos 16 prompts. Adicionados
   14 testes de mutação; 14/14 aprovados.
5. (Codex) Corrigidas as costuras analíticas de KS em pontos percentuais,
   vintage ragged, features temporais, `pit_join`, scorecard/bandas/lift,
   amostragem estratificada, PK nula e drift da coluna temporal. Os 21
   known-answer tests locais passaram; integração Spark pós-correção permanece
   pendente e não foi declarada aprovada.
6. (Codex) Os 161 campos dos 16 prompts ganharam instrução, motivo e exemplo;
   todos ganharam QA e limites. Corrigidos boilerplate sem rota, contratos de
   escrita falsos e a matriz de artefatos da skill de criação.
7. (Codex) Documentação viva conciliada com ADRs e documentação oficial:
   auto-descoberta de instruções/skills/AGENTS, publicador vigente, CLI nova
   0.205+ (preferência 1.0+ GA), 78 notebooks e contagens atuais do validador.
8. (Codex) Render regenerado em `Users/usuario-free/` com 316 arquivos; removidos
   89 diretórios `__pycache__` ignorados. Gerados artefatos de revisão marcados
   como worktree sujo, sem apresentá-los como pacote de commit limpo.

## 2026-08-19 — Bateria funcional de `ml`, e a costura que ninguém tinha exercitado

Os 16 módulos de núcleo de `ml` entraram na bateria repetível do
`spark_smoke_test.py`. Resultado da execução real no Free: **145 verificações,
136 PASS, 0 FAIL**, registro em
`docs/testes/spark/resultados/2026-08-19_bateria_ml.json`.

### Corrigido

1. (Claude) **`PLANO_HUB.md` §10 dizia que "os 16 da Sprint 7 nunca executaram"
   no Free — e estava errado desde 17/08.** O relatório da Sprint 7 traz os 16
   como job, todos `SUCCESS`. O que faltava era outra coisa: eles não estavam na
   bateria **repetível**. Execução de uma vez prova o dia; só a bateria prova que
   continua.
2. (Claude) **`calculate_woe_iv` e `build_scorecard` não se encaixam.** O
   primeiro devolve **Spark**, com a coluna de faixa nomeada como a feature; o
   segundo quer **pandas** com as colunas `faixa` e `woe`. Os dois passam
   sozinhos, e o notebook do scorecard monta a tabela à mão — então a junção
   nunca tinha sido exercitada por ninguém. A ponte de duas linhas está fixada no
   caso `ml:scorecard_builder` e documentada nos dois módulos e no catálogo.
3. (Claude) **`exemplo_vintage_analysis.py` importava `build_vintage_table` e
   nunca o chamava.** As quatro funções públicas do módulo não eram exercitadas
   por ninguém, e o notebook rodava com `SUCCESS` porque não havia o que quebrar.
   Ganhou as células que usam o módulo, com saída real colada.
4. (Claude) A "Nota de duplicação" do mesmo notebook ainda dizia que o módulo
   redeclara as cores — deixou de ser verdade em 18/08, quando passaram a derivar
   de `constants.colors`.

### Adicionado

1. (Claude) `check_notebook_exercita_o_objeto` — **23º check**. O notebook do
   objeto precisa **chamar** pelo menos uma função pública dele. Medição na
   origem: **1 de 60**. Por isso nasceu como falha.
2. (Claude) `run_case_bloqueado` no smoke test: caso que **precisa** falhar
   porque a plataforma o bloqueia, e que **reprova se passar**. `mlflow_run` é o
   primeiro. Um bloqueio documentado que deixa de existir é notícia tão relevante
   quanto um que aparece — e sem essa inversão chegaria como `PASS` silencioso.
3. (Claude) `run_case` passou a classificar `ImportError` sem `name`, que é o que
   o pandas levanta na dependência escondida (*"Missing optional dependency
   'tabulate'"*). Antes isso viraria `FAIL` e diria que a biblioteca está
   quebrada quando ela só precisa de `%pip`.

### Notas

- **Quatro das cinco falhas da primeira execução eram dos testes, não da
  biblioteca** — e o repositório documentava cada contrato que eu quebrei:
  `split_temporal` trabalha em pandas (o notebook avisa em caixa alta),
  `calculate_csi` quer `Series`, a chave é `auc_roc`, e `coefs` é array na ordem
  de `feature_names` — exatamente a confusão que a auditoria da Sprint 7
  registrou num notebook, e que a primeira versão do teste repetiu.
- **A quinta era real**, e é a costura WOE → scorecard. Nenhum portão a pegaria:
  a validação olha o disco, o `--verify` olha o workspace, e ambos os módulos
  passam sozinhos. Só a execução da junção a expõe.

## 2026-08-19 — Auditoria de segunda origem: a regra de idioma contra a biblioteca

Primeira rodada com modelo de outra família, e a primeira **sem execução**: o
corpus versionado inteiro numa janela só, 402 arquivos. Relatório em
`docs/auditoria/2026-08-19_leitura-contexto-longo/`.

> **Correção da primeira versão desta entrada**, escrita horas antes: ela dizia
> que a rodada *"abre o gate de segunda origem do `PLANO_HUB.md` §10"*. **Não
> abre.** O gate do §10 é *"auditoria de segunda origem **da biblioteca**"*, e
> esta rodada foi de leitura, sem executar uma linha — auditou consistência
> documental, não corretude de código. O gate continua aberto. A frase é a classe
> de defeito que este projeto mais corrige, escrita por quem a nomeou.

Três achados reportados — 1 procedente, 1 parcial, 1 improcedente — e **um achado
forte fora da lista**, na única análise que nenhuma rodada anterior tinha pedido.

### Corrigido

1. (Claude) **Três documentos vivos mandavam "inglês em identificadores", e a
   biblioteca praticava outra coisa:** 85 funções públicas em inglês contra 5 em
   português, e **37 constantes em português**. O que torna o caso grave é onde a
   regra vivia — o `.assistant_instructions.md` é publicado e injetado em **toda**
   conversa do Genie Code, então o assistente era instruído a usar inglês e, na
   mesma sessão, mandado importar `AZUL_CAIXA` e `SECOES_EDA`.
   **A correção foi na regra, não na biblioteca:** constante de domínio em
   português nomeia coisa que só existe aqui, e traduzir apaga o referente. A
   regra passou a dizer o que o projeto pratica.
2. (Claude) `PLANO_HUB.md` §12.2 dizia "7 cores da paleta" para `curves_plotly`.
   O módulo tinha **7 hexadecimais oficiais** — 6 da paleta mais o
   `TEXTO_SECUNDARIO`. O número estava certo e a palavra errada; a correção
   proposta pelo auditor (trocar 7 por 6) teria **introduzido** um erro.
3. (Claude) A skill do tutor escrevia "Asset Bundles"; o nome legado oficial é
   **"Databricks Asset Bundles"**.
4. (Claude) `hub-ml-criar-objeto` passou a dizer que o exemplar de skill se **lê e
   não se copia** — qualquer pasta em `.assistant/skills/` é auto-descoberta, e
   uma cópia viraria skill fantasma no chat.

### Adicionado

1. (Claude) `PLANO_HUB.md` §12.3 — **cinco funções públicas em português**
   (`aplicar_tema`, `gerar_indice_eda`, `get_tema_eda`, `calcular_psi`,
   `calcular_csi`), deriva contra uma convenção que 85 irmãs cumprem. Não
   renomeadas: renomear função pública quebra quem chama, em silêncio. **Não
   instrumentada, com razão registrada** — uma heurística de "nome em português"
   acusaria `psi_calculator` tanto quanto `calcular_psi`, e nasceria com cinco
   exceções.

### Notas

- **Segunda origem funciona mesmo com desempenho menor.** O achado de idioma
  estava disponível para as 14 rodadas anteriores e nenhuma o viu, porque nenhuma
  leu uma regra de estilo contra a biblioteca inteira. Um achado que só a troca de
  origem produz paga a rodada.
- **A análise que rendeu foi a inédita.** Das oito pedidas, a única que nenhuma
  rodada anterior tinha feito — ler as 13 skills e as instruções pessoais como um
  corpo único de instruções — foi a que achou. As sete que repetiam ângulos já
  auditados devolveram matrizes corretas e vazias.
- **Auditor sem execução precisa de âncora mais rígida.** Três problemas do
  relatório têm a mesma raiz: sem poder rodar nada, preenche-se a lacuna com
  plausibilidade. Foram uma afirmação falsa sobre o validador, um achado já
  corrigido no dia anterior, e **três enunciados de forward test inventados**
  quando o prompt indicava o arquivo com os literais. O próximo prompt de leitura
  vai exigir transcrever antes de julgar, e não só citar ao julgar.

## 2026-08-19 — Empacotador para auditoria de contexto longo

### Adicionado

1. (Claude) `tools/bundle_para_auditoria.py` — empacota o repositório versionado
   num arquivo único, com delimitador por arquivo. **402 arquivos, ~478 mil
   tokens**, o que cabe numa janela de 1M.

### Notas

- Existe para uma rodada de auditoria de **leitura**, não de execução: a classe
  de defeito que nenhum portão daqui pega por construção é a contradição entre
  dois documentos publicados, e ela só aparece com o corpus inteiro numa janela
  só. É o complemento natural das 14 rodadas anteriores, todas com acesso a
  execução e nenhuma com o corpus completo em contexto.
- Exclui por padrão `Novo_Ambiente_Simulado/`, que é cópia byte a byte do fonte,
  e `Ajustes_Codex/`, congelada: juntas dobrariam o tamanho sem acrescentar
  informação. `--incluir-espelho` traz as duas de volta.
- O arquivo gerado é git-ignored.

## 2026-08-18 — A norma vira instrumento, e as 13 skills ficam completas

Segunda parte do dia. A classe nomeada pela auditoria — *norma publicada sem
instrumento* — deixou de ser diagnóstico e virou fila de trabalho executada.

### Adicionado

1. (Claude) `check_normas_do_molde` — o **vigésimo primeiro** check, e o primeiro
   a instrumentar `hub_padroes/snippet/template.md` em bloco. Quatro ordens do
   molde que são mecanicamente decidíveis, cada uma citando a linha que a impõe:
   `cache()`/`persist()` fora de `try`; `toPandas()` sem limite verificável; o
   global `spark` dentro de módulo importado; e `__init__.py` de seção que
   reexporta. **Nasceu como falha**, porque as quatro já estavam em zero. As
   quatro foram provadas construindo uma violação de cada.
2. (Claude) **A seção "Quando esta skill se aplica" nas 12 skills que não a
   tinham**, derivada da própria `description` — que é o contrato de roteamento —
   mais a fronteira explícita com a skill vizinha. Adição pura: nenhuma linha
   existente foi alterada, e o roteamento não muda, porque quem roteia é a
   `description`.
3. (Claude) **A seção "O que nunca fazer" nas 10 skills que não a tinham.** Cada
   proibição sai de armadilha já documentada aqui — `cache()` em serverless, PSI
   com limiar universal, `shap` sem pin, API clássica de `pyspark.ml` sob Spark
   Connect, nome antigo de produto Databricks. Nenhuma foi inventada.

### Corrigido

1. (Claude) **Dois erros de medição na própria `check_skill_secoes`**, achados ao
   instrumentá-la — a mesma classe que ela existe para pegar:
   - **falso positivo:** a chave `"aplica"` contava a seção "Aplicar qualidade" de
     `hub-ml-pipeline-builder` como se fosse a de escopo, e a skill aparecia
     completa sem ter a seção. Virou `"se aplica"`.
   - **falso negativo:** sete skills listam proibições sob o título `Guardrails`,
     e três descrevem o fluxo como sequência de seções no infinitivo. A primeira
     virou palavra-chave; a segunda virou **detecção estrutural**, porque
     renomear seções boas para agradar a guarda é ajustar o mundo ao instrumento.
2. (Claude) `check_skill_secoes` **promovida de aviso a falha**. Contagem:
   **13/13 com as cinco seções**, contra 2/13 na véspera.

### Atualizado

1. (Claude) `.claude/rules/free-vs-trabalho.md` ganhou a linha e a seção sobre o
   **orçamento próprio do assistente**: ele esgota sozinho, trava até a virada do
   mês, e **não afeta compute nem workspace**. Medido, não suposto — job entra em
   `RUNNING`, `mkdirs`/`delete`/`export` respondem `exit=0`. A regra passa a
   mandar medir o alcance de um bloqueio em vez de presumi-lo.

### Notas

- **O validador tem 22 checks e roda em 0 falhas e 0 avisos.** Três guardas foram
  promovidas de aviso a falha no mesmo dia — saída colada, idioma da docstring e
  seções de skill —, todas pelo mesmo critério: aviso é para dívida aberta com
  prazo; norma cumprida se cobra.
- A dívida de §12.1 e §12.2 e a das seções eram as três **nomeadas** que restavam
  no `PLANO_HUB.md`. As três estão fechadas; o que sobra depende do chat do Genie
  Code, bloqueado até 1º/set.

## 2026-08-18 — As duas dívidas nomeadas fecham, e o validador zera

`PLANO_HUB.md` §12.1 e a higiene do §12.2 foram fechadas no mesmo dia. O
validador passou a **0 falhas e 0 avisos** pela primeira vez desde que existe.

Contexto operacional: o orçamento do assistente do Databricks Free esgotou até
1º/set, o que bloqueia o chat do Genie Code — e portanto os forward tests e as
partes 3 dos prompts. Compute, jobs e workspace continuam funcionando, o que
liberou justamente estas duas dívidas.

### Corrigido

1. (Claude) **§12.1 — os 11 notebooks sem saída real colada.** Executados **como
   um job só** no Free, com um driver que roda cada notebook célula a célula e
   captura o que cada uma imprime. **Cinquenta blocos** de saída real entraram
   nos onze arquivos, cada um na célula de markdown que lê o resultado — colar no
   fim fecharia a guarda sem fechar a dívida. Contador: `66 com bloco, 11 sem` →
   **`77 com bloco, 0 sem`**.
2. (Claude) `check_saida_colada` **promovida de aviso a falha**, que era a escada
   escrita no docstring dela desde a Sprint 6: *"promover quando `sem_bloco`
   chegar a zero"*. Provada removendo o bloco de um notebook: reprova.
3. (Claude) **§12.2 — a cor redeclarada.** Os onze sítios de cópia idêntica
   passaram a derivar de `constants.colors`; **trinta hexadecimais saíram do
   código**. Sobraram os seis da única linha divergente, agora marcada
   `PENDENTE/DECISAO` no próprio arquivo.
4. (Claude) `constants/styles` — o espelho morto — passou a **dizer no docstring**
   que nenhum módulo o importa, e suas cores institucionais agora derivam de
   `colors`. O CSS continua duplicado por decisão registrada: unificá-lo mexeria
   na saída de cinco módulos.

### Notas

- **Três provas sustentam o §12.2, e nenhuma é opinião.** O script aborta se o
  literal não bater byte a byte com o nome oficial (14 nomes e 2 paletas
  conferidos); a saída de `visual/` foi capturada antes e depois com **zero
  divergências**; e `api_publica.py` regerado nos 51 módulos deu **zero
  `__init__.py` divergentes**. Fechando, o smoke test no runtime real: **129
  verificações, 122 pass, 0 fail**, os 7 restantes sendo dependência opcional
  ausente.
- **A armadilha que a terceira prova pegou.** A forma óbvia — trocar
  `AZUL_CAIXA = "#005CA9"` por `from ... import AZUL_CAIXA` — quebraria a API
  pública de quatro módulos, porque `api_publica.py` exclui do `__all__` o que foi
  apenas importado. A forma correta é atribuição derivada.
- **A ordem também importa.** Em `ml/kaplan_meier` a lista de oito cores não é
  `PALETA_CATEGORICA[:8]`: `CINZA_ESCURO` vem por último ali. Fatiar a paleta
  teria trocado a cor de quatro curvas em silêncio.
- Três armadilhas da captura ficaram registradas no §12.1, porque a próxima vai
  encontrá-las: `display()` não escreve em stdout e **`_jdf` não existe no Spark
  Connect**; split de notebook com `\s*$` come a linha em branco seguinte; e o
  notebook do `doc_coverage` **cita** os marcadores de célula, o que quebra
  qualquer split por literal.
- Compute e workspace do Free foram medidos, não supostos: `mkdirs`/`delete`
  respondem, job entra em `RUNNING`. O bloqueio é só do assistente.

## 2026-08-18 — Auditoria de consistência e didática: 18 achados, e uma sigla que atravessou a quarentena

Décima quarta rodada, `A1`, sobre o conjunto e com foco no padrão didático da
documentação. Relatório em
`docs/auditoria/2026-08-18_consistencia-e-didatica/`.

### Corrigido

1. (Claude) **Um identificador corporativo estava publicado no produto** — a
   sigla de um órgão de governança interno, numa linha de rubrica dentro de
   `templates/` de uma skill. Estava no workspace Free e entraria no do trabalho
   pelo runbook. O `ADR-0003` quarentenou a **pasta** `Ambiente_Antigo/` em
   15/08; não alcançou o **vocabulário** que já tinha atravessado para
   `ambiente_fonte/` antes disso. O `CORPORATE_RE` ganhou uma classe de siglas
   internas — escrita com uma letra entre colchetes, para que a constante não
   reprove a si mesma, e com fronteira à mão, porque `_` conta como caractere de
   palavra. Uma varredura cruzando as 198 siglas da pasta em quarentena contra o
   produto não achou nenhuma outra.
2. (Claude) **O `CHANGELOG.md` de 17/08 registrava uma correção que nunca foi
   escrita em disco:** os avisos de superseding nos `ADR-0004` e `ADR-0005`. O
   script daquela sessão procurava a âncora `- **Status:`, que é o formato dos
   ADRs novos; os dois antigos usam `Status:` sem marcação, a âncora não casou, e
   a função **imprimiu sucesso mesmo assim**. Os banners foram escritos agora, e
   o script desta rodada aborta quando uma âncora não casa.
3. (Claude) **26% da biblioteca violava o molde que a própria biblioteca
   publica.** `hub_padroes/snippet/template.md` manda docstring em português; 15
   dos 58 módulos estavam em inglês, sendo **7 de 7** em `hub_scripts/`. As 15
   foram traduzidas, identificadores intactos.
4. (Claude) `--conferir-readme` tinha uma segunda porta de degradação
   silenciosa: quando o comando **não lançava**, o `except` devolvia zero e a
   guarda aprovava. Agora reprova, nomeando o comando e a causa provável.
5. (Claude) `CLAUDE.md` atribuía ao `ADR-0006` uma supersessão que é do
   `ADR-0005`, com a razão do 0005 colada no bullet do 0006. Separados.
6. (Claude) `forward/README.md` anunciava **GATE FECHADO 36/36** enquanto o
   `roteiro.md`, na mesma pasta, fala em 39 testes — a ressalva que a Sprint 12
   escreveu em três documentos morria a um clique de distância. Corrigido lá e no
   glossário publicado, que era o quarto documento a citar 36 sem ressalva.
7. (Claude) `ciclo-de-vida.md` mandava a um runbook "a criar" que existe,
   ignorava o runbook irmão na mesma pasta, e ordenava o ciclo de forma diferente
   dos dois documentos que dizem resumi-lo. Reescrito com a ordem única —
   registrar **depois** de conferir, porque o `--verify` produz o número que a
   entrada cita — mais diagrama e seção de fontes.
8. (Claude) `hub_padroes/README.md` era o único README do produto sem o aviso de
   não-descoberta, e é o que o guia principal indica como porta de entrada dos
   moldes. Ganhou o banner dos irmãos.
9. (Claude) O glossário publicado remetia oito verbetes a `docs/`, que não é
   publicado — beco sem saída para quem só recebeu o `.assistant/`. Ganhou o
   aviso; e a solução de problemas ganhou a linha que faltava sobre editar
   direto no workspace, que era o erro de maior custo do analista da squad e só
   estava avisado no repositório.
10. (Claude) Números mortos: sete imports cruzados (o inventário dizia seis e
    omitia `section_header -> constants.emojis`), dez nomes em `test_core.py`,
    39 de 51 módulos com mais de um nome público. Os deriváveis viraram comando.
11. (Claude) `PLANO_HUB.md` §1 dizia que o nome das skills era `hub-ml-` **antes**
    da renomeação — uma busca-e-substituição varreu a coluna histórica junto.
12. (Claude) O comentário do `PERSONAL_RE` prometia alcance global; os dois
    checks que o usam recebem `ambiente_fonte/`. Reescrito com o alcance real.

### Adicionado

1. (Claude) `check_docstring_em_portugues` — vigésimo check, e o primeiro a
   cobrar uma **norma publicada** em vez de um fato estrutural. Nasceu como
   falha, não como aviso: a dívida fechou na mesma sessão, e aviso sobre norma
   cumprida é convite à regressão.
2. (Claude) `tools/README.md` e `docs/testes/README.md`, os dois diretórios sem
   README que custavam alguma coisa a alguém. O de `tools/` abre declarando que a
   pasta **não é publicada** — que é a causa de o produto mandar rodar scripts
   que o leitor não tem.

### Notas

- **A classe nova é sobre método: norma publicada sem instrumento, auditada como
  prosa e nunca como especificação.** Treze rodadas perguntaram "isto é
  verdade?"; a décima terceira acrescentou "isto concorda com aquilo?". Nenhuma
  perguntou "isto é uma norma, e o repositório a cumpre?". O molde de
  `hub_padroes/` é especificação executável escrita em Markdown, com autoridade
  declarada e, até aqui, zero cobertura.
- **Diferença da classe anterior:** contradição entre dois artefatos é simétrica
  e qualquer lado pode ceder; aqui há hierarquia — o molde está certo por
  construção, e o que sobra é dívida de conformidade, mensurável e automatizável.
- Duas recomendações do auditor foram **recusadas com motivo registrado**: o
  roteiro de forward tests não foi parametrizado (ganhou aviso de substituição, e
  os prompts continuam coláveis sem edição por quem os usa hoje), e três dos
  cinco READMEs ausentes não foram escritos, por serem burocracia sobre pastas
  que o README da raiz já mapeia.

## 2026-08-17 — Auditoria final do conjunto: 18 achados, e a classe que doze rodadas não viram

Décima terceira rodada, a única que auditou **o conjunto** e não uma sprint.
Dezoito achados, todos procedentes. Resposta completa no fim de
`docs/sprints/sprint-12-fechamento.md`.

### Corrigido

1. (Claude) **`check_skill_helpers_resolvem` não pegava o defeito que a
   originou.** Aceitava o caminho quando a pasta-pai existia — e para
   `hub_snippets.<secao>.<objeto>` a pasta-pai é a seção, que sempre existe.
   Medição do auditor: **59 dos 72 caminhos (82%) desprotegidos**. Reescrita: o
   destino precisa ser pasta de objeto (com `__init__.py`), e quando o caminho
   termina na função, o último componente precisa estar na API pública que o
   `__init__.py` de lá exporta. Provada contra os quatro casos construídos pelo
   auditor mais o caso legítimo `hub_snippets.spark.pit_join.pit_join`.
2. (Claude) **Duas frases retratadas continuavam publicadas no
   `CATALOGO_HELPERS.md`** — que `prophet_wrapper` falha por não inicializar o
   backend, e que instalar sem fixar versão derruba o kernel. A execução de 17/08
   desmentiu as duas, e a retratação já estava em três outros documentos. O
   parágrafo passou a **remeter ao inventário em vez de repetir o conteúdo
   dele**, com a razão declarada: "foi testado" tem data de validade.
3. (Claude) **`GUIA_REPLICACAO_TEMPORARIO.md` descrevia o repositório de 35
   commits atrás**, com `x_config/`, `x_docs/` e `x_projects/` — pastas que a
   Sprint 2 apagou. Aposentado, com aviso no lugar do conteúdo. A causa é
   estrutural: o arquivo é git-ignored, e nenhum portão varre o que não está
   versionado.
4. (Claude) **`--conferir-readme` degradava em silêncio**: rótulo ausente na
   saída real fazia o laço seguir. Numa máquina sem CLI autenticada, três
   contagens erradas por 685, 684 e 86 passavam em dois segundos. Agora reprova,
   nomeando o rótulo e a causa provável.
5. (Claude) `ADR-0004` e `ADR-0005` ganharam aviso de superseding no topo, e as
   "Decisões ativas" do `CLAUDE.md` canônico — que roteava só para eles —
   passaram a citar `ADR-0006`, `ADR-0007` e `ADR-0008`.
6. (Claude) Errata append-only no `ADR-0007` (marcador `imp`, não `opt`; dez
   casos de `exec`, não dois; o alcance do "sem uma edição") e no `ADR-0008`
   (a data do ADR-0005 é 14/08).
7. (Claude) Números mortos restantes trocados por comando: a estimativa de
   esforço da rota C e os "4 diretórios `hub_`" do checklist. O `36/36` de
   roteamento ganhou, nos três documentos que o citam, a ressalva de que a 13ª
   skill **nunca foi testada** — e a instrução de incluí-la nos testes.
8. (Claude) O produto publicado mandava rodar `tools/`, que não é publicado:
   ressalva no checklist e no `README.md` do `.assistant/`, onde também caiu o
   único `x_` residual de todo o produto.

### Notas

- **A classe nova é sobre método, não sobre defeito: contradição entre dois
  artefatos publicados, quando cada um passa sozinho.** As doze rodadas
  anteriores compararam sempre *um documento contra a realidade*; nenhuma leu
  *dois documentos publicados um contra o outro*. Seis dos dezoito achados só
  aparecem por leitura pareada, e **nenhum portão pode pegá-los por construção**
  — o validador confere links, forma e contagens contra o disco, nunca duas
  afirmações entre si.
- **A variante sutil: a referência de volta.** Doze auditorias verificaram que os
  links resolvem; ninguém verificou se o destino **sabe que foi apontado**. Foi
  assim que os ADRs supersedidos ficaram sem aviso enquanto a entrada canônica
  continuava roteando para eles — com os quatro links resolvendo perfeitamente.
- **Veredito de prontidão**, contra o perfil de um analista de CRM sem CLI e sem
  acesso ao repositório: pronto para uso, com o `.assistant/README.md` recebendo
  a melhor avaliação das treze rodadas. As duas condições que o auditor pôs para
  distribuir — corrigir o catálogo e não usar o guia temporário — foram atendidas
  nesta rodada.
- Candidato de melhoria **não** aplicado: `--conferir-readme` reexecuta o
  `validate_assistant.py` como subprocesso para reler a própria saída como texto,
  quando os números já estão em variáveis no `main()`. Metade do custo de 1m41s é
  duplicação. Mudar o desenho de uma guarda no mesmo dia em que ela foi escrita e
  corrigida duas vezes é como se introduz o terceiro defeito.

## 2026-08-17 — Sprint 12: fechamento, com dois ADRs e três guardas

Última sprint de execução do `PLANO_HUB.md`. Relatório em
`docs/sprints/sprint-12-fechamento.md`.

### Adicionado

1. (Claude) `ADR-0007` — o catálogo depois da pasta de objeto. Supersede o
   ADR-0004 nos pontos de localização e forma; a decisão de fundo (declaração
   explícita de helpers) é reafirmada. Formaliza a coluna de dependência com o
   estado `exec`, que nomeia a classe descoberta nas Sprints 7 e 9.
2. (Claude) `ADR-0008` — o critério de conferência sai do ADR e vai para
   constante de código. Supersede o ADR-0005 nesse ponto. A decisão não é
   corrigir "12 skills, 6 diretórios" para 13 e 4: é **tirar o número do texto**,
   porque contagem em ADR envelhece sem que nada acuse.
3. (Claude) Três guardas em `tools/validate_assistant.py`, cada uma contra um
   defeito que aconteceu:
   - `check_saida_de_comando_no_readme` (flag `--conferir-readme`) reexecuta os
     comandos e reprova se algum número colado divergir. Provada com o defeito
     exato da Sprint 10, e **pegou quatro divergências reais** na primeira
     execução, criadas pelas edições desta própria sprint.
   - `check_skill_helpers_resolvem`: os 72 caminhos `hub_snippets.x.y` citados
     nas 13 skills resolvem. Renomear um objeto os quebraria em silêncio.
   - `check_skill_secoes`: cobra a seção de helpers e reporta **2 de 13** com as
     cinco seções do template, como contagem informativa.

### Atualizado

1. (Claude) Os três playbooks de replicação trocaram número morto por **comando
   que devolve o número**. O checklist ganhou quadro em branco para quem replicar
   preencher com a saída do `--verify` — o registro passa a ser do que foi de
   fato copiado.

### Notas

- **A guarda de seções exigiu calibragem.** A primeira versão acusava treze
  skills por execução: as 12 originais são anteriores ao template, e o casamento
  por palavra-chave produz falso positivo sobre título legítimo. A versão final
  cobra só a seção de helpers, que é a que tem consequência concreta.
- Fica declarado o que este projeto aprendeu em doze auditorias e ~150 achados:
  prosa confiante sobre coisa não verificada é a classe mais frequente; "foi
  testado" tem data de validade em ambiente gerenciado; e cada portão pega uma
  classe, nenhum pega a do vizinho.

## 2026-08-17 — Sprint 5: os 16 prompts ganham notebook, com a parte 3 declarada em branco

Os 16 prompts viraram pasta de objeto, cada um com o notebook de três partes. As
duas primeiras estão prontas e executam; a terceira depende de uma pessoa num
chat. Relatório em `docs/sprints/sprint-5-hub-prompts.md`.

### Adicionado

1. (Claude) 16 pastas em `hub_prompts/`, com o briefing e o
   `exemplo_<nome>.py`. Os 16 executaram como job: 16 de 16 SUCCESS nas partes
   1 e 2.
2. (Claude) A parte 1 de cada um cria a base sintética a que o prompt se refere,
   **com o defeito certo plantado** — duplicata de chave no `data_quality`,
   vazamento temporal no `cross_eda` e no `feature_engineering`, safra imatura no
   `safra`, prevalência e nulo em movimento no `monitoramento_modelo`.
3. (Claude) A parte 2 traz o prompt preenchido: cerca de **160 placeholders**,
   todos com valor, para a base da parte 1.

### Notas

- **A parte 3 fica em branco por decisão, não por esquecimento.** O template é
  explícito: resposta inventada é pior que resposta nenhuma, porque ensina que o
  assistente faz algo que ele não faz. Cada notebook traz o bloco canônico com o
  motivo e um roteiro de cinco passos para quem preencher.
- Onde a resposta honesta era "não sei", o placeholder foi preenchido com **"não
  informado"** — e o notebook explica que isso é informação, não omissão.
- `comparar_tabelas` e `novo_projeto` **não declaram skill recomendada**, de
  propósito. O que o Genie Code escolher neles é evidência de roteamento que
  nenhum forward test produz.

### Corrigido

1. (Claude) Os 16 briefings desceram um nível e os links para
   `../CATALOGO_HELPERS.md` quebraram — mesma classe da Sprint 2. Recalculados
   com `os.path.relpath`, não com substituição cega. A validação pegou os 16 de
   uma vez; o `--verify` pegou os 16 briefings planos que continuavam no
   workspace.
2. (Claude) `agg({"id_contrato": "countDistinct"})` no notebook do `safra` não
   resolve — o nome não existe como rotina SQL. Trocado por `F.countDistinct`,
   com o comentário explicando a diferença.

## 2026-08-17 — auditoria da Sprint 11: 19 achados, e a skill que não cumpria o próprio molde

O auditor **usou a skill** para criar um objeto, do começo ao fim, e relatou onde
travou — foi de lá que saiu o achado bloqueante. Detalhe em
`docs/sprints/sprint-11-hub-ml-criar-objeto.md`.

### Corrigido

1. (Claude) **O `SKILL.md` nunca mencionava `# Databricks notebook source`.** Ele
   descrevia as cinco etapas do notebook em detalhe e omitia a única exigência que
   o portão de fato impõe. Seguir a skill ao pé da letra produzia REPROVADO com
   duas mensagens que se contradizem sobre o mesmo arquivo.
2. (Claude) A skill afirmava que "o validador reprova" nome de módulo divergente
   do nome da pasta. Ele **pulava** o caso — `if not modulo.exists(): continue` —
   e nem contava a pasta. Ver Adicionado.
3. (Claude) "Os quatro primeiros o validador confere sozinho": o primeiro é "o
   tipo foi confirmado com quem pediu", que nenhuma ferramenta verifica. A skill
   ganhou tabela dizendo linha a linha o que é ferramenta e o que é pessoa.
4. (Claude) Faltavam **três das cinco seções** que `hub_padroes/skill/template.md`
   declara obrigatórias — inclusive a de helpers, que o template chama de "não
   opcional e não decorativa". As doze anteriores têm todas; a criada para fazer
   cumprir os moldes era a que menos cumpria.
5. (Claude) A árvore de pastas mostrava `hub_snippets/<secao>/` rotulada "para
   snippet e script"; script não tem nível de seção. E "script recebe nome de
   tabela" não classifica `doc_coverage`, que recebe caminho de arquivo.
6. (Claude) `skills/README.md` dizia "Doze skills" acima de uma tabela com treze,
   e `ambiente_fonte/README.md` ainda dizia "12 Agent Skills" — os dois
   publicados no Free. `hub_padroes/README.md` anunciava a skill como "planejado,
   ainda não existe".
7. (Claude) O roteiro de forward test dizia 36 e 39 no mesmo arquivo, com a
   **meta do gate** parada em 36/36; o formulário de resultados não tinha a
   Skill 13; e o ideal declarado do `13N` estava errado — a `description` de
   `hub-ml-validacao-estatistica` não contém "PSI" nem "safra", e o caso `04N`,
   quase idêntico, já declarava `hub-ml-monitoramento-modelo`.
8. (Claude) O exemplar de script de `hub_padroes/`, que a skill manda ler como
   referência, **não tinha saída colada** — violava a regra que a skill ensina.
   As duas saídas foram executadas e coladas. **A dívida de §12.1 caiu de 12
   para 11.**

### Adicionado

1. (Claude) `check_pasta_de_objeto_malformada` em `tools/validate_assistant.py`,
   com a regra invertida: toda pasta sob `hub_snippets/<secao>/` ou
   `hub_scripts/` que tenha `__init__.py` **precisa** ter `<nome>.py`. Provada
   com o caso que o auditor construiu.
2. (Claude) `checklist-objeto-novo.md` virou o **canônico**, com bloco por tipo,
   e os quatro templates de `hub_padroes/` passaram a apontar para ele. Três
   listas divergentes conviviam; nenhuma das duas novas cobria script ou skill.
   A lista foi dividida em **verificável por terceiro** e **juízo de quem
   escreveu** — cerca de oito de trinta itens não eram verificáveis.

### Notas

- **Previsão registrada antes do teste.** Pedi ao auditor que previsse o
  roteamento dos três forward tests lendo apenas as treze `description`. Ele
  prevê `hub-ml-criar-objeto` no `13P` e `13M`, e **não** a skill nova no `13N` —
  com a colisão real sendo `monitoramento-modelo` × `analise-safra`, anterior a
  esta sprint. O teste humano vai confirmar ou derrubar.
- **O que nenhum portão vê numa skill:** conformidade do corpo ao template.
  Doze de treze têm a seção de helpers, a décima terceira não tinha, e os dois
  portões aprovaram. Candidata de guarda para a Sprint 12.
- O auditor confirmou todas as demais afirmações do corpo, medindo cada uma —
  inclusive, com um script sobre os 64 commits, que "dois objetos ficaram fora do
  catálogo por uma sprint inteira" é verdadeiro e preciso.

## 2026-08-17 — Sprint 11: a skill que cria objeto do Hub

`hub-ml-criar-objeto`, a décima terceira skill. Primeira mudança em roteamento
desde a Sprint 3. Relatório em `docs/sprints/sprint-11-hub-ml-criar-objeto.md`.

### Adicionado

1. (Claude) `.assistant/skills/hub-ml-criar-objeto/`, com `SKILL.md` e
   `templates/checklist-objeto-novo.md`. Ela conduz a criação de qualquer um dos
   seis tipos de objeto aplicando o molde de `hub_padroes/` — e existe por causa
   da decisão §2.1, que pôs os templates dentro de `.assistant/` e portanto no
   workspace.

### Atualizado

1. (Claude) `EXPECTED_SKILLS` de 12 para 13 em `tools/publicar_free.py`.
2. (Claude) Onze arquivos afirmavam "12 skills". Onde dava, o número foi trocado
   por formulação que não envelhece; onde ele é o ponto — `EXPECTED_SKILLS`, a
   saída de exemplo do README —, foi atualizado. O próprio template de README
   avisava contra isso: *"as 12 skills vira mentira na décima terceira"*.
3. (Claude) O quadro de status do README da raiz passou a declarar 36/36 nas
   **doze originais**, com a décima terceira explicitamente não testada.

### Notas

- **A skill não gera arquivo pronto: ela conduz.** Manda confirmar o tipo antes
  de escrever, exige que o template seja anexado (`hub_padroes/` não é
  auto-descoberto), e carrega as armadilhas que custaram caro nesta fase — cada
  regra do corpo tem um custo real citado ao lado.
- **A `description` é a hipótese não testada.** Ela fecha com o que a skill não
  cobre, para não roubar a vez de quem faz análise: sem esse período, "criar um
  snippet que calcula PSI" carregaria formato em vez de estatística. Medir isso
  exige forward test, que depende de interação humana.
- Pendente: os três casos de forward test da skill nova. O **negativo** é o que
  importa — vocabulário de "criar objeto" roça o de todas as vizinhas.

## 2026-08-17 — auditoria da Sprint 10: 12 achados, e o defeito que se repetiu

O auditor seguiu o README ao pé da letra — publicou um notebook no Free com os
trechos copiados literalmente e rodou como job. Doze achados, todos procedentes.
Detalhe em `docs/sprints/sprint-10-readmes-de-topo.md`.

### Corrigido

1. (Claude) **As três saídas de comando coladas estavam erradas — pelo arquivo que
   a própria sprint apagou.** Capturei os números e só depois removi o
   `GLOSSARIO.md`; quatro contagens caíram em 1 e uma subiu em 2. Esta sprint
   existia para corrigir saídas desatualizadas e reproduziu o defeito um commit
   adiante. Recapturadas, e a ordem **editar → rodar → colar → commitar** ficou
   escrita no próprio README.
2. (Claude) A seção nova prometia saída real colada em todo notebook, com
   "sempre". Falta em **11 dos 58** — e o exemplo que eu escolhi para ilustrar,
   com "abra este primeiro", era `pit_join`, um dos onze. Trocado por
   `safe_display`, e os onze declarados com ponteiro para §12.1.
3. (Claude) Os "três casos conhecidos" de bloco não-executado erravam nos três:
   `pyspark.ml` não é bloco de não-executado (o notebook executa e cola o
   `Py4JError` real), sobrou uma dependência de pandas e não duas, e havia um
   quarto bloco no template ensinando uma limitação do Prophet que deixou de
   existir.
4. (Claude) `docs/testes/spark/README.md` ainda declarava `prophet_wrapper` não
   verificado — contra o `requirements-optional.txt`, a regra
   `free-vs-trabalho.md` e o próprio README da raiz — e usava caminhos
   `x_snippets/` de antes da Sprint 2.
5. (Claude) "Quatorze objetos de `ml/` instalam sozinhos": são **quinze**, com
   `display/dataframe_styled` estruturalmente idêntico.
6. (Claude) O "Mapa do repositório" omitia o `PLANO_HUB.md`; o
   `CATALOGO_HELPERS.md` não tinha `constants.emojis` nem `constants.styles`; e
   `checklist-replicacao.md` dizia 6 diretórios numa linha e 4 em outra.

### Atualizado

1. (Claude) `check_repo_links` ganhou a guarda de varredura vazia que só
   `check_repo_corporate` tinha. O README prometia que **ambas** reprovassem com
   zero; metade da rede não existia. Preferi consertar o código a enfraquecer a
   frase — provado com sonda que troca `REPO_ROOT` por diretório vazio.

### Notas

- **O que a auditoria confirmou é o que mais importava:** seguir o README
  funciona. Os caminhos existem na caixa exata, os três imports rodam no
  workspace, as saídas de confirmação batem caractere por caractere, e o "engano
  mais comum" documentado reproduz a mensagem prometida.
- O glossário migrou limpo: 65 termos antes, 65 depois, hierarquia correta, onze
  âncoras resolvendo — inclusive as acentuadas.
- **Nenhum portão veria nenhum dos doze.** Eles conferem estrutura, sintaxe, link
  e tipo de objeto; nenhum lê uma frase e pergunta se é verdade. A ironia do
  achado 1 é que o validador imprimia a resposta certa na tela enquanto o README
  exibia a errada. A guarda que fecharia o caso — extrair os blocos de saída,
  reexecutar e falhar na divergência — fica registrada como candidata da
  Sprint 12.

## 2026-08-17 — Sprint 10: os dois READMEs de topo, e o glossário absorvido

`README.md` da raiz e `.assistant/README.md` atualizados na variante longa.
Relatório em `docs/sprints/sprint-10-readmes-de-topo.md`.

### Atualizado

1. (Claude) As três saídas de comando coladas no README da raiz estavam da
   Sprint 2 e erravam por larga margem — 70 arquivos Python contra 193, 176
   arquivos renderizados contra 298, 409 varridos contra 674. Recolhidas de
   execução real, e o bloco do validador passou a mostrar as **quatro guardas
   criadas depois**, com o defeito real de que cada uma nasceu.
2. (Claude) `.assistant/README.md` ganhou tabela de navegação no topo — dez
   perguntas, dez âncoras — e seção nova sobre o notebook por objeto.

### Corrigido

1. (Claude) O quadro de status do README da raiz afirmava que `prophet_wrapper`
   "segue sem combinação funcional". A Sprint 8 mostrou que instala e ajusta um
   modelo completo.

### Removido

1. (Claude) `.assistant/GLOSSARIO.md`, absorvido como seção do
   `.assistant/README.md` conforme §5 do plano. Os cinco links foram reapontados
   para a âncora, e a validação pegou os que eu havia reapontado errado. O
   `--verify` da publicação pegou o que faltava: o arquivo continuava no
   workspace depois de removido da fonte.

### Notas

- **A seção nova sobre os notebooks era o buraco maior.** Nenhum dos dois READMEs
  mencionava que os 58 objetos têm, cada um, um `exemplo_*` na própria pasta —
  que é o que esta fase inteira produziu, e o que um recém-chegado precisa saber
  antes de qualquer outra coisa.
- Contrapartida registrada: o `.assistant/README.md` foi a 494 linhas. Glossário
  é documento de consulta por termo e README é leitura linear; a mesa de
  navegação no topo é o que evita que a fusão piore os dois.

## 2026-08-17 — auditoria da Sprint 9: 13 achados, e o HTML que ninguém lia

Rodada em sessão sem contexto. O auditor **imprimiu e leu o HTML que as funções
devolvem** em vez de aceitar a prosa — foi de onde saíram os quatro achados mais
graves, todos aprovados pelos dois portões. Detalhe em
`docs/sprints/sprint-9-constants-visual-display.md`.

### Corrigido

1. (Claude) `exemplo_dataframe_styled` fazia **três** afirmações erradas sobre a
   função: que ela destaca as colunas pedidas, que há gradiente, e que o realce é
   por coluna. O HTML devolvido tinha zero células destacadas — a regra é realçar
   valor **negativo** dentro das colunas declaradas, e a fixture não tinha
   negativo. Corrigido com coluna de negativos, e o `format_dict` com `"{:,.0f}"`
   (separador americano) trocado por `fmt_int`.
2. (Claude) `exemplo_section_header` dizia que o estilo vem de
   `constants.styles`. O CSS está inline no módulo, e `STYLE_SECTION_HEADER` não
   é usado por ninguém — editá-lo não muda cabeçalho nenhum.
3. (Claude) `exemplo_badge` usava o par 62/68 para explicar a política de corte.
   Os cortes reais são 80 e 50; `badge_score(68)` sai amarelo.
4. (Claude) O bloco de saída do `theme_plotly` mostrava dez cores; a execução
   imprime oito, porque o `print` corta em 88 caracteres. A afirmação era
   verdadeira e a evidência ao lado dela, fabricada. Célula nova imprime
   `len(colorway)` e a lista inteira.
5. (Claude) A docstring de `format_br` errava `fmt_delta(..., "bps")` por um
   fator de dez — dentro do módulo cujo notebook auditava essa exata armadilha.
6. (Claude) `exemplo_correlation_matrix` dizia "é `toPandas()` por baixo"; o
   módulo não chama `toPandas()`. O cálculo é distribuído e o custo cresce com
   colunas, não com linhas — amostrar ali perde precisão de graça.
7. (Claude) `display_styled` usava `Styler.applymap`, removido no pandas 3.0.
   Passou a `getattr(styled, "map", ...)` com fallback, sem mudar comportamento
   no 1.5.3 do Free.
8. (Claude) Seis dos treze blocos de saída eram transcrição editada. Refeitos
   literais; onde a saída é longa, o corte está declarado.

### Adicionado

1. (Claude) `PLANO_HUB.md` §12.2: inventário único da cor redeclarada fora de
   `constants.colors`. Eu havia registrado **2 de 12** módulos e chamado de
   contraexemplo positivo um que também copia. A tabela separa **cópia idêntica**
   (onze — unificar é higiene, sem efeito visual) de **valor divergente** (um,
   `ml/curves_plotly`, que é a única decisão de produto).
2. (Claude) Coluna `Dep.` na tabela de exploração do `CATALOGO_HELPERS.md`, com
   `dataframe_styled` e `explainability_report` marcados `exec`. O catálogo é o
   índice que as skills mandam consultar, e não marcava nenhuma das duas
   dependências escondidas.
3. (Claude) Contraste medido em `exemplo_colors`: **duas das quatro cores
   semânticas reprovam o mínimo AA com texto branco** — `COR_ALERTA` em 1,73:1 e
   `COR_POSITIVO` em 2,04:1. A regra ficou registrada: as duas são cor de
   preenchimento, nunca fundo para texto branco.

### Notas

- **A biblioteca tem 58 objetos** (51 `hub_snippets` + 7 `hub_scripts`). O "60"
  do validador soma os 2 exemplares de `hub_padroes`, que são template.
- `constants/styles` **não é importado por ninguém**, e suas oito constantes são
  cópia byte a byte de CSS que vive inline em cinco outros módulos. O arquivo
  inteiro é um espelho morto.
- **Ponto cego declarado:** nada do que é pixel foi verificado. O candidato mais
  provável a defeito escondido é a colisão entre o rodapé e a legenda do
  `theme_plotly` — anotação em `y=-0.18`, legenda em `y=-0.25`. Precisa de olho
  humano no notebook aberto.

## 2026-08-17 — Sprint 9: a biblioteca inteira convertida

Os 13 objetos de `constants`, `visual` e `display` viraram pasta de objeto, com
notebook que mostra o valor e o efeito renderizado. Com eles, **os 60 objetos da
biblioteca estão convertidos**. Relatório em
`docs/sprints/sprint-9-constants-visual-display.md`.

### Adicionado

1. (Claude) 13 pastas de objeto, com `__init__.py` gerado por
   `tools/api_publica.py` e notebook `exemplo_*`. Os 13 executaram como job:
   13 de 13 SUCCESS.

### Corrigido

1. (Claude) `exemplo_dataframe_styled` passou a instalar `jinja2`. **Segundo caso
   de dependência escondida** da biblioteca: o módulo não a importa, ela entra
   por `DataFrame.style`, que o pandas delega na hora da chamada. O primeiro foi
   o `tabulate`, por `to_markdown()`. Dois casos deixam de ser coincidência, e o
   padrão está registrado em `requirements-optional.txt`.
2. (Claude) `exemplo_correlation_matrix` foi para o bloco canônico: o módulo usa
   a API clássica de `pyspark.ml` (`VectorAssembler`, `Correlation.corr`), que o
   Spark Connect não expõe. Importa normalmente; falha ao instanciar.

### Notas

- **Três definições de "verde de selo" na mesma biblioteca**, expostas pela
  conversão: `constants.colors` (`VERDE = #8DC63F`), `constants.styles`
  (`STYLE_BADGE_OK`, hex copiado) e `visual.badge` (`#2E7D32`, cor diferente das
  outras duas). E `constants.styles` não tem uma linha de `import` — repete
  `#005CA9` e `#F8F9FA` em vez de puxar de `colors`, de modo que uma mudança de
  identidade visual não alcançaria os cabeçalhos. `visual.theme_plotly` é o
  contraexemplo positivo: importa `PALETA_CATEGORICA` de verdade. Cada caso
  registrado no notebook do objeto; unificar é etapa 2.
- `constants.format_br`: `fmt_delta` espera **razão**, não pontos percentuais,
  apesar da unidade "pp". Passar `2.4` pensando em "2,4 pp" devolve `+240,0 pp`.
  Encontrado ao escrever o próprio exemplo, que na primeira versão passava 2.4.
- Terceira variação do mesmo tema nesta fase — **importável não é executável** —,
  agora com três causas distintas: biblioteca ausente (`tabulate`), dependência
  delegada (`jinja2`) e API da plataforma (`pyspark.ml` no Spark Connect).

## 2026-08-17 — auditoria da Sprint 8: 13 achados, e uma correção que estava no lugar errado

Rodada em sessão sem contexto. O auditor executou os 14 notebooks em vez dos 5
pedidos e escreveu sondas próprias para testar as afirmações em vez de aceitá-las.
Treze achados, todos procedentes. Detalhe em
`docs/sprints/sprint-8-ml-dependencia-opcional.md`.

### Corrigido

1. (Claude) `ml/train_catboost` passou a definir `allow_writing_files=False` **no
   módulo**. A correção do efeito colateral estava no notebook, via
   `params_override` — o notebook parou de escrever, o `--verify` deu limpo, e a
   biblioteca continuou com a mina armada para qualquer outro chamador. As skills
   recomendam o módulo por caminho de import.
2. (Claude) `exemplo_autoencoder_anomaly` mandava o leitor para
   `isolation_forest`, "que acerta bem mais". Medido sobre a mesma fixture, o
   Isolation Forest tem **metade** da precisão (11,5% contra 23,5%) e metade da
   cobertura. A impressão vinha do notebook do outro objeto, cuja fixture é de
   anomalia grosseira de escala. A comparação foi substituída pelos números
   medidos, com a explicação de por que os dois cenários não se comparam.
3. (Claude) `exemplo_shap_explainer` ensinava que `max_samples=800` limitava o
   custo. O parâmetro só age em `model_type="kernel"`; o notebook chama com
   `"tree"`, e o TreeSHAP roda sobre a base inteira. O docstring do módulo estava
   certo — a prosa do notebook é que invertia.
4. (Claude) `exemplo_lgbm_ranker` lia NDCG@1 como taxa de acerto do topo. É razão
   de ganho: um ranker que nunca acerta o topo tira 0,4286 nessa escala, e o
   0,9548 obtido corresponde a ~92% de acerto, não 95%.
5. (Claude) Quatro notebooks — `kaplan_meier`, `optuna_lgbm`, `shap_explainer` e
   `umap_viz` — traziam uma seção inteira sobre `log_mlflow=False` e declaravam
   "Escrita: nenhuma" com base nele. Nenhum dos quatro módulos importa mlflow.
   Bloco copiado dos dez treinadores para quatro objetos que não treinam.
6. (Claude) `exemplo_train_lgbm` afirmava que nenhum dos nove parâmetros era o
   padrão do LightGBM; três são. `exemplo_lgbm_ranker` dizia que os NDCG "sobem
   de @1 para @10" citando uma série que desce na primeira transição — a
   não-monotonicidade virou o ponto.
7. (Claude) `requirements-optional.txt`: o mecanismo do pin do `shap` estava
   errado e citava a mensagem de erro do outro caso. O real é que ele arrasta
   numpy 2.4.6 sobre o 1.23.5 do runtime. E o custo de instalação, declarado como
   "~3 min" nos 14, erra por 4 a 6× em 11 deles — são dois grupos, torch (~5 min)
   e o resto (~1 min).

### Atualizado

1. (Claude) `check_saida_colada` passou a exigir substância no bloco — dígito ou
   trinta caracteres. Aceitava bloco vazio. O limite preserva o caso legítimo do
   `safe_display`, que cola um `RuntimeError` sem um número sequer.
2. (Claude) A exceção do `AZUL_CAIXA` passou a ser visível onde a regra é
   enunciada (`CLAUDE.md`) e no código da guarda, apontando para `PLANO_HUB` §2.2.
   Sem renomeação: é decisão registrada em 16/08.
3. (Claude) `PLANO_HUB.md` §12.1, nova: a dívida dos 12 notebooks sem saída
   colada, com caminho e sprint de origem de cada. Vivia só na narrativa, e o
   comentário no código a atribuía inteira à Sprint 6 — são 1, 4 e 6.

### Notas

- **Seis dos catorze blocos de saída são transcrições editadas**, não literais:
  omitem linhas, reordenam, renomeiam colunas. Num deles a curadoria removeu
  justamente as linhas que contradiziam a prosa. Nenhuma guarda estática
  distingue bloco editado de bloco inventado; o limite está dito no docstring.
- O auditor confirmou intacto o que mais custaria: converter é mover cumprido nos
  14, `__init__.py` gerados, pins corretos, limpeza remota, e **os números
  colados conferindo nos 14** — nenhum inventado.

## 2026-08-17 — Sprint 8: `ml` inteira convertida, e os 14 demonstram

Os 14 módulos com dependência opcional viraram pasta de objeto, com notebook
próprio que **instala a biblioteca e executa**. Com isso a seção `ml` fica
completa: 30 objetos. Relatório em
`docs/sprints/sprint-8-ml-dependencia-opcional.md`.

### Adicionado

1. (Claude) 14 pastas de objeto em `hub_snippets/ml/`, com `__init__.py` gerado
   por `tools/api_publica.py` e notebook `exemplo_*` com `%pip install` na
   primeira célula. Os 14 executaram como job: 14 de 14 SUCCESS.

### Corrigido

1. (Claude) `exemplo_train_catboost` passou a exigir
   `params_override={"allow_writing_files": False}`. Sem isso o CatBoost cria
   `catboost_info/` no diretório de trabalho — que no Databricks é a **pasta do
   notebook** —, e a primeira execução deixou dez arquivos de log publicados
   dentro de `.assistant`. Quem apanhou foi o `--verify` da publicação.

### Notas

- **O portão novo funcionou, e os erros mudaram de classe.** O
  `check_contrato_de_entrada`, criado na auditoria da Sprint 7, aprovou os 14, e
  nenhum dos três erros que apareceram na execução era de assinatura: dois eram
  de **aridade de retorno** (`prophet_wrapper` e `arima_wrapper` devolvem três
  elementos, não dois) e um era regra de domínio validada em runtime
  (`shap_explainer` recusa escolher a classe a explicar). Acerto de primeira
  execução subiu de 10/16 na Sprint 7 para 11/14 aqui.
- Três notebooks registram resultado que contraria o esperado, e ficam assim:
  `autoencoder_anomaly` acerta 19 de 81 marcados e o notebook diz que foi mal;
  `prophet_wrapper` ajusta com MAPE de 1,02% e devolve um componente `trend`
  negativo que não descreve a série — registrado como achado, sem explicação
  inventada; `arima_wrapper` escolhe (0,1,0), que é a resposta honesta.
- Os 7 `OPTIONAL_MISSING` do smoke test continuam e devem continuar: ele importa
  sem instalar, que é o comportamento de quem só faz `from hub_snippets.ml...`.

## 2026-08-17 — as 14 dependências opcionais instalam e rodam no Free

Levantamento feito antes da Sprint 8, para saber quantos dos 14 módulos com
dependência opcional conseguiriam demonstrar de verdade. A resposta mudou o
desenho da sprint: **todos**.

### Atualizado

1. (Claude) `hub_snippets/requirements-optional.txt` reescrito com o inventário
   verificado em 2026-08-17. As 12 bibliotecas foram instaladas por `%pip` e
   **exercitadas com chamada real** — ajuste de modelo, projeção, previsão —,
   não apenas importadas. Custo: 200 a 280 segundos de job.
2. (Claude) `.claude/rules/free-vs-trabalho.md`: a linha "bibliotecas ML
   opcionais ausentes" passou a "ausentes do runtime, mas instaláveis na sessão",
   com as três regras que custaram um ambiente quebrado.
3. (Claude) `PLANO_HUB.md`: a Sprint 8 deixa de produzir 14 notebooks que só
   documentam.

### Corrigido

1. (Claude) `prophet` estava registrado como **"sem combinação funcional
   conhecida"** — falhava com `'Prophet' object has no attribute 'stan_backend'`
   — e o plano o listava como fora de escopo, a documentar sem resolver. Em
   17/08 instalou sem pin e ajustou um modelo completo, com previsão de 7 dias.
   O impedimento não existe mais.
2. (Claude) O arquivo mandava fixar `numpy==1.26.4` sempre, por precaução. O
   runtime traz **1.23.5**, e o pin gera conflito em vez de evitar. Também não se
   reproduziu o aviso de que `%pip` antes do primeiro comando Spark abortaria a
   execução.

### Notas

- **Três bibliotecas exigem pin**: `shap==0.44.1` (sem ele, sobe versão que
  espera numpy 2.x e quebra no import), `umap-learn==0.5.5` e `pmdarima==2.0.4`
  (esta com `numpy==1.23.5` na mesma linha). As outras nove resolvem sozinhas.
- **Instale uma por notebook.** As três acima, juntas na mesma sessão, derrubam o
  `import numpy` do próprio notebook: `numpy.dtype size changed, Expected 96 from
  C header, got 88`. Isoladas, funcionam.
- Segunda vez no mesmo dia em que um registro de teste de 14/08 se mostrou
  desatualizado — uma vez para pior (MLflow deixou de abrir run), uma para melhor
  (Prophet passou a funcionar). Reforça a linha da regra: **"foi testado" tem
  data de validade em ambiente gerenciado.**

## 2026-08-17 — auditoria da Sprint 7: 12 achados e duas guardas novas

Rodada em sessão sem contexto, com instrução para executar e com `git show`
liberado para recuperar a versão anterior de cada módulo. Doze achados, todos
procedentes. Relatório completo em `docs/sprints/sprint-7-ml-nucleo.md`.

### Adicionado

1. (Claude) `check_contrato_de_entrada` em `tools/validate_assistant.py`: confere
   por AST o que o notebook **passa** contra a assinatura do módulo — kwarg
   inexistente, posicional a mais, obrigatório omitido. Era a direção sem portão
   nenhum, e por onde entraram seis dos dezesseis defeitos da sprint. Provado com
   os três defeitos reais reinjetados num sandbox; 0 achados no repositório.
2. (Claude) `check_saida_colada` (**aviso**): cobra do notebook um bloco
   ```text com a saída real. Só 6 de 24 tinham; hoje são 22 de 34.
3. (Claude) Seção 4 em `exemplo_drift_detection`, com a política de limiar
   declarada, e o caso de fronteira registrado — `uf` sai 0,250667 contra um
   limiar de 0,25 e dispara alarme por seis milésimos.

### Corrigido

1. (Claude) `exemplo_lgbm_temporal` ensinava a contar nulos por entidade como
   assinatura de lag correto. A função termina com `dropna()` e devolve zero
   nulos sempre; e a chamada do notebook, com a janela móvel no padrão
   `[3,6,12]` sobre 12 meses, devolvia **zero linhas**. O job reportava SUCCESS.
   A demonstração foi refeita sobre contagem de linhas removidas — 9 com
   `entity_cols`, 3 sem — e mostra o lag de B recebendo 898,2, valor de C.
2. (Claude) `exemplo_metrics_report` mandava comparar `accuracy`, que
   `calculate_binary_metrics` não devolve. Leitura reescrita em torno de
   `prevalence`.
3. (Claude) `exemplo_mlflow_run` usava o bloco canônico com motivo que o template
   proíbe ("decisão de escopo, não impedimento técnico"). Ao executar, apareceu
   impedimento real — ver Notas.
4. (Claude) `exemplo_split_temporal`: 60 das 720 linhas somiam sem menção;
   `gap_periods` explicado. `exemplo_score_bands`: pede 5 bandas e recebe 4, por
   colapso de quantis com 26,8% da base empatada no piso. `exemplo_curves_plotly`:
   prevalência 0,0185, não 0,02.
5. (Claude) Título e tabela órfãos em `exemplo_woe_iv_calculator` e
   `exemplo_split_temporal`, resíduo do desmembramento dos notebooks de trânsito.
6. (Claude) `scikit-learn` registrado em `requirements-optional.txt`: entra por
   `mlflow.sklearn`, que `import mlflow` não traz.

### Notas

- **Diferença Free × trabalho nova, e uma lição de método.** Nenhum run do MLflow
  abre no serverless do Free: `mlflow.start_run` instancia um `MlflowClient` que
  lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config. O mesmo
  caminho foi testado e **passou em 14/08/2026** — `docs/testes/spark/resultados/`
  registra `mlflow_run.completo` como "run completo aceito". Três dias, mesmo tipo
  de compute, resultado oposto. O registro de 14/08 não está errado; o runtime
  mudou. Linha nova na matriz de `.claude/rules/free-vs-trabalho.md`, com a
  conclusão: **"foi testado" tem data de validade em ambiente gerenciado.**
- Dívida declarada: 12 notebooks das Sprints 1, 4 e 6 seguem sem saída colada.
  A guarda os lista a cada execução.

## 2026-08-17 — reestruturação para Hub: Sprints 0 a 7

Execução do `PLANO_HUB.md`, iniciada em 16/08. Esta entrada cobre as oito sprints
concluídas até aqui em bloco, e não uma por uma: o registro detalhado de cada uma
está em `docs/sprints/`, e o estado de cada sprint, com data e auditoria, em
`PLANO_HUB.md` §12. **Foi um lapso de processo não registrar sprint a sprint** —
o CHANGELOG ficou dois dias atrás da execução, contrariando a regra do projeto.

### Adicionado

1. (Claude) `.assistant/hub_padroes/` — seis tipos de template (readme, snippet,
   script, prompt, skill, notebook) com exemplo executável em
   `taxa_resposta_campanha/`. Sprint 1.
2. (Claude) `tools/api_publica.py`: extrai a API pública por AST e gera o
   `__init__.py` da pasta de objeto. A regra é exaustiva, não curada.
3. (Claude) `tools/notebook_marker.py`: detecção canônica de notebook, tolerando
   BOM, linha em branco e comentário de encoding, usada pela publicação e pelo
   smoke test.
4. (Claude) `check_pastas_de_objeto` e `check_contrato_de_dados` em
   `tools/validate_assistant.py`. O segundo compara o que o módulo **produz** com
   o que o notebook **consome**; nasceu de um caso real em que o notebook filtrava
   `status != 'ok'` sobre uma coluna que devolve emoji.
5. (Claude) `docs/decisions/ADR-0006-identidade-hub.md`, com a tabela de
   correspondência `x_*`/`rodrigo-*` → nomes atuais, referenciada pelos dez
   documentos datados que preservam a nomenclatura da época.
6. (Claude) 31 notebooks `exemplo_<objeto>.py`, todos executados como job no
   laboratório: 7 em `hub_scripts` (Sprint 4), 8 em `spark`/`testing` (Sprint 6),
   16 em `ml` (Sprint 7).

### Atualizado

1. (Claude) Prefixo `x_` → `hub_`, e as 12 skills `rodrigo-<tema>` →
   `hub-ml-<tema>`. Regra de nomenclatura: underscore onde o Python importa,
   hífen onde a plataforma nomeia. Sprints 2 e 3.
2. (Claude) `hub_snippets` e `hub_scripts` passaram de arquivo plano a **pasta por
   objeto** (`__init__.py` + módulo + notebook). 31 dos 58 objetos convertidos.
3. (Claude) `tools/publicar_free.py`: detecção de diretório obsoleto,
   `--verify` rápido, e `.assistant/.mcp_servers.json` tratado como arquivo
   gerido pela plataforma.
4. (Claude) `tools/spark_smoke_test.py`: pula notebook no `walk_packages` —
   objetos NOTEBOOK aparecem como `.py` no mount `/Workspace`, o que foi
   verificado com job de sonda — e descobre `hub_scripts` automaticamente.

### Corrigido

1. (Claude) Três notebooks didáticos estavam quebrados desde 14/08: a auditoria da
   biblioteca renomeou chaves de retorno (`cobertura_pct` →
   `cobertura_pct_linhas_validas`, entre outras) e o material didático não
   acompanhou. Encontrado ao executar, não ao ler.
2. (Claude) `hub_scripts/naming_checker` usava `spark` sem importar pyspark — o
   mesmo `NameError` que a documentação declarava eliminado.
3. (Claude) 38 links relativos quebrados pela renomeação, por substituição que
   descartava a profundidade do caminho; refeitos com `os.path.relpath`.

### Removido

1. (Claude) `x_projects/`, `x_docs/` e `x_config/`, com o conteúdo aproveitável
   realocado. Sprint 2.
2. (Claude) `hub_snippets/_notebooks_a_migrar/`, pasta de trânsito criada na
   Sprint 2 para que a renomeação não apagasse o insumo das Sprints 6 e 7. O
   último dos quatro notebooks originais foi desmembrado nesta sprint.

### Notas

- **Dependência escondida.** `ml/explainability_report` está classificado como
  núcleo — não tem `import` de biblioteca opcional e o smoke test o importa com
  `PASS` —, mas não executa no laboratório: usa `DataFrame.to_markdown()`, que o
  pandas delega ao `tabulate`, ausente no runtime. Registrado em
  `hub_snippets/requirements-optional.txt`. A divisão 16/14 entre as Sprints 7 e 8
  é exata sobre importabilidade, não sobre executabilidade.
- Auditorias em sessão sem contexto ao fim das Sprints 1, 2, 4 e 3+6: 21, 13, 9 e
  13 achados, todos procedentes e corrigidos. A da Sprint 7 está pendente.
- `PALETA_CATEGORICA` tem 6 cores em `ml.curves_plotly` e 10 em
  `constants.colors`; duas das três cópias são idênticas à original, o que esconde
  a divergente. Registrado no notebook do objeto; unificar é decisão de produto.

## 2026-08-15 — segunda auditoria da documentação e 25 correções

Rodada independente sobre os **15 READMEs** do repositório, sete deles auditados
pela primeira vez. Ao contrário da rodada anterior, esta pediu que o auditor
**executasse** os procedimentos documentados em vez de apenas lê-los, e que
comparasse cada README com o conteúdo real da pasta que ele descreve. Os dois
achados mais caros vieram exatamente daí. Registro em
`docs/auditoria/2026-08-15_documentacao-rodada2/`.

### Corrigido — proteções que não cobriam o que prometiam

1. (Claude) `check_repo_corporate` varria a partir de `Path(".")`, não da raiz do
   repositório. Rodado de `tools/`, varria 4 arquivos em vez de 409 e devolvia
   `APROVADO: 0 falha(s), 0 aviso(s)` — a proteção do ADR-0003 desligava em
   silêncio conforme o diretório de onde o comando fosse chamado. A raiz passou a
   vir de `Path(__file__).resolve().parents[1]`, e **varredura vazia agora
   reprova**. O padrão foi ampliado de três alternativas para matrícula genérica
   (letra + 6 a 8 dígitos), domínio corporativo e domínio bancário, verificado
   sem falso positivo no repositório atual. O `README.md` deixou de prometer
   cobertura genérica e passou a apontar `CORPORATE_RE` como dona da lista.
2. (Claude) A validação só checava links relativos dentro de `--root`
   (`ambiente_fonte` por padrão), enquanto o `README.md` a apresentava como rede
   que "reprova link quebrado". `README.md`, `docs/` e `.claude/` — 156 links —
   nunca foram verificados. Novo `check_repo_links` cobre o repositório fora da
   raiz analisada; nenhum link quebrado encontrado. O texto passou a dizer que
   não há hook nem CI: a rede só existe quando alguém a aciona.
3. (Claude) `publicar_free.py --verify` filtrava `object_type != "DIRECTORY"`, e
   por isso não enxergava diretório órfão. Havia um caso vivo: `x_projects/archive`,
   vazio, não versionado e publicado no workspace. A conferência passou a comparar
   também os diretórios; `archive/` foi removido da fonte e do workspace.

### Corrigido — procedimento documentado que não executa

1. (Claude) O passo 4 da "Primeira hora" mandava rodar quatro comandos "logo
   abaixo", e o bloco do render aparecia **sem `--write`**. Quem copiasse os
   blocos na ordem publicaria o espelho anterior e receberia `APROVADO` na
   conferência, que compara workspace contra espelho e nunca contra a fonte. Os
   quatro comandos passaram para dentro do passo 4, com `--write` e a explicação
   do porquê a conferência não acusaria o erro.
2. (Claude) `README.md` mandava instalar a CLI com `pip install databricks-cli`,
   que é a CLI legada — parada na 0.18, desaconselhada pela própria Databricks,
   sem `auth login` nem `current-user`, e capaz de sombrear o binário correto no
   PATH em Windows. Substituído por `winget` e pelo instalador oficial, com
   `databricks --version` ≥ 0.200 como pré-requisito conferível.
3. (Claude) O comando de reexecução do smoke test estava marcado como PowerShell
   mas passava JSON entre aspas simples: o shell remove as aspas duplas antes de
   o executável recebê-las. Trocado por here-string.

### Corrigido — código

1. (Claude) `x_scripts/naming_checker.py` referenciava o global de notebook
   `spark` sem importar `pyspark` — o mesmo `NameError` que `docs/testes/spark/`
   declarava eliminado em todos os scripts. Ele nunca esteve no smoke test, então
   nunca foi importado no runtime, e a validação estática não pega porque o
   arquivo é sintaticamente válido. Corrigido; varredura por AST confirmou que
   nenhum outro módulo de `x_snippets` ou `x_scripts` usa o global.

### Corrigido — contradições entre documentos

1. (Claude) `CLAUDE.md` listava o ADR-0002 (engine do Hub) como decisão **ativa**,
   revogada pelo ADR-0005 desde então, e omitia os ADRs 0004 e 0005.
2. (Claude) `.claude/CLAUDE.md` mandava "não invente que já existem" sobre
   `publicar-free`, `forward-test-skills` e `replicar-trabalho` — as três no
   disco, com frontmatter válido e listadas como ativas em `skills/README.md`.
   Como é o primeiro arquivo que toda IA lê, a instrução fazia uma IA nova
   recusar-se a usar ferramenta existente ou reconstruí-la.
3. (Claude) `docs/testes/spark/README.md` afirmava que `requirements-optional.txt`
   traz o conjunto que funciona e, 45 linhas depois, que ele "lista nomes sem
   versão" e não é instalável — resíduo de antes de o arquivo ser pinado.
4. (Claude) `ROADMAP_SKILLS.md` mantinha em aberto dois gates fechados (Spark
   64/71 e forward tests 36/36), e `x_docs/README.md` mandava o leitor lá
   justamente para saber "gates pendentes". Marcados, com o status apontando para
   o README da raiz em vez de duplicá-lo.

### Corrigido — índices que negavam o próprio conteúdo

1. (Claude) `docs/auditoria/README.md` dizia "nenhuma auditoria formal registrada
   ainda" com duas pastas de auditoria ao lado. Tabela preenchida com as três.
2. (Claude) `docs/handoffs/README.md` declarava-se vazio enquanto guardava, dentro
   de um bloco rotulado "exemplo", os dois únicos itens de vigilância abertos do
   projeto — incluindo um que não existe em nenhum outro lugar do repositório.
   Promovido a `2026-08-14_calibracao-descriptions.md` e registrado na tabela; o
   README ficou com esqueleto genérico.
3. (Claude) O mapa do repositório no `README.md` omitia `docs/testes/`, que guarda
   a evidência dos dois gates da fase 3.

### Corrigido — fatos e mecanismos

1. (Claude) `README.md` declarava as dependências opcionais pendentes de fixação
   ("7 módulos ML") quando 13 dos 14 já haviam executado com as versões pinadas;
   só `prophet_wrapper` segue sem combinação funcional.
2. (Claude) `README.md` agrupava `x_projects/` sob "adicionar com `@`/Add context",
   que é falso e é exatamente o engano que `x_projects/README.md` existe para
   desfazer: arquivo que fique nessa pasta nunca é descoberto — é preciso copiar
   o template como `AGENTS.md` na raiz do projeto real.
3. (Claude) `x_scripts/README.md` documentava o contrato anterior à correção
   ("`spark` deve existir no ambiente"), ensinando a aceitar como normal o defeito
   que o projeto eliminou.
4. (Claude) A árvore de `x_projects/README.md` listava 3 das 5 entradas da pasta,
   e o exemplo de `quick_profile` chamava com `sample_fraction=0.05` sobre uma
   saída capturada com fração 1.0.
5. (Claude) O gate do forward test declarava 36/36 sem a ressalva que o próprio
   resultado registra: `11N-r2` passou em sentido fraco.

### Adicionado

1. (Claude) Bifurcação de leitores no `README.md`: usar, contribuir ou assumir o
   projeto. O percurso inteiro era escrito para quem contribui, e o analista que
   só vai usar o ambiente publicado não tinha caminho — o passo 4 o convidava a
   escrever no workspace na primeira hora.
2. (Claude) Diagrama dos três gates (validação estática, Spark, forward test) com
   o que cada um prova e **não** prova, e a fronteira que nenhum deles alcança.
3. (Claude) Sete verbetes no glossário, todos usados sem definição em documentos
   que remetem o leitor a ele: *event log*, *target (de bundle)*, *autologging*,
   *PII*, *LambdaRank/NDCG*, *auditoria do Codex* e `run_governado`. O primeiro
   aparecia em 3 documentos; o penúltimo, em 7.
4. (Claude) Separação entre automático e manual no checklist de pré-publicação de
   `.assistant/README.md`: oito itens viram um comando, e sobram os três que
   exigem uma pessoa.

### Atualizado

1. (Claude) Ordem de `docs/testes/spark/README.md`: a legenda dos três estados
   (`PASS`/`OPTIONAL_MISSING`/`FAIL`) subiu para junto da tabela que os usa, 80
   linhas acima de onde estava.
2. (Claude) A explicação de por que existem duas pastas deixou de ser duplicada
   no `README.md`; `ambiente_fonte/README.md` passou a ser a dona.
3. (Claude) Gênero de "Genie Code" padronizado no masculino em 16 arquivos — a
   forma feminina aparecia em 6 dos 15 READMEs.

### Descoberto durante a correção

1. (Claude) **A plataforma escreve dentro de `.assistant/`.** Abrir o painel de
   MCP em Genie Code → Settings materializa
   `/Users/<username>/.assistant/.mcp_servers.json` com a lista de conectores
   internos (observado em 2026-08-15). Sem tratamento, o `--verify` recém-corrigido
   classificaria um arquivo gerenciado pela plataforma como obsoleto e mandaria
   apagá-lo. Passou a ser reconhecido e reportado à parte. Registrado em
   `.claude/rules/genie-code-oficial.md` com a inversão que importa: o arquivo é
   **saída** da configuração, nunca entrada — criá-lo à mão não configura nada, o
   que preserva a afirmação original da regra.

## 2026-08-14 — auditoria da documentação e 22 correções

Rodada independente sobre os oito READMEs e o glossário, com o auditor tendo
acesso ao sistema de arquivos e à CLI — o que permitiu verificar afirmações
contra o código e contra o workspace, em vez de apenas contra o próprio texto.
Registro em `docs/auditoria/2026-08-14_documentacao/`.

### Corrigido — fatos falsos

1. (Claude) Os blocos de saída do `README.md` estavam desatualizados em três dos
   cinco números, e o texto mandava tratar divergência como diagnóstico. Um
   leitor novo concluiria que seu ambiente está quebrado com o repositório
   aprovado — o inverso do propósito da seção. Números regenerados e a promessa
   trocada: as linhas de contagem são voláteis, o que importa é o `APROVADO`.
2. (Claude) O bloco do `--verify` mostrava 165 arquivos contra 174 reais, e
   omitia a primeira linha da saída — ou seja, havia sido editado à mão logo
   acima da frase que afirmava o contrário. Corrigido e a afirmação ajustada.
3. (Claude) Glossário dizia que **Add context** é a "única forma" de usar
   `x_prompts` e `x_docs`, contradizendo o próprio glossário e outros três
   documentos: `@` também funciona.
4. (Claude) Contagem do smoke test divergia entre documentos (71 e 64). São
   coisas diferentes — 71 verificações, 64 aprovações — e agora está explícito.
5. (Claude) `x_config/README.md` dizia "o único arquivo desta pasta" havendo
   também o próprio README.

### Corrigido — afirmações sobre o próprio sistema

1. (Claude) O `README.md` garantia verificação automática de identificador
   corporativo "inclusive em nome de pasta", mas o validador só cobria
   `ambiente_fonte/` — e o vetor descrito no ADR-0003 se materializa em
   `Novo_Ambiente_Simulado/`, que é versionado. **A guarda foi estendida**:
   `check_repo_corporate` varre o repositório inteiro, conteúdo e caminho,
   buscando apenas padrão corporativo (o username pessoal do laboratório é
   estado aceito). O texto passou a descrever a cobertura real.
2. (Claude) Diagrama e nota de rodapé atribuíam a publicação ao engine do Hub,
   decisão revertida pelo ADR-0005 e contrariada pelo próprio código.
3. (Claude) A camada squad aparecia como "fase 2" no diagrama e "Fase 5" na
   tabela — dois sistemas de numeração sem aviso.

### Adicionado

1. (Claude) Seção **"Antes de começar"** no `README.md`: o percurso mandava
   publicar sem nunca dizer que isso exige CLI instalada e autenticada, e a
   única menção a CLI no arquivo dizia que o workspace do trabalho não tem —
   sugerindo o oposto do pré-requisito. Agora há tabela de pré-requisitos,
   comandos de instalação e como confirmar.
2. (Claude) `x_docs/README.md`, que era a única extensão sem porta de entrada.
   Cinco arquivos dela não eram citados em documento nenhum, incluindo o
   `SKILL_TEMPLATE.md`. Inclui o procedimento de criar uma skill nova, que não
   estava escrito em lugar algum.
3. (Claude) Sete verbetes no glossário para termos usados sem definição:
   driver-side, bronze/silver/gold, expectations, readiness, runbook e AST.

### Atualizado

1. (Claude) FAQ movido para logo após o percurso inicial — respondia as dúvidas
   do primeiro dia e estava atrás de governança e roadmap.
2. (Claude) Os links dos notebooks didáticos quebravam no workspace, que é onde
   o documento é lido: lá os objetos são notebook e não têm extensão.
3. (Claude) O mermaid do guia sugeria que a skill carrega os helpers sozinha —
   exatamente o engano que o prefixo `x_` existe para evitar. Ganhou distinção
   entre automático e manual, com a ressalva explícita.
4. (Claude) Diagrama do `x_projects` mostrava o arquivo em `notebooks/` enquanto
   o texto dizia `modelos/churn/`, ensinando errado o único conceito da seção. O
   nó "fim da busca" afirmava um limite não documentado.
5. (Claude) `x_snippets/README.md` declarava que o catálogo é "a única lista
   mantida" e publicava a segunda lista logo abaixo. Agora a precedência está
   dita.
6. (Claude) A seção de fluxo de engenharia do guia descrevia pipelines que o
   leitor constrói, não a publicação deste pacote — que não usa bundle. Ganhou
   cabeçalho que separa as duas coisas.
7. (Claude) Contagens fixas restantes removidas da prosa.

### Não corrigido

- Números de teste citados na documentação (36/36, 64/71) não puderam ser
  reverificados pelo auditor, que não tinha acesso a `docs/testes/` por
  instrução. Permanecem como estavam, agora com a distinção entre verificações
  e aprovações explicitada.

## 2026-08-14 — auditoria da biblioteca e 13 correções

### Auditoria

1. (Rodrigo + Claude) Rodada de auditoria com Claude em sessão sem contexto,
   registrada em `docs/auditoria/2026-08-14_biblioteca-pit-join/`. Registrada
   como **A1, não A2**: o auditor é do mesmo modelo do implementador, então
   pontos cegos comuns permanecem. O gate para o trabalho segue exigindo uma
   segunda origem.
2. Resultado: 15 achados, **13 procedentes**, todos confirmados por leitura e
   depois reproduzidos em teste.

### Corrigido em `pit_join`

1. (Claude) `atraso_publicacao_dias` passa a ser **obrigatório**. Com o default
   zero e comparação inclusiva, um snapshot diário com data de referência igual
   à data da decisão entrava no resultado — vazamento sem erro, produzido pelo
   helper cuja razão de existir é evitá-lo.
2. (Claude) `janela_maxima_dias` comparava a **disponibilidade** em vez da
   referência, o que tornava a janela efetiva igual a `janela + atraso`. Um
   valor de 8 dias entrava sob janela de 3.
3. (Claude) Diagnóstico separava mal as ausências: chave nula, entidade sem
   histórico e feature indisponível na data caíam num número só, e a leitura
   natural levava a afrouxar o atraso — o movimento que reintroduz o vazamento.
4. (Claude) Empate de instante passa a **interromper por padrão**. O desempate
   anterior era determinístico mas enviesado: escolhia sempre o menor valor, o
   que em crédito é viés conservador sistemático, não escolha neutra.
5. (Claude) Encadear duas chamadas quebrava por colisão da coluna interna de
   disponibilidade, que agora não é devolvida por padrão.
6. (Claude) Contagem de `ts_feature` nulo, tipo do parâmetro validado, nomes de
   coluna protegidos por backticks e fuso da sessão reportado no diagnóstico.

### Corrigido em `join_diagnostics`

1. (Claude) Multiplicidade e relação eram medidas sobre o lado direito inteiro:
   uma chave que só existe à direita inflava a estatística e fazia o helper
   anunciar "1:N duplica" enquanto a expansão calculada dizia 1,0.
2. (Claude) Cobertura usava denominador com chave nula, enquanto os exemplos de
   órfãs as excluíam — a combinação "3 sem match, 0 exemplos" lia como defeito
   da ferramenta. Agora há cobertura sobre chaves válidas e contagem separada.
3. (Claude) Expansão passou a distinguir `left` de `inner`; contagens em passada
   única, para não produzir métricas incoerentes sobre fonte não determinística;
   amostra de órfãs ordenada; base vazia devolve expansão 1,0.

### Notas

- Os módulos haviam passado em 13 verificações de runtime escritas por quem os
  implementou, e **nenhuma delas pegou qualquer um dos treze achados**. As
  categorias que escaparam: ambiguidade semântica de tipo de data, interação
  entre parâmetros nunca combinados no teste, diagnóstico que agrega causas
  distintas, comportamento em escala, encadeamento e política de empate.
- Duas falhas foram introduzidas durante a própria correção e resolvidas:
  `conf.get(chave, default)` valida o default como configuração no Spark Connect
  e derruba a execução; e a fixture sorteava datas que podiam coincidir, criando
  empate acidental — a guarda nova o denunciou.
- Verificação final: **10 testes, um por achado, nenhuma falha**.
- Pendente para o ambiente do trabalho: o achado de escala (A5) recomenda hint
  de range-join, que exige `explain()` sobre volume representativo.

## 2026-08-14 — reformulação das instruções pessoais

### Corrigido

1. (Claude) **Duas instruções orientavam para comportamento que falha.** O
   arquivo pedia para preferir compute serverless e, adiante, para usar cache
   com benefício demonstrável — mas serverless recusa `cache()` e `persist()`,
   como o teste de runtime provou. E mandava instalar bibliotecas "conforme a
   documentação aplicável", quando instalar sem fixar versão derruba o kernel
   por alteração de pacotes core. Ambas substituídas pelo comportamento
   verificado.

### Adicionado

1. (Claude) Seção **Limites inegociáveis**, promovida ao topo, reunindo os vetos
   que estavam dispersos entre preferências de formatação: nada de afirmar
   execução sem evidência, escrita sem declaração prévia, vazamento temporal,
   PII exposta, heurística apresentada como norma, ou falha silenciada.
2. (Claude) Seção **Restrições verificadas do runtime**: serverless sem cache,
   `spark` global inexistente em módulo, autologging do MLflow ligado por
   padrão, necessidade de fixar versão, Python possivelmente anterior ao 3.12 e
   colisão dos wrappers no run ativo.
3. (Claude) Seção **Use a biblioteca antes de escrever**, a lacuna de maior
   custo: skills só valem quando carregadas, e conversas curtas frequentemente
   não carregam nenhuma. Nessas, o único guia ativo é este arquivo, que descrevia
   `x_snippets` como "pacote opcional" sem nunca pedir preferência por ele.
   Reescrever segue permitido — desde que declarado.
4. (Claude) Junção point-in-time e atraso de publicação passam a ser citados no
   anti-leakage, e diagnóstico de junção entra na validação de dados.

### Removido

1. (Claude) Manual dos diretórios `x_` (cerca de 1.400 caracteres): é referência,
   já está no README com mais detalhe, e custava em toda interação.
2. (Claude) Parágrafo esclarecendo que `/eda` e afins não são comandos — o hábito
   acabou junto com o ambiente antigo, apagado nesta mesma série de sessões.
3. (Claude) A contagem "as 12 skills" e demais números que envelhecem sozinhos.
4. (Claude) Procedimento que pertence às skills, onde já está melhor explicado.

### Verificação

Os três critérios de aceite declarados na proposta foram conferidos por script:
nenhuma instrução contradiz fato registrado em `docs/testes/spark/`; nenhuma
contagem, lista de pastas ou alias remanescente; e presença confirmada dos seis
temas que faltavam. Resultado: **7.056 caracteres**, contra 7.371 antes — menos
texto com o conteúdo crítico presente. Instruções não influenciam a seleção de
skill, então a certificação de roteamento 36/36 permanece válida sem reteste.

## 2026-08-14 — material didático, notebooks 03 e 04

### Adicionado

1. (Claude) `03_qualidade_de_juncao.py`: os quatro desfechos de um join —
   preserva, infla, encolhe e perde por chave nula — cada um com os números que
   o denunciam. Explica por que chave nula é contada à parte: em SQL `NULL`
   nunca casa com `NULL`, e a causa costuma ser outra (erro de extração, campo
   opcional) com correção também outra.
2. (Claude) `04_armadilhas_de_credito.py`: demonstra que somar taxas de
   inadimplência por safra exagera o acumulado, porque conta o mesmo contrato
   várias vezes — o erro que a auditoria do Codex corrigiu no ambiente anterior.
   E constrói uma variável deliberadamente vazada para mostrar que IV altíssimo
   é motivo de desconfiança, não de comemoração.
3. (Claude) Seção "Como se localizar" no `x_snippets/README.md`, ligando cada
   tipo de pergunta ao documento que a responde: inventário, catálogo por
   demanda, notebooks, skill do tutor e glossário.

### Notas

- Os quatro notebooks foram executados no Free antes da entrega; os dois novos
  passaram na primeira tentativa.
- O notebook 04 aproveita para reforçar, com exemplo, que faixas de IV e limites
  de PSI são referências e não normas — apresentá-las como exigência regulatória
  sem citar fonte é algo que as instruções do ecossistema proíbem.

## 2026-08-14 — material didático da biblioteca

### Adicionado

1. (Claude) `x_docs/notebooks/01_vazamento_temporal.py`: mostra o join ingênuo
   inflando a base e trazendo dado do futuro, e depois `pit_join` e
   `temporal_split` resolvendo. Executa sobre fixtures sintéticas e imprime a
   prova — zero linhas com score futuro no resultado.
2. (Claude) `x_docs/notebooks/02_drift_e_estabilidade.py`: constrói duas
   populações com **a mesma média** e formas opostas, para mostrar por que
   comparar média e desvio não é PSI. Reproduz o erro que existia no ambiente
   anterior e explica por que a interpretação exige limite calibrado.
3. (Claude) Inventário por módulo no `x_snippets/README.md`: uma linha para cada
   um dos 47 módulos, como visão do que existe. O catálogo continua sendo a
   visão por demanda; os dois papéis são distintos e não se repetem.

### Corrigido

1. (Claude) `tools/publicar_free.py` publicava **todo** `.py` como arquivo, o
   que está certo para a biblioteca e errado para material didático: notebook
   como arquivo não tem células para executar. A ferramenta passou a detectar o
   marcador `# Databricks notebook source` e reenviar esses arquivos como
   notebook; o `verify` confere os dois tipos separadamente.

### Notas

- Ambos os notebooks foram executados no Free antes de serem entregues. As duas
  falhas encontradas eram erros meus de escrita, não defeitos de módulo: import
  faltando e um DataFrame Spark passado a `temporal_split`, que opera em pandas.
- Esse segundo erro virou conteúdo: o notebook agora explica que definir split é
  decisão sobre metadados, não processamento de volume, e que o erro
  `Attribute 'copy' is not supported` não diz nada sobre a causa real.
- Decisão de escopo: notebook apenas onde o erro é caro e a lógica não é óbvia.
  Explicar `fmt_brl` linha a linha criaria manutenção sem ensinar nada. Para
  explicação sob demanda de qualquer módulo, a skill do tutor lê a versão atual
  do arquivo e não fica defasada.

## 2026-08-14 — biblioteca, fecho do sprint 0

### Notas

1. (Claude) **13 dos 14 módulos com dependência opcional verificados em
   runtime**, contra zero no início do dia. O conjunto de versões que funciona
   foi apurado e registrado em `x_snippets/requirements-optional.txt`, que antes
   listava nomes sem versão — e nessa forma não era instalável em serverless.
2. (Claude) `prophet_wrapper` permanece o único não verificado: falha com
   `'Prophet' object has no attribute 'stan_backend'` mesmo com autologging
   desligado e sem registro. O atributo não é usado pelo nosso código; ele deixa
   de existir quando o backend de inferência do Prophet não inicializa, o que
   indica incompatibilidade da biblioteca com o ambiente serverless. Fica
   marcado como não verificado em vez de presumido funcional.

### Corrigido

1. (Claude) `requirements-optional.txt` reescrito: pacotes core fixados no topo
   com a explicação do porquê, conjunto verificado com versões exatas, e o
   Prophet comentado com o motivo. Um inventário sem versões, num ambiente onde
   instalar sem fixar derruba o kernel, era instrução para quebrar o ambiente.

### Aprendizados de ambiente registrados

- O Databricks liga autologging do MLflow por padrão, e ele intercepta o `fit`
  mesmo quando o wrapper não registra nada — foi o que mascarou a falha do
  Prophet na primeira tentativa.
- `mlp_embeddings` espera uma lista de arrays, um por feature categórica, não
  uma matriz. A mensagem de erro do módulo já dizia isso com clareza.
- `tabnet_wrapper` e `arima_wrapper` só falhavam por colisão no run ativo do
  MLflow; isolados, executam normalmente.

## 2026-08-14 — biblioteca, endurecimento do pit_join

### Corrigido

1. (Claude) **Escolha indeterminada em empate de instante.** Duas versões da
   feature publicadas no mesmo momento deixavam o desempate a cargo do plano de
   execução: o mesmo código podia devolver valores diferentes entre execuções, o
   que quebra reprodutibilidade sem emitir erro. Passou a haver desempate
   determinístico, e o diagnóstico reporta `linhas_com_empate_de_instante` —
   empate costuma indicar duplicidade na fonte e não deveria passar silencioso.
2. (Claude) **Identificador sintético de linha eliminado.**
   `monotonically_increasing_id` não tem estabilidade garantida entre
   recomputações, e era usado para particionar a janela. A resolução passou a
   ser por par (chave, instante de decisão) distinto, com junção de volta. O
   desenho novo também corrige o caso de duas decisões da mesma entidade no
   mesmo instante — legítimas, por exemplo para produtos diferentes —, que antes
   disputavam a mesma partição.
3. (Claude) `AMBIGUOUS_COLUMN_REFERENCE` introduzido pela correção anterior: a
   tabela resolvida descende dos fatos, e reaproveitar os nomes das chaves fazia
   o Spark tratar a junção como auto-join. Colunas de junção renomeadas.

### Notas

- Verificação após as correções: **13 aprovações, nenhuma falha**, incluindo dois
  testes novos — escolha estável em três execuções consecutivas sob empate, e
  preservação de decisões duplicadas da mesma entidade.
- As três primeiras perguntas do contexto de auditoria eram fragilidades reais e
  foram resolvidas antes da submissão; o registro delas permanece, porque a
  correção também precisa ser revisada. Cinco perguntas novas ficaram em aberto,
  entre elas se o desempate deveria falhar em vez de escolher, e se o contrato
  de atraso constante por fonte é limitação aceitável.

## 2026-08-14 — biblioteca, sprints 4 a 6

### Adicionado

1. (Claude) `x_snippets/ml/mlflow_run.py`: contexto `run_governado`, que recusa
   abrir sem limitações declaradas e recusa fechar sem parâmetros, métricas e
   assinatura. As instruções pessoais já exigiam esse conjunto; os wrappers
   registravam apenas parâmetros e métricas, e o restante dependia de alguém
   lembrar. As duas recusas foram verificadas em runtime.
2. (Claude) Ponteiro para o catálogo de helpers nos **16 prompts**. Antes, zero
   prompts citavam helpers enquanto 11 das 12 skills os declaravam — quem
   partisse do formulário não recebia a orientação. Optou-se por referência
   única em vez de replicar as listas, para não recriar a divergência já
   corrigida nos dois catálogos e nos dois blocos de comandos.
3. (Claude) `docs/auditoria/2026-08-14_biblioteca-pit-join/01_contexto.md`:
   contexto da auditoria A2, com papéis (Claude implementa e não se autoavalia),
   o que já está verificado e cinco perguntas específicas — entre elas o empate
   de instantes no `pit_join` e a estabilidade de `monotonically_increasing_id`.

### Notas (sprints 4 a 6)

- Sprint 0 avançou de 3 para **8 dos 14** módulos verificados. Restam seis, que
  dependem de PyTorch, TabNet, Prophet e pmdarima — conjunto de versões
  compatível com `pandas 1.5.3`/`numpy 1.26.4` ainda não resolvido.
- Dois comportamentos confirmados em runtime e documentados: os wrappers de
  treino registram no run ativo do MLflow e colidem quando usados em sequência
  na mesma sessão; e `shap_explainer` exige `output_index` em resultado
  multi-output, recusa correta em vez de arbitrar a classe positiva.
- `train_catboost` foi aprovado quando isolado: a falha da rodada 8 era colisão
  de run, não defeito do módulo.

## 2026-08-14 — biblioteca, sprints 0 a 3

### Adicionado

1. (Claude) `x_snippets/spark/pit_join.py`: junção point-in-time com atraso de
   publicação declarado. Devolve o DataFrame e o diagnóstico do que foi
   descartado por indisponibilidade temporal. Preenche exigência textual da
   skill de feature engineering que não tinha implementação.
2. (Claude) `x_snippets/spark/join_diagnostics.py`: cobertura, não-match,
   multiplicidade e fator de expansão medidos **antes** do join, com chaves
   nulas contabilizadas à parte.
3. (Claude) `x_snippets/testing/fixtures.py`: geradores determinísticos
   (tabular, série temporal, fatos/features com vazamento marcado, safras).

### Corrigido

1. (Claude) **Defeito real em `x_snippets/ml/lgbm_ranker.py`**, encontrado ao
   exercitar o módulo pela primeira vez no runtime. Em `evaluate_ranking`, o
   reordenamento `group_labels[ranked_idx]` faz busca **por rótulo** quando `y`
   é uma Series do pandas: funcionava no primeiro grupo, onde rótulo coincide
   com posição, e quebrava do segundo em diante com `KeyError`. Passou a
   converter para array antes de fatiar.
2. (Claude) Defeito na fixture `fatos_e_features`, revelado pelo próprio teste
   anti-vazamento: com clientes repetidos entre decisões, uma feature "futura"
   para uma decisão era legitimamente passada para outra do mesmo cliente, e a
   marca `eh_futura` deixava de valer. Cada decisão passou a ter cliente
   próprio, e o teste ganhou a invariante universal
   (`feature_ts + atraso <= decisão`), que não depende do rótulo.

### Notas

- Verificação no runtime: **11 aprovações, nenhuma falha**, incluindo o teste
  que prova que nenhuma feature publicada após a decisão sobrevive ao
  `pit_join`, e a expansão de join medida contra multiplicidade conhecida
  (1:1 → 1,0; 1:N controlado → 2,0).
- Rodada 7 documentou uma restrição de ambiente não conhecida: instalar as
  bibliotecas de ML sem fixar versão derruba o kernel serverless por alteração
  de pacotes core (`pandas`, `numpy`). Detalhe em `docs/testes/spark/README.md`.
- Sprint 0 permanece **aberto**: apenas 3 dos 14 módulos com dependência
  opcional foram verificados (`train_lgbm`, `survival_cox`, `kaplan_meier`).
  Os demais exigem novo ambiente com versões compatíveis fixadas.

## 2026-08-14 — documentação, sprint 6 de 6

### Atualizado

1. (Claude) `docs/decisions/README.md`: apresenta o que é um ADR e por que a
   imutabilidade importa, usando o par 0002/0005 deste próprio projeto como
   demonstração — a sequência preserva inclusive o erro corrigido.
2. (Claude) `docs/handoffs/README.md`: exemplo curto de handoff. O formato só
   fica claro vendo um pronto; a descrição sozinha não ensinava.
3. (Claude) `docs/auditoria/README.md`: explica por que auditar com mais de um
   modelo — cada um erra de forma diferente, e a divergência entre eles marca
   onde o material é ambíguo. Tabela dos quatro níveis com o gatilho de cada um.
4. (Claude) `docs/testes/forward/README.md`: define roteamento antes de mostrar
   resultado, para quem cai direto na página.
5. (Claude) `docs/testes/spark/README.md`: como ler uma falha, com os três
   padrões observados na prática e a advertência de que passar na máquina local
   não prova nada sobre o runtime.

### Encerramento do plano de documentação

Seis sprints concluídos. Balanço em relação ao diagnóstico: os 14 READMEs
receberam tratamento, mais um glossário novo; as três lacunas sistêmicas
apontadas — ausência de glossário, exemplos sem retorno e falta de percurso
inicial — foram fechadas. Nenhuma `description` de skill foi tocada em nenhum
sprint, e a certificação de roteamento 36/36 permanece válida.

## 2026-08-14 — documentação, sprint 5 de 6

### Adicionado

1. (Claude) `ambiente_fonte/README.md`: diagrama do trajeto fonte → simulado →
   workspaces e a resposta direta a "por que duas pastas com o mesmo conteúdo" —
   a fonte é neutra, o simulado acrescenta a camada `Users/<username>/` que muda
   conforme o destino. Inclui o percurso completo de uma alteração.
2. (Claude) `x_projects/README.md`: diagrama da descoberta hierárquica do
   `AGENTS.md`, com as três consequências práticas — busca de baixo para cima,
   diretórios sem o arquivo são apenas atravessados, e os arquivos encontrados
   somam contexto em vez de se substituírem.
3. (Claude) `x_scripts/README.md`: saída real de `data_quality_check` executada
   em serverless sobre tabela sintética. O exemplo escolhido reprova por prazo de
   atualização com todos os demais checks aprovados, o que evidencia que
   `status: "fail"` reflete a política de limite configurada, não qualidade do
   dado.
4. (Claude) `x_snippets/README.md`: tabela de falhas de import com causa e
   correção, montada a partir de erros reais do runtime, não de suposição.

### Atualizado

1. (Claude) O catálogo por pacote de `x_snippets` passa a apontar para o
   catálogo por demanda, encerrando a duplicação que levaria as duas listas a
   divergir na primeira alteração.

## 2026-08-14 — documentação, sprint 4 de 6

### Atualizado

1. (Claude) `x_config/README.md`: passa a explicar o que é MCP e por que outras
   ferramentas usam arquivo JSON, antes de dizer que aqui isso não vale. Um
   arquivo de configuração que não configura nada, sem mensagem de erro que
   explique, justifica o aviso. Inclui os passos da configuração real e a
   proibição de segredos em pasta versionada.
2. (Claude) `.claude/skills/README.md`: explicita a distinção entre as duas
   famílias de skill do projeto — as daqui constroem o ecossistema, as
   `rodrigo-*` são o ecossistema. Acrescenta como uma skill é acionada e como
   criar outra.
3. (Claude) `x_prompts/README.md`: percurso completo de um formulário, do modelo
   ao preenchido, com a explicação de por que `NÃO INFORMADO` difere de campo
   vazio e de como reconhecer resposta que ignorou o contrato.

### Pendente

- O passo 4 do percurso de `x_prompts` descreve o contrato esperado em vez de
  mostrar retorno real: falta uma execução no Genie Code. Marcado no próprio
  arquivo; resposta plausível não foi inventada para preencher a lacuna.

## 2026-08-14 — documentação, sprint 3 de 6

### Adicionado

1. (Claude) Guia do ecossistema: tabela com o pedido que aciona cada uma das 12
   skills sem precisar de `@`. As frases não foram inventadas — são as que
   passaram nos forward tests. Acompanham as duas lições que os testes deram:
   skill que trabalha sobre artefato não dispara sem o artefato no chat, e
   vocabulário genérico vai para a skill errada.
2. (Claude) Verificação de acesso à biblioteca com saída real, já que o import
   não imprime nada e silêncio pode ser confundido com falha.

### Atualizado

1. (Claude) Tabela de solução de problemas ampliada de 7 para 12 sintomas,
   incorporando o que apareceu durante os gates: `.py` importado como notebook,
   `cache()` recusado em serverless, arquivo obsoleto sobrevivendo à publicação,
   metadata em cache após editar skill, e nenhuma skill carregada por falta do
   artefato citado.

### Corrigido

1. (Claude) `tools/render_simulado.py` copiava a árvore inteira, inclusive
   artefatos de execução local. Rodar um helper dentro de `ambiente_fonte/` — o
   que aconteceu ao capturar as saídas deste sprint — criava `__pycache__`, que
   era renderizado e **publicado no workspace**. O `verify` não acusava, porque
   compara fonte com remoto e o lixo estava nos dois. O render passa a ignorar
   `__pycache__`, `.pyc`, `.pyo` e caches de ferramenta; fonte, simulado e
   workspace foram limpos.

## 2026-08-14 — documentação, sprint 2 de 6

### Adicionado

1. (Claude) `README.md`: percurso de primeira hora em cinco passos, do zero até
   uma alteração publicada e conferida no workspace.
2. (Claude) Seção de comandos com **saída real capturada de execução** — padrão
   que os sprints seguintes replicam. Retorno redigido à mão foi descartado como
   prática: envelhece sem avisar.
3. (Claude) FAQ com oito perguntas, entre elas as três que o diagnóstico
   apontou como não respondidas em lugar nenhum: por que duas pastas com o mesmo
   conteúdo, o que acontece ao editar direto no workspace, e por que a skill
   alterada continua se comportando como antes.

### Corrigido

1. (Claude) O diagrama de ciclo de vida ainda citava publicação pelo engine do
   Hub, decisão supersedida pelo ADR-0005. Passou a refletir os comandos reais,
   incluindo a conferência, que antes não aparecia no fluxo.

## 2026-08-14 — documentação, sprint 1 de 6

### Adicionado

1. (Claude) `x_docs/glossario.md`: 49 verbetes separados por procedência —
   plataforma Databricks, vocabulário de modelagem e convenção deste projeto —
   mais uma seção final sobre capacidades que não existem e induzem a erro
   (slash commands próprios, hooks, memória automática, MCP por arquivo).
   A separação por origem é o ponto: procurar um termo de convenção na
   documentação oficial não devolve nada, e isso não era explicado em lugar
   nenhum.
2. (Claude) Ponteiro para o glossário no `README.md` da raiz e no guia do
   ecossistema. Nenhum outro texto foi alterado neste sprint.

## 2026-08-14

### Adicionado (publicação no Free com verificação)

1. (Claude) `tools/publicar_free.py` e skill `.claude/skills/publicar-free/`:
   plano em dry-run, publicação com gate `--execute` e `verify` read-only que
   confere ausentes, obsoletos, `.py` como `FILE`, 12 skills e 6 diretórios de
   extensão. Ciclo completo executado: 164/164 arquivos, zero pendências.
2. (Claude) ADR-0005, supersedindo o ADR-0002: o engine do Hub não pode ser
   consumido nesta camada. Evidência medida no workspace — `.py` publicado por
   ele vira `NOTEBOOK` (quebraria todos os imports de `x_snippets`), enquanto
   `--format AUTO` produz `FILE`; e o cabeçalho que ele antepõe invalidaria o
   frontmatter YAML das skills. O padrão de três fases foi mantido.

### Corrigido (publicação no Free)

1. (Claude) O `verify` detectou, na primeira execução,
   `.assistant/.mcp_servers.json` remanescente no workspace — arquivo legado
   inerte que a auditoria do Codex removera do pacote e que sobrevivera porque
   `import-dir --overwrite` sobrescreve mas nunca apaga. Removido, e a detecção
   de obsoletos incorporada à ferramenta.

2. (Claude) `tools/publicar_free.py` concatenava stdout e stderr antes de fazer
   parse de JSON. A CLI emite um aviso intermitente em stderr que corrompia a
   saída e derrubava o `verify` com `JSONDecodeError`. Os fluxos passaram a ser
   tratados separadamente, com parse tolerante; verificado em execuções
   repetidas.

### Observação encaminhável (outro repositório)

- O `_fmt_args` do engine do Hub publica `.py` como notebook; o próprio
  `write_evidence.py` da camada global está nessa condição. Correção cabe ao
  dono daquele repositório, com testes próprios.

### Adicionado (fase 4 — replicação no trabalho)

1. (Claude) `docs/playbooks/replicacao-trabalho.md`: runbook completo para o
   workspace corporativo sem CLI — backup obrigatório antes de qualquer
   remoção, três rotas de transporte com o que confirmar em cada uma, limpeza
   do ambiente antigo, verificação de estrutura, testes de aceitação, rollback
   e caminho de escala para squad.
2. (Claude) Skill operacional `.claude/skills/replicar-trabalho/` com os
   pré-requisitos verificáveis e os guardrails da operação.
3. (Claude) `.claude/rules/free-vs-trabalho.md`: nova matriz de diferenças de
   runtime já observadas (cache/persist, config de cluster, bibliotecas ML,
   variável global `spark`).

### Corrigido (fase 4)

1. (Claude) `tools/spark_smoke_test.py` tinha o caminho da biblioteca fixo no
   usuário do laboratório, o que o tornava inútil no trabalho. Passa a resolver
   pelo usuário logado, com widget `assistant_root` para sobrepor. Regressão
   executada no Free: 64 aprovações, nenhuma falha.
2. (Claude) Vetor de vazamento fechado: identificador corporativo em **nome de
   pasta** escapava à validação, que só lia conteúdo. Renderizar o simulado com
   o username do trabalho criaria `Users/<identificador>/` e um `git add`
   publicaria o identificador. Agora `tools/render_simulado.py` recusa username
   com aparência corporativa e `tools/validate_assistant.py` verifica caminhos
   além do conteúdo.

### Adicionado (pacote de helpers — sprints 2 e 3 de 3)

1. (Claude) Seção `## Usar helpers da biblioteca` em 11 `SKILL.md`, cada uma com
   a tabela demanda → módulo do próprio fluxo, link para o catálogo e as
   ressalvas técnicas do domínio (leakage em splits, incidência acumulada em
   safra, thresholds calibrados em drift, escape de HTML em documentação).
2. (Claude) `rodrigo-auditoria-skills` passa a verificar aderência à biblioteca:
   novo passo na auditoria de implementação (conferir seção de helpers contra o
   catálogo), novo passo na auditoria de output (reimplementação silenciosa de
   lógica disponível vira achado) e nova dimensão de avaliação.
3. (Claude) `templates/rubrica_universal.md`: dimensão D10 reescrita com âncoras
   objetivas de aderência à biblioteca.

### Corrigido

1. (Claude) A âncora 9-10 da dimensão D10 da rubrica premiava o uso de "hooks",
   capacidade inexistente na plataforma (`.claude/rules/genie-code-oficial.md`).
   Removida junto com a reescrita da dimensão.

### Notas (pacote de helpers)

- Nenhuma `description` foi alterada nos três sprints: a seleção automática lê
  apenas o frontmatter, e as seções entram no corpo. Verificado por diff — a
  certificação de roteamento 36/36 permanece válida sem reteste.

### Adicionado (pacote de helpers — sprint 1 de 3)

1. (Claude) ADR-0004: helpers passam a ser declarados explicitamente nas skills,
   em vez de descobertos em tempo de chat. Levantamento que motivou a decisão:
   **nenhum dos 12 `SKILL.md` citava um helper** — as 3 referências do pacote
   estavam em templates auxiliares.
2. (Claude) `ambiente_fonte/.assistant/x_docs/catalogo_helpers.md`: catálogo
   demanda → módulo cobrindo os 54 helpers (47 `x_snippets` + 7 `x_scripts`),
   com API pública, marcação de dependência opcional (exigida no import vs. na
   chamada) e as restrições de runtime confirmadas no smoke test.
3. (Claude) Referências cruzadas ao catálogo em `.assistant/README.md`,
   `x_snippets/README.md` e `x_scripts/README.md`. Réplica do Free republicada.

### Adicionado

1. (Claude) `docs/testes/forward/resultados/2026-08-14_rodada1.md`: resultado da
   rodada 1 dos forward tests executada pelo Rodrigo no Genie Code do Free —
   **33 PASS, 2 FAIL, 1 pendente** de 36. Coleta automatizada via arquivos de
   evidência em `x_lab/forward_tests/` lidos por CLI.

2. (Claude) `docs/testes/forward/resultados/2026-08-14_rodada2.md`: rodada 2
   (5 testes com prompts autocontidos, IDs `-r2`) — **5 PASS, 0 FAIL**.
   **Gate de roteamento FECHADO: 36/36 PASS** (positivos 12/12, negativos
   12/12, menções 12/12), sem nenhuma alteração de `description`.

### Notas

- Rodada 2 confirmou a hipótese da rodada 1: `10P` passou com a **mesma**
  `description` e apenas o artefato embutido no prompt — a falha era do
  instrumento de teste. Nenhuma `description` foi alterada em nenhuma rodada.
- Item de vigilância registrado: `comentar-notebook` respondeu ao vocabulário
  "células %md" mas não a "markdown de documentação" no `11N-r2`; sem ação por
  ora, pois no uso real o notebook aberto no editor é sinal mais forte.
- As `description` do pacote auditado pelo Codex se mostraram bem calibradas:
  **12/12 casos negativos corretos**, sem nenhuma das colisões previstas
  (drift, materialização, deterioração, auditoria×execução); em 11 deles o
  Genie ainda escolheu a skill ideal do desvio. Nenhuma description foi
  alterada.
- As 2 falhas (`10P`, `11P`, ambas com resultado "nenhuma") concentraram-se nas
  skills que dependem de artefato no chat: os prompts citavam "este notebook"/
  "este stack trace" sem que existissem — defeito do instrumento, não do
  ambiente. Prompts v2 autocontidos aplicados no roteiro para a rodada 2
  (`07M`, `10P`, `10N`, `11P`, `11N`).
- Confirmado que skills nativas do Databricks (`data-sampling`) coexistem com as
  `rodrigo-*` no mesmo chat, sem conflito de seleção.

## 2026-08-13

### Adicionado

1. (Claude) Bootstrap do repositório: `CLAUDE.md` canônico, adaptadores
   `AGENTS.md`/`GEMINI.md`, `README.md`, este changelog e `.gitignore` com
   quarentena de `Ambiente_Antigo/`.
2. (Claude) Centro de IA `.claude/`: índice operacional, 5 regras
   (fonte de verdade, nomenclatura oficial Genie Code, Free vs. trabalho,
   multi-LLM, padrão de documentação), 3 arquivos de contexto, skills
   `validar-assistant` e `render-simulado`, e 4 templates.
3. (Claude) `ambiente_fonte/` criado como cópia editável do pacote
   `Ajustes_Codex/assistant_optimized_2026-08-13/` (12 skills, instruções,
   extensões `x_`). O pacote original permanece congelado como referência.
4. (Claude) `tools/validate_assistant.py`: recria localmente a bateria de
   validação da auditoria do Codex (frontmatter, links, tamanhos, AST Python,
   cercas Markdown, mojibake, identificadores pessoais).
5. (Claude) `tools/render_simulado.py`: gera `Novo_Ambiente_Simulado/` como
   espelho da árvore do workspace a partir de `ambiente_fonte/`.
6. (Claude) ADRs 0001 (arquitetura multi-IA), 0002 (reuso do engine
   `databricks-genie` do Verg_Alchemy_Hub) e 0003 (quarentena do
   `Ambiente_Antigo/`).

### Adicionado (testes Spark serverless — gate aprovado)

1. (Claude) `tools/spark_smoke_test.py` (notebook) + suíte `docs/testes/spark/`:
   71 checks executados em job serverless one-time no Free (Spark 4.1.0) —
   resultado final **64 PASS / 0 FAIL / 7 opcionais ausentes**.
2. (Claude) O gate revelou e levou à correção de 3 defeitos reais no
   `ambiente_fonte/` invisíveis à validação estática: `spark` como global
   inexistente em 6 módulos; `cache()`/`unpersist()` incompatíveis com
   serverless em `safe_display`, `quick_profile` e `drift_detector`;
   f-string com backslash (PEP 701, Python ≥ 3.12) em `kpi_card.py`.
   Réplica do workspace Free republicada após as correções.

### Adicionado (forward tests)

1. (Claude) Skill `.claude/skills/forward-test-skills/` e suíte em
   `docs/testes/forward/`: roteiro com 36 testes (12 skills × positivo,
   negativo e `@menção`), template de resultados e índice de rodadas. Casos
   negativos desenhados sobre as zonas de colisão entre descriptions
   (drift, WoE/IV, explicar×documentar, materialização, deterioração).

### Atualizado

1. (Claude) Workspace Databricks Free zerado e republicado como réplica deste
   projeto, a pedido do Rodrigo: backup do conteúdo anterior (camada global
   `global-*` do Hub + instruções, 10 arquivos) feito antes da remoção;
   `Novo_Ambiente_Simulado/Users/<username>/` importado via
   `databricks workspace import-dir`. Verificado: 12 skills `rodrigo-*`,
   extensões `x_`, instruções e `.py` como `FILE` (não notebook).
2. (Claude) `.claude/context/ambiente-free.md` atualizado com o novo estado do
   workspace (camada global do Hub removida; republicável pelo Hub).

### Notas

- Análise independente confirmou os achados da auditoria do Codex contra o
  export original (6 skills sem frontmatter, skills de até 2.141 linhas,
  instruções com nome sem ponto, aliases `/eda` e "hooks" não suportados,
  MCP JSON vazio, identificador corporativo em 7+ arquivos).
- Repositório GitHub privado confirmado; `Ambiente_Antigo/` mantido fora do
  git por conter identificador corporativo (ver ADR-0003).


## 2026-09-13 — R09: recuperação de preservação (ChatGPT)

### Corrigido

- (ChatGPT) Restaurados da base integrada o catálogo, o índice da iniciativa e cinco notebooks, recuperando navegação, imagens, código e saídas históricas removidos na construção R09.
- (ChatGPT) Corrigido o relato de alterações somente editoriais: o exemplo MLflow também havia alterado literais executáveis.

### Atualizado

- (ChatGPT) Registro RECUPERACAO_R09, relatório e matriz distinguem recuperação concluída de integração, freeze e runtimes ainda pendentes. Cinco novos READMEs preservados; nenhuma mudança na main, em implementações/fachadas ou publicação Databricks.
