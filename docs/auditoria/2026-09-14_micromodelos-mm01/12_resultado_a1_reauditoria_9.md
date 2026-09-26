# RELATÓRIO DE REAUDITORIA FINAL INDEPENDENTE — MM01

> Nota de preservação: o identificador pessoal presente no nome completo do repositório foi sanitizado para cumprir o gate de higiene do próprio projeto. Nenhum achado, evidência técnica, classificação ou veredito desta auditoria foi alterado.

## 1. Identificação

- Repositório: `Ambiente_Databricks` (repositório privado; owner sanitizado neste registro histórico)
- Branch: `micromodelos/mm01-contrato-canonico`
- HEAD auditado: `4dc6bb12d2e4df6c3dbff7aa4711a99bf660bb6b`
- main: `1d46c9625fb5bfd6d1b666ddff055507238788bf`
- Merge-base: `1d46c9625fb5bfd6d1b666ddff055507238788bf`
- ahead_by: `125`
- behind_by: `0`
- PR: `#51` — aberta; `merged=false`; `draft=false`; `mergeable=true`; `mergeable_state=clean`; `125` commits; `29` arquivos alterados.
- Merge-ref: `3de9090ef8c035b0c43541b6a87ea21fab44120d`
- Python: GitHub Actions `CPython 3.12.14`; runner temporário dos adversariais isolados `Python 3.13.5`.
- Dependências: no runner Actions do SHA auditado: `jsonschema 4.26.0`, `PyYAML 6.0.3`, `regex 2026.9.10`, `NumPy 2.5.3`; a suíte permanente é instalada a partir de `tools/requirements-dev.txt`.
- Limitações de ambiente: o ambiente desta auditoria não conseguiu efetuar checkout Git privado diretamente por shell por indisponibilidade de resolução de rede para `github.com`. Por isso, a reprodução da árvore completa foi baseada no HEAD/merge-ref obtidos diretamente do GitHub e no runner real do GitHub Actions do SHA exato. Os adversariais adicionais foram reexecutados localmente contra as funções/predicados exatos inspecionados no HEAD. Nenhuma mutação no repositório, branch, refs, PR, documentação ou workflows foi realizada.

## 2. Estado Git e mergeabilidade

| Item | Resultado | Evidência |
|---|---|---|
| HEAD da branch | `4dc6bb12d2e4df6c3dbff7aa4711a99bf660bb6b` | Estado atual da PR e commit Git. |
| `main` | `1d46c9625fb5bfd6d1b666ddff055507238788bf` | Base atual da PR; também é pai direto do HEAD reconciliado. |
| Merge-base | `1d46c9625fb5bfd6d1b666ddff055507238788bf` | Compare GitHub `main...HEAD`. |
| `ahead_by` | `125` | Compare GitHub retornou `status=ahead`, `ahead_by=125`. |
| `behind_by` | `0` | Compare GitHub retornou `behind_by=0`. |
| Integração real da `main` | PASS | HEAD é merge commit `chore(mm01): reconciliar main apos V13 S0`; seus pais são `e4567870e52d03b9a435dba3dd102c00215451aa` e a `main` atual `1d46c962...`. |
| Commits atuais da PR | `125` | REST atual da PR. |
| Arquivos alterados | `29` | REST/compare atuais; superfície restrita a MM01, documentos compartilhados previstos, workflow e requisitos de manutenção. |
| Estado da PR | aberta | `state=open`. |
| `merged` | `false` | Estado atual da PR. |
| `draft` | `false` | Estado atual da PR. |
| `mergeable` | `true` | Estado atual da PR. |
| `mergeable_state` | `clean` | Estado atual da PR; o texto histórico do corpo da PR não foi usado como autoridade. |
| Merge-ref | `3de9090ef8c035b0c43541b6a87ea21fab44120d` | Merge sintético atual da PR. |
| Tree SHA do HEAD | `1dfb5ff6ed6469472bd87e6063ef5723b7f2214a` | Commit Git do HEAD. |
| Tree SHA do merge-ref | `1dfb5ff6ed6469472bd87e6063ef5723b7f2214a` | Commit Git do merge-ref. |
| HEAD × merge-ref | PASS — árvores materialmente idênticas | Mesma tree SHA; o merge-ref não introduz mudança material inesperada. |
| Perda/reimplementação de frente externa | Não observada | O diff atual contra `main` contém os 29 arquivos esperados da MM01 e documentação compartilhada; não há `.assistant`, runtime V13, crawler, skill MM04, binding corporativo ou implementação visual própria. |

