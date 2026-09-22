# SE08 R2 — preparação repo-side e fronteira local

Autor da implementação: ChatGPT. Data: 2026-09-22.
Estado: `R2_COMPONENTS_PREPARED_INTEGRATION_REQUIRED`.
Não é release candidate, certificação Windows, encerramento da SE08 ou autorização
para publicar/promover. A campanha local anterior permanece `CORRECTIVE_NOT_READY`.

## Proveniência e integração

A base desta preparação remota é
`498609597728675f32f55bb931429dc71b1db71b`, da corretiva Windows/CI.
A candidata local preservada é
`5b2c16926db5f57af7864b30e99ab4b7fe798c22`, tree
`cf9896faab93f3b4665dc83fb9fc3857b5f98121`.
Seu objeto de commit não estava disponível no GitHub na leitura desta sessão.
Esta branch NÃO afirma conter a ancestralidade local nem reproduzir sua tree.

O delta R2 deve ser integrado seletivamente sobre a candidata local, preservando
os commits `3118e970` e `e3e67bce`, os 17 cherry-picks e os registros do Codex.
A montagem da identidade sintética reproduz a alteração já presente em `3118e970`.
Nenhuma alteração de `ambiente_fonte`, policy, níveis, certifier de produção,
workflows ou derivados foi preparada nesta R2. Os quatro derivados locais não
são transportados de volta nem editados manualmente.

Foi adotado SOMENTE `cleanup_diagnostics.py` da revisão
`9a81c93b87796bc71e92e9f861a522b664d52504`, com seus testes e correções R2.
O observador alternativo da branch `c6277d71` NÃO foi integrado.
Não fazer merge integral das branches experimentais.

## Correção da fixture de storage

A injeção `before_removal` lançava exceção antes de `TemporaryDirectory.cleanup()`.
Nessa fronteira o finalizador automático permanece armado. Se o objeto perde sua
última referência, o resíduo pode ser removido antes de `exists_at_oracle`.

A fixture agora mantém uma referência forte SOMENTE para essa injeção, observa o
filesystem, copia o resíduo e depois realiza o descarte explícito próprio do teste.
Não altera o finalizador de produção, não ignora falhas e não repete remoções para
obter sucesso. As nove regressões existentes e as assertivas originais de resíduo
foram preservadas; novas assertivas cobram retenção, finalizador e descarte posterior.

Seis controles de componente compilam a função real `cli_probe` por AST e usam
`TemporaryDirectory` e coleta de lixo reais, com doubles explícitos do certifier e
da convenção de saída. O mutante sem retenção reproduz o desaparecimento.
Esses controles NÃO executam a suíte completa de nove métodos nem reproduzem
WinError32 nativo. O FAIL Windows histórico 8/9 não foi reclassificado.

## Observador opt-in

O observador é separado do certifier e não certifica release. Registra fronteiras
de cleanup explícito/implícito, streams e Job Object próprio. `--case before-output`
seleciona `test_keyboard_interrupt_before_first_output`, cenário da última ocorrência
nativa; `--case never-ready` mantém o cenário de ausência de readiness. Cada chamada
executa um único caso. Skip ou ausência do caso não resulta em sucesso diagnóstico.

`--restart-manager` é opção explícita. Após uma falha com código Win32 32, consulta
os recursos stdout/stderr da própria invocação. Abre e encerra uma sessão transitória
do Restart Manager; não chama shutdown/restart de aplicações, não instala ferramentas
e não eleva privilégio. Lista usuários reportados de recursos, não todos os handles
do kernel nem prova o dono causal na hora da falha. Retorno vazio, erro ou informação
incompleta mantêm essa limitação. A consulta não é repetida para obter uma lista útil.

Hooks e consultas podem alterar timing/lifetime. Uma execução sem WinError32 só
sustenta `NOT_REPRODUCED_IN_THIS_RUN`, nunca `WINERROR32_FIXED`.
Nenhum ajuste especulativo de sleep, timeout, retry ou cleanup de produção foi feito.

## Gate e evidência desta preparação

O entrypoint SE08 mantém seus oito testes operacionais e carrega, no mesmo step,
os quatro guardrails Windows já existentes, seis controles de lifetime e 31 testes
do observador: 49 métodos de nível superior esperados. A suíte real de storage
continua comando obrigatório separado. Não há probe nativo automático nem FULL
recursivo dentro desses componentes.

Execuções desta sessão: Linux/Python 3.13.5, cópia PARCIAL de fontes, fora de um clone
completo. Conteúdos-base foram conferidos por Git blob SHA antes das alterações.

| Verificação | Resultado observado | Limite |
|---|---|---|
| Lifetime/oráculo | 6/6, exit 0 | Componente com GC real e doubles declarados |
| Observador | 31/31, exit 0 | Doubles Win32 não são Windows nativo |
| Wiring | 41 componentes descobertos, IDs únicos; oito originais preservados | Não executou o conjunto 49/49; quatro estáticos representados por double de discovery |
| Finalizador externo de metadados | 11/11 controles, exit 0 | Parsing, preservação de bytes e escrita; não executou validador do produto |

Logs externos preservam as tentativas. Não foram executados nesta sessão: storage
real 9/9, F-04, CI integral, validador completo, renderer, FULL, Windows/NTFS,
Databricks Free ou Genie. Resultados anteriores continuam vinculados a seus SHAs.

## Metadados pendentes e campanha local

O CHANGELOG raiz e o snapshot do README devem ser concluídos na árvore integrada.
Esta preparação NÃO declara o requisito de fechamento documental satisfeito.
A ferramenta externa `finalizar_metadados_r2.py`, entregue com manifesto de hashes,
contém a entrada atribuída a ChatGPT e a atualização mecânica do snapshot. Ela exige
ancestralidade `5b2c1692`, HEAD explícito, worktree limpa, escopo fechado e fontes
idênticas; preserva backups e só escreve CHANGELOG/README. Não faz commit, rollback
silencioso nem presume a contagem final. Falha de validação interrompe a preparação.
Não transformar a previsão aritmética de arquivos em saída medida.

Após integrar o delta, concluir metadados, revisar o diff e congelar NOVO SHA:

1. Rodar componentes R2, suíte real de storage e F-04, serialmente, com retenção externa exclusiva.
2. Executar os casos diagnósticos autorizados uma vez cada. A consulta RM só ocorre
   com opção explícita; indisponibilidade de symlink não é PASS de guardrail.
3. Rodar a bateria CI prescrita. Todos os resultados ficam vinculados ao mesmo SHA,
   sem repetir uma falha para obter verde. Falhas retornam à engenharia repo-side.
4. FULL permanece condicionado aos gates e ao snapshot consistentes. Seu resultado
   não apaga falha de storage ou WinError32 em outra etapa.
5. PR, Actions, merge, Free/Genie e promoção não são autorizados por esta preparação.

Preservados: SE06 24/25; `S06-A1-R4=NOT_RUN`; `SE06_DOD=INCOMPLETE`;
`SE07_FULLY_CERTIFIED=false`; `hub-ml-criar-objeto` L2 global;
`PROMOCAO_TRABALHO=BLOQUEADA`.
