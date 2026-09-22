# SE08 — corretiva de instrumentos e diagnóstico de cleanup

Data: 22/09/2026. Autor: ChatGPT.

**Estado: WIP_REVIEW_REQUIRES_NATIVE_DIAGNOSIS. Não é RC, FULL aprovado,
aceite humano ou autorização Free/Genie/trabalho.**

## Identidade e separação das linhas

A fonte remota reconciliada foi `sef/SE08-operacao` em
`25013c53db37be0984604df3c463e98cb42949e2`, com main em
`c70f5af9b4108f2d99c79ba678719347e91fc910`.
A candidata Windows entregue pelo Codex é local:

```text
25013c53db37be0984604df3c463e98cb42949e2
  -> 3118e9707fadd9bd37b3fea3d9504aba2be0a0b9
  -> e3e67bced219bfb1d78ac80b0c5a8d29f86678fc
```

Tree nativa: `7cf62a7169ce8de72debf8dbebf453bddb7572e2`.
A review `sef/review-SE08-corretiva-20260922` nasce da base remota, não de e3e67bce.
Ela não recria nem substitui os dois commits locais. A integração deve preservar
ambas as histórias e a materialização já executada pelo Codex.

O primeiro commit corretivo é `c06fcdf2065e2812fab25392445614957163d8cf`:
portabilidade de testes V02. A instrumentação e este documento pertencem ao
complemento seguinte. Resolver o HEAD da review antes de usar; não atribuir
evidência de componentes ao commit inteiro.

## Prioridade 1 — diagnóstico, não correção presumida do WinError32

`tools/skill_enforcement/cleanup_diagnostics.py` executa um caso por invocação,
com journal externo exclusivo, identidade Git anterior/posterior, hashes dos
fontes, UTC/relógio monotônico e resultados originais preservados.

Os hooks são temporários e restaurados no processo diagnóstico. Observam:

- entrada/saída do diretório temporário, cleanup explícito e finalizer implícito;
- existência dos arquivos próprios stdout/stderr/child.json e metadados lstat;
- estado dos streams do caller na entrada do cleanup;
- registros de processos sem reescrever seus resultados;
- no Windows, contabilidade e PIDs do Job Object próprio antes/depois de
  assign/terminate/close;
- opcionalmente, usuários dos dois arquivos pelo Restart Manager após WinError32.

Não altera `certify_local.py`, `_WindowsJob`, timeouts, algoritmos de remoção,
privilégios, guards ou testes históricos. Não desativa finalizer, não repete
remoção, não fecha handles/aplicações de terceiros e não chama RmShutdown/RmRestart.
O registro transitório de recursos no Restart Manager não é uma operação sem
qualquer efeito no sistema; serve somente ao diagnóstico opt-in.

Uma lista vazia do Restart Manager significa ausência de correspondências
reportadas, não prova ausência de handles. Consulta incompleta, erro ou limite
de buffer não são sucesso. A consulta ocorre após a falha, não mede
retroativamente o instante exato do erro.

## Prioridade 2 — correção delimitada dos instrumentos de CI

Em `tools/tests/test_temas_v02.py`, somente sete substituições foram feitas:
cinco predicados de caminhos usam `path.as_posix()` em vez de `str(path)`;
duas sondas de dependências usam `-I -S` em vez de apenas `-S`.

Os callbacks foram exercitados por AST com PureWindowsPath/PurePosixPath;
as flags foram exercitadas em subprocessos reais com PYTHONPATH sintético.
Não foram alterados oráculos finais, dependências instaladas, lógica visual,
thresholds, testes de symlink ou skips para obter verde.

`test_se08_ci_portability.py` contém quatro métodos de regressão.
`test_se08_cleanup_diagnostics.py` contém 25 métodos do observador, incluindo
ABI Win32 de largura fixa, doubles da API, propagação de erros, journal,
finalização automática, aliases de evidência e preflight sem elevação.
Doubles de Win32 não são execução do kernel Windows.

