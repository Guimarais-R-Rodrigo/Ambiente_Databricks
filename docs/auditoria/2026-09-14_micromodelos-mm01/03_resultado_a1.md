# RELATÓRIO DE AUDITORIA A1 — MM01

## 1. Identificação

- Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`
- Branch: `micromodelos/mm01-contrato-canonico`
- HEAD auditado: `ba9928f93a007228291d2e6533a3854d92d8de6e`
- Merge-base com `main`: `a9480391c78e2402986885db0ce08b10e0619a1a`; a comparação final registrou `behind_by=0`. O merge ref de PR usado pelo runner difere do HEAD por um único merge commit e por zero arquivos, portanto a árvore executada é equivalente à candidata auditada.
- Python: CPython `3.12.14` no runner limpo do GitHub Actions usado para repetir os gates da candidata; CPython `3.13.5` no harness adversarial temporário local. O harness local usou `jsonschema 4.26.0` e `PyYAML 6.0.3`.
- Limitações de ambiente: o ambiente local não conseguiu resolver `github.com` para realizar clone direto. Para não converter essa limitação em aprovação, o workflow permanente da PR foi reexecutado nesta sessão em runner limpo, com checkout completo, instalação de `tools/requirements-dev.txt`, suíte MM01 e `validate_assistant.py`; todos concluíram com `success`. As dependências foram instaladas com sucesso no runner. Os adversariais próprios foram exercitados em memória/cópia temporária contra as regras e fragmentos exatos das fontes permitidas. Nenhum arquivo da branch foi alterado.

## 2. Execuções reproduzidas

| Execução | Resultado | Evidência objetiva |
|---|---|---|
| `python -m pip install -r tools/requirements-dev.txt` | PASS | Reexecução da auditoria no job `104181005591`; CPython 3.12.14; instalação concluída com `PyYAML 6.0.3`, `jsonschema 4.26.0` e demais dependências. O arquivo declara PyYAML como dependência de manutenção, não runtime. |
| `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v` | PASS | Reexecução: 17 testes, `Ran 17 tests in 0.590s`, `OK`. A suíte cobria schema, template, transições, semântica binária, score, chaves duplicadas, fontes, publicação e CLI. |
| `python -B tools/validate_assistant.py --root ambiente_fonte` | PASS | Reexecução: `APROVADO: 0 falha(s), 0 aviso(s)`; 14 skills, 76/76 READMEs operacionais, 1.404 arquivos de identidade e 1.878 links. |
| CLI sobre `micromodelo.template.yaml` | PASS | O teste `test_cli_returns_zero_for_template_and_one_for_invalid_document`, reexecutado e marcado `ok`, invoca a CLI via subprocess e exige retorno `0` + `APROVADO` para o template. |
| Validade formal Draft 2020-12 | PASS | `test_schema_is_valid_draft_2020_12` passou; o schema declara `https://json-schema.org/draft/2020-12/schema`, raiz fechada e grupos materiais fechados por `additionalProperties: false`. |
| Workflow permanente MM01 | PASS | `.github/workflows/micromodelos-mm01-ci.yml` usa `permissions: contents: read`, `persist-credentials: false` e executa somente instalação/testes/gate local; não contém Databricks, ACL, MLflow ou publicação remota. |
| Harness adversarial independente temporário | PASS | Executados 18 mutantes/variações não equivalentes aos nove fixtures negativos existentes; foram encontrados bypasses que a suíte então vigente não cobria. Os fixtures existentes foram lidos apenas para evitar copiar seus mutantes. |

## 3. Casos adversariais independentes

