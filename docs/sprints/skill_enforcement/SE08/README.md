# SE08 — CI, operação, documentação e gate de promoção ao trabalho

**Status:** implementação repo-side em consolidação; não é release candidate, não está certificada e não autoriza promoção.

## Objetivo

Tornar o Skill Enforcement Framework uma capacidade permanente do Hub sem
confundir estrutura válida, comportamento do Genie Code, publicação no Free e
promoção ao workspace do trabalho.

A SE08 operacionaliza o que já foi construído em SE01–SE07. Ela não promove
skills apenas por atingir a sprint final e não reclassifica dívidas históricas.

## Escopo implementado no repositório

A integração repo-side cobre:

- `tools/validate_assistant.py`: contratos e policy SEF passam a integrar o
  validador geral contra a mesma raiz analisada;
- `tools/ci_local.py`: o subgate SEF passa a usar o perfil cumulativo `se08`,
  em modo parcial/read-only;
- `tools/skill_enforcement/certify_local.py`: perfil FULL `se08` cumulativo,
  incluindo regressão de I/O da policy, regressão operacional, renderer,
  render-diff e snapshot;
- `tools/skill_enforcement/se07_policy.py`: leitura única do registry, suporte
  a `assistant_root` e FAIL estruturado para policy ilegível;
- `validate_contracts.py`: arquivo JSON com UTF-8 inválido é contrato ilegível,
  não traceback;
- template canônico de skill, guia das skills, policy README e Manual Técnico:
  distinção permanente entre `current_level`, `target_level` e rollout;
- runbook/checklist de transição ao trabalho: gate SE08, rollback e bloqueio
  corporativo enquanto a exceção G2 não satisfizer o gate de promoção;
- regressões específicas da SE08.

`hub-ml-criar-objeto` e `hub-ml-auditoria-skills` já estavam integradas pela
SE07 e não foram alteradas só para gerar churn. Criar-objeto permanece L2 global;
auditoria permanece L3 stage-specific conforme a policy vigente.

## O que não foi feito nesta fase repo-side

- nenhuma promoção de `current_level`;
- nenhuma alteração de `policy.json`;
- nenhuma publicação no Databricks Free ou no trabalho;
- nenhum teste conversacional Genie;
- nenhuma reclassificação da SE06/SE07;
- nenhuma edição manual de `Novo_Ambiente_Simulado/`.

As alterações em `ambiente_fonte/` exigem rematerialização pelo renderer
canônico no próximo gate local. Até isso ocorrer, drift do derivado é esperado e
deve ser resolvido pelo comando canônico, não por edição manual.

## Gate de promoção ao trabalho

O Plano Mestre exige, cumulativamente:

1. validações locais pertinentes em PASS;
2. renderer sem divergência;
3. publicação Free verificada por conteúdo;
4. casos críticos SE06 sem escaped non-compliance;
5. zero achados críticos/altos abertos relacionados ao enforcement;
6. documentação operacional completa;
7. aceite explícito do usuário;
8. rollback definido.

G2 preservou `SE06_DOD=INCOMPLETE` e declarou que sua exceção não satisfaz o
gate de promoção corporativa da SE08. Portanto, no estado atual, preparação e
staging podem ser estudados, mas **PROMOCAO_TRABALHO=BLOQUEADA** até nova decisão
humana específica sustentada por evidência suficiente.

## Dívidas históricas carregadas

- SE06: 24/25; `S06-A1-R4=NOT_RUN`; `SE06_DOD=INCOMPLETE`;
  `FULLY_CERTIFIED=false`;
- SE07: encerrada por decisão humana com residual conhecido;
  `SE07_FULLY_CERTIFIED=false`;
- storage cleanup histórico: FAIL 8/9, causa do desaparecimento intermediário do
  resíduo não estabelecida;
- WinError32: não reproduzido na recertificação final não equivale a corrigido;
- criar-objeto: L2 global; piloto L3 stage-specific não promove a skill inteira.

## Próximo gate

A próxima etapa é local e está descrita em [RUNBOOK_LOCAL.md](RUNBOOK_LOCAL.md).
Somente depois da materialização do derivado, bateria local e certificação FULL
no SHA congelado a candidata pode ser avaliada para Free/Genie e posterior PR.
