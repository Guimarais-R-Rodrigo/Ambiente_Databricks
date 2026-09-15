# MM01 — Checkpoint

Status: **SÉTIMA A1 `APTA_COM_CORRECOES`; `DIVERGE-01`, `DIVERGE-02` E `DIVERGE-03` BLOQUEANTES CONFIRMADAS E CORRIGIDAS; RETESTE DE CONSTRUÇÃO VERDE; 7 WORKFLOWS PERMANENTES VERDES; OITAVA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**

## Base e superfície

- `main` inicial da iniciativa MM01: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`;
- a candidata foi reconciliada sucessivamente com as bases pós-V10, pós-V11 e com `main@28669f99db27cf23df73549297bbf57eda033f58` após a integração do plano mestre SEF;
- base vigente na segunda A1: `d106ef3158e5827a2eec3aa183dbb3b47885c960`;
- branch: `micromodelos/mm01-contrato-canonico`;
- PR: `#51`;
- MM00: encerrada e integrada;
- MM02: bloqueada até nova A1, aceite explícito e merge desta sprint.

## O que a candidata entrega

1. schema formal `1.0.0` para `micromodelo.yaml`;
2. template YAML inicial válido e sanitizado;
3. máquina de fases com rework explícito e `PUBLICADO` terminal por versão;
4. comparação opcional com especificação anterior confiável (`--previous`) para verificar transição real, impedir rewind pós-`PUBLICADO` na mesma versão e recusar regressão de versão, sem antecipar fingerprint/MM02;
5. condições operacionais ortogonais (`ATIVO`, `BLOQUEADO`, `SUSPENSO`, `DEPRECATED`);
6. proveniência `DESCOBERTO`, `INFERIDO`, `PROPOSTO`, `APROVADO`, `MEDIDO` com gates próprios;
7. regra positiva de materialidade textual: referências auditáveis precisam conter letra/número Unicode após NFKC; whitespace, controles, zero-width, variation selectors e marcas combinantes isoladas não contam;
8. proteção explícita de `FALSE` versus `INDETERMINADO`, inclusive contra equivalência apenas cosmeticamente diferente;
9. política de ausência de evidência totalmente estruturada por `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência, sem prosa normativa livre;
10. política de publicação de `INDETERMINADO` totalmente estruturada, com `indeterminado_vira_false=false` e `regra_ref` somente para `OUTRA_APROVADA`;
11. score 0–100 cuja natureza é determinada exclusivamente por `tipo_semantica`; campo livre `score.semantica` não faz parte do schema;
12. normalização de score estruturada por método/referência/proveniência, sem frase livre normativa;
13. calibração probabilística somente para `PROBABILIDADE_CALIBRADA`, com integridade referencial contra experimento existente, executado e medido;
14. limiares e pesos podem permanecer `PROPOSTO` nas fases pré-gate e passam a exigir `APROVADO` a partir de `EM_VALIDACAO`;
15. gates humanos para validação e demais decisões materiais;
16. escopo de fontes fail-closed em `CATALOGO_PRODUTO`, sem override de CLI;
17. recusa de chaves duplicadas em YAML/JSON e de IDs duplicados em coleções controladas;
18. conteúdo material mínimo obrigatório ao entrar em `EM_VALIDACAO`;
19. coerência entre fase e status da interface de publicação, com caminhos positivos testados até `PUBLICADO`;
20. fronteira de tracking preservada para MM06;
21. validador de referência/CI, fixtures sintéticos e suíte com **39 métodos de teste**;
22. gate permanente `.github/workflows/micromodelos-mm01-ci.yml`, read-only e sem acesso a ambiente corporativo;
23. pacote neutro de auditoria com os resultados históricos das sete A1 preservados, sem reclassificação retroativa.

## O que não foi feito

- não foi criada `hub-ml-micromodelos`;
- não foi alterada a lista de skills roteáveis;
- não foi criado sétimo tipo em `hub_padroes`;
- não foi criado fingerprint nem qualquer hash material da especificação;
- não houve descoberta de metadata;
- não houve leitura de dados;
- não houve alteração de `mlflow_run`;
- não houve integração visual específica da MM01; V11 foi absorvida apenas como base do repositório;
- não houve handoff/publicação real;
- não houve migração de legado.

## Primeira auditoria A1

A primeira A1 independente auditou o head pré-correção e concluiu `NAO_APTA`. Cinco achados bloqueantes foram confirmados como procedentes: proteção histórica contra rewind, referências semanticamente vazias, gate prematuro para `PROPOSTO`, contradição de `INDETERMINADO` por prosa e calibração com referência órfã. O relatório permanece em `03_resultado_a1.md`.

As cinco correções foram implementadas, a suíte passou a 24 métodos e o reteste de construção `34909835696` ficou verde.

## Segunda auditoria A1

A reauditoria independente sobre `2783bcbd6ad7f07f9f3893c66c9dc36d0557f57e` também concluiu `NAO_APTA`. Três novos achados bloqueantes foram confirmados como procedentes:

1. referências compostas exclusivamente por marcas Unicode `M*` ainda satisfaziam materialidade;
2. `FALSE` × `INDETERMINADO` ainda dependia parcialmente de interpretação de prosa livre por regex;
3. semântica probabilística ainda podia ser escondida por sinônimos não cobertos pela regex.

O resultado está preservado em `04_resultado_a1_reauditoria.md` e não foi reclassificado.

## Correções da segunda A1

As três correções foram estruturais, sem ampliar escopo:

- `_has_material_text` passou a exigir positivamente letra/número Unicode após NFKC;
- campos de descrição normativa foram removidos das políticas de ausência e publicação; comportamento executável ficou fechado em campos estruturados;
- `score.tipo_semantica` passou a ser a única autoridade executável sobre natureza probabilística; `score.semantica` livre foi removido e `score.normalizacao` virou contrato estruturado.

O workflow transitório `34912665666` preparou a árvore sem os próprios mecanismos temporários e então executou:

- `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`: **26 métodos, OK**;
- `python -B tools/validate_assistant.py --root ambiente_fonte`: **APROVADO, 0 falhas, 0 avisos**;
- commit permanente das correções: `f46b69790fc23ac6c3ebfa633053a3acb6f9ed1a`.

Esse run comprova a construção da correção, mas não substitui os workflows permanentes do próximo HEAD documental congelado.

## Terceira auditoria A1

A terceira A1 independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes: autoridade ASCII conflitante em `$defs.material_ref`, campos de proveniência de topo fora da política material e gates de conteúdo material aceitando strings visualmente vazias. O resultado histórico foi preservado em `05_resultado_a1_reauditoria_2.md`.

## Correções da terceira A1

A política de materialidade foi unificada sem ampliar o escopo da MM01:

- `_has_material_text` continua a autoridade Unicode: NFKC seguido da exigência de pelo menos uma categoria Unicode `L*` ou `N*`;
- o JSON Schema usa `format: material-text`, registrado no `FormatChecker` do próprio validador e delegado à mesma função;
- referências, proveniência material, semânticas obrigatórias, critérios, nomes de fontes e campos operacionais relevantes usam essa autoridade;
- prosa narrativa livre não recebeu a restrição indiscriminadamente;
- CJK, árabe/algarismos Unicode, Devanagari, caracteres acentuados e combining marks acompanhados de base material permanecem válidos.

O run transitório `34955861169` executou a suíte ampliada, CLI positiva/negativa/`--previous` e `validate_assistant` antes de publicar `4f686e5de163b649c4ee5e7643f75ecd56db47e7`. O mecanismo transitório não permaneceu na árvore candidata.

A sincronização documental posterior também foi validada antes da publicação: o run `34956548413` confirmou **29 métodos**, suíte MM01, CLI direta com casos Unicode positivo/negativo e `--previous`, `validate_assistant`, métrica congelada do README e invariantes dos relatórios A1 anteriores. Ele publicou `431e22cf25164dee8f8c1a5a1fc1da2943704b7a` já sem os mecanismos transitórios. Os workflows associados a esse commit automático ficaram em `action_required` e, por isso, não são tratados como evidência de CI permanente; a certificação deve ocorrer no HEAD normal subsequente.

## Quarta auditoria A1

A quarta A1 independente sobre `c0b6f5872f47f8e37ed8f55f262c276b8c105063` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com uma divergência bloqueante: seis campos normativos equivalentes ainda aceitavam conteúdo não material por `minLength` ou `.strip()`. O resultado está preservado em `06_resultado_a1_reauditoria_3.md`.

## Correções da quarta A1

A correção não criou nova heurística: `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e `identidade.estado.motivo_condicao` passaram a usar a autoridade já existente `material-text`. Os gates semânticos de resultado executado e motivo operacional também passaram a chamar `_has_material_text` em vez de `.strip()`.

