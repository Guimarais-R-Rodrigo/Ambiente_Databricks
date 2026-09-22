# SE08 — Corretiva R2 repo-side

Data: 2026-09-22

## Classificação

`R2_REPO_SIDE_READY_FOR_WINDOWS_VALIDATION` somente no sentido de preparação de código.

Este documento NÃO declara:

- certificação Windows/NTFS;
- correção causal do WinError32;
- FULL SE08 aprovado;
- Databricks Free aprovado;
- Genie aprovado;
- promoção ao ambiente de trabalho.

## Identidade de partida

- base remota da R2: `498609597728675f32f55bb931429dc71b1db71b`;
- branch: `sef/SE08-r2-repo-side`;
- HEAD imediatamente antes deste checkpoint: `b3fc79c9709af91d424419c550d30dceb1306ec3`;
- candidata Windows anterior preservada externamente: `5b2c16926db5f57af7864b30e99ab4b7fe798c22`.

A R2 é uma nova linha remota. Ela reconcilia por conteúdo duas mudanças locais anteriores aos 17 cherry-picks da corretiva:

1. `3118e970`: fixture de identidade corporativa montada em runtime;
2. `e3e67bce`: quatro derivados rematerializados pelo renderer.

Os quatro derivados da R2 foram copiados byte a byte de suas fontes canônicas; seus blobs coincidem com os blobs finais registrados no patch da campanha local.

## S1 — storage sintético

O caso `before_removal` de `test_certify_storage_cleanup.py` lançava a falha sintética antes de `TemporaryDirectory.cleanup()` desarmar o finalizador automático.

Sem uma referência forte ao objeto, o CPython podia executar o finalizador implícito antes do oráculo externo e apagar o diretório que o teste pretendia observar. Isso explica a sequência histórica `exists_before_error=true` e `exists_at_oracle=false` sem exigir retry do certifier.

A R2:

- mantém a `TemporaryDirectory` defeituosa viva até o oráculo;
- observa e copia o resíduo;
- executa teardown explícito somente depois da observação;
- usa `TemporaryDirectory.cleanup()` no teardown test-only depois do snapshot, deixando o próprio Python desarmar o finalizador pelo caminho normal;
- não altera `certify_local.py` para esta correção;
- não usa sleep, retry, `ignore_errors` ou redução de assertiva.

O teste histórico continua exigindo resíduo observável e cleanup classificado como FAIL.

## S2 — diagnóstico do WinError32

Foi adicionado `tools/skill_enforcement/cleanup_diagnostics.py` como observador opt-in.

O observador:

- não integra a lógica normal do certifier;
- não muda timeout;
- não repete remoção;
- não encerra aplicações via Restart Manager;
- registra lifecycle da `TemporaryDirectory`;
- registra fronteiras do Job Object próprio;
- preserva PID do launcher e do filho via registros existentes;
- pode consultar Restart Manager depois de WinError32;
- trata lista vazia do Restart Manager como `NO_MATCHES_REPORTED_NOT_PROOF_OF_NO_HANDLES`.

A R2 acrescenta o caso `before-output`, que executa exatamente
`test_keyboard_interrupt_before_first_output`, o teste em que o WinError32 nativo apareceu na campanha anterior.

Quando a consulta Restart Manager é habilitada, são registrados `stdout`, `stderr` e `child.json` da própria invocação. A consulta é diagnóstica e pode alterar timing; por isso não é certificação causal.

## S3 — composição do FULL SE08

O perfil `se08` passa a incluir explicitamente, além dos gates já existentes:

- `se08_storage_cleanup_tests`;
- `se08_windows_corrective_tests`;
- `se08_cleanup_diagnostics_tests`.

Consequência: um futuro `FULL_SE08_LOCAL` não pode ser considerado PASS se a suíte de storage estiver FAIL. Isso fecha a lacuna observada na campanha anterior, em que o FULL passava sem executar storage.

Os testes do observador são portáveis e não afirmam evidência Windows. Os probes nativos continuam opt-in e separados.

## Materialização derivada

Foram reconciliados exatamente quatro arquivos em `Novo_Ambiente_Simulado`:

- Manual Técnico;
- template de skill;
- README da policy SEF;
- README de skills.

Cada destino foi substituído pelo conteúdo exato da fonte canônica correspondente. Nenhum outro derivado foi editado manualmente.

## Dívidas preservadas

Permanecem:

- `S06-A1-R4=NOT_RUN`;
- `SE06_DOD=INCOMPLETE`;
- `SE07_FULLY_CERTIFIED=false`;
- `hub-ml-criar-objeto` em L2 global;
- promoção ao trabalho bloqueada;
- WinError32 nativo sem causa estabelecida até nova observação;
- campanha anterior `CORRECTIVE_NOT_READY` preservada.

