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
