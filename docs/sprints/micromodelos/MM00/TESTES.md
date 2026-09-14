# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git e reconciliação

**Abertura:** `micromodelos/mm00-baseline` nasceu da `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.

**Concorrência V08:** durante a MM00, a V08 foi integrada por `622d2c962a80998cf990b57036f7ae503bfc0458` e fechada documentalmente em `55f7006c47d90ae7f760992d252b658f53a59636`. A MM00 foi reconciliada com essa base em `edfcf58e4700ccf5d58d2befddccbd9fe50ac124`.

**Concorrência V09:** depois da A1, a V09 foi integrada pelo PR #45 em `0f7234c4734f1974ebb1a20123f3c26626c67ef3`; a correção de preparação Node do workflow operacional levou a `main` a `4ae714a35a0aafd930a8cd796d962b0a79449b88`. A MM00 incorporou essa base por merge de dois pais em `922ae38491cb7a502b834b092ea637620b54300a`.

**Status:** PASS estrutural. Reconsultar `main` imediatamente antes do aceite/merge.

## T02 — Estado visual

**Esperado:** o plano não pode depender de fotografia desatualizada de outra frente.

**Observado na base reconciliada:** V00–V09 estão integradas no Git. V08 cobre integração transversal; V09 leva o contrato temático ao kit offline de transição e não converte transporte em publicação/ativação.

**Conclusão:** o framework de micromodelos deve respeitar a frente temática vigente desde a criação de futuras skills, enquanto a composição visual específica continua adiada para MM11.

**Status:** PASS arquitetural. A A1 confirmou a fronteira visual proposta; a reconciliação V09 não a altera.

## T03 — Colisão nominal

**Método:** busca por `micromodel` na `main` de abertura.

**Observado:** nenhum resultado específico encontrado.

**Status:** PASS delimitado ao repositório. Não prova inexistência no ambiente de trabalho.

## T04 — Taxonomia do Hub

**Esperado:** micromodelo não vira sétimo tipo.

**Evidência:** `hub_padroes/skill/template.md` e `hub-ml-criar-objeto` tratam a lista de seis tipos como fechada.

**Status:** PASS. A A1 confirmou a interpretação.

## T05 — Reuso de componentes

**Esperado:** mapear cobertura atual antes de criar novos objetos.

**Evidência:** `MATRIZ_REUSO.md` classifica Concierge, EDA, cross-EDA, feature engineering, validação, auditoria, `schema_to_yaml`, helpers Spark e `mlflow_run`.

**Status:** PASS. A A1 confirmou existência e fronteira dos componentes classificados como REUSAR/ADAPTAR.

## T06 — Sanitização

**Esperado:** nenhum identificador/path real do ambiente externo no framework versionado.

**Primeira rodada:** o CI detectou um handle corporativo histórico no ADR-0017.

**Correção:** o handle foi removido e substituído por contrato genérico de handoff. Rodadas posteriores passaram a validação sem novo achado.

**A1:** PASS sem identificador externo encontrado no diff auditado.

**Status:** PASS.

## T07 — Migração tardia

**Esperado:** skill/briefing de migração não existem antes do piloto greenfield e freeze V1.

**Evidência:** Plano Mestre posiciona migração em MM12; ADR-0018 permanece proposto.

**A1:** confirmou que nenhuma dependência da fundação exige a skill de migração antecipadamente.

**Status:** PASS.

## T08 — Tracking separado da especificação

**Esperado:** YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking.

**Evidência:** Plano Mestre e ADR-0016 proposto.

**A1:** confirmou que o helper atual de MLflow não satisfaz ainda o perfil rule-based e que a adaptação foi corretamente adiada, sem promessa falsa de capacidade existente.

**Status:** PASS arquitetural; implementação somente em sprint futura.

## T09 — Não alteração funcional pela MM00

**Esperado:** a iniciativa MM00 não cria/modifica funcionalidade do produto.

**Após a reconciliação V09:** antes da atualização do README raiz, a comparação da PR #43 contra `main=4ae714a3...` continha 22 arquivos, todos contexto/ADRs/documentação MM00. Nenhum arquivo funcional V09 aparecia no diff.

A atualização posterior do README raiz serve somente para registrar V09 como estado vigente e sincronizar as métricas medidas do gate, elevando o diff nominal esperado para 23 arquivos.

Nenhum arquivo MM00 próprio pertence a `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou `.github/workflows/`.

