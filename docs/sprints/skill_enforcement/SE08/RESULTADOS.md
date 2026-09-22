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