## Próxima campanha Windows obrigatória

Executar uma vez por SHA congelado, com retenção externa exclusiva:

1. suíte de storage;
2. testes estáticos Windows;
3. testes do observador;
4. probe `preflight`;
5. probe `before-output --restart-manager`;
6. probe `never-ready --restart-manager`;
7. certifier regression;
8. CI;
9. FULL SE08 somente se as precondições anteriores não revelarem bloqueio.

Falha não autoriza retry automático. Evidência deve voltar para auditoria antes de qualquer mudança causal adicional.


## S5 — auditoria pré-Windows

A auditoria repo-side foi executada depois do hardening de S1–S4, antes de qualquer nova campanha Windows.

Achados e verificações:

- o perfil FULL SE08 contém explicitamente `se08_storage_cleanup_tests`, `se08_windows_corrective_tests` e `se08_cleanup_diagnostics_tests`; o storage não pode mais ficar fora de um FULL futuro;
- a fixture `before_removal` mantém ownership forte da `TemporaryDirectory` até o oráculo, registra se o finalizador ainda estava armado e só chama `cleanup()` depois do snapshot; não há retry nem alteração do certifier para tornar o caso verde;
- o probe nativo `before-output` aponta nominalmente para `test_keyboard_interrupt_before_first_output`;
- caso nativo ausente ou `skipped` é resultado não observável/infraestrutural, nunca sucesso do probe;
- Restart Manager permanece consulta opt-in, posterior à falha e sem `RmShutdown`/`RmRestart`; lista vazia não prova ausência de handles;
- os quatro arquivos materializados em `Novo_Ambiente_Simulado` têm blobs idênticos às respectivas fontes canônicas; `MANUAL_TECNICO.md` raiz também coincide byte a byte com a fonte;
- a contagem `repo (identidade) = 1638` foi reconciliada com o contrato do validador: arquivos Git rastreados com extensões `.md`, `.py`, `.txt` e `.json` dentro do escopo; não é a contagem bruta de todos os blobs;
- a R2 não altera `policy.json`, níveis de enforcement, contratos das skills ou lógica normal de cleanup do certifier além da composição explícita dos gates SE08;
- nenhuma observação Linux/estática é reclassificada como certificação Windows, NTFS, FULL, Free ou Genie.

Finding corrigido durante S5: a primeira versão do observador usava apenas `unittest.wasSuccessful()`; como `unittest` considera uma execução integralmente pulada como bem-sucedida, um probe ambiental poderia terminar com exit 0 sem observação nativa. A versão final exige exatamente um teste executado e zero skips para exit 0.

### Classificação S5

`R2_REPO_SIDE_AUDITED_READY_FOR_WINDOWS_CAMPAIGN`

Essa classificação significa somente que o delta repo-side foi reconciliado e está pronto para ser submetido aos gates ambientais. Ela não é certificação da SE08 nem autorização de promoção.


### Actions observadas durante S5

A criação da primeira ref de RC disparou workflows de `push` automaticamente no SHA `089a5e7d6f59ab5561cdd4c5dbc772bafc85fe32`.

A primeira observação de `Skill Enforcement SE01` ficou **FAIL**, com todos os passos funcionais anteriores aprovados e falha exclusiva em `Snapshot README`:

- validação estrutural: aprovado, mas com 1 warning de `__pycache__` em `ambiente_fonte`;
- renderer: aprovado;
- render diff: aprovado;
- snapshot: esperava `APROVADO: 0 falha(s), 0 aviso(s)`, observou `APROVADO: 0 falha(s), 1 aviso(s)`.

Causa repo-side identificada: `validate_assistant.py` importava `validate_contracts`, que carrega uma fachada estática sob `ambiente_fonte/.assistant`; sem supressão de bytecode, a própria validação criava `__pycache__` antes de executar sua guarda de higiene.

Correção: `sys.dont_write_bytecode=True` é definido antes dos imports locais do validador. Nenhum warning foi ignorado, nenhum cache foi apagado para obter verde e nenhum valor do snapshot foi reduzido.


### Segundo finding repo-side observado em Actions

No HEAD `9bd1e87c673a8484aa5a38954b4ffef10d0d1cfb`, o workflow `CI local reproduzível` preservou um FAIL no estágio `sef`, enquanto os demais estágios reportados no trecho final continuaram aprovados.

A falha foi:

`IndentationError: expected an indented block after 'if' statement on line 128`

Causa confirmada em `tools/tests/test_skill_enforcement_se08.py`: uma edição anterior inseriu sequências literais `\\n` no comentário da fixture de identidade sintética. Como o comentário permanecia na mesma linha física, o `return` seguinte também ficou comentado e o `if` perdeu seu corpo.

