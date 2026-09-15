# MM01 — Contrato canônico de micromodelos

Status da sprint: **SÉTIMA A1 `APTA_COM_CORRECOES`; `DIVERGE-01`, `DIVERGE-02` E `DIVERGE-03` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; 7 WORKFLOWS PERMANENTES VERDES; OITAVA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**
Base inicial: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`  
Branch: `micromodelos/mm01-contrato-canonico`  
PR: `#51`

## Objetivo

Transformar as decisões arquiteturais aceitas na MM00 em um contrato estrutural verificável para cada micromodelo. A MM01 define o conteúdo mínimo de `micromodelo.yaml`, a máquina de fases, as condições operacionais, a proveniência das afirmações materiais e os gates semânticos que impedem avançar um artefato incompleto.

A sprint não cria a skill `hub-ml-micromodelos`. O validador desta entrega vive em `tools/` como **oráculo de construção e CI** porque a lista de skills é fechada e a skill só nasce na MM04. Quando a MM04 criar o objeto roteável, ela deverá incorporar/derivar o contrato vigente sem criar uma segunda fonte de verdade.

A implementação começou sobre a `main` final da MM00 e foi reconciliada de forma fail-closed com as evoluções posteriores do Sistema de Temas, inclusive V10 e V11. Nenhum arquivo funcional dessas sprints foi reimplementado pela MM01; elas foram absorvidas apenas como base vigente do repositório.

## Entregas

