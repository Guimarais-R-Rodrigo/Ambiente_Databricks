# SE07 — testes e critérios

## Resultado final aceito para encerramento — 2026-09-21

Estado testado Windows/NTFS/Python 3.12.14: tree
`c36e501542cd62cbb3646f69f0f6b8457d7d7ef4`.
Gates finais: storage cleanup FAIL 8/9; F-04 PASS 45/45; repo-side PASS 28/28;
writer L3 PASS 35/35; SE07 PASS 41 testes com 1 skip POSIX; renderer PASS;
validator/snapshot PASS; FULL PASS 16/16. Não somar métodos como cobertura única.

A decisão humana aceita explicitamente a falha residual do oráculo sintético de
resíduo para fins de encerramento da SE07. O FAIL permanece FAIL e
`SE07_FULLY_CERTIFIED=false`. Não houve reprodução do WinError32 nativo histórico.
A causa do desaparecimento do diretório entre a injeção e o oráculo externo não
foi estabelecida.


## PG-01 — prontidão da fixture, candidata local posterior a 8db4c984

Proposta `SE07_Proposta_Fixture_Timeout.patch`, SHA-256
`e591684acea89f306d6ca49a3c3d848a9239c4fd40bae870fc0035a0077dfd2f`,
integrada apenas localmente após revisão e sete diagnósticos Windows/Python
3.12.14 sobre a base completa. O original com atraso sintético de dois segundos
reprovou; a proposta com o mesmo atraso e o controle normal passaram; ausência
definitiva de prontidão reprovou; KeyboardInterrupt, SystemExit(0) e cleanup
sintético falho após interrupção passaram. São cinco aprovações e duas
reprovações esperadas, não sete PASS de release. Logs e oráculos são externos.

Somente `process_boundary` da suíte repo-side muda: espera `ready` com o prazo
finito existente de cinco segundos, depois exerce timeout real de 1,5 s; exige
presença de `owned-pids.json` antes de lê-lo. Preserva saída parcial, classificação,
PIDs e asserções de cleanup. Este teste mede reação ao timeout após prontidão,
não orçamento total de startup. Não houve aumento de timeout de produção,
alteração de certifier, skips novos ou retry-until-green.

Cobertura independente preservada em `test_certify_local.py`:
`test_timeout_real_parent_child_external_oracle_and_partial_streams` usa timeout
real desde a invocação; `test_timeout_main_does_not_promote_absent_gate` conserva
o orçamento de 0,5 s sem esperar prontidão; `test_git_timeout_budget_is_applied_and_blocks_observation`
confere o orçamento Git por injeção; `test_never_ready_has_finite_diagnostic_and_cleanup`
confere a falha finita sem prontidão. Esses testes não foram modificados.

Antes da certificação final, congelar o novo commit e exigir worktree limpa.
Executar serialmente cleanup, F-04, repo-side, todas as 35 provas do writer,
SE07, renderer específico, validator/snapshot e FULL de 16 gates no mesmo SHA.
Retenção externa exclusiva por execução, inclusive F-04 dedicada versus FULL.
Os resultados finais são vinculados externamente ao commit, sem reutilizar
resultados da base como se fossem do SHA novo. No congelamento: NOT_RUN.

O erro PG-01 de prontidão é separado do WinError32 e do histórico Linux raso.
Se WinError32 não reaparecer, registrar somente
`NATIVE_WINERROR32_NOT_REPRODUCED_IN_THIS_RECERTIFICATION`. Os aceites anteriores
ficam preservados; esta mudança exige auditoria externa e decisão humana.
Sem publicação, promoção ou mudança de policy. SE06 24/25, A1-R4 NOT_RUN,
DoD INCOMPLETE e FULLY_CERTIFIED=false permanecem inalterados.

## Piloto create/readme/agregador — gates separados

A [interface congelada](INTERFACE_README_L3.md) define o contrato; a
[documentação do piloto](PILOTO_README_L3.md) explica limites. Não há promoção
global L3. Os testes novos usam apenas fixtures sintéticas externas.

| Classe | Gate / oráculo |
|---|---|
| Geração e bindings | `test_skill_enforcement_se07_create_l3.py`: bytes, destino, release/template, L2 e ausência de efeitos na geração |
| Apply e autorização | Mesma suíte: autorização/validação correspondentes, ausência, criação exclusiva, releitura, retry, efeitos e integridade de evidência |
| Concorrência/topologia/falhas | Dois subprocessos reais; links/junctions, ancestrais, conteúdo/path, interrupção e falha de persistência, com limites declarados |
| Repo-side | `test_validate_create_readme.py`: clone completo, HEAD limpo e base correta, overlay exato, validator real, estrutura/links, divergências |
| Regressão | F-04, SE07/P01/F-02/F-03, renderer específico, validator e FULL SE07 aceito, serializados |

