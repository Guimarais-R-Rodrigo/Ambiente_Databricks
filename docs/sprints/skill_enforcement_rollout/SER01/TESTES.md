# SER01 — testes A1 e execução delegada

## Desenvolvimento já realizado

A suíte `tools/tests/test_ser01_object_validation.py` contém 24 métodos de envelope/integridade e sete métodos de integração opt-in. Os primeiros não carregam nem simulam aprovação do catálogo completo. Os sete últimos precisam do checkout real e da autorização de evidência externa.

No Linux/Python 3.13.5 desta autoria: 24 PASS, sete SKIP explícitos por indisponibilidade do clone integral. O ensaio externo de orquestração exercitou três cenários com Git/processos reais e validators/supervisor sintéticos; confirmou fluxo positivo, reprovação da candidata inválida e reprovação de preflight malformado. Isso não é validação canônica.

Uma primeira execução de desenvolvimento encontrou duas falhas de expectativa no teste da allowlist: inserir um quinto arquivo acionava antes o limite de quatro. O teste foi corrigido para substituir um dos quatro arquivos e isolar a allowlist. O FAIL original e os logs posteriores permanecem no bundle externo. Não houve campanha certificadora congelada nem retry-until-green.

## Integrações discriminantes planejadas

1. Pacote snippet a partir de réplica sintética isolada do objeto `format_br`.
2. Pacote script a partir de réplica sintética isolada de `data_quality_check`.
3. Pacote prompt a partir de réplica sintética isolada de `eda_rapida`.
4. Notebook adicional de fixture na pasta do prompt existente.
5. README agregador de fixture na pasta scripts do piloto.
6. Notebook com sintaxe inválida: a base deve passar e a candidata deve reprovar.
7. Fachada pública incorreta: recusar, sem regenerar bytes para fazer o teste passar.

As cópias existem apenas no overlay externo. Não entram em `ambiente_fonte/` do checkout original, não são publicação, não executam os exemplos e não fabricam novas saídas analíticas.

## Preparação anterior ao freeze

O conector permitiu publicação dos novos arquivos, mas este ambiente não conseguiu clonar o Git por DNS. A aplicação preservadora da entrada em `CHANGELOG.md` e a atualização **medida** do snapshot raiz serão operações mecânicas delegadas, antes da campanha formal. Não se considera a candidata pronta enquanto isso faltar.

O executor deve usar uma worktree dedicada, preservar as worktrees A07 antigas, ler `CLAUDE.md` e regras aplicáveis, confirmar a base e preparar dependências pelos arquivos existentes. Não escolher outra arquitetura, não editar a primitive/testes, não mudar policy ou ampliar escopo.

Aplicar `ENTRADA_CHANGELOG.md` integralmente como nova seção após `# Changelog`, apenas se o título ainda não existir. Estagiar os arquivos documentais antes de medir o censo: o validator usa inventário Git. Executar o validator normal; só com aprovação estrutural medir as duas linhas `repo (identidade)`/`repo (links)` e atualizá-las no bloco do README. Não alterar outras expectativas para obter verde. Um único commit de preparação pode modificar **somente** `CHANGELOG.md` e `README.md`.

Confirmar HEAD, tree, base, merge-base, behind=0, diff permitido e worktree limpa. Esse SHA posterior à preparação é o freeze real; o SHA de autoria recebido não herda sua certificação.

## Campanha A1-LAB

Diretório externo novo, sem logs/ZIPs dentro do repo. UTF-8 explícito para o Python pai e subprocessos. Detectar host; não pressupor Linux nem Windows. Instalações e probes ambientais acontecem antes do freeze, sem alteração dos manifests/lockfiles.

Executar uma vez os testes novos, com `SER01_RUN_REPO_INTEGRATION=1` e `SER01_EVIDENCE_ROOT` externo. Comandos de referência, a resolver no host:

```text
python -B -m unittest tools.tests.test_ser01_object_validation -v -f
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/skill_enforcement/se07_policy.py
python -B tools/validate_assistant.py
python -B tools/render_simulado.py --write
python -B tools/validate_assistant.py --conferir-readme
python -B tools/ci_local.py --verbose
python -B tools/skill_enforcement/certify_local.py --profile se08 --evidence-dir <novo-diretorio-externo>
```

Remover a flag de integração do ambiente após a execução explícita da suíte SER01, para não dispará-la implicitamente em outras campanhas. Não omitir os testes SER01 por não constarem do perfil histórico SE08.

Após renderer, exigir zero drift rastreado/não rastreado. FULL só após todos os gates prévios passarem. O stderr de um teste negativo esperado pode conter FAIL da candidata sintética; quem define sucesso desse caso é seu oráculo unittest, nunca uma busca cega pela palavra FAIL. Falha do teste ou comando obrigatório encerra a campanha, preservando o restante como NOT_RUN.

## Entrega do laboratório

