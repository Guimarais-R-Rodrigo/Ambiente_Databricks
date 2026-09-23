# RELATÓRIO DE AUDITORIA A1 — MM01

## 1. Identificação

-  Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks` 
-  Branch: `micromodelos/mm01-contrato-canonico` 
-  HEAD auditado: `9e3ce44ae0750321802b95d96ff43bb29468eab2`, confirmado diretamente na branch ao início e reconfirmado ao final. 
- `main` observada: `28669f99db27cf23df73549297bbf57eda033f58`. 
-  Merge-base com main: `28669f99db27cf23df73549297bbf57eda033f58` 
-  Comparação: `ahead_by=100`, `behind_by=0`, 100 commits, 24 arquivos alterados. 
-  PR #51: aberta, `merged=false`, `draft=false`, `mergeable=true`; endpoint REST retornou `mergeable_state=clean`. O HEAD/base e as contagens permanecem 100 commits e 24 arquivos. 
-  Python: CPython **3.12.14** no runner canônico reproduzido; Python 3.13.5 foi usado apenas para adversariais isolados sobre os mesmos predicados, com `jsonschema 4.26.0` e `PyYAML 6.0.3`. 
-  Dependências: instalação concluída com sucesso na reprodução do workflow. 
-  Limitações de ambiente: a A1 obedeceu à hierarquia normativa de `01_contexto.md` e `02_prompt_auditoria.md`. Por isso, `CHANGELOG.md`, relatórios A1 anteriores e os documentos narrativos MM01 (`README`, `CONTRATO_MICROMODELO`, `ESTADOS_E_PROVENIENCIA`, `TESTES`, `CHECKPOINT`) não foram usados nem lidos como fundamento da conclusão; o próprio contexto os classifica explicitamente como fontes vedadas.  A auditoria concentrou-se nas fontes primárias permitidas e nos adversariais independentes exigidos. 

## 2. Execuções reproduzidas

| ExecuçãoResultadoEvidência objetiva                             |                             |                                                                                                                                                                   |
| --------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Estado GitHub da candidata                                      | PASS                        | HEAD `9e3ce44…`, `main=28669f9…`, merge-base=`main`, `ahead=100`, `behind=0`; PR aberta, não merged, não draft e mergeable                                        |
| `python -m pip install -r tools/requirements-dev.txt`           | PASS                        | Reprodução em runner real Ubuntu 24.04.5 / CPython 3.12.14 concluída; `jsonschema 4.26.0` e `PyYAML 6.0.3` instalados                                             |
| `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v` | PASS                        | **36 testes executados; 36 OK**                                                                                                                                   |
| Validação do template pela CLI                                  | PASS                        | `test_cli_returns_zero_for_template_and_one_for_invalid_document` executa a CLI real sobre o template e exige RC=0/`APROVADO`; passou.                            |
| `python -B tools/validate_assistant.py --root ambiente_fonte`   | PASS                        | Reprodução: `APROVADO: 0 falha(s), 0 aviso(s)`; 14/14 skills estruturalmente válidas                                                                              |
| Workflow permanente MM01                                        | PASS                        | Job reproduzido nesta auditoria (`104557187778`) concluiu `success`; o check atual está associado ao HEAD real. O endpoint contém exatamente 7 check-runs atuais. |
| Permissões/credenciais do workflow                              | PASS                        | `contents: read`, checkout com `persist-credentials: false`; workflow executa suíte, `validate_assistant` e registro de fronteira, sem ação corporativa.          |
| Outros 6 checks do HEAD                                         | PASS                        | CI local, V00, V01, V02, V10 e V11 possuem jobs reais concluídos em `success`; não são checks vazios                                                              |
| Runs administrativos vermelhos anteriores                       | PASS quanto à classificação | Sete runs antigos `failure/action_required` foram inspecionados individualmente e retornaram `jobs=[]`; portanto não houve runner nem execução de código          |
| Merge-ref usado pelo CI                                         | PASS                        | CI usou `683712cfff3ef23be78e1e209e33a524bcc9dcc3`; comparação com o HEAD retornou `files=[]`                                                                     |
| Merge-ref atual da PR                                           | PASS                        | `10bc94c1c2a060547ed5fe3e0081c60770534803`; comparação com HEAD também retornou `files=[]`; árvore materialmente equivalente                                      |
| Reconciliação com SEF                                           | PASS                        | `PLANO_MESTRE.md` possui o mesmo blob SHA `4a7c0a3…` em `main` e na candidata.                                                                                    |
| Alterações em `.assistant`                                      | PASS                        | Nenhum dos 24 arquivos da PR pertence a `.assistant`; `validate_assistant` permaneceu verde                                                                       |
| Template/fixture positivo                                       | PASS                        | Fixture utiliza `CATALOGO_PRODUTO`, nomes explicitamente sintéticos e proveniência/execuções sintéticas.                                                          |

A reprodução mínima obrigatória definida pelo prompt normativo foi, portanto, possível.

## 3. Casos adversariais independentes

| CasoResultado observadoCódigo/erroMotivo correto?                                          |                                                                      |                                 |                      |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- | ------------------------------- | -------------------- |
| Texto somente com whitespace ASCII/Unicode/NBSP                                            | Rejeitado                                                            | `SCHEMA / material-text`        | SIM                  |
| Somente `Mn`, `Mc`, `Me`, `Cf`, ZWSP, ZWNJ, ZWJ, WORD JOINER, U+2063, variation selector   | Rejeitado                                                            | `SCHEMA / material-text`        | SIM                  |
| Somente pontuação, símbolo, emoji ou combinações não materiais                             | Rejeitado                                                            | `SCHEMA / material-text`        | SIM                  |
| Grego, cirílico, árabe, hebraico, CJK, Devanagari, dígitos Unicode e base + combining mark | Aceito                                                               | sem erro                        | SIM                  |
| `pattern: ".*\\S.*"` + `string + minLength` sem `material-text`                            | Guard detecta                                                        | violação de política estrutural | SIM                  |
| Variantes `.+`, `.*[A-Za-z].*`, `.*[^ ].*` sem `material-text`                             | Guard de `minLength` detecta                                         | violação de política estrutural | SIM                  |
| Quarto `pattern` arbitrário em qualquer path                                               | Guard de allowlist detecta                                           | mismatch de allowlist           | SIM                  |
| Deslocamento de pattern autorizado para outro path                                         | Guard detecta                                                        | mismatch de path                | SIM                  |
| Alteração da regex estrutural autorizada                                                   | Guard detecta                                                        | mismatch de regex               | SIM                  |
| Pattern dentro de `$defs`, `items`, `allOf`, `anyOf`, `oneOf` ou branch aninhado           | Travessia recursiva alcança o nó                                     | guard estrutural                | SIM                  |
| `type: ["string"] + minLength`, sem `material-text`                                        | **Não detectado pelo guard permanente**                              | nenhum                          | **NÃO — DIVERGE-02** |
| `type: ["string","null"] + minLength`, sem `material-text`                                 | **Não detectado pelo guard permanente**                              | nenhum                          | **NÃO — DIVERGE-02** |
| `quando_false` igual a `quando_indeterminado` salvo maiúsculas, espaços e pontuação        | Rejeitado                                                            | `AMBIGUOUS_BINARY_SEMANTICS`    | SIM                  |
| Mesma semântica com U+200B inserido dentro de uma palavra                                  | **Aceito**                                                           | nenhum                          | **NÃO — DIVERGE-01** |
| Mesma mutação com ZWNJ, ZWJ, WORD JOINER, U+2063 ou VS16                                   | **Aceito**                                                           | nenhum                          | **NÃO — DIVERGE-01** |
| `limiares[].valor: .nan` via YAML                                                          | **Aceito**                                                           | nenhum                          | **NÃO — DIVERGE-03** |
| `limiares[].valor: .inf`/`-.inf`                                                           | **Aceito**                                                           | nenhum                          | **NÃO — DIVERGE-03** |
| `score.componentes[].peso` não finito                                                      | **Aceito**                                                           | nenhum                          | **NÃO — DIVERGE-03** |
| JSON permissivo com `NaN`/`Infinity`                                                       | Loader Python materializa `float` não finito; schema aceita `number` | nenhum                          | **NÃO — DIVERGE-03** |
| YAML `true:` + `True:`                                                                     | Rejeitado como chave duplicada                                       | `ValueError`                    | SIM                  |
| YAML `true:` + `1:`                                                                        | Rejeitado como chave duplicada                                       | `ValueError`                    | SIM                  |
| YAML `false:` + `0:`                                                                       | Rejeitado como chave duplicada                                       | `ValueError`                    | SIM                  |
| Propriedade desconhecida em bloco material                                                 | Rejeitada                                                            | `SCHEMA`                        | SIM                  |
| Salto `IDEIA → EM_ESTUDO`                                                                  | Rejeitado                                                            | transição inválida              | SIM                  |
| Rewind de `PUBLICADO` na mesma versão                                                      | Rejeitado                                                            | `STATE_REWIND`                  | SIM                  |
| Ausência de evidência → `FALSE` sem política aprovada                                      | Rejeitado                                                            | `MISSING_POLICY_*`              | SIM                  |
| Score probabilístico sem calibração adequada                                               | Rejeitado                                                            | `CALIBRATION_*`                 | SIM                  |
| Calibração apontando para experimento inexistente/não executado-medido                     | Rejeitado                                                            | `CALIBRATION_EVIDENCE_REF`      | SIM                  |
| Fonte fora de `CATALOGO_PRODUTO`                                                           | Rejeitada                                                            | `CATALOG_SCOPE`                 | SIM                  |
| Tentativa de contornar catálogo via `--catalog-ref`                                        | CLI não oferece bypass                                               | RC=2, argumento desconhecido    | SIM                  |
| Score desabilitado mantendo resíduos materiais                                             | Rejeitado                                                            | `SCORE_DISABLED`                | SIM                  |
| `PUBLICADO` sem lifecycle externo necessário                                               | Rejeitado pelos gates de publicação                                  | `PUBLICATION_*`                 | SIM                  |

A política `material-text` em si mostrou-se consistente: `_has_material_text` usa NFKC e exige ao menos uma categoria Unicode `L*` ou `N*`.  A suíte também cobre várias classes Unicode adversariais e positivos multilíngues.

## 4. Achados

### QUEBRA

Nenhum achado.

### [DIVERGE-01] Normalização de equivalência semântica pode ser burlada com caracteres Unicode invisíveis

-  Severidade: **BLOQUEANTE** 
-  Arquivo/trecho: `tools/micromodelo_mm01_contract.py`, `_normalize_semantic_text()` e comparação de `quando_true` / `quando_false` / `quando_indeterminado`. O normalizador faz NFKD + `casefold`, remove somente caracteres com combining class não zero e depois transforma `[\W_]+` em espaço.  A decisão de ambiguidade depende exclusivamente da igualdade dessas três representações normalizadas. 
-  Como reproduzir: tomar duas definições semanticamente iguais, por exemplo `informação disponível ...`, e inserir U+200B entre `dispo` e `nível` em apenas uma delas. Repetir com ZWNJ, ZWJ, WORD JOINER, U+2063 ou VS16. 
-  Esperado: por serem diferenças invisíveis/editoriais, `FALSE` e `INDETERMINADO` semanticamente idênticos deveriam continuar sendo identificados como ambíguos, conforme critério normativo 10 e o adversarial obrigatório de equivalência cosmética. 
-  Observado: o caractere invisível vira fronteira de palavra durante a regex; `disponivel` e `dispo nivel` produzem strings normalizadas diferentes. O documento permanece material para `_has_material_text` e **não** recebe `AMBIGUOUS_BINARY_SEMANTICS`. 
-  Impacto: é possível construir contrato visualmente/semanticamente contraditório que preserve a aparência de três semânticas distintas para o validador. Isso enfraquece diretamente a separação normativa `FALSE` × `INDETERMINADO`. 
-  Recomendação: normalizar explicitamente caracteres Unicode default-ignorable relevantes antes da tokenização — removendo-os quando são puramente editoriais, em vez de convertê-los em separadores — e adicionar regressões permanentes para ZWSP, ZWNJ, ZWJ, WORD JOINER, U+2063 e variation selectors inseridos no interior de palavras. 

### [DIVERGE-02] Guard permanente de `string + minLength` não é semanticamente fail-closed para `type` em array

-  Severidade: **BLOQUEANTE** 
-  Arquivo/trecho: `tools/tests/test_micromodelo_mm01.py`, `_required_minlength_without_material_text()`. 
-  Como reproduzir: mutar temporariamente o schema com:
   `{"type":["string"],"minLength":3}` ou `{"type":["string","null"],"minLength":3}`, sem `format: material-text`. 
-  Esperado: qualquer schema node em que uma instância string esteja sujeita a `minLength` deve exigir a política material comum, independentemente da sintaxe equivalente usada para `type`. 
-  Observado: o helper testa literalmente `node.get("type") == "string"`. Consequentemente, ambos os schemas acima retornam zero violações. A implementação atual do helper está visível diretamente no teste permanente. 
-  Prova adicional: `type: ["string"]` é sintaxe válida no Draft 2020-12; o próprio schema da MM01 já usa listas de tipos em outros campos, por exemplo `["string","null"]`. 
-  Impacto: a árvore **atual** permanece limpa, mas a proteção destinada a impedir regressões futuras pode ser contornada por uma representação JSON Schema válida e já idiomática no próprio contrato. A exigência de fail-closed para novos campos, portanto, não está integralmente satisfeita. 
-  Recomendação: identificar semanticamente a presença do tipo string — `type == "string"` **ou** lista de tipos contendo `"string"` — e acrescentar regressões para `["string"]`, `["string","null"]` e branches aninhados. 

### [DIVERGE-03] Valores numéricos não finitos atravessam limiares e pesos materiais

-  Severidade: **BLOQUEANTE** 
-  Arquivo/trecho: `docs/sprints/micromodelos/MM01/micromodelo.schema.json` e `tools/micromodelo_mm01_contract.py`. 
-  Como reproduzir: fornecer `.nan`, `.inf` ou `-.inf` em YAML para `classificacao.limiares[].valor` ou `score.componentes[].peso`. Também é possível fazê-lo pelo parser JSON Python com tokens permissivos `NaN`/`Infinity`. 
-  Esperado: valores materiais de limiar e peso precisam ser números finitos e semanticamente utilizáveis. 
-  Observado: o schema define ambos apenas como `"type": "number"`, sem restrição de finitude.  `PyYAML 6.0.3` materializa `.nan/.inf` como `float`; `jsonschema 4.26.0` aceita esses objetos como `number`; o validador posterior verifica proveniência/aprovação, mas não `math.isfinite()` para os valores. 
-  Impacto: um limiar ou peso aprovado pode ser materialmente impossível de comparar, ordenar, agregar ou transportar com segurança para JSON estrito/downstream. `NaN`, em particular, possui semântica de comparação patológica (`NaN != NaN`) e pode contaminar cálculo posterior. 
-  Recomendação: rejeitar explicitamente todo número não finito nos pontos materiais do contrato, endurecer o loader JSON quanto a constantes não padrão quando aplicável e adicionar casos permanentes YAML/JSON para `NaN`, `+Infinity` e `-Infinity`. 

### MELHORÁVEL

Nenhum achado.

## 5. Cobertura dos critérios

| CritérioStatusEvidência                                                    |                  |                                                                                                             |
| -------------------------------------------------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------- |
| 1. Micromodelo permanece artefato de domínio, sem 7º tipo/skill antecipada | PASS             | Nenhuma skill/tipo novo nos 24 arquivos; `validate_assistant` mantém 14 skills                              |
| 2. Especificação canônica estruturada compatível com YAML                  | PASS             | Schema + template YAML + loader dedicado                                                                    |
| 3. Draft 2020-12 e propriedades desconhecidas fechadas                     | PASS             | `Draft202012Validator.check_schema` protegido por teste; blocos materiais usam `additionalProperties:false` |
| 4. `fase` e `condicao` distintas                                           | PASS             | Campos/enums independentes e gates específicos                                                              |
| 5. Máquina de estados sem saltos, com rework explícito                     | PASS             | Saltos adversariais rejeitados; tabela permanente testada                                                   |
| 6. `PUBLICADO` sem rewind silencioso na mesma versão                       | PASS             | `STATE_REWIND`; teste via `--previous`                                                                      |
| 7. Proveniências têm significados operacionais distintos                   | PASS             | Gates específicos para DESCOBERTO/INFERIDO/PROPOSTO/APROVADO/MEDIDO                                         |
| 8. `APROVADO` requer decisão humana auditável                              | PASS             | Status sozinho não basta; bloco de aprovação é validado                                                     |
| 9. `MEDIDO` requer referência de execução                                  | PASS             | Medição sem `referencia_execucao` não atravessa o contrato                                                  |
| 10. `FALSE` distinguível de `INDETERMINADO`                                | **FAIL**         | DIVERGE-01 permite equivalência semântica mascarada por Unicode invisível                                   |
| 11. Ausência de evidência não vira `FALSE` silenciosamente                 | PASS             | Estrutura `tratamento/resultado_sem_evidencia/regra_ref` + aprovação                                        |
| 12. Score habilitado tem semântica e escala 0–100                          | PASS             | Validador exige `tipo_semantica`, saída de score e escala exata 0/100.                                      |
| 13. Score 0–100 não implica probabilidade                                  | PASS             | Semânticas enumeradas separadamente                                                                         |
| 14. Probabilidade exige calibração medida e experimento executado/medido   | PASS             | `CALIBRATION_REQUIRED`, `CALIBRATION_EVIDENCE`, `CALIBRATION_EVIDENCE_REF`                                  |
| 15. Pesos/limiares materiais exigem aprovação humana                       | **FAIL parcial** | Gate de aprovação funciona, mas DIVERGE-03 permite que o valor aprovado seja `NaN/Infinity`                 |
| 16. Fontes limitadas a `CATALOGO_PRODUTO`; fixtures sintéticos             | PASS             | Fixture auditado usa `CATALOGO_PRODUTO`, `dominio_sintetico`, `eventos_sinteticos`.                         |
| 17. Referências de evidência não podem ser órfãs                           | PASS             | `UNKNOWN_SOURCE_REF`                                                                                        |
| 18. Estudo preserva TRUE/FALSE/INDETERMINADO                               | PASS             | Contrato de estudo preserva explicitamente os três estados                                                  |
| 19. Publicação BOOLEAN com política explícita para indeterminado           | PASS             | Campo BOOLEAN e política estruturada; conversão implícita para FALSE bloqueada                              |
| 20. Autoridade de publicação externa                                       | PASS             | ADR/validador mantêm handoff e autoridade externa; nenhuma ação corporativa executada                       |
| 21. YAML não acumula histórico de runs                                     | PASS             | Proveniência pontual; nenhum log crescente embutido                                                         |
| 22. Não antecipa MM02/MM03/MM04/MM06/legado/publicação real                | PASS             | Ausência dessas implementações na árvore alterada; `--previous` segue snapshot-vs-snapshot                  |
| 23. Testes/fixtures não dependem de dado/ACL/workspace/segredo real        | PASS             | Dados e referências sintéticos                                                                              |
| 24. Workflow MM01 read-only e sem ação corporativa                         | PASS             | Permissões somente leitura; runner reproduzido sem Databricks/UC/MLflow/ACL real                            |
| Autoridade única de materialidade textual                                  | PASS             | `_has_material_text` + `format: material-text`; não foi encontrada segunda regex material concorrente.      |
| Inventário de `pattern`                                                    | PASS             | Somente 3 ocorrências estruturais, congeladas por path + regex                                              |
| Política dos `string + minLength` existentes                               | PASS             | Todos os 40 nós atuais possuem `format: material-text`                                                      |
| Fail-closed do guard para futuros `string + minLength`                     | **FAIL**         | DIVERGE-02                                                                                                  |
| Coerência de números materiais                                             | **FAIL**         | DIVERGE-03                                                                                                  |
| Template e fixture positivo                                                | PASS             | CLI/template e fixture validado passam                                                                      |
| Reconciliação com `main`/SEF                                               | PASS             | `behind_by=0`; blob SEF idêntico; nenhuma modificação `.assistant`                                          |
| CI/check-runs                                                              | PASS             | 7 checks atuais verdes; MM01 reproduzido nesta A1                                                           |
| Documentação narrativa MM01                                                | INCONCLUSIVO     | Deliberadamente não auditada como fonte nesta A1 porque `01_contexto.md` a veda expressamente.              |

Inventário completo de `pattern`:

| PathRegexFinalidade`material-text` coexistente?Autoridade textual concorrente? |                          |                            |     |     |
| ------------------------------------------------------------------------------ | ------------------------ | -------------------------- | --- | --- |
| `$defs.id`                                                                     | `^[a-z][a-z0-9_]{2,63}$` | identificador estrutural   | NÃO | NÃO |
| `properties.identidade.properties.nome`                                        | `^[a-z][a-z0-9-]{2,63}$` | slug/nome estrutural       | NÃO | NÃO |
| `properties.identidade.properties.micromodel_version`                          | `^\d+\.\d+\.\d+$`        | forma estrutural de versão | NÃO | NÃO |

Não existe quarto `pattern`. O teste permanente percorre dicts e listas recursivamente, proíbe `material-text + pattern` e compara a coleção observada com essa allowlist exata.

Inventário completo dos **40 nós diretos** **`type:string + minLength`**. Todos são categoria **A — conteúdo material governado por** **`format: material-text`**:

| GrupoPaths               |                                                                                                                                                                   |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$defs`                  | `$defs.proveniencia.properties.origem`; `$defs.proveniencia.properties.aprovacao.properties.por`; `$defs.material_ref`                                            |
| `identidade` / `negocio` | `identidade.titulo`; `negocio.caracteristica`; `negocio.objetivo`; `negocio.definicao_operacional`; `negocio.uso_pretendido.items`; `negocio.nao_usar_para.items` |
| `entidade`               | `entidade.tipo`; `entidade.chave_logica`; `entidade.granularidade`; `entidade.populacao_elegivel`; `entidade.referencia_temporal`                                 |
| `fontes`                 | `fontes[].catalogo_ref`; `fontes[].schema`; `fontes[].objeto`; `fontes[].campos[]`                                                                                |
| `evidencias`             | `evidencias[].descricao`; `evidencias[].regra`                                                                                                                    |
| `contra_evidencias`      | `contra_evidencias[].descricao`; `contra_evidencias[].regra`                                                                                                      |
| `classificacao`          | `semantica.quando_true`; `semantica.quando_false`; `semantica.quando_indeterminado`; `limiares[].descricao`; `limiares[].unidade`                                 |
| `score`                  | `componentes[].descricao`; `calibracao.metodo`                                                                                                                    |
| `experimentos`           | `experimentos[].hipotese`                                                                                                                                         |
| `validacao`              | `validacao.criterios[]`; `validacao.resultado.resumo`                                                                                                             |
| `saida`                  | `saida.estudo.campo_classificacao`; `saida.publicacao.campo_booleano.nome`                                                                                        |
| `governanca`             | `governanca.classificacao_dados`; `governanca.lgpd`; `governanca.gestor_informacao`                                                                               |
| `proveniencia` raiz      | `proveniencia.gerado_por`; `proveniencia.pedido_original_ref`; `proveniencia.registros[].alvo`                                                                    |