| Caso | Resultado observado | Código/erro | Motivo correto? |
|---|---|---|---|
| Remover campo profundo obrigatório `publicacao.autoridade` | REJEITADO | `SCHEMA` | SIM |
| Inserir propriedade desconhecida em `publicacao` | REJEITADO | `SCHEMA` | SIM |
| Saltar `EM_DESCOBERTA → VALIDADO` | REJEITADO | `STATE_TRANSITION` | SIM |
| Reescrever, na mesma `micromodel_version`, documento anteriormente `PUBLICADO` como `fase_anterior=VALIDADO`, `fase_atual=EM_ESTUDO`, limpando publicação | ACEITO pelo contrato de estado corrente | nenhum | NÃO |
| `VALIDADO` com `aprovacao_humana.por="   "` e `referencia="   "` | ACEITO | nenhum | NÃO |
| `quando_false` semanticamente igual a `quando_indeterminado`, variando caixa, acento/espaçamento/pontuação | REJEITADO | `AMBIGUOUS_BINARY_SEMANTICS` | SIM |
| `ausencia_evidencia.tratamento=REGRA_EXPLICITA_APROVADA` com proveniência `PROPOSTO` | REJEITADO | `MISSING_POLICY_APPROVAL` | SIM |
| Limiar `PROPOSTO` em `EM_VALIDACAO` | REJEITADO | `THRESHOLD_APPROVAL` | SIM |
| Peso `PROPOSTO` em `EM_VALIDACAO` | REJEITADO | `WEIGHT_APPROVAL` | SIM |
| Limiar/peso `PROPOSTO` em `EM_ESTUDO`, antes do gate de aprovação | REJEITADO | `THRESHOLD_APPROVAL` / `WEIGHT_APPROVAL` | NÃO |
| Proveniência `MEDIDO` com timestamp válido, mas `referencia_execucao="   "` | ACEITO | nenhum | NÃO |
| Score `FORCA_EVIDENCIA` descrito como “chance percentual de possuir a característica” sem calibração | REJEITADO | `SCORE_PROBABILITY_LANGUAGE` | SIM |
| Calibração `MEDIDO` com `evidencia_ref` órfão e referência de execução sintaticamente presente | ACEITO | nenhum | NÃO |
| Score desabilitado com os demais campos limpos, mas `saida.estudo.campo_score` residual | REJEITADO | `SCORE_DISABLED` | SIM |
| Contra-evidência apontando simultaneamente para fonte existente e uma fonte órfã | REJEITADO | `UNKNOWN_SOURCE_REF` | SIM |
| `catalogo_ref="catalogo_produto"` em vez de `CATALOGO_PRODUTO` | REJEITADO | `CATALOG_SCOPE` | SIM |
| `PUBLICADO` com `produto_dados_ref=null` | REJEITADO | `PUBLICATION_GATE` | SIM |
| `PUBLICADO` com `produto_dados_ref="   "` | ACEITO | nenhum | NÃO |
| Política estruturada `CAMPO_COBERTURA_SEPARADO`, porém `descricao` manda gravar `INDETERMINADO` como `FALSE` | ACEITO | nenhum | NÃO |
| YAML usando chaves `true:`/`false:` no lugar de `quando_true:`/`quando_false:` | REJEITADO | `SCHEMA`; PyYAML resolve as chaves como booleanos `True`/`False`, que viram propriedades inesperadas e deixam as obrigatórias ausentes | SIM |

## 4. Achados

### [QUEBRA-01] `PUBLICADO` pode ser silenciosamente rebobinado na mesma versão material

