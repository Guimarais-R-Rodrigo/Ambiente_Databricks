# V14 — Plano Mestre de Production Readiness e Operação Sustentada do Sistema de Temas

Status: **candidata de planejamento; nenhuma implementação S0–S8 iniciada**.

Data de abertura do planejamento: 16/09/2026.

Base canônica inicial deste plano: `99161fdeb9253c30a82243644ba89af8cd50d79e`, fechamento documental pós-merge da V13/PR #67 na `main`.

Este documento transforma a fronteira explicitamente reservada pela V13 em um contrato executável para a V14. Ele não concede autorização para mutações Databricks, não transforma evidência formativa em production readiness, não cria SLA/SLO sem base observada e não altera silenciosamente contratos V01–V13.

## 1. Decisão executiva

A V14 será a etapa de **production readiness, operação sustentada e decisão final de go-live** do Sistema de Temas.

A V13 comprovou que o sistema possui owners técnicos, preflight, release/rollback local, diagnóstico, compatibilidade/acessibilidade operacional, ensaios locais/simulados e handoff formativo. A V14 não deve duplicar essas capacidades nem criar uma segunda engine. Seu papel é responder, com evidência rastreável, se o sistema pode ser sustentado de maneira responsável em uso compartilhado e sob quais condições.

A V14 deve responder, sem inferência ou marketing operacional, às perguntas finais:

- quem responde operacionalmente pelo Sistema de Temas e quem substitui o owner principal;
- quais decisões cada papel pode tomar e quais exigem autorização externa;
- como incidentes são classificados, registrados, escalados e encerrados;
- quais sinais realmente podem ser medidos e com que confiabilidade;
- quando existe base suficiente para propor SLI/SLO e, separadamente, SLA;
- quais custos são observados, estimados ou ainda desconhecidos;
- quais artefatos/evidências devem ser retidos, limpos, revisados ou depreciados;
- quais superfícies estão prontas, bloqueadas, falhando ou não aplicáveis;
- quais dívidas residuais são impeditivas e quais podem ser aceitas formalmente;
- se existe evidência suficiente para uma decisão final `GO`, `NO_GO` ou `BLOCKED`;
- se uma decisão `GO` exigir mutação remota, qual autorização específica ainda será necessária para executá-la.

**A V14 não significa go-live automático.** A decisão final é um gate. Qualquer ação remota que materialize o go-live continua sujeita a autorização explícita, identidade/permissão efetiva, rollback e evidência do ambiente-alvo.

## 2. Estado herdado da V13

A V13 está encerrada no Git. A PR #67 foi integrada no merge `99161fdeb9253c30a82243644ba89af8cd50d79e`, após fechamento funcional S7/PR #66 e auditoria pós-merge.

A V14 herda como fatos separados:

- V13 S1–S7 concluídas no alcance documentado;
- regressões V01–V13 certificadas no fechamento V13;
- `HUMAN-01 = PASS` somente como evidência formativa de handoff;
- nenhuma mutação Databricks executada pela V13;
- `DOC-02 = PASS` no alcance documentado;
- `DOC-03 = PASS` no alcance documentado;
- `SEC-01 = PASS` somente no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 já evidenciado;
- `A11-01 = FAIL`, issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

Nenhum desses estados é promovido automaticamente pela abertura da V14.

Uma sessão humana formativa não produz, por si só:

- capacidade operacional estatística;
- disponibilidade;
- tempo de resposta;
- SLA;
- SLO;
- custo observado de produção;
- suporte sustentado;
- production readiness;
- autorização Databricks;
- go-live.

## 3. Contratos herdados e congelados

A V14 é uma camada de readiness/governança operacional sobre owners existentes. Ela não reabre as fontes de verdade funcionais.

| Camada | Owner integrado | Regra V14 |
|---|---|---|
| papéis e transições de governança | V01 | referenciar; não criar workflow concorrente |
| schema, parsing, validação e `ResolvedTheme` | V02 | permanece fonte técnica de verdade |
| consumidores Plotly/HTML/visuais | V03/V04/V07 | medir readiness sem reimplementar aparência |
| Visual Lab | V05 | avaliar operação/ambiente sem criar segunda autoria |
| assets e derivação | V06 | preservar lineage e hashes |
| integração transversal | V08 | preservar owners e documentação vigente |
| transporte e `theme_contract` | V09 | reutilizar identidade do artefato |
| Databricks App | V10 | tratar como superfície própria de readiness |
| AI/BI e workspace theme | V11 | preservar fronteiras e bindings congelados |
| homologação/evidência | V12 | reutilizar fail-closed e classes de evidência |
| operação/preflight/release/diagnóstico/handoff | V13 | reutilizar; não criar segunda engine operacional |

