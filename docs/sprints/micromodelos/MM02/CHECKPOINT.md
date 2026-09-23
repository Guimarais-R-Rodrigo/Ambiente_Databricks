# MM02 — checkpoint

## Estado

```text
MM02 = EM_IMPLEMENTACAO
BASE_MAIN = 86d1ff6a52d8ef03f6d5567afed6897c1b96c8c3
BRANCH = micromodelos/mm02-spec-fingerprint
CANDIDATE_FREEZE = NOT_REACHED
LOCAL_EXECUTION = NOT_RUN
PR = #109 OPEN_DRAFT
```

## Escopo implementado repo-side

Até este checkpoint foram materializados:

- algoritmo `mm02-spec-fingerprint-v1`;
- SHA-256 sobre JSON canônico UTF-8;
- validação obrigatória pelo contrato MM01 antes do hash;
- perfil explícito de campos materiais versus ciclo de vida;
- reutilização da equivalência editorial MM01;
- canonicalização de coleções não ordenadas;
- deduplicação de listas editoriais após equivalência MM01;
- canonicalização numérica `int/float` equivalente;
- suíte metamórfica permanente;
- documentação de limites e smoke.

## Decisões da sprint

### Definição versus evidência

O fingerprint identifica a **definição analítica material**.

Ficam fora da identidade:

- fase/condição;
- versão humana;
- proveniência;
- aprovação;
- medição;
- experimento/resultado observado;
- validação;
- tracking;
- governança;
- status institucional de publicação.

Isso preserva a separação arquitetural já aceita:

```text
YAML = definição
fingerprint = identidade material da definição
run / evidence = execução
approval = governança
publication = autoridade externa
```

### Identidade humana

`identidade.nome`, `titulo` e `micromodel_version` não entram no preimage.

O fingerprint pode coincidir entre artefatos distintos quando a definição material for a mesma. Nome e versão humana continuam disponíveis separadamente para rastreabilidade.

### Texto

Não existe normalização semântica geral.

Somente textos normativos selecionados usam a equivalência editorial conservadora já implementada pela MM01. Identificadores operacionais permanecem exatos.

### Números

Valores numéricos materiais usam representação decimal determinística para que `70` e `70.0` sejam equivalentes.

O domínio aceito continua sendo o domínio validado pela MM01.

### Referências materiais versus audit trail

A revisão estática distinguiu referências que apenas provam uma decisão das que definem uma regra:
- `score.semantica_ref` só entra para `OUTRA_APROVADA`;
- `score.normalizacao.referencia` só entra para `CUSTOM_APROVADO`;
- `score.calibracao.evidencia_ref` entra como identidade da calibração escolhida;
- resultados, run IDs, timestamps, responsáveis e proveniência continuam fora.

## Não implementado

- persistência de `spec_fingerprint` no YAML;
- alteração do schema MM01;
- skill;
- prompt;
- metadata crawler;
- MLflow;
- Receipt/Postflight;
- publicação;
- integração Databricks;
- certificação local;
- auditoria independente.

## Próximo gate

Executar `PRE_CERTIFICATION_SMOKE` local, começando pela suíte MM02 e regressões MM01.

Somente após o smoke verde:

1. reconciliar qualquer avanço material da `main`;
2. atualizar documentação viva/snapshot;
3. congelar candidata;
4. executar certificação proporcional single-shot;
5. abrir PR para revisão;
6. submeter à auditoria independente.

Nenhum aceite ou merge é solicitado neste checkpoint inicial.