Correção repo-side:
- converter as sequências literais em quebras de linha Python reais;
- preservar a construção runtime da identidade sintética;
- acrescentar guardrail com `ast.parse` do módulo operacional SE08.

A tentativa vermelha permanece histórica; não foi feito rerun manual.


## R2 Windows — campanha d3720f59

Campanha local executada em 2026-09-22 sobre:

- SHA: `d3720f593d56dea64b1f027ad7ba725075f55ef3`;
- tree: `4061694897bb86afbe4368969799d2d9525b04ad`;
- Windows 11 build 26200;
- Python 3.12.14;
- NTFS.

Bundle externo recebido:

- arquivo: `SEF_SE08_R2_WINDOWS_d3720f59_20260922.zip`;
- SHA-256: `7b276cd7ffa88104855d53eede60dc8f526e98e1fbf17e0b0f5dac8b95bf2e5e`;
- classificação do executor: `WINDOWS_NOT_READY`.

Resultados principais:

- storage standalone: FAIL 8/9, porém o antigo caso `test_residue_is_observed_not_deleted_or_certified_by_recovery` PASSOU com `exists_at_oracle=true`, ownership forte e finalizer ativo observados;
- a falha standalone nova ocorreu no subtest `nonzero/gate/after_removal` porque um WinError32 nativo ocorreu antes da injeção sintética;
- windows corrective: PASS 6/6;
- cleanup diagnostics: PASS 31/31;
- before-output e never-ready: PASS diagnóstico, sem WinError32 nessas invocações;
- certifier regression standalone: PASS 46/46;
- CI Windows: FAIL apenas na etapa `sef`; 9/10 etapas OK;
- no CI, storage/corrective/diagnostics passaram e `certifier_regression` sofreu WinError32 no teste `test_timeout_real_parent_child_external_oracle_and_partial_streams`;
- FULL: `NOT_RUN_CONDITION_NOT_MET`.

Foram observadas duas ocorrências nativas de WinError32:

1. storage `nonzero/gate/after_removal`, em `stderr`;
2. CI/certifier regression, timeout pai-filho, em `stderr`.

Em ambas:

- `process_cleanup=COMPLETE`;
- `temporary_cleanup=FAILED`;
- `cleanup=FAILED`;
- launcher e child tinham sido encerrados segundo a telemetria disponível;
- o dono do handle no instante da falha permaneceu `NOT_OBSERVED`.

Os probes autorizados possuíam Restart Manager, mas ficaram verdes; as falhas reais ocorreram fora desses hooks. Portanto observações dos probes não podem ser transferidas para as invocações que falharam.

### Leitura técnica

A R2 resolveu o defeito do oráculo/finalizer sintético originalmente identificado, mas não resolveu o sharing violation nativo do certifier. O novo FAIL da suíte de storage é evidência do mesmo blocker de cleanup, não fundamento para enfraquecer a assertiva da fixture.

A documentação Microsoft sobre Job Objects registra que processos filhos normalmente permanecem associados ao Job salvo breakaway explícito e que `ActiveProcesses` é contabilidade do Job. Isso torna insuficiente atribuir a falha aos processos supervisionados sem observar o owner real do recurso. A próxima rodada deve medir o owner no próprio boundary que falha, não apenas em probes paralelos.

## R3 — observabilidade nativa no boundary real

A R3 não tenta corrigir causalmente o WinError32 ainda.

Mudanças autorizadas repo-side:

- quando o cleanup já falhou com WinError32, consultar uma única vez o Restart Manager para os recursos remanescentes da própria invocação;
- registrar estado instantâneo, sem espera, de launcher PID e child PID;
- registrar snapshots do Job Object imediatamente após `TerminateJobObject` e antes de fechar o Job;
- manter a exceção original e o verdict intactos;
- não adicionar sleep, retry, nova remoção, `ignore_errors`, `RmShutdown` ou `RmRestart`;
- fazer o CI imprimir integralmente a saída de uma etapa reprovada, eliminando a limitação histórica dos 4.000 caracteres.

Próximo gate ambiental deve observar especificamente storage, certifier regression e CI Windows. FULL continua condicionado.


## R3 Windows — campanha 3556f198

A campanha Windows R3 foi executada sobre:

- SHA `3556f198670c38d3ced118b3e84db59b5728efa8`;
- tree `ce50b5414f39c40b0bf26610e3b5d78edda7b248`;
- bundle `SEF_SE08_R3_WINDOWS_3556f198_20260922.zip`;
- SHA-256 verificado externamente: `bc2d66bcd6fab1619b824458256622fbadd393c7372f04703ef16f90fb1ab5fb`;
- manifesto interno: 1620 arquivos conferidos, zero divergências;
- classificação: `R3_WINDOWS_NOT_READY`.