## 3. Execuções reproduzidas

| Execução | Resultado | Evidência objetiva |
|---|---|---|
| `python -m pip install -r tools/requirements-dev.txt` | PASS | Run MM01 `35036376210`, job real `104606295866`, Ubuntu 24.04.5; step de instalação concluído `success`; NumPy foi efetivamente instalado antes da regressão R03. |
| `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v` | PASS | Mesmo job: `47` testes, `OK`. A suíte foi inspecionada, e não apenas seu status. |
| `python -B -m unittest tools/tests/test_micromodelo_mm01_r03.py -v` | PASS | Mesmo job: regressão R03 executada após instalação do NumPy, `1` teste, `OK`. O teste usa `np.float64`, injeta-o em limiar e peso e exige `SCHEMA`. |
| `python -B tools/validate_assistant.py --root ambiente_fonte` | PASS | Mesmo job: `APROVADO — 0 falha(s), 0 aviso(s)`. |
| CLI sobre `micromodelo.template.yaml` com `--schema` | PASS | O comando exato é executado como subprocesso pela suíte permanente; exige retorno `0`, `SNAPSHOT_VALIDO` e `HISTORICO_NAO_CERTIFICADO`. A mesma regressão também comprova `APROVADO_EVOLUCAO` quando `--previous` é fornecido. |
| Template × schema/validador | PASS | Template canônico percorre o caminho positivo da suíte de 47 testes. |
| Fixture `valido_validado.json` | PASS | Fixture completa de fase `VALIDADO`, com aprovações, experimento `EXECUTADO/MEDIDO`, tracking ainda sem contrato MM06 e autoridade `GOVERNANCA_EXTERNA`. |
| Workflow MM01 permanente | PASS | Run `35036376210`; checkout, Python, instalação, contrato/mutantes, gate estrutural e fronteira concluíram `success`. |
| Workflow V12 transversal | PASS | Run `35036376279`, job `104606296293`: resultado global `success`; `Aplicabilidade do escopo estrito V12=success`; `Escopo V12 e higiene=skipped`. O workflow atual calcula explicitamente `applicable=false` para PR alheia à V12. |
| HEAD × merge-ref | PASS | Árvores idênticas `1dfb5ff6...`. |
| Adversariais temporários R01–R08 | FAIL material em R02 | R01 e R03–R08 produziram o comportamento esperado; R02 revelou sobrecanonicalização de pontuação inicial, detalhada abaixo. |

## 4. Cobertura da MATRIZ_ACEITE_FINAL

| Requisito | Status | Evidência |
|---|---|---|
| R01 | PASS | `_has_material_text` exige `str`, aplica NFKC, remove `Default_Ignorable_Code_Point` e decide positivamente pela existência de categoria Unicode `L*` ou `N*`. Filler invisível/pontuação/símbolo isolado é recusado e texto Unicode legítimo é preservado. |
| R02 | FAIL | A matriz congela NFKC + `casefold` + DICP + whitespace e tolerância somente a pontuação terminal editorial, preservando diferenças potencialmente semânticas. A implementação termina com `normalized.strip().strip(_EDITORIAL_EDGE_PUNCTUATION).strip()`: `str.strip(chars)` remove `. ! ? …` tanto no início quanto no fim. Reexecução independente: `"?resultado"` = `"resultado"` e `"…resultado"` = `"resultado"`. Ao ocupar duas semânticas, isso produz `AMBIGUOUS_BINARY_SEMANTICS`. |
| R03 | PASS | Implementação atual segue regra positiva: `type(value) is int` aceita inteiro Python sem cast; `type(value) is float` aplica `math.isfinite`; qualquer outro tipo retorna `False`. `np.float64(0.5)` e `np.float64(0.25)` foram recusados; inteiro enorme e float finito aceitos; `NaN` e `±Inf` recusados. Regressão permanente cobre `np.float64` em ambos os campos materiais. |
| R04 | PASS | Aprovação/reprovação humana final exige `por`, `em_utc` e `referencia`; status final deve coincidir com `validacao.status`; `PENDENTE` não pode carregar metadados de decisão final. Adversarial com aprovação incompleta retornou `VALIDATION_HUMAN_GATE`. |
| R05 | PASS | `_validate_provenance` aplica invariantes localmente: `APROVADO` exige aprovação auditável; `MEDIDO` exige medição e referência de execução; blocos incompatíveis são recusados independentemente da fase. |
| R06 | PASS | `EXECUTADO` exige resultado material e proveniência `MEDIDO`; demais estados exigem `resultado=null` e não podem declarar `MEDIDO`. Adversarial pré-execução retornou `EXPERIMENT_RESULT`. |
| R07 | PASS | Snapshot sem `--previous` não certifica histórico; com histórico, identidade, versão, `fase_anterior`, rewinds e reescrita da mesma fase/versão são verificados. Rewind a partir de `PUBLICADO` retorna `STATE_REWIND`. |
| R08 | PASS | A suíte guarda o perfil congelado: recusa `allOf`/`oneOf`, limita `anyOf`, recusa constraints irmãs de `$ref` e fixa allowlist exata de `pattern`. Mutações sintéticas próprias com `allOf` e `$ref + type` foram detectadas. |

