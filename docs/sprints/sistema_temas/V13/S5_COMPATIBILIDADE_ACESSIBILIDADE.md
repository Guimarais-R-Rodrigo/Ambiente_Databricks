# V13 — S5: compatibilidade e acessibilidade operacional

Data de abertura: 16/09/2026.

Estado: **candidata S5**. Este documento é operacional e não reescreve evidência
histórica V12.

## 1. Objetivo

A S5 incorpora à operação verificações que a V12 mostrou não serem capturadas
apenas por CI de contrato. O foco é compatibilidade por superfície e
acessibilidade operacional, em especial o finding real `A11-01`.

Esta sprint não cria nova capacidade visual, não amplia a V11 e não executa
mutação Databricks.

## 2. Decisão da issue #57

Decisão S5:

`PREFLIGHT_FAIL_CLOSED`

A V13 adota o primeiro caminho previsto no Plano Mestre: **preflight fail-closed
de contraste para formatação explícita de dashboard**, quando houver pares de
foreground/background provenientes de export real revisado e identificável.

A issue #57 permanece aberta.

Motivo: esta sprint define e testa uma decisão operacional verificável, mas não
corrige os pares que falharam na V12 e não produz nova observação de ambiente.
`A11-01 = FAIL` continua historicamente verdadeiro e reproduzível até existir
correção e nova evidência aplicável.

A decisão NÃO significa:

- alterar `cellFormat`;
- transformar formatação condicional em token;
- adicionar binding V11;
- inventar schema global de dashboard;
- concluir que High Contrast foi exercitado;
- fechar a issue com base em percepção subjetiva;
- publicar dashboard;
- alterar workspace theme.

## 3. Contratos congelados

Continuam válidos, sem modificação:

- `ResolvedTheme` é a fonte configurável de verdade;
- `context="aibi"` permanece reservado;
- a matriz V11 continua **3 `translated`, 23 `approximated`, 22 `unsupported`**;
- os únicos bindings diretos continuam:
  - `surface.card -> widget.background`;
  - `palette.categorical -> visualization.categorical_palette`;
  - `card.radius_px -> widget.corner_radius`;
- `dashboard_sintetico.json` não é arquivo nativo importável;
- `approximated` e `unsupported` não são automatizados;
- dashboard theme e workspace theme são superfícies separadas;
- `Import theme` e `Publish` são gates independentes;
- `cellFormat` não vira token do Hub.

## 4. Owner e fronteira do preflight

Ferramenta S5:

`tools/temas_v13_compatibilidade.py`

O preflight atual é deliberadamente estreito:

- superfície suportada: `aibi_dashboard`;
- evidência declarada: `REVIEWED_REAL_EXPORT`;
- export identificado por SHA-256;
- fixture sintético precisa estar explicitamente ausente;
- pares de cor precisam ser fornecidos de forma explícita;
- somente pares `observed=true` são medidos;
- estados não exercitados não são inferidos.

O preflight não lê um dashboard por conta própria. Isso evita assumir um schema
nativo global que a documentação oficial/contrato V11 não garante. O chamador é
responsável por extrair, a partir do export real revisado, somente os pares que
foram efetivamente identificados no caminho auditado.

A ferramenta não autentica o SHA ou a proveniência externa. A saída declara:

`evidence_authenticated = false`

Portanto um `PASS` S5 significa apenas:

> os pares explicitamente observados e fornecidos ao preflight atendem ao limiar
> local calculado.

Não significa homologação de ambiente, browser ou dashboard inteiro.

## 5. Cálculo de contraste

O cálculo usa luminância relativa sRGB/WCAG e compara o ratio bruto, sem
arredondamento para aprovação.

Classes aceitas:

- `NORMAL` → limiar 4,5:1;
- `LARGE` → limiar 3,0:1 somente quando a classificação foi declarada.

Modos aceitos:

- `LIGHT`;
- `DARK`;
- `HIGH_CONTRAST`.

Um modo ou par com `observed=false` recebe `NOT_APPLICABLE` /
`STATE_NOT_EXERCISED`; nenhum ratio é calculado.

Essa distinção é central: ausência de observação não vira PASS.

## 6. Reprodução do A11 histórico

