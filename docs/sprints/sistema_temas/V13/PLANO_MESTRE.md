# V13 — Plano Mestre de Consolidação Operacional do Sistema de Temas

Status: **candidata de planejamento; nenhuma implementação V13 iniciada**.

Base canônica deste plano: `a6309a4d0b3a3530c52330e65ee5a18674118378`, merge da V12 na `main`.

Este documento transforma a formulação histórica “V13/V14 consolidam operação e suporte” em um contrato executável para a V13. Ele não concede autorização para mutações Databricks, não inicia V14 e não altera os contratos técnicos integrados em V00–V12.

## 1. Decisão executiva

A V13 será a sprint de **consolidação operacional** do Sistema de Temas.

O objetivo não é acrescentar novas capacidades visuais. O objetivo é fazer com que as capacidades já construídas possam ser preparadas, verificadas, transportadas, aplicadas quando autorizadas, diagnosticadas e revertidas de forma repetível, observável e documentada.

A V13 deve responder, com artefatos e testes, às perguntas operacionais que ainda dependem de conhecimento tácito:

- qual é a fonte de verdade de cada parte do Sistema de Temas;
- quais pré-requisitos devem ser verificados antes de cada operação;
- qual artefato deve ser usado em cada superfície;
- qual é a sequência segura de instalação, atualização, aplicação e rollback;
- como distinguir erro de tema, erro de consumidor, erro de pacote, erro de ambiente e falta de autorização;
- como provar que uma aplicação não alterou dados, métricas, queries, filtros ou semântica analítica;
- como preservar hashes, versão, ambiente e evidência sem versionar credencial ou PII;
- como um operador novo consegue executar o procedimento sem depender do autor do código;
- como retornar ao último estado conhecido quando uma etapa falha.

A V13 **não** declara produção pronta. Production readiness, operação sustentada de suporte, níveis de serviço, ownership final, escalonamento e encerramento de governança ficam reservados à V14.

## 2. Estado herdado da V12

A V12 foi integrada na `main` pelo PR #54. O fechamento formativo preserva explicitamente estados diferentes em vez de transformar ausência de autorização em PASS.

Estado herdado relevante para V13:

- `DOC-02`: PASS;
- `DOC-03`: PASS;
- `SEC-01`: PASS de ambiente;
- `UAT-01`: PASS da rota textual;
- `V12-AIBI-01`: PASS real de dashboard draft, dados sintéticos e rollback;
- `A11-01`: **FAIL conhecido**, rastreado na issue #57;
- `V12-LAB-01`: `BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01`: `BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02`: `BLOQUEADO_AUTORIZACAO`.

Nenhum desses estados é reinterpretado pela V13. Os três casos ambientais bloqueados podem virar ensaios operacionais V13 somente após autorização própria. O finding A11 permanece FAIL até existir correção ou decisão explícita respaldada por nova evidência.

## 3. Contratos que a V13 herda e não reabre

A V13 não é uma refatoração geral do Sistema de Temas. Ela opera sobre donos já definidos.

| Camada | Dono integrado | Regra V13 |
|---|---|---|
| papéis, estados e separação entre autoria/aprovação/publicação | V01 | reutilizar; não criar workflow paralelo |
| schema, parsing, validação e `ResolvedTheme` | V02 | fonte de verdade técnica permanece aqui |
| adaptação Plotly | V03 | consumir; não redefinir tokens |
| componentes HTML/tabelas | V04 | consumir; não criar CSS temático paralelo |
| Visual Lab, draft, comparação, sessão e histórico | V05 | reutilizar como superfície de autoria |
| assets e geração editorial | V06 | preservar hashes e derivação controlada |
| consumidores visuais adicionais | V07 | preservar separação entre cálculo e aparência |
| integração transversal com skills/padrões/Manual | V08 | preservar owners e orientação |
| transporte/kit e `theme_contract` | V09 | reutilizar; não criar segundo manifesto concorrente |
| Databricks App | V10 | tratar como superfície operacional própria |
| AI/BI | V11 | preservar a ponte fail-closed e apenas 3 bindings diretos |
| protocolo/evidência/homologação | V12 | reutilizar princípios de evidência e fail-closed |

