# Sprints da reestruturação do Hub

Estes relatórios registram a transformação do pacote original no ambiente atual. São evidência histórica: não servem como manual vigente e não devem ser reescritos para acompanhar o produto.

## Como ler

1. Comece pelo plano e registro de execução em [`PLANO_HUB.md`](../../PLANO_HUB.md).
2. Abra a sprint do componente que deseja investigar.
3. Use a auditoria citada no relatório para conferir o contraditório da rodada.
4. Para o estado atual, volte ao [README raiz](../../README.md) ou aos [testes vigentes](../testes/README.md).

## Índice

| Bloco | Relatórios | Tema |
|---|---|---|
| Fundação | [Sprint 0](sprint-0-fundacao.md) · [Sprint 0b](sprint-0b-fixtures-e-api-publica.md) | arquitetura, fixtures e API pública |
| Forma do Hub | [Sprint 1](sprint-1-padroes.md) · [Sprint 2](sprint-2-renomeacao.md) · [Sprint 3](sprint-3-skills.md) | padrões, identidade e skills |
| Conteúdo | [Sprint 4](sprint-4-hub-scripts.md) · [Sprint 5](sprint-5-hub-prompts.md) · [Sprint 6](sprint-6-snippets-spark.md) | scripts, prompts e Spark |
| Biblioteca de ML | [Sprint 7](sprint-7-ml-nucleo.md) · [Sprint 8](sprint-8-ml-dependencia-opcional.md) | núcleo e dependências opcionais |
| Experiência e fechamento | [Sprint 9](sprint-9-constants-visual-display.md) · [Sprint 10](sprint-10-readmes-de-topo.md) · [Sprint 11](sprint-11-hub-ml-criar-objeto.md) · [Sprint 12](sprint-12-fechamento.md) | visual, documentação, criação e gates |

Nomenclatura antiga dentro dos relatórios permanece como evidência da época. A correspondência com a identidade `hub_`/`hub-` está no [ADR-0006](../decisions/ADR-0006-identidade-hub.md).

## Iniciativa de READMEs por objeto

A [iniciativa R00–R13](readmes_objetos/README.md) usa numeração própria e está encerrada no Git desde 14/09/2026: 75/75 READMEs operacionais, 3/3 exemplares, zero pendências e auditoria final local `A0_light`. Homologação Databricks/Genie Code e auditoria independente permanecem gates separados.

As subseções cronológicas abaixo preservam o estado observado em cada etapa. O [checkpoint R02-I](readmes_objetos/CHECKPOINT_INTEGRACAO_R02.md), o [piloto R02](readmes_objetos/CHECKPOINT_R02.md) e os relatos R00/R01 continuam históricos; frases como “R03 não iniciada” descrevem aquele checkpoint, não o estado vigente.

## Sistema de Temas do Hub

A [iniciativa V00–V14](sistema_temas/README.md) preserva a numeração própria. V00, [V01](sistema_temas/V01/README.md), [V02](sistema_temas/V02/README.md), [V03](sistema_temas/V03/README.md) e [V04](sistema_temas/V04/README.md) estão aceitas e integradas no Git.

A [V05 — Visual Lab](sistema_temas/V05/README.md) está em fechamento numa branch separada, reconciliada com a `main` pós-D05. Ela acrescenta escolha guiada de ponto de partida, ajuste, comparação e sessão rastreável/reabertura, mas **ainda não possui aceite nem merge**. O [checkpoint V05](sistema_temas/V05/CHECKPOINT_V05.md) preserva as execuções e os bloqueios; nenhum teste Python equivale a homologação Databricks.

A V02 entrega o núcleo de carga, validação e resolução de configurações completas. A V03 acrescenta o adaptador Plotly opt-in. A V04 estende a arquitetura a HTML, estilos compartilhados e tabela pandas por rotas `_resolvido`. A V05 usa essas camadas para autoria assistida sem tornar a configuração global nem publicar tema.

Não houve publicação Databricks da iniciativa; homologação operacional, auditoria independente e avaliação com usuário iniciante permanecem separadas. A V06 não foi iniciada.

## Cronologia preservada — READMEs por objeto

### Continuidade READMEs — 2026-09-12, R03-A
Integração R02-I aprovada por Rodrigo e realizada pelo PR nº 7 (`5493f7d`). Contrato 1.0.0 estabilizado; sete novos guias da R03-A foram entregues em branch separada para revisão. Registro no [fechamento da R03-A](readmes_objetos/RELATORIO_R03A.md).

### Continuidade READMEs — 2026-09-12, R03-B
Seis guias de display/visual, preservando o contrato 1.0.0 e as APIs. Estado, matriz e testes em [RELATORIO_R03B.md](readmes_objetos/RELATORIO_R03B.md).

### Integração READMEs com a main V01 — 2026-09-12
Rodrigo autorizou a reconciliação e integração das R03-A/R03-B com a main que já continha V01. Registro em [`INTEGRACAO_R03_V01.md`](readmes_objetos/INTEGRACAO_R03_V01.md).

### READMEs R04-A a R13
As rodadas R04-A, R04-B, R05, R06, R07, R08, R09, R10, R11, R12 e R13 permanecem documentadas em [`readmes_objetos/`](readmes_objetos/README.md), com relatórios, matrizes e checkpoints próprios. A R13 foi aceita e integrada pelo PR #33 (`b0e953cc`) e encerrou a iniciativa no Git com 75/75 objetos operacionais, 3/3 exemplares, 0 pendências e auditoria final local `A0_light`.

### Reconciliação documental pós-R13
O escopo D01–D04 está em [`documentacao_pos_r13.md`](documentacao_pos_r13.md). A D05 do Sistema de Temas foi integrada antes da retomada V05 e está registrada em [`sistema_temas/RECONCILIACAO_DOCUMENTAL_D05.md`](sistema_temas/RECONCILIACAO_DOCUMENTAL_D05.md).
