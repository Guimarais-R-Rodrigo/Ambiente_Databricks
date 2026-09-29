# Preparação do piloto E2 de Micromodelos

**Data:** 2026-09-29. **Estado:** `PLANO_PRONTO; E2_NOT_RUN`. O [laboratório sintético](CHECKPOINT_ACEITE_LAB_2026-09-29.md) foi aceito pelo responsável. Este plano prepara a homologação no Databricks do trabalho e o primeiro micromodelo novo; não autoriza acesso corporativo, instalação, leitura de registros, alteração de ACL ou publicação. Identificadores reais e evidências brutas ficam somente no ambiente autorizado.

## Ordem e limites

O [plano mestre](PLANO_MESTRE.md) e o [ADR-0018](../../decisions/ADR-0018-piloto-novo-antes-legados.md) fixam a sequência: homologar a esteira no trabalho → criar e validar um micromodelo **novo** → obter a publicação institucional, se autorizada → reconciliar runs e Produto de Dados → hardening e freeze V1 → somente então avaliar migração de legados. O [ADR-0017](../../decisions/ADR-0017-governanca-externa-publicacao.md) mantém a autoridade de publicação fora do Hub. O [ADR-0020](../../decisions/ADR-0020-fontes-catalogo-configurado.md) limita a descoberta ao catálogo de Produtos de Dados configurado, salvo decisão humana expressa.

A candidata atual é skill `L1`/`audit`, contrato estático, sem runner ou Receipt. O aceite de laboratório não certifica MM04, não aprova a frente MM03 no destino e não promove a skill a L3. O Free comprovou apenas o ambiente E1 e os bytes do kit r4. A PR #116 ainda não foi integrada; GitHub Actions permanece `BLOCKED_EXTERNAL_CI` por saldo, e a branch possui commits locais não enviados. O [checklist de transição](../../playbooks/checklist-replicacao.md) exige verificar o gate SE08 vigente antes de **promoção** no trabalho; seu registro atual marca promoção bloqueada enquanto G2 cobrir apenas SE06 → SE07. Staging técnico e ativação pessoal são gates distintos.

## Portas de avanço

| Porta | Preparação e prova mínima | Estado agora | Quem decide/age |
|---|---|---|---|
| G0 — versão e transporte | Fixar SHA, reconciliar interfaces B1/main, validar fonte/derivado e testes pertinentes; obter canal permitido e kit mínimo do mesmo commit, com manifesto. | PENDENTE: integração Git e CI remoto indisponível. | Integrador e responsável pelo repositório. |
| G1 — staging sem dados reais | Confirmar autorização de upload/compute; aplicar o [runbook](../../playbooks/replicacao-trabalho.md) em pasta pessoal de staging, fazer backup verificável, conferir hashes/tipos, imports e casos sintéticos. Não ativar skill nem consultar tabelas. | NOT_RUN. | Operador no computador do trabalho e responsável pela instalação. |
| G2 — promoção pessoal e Genie | Revalidar SE08 e obter aceite específico da promoção; preservar terceiros/MCP/instruções existentes, ativar seletivamente, repetir testes e casos Genie com `@hub-ml-micromodelos` em chats novos. | BLOQUEADO até gate SE08 e autorização específicos; evidência Free não substitui teste E2. | Responsável pelo Hub/SEF e operador autorizado. |
| G3 — descoberta metadata-only | Configurar **no destino** `<CATALOGO_PRODUTO>` e escopo de schemas permitido; comprovar acesso às views de metadata e registrar `OBSERVED/DENIED/UNAVAILABLE/PARTIAL` e `ESCOPO_OBSERVADO`. Sem `SELECT` de linhas, amostragem ou `count(*)`. | NOT_RUN; binding e escopo reais ausentes. | Dono do dado e operador com permissão de metadata. |
| G4 — piloto greenfield com dados | Selecionar decisão nova, população, entidade/grão, instante/horizonte, evidências/contra-evidências, rubrica de `INDETERMINADO` e score; aprovar necessidade de leitura, minimização, permissões, compute e retenção. Versionar YAML e evidências **somente no destino**. Separar DEVELOPMENT de VALIDATION com plano efetivo; mesmas linhas não constituem holdout. | NOT_RUN; depende de decisões e autorização institucional. | Dono de negócio, dono dos dados, ciência de dados e governança aplicável. |
| G5 — handoff, scoring e reconciliação | Revisar contrato/MLflow/artefatos; governança externa decide geração/validação/publicação do Produto de Dados. Se publicado, executar SCORING autorizado e reconciliar população, contagens e cobertura de score com resultado governado. `SUPPLIED_UNVERIFIED` não vira medido por declaração. | NOT_RUN; publicação não autorizada. | Autoridade institucional de publicação e responsáveis técnicos. |
| G6 — hardening e V1 | Medir uso da esteira e limitações, avaliar integração visual/monitoramento disponíveis; corrigir falhas, congelar V1 após revisão. Migração MM12 requer gate próprio e equivalência real. | NOT_RUN. | Responsáveis de produto, técnica e governança. |

