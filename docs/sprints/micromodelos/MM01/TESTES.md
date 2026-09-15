# MM01 — Plano e evidências de testes

## Escopo

Os testes da MM01 exercitam o contrato estrutural e semântico. Não acessam Databricks, Unity Catalog, MLflow, dados reais, ACLs nem publicação externa. Todos os recursos usados são sintéticos.

## Matriz de comportamento

| ID | Caso | Resultado esperado |
|---|---|---|
| T01 | JSON Schema Draft 2020-12 | schema formal aceito |
| T02 | `micromodelo.template.yaml` | APROVADO |
| T03 | fixture `VALIDADO` completo | APROVADO |
| T04 | grupo obrigatório ausente | `SCHEMA` |
| T05 | salto `IDEIA → EM_VALIDACAO` | `STATE_TRANSITION` |
| T06 | score habilitado sem semântica estruturada | `SCORE_SEMANTICS` |
| T07 | limiar/peso `PROPOSTO` antes de `EM_VALIDACAO` | permitido como proposta |
| T08 | limiar/peso não aprovado em `EM_VALIDACAO+` | `THRESHOLD_APPROVAL` / `WEIGHT_APPROVAL` |
| T09 | resultado `MEDIDO` sem referência material de execução | rejeição fail-closed |
| T10 | aprovação humana com referência vazia, whitespace, zero-width ou marca Unicode isolada | rejeição fail-closed |
| T11 | fase `PUBLICADO` sem validação/saída/publicação externa | gates de fase/publicação |
| T12 | `PUBLICADO` com referência externa vazia, whitespace ou marca Unicode isolada | rejeição fail-closed |
| T13 | fonte com `catalogo_ref` não autorizado | `CATALOG_SCOPE` |
| T14 | definições TRUE/FALSE/INDETERMINADO semanticamente iguais | `AMBIGUOUS_BINARY_SEMANTICS` |
| T15 | `PROBABILIDADE_CALIBRADA` sem calibração | `CALIBRATION_REQUIRED` |
| T16 | calibração com `evidencia_ref` órfã ou experimento não executado/medido | `CALIBRATION_EVIDENCE_REF` |
| T17 | evidência referencia fonte inexistente | `UNKNOWN_SOURCE_REF` |
| T18 | score desabilitado com resíduos de score | `SCORE_DISABLED` |
| T19 | decisão humana diverge do `validacao.status` | `VALIDATION_HUMAN_GATE` |
| T20 | skips de fase e retorno declarado diretamente de `PUBLICADO` | recusados pela tabela de transições |
| T21 | especificação anterior `PUBLICADO` reescrita na mesma versão para fase anterior | `STATE_REWIND` |
| T22 | comparação com especificação anterior preserva identidade/versão e valida transição real | fail-closed |
| T23 | CLI `--previous` bloqueia rewind pós-publicação | exit não zero + diagnóstico |
| T24 | propriedade livre `score.semantica` tenta reintroduzir prosa probabilística | `SCHEMA` |
| T25 | `tipo_semantica=PROBABILIDADE_CALIBRADA` com calibração medida/resolvida | APROVADO |
| T26 | calibração presente em score não probabilístico | `CALIBRATION_UNEXPECTED` |
| T27 | normalização textual/legada em vez de contrato estruturado | `SCHEMA` |
| T28 | normalização `PENDENTE` ao chegar em `EM_VALIDACAO+` | `SCORE_NORMALIZATION` |
| T29 | IDs duplicados em componentes/experimentos | `DUPLICATE_ID` |
| T30 | `EM_VALIDACAO+` com fontes/evidências/contra-evidências/critérios vazios | `PHASE_CONTENT_GATE` |
| T31 | status de publicação incompatível com fase | `PUBLICATION_STATUS_PHASE` |
| T32 | política de ausência `INDETERMINADO` com `resultado_sem_evidencia=FALSE` | `MISSING_POLICY_CONTRADICTION` |
| T33 | tentativa de reintroduzir `descricao` normativa em ausência/publicação | `SCHEMA` |
| T34 | política `REGRA_EXPLICITA_APROVADA` com regra auditável | APROVADO |
| T35 | `indeterminado_vira_false=true` | `SCHEMA` / gate estruturado |
| T36 | caminhos positivos `CANDIDATO_PRODUTO → EM_VALIDACAO_GOVERNANCA → PUBLICADO` | APROVADOS |
| T37 | propriedade material desconhecida | `SCHEMA` |
| T38 | YAML/JSON com chave duplicada | erro de carga fail-closed |
| T39 | CLI válido/inválido e tentativa de `--catalog-ref` não contratada | exit 0/1/2 |
| T40 | gate estrutural do repositório | `tools/validate_assistant.py` sem FAIL |
| T41 | CI agregado da PR | regressão zero no head final técnico |
| T42 | política `material-text`: marcas/formatos/whitespace/pontuação/símbolo isolados | `SCHEMA` |
| T43 | materialidade Unicode positiva (`é`, CJK, algarismos Unicode, Devanagari, combining mark com base material) | APROVADO |
| T44 | proveniência de topo e gates materiais usam a mesma política Unicode | rejeição/aceite coerentes |

