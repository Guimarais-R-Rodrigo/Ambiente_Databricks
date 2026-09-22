# SE08 — checkpoint final

**Estado:** `ENCERRADA_CERTIFICADA_INTEGRADA`.

## Identidades

```text
main de partida                  = c70f5af9b4108f2d99c79ba678719347e91fc910
RC certificada                   = ee1cf04b031497bb5b7ddfa47ce28b8015d15668
tree da RC                       = d29fb8221c08ab3ea1fb0198004d4720d4785f92
merge PR #90                     = 627bcc798261451b70d396550fb5f11ca6d609c2
corretiva pós-merge PR #92 HEAD  = 03c66d33efc1acf04b447976284c9c2f0fe64a8b
main final observada             = 431c46fcffc9345ad4c24280ba13f2ba1dba579b
```

## Estado de certificação

```text
LOCAL_CERTIFICATION          = PASS
FULL_SE08_LOCAL              = PASS
WINDOWS_R5                   = READY_FOR_REVIEW
DATABRICKS_FREE              = PASS
GITHUB_ACTIONS               = PASS
GENIE_BEHAVIORAL_SCREENING   = NOT_APPLICABLE
SE08_FULLY_CERTIFIED         = true
PROMOCAO_TRABALHO            = BLOQUEADA
```

A RC foi certificada em Windows/FULL, GitHub Actions e Databricks Free. O
produto publicado não sofreu alteração depois dessa certificação.

## Pós-merge

A primeira integração, PR #90, produziu 18/19 workflows de push em success.
O único FAIL ocorreu no `Kit de transição para o trabalho`, porque a suíte
SE07 chamava `Path.is_junction()` em Python 3.11, onde a API não existe.

A tentativa vermelha foi preservada.

A PR #92:

- tornou a detecção de junction compatível com runtimes sem `Path.is_junction`;
- adicionou regressões do helper;
- fez o workflow de transição acompanhar `tools/ci_local.py`,
  `tools/skill_enforcement/**` e `tools/tests/test_skill_enforcement_*.py`.

Pré-merge da #92: V00, V01, V02 e CI em success.

Pós-merge da #92: 17/17 workflows disparados em success. O workflow Python 3.11
que havia falhado passou integralmente, incluindo gate local SEF, contrato V09,
Spark local, geração e conferência do kit.

## Vinculação da evidência

Windows R5 pertence ao SHA da RC:
`ee1cf04b031497bb5b7ddfa47ce28b8015d15668`.

Free final pertence ao mesmo SHA, com 573/573 arquivos comparados.

Entre a RC e a main final, o diff é restrito a:

- `.github/workflows/kit-transicao-trabalho.yml`;
- `tools/tests/test_skill_enforcement_se07.py`.

Não houve mudança do pacote `.assistant`, do simulado, da policy ou do
certifier. A certificação de produto é preservada por equivalência explícita;
não se atribui uma execução Windows inexistente ao merge commit.

## Dívidas preservadas

- SE06 24/25;
- `S06-A1-R4=NOT_RUN`;
- `SE06_DOD=INCOMPLETE`;
- `SE06_FULLY_CERTIFIED=false`;
- `SE07_FULLY_CERTIFIED=false`;
- WinError32 histórico sem owner/root cause estabelecidos;
- criar-objeto L2 global.

## Limite do aceite

O aceite humano autorizou a integração da SE08 e da corretiva pós-merge. Ele não
autoriza promoção corporativa.

`PROMOCAO_TRABALHO=BLOQUEADA` permanece estado canônico.

O procedimento reproduzível continua documentado em
[RUNBOOK_LOCAL.md](RUNBOOK_LOCAL.md).