Cada porta conserva evidência própria. Falha ou capacidade ausente permanece `FAIL`, `DENIED`, `UNAVAILABLE` ou `NOT_RUN`; não é convertida em PASS por um teste anterior. A permissão de metadata não concede leitura de registros; SELECT não concede escrita/publicação. `current_level=L1` governa a capacidade presente.

## Registro de decisão a preencher somente no trabalho

Não preencher com nomes corporativos neste repositório. O operador mantém a ficha no canal institucional aprovado e devolve aqui apenas estado sanitizado por porta.

| Campo a decidir | Resposta esperada no ambiente autorizado |
|---|---|
| Patrocinador e dono da decisão | Quem solicita e quem aceita o objetivo e os critérios de negócio. |
| Operador e ambiente de teste | Quem pode instalar em staging pessoal, qual compute e limite de custo; confirmação de backup e janela. |
| Catálogo e escopo de metadata | Binding do catálogo de Produtos de Dados e schemas/objetos autorizados; permissão de metadata separada. |
| Candidata greenfield | Decisão nova, população, entidade/grão, instante de decisão e horizonte; sem reaproveitar legado como primeiro piloto. |
| Acesso a registros | Tabelas/colunas e intervalo mínimos, fundamento institucional, autorizações de SELECT e tratamento de dados; plano para não exportar linhas. |
| Classificação e score | Critérios TRUE/FALSE/INDETERMINADO, contra-evidência, semântica/limiar do score e quem aprova mudanças. |
| Tracking e resultados | Experimento autorizado, métricas agregadas, local governado dos resultados individuais, retenção, acesso e auditoria. |
| Publicação e rollback | Autoridade externa, pontos de aceite, objetos próprios que poderão ser revertidos e política de preservação de evidência. |

## Primeira execução recomendada

1. **Agora, local:** manter esta candidata e suas evidências no Git local; reconciliar a versão quando GitHub/CI voltar, sem chamar `BLOCKED_EXTERNAL_CI` de PASS. Verificar a versão atual dos gates B1/SE08 antes de preparar transporte.
2. **Com operador autorizado no trabalho:** preencher a ficha institucional acima e executar apenas G1, o staging técnico sintético do [runbook](../../playbooks/replicacao-trabalho.md). Registrar SHA do pacote, checks de integridade, runtime, permissões e custos observados; manter opções MLflow e UC desligadas. Nenhum dado real é necessário nessa porta.
3. **Depois de G1:** decidir G2 e G3 separadamente. Só avançar a leitura de linhas em G4 após escopo, minimização e permissões explícitas. Não transportar o pacote Free como se fosse o kit corporativo; o Free usa outra organização de arquivos e outro gate de autoridade.

Se uma porta falhar, parar a ação dependente, preservar o resultado e corrigir na fonte canônica. Para staging/promoção, o rollback segue o [runbook](../../playbooks/replicacao-trabalho.md): backup completo antes da mudança, restauração apenas do escopo próprio, preservando alterações alheias e auditando a recuperação. Para o piloto, qualquer limpeza de tabela, run ou artefato exige identificar que foi criado pelo ensaio e respeitar a política local; não há remoção automática neste plano.