**A1:** PASS para ausência de mudança funcional no head auditado; a bateria final deve reconfirmar o escopo pós-V09.

**Status:** PASS nominal, sujeito à última conferência.

## T10 — Validação automática

### Snapshot auditado

No head `f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843`, CI geral, V00, V01 e V02 estavam em `success` antes da A1.

### Pós-A1 / base V08

A inclusão de `03_resultado_a1.md` elevou a identidade medida de 1368 para 1369 arquivos, mantendo 1859 links. O CI geral `34878871911` reprovou exclusivamente a contagem congelada 1368; as demais etapas e V00/V01/V02 passaram.

### Pós-reconciliação V09

No head `922ae38491cb7a502b834b092ea637620b54300a`:

- V00 `34881774750`: `success`;
- V01 `34881774788`: `success`;
- V02 `34881774645`: `success`;
- CI geral `34881774760`: `failure` exclusivamente na validação do bloco congelado do README raiz.

O próprio gate mediu **1374 arquivos / 1859 links**. As etapas `temas`, `biblioteca`, `ferramentas`, `transicao`, `readmes`, `concierge-pacote`, `concierge-regressoes` e `concierge-integracao` passaram nessa mesma execução. O README raiz foi reconciliado para 1374/1859 sem relaxar validador e preservando os dois links Markdown já existentes da V08 para não alterar a métrica por efeito editorial.

**Status:** PENDENTE apenas da bateria final sobre o head documental reconciliado.

## T11 — Auditoria independente A1

Pacote:

- `docs/auditoria/2026-09-14_micromodelos-mm00/01_contexto.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/02_prompt_auditoria.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/03_resultado_a1.md`.

**Resultado:** `APTA_COM_CORRECOES`.

Achados:

- Q-01 — falta de entrada própria MM00 no `CHANGELOG.md`: **PROCEDE e continua bloqueador**;
- M-01 — cronologia do baseline não reconciliada uniformemente: **PROCEDE e foi corrigido**;
- `DIVERGE`: nenhum achado atribuível à MM00.

A A1 também confirmou como adequadamente diferidas para MM01/MM02 as decisões de encoding do YAML, máquina de estados detalhada e materialidade fina do fingerprint.

**Status:** EXECUTADA; M-01 fechado, Q-01 aberto.

## T12 — Contexto canônico

**Esperado:** `CLAUDE.md` reflete a `main` vigente e não transforma ADR proposto em decisão ativa.

**Observado após reconciliação V09:** `CLAUDE.md` registra V00–V09 integradas, distingue transporte de ativação/publicação, registra a A1 da MM00 e mantém ADR-0014 a ADR-0020 como propostos.

**Status:** PASS documental, sujeito ao CI final e nova reconsulta da `main`.

## T13 — Regra de changelog

`CLAUDE.md` exige entrada em `CHANGELOG.md` para toda sessão que altera algo.

A A1 classificou a ausência da entrada MM00 como **QUEBRA Q-01**. Uma tentativa de atualização por substituição integral acrescentou o bloco desejado, porém também reformatou duas linhas históricas e corrigiu inadvertidamente um typo antigo. O patch detectou as três mudanças laterais; a tentativa foi recusada e o blob histórico original `2095dbcf1dd6b99e7ff008a9180361702222092b` foi restaurado integralmente por SHA.

A reconciliação V09 preservou esse mesmo blob oficial. Assim, nenhuma entrada histórica permanece modificada, mas a entrada MM00 ainda não existe.

**Status:** BLOQUEIO CONHECIDO. Não converter em PASS sem atualização estritamente aditiva comprovada ou exceção humana explícita e registrada.

## Critério final

PASS global exige T01–T13 resolvidos, diff da MM00 delimitado contra a `main` vigente, CI verde no head final e aceite humano explícito.

Neste momento, o único bloqueio de conteúdo conhecido é T13/Q-01. A bateria automática final ainda precisa confirmar o head documental reconciliado com V09.