Contratos V11 continuam congelados:

- `ResolvedTheme` permanece fonte configurável de verdade;
- `context="aibi"` continua reservado;
- 48 tokens permanecem 3 `translated`, 23 `approximated`, 22 `unsupported`;
- somente três bindings diretos permanecem autorizados;
- `dashboard_sintetico.json` não é import nativo;
- `cellFormat` não vira token;
- `approximated`/`unsupported` não são automatizados;
- dashboard theme é distinto de workspace theme;
- `Import theme` é distinto de `Publish`.

## 4. Princípios arquiteturais da V14

### 4.1 Readiness não é feature

A V14 não deve criar novas capacidades visuais para conseguir um `GO`. Lacuna funcional relevante deve aparecer como dívida, bloqueio ou nova iniciativa, não como expansão silenciosa de escopo.

### 4.2 Evidência por classe e alcance

Toda afirmação de readiness deve declarar:

- superfície;
- ambiente;
- owner da evidência;
- data/versão/commit aplicável;
- classe da evidência;
- o que foi observado;
- o que não foi observado;
- validade/expiração quando aplicável.

PASS local não é PASS remoto. PASS de uma superfície não é PASS global.

### 4.3 Fail-closed

Ausência de autorização, owner, canal, rollback, métrica confiável, identidade efetiva, evidência ambiental ou decisão humana exigida deve resultar em `BLOCKED`/`FAIL` conforme o contrato aplicável, nunca em PASS presumido.

### 4.4 Não inventar SLA/SLO

SLI pode ser definido como medida antes de existir meta. SLO só pode ser proposto quando houver base observada suficiente para justificar a meta. SLA, por envolver compromisso formal, exige ainda owner/autoridade competente e aprovação própria.

A V14 deve permitir explicitamente o resultado:

`SLA/SLO = BLOCKED — BASELINE_INSUFFICIENT`

sem tratar isso como falha do projeto quando a ausência de base for a conclusão honesta.

### 4.5 Custos observados separados de estimativas

Todo valor deve ser classificado como:

- `OBSERVED` — medido em fonte identificada;
- `ESTIMATED` — cálculo explícito com premissas;
- `UNKNOWN` — ainda não sustentado por evidência.

Estimativa nunca deve ser apresentada como custo real.

### 4.6 Go-live é decisão, não efeito colateral

Nenhum merge, workflow, teste ou PASS humano ativa uso compartilhado por inferência.

A decisão final deve ser uma destas:

- `GO` — readiness suficiente no escopo definido;
- `NO_GO` — existe impedimento material conhecido;
- `BLOCKED` — faltam autorizações/evidências externas necessárias para decidir.

Mesmo `GO` não substitui autorização específica para uma mutação remota.

### 4.7 CI continua read-only

A CI V14 deve operar sem credenciais Databricks, com `contents: read`, checkout sem credencial persistente e sem mutação remota. Ela pode validar contratos, matrizes, evidência versionada e consistência documental, mas não pode fabricar observações do ambiente.

### 4.8 Operador não técnico continua público de primeira classe

Toda rotina destinada a operação humana deve explicar:

- objetivo;
- pré-requisitos;
- owner;
- quando usar;
- o que pode alterar;
- como verificar;
- como interromper;
- como escalar;
- como desfazer;
- como registrar evidência sem PII/segredo.

## 5. Modelo de readiness alvo

A V14 organizará readiness por dimensões independentes. Nenhuma dimensão pode ser escondida por um PASS agregado.

Dimensões mínimas:

1. **TECHNICAL** — contratos, testes, integridade, compatibilidade e rollback;
2. **ENVIRONMENT** — runtime/recursos/identidade/permissão observados;
3. **SECURITY_PRIVACY** — segredo, PII, least privilege e evidência sanitizada;
4. **ACCESSIBILITY** — contraste e demais oráculos aplicáveis no alcance observado;
5. **OPERATIONS** — runbooks, ownership, handoff, recovery e suporte;
6. **INCIDENT_MANAGEMENT** — severidade, triagem, escalonamento e encerramento;
7. **SERVICE_MEASUREMENT** — SLIs, baseline e eventual SLO/SLA;
8. **COST_CAPACITY** — custo, limites e capacidade observados/estimados;
9. **LIFECYCLE** — retenção, housekeeping, revisão e depreciação;
10. **GOVERNANCE** — autorização, aceite de risco e decisão de go-live.

