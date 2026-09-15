# MM01 — Contrato canônico de micromodelos

Status da sprint: **AUDITORIA FINAL FECHADA `NAO_APTA_PARA_FECHAMENTO_DOCUMENTAL` PRESERVADA; B01/B02 CORRIGIDOS; 47 TESTES DA MATRIZ + 1 REGRESSÃO R03 VERDES; REAUDITORIA FINAL INDEPENDENTE PENDENTE; NÃO ACEITA; NÃO INTEGRADA**
Base inicial: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`  
Branch: `micromodelos/mm01-contrato-canonico`  
PR: `#51`

## Objetivo

Transformar as decisões arquiteturais aceitas na MM00 em um contrato estrutural verificável para cada micromodelo. A MM01 define o conteúdo mínimo de `micromodelo.yaml`, a máquina de fases, as condições operacionais, a proveniência das afirmações materiais e os gates semânticos que impedem avançar um artefato incompleto.

A sprint não cria a skill `hub-ml-micromodelos`. O validador desta entrega vive em `tools/` como **oráculo de construção e CI** porque a lista de skills é fechada e a skill só nasce na MM04. Quando a MM04 criar o objeto roteável, ela deverá incorporar/derivar o contrato vigente sem criar uma segunda fonte de verdade.

A implementação começou sobre a `main` final da MM00 e foi reconciliada de forma fail-closed com as evoluções posteriores do Sistema de Temas. Nenhum arquivo funcional dessas sprints foi reimplementado pela MM01; as evoluções foram absorvidas apenas como base vigente do repositório.

## Entregas

- `micromodelo.schema.json`: schema formal Draft 2020-12, versão `1.0.0`;
- `micromodelo.template.yaml`: template inicial válido e sanitizado;
- `CONTRATO_MICROMODELO.md`: semântica de cada grupo e regras de preenchimento;
- `ESTADOS_E_PROVENIENCIA.md`: máquina de fases, condições, proveniência e gates;
- `tools/micromodelo_mm01_contract.py`: validador de referência/CI;
- fixtures sintéticos positivos e negativos em `tools/tests/fixtures/micromodelos_mm01/`;
- `tools/tests/test_micromodelo_mm01.py`: suíte canônica automatizada com **47 métodos** e múltiplos subtests;
- `tools/tests/test_micromodelo_mm01_r03.py`: regressão permanente dedicada ao requisito R03 para recusar `np.float64` e demais tipos numéricos externos ao domínio canônico;
- `.github/workflows/micromodelos-mm01-ci.yml`: gate permanente, read-only, para branch/PR/`main`;
- pacote de auditoria com contexto, prompt, oito resultados A1 exploratórios preservados e a auditoria final fechada preservada separadamente, além da `MATRIZ_ACEITE_FINAL.md` congelada após o contraditório da oitava A1;
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

`fase_anterior` torna o par declarado localmente verificável, mas não é tratada como prova autorreferente de histórico. Sem `--previous`, a CLI certifica apenas a consistência interna do snapshot e declara explicitamente `HISTORICO_NAO_CERTIFICADO`. Quando um snapshot anterior confiável é fornecido por `--previous`, a validação passa a certificar evolução histórica: confere identidade/versão, valida a transição observada e impede rewind de uma versão já `PUBLICADO`. Esse modo não descobre histórico por conta própria nem antecipa fingerprint/MM02.

### `FALSE` não significa “não encontrei evidência”

O contrato exige três definições distintas: `quando_true`, `quando_false` e `quando_indeterminado`. A comparação é deliberadamente **editorial, não semântica**: aplica NFKC/casefold, remove `Default_Ignorable_Code_Point`, normaliza whitespace e tolera apenas pontuação editorial prevista. Diacríticos, operadores e pontuação interna potencialmente semânticos são preservados; a MM01 não tenta resolver equivalência geral de linguagem natural.

Após a segunda A1, a política de ausência de evidência deixou de depender de prosa normativa. O comportamento é declarado por `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência. `tratamento=INDETERMINADO` exige resultado `INDETERMINADO`; uma conversão explícita para outro resultado só pode existir como `REGRA_EXPLICITA_APROVADA` com referência auditável.

### Score 0–100 não é probabilidade por padrão

`score.tipo_semantica` é a única autoridade executável sobre a natureza do score. `FORCA_EVIDENCIA`, `PROBABILIDADE_CALIBRADA` e `OUTRA_APROVADA` são estados estruturados; o campo livre `score.semantica` deixou de fazer parte do schema.

Assim, textos como “percentual estimado”, “risco percentual”, “likelihood”, “chance” ou “probabilidade” não podem redefinir silenciosamente um score não probabilístico. Se o score for probabilístico, o contrato exige `PROBABILIDADE_CALIBRADA`, calibração `MEDIDO` e `evidencia_ref` resolvida para experimento existente, `EXECUTADO` e `MEDIDO`.

A normalização também é estruturada (`PENDENTE`, `SOMA_PONDERADA_0_100`, `MIN_MAX_0_100`, `LINEAR_0_100` ou `CUSTOM_APROVADO`) e carrega proveniência. Em `EM_VALIDACAO+`, ela precisa estar definida e aprovada.

### Decisões materiais são progressivas, mas não atravessam gate sem aprovação

Limiar ou peso pode permanecer `PROPOSTO` em descoberta/estudo, preservando a alimentação progressiva da fonte canônica. A partir de `EM_VALIDACAO`, limiares e pesos existentes precisam estar `APROVADO`.

Na mesma fase, fontes, evidências, contra-evidências e critérios de validação precisam estar presentes; semânticas, políticas e regras materiais precisam satisfazer seus contratos estruturados.

### Provas auditáveis precisam conter informação material

A segunda A1 demonstrou que uma blacklist de whitespace/controles não era suficiente para caracteres Unicode `M*`. A terceira A1 mostrou que schema e validador ainda podiam divergir e que campos materiais equivalentes não compartilhavam a mesma autoridade. A regra atual é positiva e única: após NFKC, caracteres com a propriedade Unicode `Default_Ignorable_Code_Point` são removidos e o conteúdo restante precisa conter ao menos uma letra ou número Unicode.

O JSON Schema usa `format: material-text` e o `FormatChecker` do validador delega esse formato à mesma função `_has_material_text`. Isso rejeita strings compostas somente por espaços, zero-width, variation selectors, combining marks isolados, pontuação ou símbolos nos campos materiais, sem rejeitar CJK, Devanagari, caracteres acentuados, algarismos Unicode ou combining marks acompanhados de texto material. Campos puramente narrativos não foram restringidos indiscriminadamente.

A quarta A1 identificou seis campos normativos equivalentes que ainda escapavam dessa autoridade. `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e `identidade.estado.motivo_condicao` agora usam o mesmo `material-text`; os gates de resultado executado e motivo operacional chamam `_has_material_text` em vez de `.strip()`.

