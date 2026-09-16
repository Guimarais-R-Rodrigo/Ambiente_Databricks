# V13 — S7: protocolo de homologação humana do handoff

Status histórico inicial: **`HUMAN-01 = BLOCKED` — `HUMAN_EVIDENCE_MISSING`**.

Estado atual após sessão real registrada pelo mantenedor: **`HUMAN-01 = PASS` — `HUMAN_EVIDENCE_RECORDED`**.

Este documento define o ensaio humano mínimo exigido pelo Plano Mestre V13 e preserva também a evidência sanitizada da sessão executada. Ele não autoriza operação Databricks.

Git/CI não podem fabricar nem alterar por conta própria um status humano para PASS. O PASS atual decorre de uma sessão real informada pelo mantenedor e pode apenas ser verificado por CI como evidência versionada.

## 1. Objetivo

Demonstrar, em uma amostra formativa e sem inferência estatística, que outra pessoa consegue operar o handoff V13 sem instrução verbal do autor.

O participante deve conseguir:

1. encontrar o guia correto;
2. escolher a superfície/owner correto;
3. executar um preflight local;
4. interpretar um PASS local sem ampliar seu alcance;
5. interpretar um BLOCKED como ordem de parada;
6. localizar o diagnóstico correto;
7. localizar o rollback aplicável;
8. registrar dúvida/ajuda/erro de interpretação sem PII ou segredo.

## 2. Quem pode participar

Requisitos cumulativos:

- pessoa autorizada pelo mantenedor para este ensaio formativo;
- não ter construído o procedimento S7;
- usar somente os artefatos sintéticos/sanitizados indicados;
- não receber instrução verbal do autor durante a tarefa;
- não executar Databricks remoto;
- não usar credenciais reais no registro.

O registro versionado usa apenas um identificador sanitizado, por exemplo `P-S7-01`. Não versionar nome, e-mail, matrícula, workspace, host, token, URL privada ou caminho corporativo.

## 3. Preparação pelo facilitador

Antes de começar:

- checkout candidato S7 disponível;
- dependências locais prontas;
- diretório `.artifacts/` limpo para os requests temporários;
- abrir somente [S7_HANDOFF_OPERACIONAL.md](S7_HANDOFF_OPERACIONAL.md) como ponto inicial;
- cronômetro disponível fora do repositório;
- não explicar oralmente onde ficam S1–S6;
- não antecipar os resultados PASS/BLOCKED além do que já está escrito no guia.

A tarefa não exige navegador Databricks e não reexecuta `V12-LAB-01`, `V12-APP-01` ou `V12-AIBI-02`.

## 4. Tarefa do participante

Entregue esta instrução, sem complemento verbal:

> Use o guia “S7 — handoff operacional e fechamento”. Execute a primeira operação de treinamento. Registre o resultado de cada preflight, explique o que pode e o que não pode ser concluído, diga o que faria diante do bloqueio e mostre onde está o procedimento de rollback. Não execute nenhuma operação remota.

## 5. Oráculos

### H1 — navegação

PASS somente se o participante localizar, a partir do guia S7:

- matriz S1;
- preflight S2;
- diagnóstico S4;
- rollback S3.

### H2 — cenário notebook

PASS somente se:

- o request for executado pelo `tools/temas_v13_preflight.py`;
- `overall_status = PASS`;
- `THEME_VALID` estiver presente;
- o participante declarar que isso é PASS **local** e não prova Databricks/browser/Publish.

### H3 — cenário workspace theme

PASS somente se:

- o preflight retornar exit code 2;
- `overall_status = BLOCKED`;
- `AUTHORIZATION_CANONICALLY_BLOCKED` estiver presente;
- o participante decidir parar, sem fabricar autorização/identidade/snapshot.

### H4 — diagnóstico

PASS somente se o participante associar o bloqueio a governança/autorização e localizar o runbook S4 como próximo caminho seguro.

### H5 — rollback

PASS somente se o participante localizar no S3:

- Last Known Good;
- rollback preparado antes de mutação;
- verificação pós-rollback;
- diferença entre dry-run/local e ambiente real.

### H6 — segurança/privacidade

PASS somente se:

- nenhuma credencial/PII for usada;
- nenhuma mutação remota for executada;
- nenhum dos três casos ambientais bloqueados for reclassificado;
- `A11-01 = FAIL`/issue #57 não forem fechados por inferência.

## 6. Registro mínimo da execução

Sessão real informada pelo mantenedor após a execução do protocolo. O identificador `Tester` é tratado aqui como identificador sanitizado da sessão, não como identidade pessoal.

| Campo | Valor |
|---|---|
| `case_id` | `HUMAN-01` |
| `participant_id` | `Tester` |
| participante não construiu o procedimento | `true` |
| autorizado para o ensaio | `true` |
| início observado | `não versionado` |
| duração observada | `5 minutos` |
| ajuda verbal do autor | `0` |
| ajuda documental extra | `0` |
| erros de interpretação | `0` |
| H1 navegação | `PASS` |
| H2 notebook | `PASS` |
| H3 workspace BLOCKED | `PASS` |
| H4 diagnóstico | `PASS` |
| H5 rollback | `PASS` |
| H6 segurança/privacidade | `PASS` |
| resultado humano | `PASS` |
| observação formativa | `Sessão concluída com sucesso em 5 minutos; nenhum problema, ajuda ou erro de interpretação foi relatado.` |

A evidência acima foi preenchida a partir do relato do mantenedor após uma sessão real. Não há alegação de observação independente pela CI ou pelo autor deste registro.

## 7. Regra de decisão

Estados permitidos para `HUMAN-01`:

- `BLOCKED`: sessão não executada, participante inválido ou evidência mínima ausente;
- `FAIL`: sessão executada e pelo menos um oráculo H1–H6 falhou;
- `PASS`: sessão real executada, todos os H1–H6 passaram e os requisitos do participante foram satisfeitos.

`NOT_APPLICABLE` não é permitido para o caso HUMAN-01 porque a homologação humana é critério explícito da S7.

Nenhum número agregado, score ou percentual substitui essa decisão.

Para a sessão registrada na seção 6, todos os requisitos mínimos e H1–H6 estão registrados como satisfeitos. Portanto:

`HUMAN-01 = PASS`.

## 8. Ajuda e erros de interpretação

Registrar de forma categórica e sanitizada, por exemplo:

- `NAVIGATION_OWNER` — escolheu owner incorreto;
- `STATUS_SCOPE` — interpretou PASS além do alcance;
- `BLOCKED_BYPASS` — tentou contornar BLOCKED;
- `DIAGNOSTIC_ROUTE` — não localizou S4;
- `ROLLBACK_ROUTE` — não localizou S3/LKG;
- `PRIVACY_BOUNDARY` — tentou registrar dado sensível.

Ajuda do facilitador depois do erro pode ser registrada, mas o oráculo correspondente continua FAIL para aquela sessão. Não “corrigir” a evidência após ensinar a resposta.

Na sessão `Tester`, ajuda verbal = 0, ajuda documental extra = 0 e erros de interpretação = 0.

## 9. Duração

A duração deve ser observada na sessão quando aplicável, conforme o Plano Mestre. Ela é descritiva e formativa.

A sessão registrada durou 5 minutos.

Não definir SLA, SLO, meta de produtividade, percentil ou capacidade operacional a partir de uma única sessão. Esses assuntos pertencem à V14 somente se houver base real.

## 10. Evidência e versionamento

A evidência versionada pode conter:

- identificador sanitizado do participante;
- duração em minutos;
- contagens de ajuda/erros;
- categorias de erro;
- estados H1–H6;
- resultado final;
- hashes/commit públicos do próprio repositório quando necessários.

Não versionar:

- nome/e-mail/matrícula;
- host/token/secret;
- URL corporativa privada;
- workspace ID;
- path sensível de Volume;
- screenshot com PII;
- conteúdo de dados reais.

## 11. Estado desta candidata

A sessão humana S7 foi registrada pelo mantenedor com participante sanitizado `Tester`, autorizado e não construtor, duração de 5 minutos, zero ajuda, zero erros e H1–H6 em PASS.

Estado atual:

`HUMAN-01 = PASS`

Motivo:

`HUMAN_EVIDENCE_RECORDED`.

Esse PASS é exclusivamente o gate humano formativo da S7. Ele não altera `A11-01 = FAIL`, não fecha a issue #57, não promove os três casos ambientais bloqueados e não prova production readiness. A V13 ainda depende do checkpoint final, recertificação do SHA exato e aceite explícito antes da integração da PR S7.
