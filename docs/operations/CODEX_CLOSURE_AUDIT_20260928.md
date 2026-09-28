# Fechamento técnico do controller CLI — 28/09/2026

Autor: (ChatGPT). Manutenção autorizada pelo usuário nesta conversa para reduzir falhas evitáveis antes do retorno ao PC.
Base auditada: `84ad737acc78905b730656cc5e0bdc6f84240d8c`.

Este registro é de auditoria/correções da camada do controller. Não é certificação CQ, não altera o estado vivo B1 e não concede autoridade material.

## Método e limites

Foram materializados 44 arquivos de governança e dependências, conferidos pelos respectivos Git blob SHAs retornados pelo conector GitHub. O ambiente de testes é uma projeção dessas fontes, não um clone integral do commit original. Um índice Git local foi usado para conferir o modo executável do validator e os testes criaram repositórios temporários sintéticos.

Execução observada: Linux, CPython 3.13.5. O host canônico continua Windows com CPython 3.12. Windows PowerShell 5.1, Codex CLI, hooks despachados pelo Codex, sandbox Windows, rede do executor e publicação CQ4 não foram executados neste ambiente. Não se transporta um PASS local para essas superfícies.

## Resultados executados

| Verificação | Resultado |
|---|---|
| Suíte original completa, base auditada | 132 testes; 3 falhas reproduzidas; exit 1 |
| Validator candidato | V21; PASS; issues vazios; exit 0 |
| Suíte candidata completa | 140 métodos; 138 executados e aprovados; 2 testes Windows pendentes; exit 0 com skipped=2 |
| Resposta normal do guard Python original contra schema oficial PreToolUse | Inválida: propriedade adicional `ser_controller` |
| Resposta normal do guard Python corrigido contra o mesmo schema | Válida, decisão deny |
| Mapas de fontes produtor preflight e consumidor operacional | Iguais |
| Placeholders do prompt e substituições do produtor | Conjuntos iguais |
| Permission profiles e feature flags versus base | Semanticamente idênticos |
| Configuração executor exceto developer_instructions | Semanticamente idêntica |
| Envelope de autoridade | Blob preservado `0956016350b06ccf3ef87b9ab102c102802843c1`; 10 write roots |

Os dois testes Windows não são opcionais no PC: a suíte os executa em Windows; ausência de powershell.exe causa erro, e o preflight rejeita qualquer skipped positivo. O esperado no host é 140/140, não o aproveitamento de 138/140.

## Achados e correções

### 1. Resposta do hook incompatível com seu consumidor

Os guards externos decidiam negar, mas acrescentavam `ser_controller` à raiz do JSON. O schema oficial `pre-tool-use.command.output.schema.json` declara `additionalProperties: false`; o mesmo blob `6730b27fd4fc80f8075d64346a554a1cfc94470a` foi inspecionado nas tags `rust-v0.157.1` e `rust-v0.158.0-alpha.2.1` de openai/codex.

A incompatibilidade foi reproduzida com o subprocesso Python real recebendo stdin normal, não somente por inspeção de strings. A correção remove os campos incompatíveis, trata entradas malformadas com uma resposta de negação válida e testa a saída efetiva de subprocessos Python e PowerShell. Os testes cobrem nomes MCP/dinâmicos, controles de recursos, web, entradas inválidas e a única exceção interna esperada.

Retificação: os dois SECURITY_STOP históricos continuam resultados válidos, mas não permitem atribuir a causa exclusivamente ao Desktop sem trace de dispatch. O defeito do protocolo de resposta é independente dessa hipótese. Mantém-se a migração já aprovada para CLI; nenhum cliente foi declarado qualificado por este achado.

### 2. Três falhas reais na suíte anterior

A execução da base reproduziu uma asserção frágil a quebra de linha e duas exigências de identificadores removidos do validator durante a migração. Foram corrigidos os oráculos, preservando os critérios materiais. Não foi removida cobertura para obter verde.

### 3. Falhas dos scope guards sem resposta bloqueante confiável

Caminhos de exceção/inspeção Git podiam terminar sem JSON bloqueante. No PowerShell, uma resposta emitida numa função capturada podia ser absorvida como dado da inspeção. Os guards agora emitem a resposta diretamente na saída padrão, diferenciam falha de self-test de resposta normal e possuem testes de falha fora de um repositório Git. Nenhuma ferramenta externa é invocada por esses testes.

### 4. Instruções ativas do executor contraditórias

