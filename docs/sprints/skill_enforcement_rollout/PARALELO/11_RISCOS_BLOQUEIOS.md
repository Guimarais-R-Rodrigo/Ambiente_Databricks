# 11 — Bloqueios de autoria, riscos e controle de escopo

## Estado dos blockers deste catálogo

A tabela B01–B20 é um snapshot de planejamento. B01–B08 e B20 não devem ser
reabertos apenas porque aparecem como antigos `OPEN_BEFORE_IMPLEMENTATION`.
O catálogo JSON correspondente declara `PLANNING_BLOCKER_CATALOG_NOT_LIVE_STATE`.
Para blockers atuais de B1, consulte `B1/AUTHORING_STATE.json`.

## 11.1 Regra de resolução

Os bloqueios abaixo não são pedidos para o executor local improvisar. Cada um tem owner, evidência faltante e gate impedido. A autoria resolve os técnicos; o usuário decide somente matéria que altera escopo/autoridade/efeito. Não enviar novamente a mesma pergunta se a evidência do repositório já puder resolvê-la.

Bloqueio de uma fase não impede trabalho independente: materializer pendente não impede escrever o contrato L2 da própria skill nem testar safra. Entretanto, uma liberação nominalmente L4 não pode omitir a superfície materializadora e manter a mesma claim ampla.

O catálogo dono é `catalogos/BLOQUEIOS.json`. Estados são de planejamento e permanecem abertos até a implementação/prova correspondente, não até alguém simplesmente editar o texto para “resolvido”.

| ID | Escopo e questão | Quem resolve | Evidência/ação exigida | Gate |
|---|---|---|---|---|
| B01 | GLOBAL: Formalização do adendo | Autoria B0 | Formalizar a ordem por DAG e lotes preservando gates; não reescrever ADR aceito. | B0_RELEASE |
| B02 | GLOBAL: Cobertura por método | Autoria B0 | Enumerar coleção/test IDs e classificar invariantes atuais, história e NA. | B0_RELEASE |
| B03 | GLOBAL: Schemas e launcher runtime inexistentes | Autoria B0 | Implementar interfaces e metatestes M01–M28, sem engine analítico universal. | B0_RELEASE |
| B04 | GLOBAL: Cliente/modelos/permissões | Qualificação local com roteiro repo-side | Executar probes aprovados; resolver aliases; testar bloqueio de escrita/credenciais. | LOCAL_QUALIFICATION |
| B05 | GLOBAL: Budgets | Qualificação local com roteiro repo-side | Medir recurso e congelar limites por classe antes da campanha. | LOCAL_QUALIFICATION |
| B06 | GLOBAL: Persistência probatória | Autoria B0 | Implementar verificador independente e falhas adversariais sem circularidade. | B0_RELEASE |
| B07 | GLOBAL: Interoperabilidade de verifiers | Autoria B0 | Definir contracts por produtora, rejeição de outra skill e auditoria sem self-proof. | INTEGRATED_CERTIFICATION |
| B08 | GLOBAL: Base concorrente MM/PSEF | Autoria B0 e integrador | Mapear impactos na base exata; reservar integração; sem incorporar branches por conveniência. | INTEGRATED_FREEZE |
| B09 | hub-ml-explainability: Linhas SHAP efetivas | Autoria SER02 | Controlar amostragem e provar IDs; bloquear modos não vinculáveis. | AUTHORING_READY |
| B10 | hub-ml-analise-safra: Semântica de denominador e maturidade | Autoria SER03 | Congelar escopo binário e fixtures incompletas; testar tabela independente. | AUTHORING_READY |
| B11 | hub-ml-validacao-estatistica: Catálogo estatístico | Autoria SER04 | Enumerar métodos e APIs públicas reais; p-value/efeito/IC só quando suportado e definido. | AUTHORING_READY |
| B12 | hub-ml-cross-eda-ml: Contrato temporal | Autoria SER05/06 | Validar premissas, limites/tie/timezone; bloquear fonte que exceda o contrato. | AUTHORING_READY |
| B13 | hub-ml-feature-engineering: Materialização | Autoria SER07/08 | Implementar adapter e autorização/readback; manter L4 de efeito bloqueado até prova real. | L4_RELEASE |
| B14 | hub-ml-baseline-ml: Tracking efetivo | Autoria SER09/10 | Vincular objetos reais, parâmetros/run/artefatos e testar MLflow. | L4_RELEASE |
| B15 | hub-ml-monitoramento-modelo: Ação versus recomendação | Autoria SER11/12 | Fechar escopo das ações reais; impedir completion fictício e autoridade inferida. | L4_RELEASE |
| B16 | hub-ml-pipeline-builder: Executor de deploy | Autoria SER13/14 | Escolher/implementar operação pessoal suportada; sem serviço disponível, manter bloqueio. | L4_RELEASE |
| B17 | GLOBAL: Free runtime/permissões | Autoria externa + usuário | Roteiro read-only prévio; autorizações de destinos/efeitos separadas; nada corporativo. | EXTERNAL_RELEASE |
| B18 | GLOBAL: Observabilidade Genie | Autoria externa | Definir eventos/output mínimo por caso e validar transporte antes dos chats. | EXTERNAL_RELEASE |
| B19 | GLOBAL: Promoção e merge | Autoria e usuário nos gates próprios | Recolher aceite nominal por skill/superfície/candidata e merge separado. | POLICY_PROMOTION |
| B20 | GLOBAL: Acesso de escrita do conector | Autoria repo-side | Versionar os bytes preparados quando houver ferramenta de escrita autorizada; não dizer que já foi publicado. | REPO_VERSIONING |

