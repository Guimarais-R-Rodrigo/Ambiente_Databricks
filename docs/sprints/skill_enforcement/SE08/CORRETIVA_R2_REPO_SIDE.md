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
- desarma o finalizador depois do teardown;
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

A R2 acrescenta o caso `keyboard-before-output`, que executa exatamente
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
5. probe `keyboard-before-output --restart-manager`;
6. probe `never-ready --restart-manager`;
7. certifier regression;
8. CI;
9. FULL SE08 somente se as precondições anteriores não revelarem bloqueio.

Falha não autoriza retry automático. Evidência deve voltar para auditoria antes de qualquer mudança causal adicional.
