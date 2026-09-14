# Checkpoint V09 — kit de instalação/transição

## Estado

**EM EXECUÇÃO; SEM ACEITE, MERGE OU PUBLICAÇÃO DATABRICKS.**

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
- documentação V09.

## Limite arquitetural deliberado

O núcleo `tools/aceite_trabalho.py` continua genérico. Ele é embutido no notebook offline e não deve importar outro módulo de `tools/`, que não é levado ao destino. Duplicar nele os nove caminhos temáticos criaria uma segunda fonte de verdade.

Por isso, a cadeia de confiança V09 é:

1. contrato canônico antes do build;
2. validação dos bytes efetivamente colocados no ZIP depois do build;
3. manifesto fixado pelo hash que o notebook já recebe;
4. conferência SHA256 de todos os FILEs pelo aceite no staging/final;
5. conferência humana explícita do `theme_contract` pelo checklist.

## Failures já observados

Os runs `34877035267` e `34877297808` permanecem failures e estão detalhados em `TESTES.md`. O primeiro expôs um oráculo textual incorreto da suíte; o segundo chegou a todos os gates funcionais verdes e falhou apenas porque o README raiz estava com a contagem antiga de arquivos.

## Restrições preservadas

- sem alteração de runtime do produto em `.assistant`;
- sem registro global de tema;
- sem alteração de paleta/schema/tokens;
- sem upload, publicação ou chamada Databricks;
- workflows com `contents: read` e checkout sem credenciais persistentes;
- sem início da V10.

## Próximo gate

Executar o workflow V09 no **head final da candidata**, incluindo a nova inspeção do ZIP, e registrar exatamente contagens, SHA do head, resultado do validador e geração do kit. Só então abrir PR draft para revisão; merge exige aceite explícito de Rodrigo.
