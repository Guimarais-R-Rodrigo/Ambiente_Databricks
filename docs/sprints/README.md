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

## Framework de Micromodelos — MM00 e MM01 integradas; MM02 pós-certificação

A [iniciativa MM00–MM13](micromodelos/README.md) usa trilha própria. A MM00 foi aceita e integrada pela PR #43 no commit `36e89515a46df24f41deea4791b109f5a1f938f2`; ADR-0014 a ADR-0020 permanecem aceitos sem ressalvas.

A MM01 — contrato canônico `micromodelo.yaml` — foi aceita e integrada pela PR #51 no merge `73d7659dcf11509a7fba392221c4810d10401c35`, com HEAD integrado `fa1a3653e60472d171307663d1175344bb3f6a8d`. A integração posterior da SER00/PR #101 não reabre a MM01 nem promove levels da policy.

O estado vivo e a preparação de MM02 estão no [README de Micromodelos](micromodelos/README.md), na [revisão pós-SEF/PSEF/SER](micromodelos/REVISAO_PLANO_POS_SEF_2026-09-23.md), na [retrospectiva MM01](micromodelos/RETROSPECTIVA_MM01.md) e no [protocolo de certificação](micromodelos/PROTOCOLO_CERTIFICACAO_SPRINTS.md).

**MM02 = POS_CERTIFICACAO**. O SHA funcional `3d3c6d40263a253449b448a3bcca679143252e54` passou smoke, FULL single-shot e auditoria independente; o único finding probatório de sanitização do bundle foi encerrado sem reexecução. A revalidação final documental ainda precede aceite e merge. Estado corrente: [MM02 — spec fingerprint](micromodelos/MM02/README.md).

## Sistema de Temas do Hub

A [iniciativa V00–V14](sistema_temas/README.md) preserva a numeração das sprints históricas. **V00–V13 estão aceitas e integradas no Git.** A S7/V13 foi integrada pela PR #66 no merge `62e9404851d6a7902371bd5b6531a113d521311c`; sua auditoria posterior permanece em [AUDITORIA_POS_MERGE.md](sistema_temas/V13/AUDITORIA_POS_MERGE.md).

O [Plano Mestre V14](sistema_temas/V14/PLANO_MESTRE.md) foi aceito e integrado pela PR #70 no merge `350dcf0b37e730042ef961f12f11b30b2660d2c6`. Os **15/15 workflows de `push`** desse SHA concluíram em `success`. A V14 está agora na **S0 — reconciliação pós-V13 e freeze de readiness**; o estado vivo fica em [V14/README.md](sistema_temas/V14/README.md) e o registro da execução em [V14/CHECKPOINT_S0.md](sistema_temas/V14/CHECKPOINT_S0.md). **S1–S8 não foram iniciadas.**

Os estados herdados continuam separados: `DOC-02`, `DOC-03`, `SEC-01`, `UAT-01` e `V12-AIBI-01` possuem PASS somente no alcance documentado; `A11-01` permanece **FAIL** na issue #57; `V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` permanecem **BLOQUEADO_AUTORIZACAO**. `HUMAN-01 = PASS` continua apenas como evidência formativa. A S0 não executa mutação Databricks, não declara production readiness e não decide go-live.

O [Plano Mestre V13](sistema_temas/V13/PLANO_MESTRE.md) foi aceito pela PR #58 e a sequência S0–S7 foi concluída sem criar uma segunda fonte de verdade. A V14 referencia esses owners e contratos; não reimplementa preflight, release/rollback, diagnóstico, schema, tokens ou bindings.

A V11 continua dona da ponte fail-closed entre um `ResolvedTheme` `notebook` e capacidades documentadas de temas nativos AI/BI sem ampliar silenciosamente o schema V01/V02: `context="aibi"` permanece reservado. A matriz cobre exatamente 48 tokens, classificados em 3 traduzidos, 23 aproximados e 22 não suportados. O projeto não inventa o schema do JSON nativo de `Import theme`; um binding nativo exige export real fixado por SHA-256, campos existentes e JSON Pointers revisados. Estado e limites estão em [V11](sistema_temas/V11/README.md), [testes V11](sistema_temas/V11/TESTES.md) e [checkpoint V11](sistema_temas/V11/CHECKPOINT_V11.md).

