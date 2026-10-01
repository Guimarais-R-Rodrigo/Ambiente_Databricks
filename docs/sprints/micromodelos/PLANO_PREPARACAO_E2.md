# Preparação do piloto E2 de Micromodelos

**Data:** 2026-09-29; atualização de estado em 2026-10-01. **Estado:** `PACOTE_LOCAL_CONFERIDO; FREE_READBACK_PASS; E2_NOT_RUN`. O [laboratório sintético](CHECKPOINT_ACEITE_LAB_2026-09-29.md) foi aceito pelo responsável. B1 e o módulo Micromodelos foram integrados ao `main` pelos PRs #118 e #119; o escopo técnico A da B1 foi aceito e integrado pelos PRs #122 e #123. O kit atualizado do commit `2f5a0cb9` foi gerado com 691 arquivos de produto e passou no aceite E0 extraído. O readback Free 691/691 PASS pertence à versão anterior `63601e09`; o novo kit não foi publicado no Free. Este plano prepara a homologação no Databricks do trabalho e o primeiro micromodelo novo; não registra execução E2, leitura de registros, alteração de ACL ou publicação. Identificadores reais e evidências brutas ficam somente no ambiente autorizado.

## Ordem e limites

O [plano mestre](PLANO_MESTRE.md) e o [ADR-0018](../../decisions/ADR-0018-piloto-novo-antes-legados.md) fixam a sequência: homologar a esteira no trabalho → criar e validar um micromodelo **novo** → obter a publicação institucional, se autorizada → reconciliar runs e Produto de Dados → hardening e freeze V1 → somente então avaliar migração de legados. O [ADR-0017](../../decisions/ADR-0017-governanca-externa-publicacao.md) mantém a autoridade de publicação fora do Hub. O [ADR-0020](../../decisions/ADR-0020-fontes-catalogo-configurado.md) limita a descoberta ao catálogo de Produtos de Dados configurado, salvo decisão humana expressa.

A skill atual é `L1`/`audit`, com contrato estático, sem runner de enforcement ou Receipt próprios. O aceite de laboratório não certifica MM04, não aprova a frente MM03 no destino e não promove a skill a L3. O PR #116 permanece rascunho histórico; sua integração após B1 ocorreu pelo PR #119. O Free comprovou os ensaios E1 anteriores e o readback integral da versão do `main`, sem substituir os testes no destino. O [checklist de transição](../../playbooks/checklist-replicacao.md) exige verificar o gate SE08 vigente antes de **promoção** no trabalho; seu registro atual marca promoção bloqueada enquanto G2 cobrir apenas SE06 → SE07. Staging técnico e ativação pessoal são gates distintos.

## Portas de avanço

| Porta | Preparação e prova mínima | Estado agora | Quem decide/age |
|---|---|---|---|
| G0 — versão e transporte | Fixar SHA, reconciliar interfaces B1/main, validar fonte/derivado e testes pertinentes; obter canal permitido e kit mínimo do mesmo commit, com manifesto. | PASS LOCAL no `main` `2f5a0cb9`: B1/MM integrados, validador 0/0, kit de 691 arquivos e aceite E0 extraído PASS. Canal permitido e instalação no destino ainda exigem G1. | Integrador e responsável pelo repositório. |
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

1. **Agora, local:** preservar o kit do `main` `2f5a0cb9` e seu manifesto. O ZIP extraído passou; o readback Free integral é da versão anterior. Verificar o gate SE08 vigente antes de qualquer promoção.
2. **Com operador autorizado no trabalho:** preencher a ficha institucional acima e executar apenas G1, o staging técnico sintético do [runbook](../../playbooks/replicacao-trabalho.md). Registrar SHA do pacote, checks de integridade, runtime, permissões e custos observados; manter opções MLflow e UC desligadas. Nenhum dado real é necessário nessa porta.
3. **Depois de G1:** decidir G2 e G3 separadamente. Só avançar a leitura de linhas em G4 após escopo, minimização e permissões explícitas. Não transportar o pacote Free como se fosse o kit corporativo; o Free usa outra organização de arquivos e outro gate de autoridade.

## Pré-voos locais

Em 2026-10-01, o kit local do `main` `2f5a0cb94f82b78324f6a79d70af7d03e7b57040` foi gerado em `.artifacts/kit-mm-main-2f5a0cb9-20261001/`, sem upload. O manifesto contém 691 arquivos e tem SHA-256 `82b414f6f2c8ff577f3457c2fbdab8d6daa2625ae4fedd8e8528dd1b9932113e`. Os nove arquivos externos bateram com `SHA256SUMS.txt`; os dois ZIPs não têm paths absolutos ou traversal. O ZIP de produto extraído passou no aceite Micromodelos E0 (integridade, dependências, imports, metadata sintética, contrato, fingerprint, classificação, handoff e catálogo), com `TRUE=1`, `FALSE=2`, `INDETERMINADO=3`. O ZIP de aceite contém dois notebooks sem outputs salvos. `validate_assistant.py` passou com 0 falhas/0 avisos; os testes focais de transição passaram com oito skips (um symlink não disponível no Windows e sete casos Spark local desabilitados), e os cinco testes de aceite Micromodelos passaram. Esta é prova local do pacote fixado, não prova de importação na UI, runtime corporativo ou Genie no destino.

O gerador corporativo `tools/kit_transicao_trabalho.py` produziu **apenas uma prévia local**, em `.artifacts/kit-mm-e2-prep-05c8e01b/`, do commit limpo `05c8e01b59dfebf57d3aa121fd0d2ad9cdd3b035`: manifesto com 582 arquivos de produto, ZIP com 583 entradas incluindo manifesto, sete hashes externos conferidos, zero paths absolutos/traversal/quarentena e presença da skill MM04. SHA-256 do manifesto: `d1e1004bcc8766a971e7c057d7fe239a9a6f78b51c7ad7a29739f77869edc4f8`. Não houve upload, instalação ou execução no trabalho. Esta prévia **não é o artefato de transporte**: a origem ainda não está no remoto, e um kit de uso deve ser regenerado do commit final aprovado conforme o runbook.

Conferência B1 somente leitura: `SKILL.md`, `execution_contract.json` e `policy.json` têm SHA-256 idêntico à candidata local; o checkout compartilhado não foi modificado. O estado documentado em [SE08](../skill_enforcement/SE08/README.md) permanece `PROMOCAO_TRABALHO=BLOQUEADA` por dívida SE06/SE07. Assim, o primeiro trabalho corporativo possível, após autorização e transporte aprovados, é **staging técnico sintético sem ativação**. A decisão de promover fica separada e pendente.

Se uma porta falhar, parar a ação dependente, preservar o resultado e corrigir na fonte canônica. Para staging/promoção, o rollback segue o [runbook](../../playbooks/replicacao-trabalho.md): backup completo antes da mudança, restauração apenas do escopo próprio, preservando alterações alheias e auditando a recuperação. Para o piloto, qualquer limpeza de tabela, run ou artefato exige identificar que foi criado pelo ensaio e respeitar a política local; não há remoção automática neste plano.