- `micromodelo.schema.json`: schema formal Draft 2020-12, versão `1.0.0`;
- `micromodelo.template.yaml`: template inicial válido e sanitizado;
- `CONTRATO_MICROMODELO.md`: semântica de cada grupo e regras de preenchimento;
- `ESTADOS_E_PROVENIENCIA.md`: máquina de fases, condições, proveniência e gates;
- `tools/micromodelo_mm01_contract.py`: validador de referência/CI;
- fixtures sintéticos positivos e negativos em `tools/tests/fixtures/micromodelos_mm01/`;
- `tools/tests/test_micromodelo_mm01.py`: suíte automatizada com **39 métodos** e múltiplos subtests;
- `.github/workflows/micromodelos-mm01-ci.yml`: gate permanente, read-only, para branch/PR/`main`;
- pacote de auditoria A1 com contexto, prompt e sete resultados históricos preservados (`NAO_APTA`, `NAO_APTA`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`, `APTA_COM_CORRECOES`);
- `TESTES.md` e `CHECKPOINT.md`.

## Decisões fechadas nesta sprint

### Fase e condição são dimensões diferentes

A fase analítica segue o ciclo:

```text
IDEIA
→ EM_DESCOBERTA
→ EM_ESTUDO
→ EM_VALIDACAO
→ VALIDADO
→ CANDIDATO_PRODUTO
→ EM_VALIDACAO_GOVERNANCA
→ PUBLICADO
```

`BLOQUEADO`, `SUSPENSO` e `DEPRECATED` são condições ortogonais, não saltos da máquina de fases.

`fase_anterior` torna o par declarado localmente verificável, mas não é tratada como prova autorreferente de histórico. Quando um snapshot anterior confiável existe, a CLI aceita `--previous` e valida a transição contra a fase efetivamente observada nele. Uma versão já `PUBLICADO` não pode ser silenciosamente reescrita para fase anterior mantendo a mesma `micromodel_version`.

### `FALSE` não significa “não encontrei evidência”

O contrato exige três definições distintas: `quando_true`, `quando_false` e `quando_indeterminado`. A comparação normaliza diferenças editoriais simples; não é possível contornar o gate copiando a mesma definição com caixa, acento ou pontuação diferente.

Após a segunda A1, a política de ausência de evidência deixou de depender de prosa normativa. O comportamento é declarado por `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência. `tratamento=INDETERMINADO` exige resultado `INDETERMINADO`; uma conversão explícita para outro resultado só pode existir como `REGRA_EXPLICITA_APROVADA` com referência auditável.

### Score 0–100 não é probabilidade por padrão

`score.tipo_semantica` é a única autoridade executável sobre a natureza do score. `FORCA_EVIDENCIA`, `PROBABILIDADE_CALIBRADA` e `OUTRA_APROVADA` são estados estruturados; o campo livre `score.semantica` deixou de fazer parte do schema.

Assim, textos como “percentual estimado”, “risco percentual”, “likelihood”, “chance” ou “probabilidade” não podem redefinir silenciosamente um score não probabilístico. Se o score for probabilístico, o contrato exige `PROBABILIDADE_CALIBRADA`, calibração `MEDIDO` e `evidencia_ref` resolvida para experimento existente, `EXECUTADO` e `MEDIDO`.

A normalização também é estruturada (`PENDENTE`, `SOMA_PONDERADA_0_100`, `MIN_MAX_0_100`, `LINEAR_0_100` ou `CUSTOM_APROVADO`) e carrega proveniência. Em `EM_VALIDACAO+`, ela precisa estar definida e aprovada.

### Decisões materiais são progressivas, mas não atravessam gate sem aprovação

Limiar ou peso pode permanecer `PROPOSTO` em descoberta/estudo, preservando a alimentação progressiva da fonte canônica. A partir de `EM_VALIDACAO`, limiares e pesos existentes precisam estar `APROVADO`.

Na mesma fase, fontes, evidências, contra-evidências e critérios de validação precisam estar presentes; semânticas, políticas e regras materiais precisam satisfazer seus contratos estruturados.

### Provas auditáveis precisam conter informação material

A segunda A1 demonstrou que uma blacklist de whitespace/controles não era suficiente para caracteres Unicode `M*`. A terceira A1 mostrou que schema e validador ainda podiam divergir e que campos materiais equivalentes não compartilhavam a mesma autoridade. A regra atual é positiva e única: após NFKC, conteúdo material precisa conter ao menos uma letra ou número Unicode.

O JSON Schema usa `format: material-text` e o `FormatChecker` do validador delega esse formato à mesma função `_has_material_text`. Isso rejeita strings compostas somente por espaços, zero-width, variation selectors, combining marks isolados, pontuação ou símbolos nos campos materiais, sem rejeitar CJK, Devanagari, caracteres acentuados, algarismos Unicode ou combining marks acompanhados de texto material. Campos puramente narrativos não foram restringidos indiscriminadamente.

A quarta A1 identificou seis campos normativos equivalentes que ainda escapavam dessa autoridade. `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e `identidade.estado.motivo_condicao` agora usam o mesmo `material-text`; os gates de resultado executado e motivo operacional chamam `_has_material_text` em vez de `.strip()`.

### Publicação não apaga o indeterminado

A fase `CANDIDATO_PRODUTO` ou posterior exige contrato explícito de publicação: campo final BOOLEAN e política aprovada para os casos `INDETERMINADO`.

Essa política também deixou de ter descrição normativa livre. `indeterminado_vira_false=false` é constante estrutural; `tratamento` é enum fechado e `OUTRA_APROVADA` exige `regra_ref` material. Não há texto livre no mesmo bloco capaz de ordenar comportamento oposto.

## Auditorias A1 e correções

### Primeira A1

A primeira auditoria independente concluiu `NAO_APTA` com cinco achados bloqueantes: rewind pós-`PUBLICADO`, provas auditáveis semanticamente vazias, gate prematuro para `PROPOSTO`, contradição textual de `INDETERMINADO` e calibração com referência órfã. Todos foram confirmados como procedentes e corrigidos. O relatório permanece em `03_resultado_a1.md`.

### Segunda A1

A reauditoria independente sobre `2783bcbd6ad7f07f9f3893c66c9dc36d0557f57e` também concluiu `NAO_APTA`, agora com três achados bloqueantes:

1. marcas Unicode `M*` ainda satisfaziam provas auditáveis;
2. `FALSE` × `INDETERMINADO` ainda dependia parcialmente de regex aplicada a prosa normativa;
3. semântica probabilística podia escapar por sinônimos não cobertos.

Os três foram confirmados como procedentes. A correção removeu a fragilidade de origem em vez de ampliar listas de regex. O relatório permanece em `04_resultado_a1_reauditoria.md`.

O workflow de construção `34912665666` executou a árvore corrigida sem os próprios mecanismos transitórios: **26 testes, OK**, e `validate_assistant.py` com **0 falhas / 0 avisos**. Só então publicou o commit permanente `f46b69790fc23ac6c3ebfa633053a3acb6f9ed1a`.

### Terceira A1

A terceira auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes: `$defs.material_ref` ainda impunha ASCII no schema, campos auditáveis de proveniência de topo escapavam da materialidade e alguns gates de conteúdo material podiam ser satisfeitos por strings visualmente vazias.

O resultado histórico permanece em `05_resultado_a1_reauditoria_2.md`. As três divergências foram corrigidas por uma autoridade Unicode única e testes positivos/negativos multilíngues. O run de construção `34955861169` removeu os mecanismos transitórios, executou suíte, CLI adversarial e `validate_assistant`, e só então publicou o commit permanente `4f686e5de163b649c4ee5e7643f75ecd56db47e7`.

### Quarta A1

A quarta auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com uma divergência bloqueante: a autoridade Unicode comum estava correta, mas seis campos normativos/materialmente decisivos equivalentes ainda aceitavam conteúdo não material por `minLength` ou `.strip()`.

O resultado histórico permanece em `06_resultado_a1_reauditoria_3.md`. A correção aplicou a mesma autoridade `material-text` aos seis campos, removeu `.strip()` dos dois gates materiais correspondentes e ampliou a suíte para **31 métodos**. O run `34960256357` validou a árvore sem seus mecanismos transitórios e só então publicou `8fd8e7892ead1bb63a554b5283f7062adf582976`.

### Quinta A1

A quinta auditoria independente sobre `0b7a712cd2c897483da34517f10516012711f153` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com `DIVERGE-01`: textos centrais ainda eram validados apenas por comprimento. O resultado permanece em `07_resultado_a1_reauditoria_4.md`.

O contraditório confirmou a divergência. A correção reutiliza `material-text` nos demais textos obrigatórios do contrato e acrescenta uma invariável estrutural para impedir novos `string + minLength` sem política explícita. `governanca.observacoes[]` permanece narrativa opcional. A suíte passou a **34 métodos**.

### Sexta A1

A sexta auditoria independente sobre `e0b6ed916386bef19006e7d41e183ffde25e360a` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com duas divergências bloqueantes. `DIVERGE-01` mostrou três regex genéricas `.*\S.*` ainda concorrendo com `material-text`; `DIVERGE-02` mostrou que o guard permanente aceitava qualquer `pattern` como política suficiente. O resultado histórico permanece em `08_resultado_a1_reauditoria_5.md`.

O contraditório confirmou ambos os achados. A correção remove as três regex textuais genéricas, exige `material-text` em todo `type=string + minLength` e congela os únicos patterns remanescentes por path e regex exata como contratos estruturais. Um adversarial sintético prova que `minLength + pattern: .*\S.*` sem `material-text` é violação. A suíte passa a **36 métodos**.

### Sétima A1

A sétima auditoria independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes. `DIVERGE-01` demonstrou bypass da equivalência `FALSE` × `INDETERMINADO` por caracteres Unicode default-ignorable inseridos dentro de palavras; `DIVERGE-02` mostrou que o guard de `string + minLength` não reconhecia `type` representado por array; `DIVERGE-03` demonstrou que `NaN` e `±Infinity` atravessavam limiares e pesos materiais. O resultado histórico permanece em `09_resultado_a1_reauditoria_6.md`.

O contraditório confirmou os três achados. A correção remove `Cf` e variation selectors antes da tokenização semântica, torna o guard sensível a arrays de tipos contendo `string`, registra `finite-number` no mesmo `FormatChecker` para limiares/pesos e recusa constantes JSON não finitas no loader. A suíte passa a **39 métodos**.

## Fronteiras preservadas

- Micromodelo continua artefato de domínio, não sétimo tipo do Hub.
- Nenhuma pasta nova é criada em `.assistant/skills/` nesta sprint.
- Não há coleta de metadata nem leitura de dados; isso começa na MM03.
- Não há fingerprint; pertence à MM02.
- `--previous` compara snapshots explicitamente fornecidos e não calcula hash/fingerprint.
- Não há contrato definitivo de MLflow; `tracking.politica=PENDENTE_MM06` preserva a fronteira.
- Não há regra institucional de publicação copiada para o Hub; a autoridade permanece `GOVERNANCA_EXTERNA`.
- Nenhum nome real de catálogo, schema, tabela, pessoa ou workspace corporativo entra nos fixtures.

## Evidência técnica atual

A suíte MM01 possui **39 métodos automatizados**, além de mutações e subtests. O reteste das correções da sétima A1 ficou verde, e os sete workflows permanentes executaram com sucesso antes da sincronização documental para a oitava A1.

Run IDs e o SHA final da árvore documental não são congelados neste arquivo para evitar que registrar a evidência altere a própria árvore validada. A descrição da PR #51 é o registro operacional do head e dos runs finais; `TESTES.md` mantém a cronologia histórica.

## Gate de saída

Como o contrato mudou materialmente depois da sétima A1, a MM01 só pode ser aceita após uma **oitava A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural, CLI e construir adversariais próprios sobre as três classes corrigidas.

O bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após uma oitava A1 limpa e contraditório final.

**MM02 permanece bloqueada até oitava A1, eventual contraditório, fechamento do changelog, aceite explícito e integração da MM01.**
