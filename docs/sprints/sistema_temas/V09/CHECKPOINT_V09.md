# Checkpoint V09 — kit de instalação/transição

## Estado

**CANDIDATA TECNICAMENTE FECHADA; SEM ACEITE, MERGE OU PUBLICAÇÃO DATABRICKS.**

Base: `55f7006c47d90ae7f760992d252b658f53a59636`.

Branch: `codex/temas-v09-kit-transicao-20260914`.

## Achado de entrada

O kit existente já empacotava a árvore sanitizada completa e protegia FILEs por SHA256. A integração do Sistema de Temas, contudo, era implícita: o manifesto não nomeava um subconjunto temático obrigatório e o bundle não tinha uma guarda específica contra perda desse contrato.

## Decisão V09

Adicionar uma guarda offline de inventário e um bloco declarativo `theme_contract` ao manifesto v2, preservando todo o fluxo de aceite existente.

O contrato distingue explicitamente:

- **transportar:** obrigatório e protegido por hash;
- **ativar:** somente opt-in/manual;
- **publicar:** não realizado pela V09.

## Implementação atual

- `tools/temas_v09_transicao.py`: contrato, validação fail-closed do inventário e verificação pós-build do ZIP;
- `tools/bundle_implantacao.py`: valida o contrato antes de criar o ZIP e grava `theme_contract` no manifesto;
- `tools/tests/test_temas_v09.py`: mutantes negativos, invariantes e verificação dos bytes do ZIP;
- `docs/playbooks/checklist-replicacao.md`: instrução operacional para usuário não técnico;
- `.github/workflows/temas-v09-ci.yml`: gate permanente read-only, incluindo reabertura do ZIP gerado;
- `.github/workflows/kit-transicao-trabalho.yml`: gate V09 e verificação do ZIP antes de `upload-artifact`;
- documentação e índices da V09.

## Limite arquitetural deliberado

O núcleo `tools/aceite_trabalho.py` continua genérico. Ele é embutido no notebook offline e não deve importar outro módulo de `tools/`, que não é levado ao destino. Duplicar nele os nove caminhos temáticos criaria uma segunda fonte de verdade.

Por isso, a cadeia de confiança V09 é:

1. contrato canônico antes do build;
2. validação dos bytes efetivamente colocados no ZIP depois do build;
3. manifesto fixado pelo hash que o notebook já recebe;
4. conferência SHA256 de todos os FILEs pelo aceite no staging/final;
5. conferência humana explícita do `theme_contract` pelo checklist.

## Failures preservados

Os runs `34877035267` e `34877297808` permanecem **FAILURE** e estão detalhados em `TESTES.md`.

- `34877035267`: 7/8 V09; falhou por oráculo textual incorreto que procurava `manual/opt-in` em vez da chave real `manual_opt_in`.
- `34877297808`: todos os gates funcionais passaram, mas o validador reprovou porque o README raiz ainda registrava 1350 arquivos em vez dos 1355 medidos.

Nenhum deles foi reclassificado.

## Gate completo verde de referência

O run `34878578986`, no head `6c19ef6da1012b4c33bd0e15c1bb332a6cb046a3`, concluiu com `success` em todas as etapas:

- V09 **11/11**;
- kit de transição **43 testes, 36 PASS + 7 SKIP Spark** nessa chamada sem `--spark`;
- cumulativo V01–V09 **416/416**;
- V00 **12/12**;
- bundle offline **535 arquivos + `MANIFEST.json`**;
- `theme_contract` v1 **9/9 caminhos presentes e SHA256 válidos no ZIP**;
- validador **0 falhas / 0 avisos**;
- `GITHUB_TOKEN` somente `Contents: read` / `Metadata: read`;
- nenhuma publicação, ativação ou promoção Databricks.

As alterações posteriores a esse run são somente documentais: reconciliação dos índices e deste registro. O head que for aberto em PR precisa repetir o gate exato; o resultado da PR, e não este parágrafo, será a evidência final de mergeabilidade.

## Escopo do diff

A V09 não altera qualquer arquivo do produto em `ambiente_fonte/.assistant` ou `Novo_Ambiente_Simulado`. O runtime, schema temático, tokens, paletas, APIs legadas e rotas `_resolvido` permanecem byte a byte como estavam na base V08. A mudança funcional fica na ferramenta de empacotamento e nas guardas offline.

## Restrições preservadas

- sem alteração de runtime do produto em `.assistant`;
- sem registro global de tema;
- sem alteração de paleta/schema/tokens;
- sem upload, publicação ou chamada Databricks;
- workflows com `contents: read` e checkout sem credenciais persistentes;
- sem início da V10.

## Próximo gate

Executar o workflow V09 no **head documental final**, confirmar `behind_by=0`, abrir PR em draft e auditar os checks realmente disparados pela PR. Merge exige aceite explícito de Rodrigo.
