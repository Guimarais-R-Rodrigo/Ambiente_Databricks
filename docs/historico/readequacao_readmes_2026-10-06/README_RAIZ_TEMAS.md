# Histórico transferido do README raiz

Texto preservado da baseline `2f5a0cb94f82b78324f6a79d70af7d03e7b57040`. As datas e estados abaixo pertencem à redação anterior; para estado atual consulte o [índice de Temas](../../sprints/sistema_temas/README.md).

## 🎨 Sistema de Temas

V00–V13 estão aceitas e integradas no Git. A V12 foi integrada pela PR #54 no merge `a6309a4d0b3a3530c52330e65ee5a18674118378`, preservando estados honestos distintos: `DOC-02`, `DOC-03`, `SEC-01`, `UAT-01` e `V12-AIBI-01` possuem PASS no alcance documentado; `A11-01` permanece **FAIL** rastreado na issue #57; `V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` permanecem **BLOQUEADO_AUTORIZACAO**. Esses estados não são intercambiáveis.

O Plano Mestre V13 foi aceito e integrado pela PR #58 no merge `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`. S0–S6 foram integradas pelas PRs #59–#65. A **S7 — handoff operacional e fechamento** foi aceita e integrada pela PR #66 no merge `62e9404851d6a7902371bd5b6531a113d521311c`; os **15/15 workflows de `push`** desse SHA concluíram em `success`. A homologação humana S7 está registrada como `HUMAN-01 = PASS`, com participante sanitizado `Tester`, duração de 5 minutos, zero ajuda, zero erros de interpretação e H1–H6 em PASS. Esse resultado é formativo: não constitui production readiness, não autoriza Databricks e não fecha #57. A [auditoria pós-merge V13](../../sprints/sistema_temas/V13/AUDITORIA_POS_MERGE.md) registra a certificação e o drift documental dos índices vivos encontrado após o merge.

A V11 projeta um `ResolvedTheme` `notebook` para capacidades documentadas de temas nativos AI/BI sem criar uma segunda fonte de verdade. `context="aibi"` continua reservado no schema central. A matriz integrada cobre os 48 tokens notebook como **3 traduzidos, 23 aproximados e 22 não suportados**. Como as fontes oficiais verificadas não publicam um schema completo e versionado do JSON produzido por `Export theme`, a V11 não inventa campos nativos: um candidato de importação só pode ser construído sobre um export real fixado por SHA-256 e um binding revisado para campos já existentes.

Regras atuais:

- `ResolvedTheme` continua sendo a fonte configurável de verdade;
- consumidores visuais usam rotas explícitas `_resolvido` quando suportadas;
- aparência não pode alterar cálculo, amostragem, embedding, política de monitoramento ou métricas;
- o template EDA não mantém paleta ou dicionário de tema paralelos;
- o kit V09 exige `theme_contract` v1 com nove caminhos canônicos protegidos por hash;
- transporte é obrigatório, ativação continua `manual_opt_in` e publicação continua `not_performed`;
- a V10 não implementa `context="app"`; o App gerencia propostas `notebook` existentes;
- a V11 não implementa `context="aibi"`, não chama SDK/REST/CLI Databricks e não publica dashboard;
- a V12 não converte CI em homologação de ambiente ou UAT e falha fechado sem autorização, identidade, classificação de dados, evidência ou rollback aplicável;
- o PASS real `V12-AIBI-01` cobre somente import de tema em dashboard draft de teste, e `SEC-01` cobre somente identidade/permissão efetiva observadas; workspace theme, ACL, deploy de App e `Publish` continuam não autorizados;
- tema do workspace e tema local do dashboard têm escopos distintos; reaplicação de workspace theme em dashboard existente é manual, não propagação universal;
- SHAP/Matplotlib e Kaplan–Meier continuam limites explícitos onde o contrato atual não representa a semântica necessária;
- nada disso publica automaticamente no Databricks.

Na V10, os gates Git/CI exercitam identidade sintética, isolamento, persistência V05, bundle implantável derivado e regressões locais. No head reconciliado `cb942ee955ff9236f19099e5ed4ceee9beb32000`, os dez workflows reais de PR concluíram com `success`; depois do merge `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`, os 12 workflows disparados por `push` na `main` também concluíram em `success`, incluindo o workflow V10 `34896944061`. Isso **não** comprova headers reais, permissões/grupos do workspace, UC Volume real, browser, acessibilidade, concorrência multiusuário ou UAT. Nenhuma criação/atualização de Databricks App foi executada por essa sprint.

Estado corrente: [V13](../../sprints/sistema_temas/V13/README.md) está encerrada no Git e sua [auditoria pós-merge](../../sprints/sistema_temas/V13/AUDITORIA_POS_MERGE.md) preserva os limites e dívidas transferíveis. O [Plano Mestre V14](../../sprints/sistema_temas/V14/PLANO_MESTRE.md) foi aceito e integrado pela PR #70 no merge `350dcf0b37e730042ef961f12f11b30b2660d2c6`. A **S0 V14 foi aceita e integrada pela PR #71** no merge `e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493`; os **16/16 workflows de `push`** desse SHA concluíram em `success`. A V14 está agora na **S1 — ownership, autoridade e modelo operacional**, documentada no [README V14](../../sprints/sistema_temas/V14/README.md), na [matriz de ownership](../../sprints/sistema_temas/V14/MATRIZ_OWNERSHIP.json), no [runbook S1](../../sprints/sistema_temas/V14/S1_MODELO_OPERACIONAL.md) e no [checkpoint S1](../../sprints/sistema_temas/V14/CHECKPOINT_S1.md). A S1 mantém owner/backup/autoridade não evidenciados em `BLOCKED`; **S2–S8 não foram iniciadas**, nenhuma decisão de production readiness/go-live foi tomada e nenhuma autorização Databricks decorre da S1. O fechamento herdado permanece em [V12](../../sprints/sistema_temas/V12/README.md) e [escopo/aceite V12](../../sprints/sistema_temas/V12/ESCOPO_E_ACEITE.md).

