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


## Evidência posterior — R2 a R5 Windows

A seção anterior "Evidência ainda não executada" registra corretamente o estado da consolidação inicial. Ela foi superada por campanhas posteriores e não deve ser lida como estado atual.

### R2

- SHA `d3720f593d56dea64b1f027ad7ba725075f55ef3`;
- classificação `WINDOWS_NOT_READY`;
- storage standalone FAIL 8/9 por WinError32 nativo em subcaso distinto do antigo falso negativo do finalizer;
- certifier standalone 46/46 PASS;
- CI Windows FAIL apenas em SEF/certifier regression;
- FULL não executado.

### R3

- SHA `3556f198670c38d3ced118b3e84db59b5728efa8`;
- classificação `R3_WINDOWS_NOT_READY`;
- storage standalone 9/9 PASS;
- certifier standalone exit 0;
- CI 10/10 PASS;
- FULL FAIL 20/21 por WinError32 em storage;
- Job Object vazio, launcher/child encerrados e Restart Manager sem matches na ocorrência observada.

### R4

- SHA `50776fefc35ae65a48b913b1b190adff9738d19e`;
- classificação `R4_WINDOWS_NOT_READY`;
- storage standalone 9/9 PASS;
- certifier standalone exit 0;
- CI FAIL apenas em SEF, com WinError32 no timeout pai-filho;
- Restart Manager sem matches;
- `FileProcessIdsUsingFileInformation` retornou NTSTATUS success/count=0 após a falha;
- FULL não executado.

### R5

- SHA `ee1cf04b031497bb5b7ddfa47ce28b8015d15668`;
- tree `d29fb8221c08ab3ea1fb0198004d4720d4785f92`;
- classificação do executor `R5_WINDOWS_READY_FOR_REVIEW`;
- windows corrective: PASS 10/10;
- storage standalone: PASS 9/9;
- certifier: 51 métodos, 0 failures, 0 errors, 1 skip de escopo, exit 0;
- CI: PASS 10/10 etapas;
- FULL: `FULL_SE08_LOCAL`, PASS 21/21 gates;
- `failure_count=0`;
- `gate_failure_count=0`;
- `infrastructure_error_count=0`;
- `release_clean_certification=true`;
- `DERIVED_STALE=false`;
- `scope_complete=true`;
- nenhuma ocorrência nativa WinError32 nos process records retidos.

Bundle R5:

- `SEF_SE08_R5_WINDOWS_ee1cf04b_20260922.zip`;
- SHA-256 `215176bd9804ab38b2d55678778f1d0defaa334c5040aa13ce5810a43d105d03`;
- 1628 entradas do manifesto verificadas, zero divergências;
- CRC sem erro.

A R5 demonstra uma campanha Windows completa e verde no SHA testado. Ela não demonstra a root cause das ocorrências intermitentes anteriores e não permite reescrever R2–R4 como se nunca tivessem falhado.

## Classificação atual

- `FULL_SE08_LOCAL=PASS` para `ee1cf04b...`;
- candidata técnica: `READY_FOR_PR_REVIEW`;
- `SE08_FULLY_CERTIFIED=false` no sentido global enquanto Free/Genie e demais gates externos aplicáveis não forem fechados;
- `PROMOCAO_TRABALHO=BLOQUEADA`.

A atualização documental posterior à R5 cria novo SHA e exige recertificação mínima de identidade + CI + FULL antes da integração final.
