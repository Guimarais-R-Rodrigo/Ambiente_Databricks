# B1 P2 — primeira campanha real governada

## Estado

Esta entrega materializa a arquitetura repo-side da P2 para a dupla SER03 L3 mensal/binária + SER05 L2 contexto. Ela **não executa a campanha, não certifica e não promove** as skills.

A P1 integrada permanece vinculada ao commit `d2b6079ee2e6ecec628d14411afbdbdb878a5fb9`. A P2 adiciona somente infraestrutura de campanha, testes e documentação; os bytes funcionais das fachadas P1 não devem ser alterados por esta etapa.

## Decisão arquitetural

O B0 mantém registry e release identity deliberadamente fechados em comandos `b0:*`. O `launcher.py` e o `verifier.py` importam o resolver B0 diretamente. Portanto, criar apenas outro JSON de comandos não produziria uma campanha verificável.

A P2 usa um adapter aditivo em `tools/skill_enforcement/real_campaigns/b1/`. Ele:

1. mantém `tools/skill_enforcement/parallel/**` byte-idêntico à base;
2. define registry B1 fechado, com command IDs e argv exatos;
3. cria release spec B1 que liga SHA/tree/base, registry, coverage, policy, host, interpreter e digest dos componentes B0 reutilizados;
4. injeta o resolver/validator B1 somente no processo que chama o launcher/verifier B0 e restaura os globals no `finally`;
5. reutiliza scheduler, lease, sandbox, process supervision, result schema e verifier B0;
6. mantém campanha read-only, effects `NONE` e concorrência qualificada `2/1`.

Não existe segundo scheduler, segundo sandbox, segundo verifier de processo ou engine paralelo.

## DAG

As duas frentes começam independentes:

```text
SER03 preflight ─→ SER03 execute+Receipt+verify ─→ SER03 domain audit ─┐
                                                                    ├─→ evidence/coverage audit
SER05 preflight ────────────────────────→ SER05 domain audit ───────┘
```

O scheduler B0 decide ondas e recursos. `max_parallel=2`; `max_auditors=1`. Auditorias de domínio compartilham a classe `audit`, e o auditor de evidência/coverage só libera após ambas.

## Comandos e efeitos

O registry B1 contém apenas comandos Python exatos sobre:

- fixtures sintéticas versionadas;
- preflights P1;
- runner/Receipt/verifier SER03;
- auditorias de domínio;
- negativos discriminantes selecionados;
- verificação da cobertura.

Todos declaram `effects=none`. O sandbox B0 continua bloqueando escrita fora de scratch, subprocessos filhos e rede.

## Coverage

`coverage_registry.json` fecha o vínculo de 19 casos no escopo com:

`case_id → test_id P1 → oracle_id → command_id P2 → evidência`.

CE03, CE04, CE09, CE11 e CE12 permanecem explicitamente fora da etapa L2, sem serem reinterpretados como PASS.

## Gates locais ainda necessários

Nenhum resultado deste commit deve ser chamado de LOCAL_PASS antes de uma execução local, no mesmo SHA, em checkout limpo:

1. `python -B -m tools.skill_enforcement.real_campaigns.b1.preflight`;
2. `python -B -m unittest tools.tests.test_ser_b1_campaign -v`;
3. `python -B -m tools.skill_enforcement.real_campaigns.b1.prepare --output-dir <diretorio-externo-novo>`;
4. executar **uma única vez** o `execution_argv` gerado no `HANDOFF.json`;
5. auditar o bundle/evidence resultante antes de freeze/certificação.

Cada gate é fail-fast, sem retry-until-green. O diretório `EVIDENCE` precisa não existir antes do launcher.

## Autoridade

P2 não altera `policy.json`. SER03 permanece current L0/target L3 e SER05 current L0/target L4 até campanha, auditoria, eventual prova externa pertinente e gate humano específico.

Não autoriza Ready, merge, Databricks Free/Genie, SER06 ou 3/2.


## Endurecimento pós-contraditório repo-side

O contraditório do primeiro commit P2 identificou dois gaps antes da execução local e ambos foram fechados em autoria:

- a identidade B1 agora exige correspondência exata, arquivo por arquivo e de fileset, com todo o diretório `tools/skill_enforcement/parallel/**` qualificado na PR #113/main `4ba7f551...`; não é permitido rebinding silencioso a um B0 futuro;
- o handoff passou a carregar `profile_digest` top-level e por task, derivado de registry, coverage, B0 qualificado, adapter, recursos e target vector.

O preflight também prova que os bytes funcionais P1 permanecem idênticos a `d2b6079...` e `prepare` recusa diretório de saída dentro (ou acima) do repositório. Essas mudanças ainda são autoria: exigem os gates locais no novo SHA.


