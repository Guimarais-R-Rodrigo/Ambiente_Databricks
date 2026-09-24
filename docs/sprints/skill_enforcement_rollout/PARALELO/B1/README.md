# B1 — SER03 L3 + SER05 L2

Base inicial de autoria: `4ba7f551767d847381df1556ed937116258fa77d`, após merge do B0/PR #113.  
P1 integrada: `d2b6079ee2e6ecec628d14411afbdbdb878a5fb9`, PR draft #115.  
A issue #114 é o registro operacional. Nada nesta pasta é promoção automática.

## P1 — autoria de domínio integrada

SER03 recebeu contrato SEF 0.1, schema, preflight mensal/binário, runner fino de `build_vintage_table`, Receipt V1 e verifier vinculado a request/run/oráculo. SER05 recebeu contrato/schema e preflight L2 de contexto, sem leitura de fonte ou join.

No SHA P1 foram observados: 47/47 testes B1 PASS, os 2 testes de integração pública PASS, Temas V07 17/17, mirror 2/2, V08 22/22, validator e renderer PASS. O canal SE07 preservou exatamente os dois FAILs temporais historicamente esperados. Esses resultados permanecem evidência do SHA P1; a P2 não os renomeia como reexecução em SHA posterior.

## P2 — campanha real governada, autoria repo-side

A P2 está materializada em `tools/skill_enforcement/real_campaigns/b1/` e documentada em `P2_ARCHITECTURE.md`.

O B0 fica fechado. Nenhum arquivo em `tools/skill_enforcement/parallel/**` é alterado para aceitar comandos reais. O adapter B1 reutiliza launcher, scheduler, lease, sandbox, process supervision e verifier B0, mas injeta no processo um registry B1 fechado e uma release identity própria. O `finally` restaura os globals importados.

A campanha é read-only, effects `NONE`, uma campanha por host, `max_parallel=2` e `max_auditors=1`.

## Coverage e limites

O registry de coverage liga 19 casos no escopo a testes P1, oráculos e comandos P2. CE03/CE04/CE09/CE11/CE12 permanecem fora do L2 e não são declarados cobertos.

SER03 continua restrita ao perfil mensal/binário sintético. Não há suporte alegado a trimestre, comparação de safras, estimando monetário, plots, Free ou Genie.

SER05 continua contexto/preflight L2. Não há join, Spark, coverage real, readiness ML ou Postflight.

## Próximo gate

P2 está `AUTHORED_NOT_LOCALLY_QUALIFIED`. O próximo passo exige checkout local completo para, uma vez por gate:

1. preflight B1;
2. metatestes da campanha;
3. preparação SHA-bound e geração mecânica do handoff;
4. campanha sandboxed 2/1;
5. auditoria independente das evidências.

Somente depois disso se discute freeze/certificação. Policy, Ready, merge, Free/Genie e promoção continuam não autorizados.
