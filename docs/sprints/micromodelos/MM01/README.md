# MM01 — Contrato canônico de micromodelos

Status da sprint: **CANDIDATA EM VALIDAÇÃO; NÃO ACEITA; NÃO INTEGRADA**  
Base inicial: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`  
Base reconciliada após V10: `a9480391c78e2402986885db0ce08b10e0619a1a`  
Branch: `micromodelos/mm01-contrato-canonico`

## Objetivo

Transformar as decisões arquiteturais aceitas na MM00 em um contrato estrutural verificável para cada micromodelo. A MM01 define o conteúdo mínimo de `micromodelo.yaml`, a máquina de fases, as condições operacionais, a proveniência das afirmações materiais e os gates semânticos que impedem avançar um artefato incompleto.

A sprint não cria a skill `hub-ml-micromodelos`. O validador desta entrega vive em `tools/` como **oráculo de construção e CI** porque a lista de skills é fechada e a skill só nasce na MM04. Quando a MM04 criar o objeto roteável, ela deverá incorporar/derivar o contrato vigente sem criar uma segunda fonte de verdade.

A implementação começou sobre a `main` final da MM00. Durante a sprint, a frente do Sistema de Temas integrou a V10; por isso a candidata foi reconciliada de forma fail-closed com `main@a9480391c78e2402986885db0ce08b10e0619a1a` antes da abertura da PR. A reconciliação passou novamente pela suíte MM01 e pelo gate estrutural. Nenhum arquivo da V10 foi reimplementado ou alterado pela MM01.

## Entregas

- `micromodelo.schema.json`: schema formal Draft 2020-12, versão `1.0.0`;
- `micromodelo.template.yaml`: template inicial válido e sanitizado;
- `CONTRATO_MICROMODELO.md`: semântica de cada grupo e regras de preenchimento;
- `ESTADOS_E_PROVENIENCIA.md`: máquina de fases, condições e proveniência;
- `tools/micromodelo_mm01_contract.py`: validador de referência/CI;
- fixtures sintéticos positivos e negativos em `tools/tests/fixtures/micromodelos_mm01/`;
- `tools/tests/test_micromodelo_mm01.py`: suíte automatizada da sprint;
- `.github/workflows/micromodelos-mm01-ci.yml`: gate permanente, read-only, para branch/PR/`main`;
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

### `FALSE` não significa “não encontrei evidência”

O contrato exige três definições distintas: `quando_true`, `quando_false` e `quando_indeterminado`. A ausência de evidência só pode resultar em `INDETERMINADO` ou seguir uma regra explícita previamente aprovada. O contrato não oferece a opção silenciosa “ausência = FALSE”.

### Score 0–100 não é probabilidade por padrão

Score habilitado exige escala exatamente 0–100, semântica e normalização explícitas. `PROBABILIDADE_CALIBRADA` só é aceita com bloco de calibração cuja proveniência seja `MEDIDO` e tenha referência de execução.

### Decisões materiais exigem aprovação humana

Limiares e pesos não podem permanecer `PROPOSTO` ou `INFERIDO` e ainda assim avançar como decisão válida. A partir de `EM_VALIDACAO`, as semânticas de classificação, ausência de evidência, score habilitado e regras de evidência/contra-evidência precisam estar aprovadas.

### Publicação não apaga o indeterminado

A fase `CANDIDATO_PRODUTO` ou posterior exige contrato explícito de publicação: campo final BOOLEAN e política aprovada para os casos `INDETERMINADO`. O contrato não admite mapeamento implícito de indeterminado para `FALSE`.

## Fronteiras preservadas

- Micromodelo continua artefato de domínio, não sétimo tipo do Hub.
- Nenhuma pasta nova é criada em `.assistant/skills/` nesta sprint.
- Não há coleta de metadata nem leitura de dados; isso começa na MM03.
- Não há fingerprint; pertence à MM02.
- Não há contrato definitivo de MLflow; `tracking.politica=PENDENTE_MM06` preserva a fronteira.
- Não há regra institucional de publicação copiada para o Hub; a autoridade permanece `GOVERNANCA_EXTERNA`.
- Nenhum nome real de catálogo, schema, tabela, pessoa ou workspace corporativo entra nos fixtures.

## Gate de saída

A MM01 só pode ser aceita quando o schema formal for válido, o template e o fixture positivo passarem, todos os fixtures negativos forem rejeitados pelo motivo esperado, o gate permanente MM01, `tools/validate_assistant.py` e a suíte agregada continuarem verdes e uma auditoria A1 independente reproduzir os gates sem depender desta documentação de autoria.

A MM02 permanece bloqueada até aceite e integração da MM01.