- Severidade: **BLOQUEANTE**
- Arquivo/trecho: `tools/micromodelo_mm01_contract.py`, `TRANSICOES_FASE`, validação de `fase_anterior/fase_atual` e CLI; `micromodelo.schema.json`, `identidade.micromodel_version`.
- Como reproduzir: partir conceitualmente de um micromodelo já `PUBLICADO`, manter a mesma `micromodel_version`, substituir o estado corrente por `fase_anterior=VALIDADO` / `fase_atual=EM_ESTUDO`, definir `publicacao.status=NAO_INICIADA`, limpar `handoff_ref`/`produto_dados_ref` e retornar `saida.publicacao` a `PENDENTE`.
- Esperado: depois de `PUBLICADO`, a mesma versão material não pode apagar/rebobinar silenciosamente a fase de publicação; rework deve deixar rastro auditável e/ou exigir versão material distinta.
- Observado: a candidata impede um par explícito `PUBLICADO → EM_ESTUDO`, mas não impede a alteração do próprio campo `fase_anterior`. A proteção é autorreferente.
- Impacto: viola o critério 6. Um arquivo canônico versionado pode apresentar um histórico de estado falso sem que o validador detecte; isso compromete a auditabilidade da máquina de fases após publicação externa.
- Recomendação: tornar a regra de não-rewind verificável contra estado anterior confiável — por exemplo, validar transição contra a especificação precedente/registro imutável ou exigir mecanismo equivalente — e adicionar regressão que parta de `PUBLICADO` e tente reescrever a mesma versão para fase anterior.

### [QUEBRA-02] Aprovação, medição e confirmação externa aceitam referências semanticamente vazias

- Severidade: **BLOQUEANTE**
- Arquivo/trecho: `micromodelo.schema.json` em `$defs.proveniencia.aprovacao`, `$defs.proveniencia.medicao`, `validacao.aprovacao_humana`, `publicacao.handoff_ref` e `publicacao.produto_dados_ref`; `tools/micromodelo_mm01_contract.py` em `_validate_provenance`, gate humano e gates de publicação.
- Como reproduzir: em documento `VALIDADO`, usar `aprovacao_humana.por="   "` e `referencia="   "` com timestamp válido; em proveniência `MEDIDO`, usar `referencia_execucao="   "`; em `PUBLICADO`, usar `produto_dados_ref="   "`.
- Esperado: `APROVADO` deve possuir identidade/referência humana auditável; `MEDIDO` deve possuir referência de execução efetiva; `PUBLICADO` deve possuir referência externa material.
- Observado: os três guardrails podem ser satisfeitos com whitespace.
- Impacto: viola os critérios 8 e 9 e torna insuficientes as provas dos critérios 14 e 20.
- Recomendação: validar conteúdo não branco após normalização/`strip()` em todos os identificadores e referências materiais, no schema e/ou no validador semântico; incluir mutantes com vazio, espaços, tabs/newlines e Unicode equivalente a vazio visual.

### [DIVERGE-01] `PROPOSTO` existe no contrato, mas limiares e pesos não podem ser progressivamente propostos

- Severidade: **BLOQUEANTE**
- Arquivo/trecho: `tools/micromodelo_mm01_contract.py`, loops de `classificacao.limiares` e `score.componentes`.
- Como reproduzir: criar em `EM_ESTUDO` um limiar ou componente de score em elaboração, com proveniência `PROPOSTO` e sem bloco de aprovação. Mesmo antes de `EM_VALIDACAO`, o documento recebe `THRESHOLD_APPROVAL`/`WEIGHT_APPROVAL`.
- Esperado: a especificação canônica deve conseguir representar uma proposta enquanto proposta; a falta de aprovação deve impedir avançar para a fase que exige decisão, não impedir registrar o valor tentativo nas fases de descoberta/estudo.
- Observado: qualquer limiar/peso persistido precisa fingir-se já `APROVADO` ou ser totalmente omitido do YAML.
- Impacto: contradiz o objetivo de uma fonte canônica progressiva e enfraquece rastreabilidade de decisão.
- Recomendação: separar “pode existir no YAML” de “pode avançar de fase”; permitir `PROPOSTO` nas fases pré-gate e exigir `APROVADO` apenas a partir do ponto formal definido pelo contrato.

### [DIVERGE-02] A política de `INDETERMINADO` pode contradizer o próprio tratamento estruturado

