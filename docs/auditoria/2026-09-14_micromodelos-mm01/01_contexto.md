# Auditoria A1 — MM01 — contexto neutro

## Objeto

Auditar a candidata da sprint **MM01 — contrato canônico de micromodelos**, na branch:

`micromodelos/mm01-contrato-canonico`

A auditoria deve sempre registrar o **HEAD efetivamente observado no início da sessão**. Não assuma que o SHA deste contexto continuará sendo o último da branch.

## Propósito da auditoria

Verificar de forma independente se o schema, o template e o validador implementam um contrato coerente, fail-closed e alinhado às decisões arquiteturais já aceitas, sem antecipar sprints posteriores.

Este arquivo não descreve o conteúdo da implementação nem fornece um resumo dos testes. Ele existe apenas para fixar o objeto, as fontes permitidas e as fontes vedadas.

## Fontes primárias permitidas

Leia e audite diretamente:

- `docs/sprints/micromodelos/MM01/micromodelo.schema.json`;
- `docs/sprints/micromodelos/MM01/micromodelo.template.yaml`;
- `tools/micromodelo_mm01_contract.py`;
- `tools/tests/test_micromodelo_mm01.py`;
- `tools/tests/fixtures/micromodelos_mm01/valido_validado.json`;
- `tools/tests/fixtures/micromodelos_mm01/casos_invalidos.json`;
- `.github/workflows/micromodelos-mm01-ci.yml`;
- `tools/requirements-dev.txt`.

Para requisitos arquiteturais, consulte somente as decisões aceitas e políticas estruturais relevantes:

- `docs/decisions/ADR-0014-micromodelo-artefato-de-dominio.md`;
- `docs/decisions/ADR-0015-micromodelo-yaml-canonico.md`;
- `docs/decisions/ADR-0016-mlflow-historico-execucao.md`;
- `docs/decisions/ADR-0017-governanca-externa-publicacao.md`;
- `docs/decisions/ADR-0018-migracao-legado-pos-piloto.md`;
- `docs/decisions/ADR-0019-integracao-visual-tardia.md`;
- `docs/decisions/ADR-0020-fontes-catalogo-configurado.md`;
- `tools/project_policy.py`;
- `tools/validate_assistant.py`;
- `ambiente_fonte/.assistant/hub_padroes/auditoria/template.md`.

## Fontes vedadas ao auditor

Não leia nem use como fundamento:

- `CHANGELOG.md`;
- histórico/ mensagens de commits ou PRs para inferir intenção;
- qualquer relatório anterior em `docs/auditoria/` além deste contexto e do prompt desta auditoria;
- `docs/sprints/micromodelos/MM01/README.md`;
- `docs/sprints/micromodelos/MM01/CONTRATO_MICROMODELO.md`;
- `docs/sprints/micromodelos/MM01/ESTADOS_E_PROVENIENCIA.md`;
- `docs/sprints/micromodelos/MM01/TESTES.md`;
- `docs/sprints/micromodelos/MM01/CHECKPOINT.md`;
- respostas ou explicações do autor da candidata.

A intenção é evitar que a auditoria apenas confirme a narrativa da implementação.

## Regras de independência

- execute/reproduza os testes; não se limite a ler arquivos;
- crie casos adversariais próprios em memória ou arquivos temporários não versionados;
- não implemente correções;
- não altere a branch candidata;
- não transforme falha de infraestrutura em aprovação técnica;
- se um requisito não puder ser provado pelas fontes permitidas e pela execução, registre a incerteza;
- classifique cada achado como `QUEBRA`, `DIVERGE` ou `MELHORÁVEL`, conforme o template canônico.
