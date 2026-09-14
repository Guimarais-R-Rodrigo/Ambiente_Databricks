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

A [iniciativa R00–R13](readmes_objetos/README.md) usa numeração própria e está
encerrada no Git desde 14/09/2026: 75/75 READMEs operacionais, 3/3 exemplares,
zero pendências e auditoria final local `A0_light`. Homologação Databricks/Genie
Code e auditoria independente permanecem gates separados.

As subseções cronológicas abaixo preservam o estado observado em cada etapa. O
[checkpoint R02-I](readmes_objetos/CHECKPOINT_INTEGRACAO_R02.md), o
[piloto R02](readmes_objetos/CHECKPOINT_R02.md) e os relatos R00/R01 continuam
históricos; frases como “R03 não iniciada” descrevem aquele checkpoint, não o
estado vigente.

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

## Framework de Micromodelos

A [iniciativa MM00–MM13](micromodelos/README.md) usa numeração própria. A MM00
registra baseline, Plano Mestre, inventário, matrizes de reuso/risco/dependência,
ADRs, testes e checkpoint antes de qualquer implementação funcional. O desenho
obriga piloto greenfield antes da migração de legados e mantém a integração
visual definitiva para a fase de hardening. MM01 não começa sem aceite explícito
do checkpoint MM00.

## Sistema de Temas do Hub

A [iniciativa V00–V14](sistema_temas/README.md) preserva a numeração das sprints
históricas. **V00–V07 estão aceitas e integradas no Git.** A V08 ainda não foi
iniciada neste fechamento pós-merge da V07.

A [V07 — demais consumidores e formatos de saída](sistema_temas/V07/README.md)
cria rotas temáticas opt-in para consumidores runtime de `display` e `ml`, sem
mudar cálculo, agregação, amostragem ou decisões analíticas. O
[checkpoint V07](sistema_temas/V07/CHECKPOINT_V07.md) e o
[registro de testes](sistema_temas/V07/TESTES.md) preservam failures históricos,
a correção para `palette.diverging`, a PR #40 e os nove checks pós-merge verdes.

A V07 foi mesclada no commit
`67114605c7345a01c1144e5d6c6d24e9c24e2491`, a partir do head final
`6b50151738a311eff8530c3191e24693af3fb036`; merge e candidata apontam para a
mesma árvore `5438288bda2326e96372c7464b3aef0cb8375102`.

A V06 havia sido mesclada pelo PR #38 no commit
`418946de8d1e95e87cbfd9df528ddcced5075237`, e seu fechamento documental foi
integrado pela PR #39 no commit `0c0c71bce4bbc09130ec51eec8245057be4f3d81`,
base de criação da V07.

A V02 entrega o núcleo de carga, validação e resolução de configurações completas.
A V03 acrescenta o adaptador Plotly opt-in. A V04 estende a mesma arquitetura a
componentes HTML, estilos compartilhados e tabela pandas. A V05 acrescenta o
Visual Lab opt-in em notebook. A V06 atua na camada de geração editorial. A V07
completa consumidores runtime e delimita os formatos de saída exercitados. A V08
é a próxima camada transversal: liga o sistema já implementado a skills, padrões
e Manual sem duplicar fontes de verdade.

Não houve publicação Databricks da V07; browser/runtime, acessibilidade, ACL real,
UAT, promoção visual e auditoria independente permanecem gates separados.

### Continuidade do Sistema de Temas — V04

A V03 foi efetivamente integrada pelo PR #16 no commit `b83a7cde`. Rodrigo aceitou
a V04 em 12/09/2026 e ela foi integrada pelo PR #21 no commit
`5a7b33d7137f88c1ec80315de1b422293b3ba206`. A árvore do merge coincide com a
candidata validada e os seis workflows permanentes pós-merge concluíram com
`success`. A homologação Databricks continua separada; a frase histórica de que
V05 ainda não havia sido iniciada descreve o fechamento V04.

### READMEs de objeto — R04-B
A R04-A está integrada em `a8f314a`. A R04-B cobre seis Hub Scripts e pausa para revisão antes da R05. Consulte `readmes_objetos/RELATORIO_R04B.md` e `readmes_objetos/MATRIZ_ALTERACOES_R04B.md`.

### READMEs de objeto — R05
A R04-B está integrada em `d9da056`. A R05 cobre seis modelos tabulares e pausa para revisão antes da R06. Consulte `readmes_objetos/RELATORIO_R05.md` e `readmes_objetos/MATRIZ_ALTERACOES_R05.md`.

### READMEs de objeto — R06
A R05 foi integrada em `cae94988`. A R06 cobre cinco objetos de séries/validação temporal e pausa para revisão antes da R07. Consulte `readmes_objetos/RELATORIO_R06.md` e `readmes_objetos/MATRIZ_ALTERACOES_R06.md`.

### READMEs de objeto — R07
A R06 foi integrada em `289731c`. A R07 cobre seis objetos de score, vintage e sobrevivência e pausa para revisão antes da R08. Consulte `readmes_objetos/RELATORIO_R07.md` e `readmes_objetos/MATRIZ_ALTERACOES_R07.md`.

### READMEs de objeto — R08
A R07 foi integrada pelo PR #25. A R08 cobre seis objetos de clusterização, anomalias e explicabilidade e preserva implementações/fachadas. Relatório, matriz e achados ficam em `docs/sprints/readmes_objetos/`. A cobertura esperada após validação é 55/75 operacionais + 3/3 exemplares; isso não representa aceite editorial antecipado.
### READMEs R09
Leva de avaliação, drift e MLOps: cinco objetos; cobertura candidata 60/75, sujeita ao freeze e aceite.

### READMEs R10
Após a integração da R09 pelo PR #29 (`d412acb`), a R10 cobre seis Hub Prompts de exploração, qualidade, reconciliação, feature engineering e validação estatística. A cobertura alvo é 66/75 operacionais + 3/3 exemplares, sujeita ao validador e ao aceite editorial.

### READMEs R11
A R10 foi integrada pelo PR #30 (`7ba5d386`). A R11 cobre os nove Hub Prompts restantes e busca fechar a migração estrutural em 75/75, sem antecipar homologação ou etapas posteriores.

### READMEs R12 — integração de navegação
Após a R11 fechar 75/75 objetos, a R12 cria os seis índices de categoria de `hub_snippets` e reconcilia a navegação com o catálogo, a entrada `.assistant` e o Manual Técnico. Não altera implementação nem reabre a migração de objetos.

### READMEs R13 — auditoria final consolidada
Após a integração da R12 pelo PR #32 (`ec4b559d`), a R13 audita em conjunto contrato, checklist, skill de criação, validador, Manual, 75 READMEs operacionais, três exemplares, seis índices de categoria e espelho derivado. A rodada é local e registra `A0_light`; homologação Databricks/Genie Code e auditoria independente permanecem gates separados.

### READMEs R13 — encerramento da iniciativa
A R13 foi aceita e integrada pelo PR #33 (`b0e953cc`). A iniciativa própria de READMEs R00–R13 está encerrada no Git com 75/75 objetos operacionais, 3/3 exemplares, 0 pendências e auditoria final local `A0_light` aprovada. Homologação Databricks/Genie Code e auditoria independente continuam fora deste fechamento.

### Reconciliação documental pós-R13
Escopo D01–D04: `docs/sprints/documentacao_pos_r13.md`. A D05 do Sistema de Temas
foi integrada antes da retomada V05 e está registrada em
[`sistema_temas/RECONCILIACAO_DOCUMENTAL_D05.md`](sistema_temas/RECONCILIACAO_DOCUMENTAL_D05.md).
