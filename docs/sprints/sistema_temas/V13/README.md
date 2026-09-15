# V13 — consolidação operacional do Sistema de Temas

## Estado vigente

A V13 está em **S0 — reconciliação pós-V12 e freeze de escopo**, em candidata documental separada. A base inicial real da S0 é a `main` `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`, merge da PR #58.

A PR #58 integrou o [Plano Mestre V13](PLANO_MESTRE.md). O texto do plano preserva o estado em que foi escrito, antes de seu aceite; este README é a superfície viva para o estado posterior à integração. Alterar o estado corrente aqui não reescreve a evidência histórica nem modifica silenciosamente o plano aceito.

**S1 não foi iniciada.** A S0 não cria `MATRIZ_OPERACIONAL.json`, preflight, runbook executável, workflow V13, código de release/rollback nem qualquer alteração de runtime.

Para quem nunca entrou no Hub: nesta etapa não há nada para instalar, executar ou alterar no Databricks. A S0 apenas alinha a documentação ao estado real, confirma quem é dono de cada contrato e congela a fronteira entre V13 e V14.

## Plano canônico e limite desta S0

O [Plano Mestre](PLANO_MESTRE.md) é o contrato aceito da V13. A S0 pode registrar o estado posterior à sua integração, mas não pode redefinir silenciosamente seu conteúdo.

A V13 permanece a etapa de **consolidação operacional**: inventário operacional, preflight, release/install/update/rollback, observabilidade técnica, diagnóstico, compatibilidade e acessibilidade operacional, ensaios autorizados e handoff.

A V14 permanece responsável por **production readiness e suporte sustentado**: ownership operacional definitivo e substitutos, incidentes/severidades formais, SLA/SLO somente quando houver base real, custos observados, retenção/housekeeping final, escalonamento, calendário de revisão/depreciação e decisão final de go-live/uso compartilhado.

Essa fronteira é explicada em detalhe na seção 9 do Plano Mestre. A S0 não antecipa nenhuma dessas implementações.

## Estado herdado da V12

A V12 foi aceita e integrada pela PR #54 no merge `a6309a4d0b3a3530c52330e65ee5a18674118378`. Os estados herdados permanecem distintos:

| Caso | Estado herdado | Regra V13 |
|---|---|---|
| `DOC-02` | `PASS` | preservar evidência V12 |
| `DOC-03` | `PASS` | preservar evidência V12 |
| `SEC-01` | `PASS` de ambiente | não generalizar para outras autorizações |
| `UAT-01` | `PASS` da rota textual | não confundir com browser/runtime do Visual Lab |
| `V12-AIBI-01` | `PASS` real em dashboard draft sintético + rollback | não confundir com Publish ou workspace theme |
| `A11-01` | `FAIL` | dívida real na issue #57 |
| `V12-LAB-01` | `BLOQUEADO_AUTORIZACAO` | nova execução exige autorização específica |
| `V12-APP-01` | `BLOQUEADO_AUTORIZACAO` | deploy/rollback real exige autorização específica |
| `V12-AIBI-02` | `BLOQUEADO_AUTORIZACAO` | workspace theme/admin exige autorização específica |

`FAIL`, `BLOQUEADO_AUTORIZACAO`, `NOT_APPLICABLE` e `PASS` continuam estados diferentes. Nenhum deles pode ser promovido por inferência.

## Owners canônicos V01–V12

Este mapa é de navegação. Ele aponta para os donos já integrados e **não copia seus contratos como nova fonte de verdade**.

| Camada | Owner canônico | O que a V13 deve fazer |
|---|---|---|
| papéis, estados e transições de governança | [V01](../V01/README.md) | referenciar; não criar segunda política de papéis |
| schema, parsing, validação e `ResolvedTheme` | [V02](../V02/README.md) | reutilizar; não criar segundo schema/resolvedor |
| adaptação Plotly | [V03](../V03/README.md) | consumir sem redefinir tokens |
| HTML, estilos e tabelas | [V04](../V04/README.md) | consumir sem CSS temático paralelo |
| Visual Lab, draft, comparação, sessão e histórico | [V05](../V05/README.md) | reutilizar como superfície de autoria |
| assets e geração editorial | [V06](../V06/README.md) | preservar hashes e derivação controlada |
| consumidores visuais adicionais | [V07](../V07/README.md) | preservar cálculo separado de aparência |
| integração transversal com skills/padrões/Manual | [V08](../V08/README.md) | manter orientação apontando para os mesmos owners |
| transporte, kit e `theme_contract` | [V09](../V09/README.md) | reutilizar; não criar manifesto concorrente |
| Databricks App | [V10](../V10/README.md) | tratar como superfície operacional própria |
| ponte AI/BI | [V11](../V11/README.md) | preservar fail-closed e os três bindings diretos |
| protocolo, evidência e homologação | [V12](../V12/README.md) | preservar classes de evidência e bloqueios honestos |

