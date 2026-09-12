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

## Sistema de Temas do Hub

A [iniciativa V00–V14](sistema_temas/README.md) preserva a numeração das sprints
históricas e dos READMEs. V00 foi integrada no Git; a [candidata V01](sistema_temas/V01/README.md)
propõe contrato e experiência, sem alterar a aparência ou publicar no Databricks.