## 5. Casos adversariais independentes

| Caso | Requisito | Resultado observado | Código/erro | Motivo correto? |
|---|---|---|---|---|
| DICP + whitespace + `!€` + combining isolado, sem letra/número | R01 | Não material | `SCHEMA` / `_has_material_text=False` | SIM |
| Dígito árabe, Devanagari com marca combinante e português acentuado | R01 | Material/aceito | sem erro R01 | SIM |
| DICP inserido no interior de definição já existente | R02 | Canonicalizado como equivalente | `AMBIGUOUS_BINARY_SEMANTICS` quando usado para duplicar definição | SIM |
| `ação` × `acao` | R02 | Permanecem distintos | sem erro R02 | SIM |
| `x < 10` × `x > 10` e `≥` × `≤` | R02 | Permanecem distintos | sem erro R02 | SIM |
| `a,b` × `ab` | R02 | Pontuação interna preservada | sem erro R02 | SIM |
| `"resultado?"` × `"resultado"` | R02 | Equivalentes por pontuação terminal | normalização idêntica | SIM |
| `"?resultado"` × `"resultado"` | R02 | Equivalentes indevidamente | normalização idêntica; quando ocupam duas classes, `AMBIGUOUS_BINARY_SEMANTICS` | NÃO |
| `"…resultado"` × `"resultado"` | R02 | Equivalentes indevidamente | normalização idêntica | NÃO |
| `np.float64(0.5)` em `classificacao.limiares[].valor` | R03 | Recusado | `SCHEMA`; finite-number `False` | SIM |
| `np.float64(0.25)` em `score.componentes[].peso` | R03 | Recusado | `SCHEMA`; finite-number `False` | SIM |
| `int` Python comum | R03 | Aceito como número canônico | sem erro R03 | SIM |
| `10**10000` | R03 | Aceito sem conversão a float/`OverflowError` | sem erro R03 | SIM |
| `float(0.5)` | R03 | Aceito | sem erro R03 | SIM |
| `float("nan")` | R03 | Recusado | `SCHEMA` | SIM |
| `float("inf")` | R03 | Recusado | `SCHEMA` | SIM |
| `float("-inf")` | R03 | Recusado | `SCHEMA` | SIM |
| `validacao.status=APROVADO`, decisão humana `APROVADO` sem `referencia` | R04 | Recusado | `VALIDATION_HUMAN_GATE` | SIM |
| Proveniência `APROVADO` com `aprovacao=null` | R05 | Recusado | `PROV_APPROVAL_REQUIRED` | SIM |
| Experimento `EM_EXECUCAO` contendo resultado observado | R06 | Recusado | `EXPERIMENT_RESULT` | SIM |
| Snapshot anterior `PUBLICADO`, mesma versão, snapshot atual retornando a `VALIDADO` | R07 | Recusado | `STATE_REWIND` | SIM |
| Schema sintético com `allOf` e `$ref` acompanhado de `type` | R08 | Guard de autoria detecta ambas as violações | `allOf fora do perfil`; constraint irmã de `$ref` | SIM |