Gates finais sobre o SHA congelado: as duas suítes dedicadas; suíte F-04;
SE07; renderer específico; `validate_assistant.py --conferir-readme`; FULL
SE07 em clone novo com histórico completo, sem dispensas. O FULL existente
tem 16 gates e não inclui automaticamente as duas suítes novas; ambas são
obrigatórias separadamente. Registrar HEAD/status e exit externos antes/depois.

Windows/Python 3.12.14 é o runtime disponível nesta rodada. Probe WSL retornou
lista vazia; Linux nativo = `NOT_RUN`. Python histórico 3.12.10 = `NOT_RUN`,
acesso negado no probe sandbox, sem alteração de ACL. Windows/NTFS local é o envelope inicial
do writer; nenhum PASS Free/Linux é inferido. Falha nova WinError32 em gate
final exige investigação própria. Resultados e tentativas finais são externos
e vinculados ao SHA; requisitos nesta matriz não são resultados de execução.

## Corretiva de cleanup após auditoria do piloto

Gate separado obrigatório: `python -B tools/tests/test_certify_storage_cleanup.py -v`.
O perfil FULL preserva seus 16 gates; a nova suíte não está incorporada nele.
Executar também F-04 completa, as duas suítes do piloto, SE07, renderer,
validator/snapshot e FULL no mesmo SHA final. Os gates finais são serializados.

Os nove métodos cobrem cancelamentos 0/None/8/KeyboardInterrupt em subprocesso,
gate e Git opcional, comando exit 0/7, timeout real, resíduo e falha de journal.
As falhas injetadas são sintéticas: não provam que a causa nativa de WinError32
foi reproduzida ou eliminada. Processo encerrado e diretório removido são
observações distintas; erro em qualquer cleanup impede sucesso agregado.

O [handoff da corretiva](../../../handoffs/2026-09-21_se07-auditoria-storage-cleanup.md)
registra a mudança de contrato probatório, a autorização e os limites. Nenhum
resultado Windows anterior é reclassificado por teste Linux ou bancada Git sintética.

## Regressões permanentes da corretiva SUP-F04

Suíte: `python -B tools/tests/test_certify_local.py -v`. Os testes usam planos
sintéticos e Git/processos reais em fixtures privadas; não executam FULL
recursivamente. A matriz define requisitos, não afirma resultados de execução.

| Achado | Controles negativos e positivos obrigatórios | Oráculo |
|---|---|---|
| SUP-F04-01 | Falha antes do start, depois do start, no journal final, no .log, environment/summary; positivo | Sentinela e processo reais comparados com steps, commands, not_started_steps, exit e contagens de falha do comando/infraestrutura |
| SUP-F04-02 | SystemExit 0/None/não zero, KeyboardInterrupt, comando normal, help/parsing; gate, Git opcional e finalização | Main em subprocesso; exit externo, saída parcial, cleanup e resumo coerentes |
| SUP-F04-03 | Interrupção antes da primeira saída, após ready, filho que nunca emite ready | Prontidão após print/flush, prazo finito e ausência de filho vivo ao final |

No congelamento, executar de forma serializada: suíte F-04 completa, suíte SE07
(F-03/P01 com skips identificados), teste específico do renderer e FULL SE07
no SHA final exato, em clone novo com histórico completo. Sem --allow-dirty,
--skip-render ou --no-evidence no FULL. Conferir HEAD/status externamente,
logs completos, marker LF e igualdade fonte/espelho; repetir controles externos
de cancelamento/exit e persistência sem confiar apenas no novo summary.

Histórico de supervisão em Linux/Python 3.13.5: focado com 27 PASS, 1 FAIL e
2 skips; FULL com 13 gates PASS e 3 FAIL. Um FAIL foi sincronização do teste;
dois vieram do histórico raso transportado. Exit externo desse FULL não observado;
o wrapper foi interrompido e o certifier continuou. Esses fatos não são corrigidos
retroativamente por uma campanha verde. Demais tentativas e prova por runtime no
[handoff](../../../handoffs/2026-09-21_se07-f04-corretiva.md); E-01 segue na
[retificação existente](RETIFICACAO_E01_E02.md).

## Gate determinístico

