# Framework de Micromodelos — execução por sprints

> Estado: **MM00–MM03 integradas; módulo de laboratório MM04–MM13 integrado ao Hub no Git pelo PR #119 (`63601e09`).** O laboratório sintético foi aceito pelo responsável. Kit r4 revisado, adapter metadata e três runs MLflow sintéticas foram executados no Free via CLI; skill instalada. O Hub integrado foi publicado no Free e teve readback de conteúdo 691/691 PASS em 2026-09-30. Os três casos Genie E1 da revisão corrigida passaram nos critérios de resposta, com ressalvas. A skill permanece L1/audit; certificação MM04 e E2 no trabalho continuam pendentes.

## Objetivo

Construir uma esteira rastreável e auditável para descobrir, especificar, estudar, validar, publicar e, somente após um piloto novo e o congelamento da V1, migrar micromodelos.

O repositório usa somente fixtures e placeholders. O catálogo real do trabalho é representado aqui por `<CATALOGO_PRODUTO>` e o binding para nomes reais ocorre apenas no workspace autorizado.

Documentos vivos desta fase:

- [integração de Micromodelos ao Hub e entrega do ambiente completo](PLANO_INTEGRACAO_HUB_MICROMODELOS.md) — integração Git concluída; separa o pacote local dos gates no trabalho;
- [execução de laboratório e revisão processual](PLANO_EXECUCAO_LAB.md);
- [aceite do laboratório sintético](CHECKPOINT_ACEITE_LAB_2026-09-29.md);
- [entrega local completa antes da transferência](PLANO_ENTREGA_LOCAL.md);
- [preparação do piloto E2 e portas de avanço](PLANO_PREPARACAO_E2.md);
- [relatório da candidata E0 e estados E1/E2](RELATORIO_ENTREGA_LAB.md);
- [resultados Genie E1 e limites](RESULTADOS_GENIE_E1_2026-09-29.md);
- [reconciliação B1 e pré-gates MM04](RECONCILIACAO_B1_PRE_GATES_MM04_2026-09-29.md);
- [teste manual dos briefings MM04–MM05 no Genie](TESTE_BRIEFINGS_MM04_E1.md);
- [kit Databricks Free e roteiro E2 posterior](KIT_FREE.md);
- [MM03 — metadata-only](MM03/README.md);
- [MM03 — contrato metadata v1](MM03/CONTRATO_METADATA.md);
- [MM03 — testes e gates](MM03/TESTES.md);
- [MM03 — checkpoint](MM03/CHECKPOINT.md);

Documentos históricos da MM02:

- [MM02 — spec fingerprint](MM02/README.md);
- [MM02 — matriz de materialidade](MM02/MATRIZ_MATERIALIDADE.md);
- [MM02 — testes e certificação](MM02/TESTES.md);
- [MM02 — checkpoint](MM02/CHECKPOINT.md);

- [revisão pós-MM01/SEF/PSEF/SER](REVISAO_PLANO_POS_SEF_2026-09-23.md);
- [retrospectiva operacional da MM01](RETROSPECTIVA_MM01.md);
- [protocolo de certificação para MM02–MM13](PROTOCOLO_CERTIFICACAO_SPRINTS.md);
- [checkpoint pós-merge da MM01](MM01/POST_MERGE_CHECKPOINT.md).

## Fases

- MM00–MM06: fundação do framework.
- MM07–MM08: pacote departamental e homologação no trabalho.
- MM09–MM10: primeiro micromodelo novo e prova ponta a ponta.
- MM11: hardening, visual e monitoramento quando disponíveis; freeze V1.
- MM12: migração conservadora dos legados.
- MM13: catálogo, impacto e fechamento.

## Regra de avanço desta candidata de laboratório

O [plano ativo](PLANO_EXECUCAO_LAB.md) usa implementação incremental, testes proporcionais e revisão focal separada. Freeze, FULL, bundle, contraditório e aceite por sprint descritos nos registros anteriores são histórico da execução MM00–MM03; não são gates automáticos desta candidata. Contratos de produto, validações e autoridade externa de publicação permanecem vigentes.

## Estado da MM00

A MM00 congelou baseline, arquitetura, reuso, riscos, dependências e fronteiras de governança sem alterar funcionalmente o produto `.assistant`.

