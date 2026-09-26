# RELATÓRIO DE AUDITORIA A1 — MM01

## 1. Identificação

- Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`
- Branch: `micromodelos/mm01-contrato-canonico`
- HEAD auditado: `2783bcbd6ad7f07f9f3893c66c9dc36d0557f57e`. O HEAD foi confirmado novamente ao final da sessão e permaneceu inalterado.
- Merge-base com main: `d106ef3158e5827a2eec3aa183dbb3b47885c960`; `main` é o merge-base da branch, com `behind_by=0` e a candidata 51 commits à frente.
- Python: CPython `3.12.14` no runner limpo usado para reproduzir os gates obrigatórios; CPython `3.13.5` no harness temporário usado para casos adversariais independentes.
- Limitações de ambiente: o checkout local direto não pôde ser feito por indisponibilidade de resolução de rede do container. Para não transformar essa limitação em aprovação, o job permanente da PR foi reexecutado nesta sessão: ele fez checkout limpo da PR, instalou as dependências, executou os 24 testes MM01 e `validate_assistant.py`, todos com sucesso. O merge-ref executado pelo GitHub Actions (`e62fdbc0...`) foi comparado ao HEAD auditado e contém zero diferenças de arquivo, portanto a árvore testada é idêntica à candidata. A validação da CLI do template foi executada pelo subprocesso literal existente na suíte reexecutada, com o mesmo `argv` exigido pelo prompt. Os casos adversariais adicionais foram construídos independentemente a partir das fontes primárias permitidas. `03_resultado_a1.md` não foi lido nem utilizado; documentos MM01 vedados pelo contexto também não foram usados como fundamento.

## 2. Execuções reproduzidas

| Execução | Resultado | Evidência objetiva |
|---|---|---|
| `python -m pip install -r tools/requirements-dev.txt` | PASS | Reexecução nesta sessão no runner limpo; CPython 3.12.14. Instalação concluída com sucesso, incluindo `PyYAML 6.0.3` e `jsonschema 4.26.0`. |
| `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v` | PASS | Reexecução nesta sessão: `Ran 24 tests in 0.763s` e `OK`. A suíte atual inclui testes de continuidade com `previous`, Unicode comum, gate temporal de limiar/peso, política de indeterminado e integridade básica de calibração. |
| `python -B tools/validate_assistant.py --root ambiente_fonte` | PASS | Reexecução nesta sessão: `APROVADO: 0 falha(s), 0 aviso(s)`; 14 skills, 76/76 READMEs operacionais, 221 arquivos Python AST, 1.422 arquivos de identidade e 1.887 links externos à raiz analisada. |
| CLI direta de `micromodelo.template.yaml` com `--schema` | PASS | O subprocesso literal da CLI é executado por `test_cli_returns_zero_for_template_and_one_for_invalid_document`; na reexecução desta sessão o teste ficou `ok`, exigindo `returncode=0` e texto `APROVADO`. |
| Validade formal Draft 2020-12 | PASS | O schema declara Draft 2020-12, fecha a raiz e blocos materiais com `additionalProperties: false`; `Draft202012Validator.check_schema` passou na suíte reexecutada. |
| Workflow permanente MM01 | PASS | `permissions: contents: read`, `persist-credentials: false`; executa apenas checkout, setup Python, dependências, testes, gate estrutural e mensagem de fronteira. Não contém ação Databricks, ACL, MLflow ou publicação corporativa. |
| Casos adversariais independentes | FAIL | A maior parte dos novos mutantes foi recusada corretamente, mas foram reproduzidos bypasses com caracteres Unicode invisíveis da categoria `Mn` e com formulações semânticas não cobertas pelas regex de `INDETERMINADO` e probabilidade. |

## 3. Casos adversariais independentes

| Caso | Resultado observado | Código/erro | Motivo correto? |
|---|---|---|---|
| Remover `publicacao.autoridade` | REJEITADO | `SCHEMA` | SIM |
| Adicionar propriedade desconhecida em bloco material | REJEITADO | `SCHEMA` | SIM |
| Salto `EM_DESCOBERTA → VALIDADO` | REJEITADO | `STATE_TRANSITION` | SIM |
| Especificação anterior confiável `PUBLICADO` v1.0.0 → corrente `EM_ESTUDO` v1.0.0 | REJEITADO | `STATE_REWIND` | SIM |
| Mesmo nome, versão corrente menor que anterior | REJEITADO | `VERSION_REWIND` | SIM |
| Nome do micromodelo corrente diferente do anterior | REJEITADO | `PREVIOUS_IDENTITY_MISMATCH` | SIM |
| Mesma fase e mesma versão, mas `fase_anterior` reescrita | REJEITADO | `PREVIOUS_HISTORY_REWRITE` | SIM |
| Versão material superior iniciando novo ciclo válido | ACEITO | nenhum | SIM |
| Usar `--previous` como tentativa de fingerprint: alterar conteúdo material mantendo nova versão | ACEITO pela comparação histórica; demais regras continuam validadas normalmente | nenhum código de fingerprint | SIM — MM02 não foi antecipada |
| Aprovação `por`/`referencia` com vazio, espaços, tab ou newline | REJEITADO | `SCHEMA` / `PROV_APPROVAL_REQUIRED` | SIM |
| Aprovação/medição com zero-width space U+200B ou word joiner U+2060 | REJEITADO | `PROV_APPROVAL_REQUIRED` / `PROV_MEASUREMENT_REQUIRED` | SIM |
| Aprovação/medição contendo somente COMBINING GRAPHEME JOINER U+034F, VARIATION SELECTOR-16 U+FE0F ou COMBINING ACUTE U+0301 | ACEITO | nenhum | NÃO |
| `handoff_ref`/`produto_dados_ref` com espaços, tabs/newlines, NBSP ou caracteres Unicode categoria `C*` | REJEITADO | `SCHEMA` / `PUBLICATION_GATE` | SIM |
| `handoff_ref`/`produto_dados_ref` contendo somente U+034F ou U+FE0F | ACEITO | nenhum | NÃO |
| Limiar e peso `PROPOSTO` em `EM_ESTUDO` | ACEITO | nenhum `THRESHOLD_APPROVAL`/`WEIGHT_APPROVAL` | SIM |
| Limiar e peso `PROPOSTO` em `EM_VALIDACAO` | REJEITADO | `THRESHOLD_APPROVAL` / `WEIGHT_APPROVAL` | SIM |
| Limiar e peso ainda não aprovados em `VALIDADO` | REJEITADO | `THRESHOLD_APPROVAL` / `WEIGHT_APPROVAL` | SIM |
| `quando_false` cosmeticamente igual a `quando_indeterminado` | REJEITADO | `AMBIGUOUS_BINARY_SEMANTICS` | SIM |
| `ausencia_evidencia.tratamento=INDETERMINADO`, mas descrição diz “na ausência de evidência classificar como FALSE” | ACEITO | nenhum | NÃO |
| Política de publicação com `indeterminado_vira_false=true` | REJEITADO | `SCHEMA` / `INDETERMINATE_FALSE_POLICY` | SIM |
| Política de publicação com `indeterminado_vira_false=false` e descrição “indeterminado deve ser gravado como FALSE” | REJEITADO | `INDETERMINATE_POLICY_CONTRADICTION` | SIM |
| Mesma política com descrição “INDETERMINADO será FALSE na saída final” | ACEITO | nenhum | NÃO |
| Mesma política com descrição “casos INDETERMINADOS retornam FALSE” | ACEITO | nenhum | NÃO |
| Proveniência `MEDIDO` sem `medicao` | REJEITADO | `PROV_MEASUREMENT_REQUIRED` | SIM |
| Proveniência `MEDIDO` com `referencia_execucao` vazia/whitespace | REJEITADO | `SCHEMA` / `PROV_MEASUREMENT_REQUIRED` | SIM |
| Proveniência `MEDIDO` com `referencia_execucao=U+034F` | ACEITO | nenhum | NÃO |
| Score `FORCA_EVIDENCIA` descrito explicitamente como “probabilidade” ou “chance” | REJEITADO | `SCORE_PROBABILITY_LANGUAGE` | SIM |
| Score `FORCA_EVIDENCIA` descrito como “percentual estimado de ocorrência da característica” | ACEITO | nenhum | NÃO |
| Score `FORCA_EVIDENCIA` descrito como “risco percentual de possuir a característica” | ACEITO | nenhum | NÃO |
| Score probabilístico sem bloco de calibração | REJEITADO | `CALIBRATION_REQUIRED` | SIM |
| Calibração com `evidencia_ref` inexistente | REJEITADO | `CALIBRATION_EVIDENCE_REF` | SIM |
| Calibração apontando para experimento existente, mas `PROPOSTO`/não executado | REJEITADO | `CALIBRATION_EVIDENCE_REF` | SIM |
| Calibração apontando para experimento `EXECUTADO`, mas sem proveniência `MEDIDO` | REJEITADO | `CALIBRATION_EVIDENCE_REF` e/ou `EXPERIMENT_MEASUREMENT` | SIM |
| Calibração apontando para experimento `EXECUTADO` e `MEDIDO` | ACEITO | nenhum erro de integridade referencial | SIM |
| Score desabilitado mantendo semântica/componentes/campo de saída | REJEITADO | `SCORE_DISABLED` | SIM |
| Evidência/contra-evidência referenciando fonte não declarada | REJEITADO | `UNKNOWN_SOURCE_REF` | SIM |
| Fonte com `catalogo_ref` diferente de `CATALOGO_PRODUTO` | REJEITADO | `CATALOG_SCOPE` | SIM |
| `PUBLICADO` sem `produto_dados_ref` | REJEITADO | `PUBLICATION_GATE` | SIM |
| YAML com `true:`/`false:` em vez de `quando_true:`/`quando_false:` | REJEITADO | `SCHEMA`; chaves são resolvidas pelo YAML como booleanos e não satisfazem o contrato | SIM |

## 4. Achados

### [QUEBRA-01] Caracteres Unicode invisíveis da categoria `Mn` ainda satisfazem provas auditáveis

- Severidade: BLOQUEANTE
- Arquivo/trecho: `tools/micromodelo_mm01_contract.py`, função `_has_material_text`; `micromodelo.schema.json`, campos de aprovação, `referencia_execucao`, `handoff_ref` e `produto_dados_ref`. `_has_material_text` remove caracteres cujas categorias Unicode começam por `Z` ou `C`, mas preserva marcas `M*`. O schema usa `pattern: ".*\\S.*"`, que também considera essas marcas como não-whitespace.
- Como reproduzir: substituir uma referência auditável válida por uma string contendo somente U+034F `COMBINING GRAPHEME JOINER`, U+FE0F `VARIATION SELECTOR-16` ou U+0301 `COMBINING ACUTE ACCENT`. No harness independente, `unicodedata.category` retorna `Mn`; após NFKC, `_has_material_text` retorna `True`, e `\\S` do JSON Schema também aceita esses caracteres. O mesmo bypass se aplica a `aprovacao.por`, `aprovacao.referencia`, `medicao.referencia_execucao`, `handoff_ref` e `produto_dados_ref`.
- Esperado: campos usados como prova de aprovação, execução ou publicação externa devem conter informação auditável perceptível/referenciável, e caracteres exclusivamente invisíveis não devem satisfazer o gate.
- Observado: espaços, tabs, newlines, NBSP e formatos `Cf` como U+200B são recusados, mas marcas combinantes/invisíveis `Mn` passam por ambas as camadas.
- Impacto: uma especificação pode declarar `APROVADO`, `MEDIDO`, handoff externo ou `PUBLICADO` sem registrar uma identidade/referência humana ou de execução realmente utilizável. Isso compromete diretamente guardrails obrigatórios de proveniência e publicação.
- Recomendação: definir “texto material” por presença de caracteres semanticamente visíveis/alfa-numéricos ou por política Unicode positiva mais restritiva, em vez de excluir apenas `Z*`/`C*`; adicionar regressões para categorias `Mn`/variation selectors/combining marks nos campos auditáveis.

### [DIVERGE-01] A proteção `FALSE` × `INDETERMINADO` ainda depende de semântica textual incompleta

- Severidade: BLOQUEANTE
- Arquivo/trecho: `classificacao.ausencia_evidencia` no schema/validador e `_description_maps_indeterminate_to_false` em `tools/micromodelo_mm01_contract.py`; `saida.publicacao.politica_indeterminado` no schema. A política de publicação possui `indeterminado_vira_false=false`, mas a coerência da descrição é inferida por uma regex baseada em verbos específicos (`grav*`, `convert*`, `mape*`, `trat*`, `registr*`, `defin*`, `vira*`, `equival*`). Já a descrição de `classificacao.ausencia_evidencia` não passa por verificação semântica equivalente.
- Como reproduzir: manter `classificacao.ausencia_evidencia.tratamento=INDETERMINADO` e escrever `descricao="na ausência de evidência classificar como FALSE"`; o documento não recebe erro específico. Na publicação, manter `indeterminado_vira_false=false` e usar `descricao="INDETERMINADO será FALSE na saída final"` ou `"casos INDETERMINADOS retornam FALSE"`; essas formulações não correspondem aos stems da regex e escapam de `INDETERMINATE_POLICY_CONTRADICTION`.
- Esperado: nenhuma especificação válida deve conter simultaneamente regra estruturada que preserva `INDETERMINADO` e prosa canônica que ordena ou define sua conversão para `FALSE`.
- Observado: uma formulação particular (“deve ser gravado como FALSE”) é detectada, mas várias formulações semanticamente equivalentes são aceitas; no bloco de ausência de evidência, a contradição nem sequer é confrontada com o tratamento estruturado.
- Impacto: dois consumidores competentes podem seguir partes distintas da mesma fonte canônica e produzir classificações materialmente diferentes. O problema atinge diretamente o guardrail de não converter ausência de evidência em `FALSE` e o contrato de publicação.
- Recomendação: remover a necessidade de inferir comportamento executável de prosa livre ou estruturar completamente a semântica relevante; se a descrição continuar normativa, sua consistência precisa ser validada por regra que não dependa de uma lista aberta de verbos.

### [DIVERGE-02] Linguagem probabilística pode escapar do gate por sinônimos não cobertos

- Severidade: BLOQUEANTE
- Arquivo/trecho: `_uses_probability_language` em `tools/micromodelo_mm01_contract.py`. A função procura apenas stems de `probabil*` e `chance(s)`, depois de remover disclaimers explícitos.
- Como reproduzir: manter `score.tipo_semantica=FORCA_EVIDENCIA`, sem calibração, e definir `score.semantica="percentual estimado de ocorrência da característica"` ou `"risco percentual de possuir a característica"`. O harness independente reproduziu `_uses_probability_language=False` para essas formulações, enquanto “probabilidade estimada” e “chance” são corretamente detectadas.
- Esperado: qualquer semântica que atribua interpretação probabilística ao score 0–100 deve exigir `PROBABILIDADE_CALIBRADA`, calibração `MEDIDO` e experimento executado/referenciável.
- Observado: o gate é lexical e aceita formulações probabilísticas inequívocas sem usar as duas palavras cobertas.
- Impacto: um score não calibrado pode ser documentado na fonte canônica como percentual/risco probabilístico e passar pelo validador, permitindo interpretação materialmente incorreta a jusante.
- Recomendação: representar a natureza probabilística exclusivamente por campo estruturado e proibir que a prosa redefina essa semântica, ou ampliar a validação de consistência para não depender de um vocabulário incompleto.

MELHORÁVEL — Nenhum achado.

## 5. Cobertura dos critérios

| Critério | Status | Evidência |
|---|---|---|
| 1. Micromodelo continua artefato de domínio; sem sétimo tipo/skill antecipada | PASS | ADR-0014 mantém a taxonomia fechada; `project_policy.py` continua listando 14 skills e não contém `hub-ml-micromodelos`; o diff não altera `.assistant`. |
| 2. Especificação canônica estruturada compatível com `micromodelo.yaml` | PASS | Schema formal e template YAML existem; ADR-0015 define o YAML como fonte canônica progressiva. |
| 3. Schema Draft 2020-12 válido e fechado em blocos materiais | PASS | `Draft202012Validator.check_schema` passou; raiz/blocos materiais usam `additionalProperties: false`. |
| 4. `fase` e `condicao` não são confundidas | PASS | Campos e validações são independentes; condição possui regras próprias e fase usa máquina de transição separada. |
| 5. Máquina rejeita saltos e limita rework | PASS | Mutante independente de salto foi rejeitado; transições permitidas permanecem enumeradas explicitamente. |
| 6. `PUBLICADO` não pode ser silenciosamente rebobinado na mesma versão | PASS | Com `previous_spec` confiável, mesma versão previamente `PUBLICADO` recebe `STATE_REWIND`; alteração de `fase_anterior` sem mudança de fase recebe `PREVIOUS_HISTORY_REWRITE`. Nova versão material reinicia ciclo sem executar fingerprint. |
| 7. Estados de proveniência têm significado operacional distinto | PASS | Enum fechado e regras separadas de aprovação/medição continuam vigentes. |
| 8. `APROVADO` exige decisão humana auditável | FAIL | QUEBRA-01: campos formados somente por marcas Unicode invisíveis `Mn` satisfazem schema e `_has_material_text`. |
| 9. `MEDIDO` exige referência de execução real/auditável | FAIL | QUEBRA-01: `referencia_execucao` contendo somente U+034F/U+FE0F é tratada como material. |
| 10. `FALSE` permanece distinto de ausência/`INDETERMINADO` | FAIL | O contrato estruturado distingue os estados, mas DIVERGE-01 permite prosa canônica contraditória que redefine `INDETERMINADO` como `FALSE`. |
| 11. Ausência de evidência não vira `FALSE` sem regra aprovada | FAIL | `tratamento=INDETERMINADO` pode coexistir com descrição que manda classificar ausência como `FALSE`; não há confronto semântico nesse bloco. |
| 12. Score habilitado tem semântica explícita e escala 0–100 | PASS | Escala 0–100 e campos de semântica/normalização são exigidos pelo validador. |
| 13. Score 0–100 não é automaticamente probabilidade | PASS | O tipo estruturado distingue `FORCA_EVIDENCIA` de `PROBABILIDADE_CALIBRADA`; não há promoção automática pela escala. |
| 14. Semântica probabilística exige calibração medida e execução referenciada | FAIL | Integridade de `evidencia_ref` foi corrigida, mas DIVERGE-02 permite declarar semântica probabilística por sinônimos como “percentual estimado” sem ativar o gate de calibração. |
| 15. Pesos e limiares não avançam sem aprovação humana | PASS | `PROPOSTO` é permitido antes de `EM_VALIDACAO`; a partir de `EM_VALIDACAO` os mutantes recebem `THRESHOLD_APPROVAL`/`WEIGHT_APPROVAL`. |
| 16. Fontes limitadas ao binding `CATALOGO_PRODUTO`; fixtures sanitizados | PASS | `ALLOWED_CATALOG_REFS` contém apenas `CATALOGO_PRODUTO`; fixture observado usa nomes sintéticos; ADR-0020 mantém binding real para MM03. |
| 17. Evidências não referenciam fontes inexistentes | PASS | Mutante independente foi rejeitado por `UNKNOWN_SOURCE_REF`. |
| 18. Estudo preserva `TRUE`, `FALSE`, `INDETERMINADO` | PASS | `valores_classificacao` é constante nos três estados. |
| 19. Publicação BOOLEAN + política explícita/aprovada para `INDETERMINADO` | FAIL | Estrutura BOOLEAN e flag `indeterminado_vira_false=false` existem, porém DIVERGE-01 demonstra descrições contraditórias aceitas por formulações fora da regex. |
| 20. Autoridade final de publicação permanece externa | FAIL | `autoridade=GOVERNANCA_EXTERNA` permanece fixa e ADR-0017 está preservado, mas QUEBRA-01 permite satisfazer `handoff_ref`/`produto_dados_ref` com conteúdo invisível `Mn`, enfraquecendo a prova auditável de confirmação externa. |
| 21. YAML não vira histórico crescente de runs | PASS | `armazenar_historico_runs_no_yaml=false`; ADR-0016 mantém histórico operacional no MLflow/MM06. |
| 22. Não antecipa fingerprint/MM02, crawler/MM03, MLflow/MM06, visual, migração ou publicação real | PASS | `--previous` compara somente nome, SemVer e continuidade de fase; versão material superior retorna sem calcular hash/fingerprint. O diff não cria crawler/skill/MLflow definitivo; ADRs 0016/0018/0019/0020 mantêm as fronteiras futuras. |
| 23. Testes/fixtures independem de dado real, ACL, workspace ou segredo | PASS | Fixture positivo usa exclusivamente nomes sintéticos e `CATALOGO_PRODUTO`; política do projeto mantém detectores de identidade corporativa; gate estrutural reexecutado ficou verde. |
| 24. Workflow permanente é read-only e não executa ações corporativas | PASS | `contents: read`, credenciais de checkout não persistidas e apenas comandos locais de instalação/teste/validação. |

## 6. Veredito

**VEREDITO: NAO_APTA**

Bloqueios para aceite:

- Fechar o bypass de referências auditáveis compostas exclusivamente por marcas Unicode invisíveis da categoria `M*`, abrangendo aprovação, medição, handoff e referência de Produto de Dados.
- Tornar a proteção `FALSE` × `INDETERMINADO` semanticamente fechada: a prosa canônica não pode contradizer `tratamento`/`indeterminado_vira_false`, independentemente do verbo usado.
- Tornar a semântica probabilística estruturada e não burlável por sinônimos como “percentual estimado”, “risco percentual”, `likelihood` ou equivalentes sem calibração.
- Acrescentar casos de regressão independentes para esses bypasses e repetir todos os gates da candidata.

Melhorias não bloqueantes:

- Nenhum achado.

Condições para reauditoria:

- Auditar um novo HEAD explicitamente identificado e confirmar novamente merge-base/`behind_by` com `main`.
- Reproduzir instalação, 24+ testes MM01, `validate_assistant.py` e CLI direta do template em checkout limpo.
- Reexecutar adversariais com categorias Unicode `Mn`/variation selectors/combining marks em todos os campos auditáveis.
- Reexecutar formulações semanticamente equivalentes de conversão `INDETERMINADO → FALSE` que não dependam dos stems atualmente codificados.
- Reexecutar formulações probabilísticas sem as palavras literais “probabilidade” ou “chance”.
- Confirmar que qualquer correção continue sem introduzir fingerprint/MM02, binding/crawler/MM03, MLflow definitivo/MM06, publicação real, sistema visual próprio ou migração antecipada.