## 6. Fechamento dos bloqueios da auditoria anterior

### R03 — domínio numérico

- Resultado: FECHADO / PASS
- Evidência: o código atual deixou de usar teste amplo de subtipo e aplica identidade estrita de tipo: `type(value) is int`, `type(value) is float`, `return False` para externos.
- np.float64 em limiar: `np.float64(0.5)` recusado; caminho de schema resulta em `SCHEMA`.
- np.float64 em peso: `np.float64(0.25)` recusado; caminho de schema resulta em `SCHEMA`.
- Teste permanente: `tools/tests/test_micromodelo_mm01_r03.py` importa NumPy real, usa `np.float64`, verifica diretamente que o checker retorna `False` e injeta o valor tanto no limiar quanto no peso. Ele não é tautológico: uma implementação vulnerável baseada em `isinstance(value, float)` faz `np.float64` entrar como `float` em versões atuais do NumPy e faria o primeiro `assertFalse` falhar. O workflow instala NumPy antes de executar esse teste.
- Conclusão: o bloqueio R03 da rodada histórica está tecnicamente encerrado na candidata atual.

### Sincronização com main

- Resultado: FECHADO / PASS
- main: `1d46c9625fb5bfd6d1b666ddff055507238788bf`
- merge-base: `1d46c9625fb5bfd6d1b666ddff055507238788bf`
- behind_by: `0`
- merge-ref: `3de9090ef8c035b0c43541b6a87ea21fab44120d`; tree `1dfb5ff6ed6469472bd87e6063ef5723b7f2214a`, idêntica à tree do HEAD.
- Conclusão: houve integração real da `main`; ela é pai direto do HEAD reconciliado. O compare atual não evidencia perda de frente externa ou reimplementação acidental: `behind_by=0` e a superfície residual contra `main` é a superfície própria/documental da MM01.

## 7. Consistência transversal

- Schema × validador: estruturalmente coerentes para R01, R03–R08 e demais gates materiais. Há, porém, divergência semântica R02 no normalizador do validador: o schema permite texto material iniciado por pontuação, enquanto `_normalize_editorial_text` apaga `. ! ? …` também da borda inicial.
- Template × schema: coerente; template percorre o caminho positivo do contrato e mantém fases/gates posteriores pendentes.
- Testes × requisitos: cobertura extensa e efetiva, incluindo Unicode, DICP, finitude, NumPy, decisão humana, proveniência, experimentos, histórico e perfil de autoria. Entretanto, o bloco R02 exercita DICP, diacríticos, operadores e pontuação interna, mas não protege a restrição posicional “somente terminal”; por isso os 47 testes permanecem verdes apesar da sobrecanonicalização identificada.
- CLI snapshot × evolução: coerente; sem `--previous`, a CLI afirma `SNAPSHOT_VALIDO/HISTORICO_NAO_CERTIFICADO`; com histórico válido, `APROVADO_EVOLUCAO`.
- Workflow MM01: PASS no run `35036376210`; runner real, checkout sem credencial persistida, dependências instaladas, 47 testes + regressão R03 + validador estrutural.
- Workflow V12: PASS no run `35036376279`; aplicabilidade avaliada corretamente e `Escopo V12 e higiene` ficou `skipped`, eliminando o bloqueio transversal indevido.
- HEAD × merge-ref: equivalência material completa; ambos apontam para tree `1dfb5ff6ed6469472bd87e6063ef5723b7f2214a`.
- Fronteiras MM02/MM03/MM04/MM06: preservadas. Não há fingerprint/MM02, crawler ou binding corporativo/MM03, skill `hub-ml-micromodelos` ou sétimo tipo/MM04, contrato definitivo de MLflow/MM06, publicação/ACL/dado corporativo real, migração de legado ou integração visual própria. Os ADRs mantêm YAML como especificação, histórico de runs fora dele, governança externa como autoridade e bindings reais para etapas posteriores.
- O bloco MM01 do `CHANGELOG.md` continua deliberadamente pré-fechamento — por exemplo, ainda descreve contagens e estado antigos da candidata. Essa é a dívida documental prevista no procedimento e não foi classificada como bloqueio nem alterada nesta sessão.

## 8. Achados

### QUEBRA

Nenhum achado.

### DIVERGE