A seção ativa de developer_instructions encaminhava trabalho comum ao transporte de qualificação, embora o protocolo reservasse esse transporte ao CQ. A correção coloca a separação na instrução efetivamente consumida: CQ4 single-shot versus operação posterior com checkpoint e PASS canônico adjudicado. Permissões, modelos e classes de autoridade não foram alterados.

### 5. Contratos, diagnósticos e retomada

Foram reconciliadas referências normativas remanescentes do Desktop/host v6, duplicação de separadores Windows e o uso de Python host-only em CQ0.5/CQ5. O validator informa os tokens ausentes além do identificador agregado da falha.

O preflight mantém stdout/stderr separados, exibe ambos quando um subprocesso falha, cita a etapa em execução, preserva UTF-8 e aplica quoting de argumentos. Valida os remotes contra a mesma lista explícita dos transportes, fixa o scratch esperado pelos consumidores e reconfirma os hashes das fontes após os testes.

`CQ_LAUNCH_READY.json` registra a última tentativa host como IN_PROGRESS, FAIL ou PASS. Seu run_id e os hashes vinculam request/evidence/prompt. PASS significa apenas HOST_PREFLIGHT_ONLY: não é assinatura, trust, autorização nem CQ aprovado. Um preflight incompleto não libera um prompt antigo. O hash registrado para codex.cmd identifica o launcher, não prova sozinho toda a instalação binária do Codex.

O procedimento externo `RETOMAR_CQ.ps1` fica vinculado ao commit/tree publicado. Ele sincroniza por fast-forward os dois checkouts conhecidos, executa o preflight e valida o handoff; abre o CLI para revisão humana dos hooks; somente após confirmação explícita inicia uma sessão CLI nova lendo o prompt canônico por caminho/hash. Não é necessário copiar texto pelo clipboard ou pedir confirmação no chat de cada saída verde.

Uma falha interrompe o procedimento e prepara diagnóstico restrito fora do repositório. Não coleta credenciais, auth.json, configuração do usuário ou histórico de chat. A sanitização automática não substitui revisão antes de compartilhar. Não existe upload automático ou retry de falhas; somente expiração da freshness durante a revisão humana admite uma regeneração única por essa causa.

## Preservações e próximo gate

Envelope, 10 write roots, profiles A0/A1, restrições de rede, regras de transporte, implementação dos dois transportes, probe TCP, produto, outras frentes e state/journal não foram alterados nesta manutenção. A2 permanece inativa. Históricos anteriores não são reescritos como PASS.

A próxima prova obrigatória é o fresh host preflight no PC, incluindo os testes PowerShell, seguido de CQ0–CQ5 no CLI/TUI. O resultado técnico do CQ fica no bundle externo. `AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION` permanece até adjudicação independente e Human Gate CONTROLLER_MAINTENANCE. Não há autorização de B1 material, G6, Genie/Databricks material, promoção, Ready ou merge.

## Referências de implementação inspecionadas

- openai/codex, tags `rust-v0.157.1` e `rust-v0.158.0-alpha.2.1`: `codex-rs/hooks/schema/generated/pre-tool-use.command.output.schema.json`.
- openai/codex, tag `rust-v0.157.1`: `codex-rs/hooks/src/events/pre_tool_use.rs`, `codex-rs/hooks/src/engine/output_parser.rs` e `codex-rs/hooks/src/schema.rs`.
- Fontes canônicas deste repositório: config, cinco roles, três pares de guards, validator, suíte, preflight, prompt, contratos CQ, envelope, policies, delta checker, regras, transportes e probe TCP.

Os logs executados, comparação da resposta com schema oficial e manifesto dos arquivos estão no pacote externo de auditoria entregue ao usuário. Este documento registra esta manutenção sem substituir o histórico de runs nem o estado canônico de qualificação.


## Adendo — isolamento do shared background server

Uma tentativa nativa posterior ao fechamento conferiu prompt/request/evidence e parou antes de CQ0 ao observar versão/source de sessão diferentes do launcher qualificado. A investigação do código upstream 0.157.1 mostrou que o TUI pode usar um shared background server e oferece `--no-daemon` para operar sem ele. Como o servidor compartilhado pode ser de outro cliente/versão, o binding anterior ao `codex.cmd --version` não garantia sozinho que a conversa usaria o mesmo runtime.

O contrato agora exige `EMBEDDED_NO_DAEMON` e `--no-daemon` na revisão e na conversa CQ. `originator`/terminal-name é telemetria diagnóstica, não oráculo isolado de client identity. A tentativa interrompida não executou CQ0–CQ5 materialmente e não altera o blocker.


