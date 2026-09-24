# SER paralelo — plano detalhado de autoria e execução governada

**Versão 1.2 — 24/09/2026. Autoria: ChatGPT.**

O usuário aprovou a direção de execução paralela e, em 24/09/2026, autorizou a implementação do B0. Este pacote continua sendo o plano detalhado; a candidata de mecanismo está em `tools/skill_enforcement/parallel/` e seu estado vivo está em `B0/`. A existência do mecanismo não autoriza campanhas de skills, publicação, promoção de policy ou merge.

Base Git conferida: `d2988e97e7b6c5fe1fd561852e947a155c2d731b`, no repositório `Guimarais-R-Rodrigo/Ambiente_Databricks`. A SER01 está integrada nessa base. As oito frentes restantes preservam os identificadores SER02–SER14; SER15/SER16 preservam suas funções de reconciliação e fechamento.

## Próxima ação

Executar, em fail-fast, **preflight V3 → 72 metatestes B0 → coverage V3** no checkout real do SHA final. Somente se esses gates passarem, preparar o freeze e executar a qualificação local do pacote B0 conforme [B0](B0/README.md) e [plano de implantação](10_IMPLANTACAO.md). Nenhuma skill vai para o laboratório enquanto o B0 não estiver qualificado no alcance efetivamente provado e a implementação, testes, oráculos, perfis e decisões materiais da própria skill não estiverem fechados.

A corretiva V3 também adota coordenação host-wide conservadora: uma única campanha/launcher por host via lease do SO; `max_parallel` é o total de tasks simultâneas dentro da campanha e `max_auditors` é um subconjunto desse total. Aumento de concorrência, despacho por slot liberado e cache de inventory dependem de medição do piloto, não de expectativa documental.

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

`catalogos/CASOS.json` é o catálogo dono dos IDs de casos e das obrigações discriminantes; as tabelas dos dossiês e do documento 05 são visualizações desse catálogo. `catalogos/COBERTURA_BASE.json` preserva o inventário de planejamento; o inventário executável por método é produzido por `tools.skill_enforcement.parallel.coverage`. `catalogos/DAG.json` descreve dependências, não dispara agentes. `catalogos/BLOQUEIOS.json` registra as decisões e lacunas de autoria. `CONTROLE_PLANO.json` concentra o estado da transição.

## Regra operacional em uma frase

**Aqui se define e implementa; localmente se executa e audita; apenas o integrador opera arquivos/destinos compartilhados; o usuário autoriza efeitos e promoções específicas.**

## O que este pacote não alega

As especificações de casos não são testes Python já implementados. Os modelos de JSON não são uma campanha liberada. A validação estrutural deste pacote não comprova qualidade de runtime, sandbox, API pública, capacidade do Free ou conformidade das skills. Os scripts futuros indicados em código monoespaçado são interfaces planejadas, salvo quando expressamente identificados como existentes na baseline.

Nenhum resultado histórico vermelho é apagado. Nenhuma narrativa de uma IA é convertida em chamada de ferramenta observada. Nenhum hash é tratado como autenticação humana. As seis skills já no target entram em regressão, sem nova promoção nesta frente.
