---
name: validar-assistant
description: >-
  Valida localmente ambiente_fonte/ e interpreta contadores, avisos e falhas
  antes de commit do produto, render ou publicação. Use para checar a estrutura
  do Hub; não para executar análise de dados, publicar ou certificar runtime.
---

# Validar o ambiente_fonte

## Intenção e pré-condições

Use para validar alterações aprovadas do produto ou conferir a fonte antes de
renderizar/publicar. Não use como substituto de EDA, testes comportamentais,
certificação de enforcement ou aceite Databricks.

Precisa do checkout completo, Python compatível e dependências dos owners em
[tools/README.md](../../../tools/README.md). Confira a raiz/branch/SHA e o
escopo autorizado. Dependência ausente, checkout incompleto ou raiz inexistente
é bloqueio a relatar; não instale dependências nem relaxe checks sem o escopo
necessário. O procedimento é de leitura local; selecionar esta skill não autoriza mudança
no produto, publicação, acesso remoto ou correção automática.

## Executar e interpretar a saída

Da raiz do repositório:

```sh
python tools/validate_assistant.py
```

O owner é [validate_assistant.py](../../../tools/validate_assistant.py). A saída
real contém contadores de cobertura, depois apenas linhas `WARN`/`FAIL`, se
houver, e um resumo `APROVADO: N falha(s), M aviso(s)` ou
`REPROVADO: N falha(s), M aviso(s)`. **Não há PASS por check.**
Exit code 0 significa nenhuma falha bloqueante nos checks executados; 1 indica
falha. Um erro de execução/pré-requisito deve ser registrado como tal, não como
validação concluída. Avisos podem coexistir com exit 0: informe-os.

Contagens vêm da execução nesse SHA e dos owners, nunca de números congelados
nesta skill. Confira principalmente:

- catálogo/frontmatter/seções de produto: `EXPECTED_SKILL_NAMES` em
  [project_policy.py](../../../tools/project_policy.py);
- prompts/campos, helpers citados, READMEs operacionais e exemplares separados;
- contratos SEF e issues de policy, sem confundir quantidade de contratos com
  quantidade de skills;
- volume não vazio da varredura de identidade, links e AST. Zero onde deveria
  haver conteúdo pede investigação; não significa cobertura total.

`--conferir-readme` acrescenta a conferência de saídas locais do README, sem
Databricks. `--root <raiz>` escolhe outra raiz de produto para diagnóstico local.
`--conferir-readme-remoto` consulta CLI autenticada e é outro escopo; não use
essa flag em uma validação somente local nem como teste offline.

## Cobertura e limites

O validador cobre inventário/frontmatter, cinco seções estruturais do produto,
referências a helpers, contrato humano dos prompts, READMEs de objeto e pendências,
links Markdown/notebooks e links externos à raiz analisada com caixa correta,
cercas de código, Python por AST, forma das pastas e fachadas `__init__`, contratos
de entrada/saída, normas do molde (coleta/cache/sessão), sincronia do marcador do
smoke, docstrings, exemplos exercitados e saídas coladas. Confere também o limite
das instruções, UTF-8/mojibake, identidade pessoal/corporativa e higiene do
worktree. Tamanho de skill e `__pycache__` produzem avisos.

Na baseline de migração `f2843eafae84d44cd751f307101de84f11981bd7`, a descoberta
primária cobre **14 contratos** `skills/*/execution_contract.json`; existem
**oito contratos auxiliares** fora desse glob. Eles não são certificados pelo
resumo primário, nem a soma representa skills. Para conferir auxiliares,
inventarie os paths do SHA e use explicitamente `--contract <path>` (repetível)
no [validador de contratos](../../../tools/skill_enforcement/validate_contracts.py),
apenas conforme o escopo. Não transforme 14/14 em aprovação dos oito auxiliares.
Essa ferramenta específica tem saída e retorno próprios; não confunda seu
`PASS` por contrato com a saída do validador geral.

Esta lista descreve cobertura, não suficiência. Link para documento errado que
existe, path só em crase, frase truncada, qualidade didática e comportamento de
runtime exigem revisão adicional. Um gate estático não prova execução Spark,
ACL, seleção Genie, publicação, CI agregado ou homologação corporativa.

## Falhas e conclusão

- Identificador pessoal/corporativo: bloqueie commit, remova ou parametrize na
  fonte dentro do escopo aprovado; nunca contorne o gate.
- Aviso de tamanho: ao editar a skill, mova detalhes para `references/` ou
  `templates/` pertinentes e preserve a rota de leitura.
- Correção autorizada: refaça a validação depois da última edição. Não repare o
  espelho à mão nem corrija produto fora do pedido.
- Registre SHA/estado do checkout, comando, exit code, contadores, avisos,
  falhas e o que não foi testado no [CHANGELOG](../../../CHANGELOG.md) e na
  evidência da tarefa. Sucesso é apenas o alcance efetivamente observado.

## Casos de aceitação do procedimento

- **Positivo:** “Confira a fonte antes do render.” Executar o gate local e
  relatar seu resumo real, sem publicar.
- **Negativo de intenção:** “Faça EDA da tabela.” Não selecionar esta rotina
  como execução analítica; encaminhar ao
  [catálogo do produto](../../../ambiente_fonte/.assistant/skills/README.md).
- **Pré-requisito ausente:** fonte ou dependência indisponível. Parar no
  bloqueio, sem inventar contadores ou PASS e sem instalar silenciosamente.
