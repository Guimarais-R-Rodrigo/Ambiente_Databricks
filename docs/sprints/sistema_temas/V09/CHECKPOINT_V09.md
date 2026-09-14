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

- `tools/temas_v09_transicao.py`: contrato e validação fail-closed;
- `tools/bundle_implantacao.py`: valida o contrato antes de criar o ZIP e grava `theme_contract` no manifesto;
- `tools/tests/test_temas_v09.py`: mutantes negativos e invariantes;
- `docs/playbooks/checklist-replicacao.md`: instrução operacional para usuário não técnico;
- `.github/workflows/temas-v09-ci.yml`: gate permanente read-only;
- documentação V09.

## Restrições preservadas

- sem alteração de runtime do produto em `.assistant`;
- sem registro global de tema;
- sem alteração de paleta/schema/tokens;
- sem upload, publicação ou chamada Databricks;
- sem início da V10.

## Próximo gate

Executar o workflow V09 real na branch e registrar exatamente os resultados, inclusive qualquer failure intermediário.
