# V14 S1 — Modelo operacional de ownership, autoridade e escalonamento

Data: 16/09/2026.

Baseline: `main@e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493`, merge da PR #71 que integrou e certificou a S0.

## 1. Objetivo

A S1 transforma os owners técnicos já versionados em um **mapa explícito de responsabilidade operacional e autoridade**, sem promover referências técnicas a poderes corporativos que o repositório não comprova.

A regra fail-closed é deliberada:

> se owner operacional, backup, aprovador de mudança, responsável por incidente, autoridade de go-live ou autoridade de risco residual não estiverem evidenciados, o estado é `BLOCKED`.

`BLOCKED` nesta S1 não é um defeito a esconder. É a representação correta de uma lacuna de autoridade que precisa ser resolvida fora de inferência automática.

## 2. Fontes canônicas reutilizadas

A S1 não cria uma segunda política de papéis nem um novo inventário técnico.

- [V01 — governança](../V01/GOVERNANCA.md): papéis `Leitor`, `Proponente`, `Aprovador`, `Publicador` e `Mantenedor`, incluindo a proibição de self-approval e a separação entre aprovação e publicação;
- [V13 — matriz operacional](../V13/MATRIZ_OPERACIONAL.json): superfícies, owners técnicos e relacionamentos operacionais;
- [V13 — inventário operacional](../V13/S1_INVENTARIO_OPERACIONAL.md): interpretação referencial dos owners e fronteiras;
- [Plano Mestre V14](PLANO_MESTRE.md): contrato da S1 e gate de ownership/autoridade.

A [matriz S1](MATRIZ_OWNERSHIP.json) apenas referencia essas fontes.

## 3. O que significa cada responsabilidade

| Slot | Pergunta operacional | Pode ser inferido do owner técnico? |
|---|---|---|
| owner técnico | qual versão/contrato é responsável pela superfície? | sim, quando já versionado |
| owner operacional | quem responde pela operação sustentada? | **não** |
| backup operacional | quem substitui o owner operacional? | **não** |
| aprovador de mudança | quem pode aprovar uma mudança aplicável ao ambiente? | **não** |
| responsável por incidente | quem coordena resposta a falha operacional? | **não** |
| autoridade de go-live | quem pode autorizar entrada em produção? | **não** |
| autoridade de risco residual | quem pode aceitar risco residual? | **não** |

O papel abstrato da V01 também não é identidade. Dizer que existe o papel `Aprovador` não prova quem ocupa esse papel no ambiente real.

## 4. Ownership técnico evidenciado

| Superfície | Owner técnico canônico | Evidência principal |
|---|---|---|
| `notebook_visual_core` | V02 | V13 `MATRIZ_OPERACIONAL.json` + V02 |
| `visual_lab` | V05 | V13 `MATRIZ_OPERACIONAL.json` + V05 |
| `transition_bundle` | V09 | V13 `MATRIZ_OPERACIONAL.json` + V09 |
| `databricks_app` | V10 | V13 `MATRIZ_OPERACIONAL.json` + V10 |
| `aibi_dashboard` | V11 | V13 `MATRIZ_OPERACIONAL.json` + V11 |
| `workspace_theme` | V11 | V13 `MATRIZ_OPERACIONAL.json` + V11 |

Esses owners dizem onde está o contrato técnico. Eles **não** constituem owner operacional, grupo Databricks, aprovador de mudança, plantão, suporte, autoridade de go-live ou aceite de risco.

## 5. Estado operacional atual

Na abertura da S1, o repositório não contém evidência suficiente para preencher os seis slots corporativos de nenhuma das seis superfícies. Portanto todos permanecem `BLOCKED` na matriz.

Não foram inventados:

- nomes de pessoas;
- grupos corporativos;
- e-mails;
- canais de Teams/Slack;
- filas de suporte;
- horários de plantão;
- SLA/SLO;
- comitês ou autoridades de go-live;
- autoridade para aceitar risco residual.

Quando uma dessas informações vier a existir, a matriz só poderá promover um slot para `EVIDENCED` com `principal_ref` e `evidence_refs` concretos e revisáveis.