- Severidade: **BLOQUEANTE**
- Arquivo/trecho: `micromodelo.schema.json`, `saida.publicacao.politica_indeterminado`, que possui `tratamento` fechado mas `descricao` livre; `tools/micromodelo_mm01_contract.py`, que valida presença do contrato e proveniência `APROVADO`, sem checar coerência entre `tratamento` e `descricao`.
- Como reproduzir: em fase `CANDIDATO_PRODUTO` ou posterior, usar `tratamento=CAMPO_COBERTURA_SEPARADO`, proveniência `APROVADO`, e `descricao="indeterminado deve ser gravado como FALSE"`.
- Esperado: nenhuma interpretação válida da mesma especificação deve permitir que `INDETERMINADO` seja silenciosamente confundido com `FALSE`.
- Observado: um consumidor que segue `tratamento` preserva cobertura separada; outro que segue `descricao` converte para `FALSE`.
- Impacto: falha o critério 19 e reabre a ambiguidade `FALSE` × ausência de evidência.
- Recomendação: fazer o comportamento executável depender de enumeração/estrutura semântica fechada e impedir descrições contraditórias.

### [DIVERGE-03] `score.calibracao.evidencia_ref` aceita referência órfã

- Severidade: **BLOQUEANTE**
- Arquivo/trecho: `micromodelo.schema.json`, `score.calibracao.evidencia_ref`, definido apenas como string não vazia; no validador, a calibração verifica proveniência e `MEDIDO`, mas não resolve `evidencia_ref` contra coleção canônica.
- Como reproduzir: configurar `tipo_semantica=PROBABILIDADE_CALIBRADA`, preencher calibração com proveniência `MEDIDO` e referência de execução sintaticamente válida, mas usar `evidencia_ref="exp_inexistente"`.
- Esperado: calibração usada para autorizar semântica probabilística deve apontar para evidência referenciável segundo namespace explicitamente definido.
- Observado: não existe lookup de `evidencia_ref`; qualquer string aceita pelo schema satisfaz essa parte do contrato.
- Impacto: o contrato pode declarar probabilidade calibrada citando evidência inexistente dentro da especificação.
- Recomendação: definir explicitamente o namespace de `evidencia_ref` e validar integridade referencial, incluindo teste de referência órfã e, se aplicável, incompatibilidade entre tipo de evidência e calibração.

**MELHORÁVEL — Nenhum achado.**

## 5. Cobertura dos critérios