## Adendo — hooks Active mas com exit não-zero em runtime

A primeira sessão CLI embedded/no-daemon posterior exibiu repetidamente `Hook failed / hook exited with code 1` após operações read-only, antes de CQ0. Isso demonstra que `Installed/Active` e o self-test funcional não bastavam para provar a invocação normal pelo host Windows. A tentativa parou sem probes CQ.

A manutenção substitui wrappers `powershell -Command ... git rev-parse ...` por `powershell -File .codex\\hooks\\<guard>.ps1`, adiciona `exit 0` explícito no caminho normal dos scope guards e faz o host preflight executar stdin normal sintético dos três hooks (incluindo allow silencioso e deny JSON) com a mesma forma de processo Windows. O preflight passa a exigir `HOOK_WIRE_RUNTIME_SELFTEST = PASS`. Qualquer `Hook failed` visível continua bloqueante, mesmo com 2/2 e 1/1 Active.


## Adendo — contraditório final antes do próximo host run

A nova revisão encontrou quatro classes de risco que ainda poderiam gerar roundtrips ou falso PASS e as fechou em uma única manutenção:

1. **CQ3 e o oráculo errado:** os negativos de filesystem eram descritos como writes diretos, mas sem obrigar a superfície shell. Como o PreToolUse de scope também intercepta apply_patch/Edit/Write, uma negação do hook poderia ser confundida com prova do permission profile. O contrato e os cinco roles agora exigem shell/Bash + comando PowerShell WriteAllText exato, com controle read-only, sentinel preexistence/absence e NOT_PROVEN para erro não relacionado a authority.

2. **Host/runtime não idênticos para hooks:** os wire probes passam agora pelo shell Windows (`%COMSPEC% /D /S /C`) usando exatamente as strings `command_windows` canônicas, reproduzindo a forma usada pelo runtime upstream em Windows.

3. **CQ1 tarde demais:** o host preflight agora executa `codex execpolicy check` real para os dois transportes e dois negativos, exigindo prompt somente nos exatos e zero matches nos incompletos/alternativos. O contrato registra que execpolicy é prefix-based e os scripts continuam responsáveis por rejeitar sufixos/switches não suportados.

4. **Compatibilidade Windows/config:** removido o alias legado `features.connectors` (o `apps=false` canônico permanece), review/CQ passam a exigir `--strict-config`, e sidecars de CQ3/CQ4/operação foram tornados null-safe para que arquivo vazio produza diagnóstico próprio, não InvokeMethodOnNull.

Nenhuma dessas mudanças altera o envelope, os 10 write roots, A2, command network, produto ou os efeitos permitidos. O próximo host run ainda é prova obrigatória; esta auditoria não o substitui.


## Adendo — contraditório upstream dos hooks e CQ3 root probe

A revisão contra o código-fonte do Codex 0.157.1 encontrou um problema lógico adicional antes de nova execução: o pre_scope_guard casava apply_patch/Write/Edit e negava qualquer path fora dos A1 write roots. O CQ3 exige que o root A0 tente criar `.cq3_root_negative_probe.txt` para provar a negação do sandbox. Sem exceção estrita, o próprio hook poderia negar o sentinel e produzir falso PASS. Os guards agora deixam passar exclusivamente esse sentinel de qualificação; qualquer efeito inesperado continua SECURITY_STOP.

O host preflight também passou a construir payloads sintéticos com os campos obrigatórios do schema upstream PreToolUse/PostToolUse. A inspeção upstream confirmou: hooks são executados no request.cwd; no Windows o command runner usa COMSPEC/cmd.exe /C quando não há shell explícito; apply_patch usa aliases Write/Edit mas stdin canônico tool_name=apply_patch; shell-like usa tool_name=Bash; PreToolUse exit 0 + stdout vazio é allow; deny JSON válido bloqueia; PostToolUse exit 0 + stdout vazio é sucesso.


### Correção do adendo CQ3

O adendo anterior identificou corretamente o risco conceitual de confundir hook denial com sandbox denial, mas a manutenção imediatamente anterior já havia resolvido esse risco de forma mais forte: todos os negativos CQ3 foram movidos para Bash/shell e `apply_patch/Edit/Write` foram proibidos. Portanto, não é necessário nem desejável abrir exceção no scope guard para o sentinel root. Essa exceção foi revertida antes de qualquer novo host run. Mantém-se apenas a melhoria independente dos wire probes host, agora com payloads que reproduzem os campos obrigatórios do schema upstream.