As ocorrências aparecem de forma consistente ao longo do schema.

Categorias **B, C e D entre os nós** **`string + minLength`** **atuais: nenhuma ocorrência**. Os três identificadores governados por `pattern` são estruturais, mas não pertencem a esse conjunto porque não possuem `minLength`.

## 6. Veredito

**VEREDITO: APTA_COM_CORRECOES**

A arquitetura principal da MM01 é reproduzível e permaneceu íntegra: schema válido, template executável, máquina de estados, proveniência, score/calibração, referências, publicação externa, fronteiras de escopo e CI funcionam; o job MM01 reproduzido nesta sétima A1 executou **36/36 testes com sucesso**, e a reconciliação com `main` permanece limpa.

Entretanto, esta auditoria independente encontrou **três DIVERGÊNCIAS materiais e bloqueantes**, todas reproduzíveis e localizadas. Pelo critério normativo, isso impede `APTA`, mas não invalida a arquitetura como um todo; portanto corresponde a `APTA_COM_CORRECOES`.

Bloqueios para aceite:

- **DIVERGE-01:** equivalência `FALSE` × `INDETERMINADO` pode ser mascarada com caracteres Unicode invisíveis inseridos dentro de palavras. 
- **DIVERGE-02:** o guard permanente de `string + minLength` não cobre `type` representado por array, deixando uma via válida de regressão futura sem `material-text`. 
- **DIVERGE-03:** `NaN` e `±Infinity` podem atravessar `limiares[].valor` e `score.componentes[].peso`. 

Melhorias não bloqueantes:

-  Nenhuma. 

Condições para reauditoria:

-  Corrigir a normalização semântica e adicionar regressões permanentes para caracteres Unicode invisíveis/default-ignorable em posições internas. 
-  Tornar o guard de `string + minLength` semântico em relação a `type`, cobrindo `["string"]`, `["string","null"]` e estruturas aninhadas. 
-  Rejeitar explicitamente valores numéricos não finitos nos campos materiais e adicionar adversariais YAML/JSON correspondentes. 
-  Reexecutar integralmente a suíte MM01, `validate_assistant`, template CLI e adversariais das três classes. 
-  Reconfirmar HEAD, `main`, merge-base, `behind_by`, mergeabilidade, check-runs e equivalência do merge-ref. 
-  Não dar aceite, não fechar `CHANGELOG.md`, não iniciar MM02 e não fazer merge enquanto os três bloqueios permanecerem. 