A suíte passou para **31 métodos**, incluindo negativos de `Mn/Mc/Me`, `Cf`, zero-width, whitespace Unicode, pontuação, símbolos e combinações, e positivos multilíngues. O run transitório `34960256357` executou suíte, CLI positiva/negativa/`--previous`, `validate_assistant`, conferência do README e invariantes históricos antes de publicar `8fd8e7892ead1bb63a554b5283f7062adf582976`; os mecanismos transitórios foram removidos.

## Quinta auditoria A1

A quinta A1 independente sobre `0b7a712cd2c897483da34517f10516012711f153` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`. O único achado, `DIVERGE-01`, foi confirmado no contraditório: textos centrais de identidade, negócio, entidade, calibração e outros campos equivalentes ainda podiam ser materialmente vazios. O relatório histórico foi preservado em `07_resultado_a1_reauditoria_4.md`.

## Correções da quinta A1

A correção mantém `_has_material_text` como autoridade única e amplia `format: material-text` aos textos obrigatórios que participam do contrato. Um teste estrutural protege a classificação futura; `governanca.observacoes[]` é a exceção narrativa opcional explícita. A suíte passa a **34 métodos**.

## Sexta auditoria A1

A sexta A1 independente sobre `e0b6ed916386bef19006e7d41e183ffde25e360a` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`. Dois desvios bloqueantes foram confirmados: três `pattern: ".*\\S.*"` ainda competiam com `material-text`, e o guard de `string + minLength` considerava qualquer `pattern` suficiente. O relatório foi preservado em `08_resultado_a1_reauditoria_5.md`.

