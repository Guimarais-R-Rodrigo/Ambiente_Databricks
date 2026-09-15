# MM01 — Contrato canônico de micromodelos

Status da sprint: **CORRIGIDA APÓS SEGUNDA A1; RETESTE DE CONSTRUÇÃO VERDE; TERCEIRA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**  
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
- `tools/tests/test_micromodelo_mm01.py`: suíte automatizada com **26 métodos** e múltiplos subtests;
- `.github/workflows/micromodelos-mm01-ci.yml`: gate permanente, read-only, para branch/PR/`main`;
- pacote de auditoria A1 com contexto, prompt e os dois resultados históricos `NAO_APTA`;
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

A segunda A1 demonstrou que uma blacklist de whitespace/controles não era suficiente para caracteres Unicode `M*`. A regra atual é positiva: após NFKC, uma referência auditável precisa conter ao menos uma letra ou número Unicode.

Isso rejeita strings compostas somente por espaços, zero-width, variation selectors, COMBINING GRAPHEME JOINER ou outros combining marks isolados em aprovação, medição, handoff e referência de Produto de Dados.

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

A suíte MM01 possui **26 métodos automatizados**, além de mutações e subtests. O reteste de construção das correções da segunda A1 ficou verde antes da publicação do commit permanente.

Run IDs e o SHA final da árvore documental não são congelados neste arquivo para evitar que registrar a evidência altere a própria árvore validada. A descrição da PR #51 é o registro operacional do head e dos runs finais; `TESTES.md` mantém a cronologia histórica.

## Gate de saída

Como o contrato mudou materialmente depois da segunda A1, a MM01 só pode ser aceita após uma **terceira A1 independente** sobre o novo HEAD congelado. O auditor deve reproduzir instalação, suíte, gate estrutural e CLI e criar adversariais próprios sem usar os relatórios anteriores como prova.

O bloco MM01 do `CHANGELOG.md` também precisa ser sincronizado antes do merge por operação preservadora do histórico e a árvore resultante deve ser novamente validada.

**MM02 permanece bloqueada até terceira A1, eventual contraditório, fechamento documental, aceite explícito e integração da MM01.**