## Envelope de evidência P2

Após a tentativa única da campanha, o adapter persiste `ADAPTER_RESULT.json` no output externo. O `post_run_package_argv` do handoff executa `package_evidence`, que reutiliza `parallel.bundle.build_share`, sanitização V2 e `verify_raw_share_binding`. O RAW recebe manifesto e permanece privado; o SHARE recebe identidade própria, secret/path scan e verificação de envelope. O artefato destinado à auditoria remota é o ZIP SHARE sanitizado com SHA-256 registrado no verdict externo.

Empacotar evidência após um FAIL não constitui retry do gate: é preservação da primeira tentativa. A campanha não é reexecutada.


## Bundle público de auditoria

O arquivo a retornar não é mais um ZIP contendo apenas o SHARE. O empacotador cria um `*_AUDIT_BUNDLE.zip` com:
- `SHARE/**` sanitizado e seu manifesto;
- `RAW_SHARE_BINDING.json` (somente hashes/scan, sem bytes RAW);
- `ENVELOPE_VERIFICATION.json`;
- `AUDIT_CONTEXT.json`, com identidade da campanha, status, SHA candidato e hashes dos sidecars;
- manifesto do próprio audit bundle e scan final.

O RAW não entra no audit bundle. Assim, o auditor remoto consegue revalidar integralmente o conteúdo compartilhado, o scan e os sidecars públicos; a autenticidade dos bytes RAW permanece limitada ao hash/binding e à verificação local, como previsto pelo contrato de evidência.


## Autoridade ambiental do perfil 2/1

A qualificação B0 observou Windows, NTFS, sandbox negativo, Windows Job Object, recursos e concorrência 2/1. A P2 não transporta esse limite para outro host por mera compatibilidade de código. O preflight B1 atual exige `Windows` + filesystem `NTFS`; execução em Linux/Cloud ou Windows não-NTFS retorna bloqueio ambiental antes de preparar a campanha.

Outro host poderá ser usado somente após uma qualificação ambiental própria e uma alteração versionada dessa autoridade; isso não faz parte desta P2.


## Bootstrap do interpretador após R1

A primeira tentativa local em `3149ff6...` encerrou antes de iniciar Python porque o handoff usava o alias literal `python`, ausente no PATH daquela sessão. O histórico está preservado em `P2_R1_FAILURE.md`.

A correção é exclusivamente de bootstrap. `resolve_python_windows.ps1` roda antes do primeiro gate formal, não escreve no repositório e não executa nenhum gate P2. Ele procura candidatos Python 3 via ambiente, `Get-Command`, `py.exe -3` e instalações locais; cada candidato precisa provar seu próprio `sys.executable`. O output PASS fornece `python_executable` real.

P2-01, P2-02 e P2-03 devem então ser chamados por esse caminho exato. P2-03 congela o mesmo `sys.executable` no release spec e os argv gerados continuam SHA/release-bound. Falha do resolver é `BLOCKED_ENVIRONMENT`, não um retry de P2-01.


## R2 bloqueada e resolver V2

R2 comprovou Windows/NTFS e identidade Git, mas o resolver V1 não encontrou Python 3; nenhum gate formal iniciou.

R3 amplia exclusivamente a descoberta pré-gate para PythonCore Registry, USERPROFILE/ProgramData Conda-Miniconda-Miniforge-Mambaforge, pyenv-win, Rye, Scoop, stores do uv, ProgramFiles(x86) e roots legados. Não há instalação, download, criação de venv ou mudança de PATH.

O schema passa a `SER-B1-WINDOWS-PYTHON-RESOLUTION-2`. Se V2 falhar, nenhuma nova alteração automática de resolver deve ser feita: tratar o host como sem Python 3 utilizável observável e exigir remediação ambiental explícita fora da campanha.


## R3 bloqueada: WindowsApps não é prova de ausência de Python

O resolver V2 abortou ao avaliar `WindowsApps/python.exe` com PermissionDenied antes de emitir seu JSON. Esse path é um App Execution Alias e não deve ser tratado como executável Python comprovado.

R4 introduz resolver V3:
- exclui aliases `Microsoft\WindowsApps`;
- isola erros de path/registry/root por candidato;
- registra `discovery_issues` sem abortar a busca;
- não inclui paths sensíveis nos registros de tentativa;
- usa trap top-level para emitir JSON em exceção residual;
- preserva `formal_gate_executed=false` e `writes_performed=false`.

Somente um FAIL JSON válido do V3 com `PYTHON3_INTERPRETER_NOT_RESOLVED` será suficiente para classificar o host como sem Python 3 utilizável observável e partir para remediação ambiental explícita.