### O domínio numérico canônico é estrito

R03 distingue o domínio canônico de entradas Python de tipos externos. Inteiros Python arbitrariamente grandes são aceitos sem coerção para `float`; `float` Python precisa ser finito. `Decimal`, escalares NumPy e outros tipos externos não recebem suporte positivo nem conversão implícita: quando chegam diretamente à API Python, são recusados deterministicamente.

Após a auditoria final fechada, `_check_finite_number_format` passou de `isinstance` para identidade estrita de tipo. Isso impede que `np.float64`, que pode satisfazer `isinstance(value, float)`, atravesse o ramo reservado ao `float` Python. A regressão dedicada cobre limiar e peso.

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

### Oitava A1, contraditório e matriz final

A oitava A1 independente sobre `fe3a9d8b39c0016d9b487036f1d5e3ad38cb2630` concluiu `NAO_APTA` e permanece historicamente preservada em `10_resultado_a1_reauditoria_7.md`. O relatório trouxe seis `QUEBRA`, dois `DIVERGE` bloqueantes e uma melhoria. O contraditório confirmou defeitos materiais, mas também demonstrou que a auditoria exploratória vinha ampliando o threat model a cada rodada.

Para encerrar o ciclo de expansão aberta, `MATRIZ_ACEITE_FINAL.md` congela os requisitos R01–R08, as entradas suportadas, o perfil de autoria do schema e os não requisitos. A candidata foi corrigida contra essa matriz: materialidade passa a usar `Default_Ignorable_Code_Point`; a comparação passa a ser editorial conservadora; o domínio numérico canônico é determinístico; decisão humana e proveniência têm invariantes intrínsecos; resultado observado só existe após `EXECUTADO`; snapshot e evolução histórica têm níveis de garantia distintos; e o schema oficial permanece dentro do perfil de composição revisado. A suíte canônica passa a **47 métodos**.

### Auditoria final fechada — `NAO_APTA_PARA_FECHAMENTO_DOCUMENTAL`

A auditoria final fechada examinou o HEAD `337055d70a28c6d595594fa1e8c351a47615e66b` contra a matriz congelada e permanece preservada em `11_resultado_a1_reauditoria_8.md`, sem reclassificação retroativa.

Ela encontrou dois bloqueios:

1. **R03 / `MATRIX_VIOLATION`:** `np.float64(1.5)` era aceito na API direta porque `_check_finite_number_format` usava `isinstance(value, float)`;
2. **gate final / `FINAL_GATE_VIOLATION`:** a candidata estava `behind_by=4` contra a `main` vigente no momento do julgamento.

O contraditório corretivo foi objetivo: a implementação passou a definir positivamente o domínio canônico por identidade estrita de tipo, ganhou regressão permanente para `np.float64` e foi reconciliada por merge real com a `main` vigente. O caso editorial `"?true" × "true"` permanece apenas como `BACKLOG_HARDENING`; não foi convertido em requisito novo.

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

A suíte canônica MM01 permanece com **47 métodos automatizados**, além de mutações e subtests. O workflow permanente executa adicionalmente **1 regressão R03 dedicada** em `tools/tests/test_micromodelo_mm01_r03.py`, totalizando a prova operacional como **47 + 1**, sem reclassificar a identidade da suíte congelada.

A correção B01, a reconciliação B02 e a primeira sincronização documental foram certificadas com sucesso em runner real. Esta atualização documental altera novamente o HEAD; portanto, a árvore resultante precisa ser recertificada integralmente antes de ser congelada para a reauditoria final independente. Run IDs e o SHA definitivo permanecem na conversação da PR para evitar commits autorreferentes.

## Gate de saída

A MM01 mantém a condição objetiva de término em `MATRIZ_ACEITE_FINAL.md`. O próximo gate é uma **reauditoria final independente** sobre o novo HEAD congelado, usando a mesma matriz e sem reabrir implicitamente o threat model. Ela deve reproduzir instalação, 47 testes da suíte canônica, a regressão R03, CLI, gate estrutural e adversariais próprios; um achado só pode bloquear se demonstrar violação de requisito já assumido pela matriz ou ADR aceito.

O bloco MM01 do `CHANGELOG.md` permanece dívida bloqueante de merge e só deve ser sincronizado, de forma byte-preserving fora do bloco MM01, após reauditoria final limpa e contraditório final.

**MM02 permanece bloqueada até reauditoria final, contraditório final, fechamento do changelog, aceite explícito e integração da MM01.**