Decisões V11 que permanecem congeladas:

- `ResolvedTheme` continua fonte configurável de verdade;
- `context="aibi"` continua reservado;
- matriz de 48 tokens permanece 3 `translated`, 23 `approximated`, 22 `unsupported`;
- somente `surface.card -> widget.background`, `palette.categorical -> visualization.categorical_palette` e `card.radius_px -> widget.corner_radius` podem ter binding direto;
- JSON nativo Databricks não é inventado;
- `dashboard_sintetico.json` continua não importável;
- `approximated` e `unsupported` não são automatizados;
- dashboard theme e workspace theme continuam separados;
- `Import theme` e `Publish` continuam gates independentes.

## 4. Princípios arquiteturais da V13

### 4.1 Sem segunda fonte de verdade

A V13 pode criar inventários, relatórios, matrizes e preflights, mas estes devem **referenciar** donos existentes. Não podem copiar schema, tokens, lista de bindings, papéis ou regras de publicação como uma nova fonte editável.

Quando uma informação puder ser derivada automaticamente de V01–V12, a preferência é derivá-la em teste/build em vez de duplicá-la manualmente.

### 4.2 Operação não é publicação

Preparar, validar, empacotar, instalar, importar, aplicar, promover e publicar são ações diferentes. Runbooks devem separar explicitamente essas transições.

Nenhum comando da V13 deve interpretar “deploy”, “apply” ou “release” como autorização implícita para `Publish`.

### 4.3 CI continua read-only

Workflows GitHub da V13 devem usar permissões mínimas, checkout sem credencial persistente e nenhuma credencial Databricks. A CI pode gerar e verificar artefatos locais; não pode instalar, publicar ou alterar workspace remoto.

### 4.4 Fail-closed

Ambiguidade, artefato stale, hash divergente, pré-requisito ausente, identidade não verificada ou autorização inexistente devem bloquear a operação.

Não haverá fallback silencioso para comportamento “provavelmente correto”.

### 4.5 Evidência não substitui autorização

A existência de um runbook ou a capacidade técnica de executar uma operação não autoriza a operação. Mutações reais continuam exigindo autorização explícita, específica e rastreável.

### 4.6 Rollback faz parte da operação

Nenhuma operação mutável será considerada operacionalmente definida se não possuir estado anterior identificável, procedimento de rollback, verificação pós-rollback e critério de abandono seguro.

### 4.7 Usuário não técnico é público de primeira classe

Cada procedimento destinado a operação humana deve informar, sem depender de conhecimento tácito:

- para quem é;
- quando usar;
- pré-requisitos verificáveis;
- o que será alterado e o que não será alterado;
- sequência exata;
- resultado esperado;
- como conferir o resultado;
- como desfazer;
- quando parar e pedir suporte.

## 5. Modelo operacional alvo

A V13 padroniza o ciclo operacional em oito estados conceituais. Esses estados descrevem uma execução; não substituem os estados de governança V01.

1. **PREPARE** — selecionar commit/tema/artefato e declarar a superfície-alvo;
2. **PREFLIGHT** — verificar integridade, compatibilidade, pré-requisitos e autorização necessária;
3. **PACKAGE** — gerar ou selecionar o artefato derivado correto;
4. **STAGE** — preparar ambiente/draft/staging sem publicação compartilhada;
5. **APPLY** — executar a mudança explicitamente autorizada;
6. **VERIFY** — executar smoke tests, invariantes e evidência;
7. **ACCEPT** — registrar resultado e decidir continuidade operacional;
8. **ROLLBACK** — restaurar estado anterior quando requerido e verificar restauração.

