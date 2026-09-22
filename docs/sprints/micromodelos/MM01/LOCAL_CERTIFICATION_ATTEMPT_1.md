# MM01 — Local Certification v1 — tentativa 1

Data da execução: 2026-09-22

Status: **FAIL-Closed antes dos gates**

## Identidade certificada pela evidência local

- repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`;
- branch: `micromodelos/mm01-contrato-canonico`;
- HEAD: `5fd97a35426677c296078982bb58479c061d280c`;
- tree SHA: `a46149c8ad31df0aaedf9e3a872aea31d989d0f6`;
- `origin/main`: `85474968f5548c13a9a41a3c84f99b3e18f6874c`;
- merge-base: `85474968f5548c13a9a41a3c84f99b3e18f6874c`;
- `ahead_by=150`;
- `behind_by=0`;
- checkout não shallow;
- worktree limpa;
- merge-ref observado: `edcb4f3e98a9ec43f54a449c0322f3873e7d1156`;
- tree do merge-ref: `a46149c8ad31df0aaedf9e3a872aea31d989d0f6`;
- diff material HEAD × merge-ref: vazio.

## Resultado

O certifier retornou `FAIL` antes do primeiro step executável.

Nenhum gate MM01 ou transversal foi iniciado. Não houve retry-until-green e nenhum comando isolado foi usado como substituição da execução canônica.

O manifest registrou:

- `preflight_ok=false`;
- `postflight_ok=false`;
- `steps=[]`;
- `tree_sha=null` no manifest porque a falha ocorreu antes da gravação do preflight;
- coleta pós-falha com a worktree ainda limpa e a identidade Git preservada.

## Causa

A falha foi:

`FileNotFoundError: [WinError 2] O sistema não pode encontrar o arquivo especificado`

O ponto causal foi `base_runtime_preflight` ao executar `npm --version` com `subprocess.run(..., shell=False)`.

No Windows observado, Node/npm estavam instalados e `npm --version` funcionava no PowerShell, mas o entrypoint disponível era um shim `npm.cmd`/PowerShell e não `npm.exe`. A resolução direta do nome `npm` pelo subprocesso falhou antes do preflight completo.

Isso é um defeito de portabilidade do executor local, não evidência de falha funcional do contrato MM01.

## Ambiente observado

- Windows;
- Python `3.12.10`;
- ambiente Python externo ao repositório;
- Git `2.55.0.windows.5`;
- Node `22.21.1`;
- npm `10.9.4` observado externamente;
- pnpm não alcançado;
- nenhum bootstrap executado pelo certifier.

## Integridade do bundle

SHA-256 do ZIP:

`32b7eb9c42b160113d671f331a2ad4a984a2781447bbd640545899e0aa7fc773`

O hash produzido pelo certifier e o hash recalculado independentemente coincidiram.

O bundle continha somente:

- `manifest.json`;
- `postflight.json`;
- `environment.json`;
- `SHA256SUMS.txt`.

Isso é coerente com falha anterior ao preflight e aos steps.

## Correção autorizada pela natureza do finding

A correção deve permanecer restrita à camada operacional da certificação local:

1. resolver comandos por PATH/PATHEXT;
2. no Windows, executar shims `.cmd`/`.bat` pelo command processor;
3. aplicar o mesmo mecanismo a `npm`, `pnpm` e demais comandos externos;
4. manter comandos ausentes como falha fechada;
5. registrar comando lógico e comando efetivamente resolvido;
6. preservar todos os gates e critérios de aceite existentes.

Não é autorizada qualquer alteração em R01–R08, schema, validador MM01 ou testes funcionais para contornar essa falha.

## Próximo passo

A árvore corrigida precisa receber nova reconciliação com a `main` vigente, se necessária, e então uma **nova execução integral** da MM01 Local Certification v1 em novo diretório de saída.

A tentativa 1 permanece histórica como `FAIL`; uma execução posterior não a reclassifica.