Os runs V11 `34900693160`, `34901091132`, `34901776770` e `34904363803` permanecem **FAILURE** e não foram reclassificados. O head final `5532ca6d8f1b243ca705088f4b57823a333b9b1f` teve o push pré-PR `34905080083` integralmente verde; os 11 workflows reais da PR #52 concluíram com `success`, e os 13 workflows pós-merge no commit `9305bc49eaf002caec042361bf35efa66af7ca18` também concluíram com `success`. O fechamento posterior V12 é quem registra as homologações reais que efetivamente ocorreram; isso não autoriza operações futuras por inferência.

A V10 foi aceita por Rodrigo em 14/09/2026 e integrada pelo PR #48 no merge `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`. Ela reutiliza o núcleo V02 e o Visual Lab V05 em uma superfície Streamlit `authoring_only`, com identidade encaminhada pelo proxy, namespace de sessão por SHA-256 e persistência projetada em Unity Catalog Volume via recurso `theme_storage`. Ela não implementa `context="app"`, aprovação, publicação, promoção ou delete de histórico. Evidências e limites estão em [V10](sistema_temas/V10/README.md), [testes V10](sistema_temas/V10/TESTES.md) e [checkpoint V10](sistema_temas/V10/CHECKPOINT_V10.md).

Os runs V10 `34884790130`, `34885407907` e `34886250755` permanecem failures históricos. O push final original `34887162337` concluiu com `success`; após a reconciliação com a MM00, os dez workflows reais de PR do head `cb942ee955ff9236f19099e5ed4ceee9beb32000` também concluíram com `success`. Depois do merge, os 12 workflows disparados por `push` no commit `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b` concluíram com `success`, incluindo o workflow V10 `34896944061`.

A V09 integra explicitamente o Sistema de Temas ao kit offline de transição: contrato temático no manifesto v2, guarda fail-closed antes do build e conferência de presença/tamanho/SHA256 dos nove arquivos canônicos dentro do ZIP gerado. No pós-merge final, 12/12 workflows de `push` concluíram com `success`, incluindo 43/43 testes com Spark local no workflow operacional. Transporte não significa ativação, promoção ou publicação.

A [V08 — integração transversal](sistema_temas/V08/README.md) conecta skills, Hub Padrões, entrada `.assistant` e Manual às mesmas fontes de verdade das V02–V07. A [matriz V08](sistema_temas/V08/MATRIZ_INTEGRACAO.json), o [checkpoint](sistema_temas/V08/CHECKPOINT_V08.md) e o [registro de testes](sistema_temas/V08/TESTES.md) preservam escopo, failures e a regra de zero alteração runtime Python.

A V08 remove a política visual paralela do template EDA, preservando suas convenções editoriais, e explicita que tema não altera dados, métricas, denominadores, thresholds ou decisões. SHAP/Matplotlib e Kaplan–Meier continuam limites declarados do theming atual.

A V08 foi aceita em 14/09/2026 e integrada pelo PR #42. O head final validado foi `9af5615d79b02cbd86f5a6d084444c83f203ae03`; o merge na `main` é `622d2c962a80998cf990b57036f7ae503bfc0458`. Os nove checks finais da PR e os dez workflows pós-merge da `main` concluíram com `success`.

A V07 permanece integrada pelo PR #40 no commit `67114605c7345a01c1144e5d6c6d24e9c24e2491`; o fechamento documental subsequente produziu a base V08 `1b6632194f4b25afc09960c27b069c16df365ee6`.

Não houve publicação Databricks da V08; browser/runtime, acessibilidade, ACL real, UAT, promoção visual e seleção determinística de skill permanecem gates separados. Naquele fechamento, a V09 ainda não havia sido iniciada.

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