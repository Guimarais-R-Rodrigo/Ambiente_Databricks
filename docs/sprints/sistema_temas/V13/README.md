# V13 — consolidação operacional do Sistema de Temas

## Estado vigente

A S0 foi **aceita e integrada** pela PR #59 no merge `1d46c9625fb5bfd6d1b666ddff055507238788bf`. O merge partiu da candidata aceita `ec02a0bae9aab21c03da7ee2d61a889542172f1e`; os 14 workflows de `push` desse merge concluíram com `success`.

A etapa vigente é **S1 — inventário e contrato operacional**, em branch candidata separada. A S1 cria uma matriz referencial e um validador read-only para tornar explícita a rota superfície → owner → artefato → preflight futuro → autorização → smoke → rollback, sem duplicar contratos de V01–V12.

Para quem nunca entrou no Hub: a S1 não instala nada e não altera o Databricks. Ela organiza “quem é responsável por quê, onde conferir e o que precisa existir antes de uma ação”. A leitura operacional começa em [S1 — inventário operacional](S1_INVENTARIO_OPERACIONAL.md).

**S2 não foi iniciada.** O preflight unificado continua pertencendo à próxima sprint e não é antecipado pela S1.

## Plano canônico

O [Plano Mestre V13](PLANO_MESTRE.md), aceito pela PR #58, continua sendo o contrato de escopo. O [checkpoint S0](CHECKPOINT_S0.md) preserva a reconciliação que permitiu iniciar esta etapa.

A V13 continua responsável por consolidação operacional: inventário, preflight, release/install/update/rollback, observabilidade técnica, diagnóstico, compatibilidade/acessibilidade operacional, ensaios autorizados e handoff.

A V14 continua responsável por production readiness e suporte sustentado: ownership definitivo/substitutos, incidentes/severidades, SLA/SLO somente com base real, custos observados, retenção/housekeeping final, escalonamento, revisão/depreciação e decisão final de go-live.

## S1 — artefatos próprios

A S1 introduz apenas artefatos de inventário/validação operacional:

- [`MATRIZ_OPERACIONAL.json`](MATRIZ_OPERACIONAL.json): índice estruturado e referencial das seis superfícies;
- [`S1_INVENTARIO_OPERACIONAL.md`](S1_INVENTARIO_OPERACIONAL.md): explicação operacional para público técnico e não técnico;
- `tools/temas_v13_operacional.py`: validador local/read-only do contrato S1;
- `tools/tests/test_temas_v13_s1.py`: testes positivos e mutantes negativos;
- `.github/workflows/temas-v13-ci.yml`: CI read-only da V13.

A matriz não é schema de tema, manifesto de implantação, política de papéis ou matriz de bindings. Ela referencia os owners existentes.

## Seis superfícies da matriz

| Superfície | Owner primário | Regra principal |
|---|---|---|
| núcleo notebook / Plotly / HTML | V02, com V03/V04/V07 | `ResolvedTheme` permanece central; sem mutação persistente |
| Visual Lab | V05 | UAT textual não substitui ambiente real; V12-LAB-01 segue bloqueado |
| bundle/kit de transição | V09 | transporte não é instalação/ativação/publicação |
| Databricks App | V10 | bundle local ≠ deploy real; V12-APP-01 segue bloqueado |
| dashboard AI/BI | V11 | import, acessibilidade e Publish são gates separados |
| workspace theme | V11 | superfície administrativa separada do dashboard |

## Owners canônicos preservados

A S1 continua referenciando, sem copiar:

| Camada | Owner canônico |
|---|---|
| papéis, estados e transições | [V01](../V01/README.md) |
| schema, parsing, validação e `ResolvedTheme` | [V02](../V02/README.md) |
| Plotly | [V03](../V03/README.md) |
| HTML, estilos e tabelas | [V04](../V04/README.md) |
| Visual Lab e sessões | [V05](../V05/README.md) |
| assets/geração | [V06](../V06/README.md) |
| consumidores adicionais | [V07](../V07/README.md) |
| integração transversal | [V08](../V08/README.md) |
| transporte/`theme_contract` | [V09](../V09/README.md) |
| Databricks App | [V10](../V10/README.md) |
| AI/BI | [V11](../V11/README.md) |
| evidência/homologação | [V12](../V12/README.md) |

## Contratos não reabertos

Continuam congelados:

- `ResolvedTheme` é a fonte configurável de verdade;
- `context="aibi"` permanece reservado;
- a matriz V11 continua com 48 tokens: 3 `translated`, 23 `approximated` e 22 `unsupported`;
- somente os três bindings diretos já autorizados continuam diretos;
- `dashboard_sintetico.json` continua não importável no Databricks;
- `approximated` e `unsupported` não são automatizados;
- dashboard theme e workspace theme são superfícies distintas;
- `Import theme` e `Publish` são gates independentes;
- V09 continua dono do `theme_contract` e de sua lista de caminhos;
- V01 continua dona da política de papéis;
- `ambiente_fonte/` continua fonte editável; `Novo_Ambiente_Simulado/` continua derivado.

## Estados herdados preservados

| Caso | Estado | Leitura correta na S1 |
|---|---|---|
| `DOC-02` | `PASS` | evidência documental V12 |
| `DOC-03` | `PASS` | evidência documental V12 |
| `SEC-01` | `PASS` de ambiente | não é autorização universal |
| `UAT-01` | `PASS` | somente rota textual |
| `V12-AIBI-01` | `PASS` | somente dashboard draft, dados sintéticos, import + rollback |
| `A11-01` | `FAIL` | issue #57 continua aberta |
| `V12-LAB-01` | `BLOQUEADO_AUTORIZACAO` | Visual Lab real não executado |
| `V12-APP-01` | `BLOQUEADO_AUTORIZACAO` | deploy real não executado |
| `V12-AIBI-02` | `BLOQUEADO_AUTORIZACAO` | workspace theme/admin não executado |

A matriz operacional preserva esses estados separadamente. Não existe um “PASS geral” da superfície AI/BI.

## Regra de autorização e rollback

Toda ação mutável inventariada deve declarar:

1. autorização explícita;
2. verificação pós-operação;
3. rollback;
4. evidência mínima.

Na S1, todas as ações possuem `performed_by_s1=false`. Quando o procedimento real ainda não está autorizado ou comprovado, o estado permanece bloqueado — a matriz não finge que o rollback ocorreu.

## CI e ausência de mutação

O workflow V13 é somente leitura. A S1 não executa rede/SDK Databricks, não usa credenciais remotas e não altera App, dashboard, workspace theme, ACL, Volume ou qualquer outro recurso.

Git/CI continuam evidência técnica, não homologação de ambiente.

## Próxima ação

A candidata S1 deve passar seus testes, as regressões transversais e o validador estrutural no SHA exato. Depois será produzido um checkpoint S1 e a `main` será reconfirmada.

**Parar antes da S2.** O preflight unificado só começa após aceite explícito da S1.