Identidade antes/depois; hashes dos arquivos declarativos; versões; comandos, exit codes e logs completos; registros `validation.json`; candidatos sintéticos; checksums; diff de preparação; log de commits; resultado de testes unitários versus integração; CI/FULL por canal e hash do ZIP.

Preservar bruto local. Para transporte, pode-se excluir o conteúdo volumoso `.git` dos overlays somente com inventário explícito: conservar os candidatos, base/tree, registros e logs necessários à reprodução. Não apagar ou reescrever o bruto para sanitizar.

O agente externo pode devolver `A1_LAB_PASS` ou um bloqueio/falha observado. Não pode declarar SER01 encerrada, promover L3, publicar no Free, fazer merge ou iniciar SER02.

## Corretiva pós-R1 (2026-09-23)

A R1 reprovou em `test_real_script_validation`: a réplica do script herdou o README legado sem LF terminal e a primitive recusou corretamente com `CONTENT_REQUIRES_UTF8_LF`. A corretiva altera só `replica()`, que acrescenta o LF terminal ausente à fixture positiva. Não há método novo: a suíte continua com 31 métodos (24 unitários, sete integrações). O caso negativo `"sem newline"` de `test_encoding_and_size_restrictions` permanece e deve continuar bloqueando. A R2 repete a campanha inteira, uma vez, sobre o novo SHA congelado; push só depois de todos os gates verdes.

## Corretiva pós-R2 (2026-09-23)

A R2 confirmou a corretiva de LF e expôs um falso mismatch em `canonical_public_api`: o stdout de `api_publica.py` chega com CRLF no Windows. A R3 desfaz somente pares `\r\n` desse stdout antes da comparação, sem `strip` e sem tocar no candidato. Novo método unitário `test_api_stdout_canonicalizes_only_crlf_transport` (LF preservado, CRLF equivalente, CR isolado, bytes extras e conteúdo diferente não equivalentes). Suíte: 32 métodos (25 unitários, sete integrações). Critério adicional de G1: script e snippet com `canonical_public_api=PASS` e a fachada incorreta com `canonical_public_api=FAIL`.

## Reconciliação R4 (2026-09-23)

A R3 passou localmente (32/32 no G1; G2–G8 PASS), mas não foi publicada por avanço concorrente da `main` (MM02). A R4 não altera código nem testes: a suíte continua com 32 métodos (25 unitários, sete integrações). Toda a campanha G1–G8 é repetida uma vez sobre o novo SHA composto; push somente com tudo verde e sem nova concorrência.

## A2 — Receipt de domínio e ligação à skill (2026-09-23)

A candidata A2 adiciona `scripts/object_validation.py` à skill publicada e faz o
produtor repo-side emitir `SER01-OBJECT-VALIDATION-RECEIPT-1` somente quando o
record local é PASS. `verify_record` passa a falhar fechado sem Receipt válido.

A suíte existente recebe três métodos unitários de Receipt: presença/verificação,
adulteração e mismatch de run/base/candidate. Assim, antes da nova campanha, a
coleta esperada passa de 32 para **35 métodos** (28 unitários + sete integrações),
mas esse número é expectativa da candidata, não PASS. As integrações positivas
também devem conferir o Receipt emitido.

A2 precisa de checkout completo, renderer, snapshot medido, CI e FULL sobre SHA
congelado. O laboratorio deve ainda conferir `validate_contracts`, integridade do
`release_manifest.json`, ausência de bypass sem Receipt e os claims fechados
`runtime_validation=NOT_RUN`, `execution_reverified=false` e ausência de autoridade
de apply/promoção. Nenhum resultado A1 é transportado automaticamente para A2.

## A3 — certifier prospectivo SER e bypass de record (2026-09-23)

A3 adiciona `tools/skill_enforcement/ser_certify.py` com identidade própria
`SER-CERT-1` e perfil `ser01-object-validation-pre-promotion`. Ele não altera
`certify_local.py` nem reinterpreta os perfis SE01-SE08.

O verifier publicado passa a exigir `local_record` para qualquer resultado válido.
Receipt autocoerente sem o record que o originou devolve `LOCAL_RECORD_REQUIRED`.
Os dois negativos de integração passam a assertar diretamente ausência de Receipt.

A suíte SER01 passa, por expectativa de autoria, a **36 métodos**: 29 unitários e
sete integrações. `tools.tests.test_ser_certify` acrescenta cinco regressões puras
do certifier. Contagens são expectativa até execução real.

Após preparação mecânica do renderer/snapshot e freeze, executar primeiro as
regressões de desenvolvimento e depois o certifier prospectivo:

```text
python -B -m unittest tools.tests.test_ser01_object_validation -v
python -B -m unittest tools.tests.test_ser_certify -v
python -B tools/skill_enforcement/ser_certify.py --profile ser01-object-validation-pre-promotion --evidence-dir <NOVO_DIRETORIO_EXTERNO> --evidence-authorized
```