A evidência V12 registrou os pares abaixo. A suíte S5 os usa como fixture de
regressão e também confirma que os valores estão ancorados em
`docs/sprints/sistema_temas/V12/TESTES.md`.

| Par observado | Ratio bruto | Limiar | Estado histórico |
|---|---:|---:|---|
| `#9C2638` sobre `#E8F4FD` — Light | 6.837793163467097 | 4.5 | PASS |
| `#9C2638` sobre `#11171C` — Dark | 2.3624715346329377 | 4.5 | **FAIL** |
| `#FFD465` sobre `#E8F4FD` — Light | 1.264684095079348 | 4.5 | **FAIL** |
| `#FFD465` sobre `#11171C` — Dark | 12.773222792356847 | 4.5 | PASS |

Resultado agregado: **FAIL**.

A suíte S5 deve continuar reproduzindo esse FAIL enquanto os pares forem os
mesmos. Não existe arredondamento que converta 2,36 ou 1,26 em aprovação.

## 7. Matriz de compatibilidade por superfície

Esta matriz é uma visão operacional S5. Ela **referencia** a matriz S1 e os owners;
não substitui `MATRIZ_OPERACIONAL.json`, schemas, bindings ou políticas.

| `surface_id` | Owner primário | Light | Dark | High Contrast | Evidência/limite operacional |
|---|---|---|---|---|---|
| `notebook_visual_core` | `docs/sprints/sistema_temas/V02/README.md` | CONTRACT_ONLY | CONTRACT_ONLY | MIXED_BY_CONSUMER | V03/V04/V07 continuam owners; CI não prova browser/runtime |
| `visual_lab` | `docs/sprints/sistema_temas/V05/README.md` | LOCAL_CONTRACT_ONLY | LOCAL_CONTRACT_ONLY | LOCAL_LIMITED | `V12-LAB-01` continua `BLOQUEADO_AUTORIZACAO` |
| `transition_bundle` | `docs/sprints/sistema_temas/V09/README.md` | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | transporte não é render |
| `databricks_app` | `docs/sprints/sistema_temas/V10/README.md` | NOT_EXERCISED | NOT_EXERCISED | NOT_EXERCISED | `V12-APP-01` continua `BLOQUEADO_AUTORIZACAO` |
| `aibi_dashboard` | `docs/sprints/sistema_temas/V11/README.md` | REAL_OBSERVED_A11 | REAL_OBSERVED_A11 | NOT_EXERCISED | A11 real permanece FAIL; preflight S5 cobre somente pares explicitamente fornecidos |
| `workspace_theme` | `docs/sprints/sistema_temas/V11/README.md` | NOT_EXERCISED | NOT_EXERCISED | NOT_EXERCISED | `V12-AIBI-02` continua `BLOQUEADO_AUTORIZACAO` |

Leitura dos marcadores:

- `CONTRACT_ONLY`: há contrato/teste local do owner, sem inferência de ambiente;
- `MIXED_BY_CONSUMER`: a superfície agregada contém consumidores com suporte
  distinto; não se cria um PASS único;
- `LOCAL_CONTRACT_ONLY`/`LOCAL_LIMITED`: cobertura local não prova frontend real;
- `REAL_OBSERVED_A11`: modo efetivamente observado no caso histórico A11;
- `NOT_EXERCISED`: não existe evidência suficiente para inferir estado;
- `NOT_APPLICABLE`: a superfície não renderiza o modo em questão.

## 8. Política para formato/consumidor fora do contrato

Quando a formatação ou consumidor não puder ser ligado a um owner e a um caminho
revisado, a política é:

1. não inventar binding;
2. não converter em token;
3. não inferir contraste de estado não observado;
4. marcar a certificação como não demonstrada;
5. coletar evidência ou encaminhar decisão arquitetural separada.

Para AI/BI, o preflight S5 atual recusa superfícies diferentes de
`aibi_dashboard`. Workspace theme continua superfície administrativa separada.

## 9. Formato do request S5

Exemplo local, ilustrativo:

