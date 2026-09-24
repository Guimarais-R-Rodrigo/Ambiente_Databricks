# B0 — testes e gates

## 1. Gate barato de autoria

`python -B -m tools.skill_enforcement.parallel.preflight` executa antes da suíte. Ele:

- faz parse de todos os JSONs do mecanismo e do plano;
- compila os Python do mecanismo e a suíte B0;
- valida o command registry fechado;
- confere o registry de coverage;
- valida os dois pilotos;
- confronta os quatro schemas executáveis V3 com as constantes do código;
- exige `additionalProperties=false` e `$id/const` coerentes;
- confere que os templates de campanha/tarefa apontam para os contratos V3.

Erro barato não deve chegar ao laboratório.

## 2. Metatestes

`python -B -m unittest tools.tests.test_ser_parallel_b0 -v` contém **74 métodos definidos estaticamente** na candidata V3.

A suíte preserva as regressões históricas e adiciona discriminantes para os achados da auditoria: null/tipos inválidos; task obrigatória vazia; NA sem precondição aprovada; timeout/exit booleano/tempo inválido; overlap escondido por wave; causalidade de stop; ciclo; secret scan resealado e filename; colisão de metadata; symlink; CRLF/non-UTF8 reais; processo filho residual; coleta unittest real; target ausente; override histórico; identidade de rodada; schemas/findings; lease/slot semantics; preflight; troca limpa de HEAD; entrypoint COMMAND_ONLY ausente; e ordem de atribuição do Job Object antes da liberação do child.

Contagem estática não equivale a execução. O SHA final precisa produzir coleta e PASS integrais.

## 3. Cobertura herdada

`python -B -m tools.skill_enforcement.parallel.coverage` deve retornar `status=PASS`, 21 steps SE08, nove etapas CI não-SEF e cinco grupos SER01.

A saída CLI do inventory é JSON ASCII-safe (caracteres Unicode escapados) para ser transportável também em consoles Windows `cp1252`; o parsing recupera o conteúdo Unicode original.\n\nO V3 distingue:

- `MAPPED`: command de unittest realmente coletado pelo loader, com IDs normalizados;
- `COMMAND_ONLY`: validador/probe explicitamente allowlisted como não-unittest **e com entrypoint existente/verificado**;
- `EMPTY_METHOD_MAP`: command de teste resolvido mas sem testes coletados — bloqueante;
- `COLLECTION_ERROR`: import/loader/ID não resolvido — bloqueante;
- `MISSING`: alvo obrigatório inexistente — bloqueante;
- `UNCLASSIFIED`: política ausente — bloqueante.

AST é apenas diagnóstico paralelo (`ast_methods`); não define `MAPPED`. Overrides temporais têm schema fechado, SHA histórico, razão e `successor_ids` que precisam existir na coleta real. O inventory reporta ocorrências e IDs únicos separadamente.

## 4. Processos, isolamento e logs

`process.py` persiste stdout/stderr diretamente em bytes e calcula SHA-256 sobre os mesmos arquivos. No POSIX, o comando entra em process group próprio e descendentes residuais são terminados antes de liberar o recurso.

No Windows, um launcher Python permanece bloqueado em stdin. O launcher é primeiro atribuído a um Job Object com kill-on-close; somente então recebe o byte de liberação e cria o comando real. Assim, o alvo e seus descendentes nascem dentro do job. O PID do child é preservado em evidência. A prova efetiva dessa semântica no Windows continua gate de host, não inferência do teste Linux.

## 5. Pilotos e verificação independente

- selective: falha deliberada bloqueia apenas dependentes; frente independente continua; integrador/publicação sintética fica bloqueado.
- global: uma tarefa `GLOBAL_CAMPAIGN` falha; nenhuma tarefa posterior, inclusive integrador, pode iniciar.

A campanha normal permanece FAIL quando contém falha deliberada. O release driver exige exit code deliberado `1`, reabre `campaign.json`, `summary.json` e logs persistidos, recalcula `verify_campaign_run` e exige igualdade com a verificação do produtor antes de aplicar o oráculo específico do piloto.

## 6. RAW, SHARE e release verdict

O manifesto exclui somente o `MANIFEST.json` raiz. Manifestos aninhados são arquivos normais. Symlinks e escapes são proibidos.

SHARE reserva os paths do protocolo, preserva bytes quando não há substituição e reexecuta a política de secret scan sobre **nomes e conteúdos finais**. Conteúdo não UTF-8 é `BINARY_UNEXAMINED` e reprova. O verifier recalcula o scan; alterar apenas o rótulo do binding não cria PASS.

RAW e SHARE têm manifestos finais separados e binding externo não circular. `RELEASE_VERDICT.json` é o único veredito de liberação e aponta por hash para resultado do mecanismo, manifestos, binding e verificação do envelope.

## 7. Freeze

`freeze_prepare.py` exige worktree limpa, mede o snapshot, pode alterar somente `README.md` e reconfirma o snapshot. Ele não faz commit, não altera policy e não substitui os gates acima.
