# MM03 — preparação mecânica e primeiro smoke canônico

Missão local restrita, antes do freeze. Não é autorização de mudança funcional,
FULL, merge, publicação ou início de MM04. Leia primeiro o contexto canônico,
esta pasta e o protocolo de certificação da iniciativa.

## 1. Identidade e preservação

Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`.
Branch: `micromodelos/mm03-metadata-only`.
Base esperada: `073762fd8e38afadf27aca0f4d77351d9bfb627f`.
Obtenha o SHA exato da candidata no handoff/PR e reconfirme após fetch. Não invente
SHA a partir de nome de diretório. Use worktree dedicado e histórico completo;
checkout principal sujo deve permanecer intacto. Não usar reset --hard, clean,
stash automático, force-push, merge/rebase ou atualização da base por conta própria.

Se main/HEAD não coincidirem com o handoff, registre GIT_DRIFT e pare antes de
qualquer preparação. Registre HEAD/tree/main/merge-base/ahead/behind, clone não
shallow e git status completo, incluindo untracked. Identifique resíduos ignorados
sem apagar evidências. Binding local do exemplo permanece sintético.

## 2. Únicos arquivos editáveis

Somente na branch MM03 e antes do smoke:

- CHANGELOG.md: inserir a entrada exata de ENTRADA_CHANGELOG.md depois do título
  inicial, sem duplicá-la e sem alterar os demais bytes. Verificar o sufixo anterior
  por comparação binária; não normalizar quebras de linha/encoding do histórico.
- CLAUDE.md; docs/sprints/README.md; docs/sprints/micromodelos/README.md;
  docs/sprints/micromodelos/PLANO_MESTRE.md: somente a síntese viva de status de
  Micromodelos e link para MM03/README.md. MM02 integrada pela #109, MM03 candidata
  pendente de certificação. Rotular históricos em vez de apagar resultados.
- README.md raiz: somente os contadores do snapshot que o validator medir como
  divergentes. Não substituir toda a saída, não modificar validator para dar verde.

Total: seis paths. Nenhum outro arquivo pode mudar. Implementação, testes, fixture,
contrato e documentação MM03 publicados devem conservar os respectivos hashes.
Não editar ambiente_fonte, derivado, workflows, requirements ou locks.

A preservação binária é obrigatória para CHANGELOG, não apenas equivalência de texto.
Se houver necessidade de mudança fora dos seis paths, pare e devolva o finding.

## 3. Dependências e preparação

Python 3.12.x para comparação com MM01/MM02. Preferir venv existente válido ou novo
venv externo. A MM03 usa stdlib; regressões MM01/MM02 usam dependências declaradas
em tools/requirements-dev.txt. Bootstrap somente antes do smoke, sem alterar
requirements/lockfiles. Registre Python, plataforma, versões e eventuais instalações.
Não é necessário instalar Node para este smoke limitado.

Execute uma medição pré-freeze de `python -B tools/validate_assistant.py --conferir-readme`.
Conserve o log mesmo se acusar o snapshot antigo. Só as divergências previstas dos
censos podem ser corrigidas nesta missão; qualquer outra falha exige parada.
Essa medição é preparação explícita, não tentativa de FULL nem FAIL a ser ocultado.

Após os ajustes, execute diff --check e comprove o delta restrito aos seis paths.
Faça um único commit documental com mensagem `docs(mm03): preparar indices e snapshot local`.
Push normal somente à branch MM03 está autorizado para esse commit; nunca à main.
Registre pai, commit, tree, arquivos, patch e hashes antes/depois. Confirme remote
HEAD igual ao commit. Esse SHA posterior é o alvo do smoke; não atribua ao pai
resultados medidos no filho.

## 4. Smoke single-shot no SHA preparado

Use UTF-8 explícito (`PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` e
`PYTHONDONTWRITEBYTECODE=1`). Logs fora do repositório, novos e sem sobrescrita.
Execute os oito comandos de TESTES.md serialmente, capturando stdout/stderr e o
exit code real de cada processo. Pare no primeiro FAIL obrigatório e não faça
retry/patch. Verifique de novo HEAD/main/merge-base e worktree ao final.

O comando de CLI retorna um relatório de metadata, não prova autorização. Valide
os estados semânticos, as cinco operações e a ausência de detalhes da candidata
não selecionada. Não consultar Databricks ou qualquer dado real para completar a
fixture. Não chamar ferramentas que leem registros.

Não executar CI local/FULL/Actions nesta missão. PASS do smoke apenas permite
propor candidate freeze. Nenhuma etapa de auditoria independente será atribuída
a este executor nem à revisão própria do implementador.

## 5. Devolução

Relatório com PREPARATION=PASS/FAIL/NOT_STARTED e SMOKE=PASS/FAIL/NOT_STARTED,
identidade antes/depois, commit/push documental, hashes preservados, Python,
quantidades MM03/MM02/MM01/R02/R03, CLI, snapshot realmente medido, warnings/skips,
primeiro erro e estado final. Diferencie o commit documental permitido de patches
na campanha: no smoke, patches/commits/pushes/retries devem ser zero.

Entregue ZIP externo com manifest, logs, ambiente, Git, patch documental e
SHA256SUMS. Lint deve ler o ZIP real e incluir paths literais/escapados, UTF-8,
U+FFFD, duplicatas, traversal e correspondência de hashes. Conserve logs brutos
externos e crie cópias sanitizadas sem alterar fatos; registre a transformação.
A correção probatória da MM02 mostrou que inspecionar só o manifest é insuficiente.

Pare com PR Draft, MERGE=NOT_AUTHORIZED, FULL=NOT_RUN e MM04=NOT_STARTED.
