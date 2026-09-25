# G6 local package validation R2 — fechamento

## Freeze do pacote externo

```text
G6_LOCAL_PACKAGE_VALIDATION_R2 = PASS
G6_FREEZE_SHA = c11c2dff07f0f7595ed545f32990e5d54f1fd583
G6_FREEZE_TREE = 15527a29db0e6bcefa639cfadd4d66eed1d32d83
```

A R1 em `814ae6f3286...` permanece FAIL por oráculo textual frágil e não foi reexecutada.

## Gates R2

```text
validate_package = PASS
metatests = 6/6 PASS
product_diff_from_R7 = PASS / zero
authority = PASS / all external phases unauthorized
authorization_request = PASS / request only, not authorization
free_probes = PRESENT / NOT_EXECUTED
genie_manifest = PASS / 20 variants / NOT_RUN
```

O produto permanece byte-idêntico ao R7 funcional qualificado nas árvores protegidas:
- `ambiente_fonte/**`;
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/**`;
- B0;
- policy.

## Próximo gate

O primeiro efeito externo autorizável é somente:

`G6.READ_ONLY_RECONCILE`

Escopo proposto:
- descrever auth/profile;
- obter current-user;
- verificar que o workspace é pessoal/Free;
- executar somente verify de conteúdo remoto;
- nenhum publish;
- nenhum import;
- nenhum probe;
- nenhum Genie;
- nenhum cleanup.

Se houver mismatch remoto, parar. Publicação exige autorização separada posterior.

```text
G6_EXTERNAL_EXECUTION = NOT_RUN
DATABRICKS_FREE = NOT_RUN
GENIE = NOT_RUN
SER03_L3 = NOT_PROMOTED
SER05_L2 = NOT_PROMOTED
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```
