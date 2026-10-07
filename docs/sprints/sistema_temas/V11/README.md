# V11 — temas nativos Databricks AI/BI

> **Nota administrativa — 06/10/2026.** Este documento preserva o escopo e a próxima ação previstos no fechamento original. [Estado atual de Temas](../README.md) é o dono da continuidade; não repetir gates antigos por inferência. A [prova real posterior V12-AIBI-01](../V12/evidencias/V12-AIBI-01/README.md) cobre somente import em dashboard draft; não pertence ao ensaio original V11.

## Registro histórico preservado

## Estado

**ACEITA E INTEGRADA NO GIT; FECHAMENTO DOCUMENTAL PÓS-MERGE; SEM HOMOLOGAÇÃO OU OPERAÇÃO REAL NO DATABRICKS.**

Base de início: `a9480391c78e2402986885db0ce08b10e0619a1a`, fechamento documental da V10.

Branch funcional: `codex/temas-v11-aibi-20260914`.

Head final aceito: `5532ca6d8f1b243ca705088f4b57823a333b9b1f`.

PR funcional: **#52**.

Merge funcional na `main`: `9305bc49eaf002caec042361bf35efa66af7ca18`.

Rodrigo deu aceite explícito em 14/09/2026. Os 11 workflows reais da PR #52 concluíram com `success`; após o merge, os 13 workflows disparados por `push` no commit `9305bc49eaf002caec042361bf35efa66af7ca18` também concluíram com `success`.

## Objetivo entregue

A V11 cria a ponte entre o Sistema de Temas do Hub e as capacidades nativas de tema de dashboards Databricks AI/BI, sem criar uma segunda fonte de verdade e sem inventar o formato interno do JSON exportado pelo produto.

O escopo entregue inclui:
- dashboard sintético local, explicitamente não importável;
- mapeamento de tokens como **traduzidos**, **aproximados** ou **não suportados**;
- projeção/exportação controlada do Hub;
- binder fail-closed para um eventual export nativo real fixado por SHA-256;
- distinção entre tema do workspace e tema local/custom do dashboard;
- políticas locais para admin, draft, snapshot e reaplicação;
- documentação de primeiro uso e limites;
- testes permanentes e CI read-only.

## Decisão arquitetural

`ResolvedTheme` continua sendo a fonte configurável de verdade. A V11 **não** altera `theme.schema.json` e **não** torna `context="aibi"` válido.

Isso é deliberado: a documentação oficial verificada descreve capacidades de tema e oferece `Export theme` / `Import theme`, mas não publica um schema estável e completo do JSON de tema exportado. Alterar o contrato central ou gerar um JSON supostamente nativo sem esse contrato criaria uma interpretação paralela e insegura.

A ponte fica em `ambiente_databricks/.assistant/hub_padroes/identidade_visual/aibi/` e possui espelho byte a byte na [saída gerada vigente](../../../manutencao/saida-gerada.md), `.artifacts/simulado/`. `Novo_Ambiente_Simulado` é o nome preservado nas evidências históricas da V11.

## Como a projeção funciona

`project_theme()` recebe exclusivamente um `ResolvedTheme` `notebook`, revalida o tema pelo núcleo V02 e aplica a matriz canônica `aibi_mapping.json`.

A matriz cobre exatamente os 48 tokens notebook:
- **3 translated**: equivalência direta suficiente;
- **23 approximated**: capacidade parecida, mas exige decisão/revisão;
- **22 unsupported**: sem equivalência segura no contrato oficial verificado.

Somente itens `translated` podem possuir `binding_strategy="direct"`.

A projeção exportada pelo Hub possui formato próprio `hub-aibi-theme-projection`. Ela é auditável, determinística e registra fingerprint/hash do tema de origem, mas **não é arquivo nativo para Import theme**.

## Conversão para template nativo

`bind_native_template()` existe para evitar hardcode de um schema não documentado. A função exige:
1. bytes de um tema realmente exportado;
2. SHA-256 exato desses bytes no binding;
3. JSON Pointers revisados para campos que já existam no template;
4. capacidade classificada como `translated/direct`.

A função não cria campos inexistentes, não automatiza aproximações, não aplica itens não suportados e preserva campos desconhecidos do template. O resultado permanece `locally_bound_not_databricks_validated`.

Nenhum binding nativo foi distribuído pela V11 porque não houve export autorizado de um workspace real.

## Workspace theme × dashboard theme

A documentação oficial verificada em 14/09/2026 estabelece:
- gerenciar tema do workspace exige administrador do workspace;
- dashboards novos herdam o tema do workspace configurado;
- ao aplicar o tema do workspace a um dashboard existente, o dashboard recebe um **snapshot**;
- alterações posteriores no tema do workspace **não** se propagam automaticamente para dashboards existentes;
- dashboards existentes precisam de reaplicação manual;
- remover o tema do workspace não remove o snapshot já aplicado;
- configurações de tema do dashboard são acessíveis em dashboards draft;
- `Color mappings` são uma capacidade local ao dashboard;
- seleção/importação de tema e publicação são ações separadas.

A V11 codifica essas propriedades apenas como política local testável; não consulta permissões reais.

## Dashboard sintético

`dashboard_sintetico.json` é um fixture do projeto com KPI, linha, barras, tabela, texto, duas queries e dois filtros sintéticos. Ele serve para descrever a primeira jornada de dashboard draft, exercitar categorias e calcular fingerprint da semântica.

O arquivo declara `databricks_importable=false`: **não é formato Databricks** e não deve ser importado no workspace.

## Evidência técnica final

O head final `5532ca6d8f1b243ca705088f4b57823a333b9b1f` passou o run pré-PR `34905080083` integralmente:
- suíte V11: **21/21 PASS**;
- sintaxe em memória: **PASS**;
- regressões V01–V11: **457/457 PASS**;
- V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- escopo V11: **PASS**;
- source/simulado equivalentes;
- workflow com `Contents: read` e checkout sem credenciais persistentes.

Na PR #52, **11/11 workflows reais de `pull_request`** concluíram com `success`. Depois do merge `9305bc49eaf002caec042361bf35efa66af7ca18`, **13/13 workflows de `push`** concluíram com `success`.

Os failures `34900693160`, `34901091132`, `34901776770` e `34904363803` permanecem registrados como **FAILURE** em `TESTES.md`; nenhum failure ou `SKIP` foi reclassificado.

## O que PASS não prova

PASS local/GitHub não prova formato nativo real do JSON exportado, importação real, criação de dashboard, permissões reais, aplicação real de workspace theme, snapshot/reaplicação no ambiente de trabalho, preservação de queries/filtros em dashboard real, renderização, acessibilidade, UAT ou publicação.

Esses itens exigem ambiente autorizado e não são convertidos em PASS por inferência.

## Fronteira com V12

A V11 está fechada no Git após a integração desta reconciliação documental. A V12 permanece uma sprint separada, reservada para homologação de jornadas com pessoas/ambiente e só deve partir da `main` já reconciliada. Nenhuma operação real no Databricks é autorizada por este fechamento.