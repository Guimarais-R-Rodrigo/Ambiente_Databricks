# MM01 — Contrato canônico de micromodelos

Status da sprint: **CORRIGIDA APÓS A1; RETESTE TÉCNICO VERDE; REAUDITORIA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**  
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
- `tools/tests/test_micromodelo_mm01.py`: suíte automatizada com 24 métodos e múltiplos subtests;
- `.github/workflows/micromodelos-mm01-ci.yml`: gate permanente, read-only, para branch/PR/`main`;
- pacote de auditoria A1 em `docs/auditoria/2026-09-14_micromodelos-mm01/`;
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

`BLOQUEADO`, `SUSPENSO` e `DEPRECATED` são condições ortogonais, não saltos da máquina de fases. Isso evita a ambiguidade de “de qual fase um BLOQUEADO deve voltar?”.

`fase_anterior` torna o par declarado localmente verificável, mas não é tratada como prova autorreferente de histórico. Quando um snapshot anterior confiável existe, a CLI aceita `--previous` e valida a transição contra a fase efetivamente observada nele. Uma versão já `PUBLICADO` não pode ser silenciosamente reescrita para fase anterior mantendo a mesma `micromodel_version`.

### `FALSE` não significa “não encontrei evidência”

O contrato exige três definições distintas: `quando_true`, `quando_false` e `quando_indeterminado`. A comparação também normaliza diferenças editoriais simples; não é possível contornar o gate copiando a mesma definição com caixa, acento ou pontuação diferente.

A ausência de evidência só pode resultar em `INDETERMINADO` ou seguir uma regra explícita previamente aprovada. O contrato não oferece a opção silenciosa “ausência = FALSE”.

### Score 0–100 não é probabilidade por padrão

Score habilitado exige escala exatamente 0–100, semântica e normalização explícitas. `PROBABILIDADE_CALIBRADA` só é aceita com bloco de calibração cuja proveniência seja `MEDIDO` e tenha referência de execução.

`score.calibracao.evidencia_ref` precisa resolver para um experimento declarado, `EXECUTADO` e `MEDIDO`. O validador também recusa linguagem de “probabilidade” ou “chance” em score que não esteja declarado e comprovado como `PROBABILIDADE_CALIBRADA`.

### Decisões materiais são progressivas, mas não atravessam gate sem aprovação

Limiar ou peso pode permanecer `PROPOSTO` em descoberta/estudo, preservando a alimentação progressiva da fonte canônica. A partir de `EM_VALIDACAO`, limiares e pesos existentes precisam estar `APROVADO`.

Na mesma fase, fontes, evidências, contra-evidências e critérios de validação precisam estar presentes; semânticas, política de ausência, score habilitado e regras de evidência/contra-evidência precisam estar aprovados.

### Provas auditáveis precisam conter informação material

`APROVADO`, `MEDIDO`, handoff e confirmação de Produto de Dados não são satisfeitos por uma string apenas formalmente presente. Whitespace e caracteres invisíveis não contam como identidade, referência ou execução auditável. Quando o JSON Schema consegue rejeitar o valor formalmente, o erro pode surgir como `SCHEMA`; os guardrails semânticos cobrem os casos que exigem normalização adicional.

### Parsing e referências são fail-closed

YAML/JSON com chaves duplicadas são recusados, em vez de aceitar implicitamente o último valor. IDs duplicados são barrados nas coleções controladas, evidências não podem apontar para fonte inexistente e calibração não pode apontar para experimento órfão ou não medido.

`catalogo_ref` permanece restrito a `CATALOGO_PRODUTO`. A CLI não possui argumento que permita ampliar esse conjunto sem mudança explícita do contrato.

### Publicação não apaga o indeterminado

A fase `CANDIDATO_PRODUTO` ou posterior exige contrato explícito de publicação: campo final BOOLEAN e política aprovada para os casos `INDETERMINADO`.

A política possui `indeterminado_vira_false=false` como regra estruturada. O validador também rejeita descrição que contradiga essa regra, impedindo que dois consumidores válidos obtenham comportamentos opostos do mesmo contrato.

O estado da interface de publicação também deve acompanhar a fase. A suíte cobre caminhos positivos `CANDIDATO_PRODUTO`, `EM_VALIDACAO_GOVERNANCA` e `PUBLICADO` para demonstrar que os gates são satisfazíveis.

## Primeira A1 e correções

A primeira auditoria A1 independente concluiu `NAO_APTA` e registrou cinco achados bloqueantes. O contraditório confirmou os cinco como procedentes:

1. rewind pós-`PUBLICADO` não era comprovável contra snapshot anterior confiável;
2. provas auditáveis aceitavam valores semanticamente vazios;
3. limiares/pesos `PROPOSTO` eram bloqueados cedo demais;
4. a política de `INDETERMINADO` podia contradizer seu próprio tratamento;
5. `score.calibracao.evidencia_ref` podia ficar órfão.

Todos foram corrigidos sem expandir o escopo da sprint. O reteste transitório final `34909835696` executou 24 métodos de teste com `OK`, executou `validate_assistant.py --root ambiente_fonte` com zero falhas/avisos e só então publicou os artefatos permanentes corrigidos. O resultado original da primeira A1 permanece histórico e não foi reclassificado.

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

A suíte MM01 possui **24 métodos automatizados**, além de mutações e subtests. O reteste das correções A1 ficou verde antes da publicação do commit permanente. Os workflows permanentes do HEAD documental final e o CI agregado ainda precisam ser observados antes da reauditoria.

Run IDs e o SHA final da árvore não são congelados neste arquivo para evitar que registrar a evidência altere a própria árvore que acabou de ser validada. A descrição da PR #51 é o registro operacional do head e dos runs finais; `TESTES.md` mantém a cronologia relevante da sprint.

## Gate de saída

A MM01 só pode ser aceita quando o schema formal for válido, o template e fixtures positivos passarem, os casos negativos/adversariais forem rejeitados, o gate permanente MM01, `tools/validate_assistant.py` e a suíte agregada continuarem verdes e uma **reauditoria A1 independente** reproduzir os gates e confirmar as correções sem depender desta documentação de autoria.

**A primeira A1 foi `NAO_APTA`; a reauditoria da árvore corrigida está pendente. A MM02 permanece bloqueada até reauditoria, eventual novo contraditório, aceite e integração da MM01.**
