# V11 — temas nativos Databricks AI/BI

## Estado

**CANDIDATA TÉCNICA COM HEAD DOCUMENTAL REVALIDADO; PR AINDA NÃO VALIDADA; SEM ACEITE, MERGE OU OPERAÇÃO NO DATABRICKS REAL.**

Base de início: `a9480391c78e2402986885db0ce08b10e0619a1a`, fechamento documental da V10.

Branch: `codex/temas-v11-aibi-20260914`.

Primeiro head integralmente verde: `0d3180c50428d8716b44f264b915a91243ba96c3`, run `34902083889`.

Head documental reconciliado e revalidado antes deste registro final: `5bb8234422fdd284a9e14815ef566ec0b52a2952`, run `34902853430`.

## Objetivo

A V11 cria a ponte entre o Sistema de Temas do Hub e as capacidades nativas de tema de dashboards Databricks AI/BI, sem criar uma segunda fonte de verdade e sem inventar o formato interno do JSON exportado pelo produto.

O escopo recuperado do plano V00–V14 exige:
- primeiro dashboard sintético em draft;
- mapeamento de tokens como **traduzidos**, **aproximados** ou **não suportados**;
- conversão/exportação controlada;
- distinção entre tema do workspace e tema local/custom do dashboard;
- testes de permissões administrativas, personalização local, categorias, reaplicação e preservação da semântica;
- documentação de aplicação seletiva;
- nenhuma promessa de propagação universal.

## Decisão arquitetural

`ResolvedTheme` continua sendo a fonte configurável de verdade. A V11 **não** altera `theme.schema.json` e **não** torna `context="aibi"` válido.

Isso é deliberado: a documentação oficial verificada descreve capacidades de tema e oferece `Export theme` / `Import theme`, mas não publica um schema estável e completo do JSON de tema exportado. Alterar o contrato central ou gerar um JSON supostamente nativo sem esse contrato criaria uma interpretação paralela e insegura.

A ponte fica em `ambiente_fonte/.assistant/hub_padroes/identidade_visual/aibi/` e possui espelho byte a byte em `Novo_Ambiente_Simulado`.

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

Nenhum binding nativo é distribuído pela V11 porque ainda não houve export autorizado de um workspace real.

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

## Evidência técnica obtida

No primeiro run verde `34902083889`, head `0d3180c50428d8716b44f264b915a91243ba96c3`, passaram 21/21 V11, 457/457 regressões V01–V11, V00 12/12, validador 0/0 e escopo.

Depois da reconciliação de navegação/documentação, o run `34902853430`, no head `5bb8234422fdd284a9e14815ef566ec0b52a2952`, repetiu o gate completo em **SUCCESS**:
- suíte V11: **21/21 PASS**;
- sintaxe em memória: **PASS**;
- regressões V01–V11: **457/457 PASS**;
- V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- escopo V11: **PASS**;
- source/simulado equivalentes;
- workflow com `Contents: read` e checkout sem credenciais persistentes.

Os failures anteriores `34900693160`, `34901091132` e `34901776770` permanecem registrados como **FAILURE** em `TESTES.md`.

## Critérios de aceite Git da candidata

A V11 só pode pedir aceite quando:
1. matriz cobre exatamente os 48 tokens notebook;
2. classificações e estratégias são fechadas/fail-closed;
3. `aibi` continua reservado no schema central;
4. projeção revalida `ResolvedTheme`;
5. export da projeção é determinístico;
6. binder exige hash exato do template;
7. binder recusa automação de aproximações;
8. binder recusa path inexistente/colisão/tipo incompatível;
9. políticas distinguem workspace, dashboard e publicação;
10. guardas administrativas/draft falham fechado;
11. fixture sintético não se declara importável;
12. fingerprint semântico não muda por metadado visual;
13. fonte e espelho são byte a byte equivalentes;
14. workflow é read-only e não chama API/CLI/SDK Databricks;
15. regressões V01–V11 e V00 permanecem verdes;
16. validador estrutural/documental termina com 0 falhas / 0 avisos;
17. o head documental final repete o gate completo e os checks reais da PR ficam verdes.

Os itens 1–16 estão comprovados no head documental revalidado. O item 17 permanece pendente até a abertura e execução dos checks reais da PR no novo head documental final.

## O que PASS não prova

PASS local/GitHub não prova formato nativo real do JSON exportado, importação real, criação de dashboard, permissões reais, aplicação real de workspace theme, snapshot/reaplicação no ambiente de trabalho, preservação de queries/filtros em dashboard real, renderização, acessibilidade, UAT ou publicação.

Esses itens exigem ambiente autorizado e não serão convertidos em PASS por inferência.

## Fronteira com V12

V12 continua reservada para homologação de jornadas com pessoas/ambiente. V11 não inicia V12.
