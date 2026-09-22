# SE08 — corretiva R1: portabilidade e diagnóstico de cleanup

**Estado: REVIEW_PARCIAL_PARA_INTEGRACAO_LOCAL. Não é RC, FULL, aceite ou promoção.**

## Identidade e reconciliação

Base desta revisão: `c99174cffeb00372fb7936ed07f7948b6427b622`, tree
`b7ee483b505e87caafa402bbe0680602a4828578`, encontrada em
`sef/SE08-corretiva-windows-ci`. Seus dois commits, posteriores a `25013c53`,
acrescentam telemetria do certifier e um teste. Foram preservados sem reatribuição.

A revisão usa `sef/review-SE08-diagnostico-r1`; não altera a branch encontrada,
`sef/SE08-operacao` nem `main`. Na reconciliação, a canônica permanecia em
`25013c53db37be0984604df3c463e98cb42949e2` e a main em
`c70f5af9b4108f2d99c79ba678719347e91fc910`.

A candidata do Codex é LOCAL: `e3e67bced219bfb1d78ac80b0c5a8d29f86678fc`,
parent `3118e9707fadd9bd37b3fea3d9504aba2be0a0b9`, tree
`7cf62a7169ce8de72debf8dbebf453bddb7572e2`. Ela não é ancestral desta revisão.
Não perder seus dois commits ou repetir materialização manualmente: integrar
os dois históricos em clone completo e certificar o novo SHA resultante.

## Alterações delimitadas

1. `tools/tests/test_temas_v02.py`: cinco seletores de mocks usam
   `path.as_posix()` em vez de `str(path)`; dois subprocessos sem dependências
   usam `-I -S`, preservando a inserção explícita do produto em `sys.path`.
   Sete linhas alteradas. Os 78 nós de asserção/skip permaneceram idênticos por AST.
2. `test_temas_v02_portability.py`: oito testes dos predicados reais extraídos
   por AST, com PurePosixPath/PureWindowsPath e subprocesso contaminado por
   PYTHONPATH/cwd como controle negativo. Não é execução Windows da suíte V02.
3. `tools/skill_enforcement/se08_diagnostics.py`: observador opt-in para separar
   cleanup explícito, finalização automática e falha nativa. Não muda os gates
   nem a implementação de cleanup do certifier. Não integra automaticamente o FULL.
4. `test_se08_diagnostics.py`: 17 testes do instrumento, incluindo falhas da
   consulta, restauração dos hooks, erros do journal, proteção de diretório e
   identidade Git. Mocks de usuários de arquivo NÃO são prova nativa Windows.

Não foram alterados produto `.assistant`, policy, níveis, release manifests,
asserts da suíte de storage, permissões, dependências, thresholds ou timeouts
dos gates existentes. Nenhum skip novo contorna falta de privilégio de symlink.

## Resultados executados

Linux 6.18.44 x86_64 / CPython 3.13.5, componentes por bytes, sem checkout
completo do repositório. SHA de arquivo não equivale a execução da tree inteira.

| Tentativa | Métodos | Exit | Observação |
|---|---:|---:|---|
| 01 baseline de portabilidade | 8 | 1 | 12 failures, incluindo subcasos |
| 02 portabilidade corrigida | 8 | 0 | zero failures/errors/skips |
| 03 instrumento inicial | 13 | 0 | não substitui a bateria final |
| 04 adversarial da consulta | 14 | 1 | um ERROR: erro diagnóstico mascarava a exceção original |
| 05 consulta corrigida | 14 | 0 | exceção original preservada |
| 06 adversarial Git | 17 | 1 | um FAIL: identidade alterada permitia exit zero |
| 07 guarda Git corrigida | 17 | 0 | case_exit separado de wrapper_exit |
| 08 conferência final portabilidade | 8 | 0 | zero failures/errors/skips |
| 09 conferência final instrumento | 17 | 0 | zero failures/errors/skips |

As duas últimas execuções ocorreram em processos independentes e diretórios
exclusivos, sem mutação dos arquivos. Logs, comandos, horários e hashes de cada
rodada ficam no bundle externo. Repetições não são somadas como cobertura única.
ResourceWarning no ensaio de finalização automática foi preservado.

## Instrumento e limites

O CLI exige SHA completo, worktree limpa e diretório externo inexistente:

```powershell
python -B tools/skill_enforcement/se08_diagnostics.py --case capabilities --expected-sha <SHA_LOCAL_CONGELADO> --evidence-dir <NOVO_DIRETORIO_EXTERNO>
python -B tools/skill_enforcement/se08_diagnostics.py --case f04-never-ready --expected-sha <SHA_LOCAL_CONGELADO> --evidence-dir <OUTRO_DIRETORIO_EXTERNO> --query-resource-users
python -B tools/skill_enforcement/se08_diagnostics.py --case storage-residue --expected-sha <SHA_LOCAL_CONGELADO> --evidence-dir <TERCEIRO_DIRETORIO_EXTERNO>
```