## 11.2 Riscos e controles preventivos

**Explosão do framework:** limitar B0 às interfaces da arquitetura; não iniciar infraestrutura distribuída. Qualquer expansão precisa de caso real e teste discriminante que demonstre insuficiência da composição existente.

**Oito agentes repetindo o mesmo trabalho:** command registry e cache de dependências preparados uma vez; escopos não sobrepostos e relatórios específicos. Testes comuns são compartilhados somente sobre a mesma candidata/ambiente no escopo correto, não por semelhança verbal.

**Falso consenso entre modelos:** auditores separados, vereditos prévios ao resumo do executor quando viável, oráculos independentes e contraditório por evidência. Concordância de duas IAs sem artefato não valida uma chamada.

**Drift de scope:** release spec e matriz de claims congelados. Mais artefatos ou helpers não autorizam scope global; não promover convert, todos os métodos SHAP, inferência causal ou deploy universal por analogia.

**Concorrência perigosa:** limites globais de agentes e recursos, clones/processos separados, leases de publicação e integração, nenhum token remoto em executor que não precisa dele. Testar edit-and-restore como violação, não apenas git status final.

**Regressão histórica omitida:** matriz de equivalência por suíte/método, invariante vigente com sucessor testado e baseline histórica preservada. Regex de nomes não é mecanismo definitivo de classificação de erro.

**Higiene documental gerando ciclo longo:** mudar documentação em um único dono; medir snapshots após composição; executar parse, links, JSON schema e teste de fase antes do laboratório. Finding F3 isolado deve ser corrigido de forma proporcional; não chamar cada detalhe editorial de defeito funcional.

**Cota/tokens:** execução determinística não depende de uma conversa longa por gate. Cada agente recebe contexto mínimo e orçamento. Se cota não observável, registrar essa limitação e limitar trabalho por tarefa; não prometer savings quantitativos não medidos.

**Efeito remoto desconhecido:** estado de efeito separado de exit code; readback autorizado; ausência de retry automático de escrita. Cleanup só sobre destinos próprios e explicitamente autorizados, sem apagar vestígio de falha.

## 11.3 Mudança do plano depois de aprovado

A revisão registra: motivo, evidência, casos afetados, deltas de scope/autoridade, impacto em código/testes, provas invalidadas e gates necessários. Correção técnica dentro do escopo vai para autoria. Mudança de target, efeito, universo, aprovação ou regra de aceite volta ao usuário.

Não criar uma sequência infinita de novas condições de aceite depois de cada rodada. A auditoria pode encontrar lacuna material legítima; ela precisa demonstrar impacto concreto. Preferências estilísticas não geram novos gates sem relação com risco. Um finding novo não permite apagar os anteriores.

## 11.4 Compromisso realista

O plano reduz classes conhecidas de retrabalho e torna lacunas visíveis antes do laboratório. Não garante ausência de bugs, evolução da plataforma ou incompatibilidade de runtime. A excelência buscada é rastreabilidade, evidência proporcional e correção causal, não promessa de zero futuras correções.