- auditoria A1 executada: `APTA_COM_CORRECOES`;
- M-01 corrigido;
- D1-B autorizada e posteriormente consumida no fechamento pós-merge;
- ADR-0014 a ADR-0020 aceitos sem ressalvas;
- PR #43 integrada em `36e89515a46df24f41deea4791b109f5a1f938f2`;
- Q-01 fechado pela PR #49;
- fechamento pós-MM00 integrado em `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`;
- CI geral e V00–V09 pós-merge concluídos com sucesso.

A exceção D1-B terminou com o fechamento de Q-01 e não se propaga às próximas sprints.

## Estado vigente da MM01

A MM01 foi aceita e integrada. O HEAD da branch no merge foi `fa1a3653e60472d171307663d1175344bb3f6a8d`; o merge da PR #51 é `73d7659dcf11509a7fba392221c4810d10401c35`. O contrato canônico `micromodelo.yaml` está na `main`; a MM02 foi aceita e integrada pela PR #109 e a MM03 pela PR #110.

O fechamento consolidado está no [checkpoint pós-merge](MM01/POST_MERGE_CHECKPOINT.md). A arquitetura prospectiva passa a consumir a [revisão pós-SEF](REVISAO_PLANO_POS_SEF_2026-09-23.md) sem reabrir MM01.

## Histórico pré-merge da MM01

A MM01 foi iniciada na branch `micromodelos/mm01-contrato-canonico` e reconciliada de forma fail-closed com as evoluções da `main`, inclusive as bases pós-V10 e pós-V11. **Naquele estágio histórico**, a PR #51 permanecia aberta, não aceita e não integrada.

A candidata contém exclusivamente o contrato canônico `micromodelo.yaml`: schema, fases/condições, proveniência, validador de referência/CI, fixtures sintéticos, suíte com **47 métodos de teste**, documentação e pacote A1. Não cria skill de micromodelos nem altera `.assistant`.

### Primeira A1

A primeira auditoria independente concluiu `NAO_APTA` com cinco bloqueios. Todos foram confirmados como procedentes e corrigidos: continuidade pós-`PUBLICADO` por snapshot anterior confiável, provas auditáveis materialmente preenchidas, `PROPOSTO` permitido pré-gate, política de `INDETERMINADO` mais forte e integridade referencial de calibração.

### Segunda A1

A reauditoria sobre o head corrigido também concluiu `NAO_APTA`, com três novos bloqueios procedentes:

- marcas Unicode `M*` ainda podiam satisfazer provas auditáveis;
- políticas de ausência/publicação ainda dependiam parcialmente de inferência sobre prosa normativa;
- semântica probabilística podia ser escondida por sinônimos não cobertos por regex.

A segunda correção mudou o desenho para eliminar essas classes de bypass:

- materialidade textual exige positivamente letra/número Unicode após NFKC;
- ausência de evidência e política de publicação de `INDETERMINADO` usam somente campos estruturados para comportamento executável;
- `score.tipo_semantica` é a autoridade exclusiva sobre natureza probabilística; `score.semantica` livre foi removido do schema;
- `score.normalizacao` passou a contrato estruturado com método/referência/proveniência.

O workflow transitório `34912665666` executou **26 métodos com `OK`** e o gate estrutural com zero falhas/avisos antes de publicar o commit permanente `f46b69790fc23ac6c3ebfa633053a3acb6f9ed1a`. Os mecanismos transitórios não permanecem na árvore.

Os resultados das duas A1 estão versionados separadamente e continuam historicamente `NAO_APTA`.

### Terceira A1

A terceira auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com três divergências de materialidade textual/Unicode: conflito ASCII no schema, proveniência de topo fora da política material e gates operacionais que aceitavam strings visualmente vazias. O resultado está preservado em `05_resultado_a1_reauditoria_2.md`.

A terceira correção unificou a autoridade em NFKC + letra/número Unicode por `format: material-text`, sem impor essa restrição a toda prosa narrativa. O run transitório `34955861169` executou 29 métodos, CLI positiva/negativa/`--previous` e o gate estrutural antes de publicar `4f686e5de163b649c4ee5e7643f75ecd56db47e7`; os mecanismos transitórios foram removidos.

Os três resultados A1 permanecem históricos e não são reclassificados depois das correções.

### Quarta A1

