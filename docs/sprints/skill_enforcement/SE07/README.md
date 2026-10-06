# SE07 — Generalização por risco

> **Nota administrativa — 06/10/2026.** [SER e policy atuais](../../skill_enforcement_rollout/README.md) governam a continuidade. O texto abaixo preserva o fechamento SEF, inclusive níveis e próximos passos históricos; níveis posteriores não recertificam este ensaio. Cleanup permanece FAIL e `SE07_FULLY_CERTIFIED=false`; não reabrir F-04 como próxima ação automática.

## Registro histórico preservado

## Encerramento da SE07 — decisão humana com residual conhecido — 2026-09-21

A SE07 está **ENCERRADA_POR_DECISAO_HUMANA_COM_RESIDUAL_CONHECIDO**.

A decisão humana aceita a candidata PG-01 recertificada no Windows apesar da
reprovação do gate separado `01_storage_cleanup`. O resultado técnico não é
reescrito: `01_storage_cleanup=FAIL` (8/9 métodos aprovados), enquanto F-04,
repo-side, writer L3, regressão SE07, renderer, validator/snapshot e o FULL de
16 gates passaram no mesmo estado testado.

A candidata local testada foi `4b8bb46d40790ef8a7272e3a6f75c46eaee118b3`,
parent `8db4c9842112ab31dc92f97fc2740ace7df6032e`, tree
`c36e501542cd62cbb3646f69f0f6b8457d7d7ef4`. A publicação remota equivalente
usa o mesmo parent e a mesma tree testada; seu SHA é
`b5a4eb9d277697125740810d8869b49c797836fd`. A diferença de SHA decorre apenas
dos metadados do commit de publicação, não dos bytes da tree.

A falha aceita pertence ao oráculo sintético
`test_residue_is_observed_not_deleted_or_certified_by_recovery`: a injeção
observou o diretório antes do erro, mas o oráculo externo posterior já o encontrou
ausente. O processo permaneceu corretamente `INTERRUPTED`, exit externo 130,
`process_cleanup=COMPLETE`, `temporary_cleanup=FAILED` e `cleanup=FAILED`.
A causa da remoção entre os dois pontos não foi estabelecida. O WinError32
histórico nativo não foi reproduzido nesta recertificação; isso não significa
que sua causa tenha sido resolvida.

Semântica do fechamento:

- `SE07_DOD_POLICY_REGISTRY=PASS`: 14/14 skills possuem política explícita;
- `SE07_FULLY_CERTIFIED=false`: o gate obrigatório separado continua FAIL;
- a falha residual é `ACCEPTED_FOR_SE07_CLOSURE_BY_HUMAN_DECISION`;
- `hub-ml-criar-objeto` permanece L2 no registry global;
- o piloto `create/readme/agregador` não promove a skill inteira nem recebe
  promoção operacional adicional neste fechamento;
- Free/Genie do piloto, PR, Actions e merge em main não são inferidos deste aceite;
- SE06 permanece 24/25, A1-R4 NOT_RUN, DOD INCOMPLETE e FULLY_CERTIFIED=false.

A dívida do oráculo de resíduo segue registrada para operação/rollout futuro.
Qualquer promoção ao workspace do trabalho continua sujeita aos gates próprios
da SE08, inclusive validações locais pertinentes e avaliação de achados abertos.

SE08 permanece **NÃO_INICIADA** neste commit.


## Rodada histórica — piloto de criação, após aceite F-04

O usuário aceitou a corretiva F-04 `d49c8728f0e47adc15f7f78293c9fcc58c809a15`.
A canônica `sef/SE07-generalizacao` foi promovida exclusivamente até esse SHA,
por fast-forward; main e a review F-04 foram preservadas. A nova rodada implementa
somente `create/readme/agregador`, conforme [piloto L3](PILOTO_README_L3.md) e
[interface congelada](INTERFACE_README_L3.md). A candidata nova exige auditoria
externa e decisão humana; não promove `current_level=L2`.

A aprovação de D2/D9 é **parcial**, apenas esse piloto, com um destino ausente em
pasta real existente. O restante permanece `PROPOSTA_NAO_APROVADA`. Arquitetura
A+C: runner no produto; validator, renderer e certificação no repositório.
Free/Genie, conversão, overwrite, R2 e SE08 não fazem parte desta rodada.