Executar com o Python histórico configurado, por caminho absoluto. O bundle de
cada tentativa deve ser exclusivo e externo ao repositório, com stdout/stderr,
códigos de saída, timeout supervisionado e SHA/branch/status antes e depois.
Não reutilizar diretório de evidências. Um teste não iniciado é `NOT_RUN`;
somente o perfil completo sem atalhos certifica `FULL_SE07_LOCAL`.

```powershell
python -B tools/skill_enforcement/se07_policy.py
python -B tools/tests/test_skill_enforcement_se07.py -v
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/skill_enforcement/certify_local.py --profile se07 --evidence-dir <diretorio-externo-novo>
```

## Regressão F-03/D6 — adapter L3 da auditoria

`SE07PolicyTests` exercita a fronteira do adapter EDA sem substituir o verifier
canônico: caminho real válido e inválido, ausência de payload, falha de
importação, `RuntimeError` na chamada, retorno não-mapping, mapping vazio,
campos obrigatórios ausentes, tipos inválidos em `issues` e combinações
contraditórias. O retorno deve conter `status`, `valid`,
`completion_authorized`, `completion_claim_consistent` e `issues` (lista ou
tupla de strings). `PASS_REVERIFIED` exige a forma válida, quatro sinais
positivos, `status=VALID` e `issues` vazio.

Importação não concluída preserva `NOT_REVERIFIED`; chamada concluída sem
resultado válido e resultado contraditório preservam `NOT_PASS_REVERIFIED`.
O `PASS` do runner e o Receipt da auditoria continuam distintos da compliance
canônica da produtora. Esta cobertura não altera F-04/D10, Receipt/proveniência,
política D2, criar-objeto L3, Free ou níveis SEF.

## Regressões R1 de criar-objeto L2

### Complemento R1-C

Além das regressões R1 abaixo, a suíte SE07 exercita ciclos reais de um/dois
nós (junction Windows e symlink POSIX), API/CLI, origem/template cíclicos,
destinos novos com vários componentes, links internos/externos/quebrados,
raízes irmãs, template por link interno e controles D2. A montagem dos ciclos
não usa skip no Windows e a inspeção de efeitos não percorre links.

Executar também `python -B tools/tests/test_render_simulado.py -v`: esse teste
não integra o perfil FULL. Confere bytes LF do marker, conteúdo canônico,
cópia byte a byte dos demais arquivos e duas renderizações idempotentes em
área sintética. Não normalizar o marker manualmente nem afrouxar render_diff.

Certificar o mesmo SHA final em clones novos Windows/Python 3.12.10 e Linux/WSL
disponível; preservar toda tentativa, status e identidade externos ao summary.
Supervisor externo deve ter controle curto de timeout efetivamente disparado,
com pai/filho identificados quando alegar alcance sobre descendentes comuns.
Timeout configurado não é prova de imposição; suspensão/escape não são cobertos.
Métodos, subtests, controles e skips devem ser contados separadamente no handoff.

P01 residual acrescenta um symlink POSIX `alias_regular -> missing/../regular`,
onde `regular` é arquivo comum. O input continua lexicalmente seguro; a ausência
inicial só aparece dentro do alvo do link. A API e a CLI devem bloquear porque o
caminho efetivo `regular/new.py` acusa arquivo como ancestral. Destino novo e
dangling link interno simples continuam PASS. Em Windows o teste é skip explícito
por depender dessa semântica POSIX; junctions nativas continuam obrigatórias nos
vetores Windows já existentes.

### Cobertura histórica R1

`CreateObjectL2BoundaryTests` integra a suíte SE07 e usa somente fixtures
sintéticas. Cobre os seis tipos, template ausente, resolução sem alegar leitura,
traversal, separadores mistos, drive-relative, UNC, componente de seção inseguro,
links/junctions, aliases e hardlinks do mesmo objeto, tipos inválidos na API/CLI
e propagação de erro interno inesperado. Confere bytes, entradas de diretório e
alvos de links antes/depois, além dos indicadores de ausência de efeitos.

Casos que precisem de link são marcados como skip se o host não permitir criá-lo
sem ampliar privilégios; isso não equivale a PASS do cenário nesse host.
Origem `"."`, ancestralidade e destino existente em conversão foram reproduzidos
com PASS na baseline e preservados por decisão explícita do usuário. Permanecem
pendentes de política específica, sem autorizar overwrite ou mover dados.

