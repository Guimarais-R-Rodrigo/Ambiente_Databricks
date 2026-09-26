# SER paralelo — plano detalhado de autoria e execução governada

**Versão 1.3 — 26/09/2026. Autoria: ChatGPT.**

O usuário aprovou a direção de execução paralela e, em 24/09/2026, autorizou a implementação do B0. Este pacote continua sendo o plano detalhado. O B0 em `tools/skill_enforcement/parallel/` está integrado e fechado; documentos B0 permanecem como evidência histórica. O estado vivo da frente corrente está em `B1/AUTHORING_STATE.json`. A existência do mecanismo ou do controller não autoriza promoção de policy ou merge.

Base Git conferida: `d2988e97e7b6c5fe1fd561852e947a155c2d731b`, no repositório `Guimarais-R-Rodrigo/Ambiente_Databricks`. A SER01 está integrada nessa base. As oito frentes restantes preservam os identificadores SER02–SER14; SER15/SER16 preservam suas funções de reconciliação e fechamento.

## Próxima ação

O B0 está integrado pela PR #113. O piloto real B1 (SER03 L3 + SER05 L2) está em
G6 com recuperação residual de probe, sem promoção.

Com o ADR-0024, a coordenação pode usar **Codex Autonomous Controller Mode**.
O controller recebe uma frente fechada, gera internamente tasks fechadas e percorre
investigação → autoria → verificação → auditoria → reparo causal até Human Gate,
sempre dentro do envelope ativo.

Para B1, o envelope inicial em
`docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json` ativa somente A0/A1. A2
remoto permanece pendente. O state source continua
`B1/AUTHORING_STATE.json`; o protocolo autônomo não cria um segundo estado da
campanha.

## Organização e documento dono

| Documento | Responsabilidade exclusiva |
|---|---|
| [01 — Mandato e decisões](01_MANDATO_DECISOES.md) | Escopo, autoridade, baseline e alterações explícitas ao processo antigo |
| [02 — Arquitetura e contratos](02_ARQUITETURA_CONTRATOS.md) | Componentes, schemas, interfaces e identidade da campanha |
| [03 — Ciclo e gates](03_CICLO_GATES.md) | Entrada, estados, congelamento, falhas, retomada e promoção |
| [04 — CI e cobertura](04_CI_COBERTURA.md) | Cobertura herdada, fases de teste, seleção e oráculos históricos |
| [05 — Casos transversais](05_CASOS_TRANSVERSAIS.md) | Casos comuns e metatestes do mecanismo |
| [Dossiês por skill](dossies/README.md) | Escopo e provas específicas das oito skills |
| [06 — Auditoria e evidência](06_AUDITORIA_EVIDENCIA.md) | Revisão independente, RAW/SHARE, finding e suficiência probatória |
| [07 — Paralelismo e integração](07_PARALELISMO_INTEGRACAO.md) | Isolamento, recursos, DAG, merge e mudança de base |
| [08 — Databricks e Genie](08_DATABRICKS_GENIE.md) | Capacidade externa, publicação única, execução humana e observabilidade |
| [09 — Papéis e handoffs](09_PAPEIS_HANDOFFS.md) | Contratos do coordenador, executores, auditores e integrador |
| [10 — Implantação](10_IMPLANTACAO.md) | Pacotes de trabalho, pilotos, entregáveis e critério de liberação |
| [11 — Riscos e bloqueios](11_RISCOS_BLOQUEIOS.md) | Questões que precisam ser resolvidas pela autoria, sem decisão improvisada local |
| [12 — Fontes](12_FONTES.md) | Proveniência, verificações realizadas e limites da leitura |
| [13 — Adendo operacional proposto](13_ADENDO_OPERACIONAL.md) | Texto pronto para formalização no repositório, sem reescrever ADR aceito |
| [14 — Checklist de prontidão](14_CHECKLIST_PRONTIDAO.md) | Contraditório final antes do primeiro disparo |
| [Codex Autonomous Controller](../../../operations/CODEX_AUTONOMOUS_PROTOCOL.md) | Orquestração autônoma entre gates sob envelope A0/A1/A2/A3 |

`catalogos/CASOS.json` é o catálogo dono dos IDs de casos e das obrigações discriminantes; as tabelas dos dossiês e do documento 05 são visualizações desse catálogo. `catalogos/COBERTURA_BASE.json` preserva o inventário de planejamento; o inventário executável por método é produzido por `tools.skill_enforcement.parallel.coverage`. `catalogos/DAG.json`, `catalogos/BLOQUEIOS.json`, `catalogos/PRONTIDAO.json` e `CONTROLE_PLANO.json` são snapshots de planejamento/B0 e declaram essa semântica nos próprios JSONs; não são state sources vivos. Para B1, use exclusivamente `B1/AUTHORING_STATE.json` como estado corrente.

## Regra operacional em uma frase

**Aqui se define a governança; o controller pode implementar, verificar, auditar e reparar dentro do envelope ativo; somente efeitos/classes explicitamente delegados podem avançar sem nova intervenção humana; promoção e integração continuam nos Human Gates.**

## O que este pacote não alega

As especificações de casos não são testes Python já implementados. Os modelos de JSON não são uma campanha liberada. A validação estrutural deste pacote não comprova qualidade de runtime, sandbox, API pública, capacidade do Free ou conformidade das skills. Os scripts futuros indicados em código monoespaçado são interfaces planejadas, salvo quando expressamente identificados como existentes na baseline.

Nenhum resultado histórico vermelho é apagado. Nenhuma narrativa de uma IA é convertida em chamada de ferramenta observada. Nenhum hash é tratado como autenticação humana. As seis skills já no target entram em regressão, sem nova promoção nesta frente.