A quarta auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com uma divergência: regras de evidência/contra-evidência, hipótese/resultado experimental, resumo de validação e motivo operacional ainda escapavam da autoridade comum de materialidade. O resultado está preservado em `06_resultado_a1_reauditoria_3.md`.

A correção reutilizou `material-text` → `_has_material_text` nos seis campos e removeu `.strip()` dos gates de resultado executado e motivo de condição. A suíte passou para 31 métodos. O run transitório `34960256357` executou suíte, CLI adversarial, `--previous` e gates estruturais antes de publicar `8fd8e7892ead1bb63a554b5283f7062adf582976`; os mecanismos transitórios foram removidos.

Os quatro resultados A1 permanecem históricos e não são reclassificados depois das correções.

### Quinta, sexta e sétima A1

A quinta A1 concluiu `APTA_COM_CORRECOES` e levou a política `material-text` aos demais textos obrigatórios, elevando a suíte a 34 métodos. A sexta A1, também `APTA_COM_CORRECOES`, encontrou duas sobras da mesma classe: três regex genéricas concorrentes e um guard que aceitava qualquer `pattern`. O sexto relatório está preservado em `08_resultado_a1_reauditoria_5.md`.

A correção da sexta A1 remove as regex genéricas, exige `material-text` em todo `string + minLength` e congela os únicos patterns estruturais por path + regex exata. A suíte passa a 36 métodos.

A sétima A1, novamente `APTA_COM_CORRECOES`, encontrou três bloqueios: bypass de equivalência por Unicode default-ignorable, guard incompleto para arrays de tipos e aceitação de números não finitos. O sétimo relatório está preservado em `09_resultado_a1_reauditoria_6.md`.

A correção da sétima A1 remove default-ignorables antes da tokenização semântica, fecha o guard para listas contendo `string` e exige `finite-number` para limiar/peso, com JSON estrito contra `NaN/Infinity`. A suíte passa a 39 métodos.

### Oitava A1 e matriz de aceite final

A oitava A1 concluiu `NAO_APTA` e está preservada em `10_resultado_a1_reauditoria_7.md`. O contraditório posterior encerrou as auditorias exploratórias abertas: requisitos reais foram separados de hardening e de adversariais fora do threat model, e `MATRIZ_ACEITE_FINAL.md` foi congelada. A candidata agora usa materialidade baseada em `Default_Ignorable_Code_Point`, equivalência editorial conservadora, domínio numérico canônico, invariantes intrínsecos de aprovação/proveniência, resultado observado apenas após execução, níveis distintos de garantia para snapshot/evolução e perfil canônico de autoria do schema. A suíte passa a 47 métodos.

A skill roteável `hub-ml-micromodelos` pertence à MM04; fingerprint pertence à MM02, descoberta de metadata à MM03 e tracking definitivo à MM06. Este parágrafo registra a divisão histórica do contrato MM01.

## Gate histórico de fechamento da MM01 — já consumido

1. certificar os sete workflows permanentes sobre o HEAD documental final;
2. executar **uma auditoria final fechada contra `MATRIZ_ACEITE_FINAL.md`**, sem permitir expansão implícita de requisitos;
3. executar contraditório final sobre achados que efetivamente violem a matriz/ADRs;
4. se limpa, sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;
5. revalidar a árvore exata após o changelog, reconfirmar `main`/`behind_by`/mergeabilidade e solicitar aceite final explícito;
6. integrar a PR #51 somente após o aceite.

**Naquele gate histórico, MM02 permanecia bloqueada.**


## Estado corrente e próxima decisão

O módulo de domínio foi integrado pela PR #119 em `63601e09` (30/09/2026), como registra o [plano de integração](PLANO_INTEGRACAO_HUB_MICROMODELOS.md). A skill permanece L1/audit. Comece pelo [guia de uso do módulo](../../../ambiente_databricks/.assistant/hub_micromodelos/README.md) ou pelo [quickstart sintético](../../../ambiente_databricks/.assistant/hub_micromodelos/exemplos/recencia_contato/README.md).

E0 sintético, provas E1 Free e E2 corporativo são dimensões separadas. O [plano E2](PLANO_PREPARACAO_E2.md) registra portas ainda não executadas no trabalho. FULL R1 e FULL R2 de MM03 permanecem resultados históricos, sem reclassificação; integração não promove a policy nem homologa fontes corporativas.