Cada dimensão deve manter os estados operacionais já conhecidos quando aplicáveis:

- `PASS`;
- `BLOCKED`;
- `FAIL`;
- `NOT_APPLICABLE`.

A decisão final `GO/NO_GO/BLOCKED` é um gate de governança e não substitui esses estados de evidência.

## 6. Superfícies que a V14 deve avaliar

A V14 deve manter as seis superfícies operacionais inventariadas na V13:

1. `notebook_visual_core`;
2. `visual_lab`;
3. `transition_bundle`;
4. `databricks_app`;
5. `aibi_dashboard`;
6. `workspace_theme`.

Para cada superfície, a V14 deve responder:

- owner primário e substituto;
- ações suportadas;
- ambiente observado;
- autorização necessária;
- rollback aplicável;
- sinais/SLIs mensuráveis;
- evidência disponível;
- dívida aberta;
- custo/capacidade observável;
- retenção/housekeeping aplicável;
- estado final de readiness por dimensão.

Nenhuma superfície bloqueada deve desaparecer do relatório agregado.

## 7. Artefatos alvo da V14

Os nomes abaixo são arquitetura de planejamento. Durante a implementação, arquivo novo deve existir somente quando possuir owner claro e evitar duplicação.

### 7.1 `MATRIZ_READINESS.json`

Inventário estruturado por superfície/dimensão, referenciando V01–V13 sem copiar seus contratos.

Campos mínimos previstos:

- `surface_id`;
- `dimension_id`;
- `owner_ref`;
- `backup_owner_ref` quando evidenciado;
- `evidence_refs`;
- `status`;
- `reason_code`;
- `authorization_required`;
- `environment_scope`;
- `expires_or_review_at` quando aplicável;
- `residual_risk_ref` quando aplicável.

### 7.2 Modelo de ownership e autoridade operacional

Documento/matriz que distinga pelo menos:

- owner técnico;
- owner operacional;
- substituto;
- aprovador de mudança;
- responsável por incidente;
- autoridade de go-live;
- autoridade para aceitar risco residual.

Nomes, grupos ou canais corporativos não serão inventados. Se não houver evidência, o campo permanece bloqueado/pendente.

### 7.3 Catálogo de incidentes e severidade

Deve definir critérios objetivos de severidade sem inventar tempos de atendimento.

Categorias mínimas:

- indisponibilidade/incapacidade de operar;
- regressão funcional/contratual;
- semantic drift;
- corrupção/integridade de artefato;
- falha de rollback;
- segurança/privacidade;
- acessibilidade;
- custo/capacidade anômala;
- falha de autorização/identidade;
- documentação/runbook incorreto.

### 7.4 Registro de SLIs e baseline

Deve distinguir:

- métrica definida;
- fonte da medição;
- janela de observação;
- amostra;
- limitações;
- baseline observado;
- meta proposta, se justificável;
- status de elegibilidade para SLO/SLA.

### 7.5 Registro de custos e capacidade

Deve separar observação, estimativa e desconhecido, com premissas e fonte.

### 7.6 Política de retenção/housekeeping

Deve classificar:

- evidências versionadas;
- artefatos temporários;
- logs sanitizados;
- bundles/releases;
- LKG/rollback;
- sessões/drafts quando aplicável;
- dados ou metadados que não devem ser versionados.

### 7.7 Calendário de revisão/depreciação

Deve definir gatilhos de revisão sem inventar cadência quando owner/necessidade real ainda não estiver evidenciada.

### 7.8 `PACOTE_DECISAO_GO_LIVE.md`

Pacote final de evidência e decisão, contendo:

- escopo da decisão;
- baseline Git;
- matriz de readiness;
- owners/autoridades;
- incidentes e suporte;
- SLI/SLO/SLA e respectivas limitações;
- custo/capacidade;
- lifecycle;
- dívidas e riscos residuais;
- autorizações pendentes;
- decisão `GO`, `NO_GO` ou `BLOCKED`;
- condições para reversão/revisão da decisão.

## 8. Tratamento obrigatório das dívidas herdadas

### 8.1 `A11-01` / issue #57