```json
{
  "schema_version": 1,
  "engine": "V13-S5",
  "surface_id": "aibi_dashboard",
  "evidence_basis": "REVIEWED_REAL_EXPORT",
  "export_sha256": "<sha256-completo>",
  "synthetic_fixture_used": false,
  "pairs": [
    {
      "pair_id": "conditional_red_dark_widget",
      "foreground": "#9C2638",
      "background": "#11171C",
      "mode": "DARK",
      "text_class": "NORMAL",
      "observed": true
    }
  ]
}
```

Nenhum path corporativo, conteúdo do export, identidade pessoal ou credencial
precisa ser transportado pelo request.

## 10. Saída e interpretação

A saída estruturada contém:

- `overall_status`;
- `decision_code`;
- cobertura `LIGHT`/`DARK`/`HIGH_CONTRAST`;
- resultado por `pair_id`;
- ratio bruto e limiar;
- `evidence_authenticated=false`;
- `network_access=false`;
- `remote_mutation_performed=false`;
- `v11_binding_contract_changed=false`.

Estados do preflight de contraste:

- `PASS`: todos os pares observados passaram;
- `FAIL`: ao menos um par observado falhou;
- `NOT_APPLICABLE`: nenhum par do request foi exercitado.

`BLOCKED` continua sendo estado canônico do ciclo V13, mas não é fabricado pelo
cálculo puro de contraste. Bloqueios de autorização/identidade/permissão
continuam pertencendo ao preflight S2/diagnóstico S4 e à evidência de ambiente.

## 11. Negativos obrigatórios S5

A suíte precisa recusar ou caracterizar:

- request com shape inesperado;
- superfície não suportada;
- evidence basis diferente de export real revisado;
- hash inválido;
- fixture sintético tratado como export real;
- lista vazia;
- par com campo extra;
- `pair_id` inseguro/duplicado;
- cor curta, alpha, nome ou hex inválido;
- modo desconhecido;
- classe de texto desconhecida;
- `observed` não booleano;
- ratio abaixo do limite sem arredondar para PASS;
- estado não observado tratado como se tivesse sido exercitado.

## 12. Operação para usuário não técnico

Antes de usar o preflight:

1. confirme que você possui um export real revisado e seu SHA-256;
2. confirme qual caminho/campo do export foi revisado;
3. registre somente os pares de foreground/background que de fato pertencem ao
   estado observado;
4. classifique texto como `LARGE` somente quando houver base para isso;
5. execute o preflight local;
6. se houver `FAIL`, pare a certificação desse estado;
7. se houver `NOT_EXERCISED`, não escreva PASS;
8. não altere dashboard/workspace para “corrigir” durante este procedimento.

Se a correção exigir mudança de formatação condicional, ela precisa de contrato,
autorização e evidência próprios. A S5 não concede isso.

## 13. Estados herdados

Permanecem:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance de draft/sintético/rollback observado;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

## 14. Fronteira operacional

S5 não usa:

- rede;
- SDK/REST/CLI Databricks;
- subprocess/shell;
- credenciais;
- escrita em workspace;
- alteração de dashboard;
- alteração de workspace theme;
- Publish.

A CI continua read-only.

Fronteiras vivas esperadas:

- `V13_S5_NETWORK=0`;
- `V13_S5_REMOTE_MUTATION=0`;
- `V13_S5_CONTRAST_PREFLIGHT_LOCAL=1`;
- `V13_S6_NOT_STARTED=1`.

## 15. O que a S5 não prova

Mesmo com CI verde, a S5 não prova:

- comportamento de browser não exercitado;
- High Contrast quando não observado;
- acessibilidade global do dashboard;
- acessibilidade do App real;
- permissões de workspace;
- propagação de workspace theme;
- correção do finding A11;
- readiness de produção.

Essas limitações precisam continuar explícitas.

## 16. Ponto de parada

A S5 termina somente depois de:

- suíte própria e mutantes verdes;
- A11 histórico reproduzível como FAIL;
- regressões V01–V13 verdes;
- V00 verde;
- validador estrutural/documental verde;
- failures intermediários preservados;
- métricas do README raiz reconciliadas somente por medição real;
- checkpoint S5;
- certificação do SHA final exato;
- reconfirmação de `main`, merge-base, ahead/behind, issue #57 e concorrência;
- aceite explícito do mantenedor.

**S6 não foi iniciada.**
