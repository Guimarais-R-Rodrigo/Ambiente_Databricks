# SE08 — resultados observados

Este arquivo é append-only por natureza probatória. Ele não transforma comandos
planejados em evidência executada.

## Reconciliação de partida

Foi confirmado no GitHub que a SE07 principal e seus hotfixes foram integrados.
A PR #82 integrou o tratamento de UTF-8 inválido em
`main@c70f5af9b4108f2d99c79ba678719347e91fc910` e seu pós-merge observou
18/18 workflows de push em `success`.

A branch `sef/SE08-operacao` foi observada em
`aa83e5cc2e31da9dbd04ca888fe8d5b2ac2f9d53` antes desta consolidação.
Nenhum resultado de SHA anterior é atribuído automaticamente ao HEAD posterior.

## Evidência focal de policy I/O

Ambiente da bancada: Linux x86_64 / Python 3.13.5, fixtures sintéticas e
componentes conferidos por hash.

Tentativas preservadas:

| Rodada | Alvo | Resultado |
|---|---|---|
| baseline de 12 métodos | implementação anterior | exit 1; uma falha; zero skips |
| baseline ampliada de 15 métodos | implementação anterior | exit 1; três falhas; zero skips |
| candidata focal de 15 métodos | leitura/parse único | exit 0; 15/15; zero skips |

A candidata focal demonstrou que validator e resumo usam o mesmo parse, que
policy ilegível retorna `POLICY_UNREADABLE` e que o CLI respeita
`assistant_root`. Essa evidência pertence aos blobs testados, não certifica a
tree inteira da SE08.

## Evidência ainda não executada para a candidata consolidada

Permanecem sem resultado atribuído ao HEAD final desta consolidação:

- renderer/rematerialização do derivado;
- `validate_assistant.py --conferir-readme` após as mudanças documentais;
- suíte storage cleanup no novo SHA;
- regressões F-04/repo-side/writer no novo SHA;
- FULL `certify_local.py --profile se08`;
- `ci_local.py --verbose`;
- campanha nativa Windows/NTFS;
- Free/verify por conteúdo;
- Genie Code;
- GitHub Actions da futura release candidate.

Portanto: `SE08_FULLY_CERTIFIED=false` nesta fase.

## Promoção ao trabalho

`PROMOCAO_TRABALHO=BLOQUEADA`.

Além de faltarem os gates acima, a decisão G2 preserva SE06 em 24/25 e
explicitamente não satisfaz o gate corporativo da SE08. Nenhuma promoção foi
executada ou autorizada por este documento.


## Fechamento final — 2026-09-22

As pendências registradas acima pertenciam ao checkpoint repo-side inicial e
foram posteriormente executadas. Esta seção é a atualização final; não apaga os
estados históricos anteriores.

### Release candidate certificada

```text
SHA   = ee1cf04b031497bb5b7ddfa47ce28b8015d15668
TREE  = d29fb8221c08ab3ea1fb0198004d4720d4785f92
```

Windows R5:

- corrective 10/10 PASS;
- storage 9/9 PASS;
- certifier: 51 métodos, zero failures/errors, um skip de escopo;
- CI 10/10 PASS;
- FULL 21/21 PASS;
- `LOCAL_CERTIFICATION=PASS`;
- zero infrastructure errors;
- `release_clean_certification=true`;
- `scope_complete=true`.

Bundle Windows SHA-256:
`215176bd9804ab38b2d55678778f1d0defaa334c5040aa13ce5810a43d105d03`.

O WinError32 observado em R2–R4 não reapareceu em R5. Ausência de reprodução não
é prova de correção causal.

### Databricks Free

A RC foi publicada no laboratório pessoal Free e passou:

- dry-run;
- publicação canônica;
- verify rápido;
- verify completo;
- verify por conteúdo;
- 573/573 arquivos comparados;
- zero ausentes/obsoletos;
- 14/14 skills;
- `SE08_FREE_OPERATIONAL_INTEGRITY_V1=PASS`.

Bundle Free SHA-256:
`630a0920955bbba2a7140e03c95d6e7149331ecf26aeb4f08a459130a98a2aae`.

Nenhum artefato behavior-bearing do escopo definido mudou na SE08; por isso
`GENIE_BEHAVIORAL_SCREENING=NOT_APPLICABLE`.

### GitHub e integração

A PR #90 foi aceita humanamente e mergeada em
`627bcc798261451b70d396550fb5f11ca6d609c2`.

Primeiro push pós-merge:

- 18 workflows em success;
- 1 workflow em FAIL: `Kit de transição para o trabalho`;
- causa: chamada incondicional a `PosixPath.is_junction()` no Python 3.11;
- a tentativa foi preservada e não recebeu rerun.

A PR #92 corrigiu exclusivamente a portabilidade da suíte e o filtro de
dependências do workflow. Foi mergeada e produziu:

```text
main = 431c46fcffc9345ad4c24280ba13f2ba1dba579b
```

Pós-merge corretivo: 17/17 workflows disparados em success, inclusive o mesmo
workflow Python 3.11.

O diff entre a RC certificada e a main final contém somente o workflow de
transição e a suíte de teste SE07. Nenhum byte do pacote publicado, policy ou
certifier mudou.

### Classificação final

```text
LOCAL_CERTIFICATION         = PASS
FULL_SE08_LOCAL             = PASS
WINDOWS_R5                  = READY_FOR_REVIEW
GITHUB_ACTIONS              = PASS
DATABRICKS_FREE             = PASS
GENIE_BEHAVIORAL_SCREENING  = NOT_APPLICABLE
SE08_FULLY_CERTIFIED        = true
PROMOCAO_TRABALHO           = BLOQUEADA
```

A classificação da SE08 não reclassifica SE06 ou SE07. A promoção corporativa
continua bloqueada pela dívida explicitamente preservada em G2.
