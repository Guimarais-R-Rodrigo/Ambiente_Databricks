# SE07 — Generalização por risco

## Estado

**PRIMEIRA FATIA HOMOLOGADA LOCALMENTE E NO DATABRICKS FREE; screening comportamental direcionado 3/3 PASS.**

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
| hub-ml-auditoria-skills | L3 | L3 | alto |
| hub-ml-criar-objeto | L2 | L3 | alto |
| hub-ml-explainability | L0 | L3 | médio |
| hub-ml-comentar-notebook | L1 | L1 | baixo |
| hub-ml-concierge | L1 | L1 | baixo |
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


## Evidência da primeira fatia

No HEAD comportamental `af68a9e6bf1b50a3b3c164f22dce327d8cd2fbcb`:

```text
FULL_SE07_LOCAL             = PASS
DERIVED_STALE               = false
DATABRICKS_FREE             = PASS
SE07_FREE_POLICY_PROBE_V1   = PASS
A07-1                       = PASS
A07-2                       = PASS
A07-3                       = PASS
GENIE_BEHAVIORAL_SCREENING  = PASS
GITHUB_ACTIONS              = NOT_RUN
FULLY_CERTIFIED             = false
```

Esse PASS comportamental é específico aos três débitos direcionados da auditoria e não implica que as demais 13 skills já tenham alcançado seus `target_level`.


## Onda L1 homologada

No HEAD `c12d41debcf9c32aa57672c1df36c5af53369e46`, `hub-ml-comentar-notebook` e `hub-ml-concierge` foram homologadas em L1 localmente e no Free, com 2/2 contratos válidos e zero runtime gates adicionados.

A onda seguinte eleva somente a camada contratual de `hub-ml-auditoria-skills` e `hub-ml-criar-objeto` para L1. Seus targets L3 permanecem roadmap.


## Onda L2 — auditoria-skills

A auditoria passa a possuir preflight estruturado antes da lógica substantiva.
O gate resolve modo, inputs mínimos, existência da skill produtora/targets e
policy SEF observável. Ele é somente leitura e não executa verifier. L3 continua
fora desta onda.


## Onda L3 — auditoria-skills

O runner L3 estrutura a evidência, emite Receipt próprio e preserva a autoridade
do verifier da skill produtora. Para EDA L4, o adapter chama diretamente
`verify_finalized`; sem reverificação canônica, o estado continua
`NOT_REVERIFIED`.


## Onda L2 — criar-objeto

O preflight resolve a forma do objeto antes de qualquer escrita: tipo fechado,
nome, template, destino, sobreposição e, quando aplicável, seção de snippet ou
origem de conversão. O gate é somente leitura; L3 continua fora desta onda.