Cada superfície pode omitir etapas não aplicáveis, mas não pode fundi-las de forma a esconder autorização ou rollback.

## 6. Superfícies operacionais que a V13 deve cobrir

### 6.1 Núcleo notebook/Plotly/HTML

Objetivo operacional: garantir que seleção opt-in de tema e consumidores `_resolvido` possam ser verificados sem alterar dados ou defaults legados.

Preflight mínimo:

- tema válido V02;
- fingerprint conhecido;
- contexto suportado;
- consumidor explicitamente suportado;
- nenhuma alteração de dados/eixos/thresholds;
- caminho de retorno para API legada/default.

### 6.2 Visual Lab

Objetivo operacional: tornar a autoria V05 executável por procedimento repetível sem confundir preview/sessão com promoção/publicação.

A V13 deve documentar:

- launcher e presets;
- aplicação de mudanças;
- comparação Atual/Proposta;
- undo/restore;
- save/reopen;
- destino e permissões de persistência;
- recovery de sessão parcial/inválida;
- diferença entre persistir uma sessão e alterar o padrão da equipe.

`V12-LAB-01` permanece bloqueado até existir autorização específica para ensaio real.

### 6.3 Kit de transição V09

Objetivo operacional: integrar transporte ao ciclo de release sem transformar transporte em instalação.

A V13 deve reutilizar `theme_contract` e manifestos existentes para responder:

- qual commit originou o bundle;
- quais arquivos obrigatórios estão presentes;
- quais hashes precisam conferir;
- quando o artefato deve ser recusado;
- como comparar bundle atual e candidato;
- como verificar staging antes de qualquer aplicação.

### 6.4 Databricks App V10

Objetivo operacional: preparar implantação, upgrade, smoke test e rollback do App sem introduzir publicação temática ou gestão de papéis dentro da UI.

Preflight previsto:

- bundle V10 íntegro;
- `app.yaml` válido;
- recurso `theme_storage` declarado;
- storage alvo compatível com `/Volumes/`;
- identidade encaminhada disponível em produção;
- inexistência de segredos hardcoded;
- política de persistência/retention explicitada;
- ausência de ações de aprovação/publicação.

`V12-APP-01` não é herdado como PASS. Deploy real continua dependente de autorização própria.

### 6.5 AI/BI dashboard V11

Objetivo operacional: transformar o procedimento V11/V12 em runbook repetível sem ampliar o schema ou a matriz.

O runbook deve separar:

- export nativo;
- hash e revisão;
- binding local;
- import em draft;
- verificação semântica;
- Light/Dark;
- rollback;
- Publish, que permanece gate separado.

O preflight deve recusar:

- export com SHA divergente;
- JSON Pointer inexistente;
- tentativa de automatizar `approximated`/`unsupported`;
- uso de fixture sintético do projeto como arquivo nativo;
- alegação de snapshot vivo do workspace theme.

### 6.6 Workspace theme

Workspace theme não é apenas “AI/BI maior”. É superfície administrativa separada.

A V13 pode definir runbook e preflight, mas execução real requer:

- workspace de teste apropriado;
- identidade administrativa real;
- autorização específica;
- plano de snapshot/reaplicação;
- rollback;
- Publish separado quando aplicável.

`V12-AIBI-02` permanece bloqueado até essas condições existirem.

## 7. Artefatos alvo da V13

Os nomes abaixo são a arquitetura de planejamento. Durante a implementação, criar arquivo novo somente quando evitar duplicação e houver owner claro.

### 7.1 `MATRIZ_OPERACIONAL.json`

Função: inventário derivado das superfícies e suas dependências operacionais.

Não deve copiar tokens, papéis ou regras V11. Cada entrada deve referenciar o owner canônico e declarar no mínimo:

- `surface_id`;
- owner canônico;
- tipo de artefato;
- pré-requisitos;
- autorização necessária;
- ação mutável ou read-only;
- verificação pós-operação;
- estratégia de rollback;
- evidência mínima;
- estado de homologação conhecido;
- limitações abertas.

### 7.2 Preflight operacional

Uma ferramenta local V13 poderá consolidar checks existentes e produzir relatório determinístico de readiness **sem executar a operação remota**.

Propriedades obrigatórias:

- entrada explícita;
- saída estruturada;
- códigos de erro estáveis;
- nenhum acesso de rede necessário para o núcleo local;
- nenhuma credencial;
- nenhuma mutação remota;
- não reimplementar validadores existentes quando puder chamá-los;
- registrar quais checks foram executados e quais são `NOT_APPLICABLE`/`BLOCKED`;
- não promover `BLOCKED` a PASS.

### 7.3 Runbook de instalação/atualização

Deve descrever o ciclo Git → artefato → staging → aplicação autorizada → verificação.

### 7.4 Runbook de rollback

Deve ser independente do caminho feliz e conter:

- como identificar o último estado conhecido;
- bytes/hash/versão necessários;
- sequência de restauração;
- verificação pós-restauração;
- tratamento de rollback parcial;
- condições para escalar em vez de insistir.

### 7.5 Runbook de diagnóstico

Deve usar uma taxonomia mínima de falhas:

- `CONTRACT` — schema/tema/manifesto inválido;
- `ARTIFACT` — bundle/hash/conteúdo divergente;
- `COMPATIBILITY` — consumidor/contexto/capacidade incompatível;
- `AUTHORIZATION` — operação não autorizada;
- `IDENTITY` — identidade efetiva ausente ou inválida;
- `PERMISSION` — ambiente não concede a ação;
- `ENVIRONMENT` — runtime/recurso/dependência ausente;
- `SEMANTIC_DRIFT` — dados/queries/filtros/métricas alterados;
- `RENDER` — resultado visual inesperado;
- `ACCESSIBILITY` — contraste/teclado/zoom/rótulo falha;
- `ROLLBACK` — restauração não comprovada.

A mensagem para o operador deve indicar ação de recuperação sem expor segredo, PII ou conteúdo sensível.

### 7.6 Checklist de release

Um release do Sistema de Temas deve ter identidade mínima:

- commit Git;
- matriz/contratos aplicáveis;
- artefato e SHA-256;
- checks locais/CI;
- superfície-alvo;
- estado de autorização;
- rollback preparado;
- resultado de smoke test;
- evidência sanitizada.

Isso não cria um novo sistema de aprovação: papéis e transições V01 continuam valendo.

## 8. Tratamento da issue #57 / `A11-01`

O finding de acessibilidade é dívida real e precisa ser incorporado à operação, mas não autoriza ampliar a V11.

A V13 deve realizar uma decisão arquitetural explícita entre três caminhos:

1. **preflight/validação** de cores explícitas do dashboard contra fundos Light/Dark conhecidos do export real;
2. **limitação documentada**, recusando certificação quando o dashboard contém formatação não auditada;
3. **suporte futuro específico a formatação condicional**, somente se houver contrato documentado e decisão arquitetural separada.

A preferência inicial da V13 é avaliar primeiro o caminho de **preflight fail-closed**, porque corrige a lacuna operacional sem transformar `cellFormat` em token do Hub.

Regras:

- não alterar os três bindings diretos V11;
- não assumir schema global de dashboard;
- usar somente bytes/export real e caminhos revisados quando necessário;
- calcular contraste sem arredondamento oportunista;
- testar Light e Dark;
- não fechar a issue #57 apenas porque o operador “não percebeu” dificuldade;
- fechar somente com correção ou decisão operacional verificável e nova evidência.

## 9. Divisão V13 × V14

### Pertence à V13

