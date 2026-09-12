# Sprints da reestruturação do Hub

Estes relatórios registram a transformação do pacote original no ambiente atual.
São evidência histórica: não servem como manual vigente e não devem ser
reescritos para acompanhar o produto.

## Como ler

1. Comece pelo plano e registro de execução em [`PLANO_HUB.md`](../../PLANO_HUB.md).
2. Abra a sprint do componente que deseja investigar.
3. Use a auditoria citada no relatório para conferir o contraditório da rodada.
4. Para o estado atual, volte ao [README raiz](../../README.md) ou aos
   [testes vigentes](../testes/README.md).

## Índice

| Bloco | Relatórios | Tema |
|---|---|---|
| Fundação | [Sprint 0](sprint-0-fundacao.md) · [Sprint 0b](sprint-0b-fixtures-e-api-publica.md) | arquitetura, fixtures e API pública |
| Forma do Hub | [Sprint 1](sprint-1-padroes.md) · [Sprint 2](sprint-2-renomeacao.md) · [Sprint 3](sprint-3-skills.md) | padrões, identidade e skills |
| Conteúdo | [Sprint 4](sprint-4-hub-scripts.md) · [Sprint 5](sprint-5-hub-prompts.md) · [Sprint 6](sprint-6-snippets-spark.md) | scripts, prompts e Spark |
| Biblioteca de ML | [Sprint 7](sprint-7-ml-nucleo.md) · [Sprint 8](sprint-8-ml-dependencia-opcional.md) | núcleo e dependências opcionais |
| Experiência e fechamento | [Sprint 9](sprint-9-constants-visual-display.md) · [Sprint 10](sprint-10-readmes-de-topo.md) · [Sprint 11](sprint-11-hub-ml-criar-objeto.md) · [Sprint 12](sprint-12-fechamento.md) | visual, documentação, criação e gates |

Nomenclatura antiga dentro dos relatórios permanece como evidência da época. A
correspondência com a identidade `hub_`/`hub-` está no
[ADR-0006](../decisions/ADR-0006-identidade-hub.md).

## Iniciativa de READMEs por objeto

A [migração R00–R13](readmes_objetos/README.md) usa numeração própria. Os
relatórios históricos acima permanecem intactos; não são substituídos pelos
checkpoints desta iniciativa.

O [checkpoint R02-I](readmes_objetos/CHECKPOINT_INTEGRACAO_R02.md) registra a
composição candidata com o Concierge. O [piloto R02](readmes_objetos/CHECKPOINT_R02.md)
e os relatos R00/R01 permanecem históricos; não houve início da R03.

## Continuidade READMEs — 2026-09-12, R03-A

Integração R02-I aprovada por Rodrigo e realizada pelo PR nº 7 (`5493f7d`).
Contrato 1.0.0 estabilizado; sete novos guias da R03-A são entregues em branch
separada para revisão. Registro, matriz, testes e próxima parada no
[fechamento da R03-A](readmes_objetos/RELATORIO_R03A.md). R03-B não iniciada; sem publicação Databricks.

## Continuidade READMEs — 2026-09-12, R03-B

Seis guias de display/visual, preservando o contrato 1.0.0 e as APIs.
Branch separada baseada na R03-A `c60f1e5`; PR nº 9 ainda não integrado.
[Relatório, verificações e ponto de parada](readmes_objetos/RELATORIO_R03B.md).
Sem aceite antecipado, merge automático, publicação ou início da R04-A.

## Integração READMEs com a main V01 — 2026-09-12

Rodrigo autorizou a reconciliação e integração das R03-A/R03-B com a `main` que já contém V01. A candidata preserva os 19 READMEs operacionais, o contrato 1.0.0 e a documentação/guardas do sistema de temas. Registro em [`INTEGRACAO_R03_V01.md`](readmes_objetos/INTEGRACAO_R03_V01.md).

## Continuidade READMEs — 2026-09-12, R04-A

A `main` integrada `1be947b` é a base da nova leva. Seis snippets Spark recebem
README didático no contrato 1.0.0, com documentação de grão, ações/coletas,
custos e interpretação. Estado, matriz e testes em
[`RELATORIO_R04A.md`](readmes_objetos/RELATORIO_R04A.md). Cobertura candidata
25/74; sem publicação, aceite antecipado ou início da R04-B.

## Sistema de Temas do Hub

A [iniciativa V00–V14](sistema_temas/README.md) preserva a numeração das sprints
históricas e dos READMEs. V00, [V01](sistema_temas/V01/README.md) e
[V02](sistema_temas/V02/README.md) estão aceitas e integradas no Git. A V02 entrega
o núcleo de carga, validação e resolução de configurações completas.

A [V03](sistema_temas/V03/README.md) recebeu aceite explícito de Rodrigo e teve sua integração Git autorizada pelo PR #16. Ela acrescenta apenas um adaptador Plotly opt-in, preserva o caminho legado por padrão e não migra consumidores existentes. O estado efetivo do merge é registrado na PR. Não houve publicação Databricks; homologação operacional, auditoria independente e avaliação com usuário iniciante permanecem pendentes.