`test_skill_enforcement_se08.py::load_tests` incorpora essas duas suítes ao
step SE08 já chamado pelo FULL e pelo CI, sem recursão de perfis. Os oito métodos
anteriores mantêm a semântica da candidata nativa; a montagem da identidade
sintética em runtime foi portada da correção do Codex em 3118e970, não é nova
correção atribuída ao ChatGPT.

## Resultados efetivamente observados

Ambiente: Linux 6.18.44 x86_64, CPython 3.13.5. Árvore parcial de componentes,
não clone completo do produto. Fontes originais foram conferidos por hash de blob.

| Ensaio | Resultado | Limite |
|---|---|---|
| Portabilidade, baseline | 4 métodos; 7 falhas de subcasos; zero skips | callbacks/isolamento, não suíte visual completa |
| Portabilidade, corrigido | 4/4 PASS; exit 0; zero skips | não Windows nativo |
| Observador final | 25/25 PASS; exit 0; zero skips | APIs nativas substituídas por doubles |
| Storage original, sem alteração | 9/9 PASS; exit 0; zero skips | Linux; não reclassifica FAIL Windows |
| Fixture original sob observação | exit 130 preservado; resíduo presente no oráculo | diagnóstico, não aprovação da campanha |
| Wiring por AST | 30/30 PASS | 29 regressões novas + um marcador sintético da suíte original |
| Suíte F-04 original, duas tentativas | INCOMPLETE_EXTERNAL_TOOL_TIMEOUT | sem resumo unittest final nem exit do filho observado |

As suítes corretivas finais foram também executadas em paralelo, em dois
subprocessos independentes: 4/4 e 25/25. Repetições não são cobertura única extra.
A integração completa dos oito testes originais com os 29 novos não foi executada
nesta bancada; 37/37 é uma expectativa de composição, não resultado observado.

A primeira tentativa F-04 foi interrompida pelo limite externo da ferramenta.
A segunda corrigiu a configuração externa, mantendo o limite de 120 s do wrapper,
mas a ferramenta voltou a encerrar sem resultado final. Ambas mantêm logs parciais
com classificação de interrupção externa. Nenhuma foi promovida a PASS.

### Hipótese de finalização automática

O microteste do observador confirma que um erro injetado antes do __exit__ original
pode deixar a limpeza implícita ativa. Porém, na fixture ORIGINAL executada aqui,
o resíduo permaneceu no oráculo e a limpeza explícita de teardown da própria
fixture ocorreu antes do finalizer. Isso NÃO reproduz o desaparecimento anterior
ao oráculo observado no Windows. Consequentemente, a fixture não foi alterada.

A causa nativa do WinError32 e a causa do desaparecimento Windows continuam
pendentes. O código existente já termina o Job Object, consulta ActiveProcesses
e espera o launcher; uma espera arbitrária adicional não é correção demonstrada.

## Uso local — ordem obrigatória

1. Confirmar a candidata local e3e67bce, tree, worktree limpa e refs remotas.
2. Integrar a review em branch local separada por merge normal, preservando e3e67bce
   e os dois commits do Codex. Inspecionar qualquer conflito, nunca force/reset.
3. Incorporar o fragmento de changelog e medir o snapshot real do README no clone
   completo. Não copiar contagens de uma tree diferente.
4. Congelar o SHA integrado e a configuração do interpretador/dependências.
5. Rodar testes corretivos e diagnósticos em diretórios externos NOVOS.

Definir `$Python` como caminho real do interpretador escolhido e `$EvidenceRoot`
como diretório externo autorizado. Registrar essas resoluções nos metadados, nunca
inferir que venv e Python base possuem a mesma topologia de PIDs.

```powershell
& $Python -B tools/tests/test_se08_ci_portability.py -v
& $Python -B tools/tests/test_se08_cleanup_diagnostics.py -v
& $Python -B tools/skill_enforcement/cleanup_diagnostics.py --case preflight --out "$EvidenceRoot/preflight"
& $Python -B tools/skill_enforcement/cleanup_diagnostics.py --case never-ready --out "$EvidenceRoot/never-ready"
& $Python -B tools/skill_enforcement/cleanup_diagnostics.py --case storage-finalizer --out "$EvidenceRoot/storage-finalizer"
```