- inventário operacional;
- preflight;
- release/install/update/rollback;
- smoke tests e invariantes;
- observabilidade técnica da operação;
- taxonomia de falhas;
- documentação do operador;
- handoff operacional formativo;
- ensaios autorizados de staging quando necessários;
- tratamento operacional da issue #57;
- preparação de evidência para decisão de readiness.

### Fica para V14

- production readiness final;
- owner operacional definitivo e substitutos;
- modelo de suporte sustentado;
- severidades/incidentes formais;
- SLA/SLO/tempo de resposta, se houver base real para defini-los;
- escalonamento e canais corporativos;
- política final de retenção/housekeeping operacional;
- gestão de custo observada em operação real;
- calendário de revisão e depreciação;
- encerramento de dívida residual aceita;
- decisão final de go-live/uso compartilhado.

A V13 não deve inventar SLA, custo ou capacidade observada que ainda não foi medida.

## 10. Plano por sprints internas

A V13 será executada em oito subfases. Cada subfase deve terminar com evidência própria e ponto de parada explícito.

### S0 — Reconciliação pós-V12 e freeze de escopo

**Objetivo:** fazer o estado documental refletir a `main` pós-V12 e congelar o contrato V13 antes de código.

Entregáveis:

- reconciliar índices vivos que ainda dizem que V12 é candidata;
- registrar V12 integrada e V13 em planejamento;
- confirmar owners V01–V12;
- listar dívidas herdadas e issues abertas;
- congelar não-escopo V13;
- decidir quais documentos são vivos e quais são evidência histórica que não deve ser reescrita.

Testes/gates:

- links locais;
- ausência de contradição entre índices vivos;
- nenhum runtime alterado;
- nenhuma modificação em `Novo_Ambiente_Simulado` sem fonte correspondente;
- validador documental verde.

Ponto de parada: aprovação explícita do plano e do escopo antes de S1.

### S1 — Inventário e contrato operacional

**Objetivo:** transformar capacidades dispersas em uma matriz única de operação sem duplicar fontes de verdade.

Entregáveis:

- `MATRIZ_OPERACIONAL.json` ou equivalente justificado;
- mapeamento superfície → owner → artefato → preflight → autorização → smoke → rollback;
- documentação de dependências entre V05/V09/V10/V11;
- estados explícitos para funcionalidades não homologadas.

Testes/gates:

- todos os owners apontam para artefatos reais;
- nenhuma duplicação manual de token/papel/binding;
- toda ação mutável declara rollback e autorização;
- mutante sem owner, sem rollback ou sem autorização falha.

### S2 — Preflight operacional unificado

**Objetivo:** criar uma porta de entrada read-only para dizer se uma operação está preparada antes de executá-la.

Entregáveis:

- ferramenta local de preflight;
- saída estruturada e legível;
- códigos de erro estáveis;
- integração por composição com validadores existentes;
- modo por superfície e modo agregado.

Testes/gates:

- tema inválido;
- hash stale;
- bundle incompleto;
- contexto incompatível;
- JSON Pointer inexistente;
- identidade/precondição ausente;
- autorização ausente;
- rollback não preparado;
- nenhum teste pode causar rede ou mutação Databricks;
- execução repetida com mesma entrada produz mesma decisão.

### S3 — Release, instalação, atualização e rollback

**Objetivo:** documentar e testar o ciclo operacional completo sem confundir transporte com ativação/publicação.

Entregáveis:

- runbook de release;
- runbook de instalação/atualização;
- runbook de rollback;
- checklist de staging;
- estratégia de identificação do “last known good”.

Testes/gates:

- release a partir de árvore limpa;
- artefato derivado reproduzível quando o contrato exigir;
- bundle adulterado recusado;
- atualização com versão incompatível recusada;
- rollback dry-run restaura bytes/estado esperado;
- falha no meio da operação não produz falso recibo de sucesso.

### S4 — Observabilidade e diagnóstico

**Objetivo:** permitir que um operador determine onde uma falha ocorreu e qual é a próxima ação segura.

