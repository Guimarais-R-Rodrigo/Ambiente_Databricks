# MM01 Local Certification v1

Status: contrato operacional da certificação local da MM01.

## 1. Finalidade

A indisponibilidade do GitHub Actions altera o canal de execução da evidência, não os requisitos técnicos da MM01.

A MM01 Local Certification v1 é o executor mecânico e fail-closed que substitui, para a candidata MM01, a execução anteriormente realizada pelos jobs permanentes do GitHub Actions. Ela não decide aptidão para merge, não substitui auditoria independente, contraditório final nem aceite humano.

A fonte canônica continua sendo o repositório GitHub. O executor local opera somente sobre checkout real da branch `micromodelos/mm01-contrato-canonico`.

## 2. Garantias obrigatórias

Uma certificação só pode terminar com `PASS` quando, simultaneamente:

1. o repositório remoto é exatamente `Guimarais-R-Rodrigo/Ambiente_Databricks`;
2. a branch local é exatamente `micromodelos/mm01-contrato-canonico`;
3. `HEAD` coincide com o SHA completo fornecido ao executor;
4. `origin/main` coincide com o SHA completo fornecido ao executor;
5. `merge-base(HEAD, origin/main)` é exatamente o SHA esperado de `main`;
6. `behind_by=0`;
7. o checkout não é shallow;
8. a worktree está limpa antes e depois;
9. Python é 3.12 e o ambiente Python vive fora do repositório;
10. Node é major 22 e pnpm termina exatamente em 10.34.5;
11. não existem resíduos gerados prévios nos paths controlados;
12. todos os inputs críticos mantêm o mesmo SHA-256 antes/depois;
13. todos os gates obrigatórios terminam com exit code 0;
14. somente skips explicitamente allowlisted podem ocorrer;
15. o estado Git pós-execução é idêntico ao preflight;
16. o bundle probatório é produzido fora do checkout;
17. qualquer erro, drift, ausência de input, alteração de estado ou gate não-zero produz `FAIL` ou erro fatal.

## 3. Fonte dos gates

Os comandos locais são derivados dos workflows permanentes relevantes:

- `.github/workflows/ci.yml`;
- `.github/workflows/micromodelos-mm01-ci.yml`;
- `.github/workflows/temas-v00-ci.yml`;
- `.github/workflows/temas-v01-ci.yml`;
- `.github/workflows/temas-v02-ci.yml`;
- `.github/workflows/temas-v10-ci.yml`;
- `.github/workflows/temas-v11-ci.yml`;
- `.github/workflows/temas-v12-ci.yml`;
- `.github/workflows/temas-v13-ci.yml`.

O executor não trata esses YAMLs como ambiente de execução. Eles são a especificação de origem dos gates.

Para impedir drift silencioso, cada workflow-fonte possui identidade Git blob congelada em `tools/mm01_local_certify.py`. Qualquer edição em qualquer um desses arquivos — inclusive inclusão de novo gate — bloqueia a certificação até reconciliação deliberada do certifier. A presença de snippets continua sendo validada como segunda linha de defesa.

## 4. Gates executados

O plano contém bootstrap, self-test do certifier, suíte MM01, regressões R02/R03, `validate_assistant`, `ci_local.py` e os gates transversais V00, V01, V02, V10, V11, V12 e V13.

O único skip allowlisted é `V12_SCOPE_STRICT`, porque o próprio workflow V12 declara esse gate `NOT_APPLICABLE` para PRs cuja head não seja `codex/temas-v12*`. Nenhum outro gate pode ser marcado como skip.

## 5. Execução

Em um checkout dedicado e limpo, com Python 3.12 e Node 22 disponíveis:

```bash
git fetch --all --prune
git checkout micromodelos/mm01-contrato-canonico
git reset --hard <SHA_CANDIDATO>
git status --short

python -B tools/mm01_local_certify.py \
  --expected-sha <SHA_CANDIDATO> \
  --expected-main-sha <SHA_MAIN> \
  --output-dir <DIRETORIO_FORA_DO_REPOSITORIO>
```

O diretório de saída não pode existir previamente e precisa estar fora do checkout.

## 6. Bundle probatório

O executor produz:

- `manifest.json`: status, SHA candidato, SHA da main, tree SHA observada, todos os steps, exit codes e escopo da decisão;
- `preflight.json`: identidade Git, branch, tree SHA, merge-base, ahead/behind, limpeza, remote, runtime base, hashes dos inputs e drift dos workflows;
- `postflight.json`: estado Git final e prova de igualdade com o preflight;
- `environment.json`: Python, plataforma, Git, pip, Node, npm, pnpm e pacotes instalados;
- `inputs_sha256.json`: hashes dos inputs críticos;
- `logs/<STEP>.log`: stdout/stderr consolidado de cada gate;
- `SHA256SUMS.txt`: SHA-256 de todos os arquivos do bundle;
- `<bundle>.zip`: pacote final;
- SHA-256 do ZIP impresso no stdout.

O bundle é evidência mecânica. Ele não é uma decisão de governança.

## 7. Fail-closed

A execução para no primeiro gate não-zero. Mesmo em falha, o executor tenta capturar postflight, grava manifest com `FAIL`, checksums e ZIP.

Erros de preflight, divergência de SHA, branch incorreta, `origin/main` incorreto, `behind_by>0`, checkout shallow, worktree suja, runtime incompatível, input crítico ausente, workflow alterado, alteração de arquivo crítico durante a execução ou estado Git pós-execução diferente tornam a certificação inválida.

