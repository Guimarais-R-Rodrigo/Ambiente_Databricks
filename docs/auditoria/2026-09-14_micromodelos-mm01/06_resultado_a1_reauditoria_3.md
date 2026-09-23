# RELATÓRIO DE AUDITORIA A1 — MM01

## 1. Identificação

- Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`
- Branch: `micromodelos/mm01-contrato-canonico`
- HEAD auditado: `c0b6f5872f47f8e37ed8f55f262c276b8c105063`. O HEAD real coincidiu com a expectativa inicial e foi reconfirmado ao final da auditoria.
- Merge-base com main: `d106ef3158e5827a2eec3aa183dbb3b47885c960`. O HEAD final de `main` permaneceu nesse mesmo SHA. Comparação final: `ahead_by=75`, `behind_by=0`, 75 commits e 21 arquivos alterados.
- Python: CPython `3.12.14` no runner limpo da reexecução independente; CPython `3.13.5` no harness adversarial local.
- Limitações de ambiente: o container local não conseguiu resolver `github.com` para clone direto. A limitação não foi convertida em aprovação: os gates obrigatórios foram reexecutados em GitHub Actions com checkout limpo. O runner fez checkout do merge-ref `3041d4a180d34c717bd2e440d4e91a220d87fa93`; comparação desse merge-ref contra o HEAD auditado retornou um único commit de merge e `files=[]`, provando equivalência de árvore. Os adversariais próprios de Unicode/materialidade foram executados localmente reproduzindo exatamente o predicado `_has_material_text`, o `FormatChecker` e as restrições de schema relevantes da árvore atual; os casos de bypass foram ainda confrontados diretamente com os caminhos do schema e do validador. A PR #51 permaneceu aberta, `merged=false`, `draft=false`, `mergeable=true`; o estado REST observado foi `mergeable_state=clean`.

## 2. Execuções reproduzidas

| Execução | Resultado | Evidência objetiva |
|---|---|---|
| Estado Git: branch/main/merge-base/ahead/behind | PASS | HEAD=`c0b6f587…`; main=merge-base=`d106ef31…`; `ahead_by=75`; `behind_by=0` |
| Estado PR #51 | PASS | aberta; não integrada; não draft; `mergeable=true`; `mergeable_state=clean`; 75 commits; 21 arquivos |
| Workflows associados ao HEAD exato | PASS | 7 workflows associados a `c0b6f587…`; todos `completed/success`: CI local, MM01, V00, V01, V02, V10 e V11 |
| `python -m pip install -r tools/requirements-dev.txt` | PASS | reexecução em runner limpo; instalação concluída com sucesso em CPython 3.12.14 |
| `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v` | PASS | reexecução independente: `Ran 29 tests in 1.022s` / `OK` |
| `python -B tools/validate_assistant.py --root ambiente_fonte` | PASS | `APROVADO: 0 falha(s), 0 aviso(s)` |
| CLI direta do template | PASS | a suíte executada em checkout limpo chama literalmente o subprocesso `CONTRACT TEMPLATE --schema SCHEMA` e exige exit code 0 + `APROVADO`; esse teste passou na reexecução. |
| Fixture positiva | PASS | `test_validated_fixture_is_valid` validou `valido_validado.json` sem issues na reexecução. |
| Fixture negativa | PASS | os 9 casos de `casos_invalidos.json` foram mutados sobre a fixture positiva e todos produziram o código esperado na reexecução. |
| Cenário CLI com `--previous` | PASS | subprocesso real da CLI com snapshot anterior `PUBLICADO` e rewind atual retorna exit code 1 contendo `STATE_REWIND`; teste passou. |
| Draft 2020-12 | PASS | `Draft202012Validator.check_schema` passou na suíte limpa. |
| Autoridade Unicode do schema/validador | PASS parcial | `$defs.material_ref` usa `format: material-text`; o `FormatChecker` delega diretamente à mesma `_has_material_text` usada semanticamente. Não existe mais segunda regex ASCII para materialidade. |
| Ausência de arquivos transitórios | PASS | diff final contém apenas os 21 caminhos versionados esperados; varredura da árvore não encontrou nomes/extensões transitórios usuais (`.tmp`, `.bak`, `.orig`, `transitorio`, `materializador`); `validate_assistant` registrou zero extras de worktree |
| Workflow MM01 permanente | PASS | `contents: read`, `persist-credentials: false`; executa instalação, unittest e gate estrutural, sem ação corporativa. |

## 3. Casos adversariais independentes

| Caso | Resultado observado | Código/erro | Motivo correto? |
|---|---|---|---|
| U+034F COMBINING GRAPHEME JOINER isolado em `material-text` | Rejeitado | `SCHEMA`: not a `material-text` | SIM |
| U+FE0F VARIATION SELECTOR-16 isolado | Rejeitado | `SCHEMA` | SIM |
| U+0301 combining acute isolado | Rejeitado | `SCHEMA` | SIM |
| Marca `Mc` isolada | Rejeitado | `SCHEMA` | SIM |
| Marca `Me` isolada | Rejeitado | `SCHEMA` | SIM |
| U+200B ZWSP | Rejeitado | `SCHEMA` | SIM |
| U+200C ZWNJ | Rejeitado | `SCHEMA` | SIM |
| U+200D ZWJ | Rejeitado | `SCHEMA` | SIM |
| U+2060 WORD JOINER | Rejeitado | `SCHEMA` | SIM |
| U+2063 INVISIBLE SEPARATOR | Rejeitado | `SCHEMA` | SIM |
| NBSP U+00A0 | Rejeitado | `SCHEMA` | SIM |
| EM SPACE U+2003 | Rejeitado | `SCHEMA` | SIM |
| FIGURE SPACE U+2007 | Rejeitado | `SCHEMA` | SIM |
| NARROW NO-BREAK SPACE U+202F | Rejeitado | `SCHEMA` | SIM |
| Somente pontuação (`!!!`) | Rejeitado | `SCHEMA` | SIM |
| Somente símbolos (`∑€🧿`) | Rejeitado | `SCHEMA` | SIM |
| Combinação CGJ + ZWSP + NBSP + pontuação + símbolo | Rejeitado | `SCHEMA` | SIM |
| Texto acentuado Unicode `é` | Aceito | nenhum | SIM |
| CJK `資料` | Aceito | nenhum | SIM |
| Algarismos Arabic-Indic `٤٢` | Aceito | nenhum | SIM |
| Devanagari `देवनागरी` | Aceito | nenhum | SIM |
| Base + combining mark `Café` | Aceito | nenhum | SIM |
| Grego `Δοκιμή` | Aceito | nenhum | SIM |
| Cirílico `данные` | Aceito | nenhum | SIM |
| Base material + variation selector (`A` + VS16) | Aceito | nenhum | SIM |
| `material_ref` em aprovação humana com CJK/acentuado/dígito Unicode/Devanagari | Aceito | nenhum | SIM |
| `material_ref` invisível em aprovação humana | Rejeitado | `SCHEMA` | SIM |
| `referencia_execucao` de `MEDIDO` invisível | Rejeitado | `SCHEMA` / `PROV_MEASUREMENT_REQUIRED` | SIM |
| `semantica_ref`, referência de normalização, `regra_ref`, `handoff_ref` e `produto_dados_ref` não materiais | Rejeitados pela definição compartilhada `material_ref` | `SCHEMA` | SIM |
| Proveniência raiz `gerado_por`, `pedido_original_ref` e `registros[].alvo` não materiais | Rejeitados | `SCHEMA` | SIM |
| Proveniência raiz equivalente com CJK/Devanagari/dígitos Unicode | Aceita | nenhum | SIM |
| `fontes[].schema`, `fontes[].objeto`, `fontes[].campos[]` invisíveis | Rejeitados | `SCHEMA` | SIM |
| Os mesmos localizadores em CJK | Aceitos | nenhum | SIM |
| `classificacao.semantica.quando_*` invisível/pontuação/símbolo | Rejeitado | `SCHEMA` | SIM |
| `validacao.criterios[]` não material | Rejeitado | `SCHEMA` | SIM |
| nomes de saída de estudo/publicação não materiais | Rejeitados | `SCHEMA` | SIM |
| `evidencias[0].regra = ZWSP × 5` | Aceito pela combinação atual schema + validador | nenhum | NÃO |
| `evidencias[0].regra = CGJ × 5` | Aceito | nenhum | NÃO |
| `evidencias[0].regra = NBSP × 5` | Aceito | nenhum | NÃO |
| `evidencias[0].regra = "!!!!!"` | Aceito | nenhum | NÃO |
| `evidencias[0].regra = "€€€€€"` | Aceito | nenhum | NÃO |
| `contra_evidencias[0].regra` com as mesmas classes não materiais | Aceito | nenhum | NÃO |
| `experimentos[0].hipotese = ZWSP × 5` | Aceito | nenhum | NÃO |
| `experimentos[0].hipotese = marks/pontuação/símbolos` | Aceito | nenhum | NÃO |
| Experimento `EXECUTADO` com `resultado=ZWSP` e proveniência `MEDIDO` válida | Aceito: `resultado.strip()` é truthy para ZWSP | nenhum | NÃO |
| Experimento `EXECUTADO` com resultado somente combining marks | Aceito | nenhum | NÃO |
| Experimento `EXECUTADO` com resultado somente pontuação/símbolos | Aceito | nenhum | NÃO |
| Experimento `EXECUTADO` com resultado somente NBSP | Rejeitado | `EXPERIMENT_RESULT` | SIM, mas por `.strip()`, não pela autoridade comum |
| `validacao.resultado.resumo = ZWSP × 3` em validação aprovada/medida | Aceito | nenhum | NÃO |
| `validacao.resultado.resumo = NBSP × 3` | Aceito pelo `minLength` | nenhum | NÃO |
| `validacao.resultado.resumo` somente marks/pontuação/símbolos | Aceito | nenhum | NÃO |
| `condicao=SUSPENSO` + `motivo_condicao=ZWSP` | Aceito: `motivo.strip()` é truthy | nenhum | NÃO |
| `condicao=SUSPENSO` + motivo apenas combining mark/pontuação/símbolo | Aceito | nenhum | NÃO |
| `condicao=SUSPENSO` + motivo somente NBSP | Rejeitado | `STATE_CONDITION` | SIM, incidentalmente por `.strip()` |
| Chave obrigatória profunda removida | Rejeitado | `SCHEMA` | SIM |
| Propriedade desconhecida em bloco material | Rejeitado | `SCHEMA` | SIM |
| Chave YAML/JSON duplicada | Rejeitada no carregamento | erro de chave duplicada | SIM |
| Referência a fonte inexistente | Rejeitado | `UNKNOWN_SOURCE_REF` | SIM |
| Fonte fora de `CATALOGO_PRODUTO` | Rejeitado | `CATALOG_SCOPE` | SIM |
| Salto de fase não permitido | Rejeitado | `STATE_TRANSITION` | SIM |
| Decisão humana contraditória | Rejeitado | `VALIDATION_HUMAN_GATE` | SIM |
| Limiar `PROPOSTO` em `EM_VALIDACAO` | Rejeitado | `THRESHOLD_APPROVAL` | SIM |
| Peso `PROPOSTO` em `EM_VALIDACAO` | Rejeitado | `WEIGHT_APPROVAL` | SIM |
| Limiar/peso `PROPOSTO` antes do gate formal | Aceito | nenhum | SIM |
| Ausência de evidência + `tratamento=INDETERMINADO` + resultado `FALSE` | Rejeitado | `MISSING_POLICY_CONTRADICTION` | SIM |
| Reintrodução de prosa livre tentando dizer “sem evidência → FALSE” | Rejeitado | `SCHEMA` | SIM |
| `REGRA_EXPLICITA_APROVADA` sem aprovação | Rejeitado | `MISSING_POLICY_APPROVAL` | SIM |
| Regra explícita aprovada sem `regra_ref` material | Rejeitado | `MISSING_POLICY_RULE_REF` / `SCHEMA` | SIM |
| Regra explícita aprovada e referenciada | Aceita | nenhum | SIM |
| `score.semantica` textual reintroduzido com “probabilidade/chance/odds/likelihood” | Rejeitado | `SCHEMA` | SIM |
| Mesmas palavras em `score.semantica_ref` com `tipo_semantica=FORCA_EVIDENCIA` | Aceito sem mudar a natureza estruturada | nenhum | SIM |
| `PROBABILIDADE_CALIBRADA` sem calibração | Rejeitado | `CALIBRATION_REQUIRED` | SIM |
| Calibração sem proveniência `MEDIDO` | Rejeitado | `CALIBRATION_EVIDENCE` | SIM |
| Calibração com experimento inexistente | Rejeitado | `CALIBRATION_EVIDENCE_REF` | SIM |
| Experimento de calibração existente, mas não executado/medido | Rejeitado | `CALIBRATION_EVIDENCE_REF` | SIM |
| Caminho probabilístico completo medido | Aceito | nenhum | SIM |
| Score desabilitado com resíduos materiais | Rejeitado | `SCORE_DISABLED` | SIM |
| Normalização textual livre | Rejeitada | `SCHEMA` | SIM |
| Normalização `PENDENTE` em `EM_VALIDACAO` | Rejeitada | `SCORE_NORMALIZATION` | SIM |
| Método definido com proveniência `PROPOSTO` no gate | Rejeitado | `SCORE_NORMALIZATION_APPROVAL` | SIM |
| `CUSTOM_APROVADO` sem referência material | Rejeitado | `SCORE_NORMALIZATION_REF` / `SCHEMA` | SIM |
| Política de publicação com `indeterminado_vira_false=true` | Rejeitada | `SCHEMA` | SIM |
| `OUTRA_APROVADA` sem referência material | Rejeitada | `PUBLICATION_POLICY_RULE_REF` | SIM |
| `CAMPO_COBERTURA_SEPARADO` com `regra_ref` indevida | Rejeitada | `PUBLICATION_POLICY_RULE_REF` | SIM |
| `PUBLICADO` sem confirmação externa/produto referenciado | Rejeitado | `PUBLICATION_GATE` | SIM |
| Rewind de `PUBLICADO` na mesma versão via `--previous` | Rejeitado | `STATE_REWIND` | SIM |
| Regressão de SemVer | Rejeitada | `VERSION_REWIND` | SIM |
| Mudança de identidade entre snapshots | Rejeitada | `PREVIOUS_IDENTITY_MISMATCH` | SIM |
| Reescrita de `fase_anterior` na mesma fase/versão | Rejeitada | `PREVIOUS_HISTORY_REWRITE` | SIM |
| Transição histórica válida | Aceita | nenhum | SIM |
| Versão material nova válida | Aceita sem comparação de fingerprint | nenhum | SIM |

## 4. Achados

**QUEBRA: Nenhum achado.**

### [DIVERGE-01] A autoridade única `material-text` existe, mas não cobre todos os campos normativos/materialmente decisivos

- Severidade: **BLOQUEANTE**
- Arquivo/trecho: `docs/sprints/micromodelos/MM01/micromodelo.schema.json` e `tools/micromodelo_mm01_contract.py`.
- Como reproduzir: manter a fixture positiva válida e substituir isoladamente:
  - `evidencias[0].regra` ou `contra_evidencias[0].regra` por cinco ZWSP, cinco CGJ, cinco NBSP, somente pontuação ou somente símbolos;
  - `experimentos[0].hipotese` por material equivalente não textual;
  - em experimento `EXECUTADO`, `resultado` por ZWSP, combining marks, pontuação ou símbolos;
  - `validacao.resultado.resumo` por três ZWSP, três NBSP, marks, pontuação ou símbolos;
  - em estado `SUSPENSO`/`BLOQUEADO`/`DEPRECATED`, `motivo_condicao` por ZWSP/marks/pontuação/símbolos.
- Esperado: esses campos cumprem função normativa ou satisfazem explicitamente um gate de regra, execução, validação ou condição operacional; portanto conteúdo que a política comum classifica como não material deve ser rejeitado.
- Observado: as regras de evidência e contra-evidência usam apenas `minLength: 5`; o validador verifica referências e proveniência, mas não a materialidade de `regra`. O contrato de experimento deixa `hipotese` apenas com `minLength` e `resultado` sem `material-text`; no gate `EXECUTADO`, o resultado é verificado por `resultado.strip()`, que aceita ZWSP, marks, pontuação e símbolos. `validacao.resultado.resumo` também possui somente `minLength`. `motivo_condicao` não usa `material-text`, e o gate de condição também depende de `.strip()`.
- Impacto: uma especificação pode satisfazer formalmente partes materiais de `EM_VALIDACAO`/`VALIDADO` com uma regra de evidência sem conteúdo real, um resultado executado materialmente vazio ou um resumo de validação materialmente vazio. Isso contradiz o objetivo fail-closed e cria duas classes operacionais de “não vazio”: campos protegidos pela autoridade Unicode comum e campos protegidos apenas por comprimento/`.strip()`. A lacuna não invalida a arquitetura inteira, mas é material antes do aceite.
- Recomendação: aplicar a autoridade `material-text` aos campos normativos e de gate equivalentes, sem criar novo predicado. Em particular, cobrir `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado` quando presente/exigido, `validacao.resultado.resumo` e `identidade.estado.motivo_condicao` quando aplicável; incluir regressões positivas Unicode e negativas para `Mn/Mc/Me`, `Cf`, espaços Unicode, pontuação, símbolos e combinações.

**MELHORÁVEL: Nenhum achado.**

## 5. Cobertura dos critérios

| Critério | Status | Evidência |
|---|---|---|
| 1. Micromodelo permanece artefato de domínio | PASS | ADR-0014 mantém o micromodelo fora da taxonomia de tipos do Hub; a candidata não altera `.assistant` nem cria tipo novo. |
| 2. Especificação canônica estruturada em YAML | PASS | schema + template + CLI implementam a fonte estruturada requerida pelo ADR-0015. |
| 3. Schema Draft 2020-12 e propriedades materiais fail-closed | PASS | `check_schema` e teste de propriedade desconhecida passaram. |
| 4. `fase` e `condicao` separadas | PASS | estrutura e validador tratam dimensões separadamente |
| 5. Máquina de fases sem saltos silenciosos | PASS | tabela e adversariais rejeitam saltos; rework previsto permanece |
| 6. Anti-rewind de `PUBLICADO` | PASS | `--previous` produz `STATE_REWIND` |
| 7. Estados de proveniência operacionalmente distintos | PASS | `APROVADO` e `MEDIDO` acionam requisitos específicos |
| 8. `APROVADO` exige decisão humana auditável | PASS | `por` e referências são submetidos a materialidade e coerência |
| 9. `MEDIDO` exige execução referenciável | PASS | `referencia_execucao` material é obrigatória |
| 10. FALSE é distinto de INDETERMINADO/sem evidência | PASS | estrutura e adversariais confirmados |
| 11. Silêncio não vira FALSE sem regra explícita aprovada | PASS | política estruturada fail-closed |
| 12. Score habilitado tem semântica estruturada e escala 0–100 | PASS | gates reproduzidos |
| 13. Escala 0–100 não implica probabilidade | PASS | `tipo_semantica` é autoridade; conteúdo lexical da referência não muda o tipo |
| 14. Probabilidade exige calibração medida | PASS | calibração e experimento resolvido/medido obrigatórios |
| 15. Pesos/limiares no gate exigem aprovação humana | PASS | `WEIGHT_APPROVAL` / `THRESHOLD_APPROVAL` |
| 16. Fontes ficam em `CATALOGO_PRODUTO` | PASS | catálogo alternativo rejeitado; fixtures permanecem sintéticos. |
| 17. Referências órfãs de fonte | PASS | `UNKNOWN_SOURCE_REF` |
| 18. Estudo preserva TRUE/FALSE/INDETERMINADO | PASS | contrato estruturado preserva os três valores |
| 19. Publicação exige BOOLEAN + política aprovada para INDETERMINADO | PASS | caminhos positivos/negativos reproduzidos |
| 20. Autoridade de publicação permanece externa | PASS | schema mantém `GOVERNANCA_EXTERNA`, coerente com ADR-0017; nenhum publicador real foi introduzido. |
| 21. YAML não armazena histórico crescente de runs | PASS | flag permanece `false`, coerente com ADR-0016. |
| 22. Não antecipa MM02/MM03/MM04/MM06 | PASS | não há `spec_fingerprint`/hash; `--previous` compara estado/versão sem equivalência material; nenhuma API de catálogo/dados; nenhuma `hub-ml-micromodelos`; MLflow permanece apenas política futura/placeholder. O inventário atual continua com 14 skills e sem a skill MM04. |
| 23. Sem dependência de dado/workspace/ACL/segredo real | PASS | fixtures sintéticos e workflow local/read-only |
| 24. Workflow MM01 permanente read-only | PASS | `contents: read`, sem credenciais persistidas ou ações corporativas. |
| 25. Falsos positivos Unicode da política comum | PASS | marks `Mn/Mc/Me`, `Cf`, zero-width, espaços Unicode, pontuação, símbolos e combinações rejeitados |
| 26. Falsos negativos Unicode da política comum | PASS | acentuados, CJK, algarismos Unicode, Devanagari, grego, cirílico e base+combining aceitos; a suíte atual também cobre exemplos multilíngues. |
| 27. Schema e validador usam uma única definição de materialidade | PASS | `format: material-text` delega ao mesmo `_has_material_text`; não existe regex ASCII paralela. |
| 28. Todos os campos materiais equivalentes usam essa autoridade | FAIL | DIVERGE-01: regras de evidência, hipótese/resultado de experimento, resumo de validação e motivo operacional ainda escapam |
| 29. Proveniência raiz material | PASS | `gerado_por`, `pedido_original_ref`, `registros[].alvo` cobertos e testados; Unicode legítimo passa. |
| 30. Localizadores de fonte e nomes de saída materiais | PASS | schema aplica `material-text`; regressões positivas/negativas passam. |
| 31. Duplicidades YAML/JSON e IDs | PASS | rejeição explícita reproduzida |
| 32. Proteção histórica por `--previous` | PASS | identidade, SemVer, histórico e anti-rewind validados; versão superior reinicia ciclo sem fingerprint |
| 33. `--previous` não antecipa MM02 | PASS | mudança de versão retorna antes de qualquer comparação material; não há `hashlib`, SHA material ou algoritmo de fingerprint |
| 34. Fronteira MM03 | PASS | nenhum crawler/binding real ou leitura de catálogo/dados; ADR-0020 reserva o binding ao ambiente autorizado. |
| 35. Fronteira MM04 | PASS | nenhuma nova skill; `EXPECTED_SKILL_NAMES` continua sem `hub-ml-micromodelos`. |
| 36. Fronteira MM06 | PASS | nenhuma extensão definitiva de MLflow; ADR-0016 reserva essa decisão à MM06. |
| 37. Sistema visual/migração de legados | PASS | nenhum arquivo visual próprio ou migração foi introduzido; coerente com ADR-0018/0019. |
| 38. Arquivos transitórios | PASS | nenhum arquivo transitório detectado na árvore/diff; zero extras de worktree no gate |
| 39. Workflows do SHA exato | PASS | todos os 7 workflows associados a `c0b6f587…` concluídos em `success`; MM01 ainda foi reexecutado nesta auditoria |
| 40. Consistência cruzada schema/template/fixture/CLI/testes | FAIL | arquitetura e referências estão coerentes, mas a cobertura de materialidade não é uniforme nos campos descritos em DIVERGE-01 |

## 6. Veredito

**VEREDITO: APTA_COM_CORRECOES**

### Bloqueios para aceite

- Aplicar a autoridade já existente `material-text` aos campos normativos/materialmente decisivos que ainda podem satisfazer gates com conteúdo composto apenas por marks, `Cf`, zero-width, whitespace Unicode, pontuação ou símbolos, em especial:
  - `evidencias[].regra`;
  - `contra_evidencias[].regra`;
  - `experimentos[].hipotese`;
  - `experimentos[].resultado` quando materialmente requerido;
  - `validacao.resultado.resumo`;
  - `identidade.estado.motivo_condicao` quando a condição exige motivo.
- Adicionar adversariais permanentes para esses campos que testem simultaneamente rejeição de conteúdo não material e aceitação de conteúdo Unicode legítimo.

### Melhorias não bloqueantes

- Nenhuma.

### Condições para reauditoria

- Auditar o novo HEAD diretamente, sem assumir que este achado foi corrigido.
- Repetir estado Git/PR, `ahead_by`, `behind_by`, mergeabilidade e workflows do SHA exato.
- Reexecutar instalação, 29+ testes MM01, `validate_assistant`, CLI do template, fixtures positiva/negativa e `--previous`.
- Para cada campo corrigido, exercitar isoladamente `Mn`, `Mc`, `Me`, `Cf`, ZWSP/ZWNJ/ZWJ/WORD JOINER, NBSP/EM SPACE/FIGURE SPACE/NNBSP, pontuação, símbolos e combinações; todos devem ser recusados quando isolados.
- Confirmar caminhos positivos com acentuados, CJK, algarismos Unicode, Devanagari e base+combining.
- Confirmar que a correção reutiliza a autoridade `material-text` existente, sem introduzir um segundo predicado divergente.
- Confirmar novamente que a correção não introduz fingerprint/MM02, catálogo real/MM03, skill/MM04, política definitiva de MLflow/MM06, publicação corporativa, visual próprio ou migração de legados.
- Não iniciar MM02 nem integrar a PR #51 antes do fechamento desse bloqueio.