O certifier exige checkout limpo, histórico completo, behind=0, policy L2→L3 em
`audit`, contrato/manifest/SKILL coerentes, sete records reais, cinco Receipts PASS
e dois negativos sem Receipt. Ele reexecuta regressões, validator, renderer/diff,
snapshot, CI e o FULL SE08 como `PASS_SEPARATE_CHANNEL`. Qualquer FAIL interrompe
a certificação prospectiva. O PASS não autoriza promoção por si só.

## A3-R2 — regressão do defeito STEP_SET_INVALID

A suíte prospectiva passa a exigir nomes Git distintos por fase:
`git_before_<campo>` e `git_after_<campo>`. O verifier inclui os 16 probes Git
e os 11 gates materiais no conjunto mínimo, totalizando 27 nomes únicos numa
campanha completa. Há regressão para nome duplicado, ausência de gate, fases
before/after e self-verification fail-closed do produtor.

A3-R1 em `1ff6d563824ecf3dfd80fb86c1420bb46329cf5d` permanece
`FAIL_VERIFICATION/STEP_SET_INVALID`, sem push. A próxima campanha deve usar novo
SHA e novo diretório de evidência; nenhum PASS material interno da R1 é transportado.

## Reconciliação A3-R3 (2026-09-23)

A A3-R2 passou localmente (`SER-CERT-1` PASS e certificado verificável), mas não foi publicada por avanço concorrente da `main` (MM03). A A3-R3 não altera código nem testes: `test_ser01_object_validation` segue com 36 métodos e `test_ser_certify` com sete. O `SER-CERT-1` é executado uma única vez sobre o novo SHA composto; push somente com certificado verificável e sem nova concorrência.

## Retomada A3-R3 (2026-09-23)

A primeira tentativa da A3-R3 parou antes do freeze por falha estrutural da `main@3214a131` (falso positivo MM03), corrigida pela PR #111 (`8e703f1e`). Suítes inalteradas: `test_ser01_object_validation` com 36 métodos e `test_ser_certify` com sete. O `SER-CERT-1` roda uma única vez sobre o SHA composto.

## A4 — evidência externa (2026-09-23)

`tools/skill_enforcement/ser01_free_probe.py` é notebook de probe externo e não faz parte do pacote `.assistant`. Ele testa release/contrato, verifier de Receipt no runtime Free, tamper/replay, claims fracos, policy ainda L2 e ausência de mutação do pacote publicado. Sua fixture positiva é explicitamente `INTEGRITY_ONLY_NOT_EXECUTION_PROOF`; ela não substitui a execução repo-side já provada na A3.

`A4_RUNBOOK_FREE.md` exige dry-run/publicação/verify rápido/completo/conteúdo e execução única do probe. `A4_GENIE_CASES.md` fixa cinco chats novos para rota indisponível, bypass, Receipt inválido, autoridade limitada e negativo de roteamento. Preservar respostas literais e separar task correctness, agent adherence e canonical compliance.

A4 não requer mudança em `ambiente_fonte`; qualquer delta em produto desde `fcec3e34...` bloqueia a execução e volta ao ChatGPT.

### A4-FREE R2 — regressões específicas

- o probe deve compilar sem gerar artefato versionado;
- F01 deve exigir explicitamente `producer_is_published_artifact=false`;
- `validate_assistant.py --conferir-readme` deve passar com 1732/2176 ou com nova medição real se a árvore tiver mudado;
- autenticação renovada não transporta nenhum resultado funcional da R1;
- publicação e probe usam nova rodada/evidência e não reutilizam outputs R1.

## Certificação pós-promoção

`tools/skill_enforcement/ser_promotion_certify.py` usa identidade `SER-PROMOTION-CERT-1` e profile `ser01-object-validation-post-promotion`. Exige policy L3/L3, `policy_status=implemented`, `audit`, `stage_specific`, artifacts L3, route/evidence gates e regressões estruturais. SE07/SE08 são executados como canais históricos e só são aceitos se falharem exclusivamente nas assertions temporais L2 conhecidas; qualquer failure adicional reprova.

A campanha deve ocorrer em novo SHA preparado/renderizado, evidence root externo novo, sem retry-until-green. O PASS não autoriza merge; apenas torna a candidata apta ao gate humano específico.

### Promotion certifier R2

- identidade `SER-PROMOTION-CERT-2` / prefixo `serprom2:`;
- teste de policy pré-promoção usa fixture mockada e não depende do estado real;
- árvore atual L3 precisa passar `_promotion_gate` e route gate pós-promoção;
- classificador temporal exige conjunto exato de FAILs e zero ERROR;
- campanha executa sua própria regressão, piloto L3 legado, policy-I/O, certifier local e CI não-SEF;
- `test_ser_certify` pré-promoção entra como canal histórico separado com um único FAIL temporal esperado;
- summary é persistido em `finally` após qualquer exceção posterior à reserva de evidência.