## 6. Fluxo de responsabilidade e escalonamento

Para qualquer ocorrência, mudança ou pedido de ativação:

1. **Identifique a superfície.** Use as seis chaves canônicas da matriz S1 e da V13.
2. **Faça triagem técnica pelo owner canônico.** O owner técnico aponta para o contrato, testes, preflight ou runbook já existente.
3. **Classifique se a ação é apenas local/read-only ou se exige autoridade operacional.** Mudança remota, publicação, deploy, ACL, `Import theme`, workspace theme e go-live exigem autoridade própria.
4. **Verifique o slot de autoridade aplicável.** Se `principal_ref` e evidência não existirem, o estado permanece `BLOCKED`.
5. **Não faça self-approval.** A mesma identidade não pode propor/operar e ser usada como aprovação independente quando o fluxo requer aprovação separada.
6. **Não derive publicação de aprovação.** A V01 separa aprovação de conteúdo e poder técnico para publicar; a S1 preserva essa separação.
7. **Não derive go-live de owner técnico.** Ser owner do contrato V02/V05/V09/V10/V11 não autoriza entrada em produção.
8. **Escalone a lacuna, não a contorne.** Sem owner/backup/autoridade evidenciados, registre `BLOCKED` e leve a decisão a quem possua autoridade organizacional fora deste repositório.

A S1 não inventa um canal para esse escalonamento. O canal corporativo deve ser evidenciado antes de ser documentado como operacional.

## 7. Cenários negativos obrigatórios

### Owner operacional ausente

Resultado: `BLOCKED`. Não usar o owner técnico como substituto automático.

### Backup ausente

Resultado: `BLOCKED`. Não afirmar resiliência organizacional ou cobertura sustentada.

### Self-approval

Resultado: inválido. A política V01 impede autoaprovação quando revisão independente é exigida.

### Autoridade inventada

Resultado: inválido. Um texto como “comitê de go-live”, um grupo ou e-mail não versionado/evidenciado não pode transformar o slot em `EVIDENCED`.

### Aprovação confundida com publicação

Resultado: inválido. Um aprovador não recebe automaticamente poder técnico de publicação.

### Owner técnico confundido com aceite de risco

Resultado: inválido. O owner do componente não se torna autoridade de risco residual por inferência.

## 8. Instrução para usuário não técnico

Se você precisa saber “quem pode autorizar isso?” e a matriz mostra `BLOCKED`, **não escolha uma pessoa por aproximação**. O significado é: o repositório ainda não possui evidência suficiente para responder com segurança.

O procedimento correto é:

1. identificar a superfície e o tipo de decisão;
2. consultar a matriz S1;
3. se o slot estiver `BLOCKED`, interromper qualquer ação que dependa daquela autoridade;
4. obter uma referência corporativa verificável para owner/backup/autoridade;
5. só então propor atualização versionada da matriz e executar novamente os gates.

## 9. Fronteiras preservadas

A S1 não executa nem autoriza:

- deploy de Databricks App;
- alteração de ACL, grupo ou compute;
- workspace theme;
- `Import theme` remoto;
- `Publish`;
- edição real de dashboard;
- persistência remota;
- production readiness;
- decisão `GO`, `NO_GO` ou go-live;
- aceite de risco residual;
- início da S2.

`A11-01 = FAIL` continua na issue #57. `V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` continuam `BLOQUEADO_AUTORIZACAO`. `HUMAN-01 = PASS` continua somente como evidência formativa.

## 10. Próximo gate

A S1 só pode ser candidata a aceite depois que:

- matriz e runbook passarem nos negativos de owner ausente, self-approval e autoridade inventada;
- regressões V01–V14, V00 e validador permanecerem verdes;
- métricas do README forem medidas pelo runner, não estimadas;
- `main`, merge-base e concorrência forem reconfirmados;
- zero mutação Databricks for preservada;
- S2 continuar não iniciada;
- houver aceite explícito do mantenedor.

O aceite da S1 não inicia S2 automaticamente.