Resultados:

- Windows corrective: PASS 8/8;
- storage standalone: PASS 9/9;
- certifier regression: exit 0, 50 métodos, 1 skip de escopo;
- CI Windows: PASS 10/10;
- FULL SE08: FAIL 20/21, somente `se08_storage_cleanup_tests`.

O WinError32 não reapareceu nos gates focalizados standalone/CI, mas reapareceu uma vez no FULL, em `test_gate_cancellation_with_storage_error`, modo `none`, gate, `after_removal`.

Na ocorrência:

- `process_cleanup=COMPLETE`;
- `temporary_cleanup=FAILED`;
- Job Object após terminate: `active=0`, PID list vazia;
- Job Object antes de close: `active=0`, PID list vazia;
- launcher PID e child PID estavam sinalizados, `running=false`, exit code 1;
- Restart Manager retornou `NO_MATCHES_REPORTED_NOT_PROOF_OF_NO_HANDLES`;
- owner do handle permaneceu não identificado.

Conclusão: a R3 exclui como explicação suficiente a hipótese de launcher/child ainda vivos na amostra observada, mas não identifica o processo/handle que bloqueou `stderr`. A ausência de matches no Restart Manager não significa ausência de handle.

## R4 — PIDs usando o arquivo no boundary de falha

A R4 continua observacional. Ela acrescenta, somente depois de WinError32 já ocorrido, uma consulta read-only por recurso usando `NtQueryInformationFile` com `FileProcessIdsUsingFileInformation` (classe 47).

A própria documentação do Windows classifica essa information class como reservada para uso do sistema; por isso seu resultado é diagnóstico e fail-closed, nunca requisito de produto. Orientação publicada por representante Microsoft descreve esse mecanismo para obter a lista de PIDs que mantêm um arquivo aberto.

Limite importante: a consulta precisa abrir seu próprio handle de leitura de atributos para o arquivo; portanto o PID do observador pode aparecer por causa do próprio handle diagnóstico. Esse PID é rotulado como `OBSERVER_PID_QUERY_HANDLE_OR_EXISTING_HANDLE` e não prova um lock pré-existente.

A consulta:

- é uma única amostra;
- não faz retry;
- não dorme;
- não remove arquivo;
- não fecha handles de terceiros;
- não muda verdict;
- roda por recurso (`stderr`, `stdout`, `child.json` quando existentes);
- é complementar ao Restart Manager, não substituta.


## R4 Windows — campanha 50776fef

Campanha executada em `50776fefc35ae65a48b913b1b190adff9738d19e`, tree `59b4ebadc6e35d5b1e40be1539f6d8fdc976068d`.

Bundle recebido:

- `SEF_SE08_R4_WINDOWS_50776fef_20260922.zip`;
- SHA-256 externo: `ee42832a63f815937b8fe39488d91a81b07b4f5c1464bdee07edb480ebd6aac4`;
- ZIP CRC: íntegro;
- manifesto interno: 1081/1081 arquivos conferidos, zero divergências;
- classificação: `R4_WINDOWS_NOT_READY`.

Resultados:

- windows corrective: PASS 9/9;
- storage standalone: PASS 9/9;
- certifier standalone: exit 0, 50 métodos, 1 skip de escopo;
- CI: FAIL apenas em `sef`;
- FULL: `NOT_RUN_CONDITION_NOT_MET`.

O WinError32 reapareceu no CI em `test_timeout_real_parent_child_external_oracle_and_partial_streams`.

Na ocorrência:

- Job Object após terminate e antes de close: `active=0`, PID list vazia;
- launcher e child: `running=false`;
- Restart Manager: nenhum match;
- `FileProcessIdsUsingFileInformation` em `stderr` e `stdout`: NTSTATUS success, `count=0`, nenhum PID;
- a query per-file era executada depois do Restart Manager, portanto o lock podia desaparecer antes da amostra específica do arquivo.

## R5 — prioridade temporal no arquivo que falhou

A R5 reduz deliberadamente a latência observacional:

1. marca `temporary_cleanup_error_monotonic_ns` no primeiro instante do outer catch;
2. antes de formatar traceback ou consultar o diretório, invoca o observador nativo;
3. consulta primeiro, e somente uma vez, o arquivo cujo `unlink` retornou WinError32;
4. só depois executa Restart Manager;
5. somente depois consulta recursos secundários;
6. registra início/fim/duração monotônica e delta desde a captura do cleanup error;
7. registra se os objetos Python `stdout` e `stderr` do certifier pai já estavam fechados imediatamente antes do `TemporaryDirectory.__exit__`.

A R5 continua sem retry, sleep, segunda remoção ou mudança de verdict.