## Contratos que a S0 não reabre

Continuam congelados:

- `ResolvedTheme` é a fonte configurável de verdade;
- `context="aibi"` permanece reservado;
- a matriz V11 permanece com 48 tokens: 3 `translated`, 23 `approximated` e 22 `unsupported`;
- somente `surface.card -> widget.background`, `palette.categorical -> visualization.categorical_palette` e `card.radius_px -> widget.corner_radius` podem ter binding direto;
- `dashboard_sintetico.json` continua não importável no Databricks;
- `approximated` e `unsupported` não são automatizados;
- dashboard theme e workspace theme são superfícies distintas;
- `Import theme` e `Publish` são gates independentes;
- Git permanece a fonte canônica do projeto; `ambiente_fonte/` é fonte editável e `Novo_Ambiente_Simulado/` é derivado.

## Dívidas e bloqueios herdados

Na abertura da S0, a busca por issues abertas do repositório encontrou somente a issue #57 relacionada ao Sistema de Temas. Ela preserva `A11-01 = FAIL` para contraste de formatação condicional explícita e **não autoriza ampliar silenciosamente a V11**.

Os três casos ambientais bloqueados da V12 também permanecem no baseline: `V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02`. Ausência de autorização é bloqueio, não erro técnico.

Se uma subfase futura identificar nova dívida com evidência concreta, ela poderá ser registrada no momento apropriado. A S0 não cria dívida hipotética apenas para completar inventário.

## Documentação viva × evidência histórica

A S0 usa a seguinte regra de manutenção:

| Documento/superfície | Classificação na S0 | Tratamento |
|---|---|---|
| `README.md` da raiz | documentação viva | atualizar apenas o estado corrente e manter métricas somente quando medidas |
| `docs/sprints/README.md` | índice misto: navegação viva + cronologia histórica | corrigir somente o bloco de estado corrente do Sistema de Temas |
| `docs/sprints/sistema_temas/README.md` | índice misto: cabeçalho vivo + registros históricos | corrigir o bloco “Estado vigente”; preservar seções históricas |
| este `V13/README.md` | documentação viva da V13 | manter estado, limites e próxima ação da V13 |
| `V13/PLANO_MESTRE.md` | contrato de planejamento aceito | não reescrever silenciosamente após a PR #58 |
| documentos V12 de fechamento, testes, checkpoint, protocolo e escopo | evidência/contrato V12 | preservar o estado da época, inclusive “candidata pré-aceite” |
| READMEs/checkpoints V01–V11 | contratos e evidências de suas sprints | usar como owners; não modernizar frases históricas só para parecerem atuais |

Uma frase antiga como “V13 ainda não começou” dentro de um checkpoint V12 continua correta como evidência daquele momento. O estado corrente deve ser obtido das superfícies vivas acima.

## Concorrência documental observada

Na abertura da S0 existiam PRs paralelas que tocam documentação compartilhada. Em especial, há frentes abertas alterando `README.md`, `docs/sprints/README.md`, `docs/sprints/sistema_temas/README.md` e/ou `CHANGELOG.md`.

Por isso a S0:

- trabalha sobre a `main` real e em branch exclusiva;
- não altera `CHANGELOG.md`;
- limita mudanças nos índices aos blocos necessários da V13;
- reconfirma a `main`, o merge-base, o diff e as PRs paralelas antes do checkpoint final;
- se a `main` avançar, reconcilia de forma aditiva e repete os gates aplicáveis.

## CI e autorização

A manutenção do workflow V12 integrada pela PR #58 é preservada. Em PR não-V12, regressões e validador V12 continuam executando quando os caminhos compartilhados acionam o workflow, enquanto o gate estrito de escopo V12 deve ficar `NOT_APPLICABLE`. Isso não é `PASS` e não exige ampliar o allowlist histórico V12.

A S0 não autoriza nem executa deploy de App, workspace theme, ACL/grupos, `Import theme`, `Publish`, alteração de dashboard, persistência no workspace ou qualquer outra mutação Databricks.

## Próxima ação

A próxima decisão é o aceite explícito do [checkpoint S0](CHECKPOINT_S0.md). Somente depois desse aceite a S0 poderá ser integrada e/ou a S1 poderá ser iniciada, conforme a decisão do mantenedor.

**Não iniciar S1 automaticamente.**