Entregáveis:

- taxonomia de falhas;
- relatório sanitizado de execução;
- runbook de diagnóstico;
- checklist de evidência;
- regras de logging sem PII/segredo.

Testes/gates:

- cada classe de falha possui mutante ou fixture;
- mensagens não ecoam conteúdo sensível;
- logs distinguem `BLOCKED`, `FAIL`, `PASS` e `NOT_APPLICABLE`;
- diagnóstico não altera o ambiente;
- ausência de evidência não vira PASS.

### S5 — Compatibilidade e acessibilidade operacional

**Objetivo:** incorporar à operação verificações que a V12 mostrou não serem capturadas apenas por CI de contrato.

Entregáveis:

- decisão da issue #57;
- preflight de contraste/formatos quando suportado por evidência real;
- matriz de compatibilidade por superfície;
- limites Light/Dark/high-contrast explicitados;
- política para consumidor ou formatação fora do contrato.

Testes/gates:

- ratios sem arredondamento para aprovação;
- caso A11 histórico continua reproduzível como FAIL até correção;
- cores explícitas não viram automaticamente tokens do Hub;
- nenhuma ampliação silenciosa da V11;
- estados não exercitados não são inferidos.

### S6 — Ensaios operacionais por superfície

**Objetivo:** provar o ciclo prepare/preflight/package/stage/verify/rollback nas superfícies possíveis.

Ordem preferencial:

1. notebook/Plotly/HTML local;
2. Visual Lab local/simulado;
3. bundle V09;
4. App V10 em build/dry-run local;
5. AI/BI V11 com fixtures e export real apenas quando já disponível/autorizado;
6. ambiente Databricks real somente com autorização específica.

Testes/gates:

- invariantes de dados/semântica;
- idempotência onde aplicável;
- rollback;
- evidência sanitizada;
- nenhuma publicação implícita.

Os casos `V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` podem ser reexecutados como ensaio real nesta fase **somente** com autorização nova e específica.

### S7 — Handoff operacional e fechamento V13

**Objetivo:** provar que o sistema é operável por outra pessoa e preparar a entrada da V14.

Entregáveis:

- guia “comece aqui” do operador;
- roteiro de primeira operação;
- matriz de decisão “o que fazer quando...”;
- registro dos ensaios;
- lista de dívidas transferidas à V14;
- checkpoint V13;
- plano de rollback do próprio release V13.

Homologação humana mínima:

- participante autorizado que não tenha construído o procedimento;
- tarefa realista com dados/artefatos sintéticos ou sanitizados;
- duração observada quando aplicável;
- ajuda recebida registrada;
- erros de interpretação registrados;
- nenhuma inferência estatística a partir de amostra formativa.

Critério final: um operador deve conseguir identificar o runbook correto, executar preflight, interpretar bloqueio/falha, verificar o resultado e localizar rollback sem instrução verbal do autor.

## 11. Estratégia de testes da V13

A V13 deve combinar cinco classes de prova e mantê-las distintas.

### 11.1 Contrato/local

- unit tests;
- schemas e matrizes;
- mutantes negativos;
- determinismo;
- hashes;
- links/documentação;
- source/simulado quando aplicável.

### 11.2 Artefato

- build reproduzível;
- presença única;
- SHA-256;
- manifesto;
- conteúdo inesperado;
- artefato stale;
- rollback package.

### 11.3 Smoke operacional

- aplicação em staging/draft/local conforme superfície;
- preservação de dados e semântica;
- verificação de estado;
- rollback.

### 11.4 Ambiente Databricks

Somente quando autorizado:

- identidade real;
- permissão efetiva;
- recurso real;
- dados sintéticos;
- evidência sanitizada;
- rollback verificado.

### 11.5 Humano