## Correções da sexta A1

A correção remove as três regex textuais genéricas e deixa `_has_material_text` → `format: material-text` como única autoridade de conteúdo material. Os únicos patterns remanescentes são contratos de estrutura (`$defs.id`, `identidade.nome` e `micromodel_version`) e ficam congelados por path + regex exata em regressão permanente. Todo `type=string + minLength` passa a exigir `material-text`; um nó sintético `minLength + pattern: .*\\S.*` sem format deve ser detectado como violação. A suíte passa a **36 métodos**.

## Sétima auditoria A1

A sétima A1 independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências bloqueantes: equivalência semântica burlável por Unicode default-ignorable, guard incompleto para `type` em array e números não finitos em limiares/pesos. O resultado foi preservado em `09_resultado_a1_reauditoria_6.md`.

## Correções da sétima A1

A normalização semântica remove `Cf` e variation selectors antes da tokenização; o guard de `string + minLength` reconhece tanto `type="string"` quanto listas contendo `string`; e `finite-number` recusa NaN/±Infinity nos valores materiais, enquanto o loader JSON recusa constantes não padrão. A suíte passa a **39 métodos**.

## Dívida documental antes do merge

O bloco MM01 do `CHANGELOG.md` ainda descreve a candidata pré-A1. Ele deve ser sincronizado **antes do merge**, por operação que preserve byte a byte o histórico anterior. Essa pendência não deve ser usada para apagar ou reclassificar as auditorias históricas.
    
## Gate independente pendente

Como a candidata mudou materialmente após a sétima A1, é obrigatória uma **oitava A1 independente** sobre o novo HEAD congelado.

## Gates restantes

1. executar oitava A1 em sessão independente;
2. confrontar qualquer novo achado com a árvore;
3. se a oitava A1 for limpa, executar contraditório final;
4. sincronizar o bloco MM01 do `CHANGELOG.md` preservando byte-for-byte o restante do arquivo;
5. revalidar a árvore exata e reconfirmar `main`, `behind_by` e mergeabilidade;
6. obter aceite explícito;
7. só então integrar a PR #51.

Enquanto qualquer item estiver pendente, **MM02 permanece bloqueada**.