## 8. Independência e decisão final

Depois de um bundle `PASS`:

1. o SHA permanece congelado;
2. uma conversa separada executa auditoria independente sobre GitHub + bundle + adversariais próprios;
3. os achados são comparados exclusivamente com `MATRIZ_ACEITE_FINAL.md` e ADRs aceitos;
4. somente após auditoria limpa ocorre contraditório final;
5. o bloco MM01 do `CHANGELOG.md` é então sincronizado de forma byte-preserving;
6. a árvore final é revalidada;
7. o usuário fornece aceite explícito;
8. somente então a PR #51 pode ser integrada.

MM02 permanece bloqueada até esse fluxo terminar.

## 9. Fronteiras

A certificação local não:

- cria requisitos novos para R01–R08;
- altera validadores para “fazer passar”;
- acessa Databricks corporativo;
- executa publicação;
- usa credenciais de produção;
- substitui governança externa;
- transforma evidência local em aceite humano;
- autoriza merge automaticamente.


## 10. Portabilidade Windows

A execução local precisa funcionar tanto em ambientes POSIX quanto no Windows.

No Windows, entrypoints de ferramentas Node podem existir como shims `.cmd`/`.bat` em vez de executáveis `.exe`. O certifier deve:

- resolver o comando pelo PATH/PATHEXT;
- executar shims `.cmd`/`.bat` pelo command processor definido em `COMSPEC`;
- continuar usando execução sem shell para executáveis normais;
- falhar de forma fechada quando o comando não puder ser resolvido;
- registrar separadamente no bundle o comando lógico do gate e o comando efetivamente resolvido;
- sanitizar paths locais nos registros probatórios.

Essa adaptação é exclusivamente de transporte do comando no sistema operacional. Ela não altera o conteúdo lógico dos gates nem permite substituir comandos.


## 11. Interrupções controláveis

Interrupção não é sucesso.

Se um step receber `KeyboardInterrupt` e o processo Python continuar com controle suficiente para tratar o evento, o certifier deve:

- registrar o step com `status=INTERRUPTED`;
- manter `exit_code=null`;
- gravar log específico da interrupção;
- registrar `reason`;
- interromper o plano fail-closed;
- tentar coletar postflight;
- produzir manifest, checksums e ZIP de falha.

O handler externo também captura `KeyboardInterrupt` quando possível para preservar a trilha probatória.

Esse mecanismo não promete recuperar terminação externa abrupta que encerre o processo sem devolver controle ao Python. Nessas situações, a ausência de manifest/postflight/ZIP continua sendo evidência de uma execução incompleta e nunca pode ser reinterpretada como PASS.


## 12. Saída incremental dos steps

Os steps não devem permanecer silenciosos até o subprocesso encerrar.

O certifier executa os gates com tee incremental:

1. grava previamente no log o comando lógico;
2. grava o comando efetivamente resolvido;
3. lê stdout/stderr combinado linha a linha;
4. sanitiza paths/tokens antes de persistir ou emitir;
5. grava cada linha imediatamente no log;
6. faz flush do log;
7. emite a mesma linha sanitizada no stdout do certifier;
8. faz flush do stdout.

O streaming é probatório e operacional. Ele não altera o comando, não muda o environment do gate, não considera output textual como substituto do exit code e não permite continuar depois de falha.

Se ocorrer interrupção controlável durante o streaming, o log parcial já emitido permanece disponível e o step é registrado como `INTERRUPTED` quando o processo Python conserva controle.


## 13. Fechamento de pipes do streaming

O tee incremental deve fechar explicitamente o pipe de stdout do subprocesso depois do consumo.

A regressão do certifier trata `ResourceWarning` nesse caminho como erro. Isso impede que um step seja considerado operacionalmente limpo enquanto deixa file handle aberto.

A regra não altera o comando executado, seus argumentos, o environment, o exit code ou a classificação PASS/FAIL do gate.


## 14. Sanitização de representações escapadas

A sanitização de paths locais deve cobrir não apenas a forma literal produzida pelo sistema operacional, mas também representações serializadas/escapadas emitidas por subprocessos e frameworks de teste.

Para `<REPO>` e `<HOME>`, o certifier deve redigir pelo menos:

- forma literal;
- forma com separador normalizado para `/`;
- forma com backslashes duplicados;
- forma com níveis adicionais de escaping razoavelmente produzidos por `repr`, JSON ou mensagens de teste.

A regra se aplica ao output incremental antes de persistência ou emissão.

Um bundle que contenha path local identificável em qualquer dessas representações não satisfaz integralmente o contrato probatório v1, mesmo que todos os gates funcionais tenham exit code 0.


## 15. Encoding determinístico e console-safe

O transporte de stdout/stderr dos gates deve ser determinístico em Windows e não pode derrubar a certificação por limitações da página de código do terminal.

Para todos os subprocessos executados por `run_step`, o certifier deve:

- definir `PYTHONUTF8=1`;
- definir `PYTHONIOENCODING=utf-8`;
- decodificar o stream capturado como UTF-8;
- persistir o log em UTF-8;
- tentar emitir o texto sanitizado no stdout corrente;
- se o encoding do terminal não representar algum caractere, usar fallback não destrutivo/ASCII-safe em vez de lançar `UnicodeEncodeError`.

O fallback de console não altera o conteúdo probatório persistido no log e não muda o exit code do subprocesso.

A regressão deve cobrir explicitamente:

- subprocesso Python com stdout efetivamente UTF-8;
- console `cp1252/charmap` recebendo caractere não representável sem abortar o step.