- operador autorizado;
- procedimento sem ajuda inicial;
- interpretação correta de `BLOCKED`/`FAIL`/`PASS`;
- capacidade de localizar rollback;
- nenhuma PII versionada.

CI nunca substitui 11.4 ou 11.5.

## 12. Matriz mínima de negativos obrigatórios

A V13 não será aceita apenas com caminho feliz. No mínimo, os seguintes casos precisam falhar fechados ou bloquear explicitamente:

- commit/artefato divergente;
- hash inválido;
- bundle incompleto;
- schema inválido;
- contexto não suportado;
- consumidor sem suporte;
- operação mutável sem autorização;
- identidade não comprovada quando necessária;
- permissão ausente;
- storage inválido;
- export AI/BI não revisado;
- JSON Pointer inexistente;
- tentativa de automatizar `approximated`/`unsupported`;
- drift semântico;
- contraste abaixo do limite;
- rollback não preparado;
- rollback divergente;
- log contendo material sensível;
- documentação apontando para passo inexistente;
- operação real confundida com publicação.

## 13. Workflow e governança Git

A V13 deve usar branch própria e PR draft até o gate de aceite.

Regras:

- nunca desenvolver diretamente em `main`;
- reconciliar `main` aditivamente se ela avançar;
- sem rebase/force em histórico já publicado;
- preservar failures intermediários relevantes;
- CI do SHA exato antes de aceite;
- auditoria pós-merge;
- `CHANGELOG.md` só entra quando a concorrência documental estiver reconciliada;
- nenhuma atualização documental deve alegar CI de um SHA que ainda não executou.

O workflow V13 deve:

- `contents: read`;
- `persist-credentials: false`;
- sem secrets Databricks;
- sem SDK/REST/CLI remoto para alteração;
- executar suíte V13, regressões, V00 e validador;
- verificar escopo da candidata;
- verificar ausência de PII/credenciais/caminhos corporativos na evidência.

## 14. Fronteiras de autorização

O plano não concede nenhuma das autorizações abaixo.

| Operação | Estado após este plano |
|---|---|
| testes Git/local e geração de artefato offline | permitidos pela execução normal do projeto |
| leitura/observação sem mutação quando já disponível | depende do acesso da ferramenta/sessão; não implica mutação |
| mutação real do Visual Lab/persistência no workspace | requer autorização específica |
| deploy/upgrade/rollback de Databricks App | requer autorização específica |
| alteração de ACL/grupos/permissões | requer autorização específica |
| workspace theme | requer autorização específica e identidade administrativa real |
| import em dashboard real | requer autorização específica |
| Publish | sempre gate separado |
| produção | fora do aceite V13 |

Autorizações são escopadas; uma autorização para um ensaio não vira autorização permanente.

## 15. Métricas e evidência

A V13 não inventará metas numéricas sem baseline.

Métricas que podem ser **observadas** e registradas:

- tempo de preflight;
- tempo de geração de artefato;
- duração de smoke test;
- duração de rollback;
- tamanho/hashes de artefatos;
- número de checks executados/bloqueados;
- número de passos manuais;
- ajuda necessária em UAT operacional;
- falhas por categoria.

Percentis, SLA/SLO, custo monetário ou throughput só podem ser declarados quando houver amostra e contexto suficientes. Esses temas pertencem principalmente à V14.

## 16. Riscos principais e mitigação

### R1 — V13 virar nova engine

Mitigação: todas as entradas da matriz operacional referenciam owners V01–V12; teste impede duplicação de contrato.

### R2 — runbook esconder autorização

Mitigação: autorização é campo obrigatório para toda ação mutável e ausência gera `BLOCKED_AUTHORIZATION`.

### R3 — documentação divergir do runtime

Mitigação: comandos e caminhos documentados precisam ser exercitados/validados; links e nomes fazem parte do CI.

### R4 — rollback existir apenas no papel

Mitigação: cada superfície mutável exige dry-run ou evidência real quando autorizada; rollback não comprovado impede status operacional.