`capabilities` verifica a criação real de links de arquivo/diretório sem elevar
privilégios; indisponibilidade retorna exit 1, não aprovação nem skip.

`f04-never-ready` executa o caso original F-04 sob observação. Em WinError32,
a consulta opcional ao Restart Manager ocorre DEPOIS da falha, limitada ao
arquivo temporário da invocação. Consulta apenas PID, criação, sessão e tipo;
não solicita shutdown/restart ou fechamento de handles. A sessão de diagnóstico
registra recursos no Windows e é encerrada; não é uma alegação de ausência de
efeitos internos no sistema operacional.

Uma lista vazia ou erro de consulta não prova ausência histórica de handles.
O instante posterior e os hooks podem alterar o timing. A ABI ctypes e a consulta
nativa NÃO foram executadas nesta bancada: validar com controle positivo no
Windows antes de usar como evidência de dono de recurso. Isso tampouco é uma
contagem exaustiva de handles. Não concluir causa raiz somente de um PID retornado.

`storage-residue` executa diretamente o probe interno sintético original,
não o método de teste externo completo. Exit 130 é a interrupção esperada, não
certificação PASS. O instrumento registra finalização automática sem suprimir
cleanup. A coleta explícita de objetos depois do caso é identificada como
`POST_CASE_GC_REQUESTED`; não precede nem substitui o oráculo original.

Os hooks do observador usam uma fronteira privada do tempfile do CPython:
compatibilidade precisa ser confirmada em Python 3.12.14. Não destacar
finalizers, não alterar assertions e não chamar de resolvido o residual histórico.

Executar cada diagnóstico sob supervisor externo com prazo finito previamente
definido e captura de stdout/stderr/exit. A chamada nativa síncrona não oferece
prazo interno garantido. Se atingir o prazo, preservar evidência parcial e
classificar como interrupção/timeout diagnóstico, nunca PASS. Não iniciar um
processo subsequente até conferir o encerramento dos processos próprios.

## Integração local e pendências

A revisão ainda não contém a materialização nem o changelog dos dois commits
locais. Criar branch local nova a partir de e3e67bce, conferir histórico e integrar
esta revisão por merge normal, sem force ou reset destrutivo. Não fundir branches
compartilhadas antes de avaliar eventuais avanços.

A entrada desta execução está em [CHANGELOG_CORRETIVA_R1.md](CHANGELOG_CORRETIVA_R1.md).
**Sua incorporação ao CHANGELOG raiz está PENDENTE.** Não foi reconstruído um
arquivo histórico de mais de 212 kB a partir de resposta truncada. Incorporar o
fragmento preservando as entradas Codex da candidata local e todo histórico.
O snapshot do README deve ser medido novamente, nunca ajustado por estimativa.
Essas pendências impedem classificar a revisão como repo-side certificada.

Após integração/documentação e congelamento: testes novos, testes V02 reais,
F-04, storage cleanup separado, writer, validator/renderer/snapshot, FULL SE08 e
CI conforme a matriz vigente. A campanha nativa e a integração do instrumento
com os testes reais são pendentes, não substituídas pelos 25 métodos da bancada.

Separar quatro investigações: WinError32 nativo; finalização automática da fixture;
portabilidade/isolamento dos testes; capacidade de symlink e configuração Python
base versus launcher do venv. Não usar uma configuração verde para apagar outra.

## Estados preservados

- SE06: 24/25; S06-A1-R4=NOT_RUN; SE06_DOD=INCOMPLETE; FULLY_CERTIFIED=false.
- SE07: SE07_FULLY_CERTIFIED=false; storage cleanup histórico FAIL 8/9.
- WinError32 não reproduzido na recertificação histórica permanece datado;
  o nativo observado na SE08 local também permanece. WINERROR32_FIXED não foi declarado.
- Criar-objeto L2 global; target L3, stage_specific, audit.
- Free/Genie/PR/Actions/promoção NÃO executados. PROMOCAO_TRABALHO=BLOQUEADA.

## Referências técnicas consultadas

- Python 3.12, opções `-I` e `-S`: https://docs.python.org/3.12/using/cmdline.html
- Python 3.12, TemporaryDirectory: https://docs.python.org/3.12/library/tempfile.html
- Microsoft, RmGetList: https://learn.microsoft.com/en-us/windows/win32/api/restartmanager/nf-restartmanager-rmgetlist
- Microsoft, RmRegisterResources: https://learn.microsoft.com/en-us/windows/win32/api/restartmanager/nf-restartmanager-rmregisterresources

Essas referências fundamentam o desenho, não comprovam execução na máquina do usuário.