Permanece `FAIL` até existir correção/decisão respaldada por nova evidência aplicável.

A V14 não pode:

- fechar #57 por conveniência de go-live;
- ampliar V11 silenciosamente;
- transformar `cellFormat` em token;
- ignorar Light/Dark observado;
- usar ausência de reclamação humana para substituir contraste objetivo.

O resultado de readiness pode permanecer `FAIL` ou exigir aceite formal de risco somente se a governança aplicável permitir e se isso não violar requisito obrigatório. Aceite de risco não reescreve o fato histórico `A11-01 = FAIL`.

### 8.2 `V12-LAB-01`

Permanece `BLOQUEADO_AUTORIZACAO` até existir autorização e ambiente reais para a evidência exigida.

### 8.3 `V12-APP-01`

Permanece `BLOQUEADO_AUTORIZACAO` até autorização própria para deploy/ambiente real.

### 8.4 `V12-AIBI-02`

Permanece `BLOQUEADO_AUTORIZACAO` para workspace theme/admin/snapshot/reaplicação até autorização, identidade, ambiente e rollback reais.

### 8.5 Estados não observados

Light/Dark/high-contrast, browser, concorrência, capacidade ou outras dimensões não exercitadas permanecem explicitamente não evidenciadas. Não inferir PASS.

## 9. Fronteiras com outras iniciativas concorrentes

A V14 pertence exclusivamente ao Sistema de Temas.

Na abertura deste plano existem frentes paralelas no mesmo repositório, incluindo:

- PR #69 — Skill Enforcement / SE01;
- PR #51 — Micromodelos / MM01;
- PRs históricas abertas #26, #6, #5 e #4.

Regras de concorrência:

- nenhuma mudança dessas frentes será incorporada silenciosamente;
- se `main` avançar, a branch V14 deve ser reconciliada aditivamente antes de qualquer merge;
- não usar force-push/reset para esconder concorrência;
- sobreposição em `README.md`, índices ou workflows deve ser tratada semanticamente;
- V14 não deve modificar contratos de Skill Enforcement ou Micromodelos para satisfazer seus próprios gates;
- métricas do README devem sempre vir do runner sobre a árvore efetiva após reconciliação.

## 10. Plano por sprints internas

A V14 será executada em checkpoints separados. Nenhuma sub-sprint autoriza automaticamente a próxima.

### S0 — Reconciliação pós-V13 e freeze de readiness

Objetivo:

- confirmar o fechamento real da V13;
- classificar documentação viva versus evidência histórica;
- congelar o escopo V14;
- inventariar dívidas, bloqueios e concorrência;
- criar a superfície viva V14;
- definir CI V14 read-only;
- confirmar que nenhuma afirmação de production readiness já existe sem evidência.

Entregáveis previstos:

- `V14/README.md`;
- `V14/CHECKPOINT_S0.md`;
- guarda/CI V14 inicial;
- atualização mínima de índices vivos.

Testes obrigatórios:

- main/merge-base/ahead/behind;
- estados V12/V13 preservados;
- #57 aberta;
- três bloqueios preservados;
- zero mutação Databricks;
- V01–V13 regressões aplicáveis verdes;
- nenhuma duplicação de owner/schema/token/binding.

### S1 — Ownership, autoridade e modelo operacional

Objetivo:

- transformar owner técnico/handoff em responsabilidade operacional explícita;
- definir substituição, aprovação e autoridade de risco/go-live sem inventar pessoas/canais.

Entregáveis previstos:

- matriz de ownership/autoridade;
- runbook de responsabilidade e escalonamento;
- negativos para owner ausente, self-approval indevido e autoridade inventada.

Gate:

- owner/backup/autoridade não evidenciados devem permanecer `BLOCKED`.

### S2 — Matriz de production readiness e evidência

Objetivo:

- implementar `MATRIZ_READINESS.json` e validação fail-closed;
- mapear as seis superfícies às dez dimensões de readiness.

Entregáveis previstos:

- matriz estruturada;
- schema/validador local;
- suíte de mutantes;
- documentação de interpretação.

Negativos obrigatórios:

- PASS agregado escondendo FAIL/BLOCKED;
- referência de evidência inexistente;
- owner inexistente;
- estado inválido;
- tentativa de copiar contrato V11/V13;
- promoção local→remoto sem evidência.

### S3 — Suporte sustentado, incidentes e escalonamento

Objetivo:

- formalizar triagem, severidade, comunicação, investigação, mitigação, rollback e encerramento.