### R5 — observabilidade vazar PII/segredo

Mitigação: logs sanitizados, aliases, hashes e mutantes negativos de higiene.

### R6 — V13 absorver V14

Mitigação: suporte sustentado, SLA/SLO, production readiness e ownership final ficam explicitamente fora.

### R7 — issue #57 ser “corrigida” violando V11

Mitigação: primeiro preflight/decisão operacional; qualquer suporte novo a `cellFormat` exige decisão arquitetural própria.

### R8 — ensaios ambientais virarem pré-requisito informal para merge

Mitigação: separar claramente Git/local, ambiente e humano; bloqueio honesto continua válido quando a operação não foi autorizada.

## 17. Critérios de aceite da V13

A V13 só poderá ser apresentada para aceite quando, no mesmo head candidato:

1. índices vivos estiverem reconciliados com V12 integrada;
2. owners V01–V12 estiverem preservados;
3. inventário operacional estiver completo e sem fonte paralela;
4. preflight read-only cobrir todas as superfícies declaradas;
5. release/install/update/rollback estiverem documentados e testáveis;
6. diagnóstico produzir classes de falha e próxima ação sem material sensível;
7. issue #57 tiver decisão operacional explícita e evidência compatível com seu estado;
8. negativos obrigatórios falharem fechados;
9. artefatos/staging locais tiverem smoke e rollback comprovados;
10. qualquer ensaio Databricks real executado tiver autorização, evidência e rollback próprios;
11. nenhum caso bloqueado tiver sido promovido a PASS por inferência;
12. UAT operacional por pessoa autorizada estiver registrada;
13. suíte V13 passar sem SKIP que esconda dependência obrigatória;
14. regressões V01–V13 passarem;
15. V00 passar;
16. validador estrutural/documental passar;
17. workflow V13 permanecer read-only;
18. fonte/simulado permanecerem coerentes quando arquivos de produto forem alterados;
19. PR estiver reconciliada com a `main` vigente e mergeável;
20. usuário der aceite explícito conhecendo dívidas transferidas à V14;
21. pós-merge da `main` for auditado antes de iniciar V14.

## 18. Definição de pronto por subfase

Cada subfase V13 precisa produzir:

- escopo executado;
- arquivos alterados;
- testes executados com contagem real;
- failures intermediários preservados quando relevantes;
- métricas medidas, não estimadas;
- limites e bloqueios;
- decisão de avançar/parar;
- nenhum claim além da evidência.

Não é permitido acumular toda a validação para o final.

## 19. Ordem de execução recomendada

Sequência canônica:

`S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → aceite → merge → auditoria pós-merge → V14`

Se uma subfase revelar que o contrato precisa mudar, parar, registrar a decisão e revisar o plano antes de continuar. Não “compensar” arquitetura fraca com mais documentação no final.

## 20. Primeiro ponto de decisão após aprovação deste plano

Após este plano ser revisado e aceito, a primeira implementação da V13 deve ser **S0 — reconciliação pós-V12 e freeze de escopo**.

Nenhum código V13, mutação Databricks ou execução dos três casos ambientais bloqueados deve começar antes desse aceite.

## 21. Referências canônicas

- [V05 — Visual Lab](../V05/README.md)
- [V08 — integração transversal](../V08/README.md)
- [V09 — transporte/kit](../V09/README.md)
- [V10 — Databricks App](../V10/README.md)
- [V11 — AI/BI](../V11/README.md)
- [V12 — homologação](../V12/README.md)
- [V12 — escopo e aceite](../V12/ESCOPO_E_ACEITE.md)
- Issue #57 — `A11-01`, contraste insuficiente de formatação condicional

Este documento é o plano canônico da V13 enquanto estiver em revisão. Após aceite, alterações de escopo precisam ser registradas explicitamente; implementação não pode redefinir silenciosamente o plano que a autorizou.
