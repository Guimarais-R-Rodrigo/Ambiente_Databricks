# MM03 — checkpoint de implementação candidata

```text
BASE_MAIN = 073762fd8e38afadf27aca0f4d77351d9bfb627f
BASE_TREE = 3ef561af7ffcd9a613bb815c9470109375aea5ae
BRANCH = micromodelos/mm03-metadata-only
MM02 = ACEITA_E_INTEGRADA_PR109
MM03 = IMPLEMENTADA_CANDIDATA
DEVELOPMENT_TESTS = PASS_45_ON_LINUX_PY3135_PARTIAL_TREE
CANONICAL_LOCAL_SMOKE = NOT_RUN
CANDIDATE_FREEZE = NOT_REACHED
FULL_CERTIFICATION = NOT_RUN
INDEPENDENT_AUDIT = NOT_RUN
MERGE = NOT_AUTHORIZED
MM04 = NOT_STARTED
```

## Reconciliação e escopo

`main` e a integração MM02 foram reconfirmadas pelo conector. PSEF01/PR #99 e
SER01/PR #108 continuam abertas; não foram incorporadas. A policy permanece com
14 skills, sem nova skill/current_level/rollout nesta frente. A última revisão
integrada reserva skill/prompt próprios para MM04 e não impõe dependência PSEF
artificial à MM03.

As regras MM00 R03/R04/R05/R23 e ADR-0020 orientam binding, escopo observado,
metadata não confiável e ausência de ampliação automática de acesso.
Schema_to_yaml não é crawler; não há duplicação de EDA/profiling ou novo helper global.

## Executado nesta sessão

Implementação e testes do coletor/provider sintético; revisão própria do contrato,
limites e CLI; 39 testes PASS na R1 e 45 PASS na R2. Trata-se de desenvolvimento,
não auditoria independente. O conteúdo novo foi materializado no container e
executado com Python real, sem substituição de módulos de produção por mocks.
Os providers roteirizados dos adversariais são explicitamente fixtures de teste.

O acesso Git direto falhou em DNS para github.com; o conector autenticado permitiu
ler/publicar. Não houve clone completo, git status global local, validator global,
regressão MM01/MM02 ou teste Windows. Não transportar o PASS dessas sprints para MM03.

## Pendências bloqueantes antes do freeze

1. Aplicar ENTRADA_CHANGELOG.md ao CHANGELOG.md raiz preservando todos os bytes
   preexistentes; a entrada preparada nesta pasta ainda não substitui esse gate.
2. Reconciliar apenas os parágrafos vivos de Micromodelos em CLAUDE.md,
   docs/sprints/README.md, docs/sprints/micromodelos/README.md e PLANO_MESTRE.md:
   MM02 integrada, MM03 candidata; históricos/ADRs/MM02 intocados.
3. Medir o validator e reconciliar somente o snapshot verificável do README raiz.
4. Publicar um commit de preparação exclusivamente documental, identificar seu SHA
   e executar o smoke canônico. Nenhum patch funcional delegado está autorizado.

A impossibilidade de modificar incrementalmente o CHANGELOG extenso pela rota de
publicação desta sessão não é licença para reconstruí-lo parcialmente ou apagá-lo.
A PR deve permanecer Draft e NOT_READY enquanto a preparação estiver pendente.

## Próximo responsável e parada

ChatGPT mantém implementação/revisão; Codex é laboratório de preparação mecânica e
validação do checkout completo, conforme PREPARACAO_LOCAL.md. Parar no primeiro
FAIL e preservar evidências. Depois do retorno, reavaliar freeze/FULL proporcional.
Não iniciar MM04, publicar, mudar proteção de branch ou pedir ACLs.
