# SE07 — Generalização por risco

## Estado

**IMPLEMENTAÇÃO INICIAL PRESENTE NA BRANCH; gate local/renderer/Free ainda não executado.**

Branch: `sef/SE07-generalizacao`  
Baseline: `main@72894c5511abfa9a5ede3edb4a6f7c5fe11231b3`  
Origem da autorização: Gate G2 integrado pela PR #79.

## Objetivo canônico

Aplicar enforcement proporcional ao restante do catálogo sem transformar todas as skills em pipelines pesados.

O DoD do Plano Mestre é:

> todas as skills possuem uma política de enforcement explícita, inclusive quando a decisão for permanecer em L0/L1.

## Decisão arquitetural

Separar:

1. **current_level** — nível realmente implementado e provado hoje;
2. **target_level** — nível máximo aprovado para migração;
3. **rollout_mode** — guidance/audit/warn/enforce.

Uma skill citar helpers não a transforma em L2/L3. Sem contrato/preflight/runner/postflight correspondente, o `current_level` não sobe.

A política canônica fica em `hub_padroes/skill_enforcement/policy.json` e é resolvida por `hub_scripts.skill_execution.get_skill_enforcement_policy`.

## Classificação inicial

| Skill | Current | Target | Risco |
|---|---:|---:|---|
| hub-ml-eda-profissional | L4 | L4 | alto |
| hub-ml-cross-eda-ml | L0 | L4 | crítico |
| hub-ml-feature-engineering | L0 | L4 | crítico |
| hub-ml-baseline-ml | L0 | L4 | crítico |
| hub-ml-monitoramento-modelo | L0 | L4 | crítico |
| hub-ml-pipeline-builder | L0 | L4 | crítico |
| hub-ml-validacao-estatistica | L0 | L3 | alto |
| hub-ml-analise-safra | L0 | L3 | alto |
| hub-ml-auditoria-skills | L0 | L3 | alto |
| hub-ml-criar-objeto | L0 | L3 | alto |
| hub-ml-explainability | L0 | L3 | médio |
| hub-ml-comentar-notebook | L0 | L1 | baixo |
| hub-ml-concierge | L0 | L1 | baixo |
| hub-ml-tutor-databricks | L0 | L0 | baixo |

## Primeira fatia

- registry 14/14;
- resolver runtime somente leitura;
- validador determinístico;
- testes contra overclaim;
- perfil local `se07`;
- reforço da auditoria para ladder completa e reverificação independente.

## Fora desta fatia

- elevar automaticamente as outras 13 skills;
- criar contratos/runners em massa;
- abrir PR/Actions antes dos gates local/Free;
- iniciar SE08.
