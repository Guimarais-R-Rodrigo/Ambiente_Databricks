# Changelog

Marcos relevantes para usar e manter o Hub. Decisões e limites atuais pertencem aos owners abaixo; resultados antigos continuam válidos apenas para o SHA, ambiente e escopo registrados.

- Direção e decisões: [índice de ADRs](docs/decisions/README.md).
- Armadilhas recorrentes: [classes de defeito e guardas](docs/auditoria/README.md#classes-de-defeito-que-viraram-guardas).
- Estado por frente: [owners vivos](docs/ai/context/projeto.md#owners-vivos).
- Registro integral anterior à reorganização de 06/10/2026 (13/08 a 06/10): [arquivo histórico](docs/historico/changelog/2026-08-13_a_2026-10-06.md).

## 2026-10-06

- (Codex) Guarda de preservação dos testes core passa a fingerprint tipado estável entre Python 3.11 e 3.12, mantendo hashes históricos; a receita completa do kit ganha regressão em PR nos dois runtimes. Não certifica Windows nem destino institucional. [Contrato e migração](docs/manutencao/fingerprint-core.md).
- (Codex) Arquitetura por tarefa: 198 entradas preservadas, recortes explícitos de contexto, 38 arquivos de manutenção extraídos do payload e espelho gerado fora do Git. Cobertura B0 mede identidades/coleta; CI compartilha suítes somente entre ambientes equivalentes, mantendo checks. Mudança local, sem publicação ou homologação de destino. [ADR-0026](docs/decisions/ADR-0026-arquitetura-projeto-e-historia.md) · [Prova de preservação](docs/historico/changelog/README.md).
- (Codex) Documentação e instruções de manutenção passam a rotas por tarefa, núcleo AGENTS, cinco skills canônicas e adaptadores mínimos, com história preservada. Compatibilidade nativa e Windows ainda não certificadas. [ADR-0025](docs/decisions/ADR-0025-arquitetura-instrucoes-ia.md) · [Evidência READMEs](docs/auditoria/2026-10-06_readmes/README.md).

## 2026-10-01

- (Codex) Aceite técnico dos oito perfis sintéticos B1 integrado. Não equivale a homologação Genie integral nem promoção da policy. [Estado e provas](docs/sprints/skill_enforcement_rollout/README.md).

## 2026-09-30

- (Codex) Micromodelos distribuídos como módulo de domínio no Hub, com contratos, execução reutilizável e exemplo sintético. Skill permanece L1/audit; E2 exige gates próprios. [ADR-0024](docs/decisions/ADR-0024-modulo-micromodelos-no-hub.md) · [Owner](docs/sprints/micromodelos/README.md).

## 2026-09-24

- (ChatGPT) B0 qualificado localmente no perfil 2/1 com evidência RAW/SHARE sanitizada; 3/2 não qualificado. Qualificação histórica, limitada àquela base; coverage da base atual exige reconciliação própria. Campanhas e efeitos continuam com autorização própria. [ADR-0023](docs/decisions/ADR-0023-execucao-paralela-governada-ser.md) · [Provas](docs/sprints/skill_enforcement_rollout/PARALELO/B0/README.md).

## 2026-09-22

- (ChatGPT) SE08 integrada com certificação delimitada e verificação Free. Falhas históricas e bloqueio de promoção ao trabalho preservados. [Owner SEF/SER](docs/sprints/skill_enforcement/README.md).

## 2026-09-16

- (ChatGPT) Contrato estruturado verificável de skills introduzido; declaração de recurso não comprova execução. [ADR-0021](docs/decisions/ADR-0021-execucao-verificavel-de-skills.md).

## 2026-09-14

- (ChatGPT) Fundação de Micromodelos integrada: artefato de domínio, YAML canônico, runs no MLflow e governança externa. [ADRs 0014–0020](docs/decisions/README.md) · [Owner](docs/sprints/micromodelos/README.md).
- (ChatGPT) Temas V08 integram skills, padrões e Manual ao contrato visual central; aplicação continua explícita e não altera cálculo. [ADR-0013](docs/decisions/ADR-0013-sistema-de-temas.md) · [Estado posterior](docs/sprints/sistema_temas/README.md).

## 2026-09-13

- (ChatGPT) Migração READMEs R00–R13 encerrada; novos objetos continuam sujeitos ao contrato e ao ratchet. [ADR-0012](docs/decisions/ADR-0012-readmes-de-objeto.md) · [Provas](docs/sprints/readmes_objetos/README.md).

## 2026-09-12

- (Codex) Concierge integrado como entrada opcional de descoberta/composição, sem substituir helpers explícitos nem comprovar execução conversacional. [ADR-0011](docs/decisions/ADR-0011-concierge-hub.md).

## 2026-09-11

- (Codex) Manual Técnico unifica catálogo e glossário; fonte canônica e cópias de leitura/derivado seguem sincronização controlada. [ADR-0010](docs/decisions/ADR-0010-manual-tecnico-unificado.md).