A suíte `tools/tests/test_micromodelo_mm01.py` contém **29 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz. `casos_invalidos.json` mantém nove mutações negativas determinísticas além dos casos adversariais construídos diretamente pela suíte.

## Teste específico de YAML

O template não usa chaves literais `true:`/`false:`. PyYAML pode interpretar essas palavras como booleanos; por isso o contrato usa `quando_true`, `quando_false` e `quando_indeterminado`.

Além disso, o carregador customizado rejeita chaves duplicadas em YAML e JSON. A MM01 não aceita o comportamento “última chave vence”, porque uma especificação material poderia aparentar um valor na revisão humana e efetivamente validar outro.

## Regressões de materialidade Unicode

A segunda A1 demonstrou que excluir apenas categorias `Z*`/`C*` deixava passar marcas Unicode `M*`. A suíte agora testa U+034F, U+FE0F e U+0301 nos campos auditáveis relevantes. A regra semântica positiva exige, após NFKC, pelo menos uma letra ou número Unicode; marcas combinantes/variation selectors isolados não satisfazem aprovação, medição ou confirmação externa.

## Semântica executável sem regex de intenção

A segunda A1 também demonstrou que listas abertas de verbos/sinônimos não conseguem garantir coerência semântica. A correção removeu esse mecanismo:

- `classificacao.ausencia_evidencia` é estruturada por `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência;
- `saida.publicacao.politica_indeterminado` não possui descrição normativa livre; `indeterminado_vira_false=false` é estrutural;
- `score.tipo_semantica` é a autoridade executável; `score.semantica` livre deixou de fazer parte do schema;
- `score.normalizacao` é um objeto estruturado, não uma frase livre.

Os testes verificam tanto os caminhos positivos quanto tentativas de reintroduzir os campos livres legados, que devem falhar com `SCHEMA`.

## Fixtures

`tools/tests/fixtures/micromodelos_mm01/` contém:

- `valido_validado.json`: caso completo em fase `VALIDADO`;
- `casos_invalidos.json`: nove mutações negativas aplicadas à base válida.

Os testes adversariais adicionais criam cópias em memória para evitar inflar fixtures com variações mecânicas.

## Evidências históricas preservadas

### Materialização inicial — failure de transporte

- run `34899029039`;
- **failure** antes da instalação/testes por corrupção do pacote gzip usado como transporte transitório;
- nenhum artefato de produto foi publicado por essa execução;
- a falha é histórica e não foi reclassificada como teste funcional.

### Primeira A1 — `NAO_APTA`

A primeira auditoria independente encontrou cinco bloqueios procedentes: rewind pós-`PUBLICADO`, referências semanticamente vazias, gate prematuro para `PROPOSTO`, contradição de `INDETERMINADO` por prosa e `evidencia_ref` de calibração órfã. O relatório permanece versionado em `03_resultado_a1.md`.

### Reteste das correções da primeira A1

- run transitório final `34909835696`: **success**;
- 24 métodos: `OK`;
- gate estrutural: `APROVADO`, zero falhas/avisos;
- mecanismos transitórios removidos antes da publicação.

### Segunda A1 — `NAO_APTA`

A reauditoria independente sobre `2783bcbd6ad7f07f9f3893c66c9dc36d0557f57e` encontrou três novos bloqueios procedentes:

1. marcas Unicode `M*` ainda satisfaziam provas auditáveis;
2. proteção `FALSE` × `INDETERMINADO` ainda dependia de regex sobre prosa livre;
3. interpretação probabilística ainda podia escapar por sinônimos não cobertos.

O relatório histórico está versionado em `04_resultado_a1_reauditoria.md` e não será reclassificado.

### Reteste das correções da segunda A1

- workflow transitório `34912665666`: **success**;
- `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`: **26 métodos, OK**;
- `python -B tools/validate_assistant.py --root ambiente_fonte`: **APROVADO, 0 falhas, 0 avisos**;
- script e workflow transitórios foram removidos antes do commit permanente `f46b69790fc23ac6c3ebfa633053a3acb6f9ed1a`;
- a correção não introduziu fingerprint, crawler, MLflow definitivo, publicação real, visual próprio ou migração.

O run transitório é evidência de construção, não substitui os workflows permanentes da candidata documental final. Os IDs dos checks permanentes do próximo HEAD congelado serão mantidos na descrição da PR #51 para evitar commits autorreferentes.

## Terceira A1 — `APTA_COM_CORRECOES`

A terceira auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, e registrou três divergências bloqueantes de materialidade textual/Unicode:

1. `$defs.material_ref` impunha ASCII no schema enquanto o validador aceitava letra/número Unicode;
2. `proveniencia.pedido_original_ref`, `proveniencia.gerado_por` e `proveniencia.registros[].alvo` escapavam da política material;
3. semânticas obrigatórias, critérios, nomes de fonte e campos de saída podiam satisfazer gates com whitespace, zero-width, pontuação ou símbolos sem conteúdo material.

O resultado histórico está versionado em `05_resultado_a1_reauditoria_2.md` e permanece `APTA_COM_CORRECOES`, independentemente das correções posteriores.

### Reteste das correções da terceira A1

O mecanismo transitório foi executado novamente no run `34955861169`. Antes de publicar qualquer artefato permanente, ele removeu seus próprios arquivos e concluiu com sucesso:

- instalação por `python -m pip install -r tools/requirements-dev.txt`;
- `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`, com **29 métodos**;
- CLI direta sobre template, fixture positiva, caso Unicode positivo, caso Unicode negativo e continuidade por `--previous`;
- `python -B tools/validate_assistant.py --root ambiente_fonte`;
- publicação do commit permanente `4f686e5de163b649c4ee5e7643f75ecd56db47e7`.

Esse reteste é evidência de construção. A candidata documental final ainda precisa dos workflows permanentes verdes no SHA exato e de uma nova auditoria independente.

## Próxima auditoria A1

Uma **quarta auditoria A1 independente** é obrigatória porque a candidata mudou materialmente depois da terceira A1. Ela deve trabalhar sobre o novo HEAD congelado e não pode usar os relatórios anteriores, a narrativa do autor, o changelog ou mensagens de commit como prova.

A quarta A1 deve repetir instalação, 29 testes, gate estrutural, CLI direta e adversariais próprios; verificar simultaneamente falsos positivos e falsos negativos Unicode; cobrir todos os campos equivalentes; confirmar a unicidade da autoridade de materialidade; validar `--previous`; e confirmar que MM01 não antecipou MM02/MM03/MM04/MM06.

MM02 permanece bloqueada até nova A1, contraditório se necessário, fechamento do changelog, aceite explícito e integração da MM01.
