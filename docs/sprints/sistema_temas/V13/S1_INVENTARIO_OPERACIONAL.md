# V13 — S1: inventário e contrato operacional

Data de abertura: 15/09/2026.

Estado: **candidata S1 em branch separada; ainda não aceita nem integrada**.

Base de abertura: `main` `1d46c9625fb5bfd6d1b666ddff055507238788bf`, merge da S0 pela PR #59. O pós-merge da S0 concluiu com 14/14 workflows de `push` em `success`.

## Para quem nunca entrou no Hub

A S1 cria um **mapa de operação**, não um botão novo e não uma automação no Databricks.

O arquivo [`MATRIZ_OPERACIONAL.json`](MATRIZ_OPERACIONAL.json) responde, para cada superfície do Sistema de Temas:

- quem já é o owner canônico;
- onde estão os artefatos reais;
- quais verificações já existem;
- quando uma autorização é necessária;
- qual rollback precisa existir antes de uma mutação;
- qual evidência mínima pode sustentar uma afirmação;
- quais limitações ou bloqueios continuam abertos.

A matriz não copia a configuração visual, os papéis, a matriz AI/BI ou o manifesto de transporte. Ela aponta para os contratos que já existem. Assim, quem precisar saber “qual arquivo devo consultar?” tem uma rota única sem criar uma segunda fonte de verdade.

**S2 não foi implementada.** A S1 registra onde o preflight futuro deverá se apoiar, mas não implementa uma ferramenta de preflight e não decide se um ambiente Databricks está pronto.

Também não houve **nenhuma mutação Databricks** nesta sprint: sem deploy de App, sem ACL/grupos, sem workspace theme, sem `Import theme`, sem `Publish`, sem edição de dashboard e sem persistência no workspace.

## Decisão de arquitetura da S1

O Plano Mestre admite `MATRIZ_OPERACIONAL.json` “ou equivalente”. A S1 usa o JSON porque há requisitos que precisam ser verificáveis por teste e reutilizáveis pela futura S2.

O JSON é deliberadamente **referencial**. Ele não contém:

- cópia dos tokens do tema;
- nova lista de papéis;
- cópia dos três bindings diretos V11;
- cópia dos caminhos protegidos pelo `theme_contract` V09;
- novo schema de tema;
- novo manifesto de implantação.

Esses contratos continuam com seus owners originais. O validador [`tools/temas_v13_operacional.py`](../../../../tools/temas_v13_operacional.py) falha fechado se a matriz tentar introduzir chaves que representem essas duplicações.

## As seis superfícies inventariadas

| `surface_id` | Superfície | Owner primário | Estado operacional importante |
|---|---|---|---|
| `notebook_visual_core` | núcleo notebook / Plotly / HTML | V02, com consumidores V03/V04/V07 | Git/CI; UAT-01 somente na rota textual |
| `visual_lab` | Visual Lab | V05 | `V12-LAB-01 = BLOQUEADO_AUTORIZACAO` |
| `transition_bundle` | kit/bundle de transição | V09 | transporte e integridade; não é instalação |
| `databricks_app` | Databricks App | V10 | `V12-APP-01 = BLOQUEADO_AUTORIZACAO` |
| `aibi_dashboard` | dashboard AI/BI | V11 | `V12-AIBI-01 = PASS` no escopo real limitado; `A11-01 = FAIL` |
| `workspace_theme` | tema de workspace | V11 | `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO` |

A existência de uma linha na matriz não significa que a superfície está homologada. O campo `known_homologation_states` preserva os estados herdados com escopo explícito.

## Dependências e fronteiras V05/V09/V10/V11

A S1 torna explícitas as relações que já existiam sem criar fusões indevidas:

1. **V05 → V02/V03/V04.** O Visual Lab reutiliza o núcleo validado e os consumidores visuais. Ele não é uma segunda engine.
2. **V10 → V05.** O App reutiliza autoria/sessão do Visual Lab. O App não cria novo papel nem uma nova fonte de configuração.
3. **V09 → transporte.** O `theme_contract` e o bundle V09 continuam donos da integridade de transporte. A S1 não copia a lista protegida de caminhos.
4. **V09 ≠ V10 bundle.** O bundle geral de transição e o bundle implantável do App são artefatos diferentes. Um não certifica o outro.
5. **V11 → V02.** A ponte AI/BI projeta a partir de `ResolvedTheme`; não cria `context="aibi"` operacional.
6. **dashboard theme ≠ workspace theme.** As duas superfícies continuam separadas, inclusive para autorização, evidência e rollback.