Entregáveis previstos:

- catálogo de incidentes;
- matriz severidade × impacto;
- runbook de incidente;
- modelo sanitizado de registro/postmortem;
- critérios de escalonamento.

Regra:

- severidade pode ser definida por impacto; tempo de resposta/SLA não deve ser inventado.

### S4 — SLIs, baseline, SLO e fronteira de SLA

Objetivo:

- definir o que é mensurável;
- registrar baseline real quando disponível;
- decidir se existe base para SLO;
- manter SLA bloqueado sem autoridade/contrato apropriado.

Entregáveis previstos:

- catálogo de SLIs;
- ledger de observações;
- critérios de suficiência de baseline;
- decisão explícita por métrica: `eligible`, `insufficient_baseline`, `not_applicable`.

Negativos obrigatórios:

- meta inventada;
- percentil sem amostra;
- disponibilidade sem janela/fonte;
- SLA derivado automaticamente de SLO;
- uma sessão humana usada como distribuição estatística.

### S5 — Custos, capacidade, retenção e lifecycle

Objetivo:

- separar custo observado/estimado/desconhecido;
- definir housekeeping e retenção por classe de artefato;
- definir revisão/depreciação e critérios de capacidade.

Entregáveis previstos:

- ledger de custos/capacidade;
- política de retenção/housekeeping;
- calendário/gatilhos de revisão;
- runbook de depreciação.

Negativos obrigatórios:

- estimativa tratada como observado;
- remoção sem preservar LKG/rollback necessário;
- retenção de PII/segredo em evidência;
- prazo de retenção inventado sem owner/regra.

### S6 — Readiness por superfície e tratamento de dívida residual

Objetivo:

- aplicar a matriz às seis superfícies;
- confrontar #57 e bloqueios reais;
- produzir mapa de impedimentos para go-live.

Entregáveis previstos:

- relatório por superfície/dimensão;
- residual risk register;
- classificação de cada dívida como impeditiva, aceitável mediante autoridade, ou não aplicável.

Regras:

- `A11-01 = FAIL` continua histórico mesmo se risco for aceito;
- `BLOQUEADO_AUTORIZACAO` só muda com evidência/autorização própria;
- não executar Databricks por inferência a partir do aceite da sprint.

### S7 — Ensaios de operação sustentada e handoff de produção

Objetivo:

- executar tabletop/read-only/local e, apenas quando explicitamente autorizado, ensaios ambientais delimitados;
- provar que owner/substituto conseguem usar suporte, incidente, rollback e evidência.

Cenários mínimos:

- incidente funcional/contratual;
- autorização ausente;
- rollback necessário;
- evidência insuficiente;
- custo/capacidade desconhecido;
- dívida #57;
- indisponibilidade ou bloqueio de uma superfície.

A evidência humana deve permanecer sanitizada e não pode ser fabricada pelo CI.

### S8 — Pacote final e decisão de go-live

Objetivo:

- consolidar a evidência sem esconder divergências;
- executar revisão final de readiness;
- produzir `PACOTE_DECISAO_GO_LIVE.md`;
- registrar `GO`, `NO_GO` ou `BLOCKED` com justificativa rastreável.

Critérios mínimos para `GO`:

- escopo do go-live explicitamente definido;
- owners/autoridades aplicáveis evidenciados;
- nenhum FAIL impeditivo sem tratamento permitido;
- bloqueios externos relevantes resolvidos ou escopo explicitamente excluído de maneira legítima;
- rollback/recovery aplicável;
- suporte/incidente operacionalizado;
- custo/lifecycle classificados;
- evidence gaps não mascarados;
- autorização final humana registrada.

`GO` não executa automaticamente uma mutação Databricks. Se o go-live exigir deploy, Publish, workspace theme, ACL, Volume ou outra alteração remota, haverá gate explícito de autorização para a execução.

## 11. Estratégia de testes e CI

A V14 deve introduzir CI própria a partir da S0, sem remover ou relaxar regressões V00–V13.

### 11.1 Ordem de validação prevista

1. testes específicos da sub-sprint V14;
2. validador/mutantes V14;
3. regressões V01–V14 aplicáveis;
4. V00;
5. `validate_assistant.py --conferir-readme`;
6. guardas de fronteira/read-only;
7. escopo/higiene V14.

### 11.2 Negativos transversais

A CI deve falhar quando houver:

- PASS inferido de ausência de evidência;
- SLA/SLO sem base/autoridade correspondente;
- custo observado sem fonte;
- owner/canal inventado;
- fechamento de #57 sem nova evidência;
- promoção de bloqueio por autorização sem prova;
- mutação Databricks na CI;
- segredo/PII em evidência;
- segunda fonte de verdade de tokens/schema/bindings;
- alteração funcional fora do escopo da sub-sprint;
- métricas README stale.

### 11.3 Evidence classes

A V14 deve distinguir no mínimo:

- `GIT_CI`;
- `LOCAL_SIMULATED`;
- `HUMAN_FORMATIVE`;
- `ENVIRONMENT_OBSERVED`;
- `AUTHORIZATION`;
- `COST_OBSERVED`;
- `SERVICE_OBSERVED`.

Uma classe não substitui outra.

## 12. Operações Databricks e autorização

O Plano Mestre não concede autorização para:

- deploy de Databricks App;
- alteração de ACL/grupos;
- criação/alteração de UC Volume;
- workspace theme;
- `Import theme` remoto;
- `Publish`;
- edição de dashboard real;
- persistência em workspace;
- execução de go-live remoto;
- qualquer outra mutação Databricks.

Quando uma sub-sprint precisar de evidência ambiental que exija mutação, ela deve:

1. chegar ao checkpoint técnico anterior;
2. declarar exatamente a operação pretendida;
3. declarar ambiente/superfície;
4. declarar rollback;
5. pedir autorização específica;
6. executar somente depois do aceite explícito;
7. registrar a evidência sanitizada;
8. recertificar Git/CI separadamente.

## 13. Documentação para usuário não técnico

Cada sub-sprint deve manter uma rota operacional legível por alguém que nunca entrou no Hub.

O mínimo para qualquer procedimento humano:

- “o que é”;
- “quando usar”;
- “quem pode usar”;
- “antes de começar”;
- “passo a passo”;
- “resultado esperado”;
- “como saber se falhou”;
- “quando parar”;
- “como desfazer”;
- “quem/como escalar”, somente quando o canal estiver evidenciado.

Não usar jargão sem explicação quando ele representar decisão operacional.

## 14. Concorrência Git e disciplina de integração

Para cada sub-sprint:

- criar branch própria a partir da `main` certificada;
- abrir PR Draft;
- preservar failures intermediários;
- usar o runner como fonte de métricas verificáveis;
- não relaxar gate para produzir verde;
- não rebasear/resetar para apagar concorrência;
- se `main` avançar, reconciliar aditivamente;
- certificar o SHA exato final;
- exigir aceite explícito antes do merge;
- certificar todos os workflows de `push` após o merge;
- somente então considerar a próxima sub-sprint elegível para abertura.

## 15. Critérios de aceite do Plano Mestre V14

Este plano está apto para aceite apenas se:

- refletir exatamente a fronteira V13→V14 já registrada;
- preservar V01–V13 como owners canônicos;
- manter #57 e os três bloqueios honestos;
- não inventar SLA/SLO/custos/canais/owners;
- separar decisão de go-live de execução remota;
- incluir estratégia de testes, negativos, evidência e rollback;
- tratar concorrência com SE01/MM01;
- não executar mutação Databricks;
- manter S0–S8 não iniciadas até integração/aceite deste plano.

## 16. Semântica do aceite solicitado

O aceite deste Plano Mestre autorizará somente:

1. integrar a PR de planejamento depois da certificação final;
2. abrir **V14 — S0: reconciliação pós-V13 e freeze de readiness** em branch/PR separada.

O aceite do plano **não** autorizará:

- iniciar S1 automaticamente;
- executar Databricks;
- fechar #57;
- transformar `BLOQUEADO_AUTORIZACAO` em PASS;
- definir SLA/SLO sem baseline;
- aceitar risco residual;
- declarar production readiness;
- decidir `GO`;
- executar go-live.

Cada transição S0→S8 manterá checkpoint e aceite próprios.

## 17. Estado ao final desta PR de planejamento

Enquanto esta candidata não estiver integrada:

- V13 permanece a última versão operacional integrada do Sistema de Temas;
- V14 possui somente uma candidata de planejamento;
- S0–S8 permanecem não iniciadas;
- #57 permanece aberta;
- os três bloqueios V12 permanecem bloqueados;
- nenhuma mutação Databricks é executada;
- nenhuma decisão de production readiness/go-live é tomada.