Consulte [checkpoint](CHECKPOINT.md), [testes](TESTES.md) e
[handoff do piloto](../../../handoffs/2026-09-21_se07-criar-objeto-l3-readme-piloto.md).
As próximas seções registram estados históricos anteriores a esta decisão.

## Próxima ação naquele fechamento — revisão da corretiva F-04

O [checkpoint aceito](CHECKPOINT.md) é F-03, preservado na branch canônica remota.
O lote F-04 `b4f8f7b...` permanece historicamente **NAO_APTA**; a rodada seguinte
trata somente SUP-F04-01/02/03. Consulte o [handoff versionado](../../../handoffs/2026-09-21_se07-f04-corretiva.md)
para candidata, gates, tentativas e limites; [TESTES.md](TESTES.md) é a matriz
permanente e [F04_D10.md](F04_D10.md) explica o comportamento do certifier.

O próximo evento é auditoria focalizada seguida de decisão humana. Branch de
review não equivale a aceite, homologação nem avanço de nível. A
[proposta D2/D9](PROPOSTA_D2_D9.md) permanece **PROPOSTA_NAO_APROVADA**, sem writer.
As seções abaixo preservam a sequência histórica e os bloqueios de cada rodada.

## Continuidade delimitada após aceite F-03 — 2026-09-21

F-03 `1ce5806cc04654eda88966676fe90459488553d4` recebeu aceite humano focalizado.
A [retificação E-01/E-02](RETIFICACAO_E01_E02.md) preserva os FAILs recuperados e
esclarece o contrato de issues. O lote local seguinte reúne F-04/D10 e uma
[proposta D2/D9](PROPOSTA_D2_D9.md) **não aprovada**, sem writer.
Detalhes do certifier: [F04_D10.md](F04_D10.md). A certificação do SHA integrado é
registrada no handoff externo após o freeze; o aceite anterior não a substitui.

Checkpoint remoto: **BLOQUEIO_DE_PUBLICACAO** nesta rodada por indisponibilidade
de credenciais Git. A consulta de leitura observou SE07 em `b6fb5952` e main em
`72894c55`; nenhum push foi executado. O checkout do operador permanece na F-03.
PR, Actions, Free/Genie, merge, R2 e SE08 não foram autorizados neste lote.
Os estados e próximos passos datados abaixo são históricos.

## Estado

O checkpoint humano aceito da correção R1-C é
`b6fb595225e139329df450edfc33158ceb1e1253`: estabilização local L2 de
criar-objeto, limitada a F-01/F-02. O SHA R1 `2d25bd2...` permanece NAO_APTA
historicamente. O checkpoint aceito foi publicado somente na branch SE07, sem
PR, merge, Actions ou Free/Genie.

A candidata local seguinte trata F-03/D6 do adapter L3 de auditoria: distingue
verifier localizado/importado/chamado/concluído, valida a forma canônica atual
e não admite `PASS_REVERIFIED` com `issues` não vazio. Ela ainda exige
certificação e revisão focalizada; F-02 permanece preservado. Estado,
evidências externas e dívidas: [CHECKPOINT.md](CHECKPOINT.md). Sem encerramento
SE07, writer L3 ou início R2.

### Registro R1 anterior à auditoria

**R1 — estabilização local delimitada de criar-objeto L2.** A baseline intacta
`a01d12ff4e0cb7cfd795ade164f9ce9daad372ba` passou o FULL_SE07_LOCAL. O commit
candidato R1 exige certificação própria, vinculada ao SHA no bundle externo.
Estado, identidades e próximo gate: [CHECKPOINT.md](CHECKPOINT.md).

A primeira fatia e as ondas anteriores têm homologações históricas no Free;
elas não homologam a candidata R1. A próxima etapa proposta é revisão
independente somente leitura, ainda não executada nesta rodada.

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

## Classificação implementada na baseline R1

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

As seções seguintes registram a sequência histórica das ondas. Seus próximos
passos não substituem o estado corrente do checkpoint.

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
