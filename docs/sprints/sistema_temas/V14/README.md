# V14 — Production Readiness e Operação Sustentada do Sistema de Temas

Status: **S0 — reconciliação pós-V13 e freeze de readiness em execução; candidata ainda não aceita nem integrada.**

Data de abertura da S0: 16/09/2026.

Baseline Git da S0: `main@350dcf0b37e730042ef961f12f11b30b2660d2c6`, merge da PR #70 que integrou o [Plano Mestre V14](PLANO_MESTRE.md).

## Comece aqui

A V14 não adiciona um novo mecanismo visual. Ela é a etapa de **production readiness, operação sustentada e decisão final de go-live** do Sistema de Temas. A S0 apenas reconcilia o estado real do repositório, congela fronteiras e instala a guarda inicial de CI.

Para uma pessoa não técnica, a regra mais importante é simples: **nada nesta S0 publica, instala, altera ou ativa tema no Databricks**. Também não existe decisão de `GO`, SLA/SLO aprovado ou produção autorizada neste momento.

Use estes documentos nesta ordem:

1. [Plano Mestre V14](PLANO_MESTRE.md) — contrato de escopo aceito e integrado;
2. [Checkpoint S0](CHECKPOINT_S0.md) — evidência da reconciliação corrente;
3. [Auditoria pós-merge V13](../V13/AUDITORIA_POS_MERGE.md) — fechamento herdado;
4. [README V12](../V12/README.md) — classes de evidência e bloqueios herdados.

## O que a S0 faz

A S0 está limitada ao contrato do Plano Mestre:

- confirmar o fechamento real da V13;
- separar documentação viva de evidência histórica;
- congelar o escopo V14;
- inventariar dívidas, bloqueios e concorrência;
- criar a superfície viva V14;
- criar a guarda/CI V14 inicial em modo read-only;
- impedir afirmações de production readiness sem evidência.

A S0 **não** executa S1 nem antecipa artefatos de ownership, matriz de readiness, suporte sustentado, SLIs/SLO/SLA, custos, lifecycle, risco residual ou decisão de go-live.

## Baseline confirmado

O Plano Mestre V14 foi integrado pela PR #70 no merge de dois pais:

`350dcf0b37e730042ef961f12f11b30b2660d2c6`

Pais:

- `99161fdeb9253c30a82243644ba89af8cd50d79e` — `main` anterior;
- `0ee5fba40fba26da0a3dd8f152640d9a58a9acce` — HEAD certificado da PR #70.

No merge, **15/15 workflows de `push` concluíram em `success`**. O V13 executou S1–S7, regressões, V00, validador e todas as fronteiras com sucesso; o V12 executou protocolo, evidência real, regressões, V00, validador, aplicabilidade e higiene com sucesso; o CI geral executou o gate sem credenciais com sucesso.

Esse resultado certifica o baseline Git. Ele não constitui production readiness nem autorização remota.

## Estados herdados que a S0 preserva

| Item | Estado | Interpretação na S0 |
|---|---|---|
| `DOC-02` | `PASS` | somente no alcance documentado |
| `DOC-03` | `PASS` | somente no alcance documentado |
| `SEC-01` | `PASS` | somente no alcance observado |
| `UAT-01` | `PASS` | somente textual |
| `V12-AIBI-01` | `PASS` | somente no alcance V12 já evidenciado |
| `HUMAN-01` | `PASS` | evidência formativa; não é readiness estatística |
| `A11-01` | `FAIL` | issue #57 permanece aberta |
| `V12-LAB-01` | `BLOQUEADO_AUTORIZACAO` | não reclassificado |
| `V12-APP-01` | `BLOQUEADO_AUTORIZACAO` | não reclassificado |
| `V12-AIBI-02` | `BLOQUEADO_AUTORIZACAO` | não reclassificado |

`PASS`, `FAIL`, `BLOQUEADO_AUTORIZACAO` e `NOT_APPLICABLE` continuam estados distintos. A S0 não usa um PASS agregado para esconder um FAIL ou bloqueio.

## Contratos congelados

A V14 referencia os owners V01–V13; não cria uma segunda fonte de verdade.

Em especial, a fronteira V11 permanece congelada:

- `ResolvedTheme` continua fonte configurável de verdade;
- `context="aibi"` continua reservado;
- 48 tokens permanecem **3 `translated`, 23 `approximated`, 22 `unsupported`**;
- somente três bindings diretos permanecem autorizados;
- `cellFormat` não vira token;
- `approximated` e `unsupported` não são automatizados;
- dashboard theme e workspace theme continuam superfícies distintas;
- `Import theme` continua distinto de `Publish`.

A S0 também não copia schema, tokens, política de estados, engine de preflight/release ou contratos de evidência. Ela aponta para os owners existentes.

## Superfícies congeladas para a V14

A V14 mantém as seis superfícies herdadas da V13:

1. `notebook_visual_core`;
2. `visual_lab`;
3. `transition_bundle`;
4. `databricks_app`;
5. `aibi_dashboard`;
6. `workspace_theme`.

As dez dimensões de readiness permanecem definidas apenas no Plano Mestre até a S2. A S0 não cria `MATRIZ_READINESS.json` nem atribui estados de readiness novos por inferência.

## Concorrência no repositório

Na abertura da S0 existem frentes paralelas reais. As principais são:

- PR #69 — Skill Enforcement / SE01, com sobreposição em `README.md`;
- PR #51 — Micromodelos / MM01, também com sobreposição em `README.md`;
- PRs históricas abertas #26, #6, #5 e #4.

A S0 não incorpora essas frentes silenciosamente. Se a `main` avançar, esta branch deverá ser reconciliada aditivamente antes de qualquer integração. Reset/force-push não é mecanismo de reconciliação.

## Guarda e CI V14

A S0 introduz uma guarda local e um workflow V14 read-only.

A guarda verifica, entre outros pontos:

- artefatos S0 obrigatórios;
- preservação dos estados herdados;
- manutenção da fronteira V11;
- inexistência de artefatos prematuros de S1/S2;
- coerência da documentação viva;
- escopo do diff da S0 em CI;
- workflow sem credenciais Databricks e sem persistência de credenciais de checkout.

O workflow também reaproveita as regressões canônicas V01–V13, V00 e `validate_assistant.py --conferir-readme`. Isso é intencional: V14 não cria uma segunda suíte funcional para substituir os owners anteriores.

## Limites operacionais

Nesta S0:

- `V14_S0_REMOTE_MUTATION=0`;
- `V14_S0_DATABRICKS_MUTATION=0`;
- nenhuma credencial Databricks é usada;
- nenhuma publicação, deploy, ACL, workspace theme, `Import theme`, `Publish` ou persistência remota é executada;
- nenhuma autoridade corporativa, pessoa, canal, SLA, SLO ou custo é inventado;
- issue #57 não é fechada;
- S1 permanece não iniciada.

## Próximo gate

A S0 só poderá ser considerada candidata aceita depois de:

1. certificar o HEAD exato da branch nos workflows reais;
2. registrar qualquer failure intermediário sem reclassificá-lo;
3. reconciliar eventual avanço concorrente da `main`;
4. reconfirmar #57, bloqueios, métricas e fronteiras;
5. obter **aceite explícito do mantenedor**.

O aceite da S0 não inicia S1 automaticamente.