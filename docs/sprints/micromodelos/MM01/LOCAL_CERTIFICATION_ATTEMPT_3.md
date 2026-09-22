# MM01 — Local Certification v1 — tentativa 3

Data da execução: 2026-09-22

Status: **FAIL POR INTERRUPÇÃO EXTERNA/CONTROL EVENT DURANTE O PRIMEIRO BOOTSTRAP**

## Identidade observada

- repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`;
- origin: `https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks.git`;
- branch: `micromodelos/mm01-contrato-canonico`;
- HEAD: `8e7c7a8d2b11f83b0d5f558239d881c1ce66cdc6`;
- tree: `0ecdbe37631db4426c1367c60c6eb99a8b03b181`;
- `origin/main`: `17640a6a31f562e9979d235ede27cf44cef9ebbf`;
- tree da main: `687cb36f3dcbfbca02ce09965e5ac4b3bcc0b244`;
- merge-base: `17640a6a31f562e9979d235ede27cf44cef9ebbf`;
- `ahead_by=158`;
- `behind_by=0`;
- checkout não shallow;
- worktree limpa;
- merge-ref: `9e6ef83c5a13395dc88c72c8a1f90ebf2a7c653a`;
- tree do merge-ref: `0ecdbe37631db4426c1367c60c6eb99a8b03b181`;
- diff HEAD × merge-ref: vazio.

## Preflight

Diferentemente das tentativas anteriores, a R3 concluiu o preflight canônico.

Foram produzidos:

- `preflight.json`;
- `inputs_sha256.json`.

O preflight confirmou:

- identidade Git esperada;
- `behind_by=0`;
- worktree limpa;
- ambiente-base compatível;
- resolução Windows funcional para npm;
- os nove workflows-fonte com `blob_matches=true`;
- `missing_snippets=[]` em todos os workflows;
- hashes dos inputs críticos capturados.

## Portabilidade Windows

A correção introduzida após a R1 foi efetivamente exercitada.

No Windows observado:

- npm foi resolvido por shim `.CMD`;
- o comando foi transportado por `cmd.exe /d /c call ... npm.CMD --version`;
- `npm --version` concluiu com sucesso;
- o diagnóstico read-only posterior confirmou que pnpm também resolvia para shim `.CMD`.

Assim, a causa da R1 está corrigida para o caminho exercitado pelo preflight.

## Interrupção

O primeiro step executável, `BOOTSTRAP_PYTHON`, foi iniciado.

O processo global terminou com:

`-1073741510`

equivalente a:

`0xC000013A`

A execução foi interrompida durante o bootstrap de dependências Python.

Não foi estabelecida a origem externa da interrupção.

O log do step contém somente o comando lógico e o comando resolvido; não houve saída do pip preservada.

Não houve retry.

## Gates

Nenhum gate posterior foi executado.

Em particular:

- `CERT_SELFTEST=NOT_RUN`;
- `MM01_CANONICAL=NOT_RUN`;
- `MM01_R02=NOT_RUN`;
- `MM01_R03=NOT_RUN`;
- `MM01_VALIDATE_ASSISTANT=NOT_RUN`;
- `CI_LOCAL=NOT_RUN`;
- V00/V01/V02/V10/V11/V12/V13 = `NOT_RUN`.

`V12_SCOPE_STRICT` não chegou ao estado `SKIP_ALLOWED`.

## Evidência pós-interrupção

O certifier não chegou a produzir:

- manifest final;
- postflight canônico;
- environment final;
- SHA256SUMS final;
- ZIP.

Uma inspeção read-only posterior confirmou:

- estado Git igual ao preflight;
- worktree limpa;
- todos os 17 hashes críticos recalculados idênticos aos valores do preflight.

Essa verificação não substitui `postflight_ok=true`; a R3 permanece FAIL.

## Natureza da falha

A R3 não demonstra falha funcional da MM01.

Ela também não demonstra regressão da portabilidade Windows da R1.

A causa observada é uma interrupção do processo durante o primeiro bootstrap. Como a execução não produziu manifest/postflight/ZIP canônicos, ela não pode ser promovida a PASS nem parcialmente aproveitada como certificação.

## Hardening posterior

A R3 revelou uma fragilidade probatória: um `KeyboardInterrupt` controlável podia escapar do fluxo normal antes que o executor materializasse um `StepResult`, postflight, manifest e bundle de falha.

O hardening posterior introduziu:

- `72246b7b2a0c21f11ad3a2db2ef1626705ee2e72`: captura estruturada de `KeyboardInterrupt` dentro do step, com `status=INTERRUPTED`, log e reason; o handler externo também passa a aceitar `KeyboardInterrupt` quando o processo Python ainda mantém controle;
- `83aa8e6a23d7c3895eb5741ac6639ed96f05ff39`: regressão que exige a materialização de interrupção estruturada.

Esse hardening não altera nenhum gate técnico, não transforma interrupção em sucesso e não promete recuperar uma terminação externa que mate o processo sem devolver controle ao Python.

## Próximo passo

A R3 permanece histórica como FAIL.

A próxima execução integral deverá usar o HEAD técnico/documental produzido após este registro, em novo diretório probatório, depois de reconfirmar novamente:

- HEAD;
- `origin/main`;
- merge-base;
- `behind_by=0`;
- merge-ref;
- identidade dos workflows.

MM01 continua não aceita, não integrada e MM02 permanece bloqueada.