Cada comando deve passar pelo supervisor externo local com stdout/stderr separados,
exit observado, timeout finito definido ANTES de começar e retenção dos processos
próprios. Não aumentar prazos após falha para obter verde. Timeout do supervisor
não é resultado observado do teste; preservar os dois níveis.

Para observar usuários dos arquivos, acrescentar `--restart-manager` ao caso
never-ready somente em campanha explicitamente identificada como instrumentada.
Isso pode perturbar timing; resultado sem WinError32 não certifica correção.
Não executar em loop até obter um resultado preferido.

Preflight pode devolver BLOCKED por WinError1314. Ele não muda Developer Mode,
ACLs ou privilégios e não converte o bloqueio em skip. É necessário ambiente
permitido para exercer os testes de symlinks; uma troca desse ambiente deve ser
registrada, e não ser uma exceção silenciosa.

No caso storage-finalizer, o exit 130 pertence ao cancelamento sintético da fixture.
O objetivo é observar a sequência, não exigir exit 0. Comparar events.jsonl com
storage-oracles.json, observations.json e o exit externo. O journal pode receber
eventos de finalizer durante encerramento do processo, após a gravação do resumo;
hashear o bundle somente DEPOIS de confirmar o término do processo.

## Depois do diagnóstico

Somente correção causalmente sustentada pode mudar cleanup/fixture. Novo código
exige nova candidata, testes adversariais, regressões F-04/storage/writer e FULL
SE08/CI no SHA final. Não usar um PASS isolado para apagar FAIL anterior.
Se não houver causa suficiente, devolver o diagnóstico completo e manter bloqueio.
A presente autorização não permite mudar arquitetura/policy/nível ou aceitar uma
nova exceção de promoção corporativa.

## Pendências e preservação

Não houve execução Windows, FULL SE08, validator/snapshot do clone completo, Free,
Genie, PR, Actions ou merge de release nesta rodada. A canônica remota e main
permanecem fora da escrita. O derivado desta review ainda é o da base remota;
a versão materializada válida pertence à candidata local e deve ser preservada
na integração. Nenhum arquivo derivado foi editado à mão.

A incorporação de [CORRETIVA_20260922_CHANGELOG.md](CORRETIVA_20260922_CHANGELOG.md)
ao CHANGELOG raiz permanece PENDENTE: não foi reescrito um histórico de 212 kB
a partir de retorno truncado. O fragmento é rastreabilidade provisória, não
substituição do registro obrigatório. O snapshot numérico também deve ser medido
após integrar as novas adições; os números antigos não certificam esta review.

SE06: 24/25, S06-A1-R4=NOT_RUN, SE06_DOD=INCOMPLETE, FULLY_CERTIFIED=false.
SE07: encerramento humano com residual conhecido, SE07_FULLY_CERTIFIED=false;
storage cleanup histórico FAIL 8/9 preservado. WinError32 não declarado corrigido.
Criar-objeto permanece L2 global, target L3, stage_specific, audit.
PROMOCAO_TRABALHO=BLOQUEADA. Nenhum resultado desta rodada remove essas condições.

## Referências técnicas externas consultadas

Estas referências fundamentam os mecanismos, não os resultados dos testes do Hub:

- Python 3.12, opções -I/-S e PYTHONPATH: https://docs.python.org/3.12/using/cmdline.html
- Python 3.12, TemporaryDirectory e cleanup implícito: https://docs.python.org/3.12/library/tempfile.html
- Microsoft, RmGetList: https://learn.microsoft.com/en-us/windows/win32/api/restartmanager/nf-restartmanager-rmgetlist
- Microsoft, RM_PROCESS_INFO e RM_UNIQUE_PROCESS: https://learn.microsoft.com/en-us/windows/win32/api/restartmanager/ns-restartmanager-rm_process_info
- Microsoft, TerminateJobObject: https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject
