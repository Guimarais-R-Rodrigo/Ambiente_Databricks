# Checkpoint V13 — S1: inventário e contrato operacional

Data: 15/09/2026.

Branch: `codex/temas-v13-s1-inventario-operacional-20260915`.

Estado deste documento: **candidata S1 em certificação final**. O HEAD imediatamente anterior à criação deste checkpoint, `280b5a75c8799cb7e8b07b906695fd62c6e08623`, concluiu 8/8 workflows de PR com `success`. Como este checkpoint altera a árvore, a certificação do novo HEAD deve ser refeita antes do aceite.

## 1. Baseline de abertura

- S0 aceita e integrada pela PR #59;
- merge S0 na `main`: `1d46c9625fb5bfd6d1b666ddff055507238788bf`;
- pós-merge S0: 14/14 workflows de `push` com `success`, 0 failures;
- branch S1 criada diretamente desse merge certificado;
- issue aberta herdada do Sistema de Temas: #57, `A11-01 = FAIL`;
- nenhuma mutação Databricks foi autorizada ou executada pela S1.

A S1 não reutilizou a branch S0 como base paralela: nasceu da `main` já integrada e certificada.

## 2. Escopo efetivamente implementado

A S1 implementa somente o inventário e o contrato operacional previstos no Plano Mestre V13.

Artefatos próprios:

- `docs/sprints/sistema_temas/V13/MATRIZ_OPERACIONAL.json`;
- `docs/sprints/sistema_temas/V13/S1_INVENTARIO_OPERACIONAL.md`;
- `tools/temas_v13_operacional.py`;
- `tools/tests/test_temas_v13_s1.py`;
- `.github/workflows/temas-v13-ci.yml`;
- atualização do estado vivo em `docs/sprints/sistema_temas/V13/README.md`;
- atualização do estado vivo e das métricas realmente medidas em `README.md`.

Este checkpoint é o oitavo caminho documental/técnico próprio da candidata S1.

Não houve alteração em `ambiente_fonte/`, `Novo_Ambiente_Simulado/`, contratos funcionais V01–V12, `CHANGELOG.md`, App, binder AI/BI, schema ou tokens.

## 3. Decisão de arquitetura

A S1 adotou `MATRIZ_OPERACIONAL.json` como índice estruturado porque o Plano Mestre exige uma relação verificável entre superfície, owner, artefato, preflight futuro, autorização, smoke, rollback e evidência.

A matriz é **referencial**, não uma segunda fonte de verdade. Ela não copia:

- tokens de tema;
- política de papéis/transições V01;
- schema/parsing/validação V02;
- três bindings diretos V11;
- matriz 48 = 3/23/22 V11;
- lista protegida do `theme_contract` V09;
- manifesto de implantação;
- schema AI/BI ou novo contexto `aibi`.

O validador S1 falha fechado se forem introduzidas chaves que representem cópia desses contratos.

## 4. Seis superfícies inventariadas

| `surface_id` | Superfície | Owner primário | Estado operacional relevante |
|---|---|---|---|
| `notebook_visual_core` | núcleo notebook / Plotly / HTML | V02 | Git/CI; UAT-01 somente textual |
| `visual_lab` | Visual Lab | V05 | `V12-LAB-01 = BLOQUEADO_AUTORIZACAO` |
| `transition_bundle` | kit/bundle V09 | V09 | transporte/integridade; não instalação |
| `databricks_app` | Databricks App | V10 | `V12-APP-01 = BLOQUEADO_AUTORIZACAO` |
| `aibi_dashboard` | dashboard AI/BI | V11 | `V12-AIBI-01 = PASS` limitado + `A11-01 = FAIL` |
| `workspace_theme` | tema de workspace | V11 | `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO` |

A existência de uma superfície na matriz não equivale a homologação dessa superfície.

## 5. Dependências V05/V09/V10/V11 explicitadas

A matriz registra as relações sem fundir owners:

1. V05 reutiliza o núcleo V02/V03/V04;
2. V10 reutiliza autoria/sessão V05;
3. V09 continua dono do transporte e não implica ativação;
4. bundle V09 e bundle do App V10 continuam artefatos distintos;
5. V11 projeta a partir de `ResolvedTheme` V02;
6. dashboard theme e workspace theme continuam superfícies separadas.

## 6. Regra fail-closed de ações

Cada ação é classificada como `read_only`, `local_artifact_mutation`, `persistent_mutation` ou `remote_mutation`.

Toda ação não `read_only` precisa declarar:

- autorização explícita;
- referências de verificação;
- rollback obrigatório e estratégia;
- evidência mínima pela superfície.

Todas as ações da matriz têm `performed_by_s1=false`.

O campo de preflight permanece `S2_NOT_IMPLEMENTED`; a S1 não implementa a ferramenta de preflight unificado.

## 7. Testes negativos permanentes

`tools/tests/test_temas_v13_s1.py` contém 20 testes e inclui mutantes que devem falhar quando:

- owner é removido;
- owner aponta para artefato inexistente;
- ação mutável perde autorização;
- ação mutável perde rollback;
- autorização de mutação passa a opcional;
- rollback de mutação passa a opcional;
- a matriz tenta antecipar S2;
- a S1 passa a alegar execução da ação;
- surge um segundo contrato de tokens.

A suíte também verifica preservação do `A11-01 = FAIL`, dos três `BLOQUEADO_AUTORIZACAO`, da separação dashboard/workspace e da ausência de cliente de rede/Databricks no validador.

## 8. First head e failure intermediário preservado

Primeiro HEAD S1: `ae5bcceb74c566586434e1a215ec5005859b2707`.

Workflows de PR desse SHA:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35036985375` | `success` |
| Contrato de temas V01 | `35036985291` | `success` |
| Núcleo de temas V02 | `35036985369` | `success` |
| CI local reproduzível | `35036985385` | `failure` |
| Contrato operacional V13 | `35036985303` | `failure` |

A causa comum dos failures foi exclusivamente o validador estrutural/documental, após os testes funcionais já terem passado.

No workflow V13, antes do failure de documentação, foram observados:

- testes S1: **20/20 PASS**;
- validador operacional S1: **PASS**;
- regressões `test_temas*.py`: **535/535 PASS**;
- compatibilidade visual V00: **12/12 PASS**.

O validador mediu **1431 arquivos** e **1922 links**, enquanto o README ainda declarava 1427/1918, e encontrou um backlink em `S1_INVENTARIO_OPERACIONAL.md` com um `../` a menos.

O step final `Fronteira S1` ficou `skipped` nesse run por causa do failure anterior. Ele não é reclassificado como PASS.

## 9. Correção aditiva do first head

Commit: `280b5a75c8799cb7e8b07b906695fd62c6e08623`.

A correção alterou apenas:

- o backlink confirmado para `tools/temas_v13_operacional.py`;
- `README.md`, atualizando o estado vivo S0 integrada/S1 candidata e as métricas 1431/1922 efetivamente medidas.

Nenhum gate foi relaxado. Nenhum allowlist V12 foi ampliado. Nenhum failure do first head foi apagado.

## 10. Certificação do segundo head

O SHA `280b5a75c8799cb7e8b07b906695fd62c6e08623` acionou 8 workflows reais de PR e todos concluíram com `success`:

| Workflow | Run | Resultado |
|---|---:|---|
| Contrato de temas V01 | `35037337224` | `success` |
| Regressões da instrumentação V00 | `35037337251` | `success` |
| Núcleo de temas V02 | `35037337490` | `success` |
| CI local reproduzível | `35037337227` | `success` |
| Contrato operacional V13 | `35037337201` | `success` |
| Temas nativos AI/BI V11 | `35037337216` | `success` |
| Databricks App de gestão visual V10 | `35037337198` | `success` |
| Homologação de jornadas V12 | `35037337384` | `success` |

No workflow V13 `35037337201` foram observados no mesmo SHA:

- testes S1: **20/20 PASS**;
- validador operacional: **PASS**;
- regressões V01–V13: **535/535 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador estrutural/documental: **APROVADO — 0 falhas / 0 avisos**;
- `repo (identidade) = 1431`;
- `repo (links) = 1922`;
- `V13_S1_REMOTE_MUTATION=0`;
- `V13_S2_PREFLIGHT=NOT_IMPLEMENTED`.

No workflow V12 `35037337384` foram novamente preservados os gates V12 e a manutenção da PR #58:

- protocolo/mutantes V12: **47/47 PASS**;
- evidência real V12: **11/11 PASS**;
- regressões transversais, agora incluindo S1: **535/535 PASS**;
- V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**;
- `V12_SCOPE=NOT_APPLICABLE`;
- `Escopo V12 e higiene`: **skipped**, não PASS.

## 11. Estados herdados preservados

A S1 mantém separadamente:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` de ambiente;
- `UAT-01 = PASS` textual;
- `V12-AIBI-01 = PASS` somente no escopo real draft/sintético/import+rollback;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

Não existe `PASS` agregado que esconda o `A11-01 = FAIL` ou os bloqueios de autorização.

## 12. Limites e ausência de mutação Databricks

A S1 não executou:

- deploy de App;
- criação/alteração de ACL ou grupos;
- workspace theme;
- `Import theme` real adicional;
- `Publish`;
- edição de dashboard;
- persistência em workspace;
- criação/alteração de UC Volume;
- qualquer outra mutação Databricks.

O validador S1 não importa cliente Databricks, `requests`, `socket`, `urllib`, `httpx` ou `subprocess`.

Git/CI permanecem evidência técnica, não homologação de ambiente.

## 13. Métricas verificáveis

No SHA `280b5a75...`, antes da criação deste checkpoint, o validador mediu:

- `repo (identidade) = 1431` arquivos;
- `repo (links) = 1922` links fora da raiz analisada;
- 0 arquivos locais extras;
- 0 falhas e 0 avisos após a correção.

A criação deste checkpoint adiciona um arquivo à árvore e, portanto, exige nova medição antes do HEAD final. Nenhum número novo será estimado neste documento.

## 14. Estado Git/PR antes do checkpoint final

Antes da criação deste arquivo:

- base da PR #60: `main` `1d46c9625fb5bfd6d1b666ddff055507238788bf`;
- HEAD: `280b5a75c8799cb7e8b07b906695fd62c6e08623`;
- PR #60: aberta e draft;
- S2 não iniciada.

A reconciliação final de `main`, merge-base, `ahead_by`/`behind_by`, mergeabilidade, diff, PRs paralelas e workflows será preenchida no fechamento após a certificação do novo HEAD.

## 15. O que fica para S2

Somente após aceite explícito da S1:

- ferramenta de preflight unificado;
- resolução de ambiente/versões/permissões/identidade/classificação de dados conforme o Plano Mestre;
- consumo da matriz S1 como entrada, sem reabrir os owners V01–V12;
- estados fail-closed para requisitos não demonstráveis.

A S1 **não** antecipa esses itens.

## 16. Ponto de parada

Após medir a árvore com este checkpoint, reconciliar o README apenas com números observados, certificar o SHA final e reconfirmar a `main`, a PR #60 deve permanecer sem merge até aceite explícito do mantenedor.

**Parar antes da S2.**
