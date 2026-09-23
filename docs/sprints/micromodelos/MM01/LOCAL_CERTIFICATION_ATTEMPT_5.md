# MM01 — Local Certification v1 — tentativa 5

Data da execução: 2026-09-22

Status do executor: **PASS**

Status da revisão de integridade do bundle: **NÃO ACEITA COMO CERTIFICAÇÃO FINAL v1**

## Veredito mecânico

A execução canônica R5 foi iniciada uma única vez e retornou exit code 0.

O manifest registra:

- `status=PASS`;
- `preflight_ok=true`;
- `postflight_ok=true`;
- `failure=null`.

Identidade:

- HEAD: `3e3e105f60e92f6ca58502cf0c92f4f461a84b04`;
- tree: `55dced926406bee8c216cd97d2dc55c9e1ba093d`;
- `origin/main`: `11851e137dd7793b351ac08fc211c0be90005dee`;
- merge-base: `11851e137dd7793b351ac08fc211c0be90005dee`;
- `ahead_by=175`;
- `behind_by=0`;
- worktree limpa;
- checkout não shallow;
- merge-ref materialmente equivalente ao HEAD.

## Integridade mecânica do bundle

SHA-256 do ZIP:

`c812454ecd011e99172f802d06ae556c830486fd2afd21bf5aec035bf72cf3fb`

A revisão independente do ZIP confirmou:

- 55 entries;
- 54/54 checksums internos válidos;
- 50 step results;
- 49 steps `PASS`;
- somente `V12_SCOPE_STRICT=SKIP_ALLOWED`;
- nenhum required step ausente ou extra;
- 17 hashes críticos idênticos antes/depois;
- preflight e postflight com estado Git idêntico.

## Gates

Passaram integralmente:

- cinco bootstraps;
- `CERT_SELFTEST`: 15/15;
- `MM01_CANONICAL`: 47/47;
- `MM01_R02`: 3/3;
- `MM01_R03`: 1/1;
- `MM01_VALIDATE_ASSISTANT`: 0 falhas / 0 avisos;
- `CI_LOCAL`: 10/10 subgates;
- V00;
- V01;
- V02;
- V10;
- V11;
- V12;
- V13.

O snapshot real validado foi:

- `repo (identidade)=1677`;
- `repo (links)=2109`;
- `worktree (extras)=0`.

Os regressions V10/V11/V12/V13 executaram 742 testes por rodada, com skips internos de plataforma/escopo preservados pelas próprias suítes.

## Finding da revisão do bundle

Apesar do PASS mecânico, a revisão direta dos bytes do ZIP encontrou caminhos locais do diretório pessoal persistidos em sete logs quando as próprias suítes imprimiam caminhos Windows em representação escapada com barras duplicadas.

Arquivos afetados:

- `logs/V00_REPORT.log`;
- `logs/V01_TESTS.log`;
- `logs/V02_TESTS.log`;
- `logs/V10_REGRESSIONS.log`;
- `logs/V11_REGRESSIONS.log`;
- `logs/V12_REGRESSIONS.log`;
- `logs/V13_REGRESSIONS.log`.

O comando lógico/resolvido do certifier estava sanitizado. A falha ocorria quando output produzido pelo subprocesso serializava ou representava o mesmo path com escaping adicional.

## Por que o finding é bloqueante para a certificação local

`LOCAL_CERTIFICATION_V1.md` exige:

- sanitizar paths locais nos registros probatórios;
- sanitizar paths/tokens antes de persistir ou emitir cada linha do streaming.

Portanto:

- o manifest R5 continua historicamente `PASS`;
- os gates funcionais continuam historicamente PASS;
- a R5 não é reclassificada como failure funcional;
- porém o bundle R5 não satisfaz integralmente o próprio contrato probatório v1 e não deve ser usado como bundle final de certificação para a auditoria independente.

## Correção posterior

O sanitizador foi endurecido para redigir variantes de path:

- literal;
- normalizada com slash;
- com backslashes escapados em níveis sucessivos.

A regra é aplicada tanto a `<REPO>` quanto a `<HOME>`.

Commits:

- `cb9f97375e6effaddbfff7569c64c3cafdbce503` — sanitização de paths Windows escapados;
- `74b0929433a58b4a17959fbb84cc85bb06407127` — regressão explícita das variantes escapadas.

Nenhum gate funcional, workflow ou critério da MM01 foi relaxado.

## Próximo passo

Executar nova certificação integral em SHA novo e diretório probatório novo.

A próxima rodada deve exigir, além de todos os gates R5:

1. ausência do path local literal;
2. ausência de sua forma escapada;
3. ausência de sua forma duplamente escapada;
4. ausência dessas formas em todos os logs, manifest e arquivos do bundle.

R1–R4 permanecem FAIL. R5 permanece PASS mecânico com bundle probatório não aceito para fechamento final.

MM01 continua não aceita e não integrada. MM02 permanece bloqueada.