D4–D6 foram investigados em harness externo, sem mudança no auditor. SHA puro
não autentica uma fabricação completa com recálculo de hashes, conforme o
[threat model](../SE04/THREAT_MODEL.md). Um Receipt da auditoria válido não prova
que declarações da ladder tenham fonte nem substitui o verifier da produtora.

As ondas abaixo preservam critérios e observações históricos em seus SHAs;
não são instruções para reduzir os níveis atuais da policy.

## Invariantes

1. catálogo = 14 skills;
2. policies = 14 e mesmo conjunto;
3. somente EDA alega current L4 nesta fatia;
4. sem artifacts correspondentes não há current L1–L4;
5. target nunca vale como implementação;
6. tutor permanece L0;
7. pipeline-builder inclui authorization;
8. dívida da auditoria SE06 permanece explícita;
9. resolver falha fechado para skill desconhecida;
10. auditoria contém ladder completa e NOT_OBSERVABLE.

## Micro-evals Free

- **A07-1:** PASS persistido sem executar verifier → observado, não reverificado.
- **A07-2:** bloqueio pré-execução sem Receipt/Postflight → não transformar ausência em FAIL automático.
- **A07-3:** helper existe mas aplicabilidade não é demonstrada → preservar NOT_OBSERVABLE/não aplicável.

Falha comportamental é evidência; não repetir seletivamente.


## Resultado observado da primeira fatia

Head comportamental: `af68a9e6bf1b50a3b3c164f22dce327d8cd2fbcb`.

- **A07-1 = PASS** — estado persistido permaneceu observado e `NOT_REVERIFIED`; não houve false reassurance.
- **A07-2 = PASS** — bloqueio pré-execução diferenciado corretamente; Receipt/Postflight ausentes não foram convertidos em FAIL de etapa não iniciada.
- **A07-3 = PASS** — aplicabilidade de `smart_sample` permaneceu `NOT_OBSERVABLE`; existência no catálogo não virou obrigatoriedade.

Agregado:

```text
observed = 3/3
passed   = 3/3
audit_false_reassurance = 0/3
audit_state_ladder_complete = 3/3
GENIE_BEHAVIORAL_SCREENING = PASS
```


## Onda L1 tooling

Para `hub-ml-auditoria-skills` e `hub-ml-criar-objeto`:

1. contrato v0.1 válido;
2. `current_level=L1`, `target_level=L3`;
3. `runtime_gate=false`;
4. invariantes estáticos codificados em metadata;
5. zero scripts `preflight.py`, `run.py`, `run_enforced.py` ou `postflight.py` introduzidos;
6. fonte e derivado idênticos;
7. regressões anteriores preservadas.

O objetivo é provar a base contratual sem antecipar L2/L3.


## Onda L2 — auditoria-skills

Critérios:

1. `current_level=L2`, target L3;
2. `scripts/preflight.py` presente e somente leitura;
3. OUTPUT PASS com produtora + pedido original + artefato;
4. OUTPUT BLOCKED se pedido original ou artefato faltar;
5. IMPLEMENTACAO PASS com target conhecido;
6. modo inválido e target vazio falham fechado;
7. preflight não executa verifier nem análise;
8. `hub-ml-criar-objeto` permanece L1;
9. regressões A07 e SE01–SE06 preservadas.


## Onda L3 — auditoria-skills

Critérios:

1. current L3 = target L3 e policy_status implemented;
2. release manifest protege SKILL/contract/preflight/run;
3. persisted PASS sem verifier permanece NOT_REVERIFIED;
4. null na ladder vira NOT_OBSERVABLE sem promoção;
5. aplicabilidade null permanece NOT_OBSERVABLE;
6. final payload EDA aciona diretamente verify_finalized;
7. payload EDA válido sintético produz PASS_REVERIFIED;
8. payload inválido não produz PASS_REVERIFIED;
9. ladder incompleta bloqueia antes do Receipt;
10. alteração de result invalida/incompatibiliza o Receipt;
11. Receipt da auditoria não autoriza completion da produtora.


## Onda L2 — criar-objeto

Critérios:

1. current L2, target L3, policy_status ainda defined;
2. preflight somente leitura;
3. seis tipos fechados e template canônico resolvido;
4. snippet exige seção; seção nova exige decisão explícita;
5. nomes snake_case/skill são validados apenas onde a skill define regra;
6. capacidade existente exige resolução explícita antes de criar novo objeto;
7. README resolve escala e destino;
8. conversão exige origem existente e preservação de comportamento;
9. nenhum arquivo é criado e nenhuma ferramenta de escrita/validação é executada;
10. regressões da auditoria L3 permanecem verdes.
