# Construção histórica do Hub — changelog consolidado

Esta é a entrada única para entender como o ambiente pessoal se tornou o Hub
atual. Reúne a intenção do antigo `PLANO_HUB.md`, a evolução por etapas e os
marcos do changelog. Leia a trajetória; consulte os registros originais para investigar decisões ou provas.

A síntese foi consolidada em **07/10/2026 por Codex**, na base `6ac0060dfcd09134634abe204474debb5757e231`.
A síntese interpreta a trajetória; marcos e testes antigos descrevem sua época, sem certificar a base atual. Estado corrente pertence aos [owners vivos](docs/ai/context/projeto.md#owners-vivos),
decisões ao [índice de ADRs](docs/decisions/README.md) e uso ao
[Manual Técnico V2](ambiente_databricks/.assistant/MANUAL_TECNICO_V2.md).

## Trajetória da construção

### Agosto de 2026 — do ambiente pessoal a uma biblioteca de equipe

O plano original buscava tornar reconhecível o que era próprio da equipe e o
que pertencia à plataforma. Adotou `hub_*` para bibliotecas e coleções e
`hub-ml-*` para skills. Snippets e scripts passaram a objetos com implementação,
API pública, README e notebook de exemplo; prompts passaram a briefings com
exemplo de uso. Padrões foram colocados dentro de `.assistant/` para acompanhar
a distribuição e ficar disponíveis no workspace.

A construção foi organizada em sprints com dependências e auditorias. Primeiro
vieram validador, smoke test, fixtures e exports públicos; depois moldes e
renomeações. Os scripts serviram de piloto antes da conversão dos snippets.
Skills, prompts, bibliotecas, índices e a skill de criação de objetos fecharam
a primeira estrutura. O plano registra fechamento em agosto, mas também
pendências humanas nos prompts e forward tests: esses registros não devem ser
lidos como homologação integral de todas as superfícies.

As auditorias revelaram limites que passaram a orientar a manutenção:
notebooks de exemplo não podem ser importados como módulos comuns; dependências
opcionais precisam de execução no ambiente adequado; links e APIs precisam
sobreviver às mudanças de árvore; sobrescrever uma publicação não remove
objetos obsoletos. A dívida de exemplos sem saída foi explicitada e fechada em
18/08; a guarda de saída colada passou de aviso a falha. A auditoria de 20/08 e
a reexecução registrada em 29/08 amadureceram os procedimentos de teste e
replicação. Consulte o [índice das sprints](docs/sprints/README.md) e o
[plano integral congelado](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd/PLANO_HUB.md) para a sequência e os resultados da época.

### Setembro de 2026 — documentação, descoberta, temas e governança

O Manual Técnico consolidou catálogo e glossário. O Concierge surgiu como
entrada opcional para descobrir e compor recursos. A campanha R00–R13 criou
READMEs didáticos por objeto e um contrato verificável; seus números de
fechamento são históricos, enquanto a cobertura atual é medida pelo validador.
As razões e provas estão nos ADRs 0010–0012 e no
[owner da campanha de READMEs](docs/sprints/readmes_objetos/README.md).

O Sistema de Temas tornou a aparência um contrato compartilhado e opt-in,
separado dos cálculos analíticos. Micromodelos ganhou especificação, execução
reutilizável, observabilidade e governança de domínio, consumindo os temas
existentes. Em 30/09, passou a módulo distribuído no Hub. Consulte os owners de
[Temas](docs/sprints/sistema_temas/README.md) e
[Micromodelos](docs/sprints/micromodelos/README.md); a skill de Micromodelos
permanece `L1/audit` até comprovação própria para promoção.

SEF/SER introduziu contratos estruturados, provas por superfície e certificação
prospectiva. B0/B1 receberam aceites delimitados, sem autorização de efeitos,
promoção de policy ou homologação automática de outro ambiente; veja os owners
[SEF](docs/sprints/skill_enforcement/README.md) e [SER](docs/sprints/skill_enforcement_rollout/README.md).

### Outubro de 2026 — manutenção por tarefa e preparação para o trabalho

Em 06/10, instruções de manutenção passaram ao núcleo `AGENTS.md`, com rotas em
`docs/ai/`, cinco skills canônicas e adaptadores. A história extensa foi
preservada com manifesto e testes de recuperação; manutenção foi separada do
produto e o simulado passou a derivado local fora do Git. A motivação era
reduzir contexto desnecessário sem perder as razões nem as provas da construção
(ADRs 0025/0026).

Em 07/10, a revisão integrada reforçou contenção e rastreabilidade. A preparação
para VS Code com Copilot e Databricks renomeou a fonte para
`ambiente_databricks/`, retirou o protótipo Concierge duplicado e adotou o Manual
Técnico V2 como edição técnica única. Os 20 workflows foram documentados;
ferramentas receberam catálogo, índice e READMEs de subpastas. A reorganização
física de `tools/` e possíveis renomes de workflows continuam no
[plano de manutenção](docs/manutencao/organizacao-tools-raiz-workflows-2026-10-07.md).

Esta consolidação encerra a concorrência entre plano histórico e changelog
como entradas da trajetória. O corpo antigo do plano é consultável por commit;
os registros integrais e ADRs continuam evidências de aprofundamento, sem
exigir sua leitura em toda tarefa.

## Decisão vigente herdada do plano

<a id="paleta-institucional"></a>

### A paleta permanece como está

**Decidido em 16/08/2026:** manter `AZUL_CAIXA` e a nomenclatura de
`constants/colors.py`. A decisão original registra uso institucional em
repositório privado; não se deve reabrir esse ponto como defeito de identidade
sem uma nova decisão explícita. `CORPORATE_RE` cobre domínios de e-mail, não
nomes de constantes; não é necessária exceção de código para essa paleta.

Esta seção sucede a §2.2 do plano. As demais escolhas de agosto são contexto
histórico; contratos atuais pertencem aos ADRs, padrões e owners correspondentes.

## Como manter e consultar esta história

Acrescente somente marcos de uso, arquitetura, contrato ou risco material,
com data, autoria e link para o documento responsável. Use o
[critério de registro](docs/ai/templates/changelog-entry.md). A trajetória
acima deve receber síntese apenas quando uma nova etapa material se consolidar;
evidência antiga, autoria e resultados datados não são reescritos.

- **Leitura inicial por uma LLM:** trajetória acima, owners da tarefa e
  `AGENTS.md`; sem carregamento obrigatório de toda a história.
- **Investigação detalhada:** [198 registros originais de 13/08 a 06/10](docs/historico/changelog/README.md),
  com hashes, ordem e recuperação preservados.
- **Plano original:** [versão congelada no Git](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd/PLANO_HUB.md), base `09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd`,
  SHA-256 `4307e9c3dd6301b7b04733f6ebaebaa8d6ab41215550e6817bb0b68b39ac125f`; recuperação e limites no
  [ADR-0030](docs/decisions/ADR-0030-historia-consolidada.md).
- **Problema recorrente:** [classes de defeito que viraram guardas](docs/auditoria/README.md#classes-de-defeito-que-viraram-guardas).

## Marcos datados

Os relatos abaixo estão em ordem decrescente de data. Dentro do mesmo dia,
novos marcos entram primeiro. Uma etapa posterior pode substituir um estado
anterior; isso não altera o relato original.

## 2026-10-08 — Preparação individual para o trabalho (Codex)

- Configuração pessoal ignorada, comparação de host e plano offline por arquivo.
  Três skills e dois agentes preparam manutenção com Copilot no VS Code; adaptadores
  Claude Code retirados com rastreabilidade histórica. Integração corporativa e
  transferência CLI aguardam confirmação do cliente. [ADR-0032](docs/decisions/ADR-0032-preparacao-individual-copilot-trabalho.md) · [Execução](docs/manutencao/execucao-adaptacao-trabalho-2026-10-08.md).

## 2026-10-08 — Retirada do localizador histórico (Codex)

Exclui `PLANO_HUB.md`; regras e índices passam ao consolidado. Preserva dois hrefs
históricos por recuperação Git estrita, mantendo fontes e as 30 exceções anteriores.
[Decisão, execução e limites](docs/decisions/ADR-0031-retirada-localizador-plano-hub.md).

## 2026-10-07 — História consolidada (Codex)

Unifica plano e changelog nesta entrada de construção histórica, com trajetória,
marcos preservados, decisão da paleta e recuperação do plano original por commit.
`PLANO_HUB.md` passa a localizador; não contém outro plano ativo. Retira somente
a exceção de referência legada cujo trecho saiu desse localizador. Produto,
workflows, instruções e snapshots históricos permanecem preservados.
[Decisão e verificações](docs/decisions/ADR-0030-historia-consolidada.md).

## 2026-10-07 — Navegação de ferramentas e workflows (Codex)

Documenta as oito subpastas de manutenção sem entrada, cria índice individual de
`tools/` e rótulos humanos dos 20 workflows. Registra necessidade dos arquivos Git
e do plano histórico da raiz, com proposta de migração por domínio; não altera
código, YAML, produto ou pins. [Diagnóstico e plano](docs/manutencao/organizacao-tools-raiz-workflows-2026-10-07.md).

## 2026-10-07 — Faxina para manutenção no trabalho (Codex)

Fonte renomeada para `ambiente_databricks/`, com código, testes, CI e instruções migrados; protótipo Concierge duplicado retirado com recuperação Git verificável; Manual Técnico V2 adotado como edição única vigente (ADR-0028/0029). Workflows e ferramentas catalogados, perfil Copilot VS Code documentado e referências históricas preservadas com prova específica. [Execução e validação](docs/manutencao/execucao-faxina-2026-10-07.md).

## 2026-10-07

- (Codex) Documenta os 20 workflows e prepara diagnóstico de simplificação para Copilot no VS Code e Databricks, com triagem de docs/tools e plano por sprints. Renomeações, remoções e consolidação dos manuais permanecem propostas. [Análise e limites](docs/manutencao/analise-faxina-2026-10-07.md).

- (Codex) Acrescenta o Manual Técnico V2 e o Manual do Usuário completos, com partes de consulta e mapas técnicos sanitizados; base examinada `983c9936f139402a0130f290653ae713d65a3ac7`.
  Preserva `MANUAL_TECNICO.md`; a entrega documental não comprova runtime, publicação, CI remoto ou homologação. [Edição e limites](ambiente_databricks/.assistant/manuais_v2/MANTER_EDICAO.md).

- (Codex) Correção integrada de contenção local, guardas de CI/instruções IA e execução integral core; rotas documentais e certificadores históricos explicitados, com metadados reduzidos opt-in no contexto de tarefa. Preserva runtime, evidência congelada e policy; publicação e homologação exigem provas próprias. [Decisão e limites](docs/decisions/ADR-0027-correcao-controles-auditoria-integrada.md).

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