| Critério | Status | Evidência |
|---|---|---|
| 1. Micromodelo permanece artefato de domínio; sem sétimo tipo/skill antecipada | PASS | ADR-0014 proíbe o sétimo tipo; política vigente lista 14 skills e não inclui `hub-ml-micromodelos`; PR não altera `.assistant`. |
| 2. Especificação canônica estruturada compatível com `micromodelo.yaml` | PASS | Schema formal + template YAML existem; ADR-0015 define o YAML como fonte estruturada canônica. |
| 3. Draft 2020-12 válido e blocos materiais fechados | PASS | Teste formal passou; raiz e objetos materiais usam `additionalProperties: false`. |
| 4. `fase` e `condicao` distintas | PASS | `identidade.estado` possui `fase_atual`, `fase_anterior`, `condicao` e `motivo_condicao`; regras são separadas. |
| 5. Máquina rejeita saltos e permite somente rework previsto | PASS | Tabela fechada rejeitou `EM_DESCOBERTA → VALIDADO`; testes permanentes também verificam rework/skip. |
| 6. `PUBLICADO` não pode ser silenciosamente rebobinado na mesma versão | **FAIL** | QUEBRA-01. |
| 7. Estados de proveniência têm significado operacional distinto | PASS | Enum e blocos exclusivos distinguem estados. |
| 8. `APROVADO` exige decisão humana auditável | **FAIL** | QUEBRA-02. |
| 9. `MEDIDO` exige referência de execução | **FAIL** | QUEBRA-02. |
| 10. `FALSE` distinto de ausência/`INDETERMINADO` | PASS | Valores de estudo fechados e normalização semântica. |
| 11. Silêncio não vira `FALSE` sem regra explícita aprovada | PASS | Política de ausência exige tratamento explícito e aprovação. |
| 12. Score habilitado tem semântica e escala 0–100 | PASS | Regras do validador e schema. |
| 13. Score 0–100 não é automaticamente probabilidade | PASS | Tipo semântico explícito e linguagem probabilística recusada fora de calibração. |
| 14. Semântica probabilística exige calibração medida e execução referenciada | **FAIL** | QUEBRA-02 e DIVERGE-03. |
| 15. Pesos/limiares materiais não avançam sem aprovação | PASS | Guardrail de avanço existe; DIVERGE-01 aponta aplicação precoce. |
| 16. Fontes restritas a `CATALOGO_PRODUTO`; fixtures sanitizados | PASS | Allowlist fechada e fixtures sintéticos. |
| 17. Evidência/contra-evidência não referencia fonte inexistente | PASS | `UNKNOWN_SOURCE_REF`. |
| 18. Estudo preserva `TRUE`, `FALSE`, `INDETERMINADO` | PASS | `saida.estudo.valores_classificacao` é constante. |
| 19. Publicação exige BOOLEAN + política aprovada para `INDETERMINADO`, sem confusão com `FALSE` | **FAIL** | DIVERGE-02. |
| 20. Autoridade final de publicação permanece externa | **FAIL** | Autoridade é externa, mas QUEBRA-02 permite referência externa semanticamente vazia. |
| 21. YAML não vira histórico crescente de runs | PASS | `tracking.armazenar_historico_runs_no_yaml=false`; ADR-0016 mantém histórico no MLflow. |
| 22. Não antecipa MM02/MM03/MM06/visual/migração/publicação real | PASS | Escopo nominal permanece contrato/fixtures/testes/workflow/docs. |
| 23. Testes/fixtures não dependem de dados, ACL, workspace ou segredo real | PASS | Fixtures sintéticos e gate estrutural aprovado. |
| 24. Workflow permanente é read-only e não executa ação corporativa | PASS | `contents: read`, `persist-credentials: false`; somente testes/gates locais. |

## 6. Veredito

**VEREDITO: `NAO_APTA`**

### Bloqueios para aceite

- Corrigir a proteção de ciclo de vida para que um micromodelo já `PUBLICADO` não possa ser rebobinado silenciosamente na mesma versão por simples reescrita de `fase_anterior`.
- Tornar aprovação humana, `MEDIDO`, handoff e confirmação de Produto de Dados semanticamente não vazios; whitespace não pode satisfazer gate auditável.
- Resolver a divergência entre proveniência progressiva e a exigência incondicional de `APROVADO` para qualquer limiar/peso, preservando `PROPOSTO` antes da fase que efetivamente exige aprovação.
- Tornar a política de `INDETERMINADO` não contraditória entre campo estruturado e descrição.
- Definir e validar a integridade referencial de `score.calibracao.evidencia_ref`, incluindo referência órfã.
- Adicionar testes adversariais de regressão para todos os bypasses acima e repetir os gates completos.

### Melhorias não bloqueantes

- Nenhum achado.

### Condições para reauditoria

- Reexecutar, sobre novo HEAD identificado, `python -m pip install -r tools/requirements-dev.txt`, `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`, `python -B tools/validate_assistant.py --root ambiente_fonte` e a CLI direta do template.
- Reexecutar especificamente os adversariais de rewind pós-`PUBLICADO`, whitespace em provas auditáveis, `PROPOSTO` pré-gate, política contraditória de `INDETERMINADO` e calibração com referência órfã.
- Confirmar que as correções não antecipam fingerprint/MM02, catálogo/MM03, MLflow definitivo/MM06, publicação real, visual ou migração.
- Manter MM02 bloqueada até nova A1 sobre a árvore corrigida e aceite explícito.
