# V13 — S7: protocolo de homologação humana do handoff

Status inicial: **`HUMAN-01 = BLOCKED` — `HUMAN_EVIDENCE_MISSING`**.

Este documento define o ensaio humano mínimo exigido pelo Plano Mestre V13. Ele é um protocolo, não uma evidência preenchida e não autoriza operação Databricks.

Git/CI não podem alterar o status inicial para PASS. O status só pode mudar depois de uma execução real por participante autorizado que não tenha construído o procedimento.

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

Preencher **somente depois** de uma sessão real.

| Campo | Valor |
|---|---|
| `case_id` | `HUMAN-01` |
| `participant_id` | `<sanitizado>` |
| participante não construiu o procedimento | `<true/false>` |
| autorizado para o ensaio | `<true/false>` |
| início observado | `<não versionar timestamp se ele identificar contexto sensível; registrar apenas quando necessário>` |
| duração observada | `<minutos>` |
| ajuda verbal do autor | `<0 ou quantidade>` |
| ajuda documental extra | `<0 ou quantidade + referência pública/interna não sensível>` |
| erros de interpretação | `<quantidade + categoria sanitizada>` |
| H1 navegação | `<PASS/FAIL>` |
| H2 notebook | `<PASS/FAIL>` |
| H3 workspace BLOCKED | `<PASS/FAIL>` |
| H4 diagnóstico | `<PASS/FAIL>` |
| H5 rollback | `<PASS/FAIL>` |
| H6 segurança/privacidade | `<PASS/FAIL>` |
| resultado humano | `<PASS/FAIL/BLOCKED>` |
| observação formativa | `<texto sanitizado, sem inferência estatística>` |

Não substituir `<...>` por dados inventados para satisfazer teste.

## 7. Regra de decisão

Estados permitidos para `HUMAN-01`:

- `BLOCKED`: sessão não executada, participante inválido ou evidência mínima ausente;
- `FAIL`: sessão executada e pelo menos um oráculo H1–H6 falhou;
- `PASS`: sessão real executada, todos os H1–H6 passaram e os requisitos do participante foram satisfeitos.

`NOT_APPLICABLE` não é permitido para o caso HUMAN-01 porque a homologação humana é critério explícito da S7.

Nenhum número agregado, score ou percentual substitui essa decisão.

## 8. Ajuda e erros de interpretação

Registrar de forma categórica e sanitizada, por exemplo:

- `NAVIGATION_OWNER` — escolheu owner incorreto;
- `STATUS_SCOPE` — interpretou PASS além do alcance;
- `BLOCKED_BYPASS` — tentou contornar BLOCKED;
- `DIAGNOSTIC_ROUTE` — não localizou S4;
- `ROLLBACK_ROUTE` — não localizou S3/LKG;
- `PRIVACY_BOUNDARY` — tentou registrar dado sensível.

Ajuda do facilitador depois do erro pode ser registrada, mas o oráculo correspondente continua FAIL para aquela sessão. Não “corrigir” a evidência após ensinar a resposta.

## 9. Duração

A duração deve ser observada na sessão quando aplicável, conforme o Plano Mestre. Ela é descritiva e formativa.

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

Nenhuma sessão humana S7 foi executada por este documento.

Portanto o único estado honesto neste momento é:

`HUMAN-01 = BLOCKED`

Motivo:

`HUMAN_EVIDENCE_MISSING`.

A candidata técnica pode passar CI mantendo esse BLOCKED. **A V13 não pode ser declarada aceita/encerrada enquanto o gate humano permanecer BLOCKED.**
