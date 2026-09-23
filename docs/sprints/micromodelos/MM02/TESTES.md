# MM02 — testes e certificação

## Objetivo

Provar duas propriedades simultaneamente:

1. alterações puramente editoriais ou de ciclo de vida **preservam** o `spec_fingerprint`;
2. alterações analiticamente materiais **mudam** o `spec_fingerprint`.

Os testes são sintéticos e repo-side.

## Suíte permanente MM02

Arquivo:

`tools/tests/test_micromodelo_mm02_fingerprint.py`

### Metamorfismos que devem preservar

- ordem das chaves do mapping;
- ordem serial de `fontes[].campos`;
- ordem serial de componentes do score;
- case/whitespace/pontuação terminal em texto normativo sob a equivalência MM01;
- duplicação editorial equivalente em listas de uso/não uso;
- `micromodel_version`;
- título;
- `negocio.objetivo`;
- referências de aprovação/proveniência;
- `score.semantica_ref` quando `tipo_semantica` já é estruturado;
- `score.normalizacao.referencia` quando o método já é estruturado;
- timestamps;
- resultado/referência de execução de experimento;
- descrições auxiliares;
- `70` versus `70.0`;
- mudança do estado institucional `CANDIDATA ↔ REJEITADA` mantendo o mesmo contrato material.

### Metamorfismos que devem mudar

- objeto/fonte;
- referência temporal/grão de entidade;
- regra de evidência;
- threshold;
- missing policy;
- semântica TRUE/FALSE/INDETERMINADO;
- peso;
- significado do score;
- referência de semântica quando `OUTRA_APROVADA`;
- referência de normalização quando `CUSTOM_APROVADO`;
- `score.calibracao.evidencia_ref` quando muda a calibração escolhida;
- contrato de saída de estudo;
- contrato de saída de publicação.

### Fail-closed

Uma especificação que falha no contrato MM01 não recebe fingerprint.

Exemplo permanente: `catalogo_ref` fora da allowlist MM01 deve produzir `InvalidSpecificationError`.

## Comandos de desenvolvimento/smoke

Executar em checkout real da branch:

```bash
python -B -m unittest tools/tests/test_micromodelo_mm02_fingerprint.py -v
python -B -m unittest tools/tests/test_micromodelo_mm01.py -v
python -B -m unittest tools/tests/test_micromodelo_mm01_r02.py -v
python -B -m unittest tools/tests/test_micromodelo_mm01_r03.py -v
python -B tools/micromodelo_mm02_fingerprint.py \
  tools/tests/fixtures/micromodelos_mm01/valido_validado.json \
  --schema docs/sprints/micromodelos/MM01/micromodelo.schema.json \
  --show-canonical
```

Depois:

```bash
python -B tools/validate_assistant.py --root ambiente_fonte
python -B tools/validate_assistant.py --conferir-readme
```

A composição de CI local/FULL proporcional será definida somente depois do smoke barato, conforme `PROTOCOLO_CERTIFICACAO_SPRINTS.md`.

## Critérios de falha

É blocker da MM02 se ocorrer qualquer um:

- fingerprint muda por alteração somente de aprovação/run/timestamp/fase;
- fingerprint não muda ao trocar fonte, regra, peso, threshold, missing, semântica ou saída;
- algoritmo aceita especificação MM01 inválida;
- serialização depende da ordem das chaves;
- número semanticamente equivalente `70` / `70.0` gera hashes distintos;
- normalização editorial apaga diferença potencialmente semântica não autorizada pela MM01, inclusive pontuação inicial;
- referência puramente auditável gera churn de fingerprint;
- referência que define regra customizada/calibração deixa de alterar o fingerprint;
- implementação duplica ou diverge da autoridade MM01 para equivalência editorial;
- algoritmo tenta consultar Databricks, MLflow, catálogo ou dado real.

## Canais

```text
REPO_SIDE_REVIEW = EM_ANDAMENTO
LOCAL_MM02 = NOT_RUN
MM01_REGRESSION = NOT_RUN
VALIDATE_ASSISTANT = NOT_RUN
CI_LOCAL = NOT_RUN
FULL_CERTIFICATION = NOT_RUN
GITHUB_ACTIONS = DEFERRED_NO_CREDITS
DATABRICKS_FREE = NOT_APPLICABLE
GENIE = NOT_APPLICABLE
```

Nenhum estado `NOT_RUN` pode ser convertido em PASS por inferência.