**D-01 — BLOQUEANTE — R02: canonicalização aceita pontuação inicial como se fosse pontuação terminal.**

A matriz congelada estabelece explicitamente que a canonicalização pode tolerar somente pontuação terminal editorial e deve permanecer conservadora.

A implementação atual define `. ! ? …` e executa:

`normalized.strip().strip(_EDITORIAL_EDGE_PUNCTUATION).strip()`

`str.strip(chars)` atua nas duas extremidades, não apenas no fim.

Reprodução independente:

- `"?resultado positivo"` → `resultado positivo`;
- `"resultado positivo"` → `resultado positivo`;
- `"…resultado positivo"` → `resultado positivo`;
- `"resultado positivo?"` → `resultado positivo`.

O último caso é compatível com a tolerância terminal; os dois primeiros não são. Como `_has_material_text` aceita normalmente essas strings por conterem letras, não há rejeição estrutural anterior. Quando duas definições diferem apenas por essa pontuação inicial, o normalizador as colapsa e o validador pode emitir `AMBIGUOUS_BINARY_SEMANTICS` contra duas entradas que o perfil conservador congelado não autorizou tratar como equivalentes.

Isso não cria requisito novo: a violação está ligada diretamente ao R02 e ao termo restritivo “somente” da matriz. O impacto concreto é uma rejeição falsa dentro do domínio suportado por sobrecanonicalização. Portanto, trata-se de `DIVERGE`, severidade `BLOQUEANTE`.

### MELHORÁVEL

Nenhum achado.

## 9. Veredito

**VEREDITO: NAO_APTA**

Bloqueios para fechamento:

- `D-01 — R02`: `_normalize_editorial_text` remove `. ! ? …` tanto na borda inicial quanto na terminal, excedendo a tolerância editorial congelada pela matriz. Enquanto isso persistir, R02 não pode ser marcado como PASS e a condição de fechamento exige que todos R01–R08 estejam provados.

Melhorias não bloqueantes:

- Nenhuma melhoria material adicional identificada. O bloco MM01 do `CHANGELOG.md` continua sendo dívida documental deliberada de pós-fechamento e não foi transformado em finding.

Condições para próximo passo:

- Não fazer merge da PR #51.
- Não sincronizar o bloco MM01 do `CHANGELOG.md` como fechamento enquanto a candidata continuar não apta.
- Não iniciar MM02.
- Para uma nova candidata de fechamento, o comportamento R02 precisa ser alinhado à matriz e protegido por regressão permanente que diferencie pontuação inicial da pontuação terminal; depois, devem ser novamente comprovados os gates MM01, V12, `behind_by=0` e equivalência HEAD × merge-ref.
- R03 e sincronização com `main` não precisam ser reabertos conceitualmente, mas devem continuar passando na árvore que vier a ser reavaliada.

## 10. Declaração de independência

- O veredito provisório `NAO_APTA` foi formulado nesta sessão antes da consulta deliberada a `docs/auditoria/2026-09-14_micromodelos-mm01/11_resultado_a1_reauditoria_8.md`.
- A conclusão foi construída a partir do estado Git/PR corrente, da `MATRIZ_ACEITE_FINAL.md`, da implementação atual, dos testes permanentes inspecionados, dos runs reais do SHA auditado e de adversariais próprios.
- O relatório histórico `11_resultado_a1_reauditoria_8.md` foi aberto somente após esse veredito provisório e utilizado apenas para conferir o fechamento dos dois bloqueios históricos autorizados: R03/tipos numéricos externos e sincronização com `main`. Ambos estão fechados no HEAD atual.
- A consulta histórica posterior também expôs sua antiga classificação do caso de pontuação inicial em R02; essa classificação não foi usada para formar nem substituir a conclusão desta auditoria. A presente classificação decorre da comparação direta entre a redação congelada de R02 e o comportamento atual de `str.strip`.
- No início da sessão, uma resposta bruta do endpoint da PR expôs incidentalmente texto histórico embutido no próprio corpo da PR. Esse conteúdo foi explicitamente descartado como evidência e não foi usado na formação do veredito.
- Nenhum arquivo foi editado, nenhuma correção foi implementada, nenhum commit/ref/PR foi alterado, nenhum merge foi feito e MM02 não foi iniciada.