## Contrato de ação, autorização e rollback

Cada superfície possui um bloco de alto nível `authorization`, `smoke` e `rollback`, mais uma lista `actions`.

Toda ação recebe um dos modos:

- `read_only`;
- `local_artifact_mutation`;
- `persistent_mutation`;
- `remote_mutation`.

A regra fail-closed é simples: qualquer ação que não seja `read_only` deve declarar autorização e rollback. Remover owner, autorização ou rollback torna a matriz inválida.

`performed_by_s1` permanece `false` para todas as ações. Portanto a matriz descreve o contrato, mas a S1 não executa a operação.

Quando um rollback real ainda depende de autorização ou procedimento não observado, a matriz registra isso como bloqueio no texto da estratégia. Ela não inventa que o rollback foi testado.

## Estado herdado que não pode ser agregado

A S1 preserva separadamente:

- `V12-AIBI-01 = PASS` somente para import real de tema em dashboard draft com dados sintéticos e rollback;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

Um `PASS` de uma ação não promove a superfície inteira. Em especial, o PASS de import AI/BI não apaga o FAIL de contraste e não autoriza `Publish` ou workspace theme.

## Validador da S1

`tools/temas_v13_operacional.py` é uma ferramenta **local e read-only de validação de contrato**. Ela:

- rejeita JSON com chaves duplicadas;
- exige exatamente as seis superfícies previstas no Plano Mestre;
- confirma que owners, artefatos, checks, smoke, rollback e evidências apontam para caminhos reais do repositório;
- recusa `Novo_Ambiente_Simulado/` como fonte/owner;
- recusa cópia de contratos canônicos sob chaves como tokens, papéis, bindings ou caminhos protegidos;
- exige autorização e rollback em toda ação mutável;
- exige `performed_by_s1=false`;
- exige `S2_NOT_IMPLEMENTED` no preflight.

Ela não consulta rede, não usa SDK Databricks, não lê workspace, não testa ACL, não valida credencial e não executa operação.

## Testes negativos permanentes

`tools/tests/test_temas_v13_s1.py` inclui mutantes que devem falhar quando:

- um owner é removido;
- o owner aponta para arquivo inexistente;
- uma ação mutável perde autorização;
- uma ação mutável perde rollback;
- autorização ou rollback passam a ser opcionais em mutação;
- a matriz tenta antecipar S2;
- uma ação passa a afirmar execução pela S1;
- um segundo contrato de tokens é embutido.

A suíte também preserva `A11-01 = FAIL`, os três `BLOQUEADO_AUTORIZACAO`, a separação dashboard/workspace e a ausência de cliente de rede/Databricks no validador.

## CI da S1

`.github/workflows/temas-v13-ci.yml` é read-only (`contents: read`). O workflow executa:

- testes específicos da S1;
- regressões `test_temas*.py`;
- compatibilidade V00;
- validador estrutural/documental do Hub.

O workflow não recebe credencial Databricks e não executa deploy.

## Limites desta sprint

A S1 não implementa release/install/update/rollback executável, observabilidade, diagnóstico, compatibilidade de runtime, correção da issue #57, ensaios no ambiente ou handoff final. Essas entregas pertencem às sprints posteriores definidas no Plano Mestre.

A S1 também não altera `ambiente_fonte/` nem `Novo_Ambiente_Simulado/`. Os artefatos de produto permanecem nos owners V01–V12 já integrados.

## Próxima ação

Depois que a candidata S1 tiver CI no SHA exato, reconciliação com a `main` vigente e checkpoint próprio, ela deve ser apresentada ao mantenedor.

**Não iniciar S2 automaticamente.** A ferramenta de preflight unificado pertence à S2 e exige novo aceite.
