# R02-I — preparação da integração READMEs + Concierge

Data: 12/09/2026. Autor e revisor: ChatGPT (autorrevisão; sem auditor independente).
Escopo autorizado: compor as iniciativas em uma candidata isolada, resolver
conflitos e verificar; não fazer merge, publicar, congelar 1.0 ou iniciar R03.

## Resultado e o que muda para o usuário

A árvore candidata mantém o Concierge opcional da main e a fundação/piloto de
READMEs R01/R02. Quem começa pelo problema pode continuar usando a descoberta;
quem já conhece o objeto conserva a rota direta para o README, exemplo e API.
Não foi acrescentada etapa obrigatória ao uso do Hub. A mudança ocorre na
manutenção documental e em sua validação, não no comportamento dos helpers.

Os quatro conflitos textuais e a colisão de identificadores estão resolvidos
na candidata. Os PRs nº 5 e nº 6 permanecem intactos nas branches originais;
sua condição de integração não foi modificada. Um PR novo, baseado na main,
contém a composição acumulada e não deve ser mesclado junto com os anteriores
sem coordenar a substituição. Não houve merge de nenhuma branch remota.

A contagem continua 6/74 READMEs operacionais, 3/3 exemplares e 68 pendências.
Nenhum README operacional novo foi escrito nesta micro-sprint. Os nove textos,
o template, o checklist e o controle da migração são idênticos à R02 revisada.
O contrato continua `0.1.0-candidata` e a decisão documental continua proposta.

## Bases e procedência

| Referência | Commit | Árvore |
|---|---|---|
| Main com Concierge | `8744157fe9c3e0603f689fb2bcad52445e96cb41` | `0062a9e82690b96a1cf0a650d4a3f362b78f6b38` |
| R01/R02 e revisão | `5996574a337e7c878e19db9d8312c871cb4cd98f` | `9daeb7c0de86a0c8655119b58d7e5e471b9c1f6c` |
| Ancestral comum | `f748c144dbb6909c7437b53498b25dd4f4854ab7` | referência de comparação dos deltas |

Os heads foram lidos no GitHub antes da composição. O acesso Git direto do
ambiente local falhou por resolução de DNS; a obtenção foi pelo conector.
O bundle autorizado de bases contém o histórico até a R02 original e a main.
A aplicação do patch do fechamento fornecido na conversa reproduziu exatamente
a árvore `9daeb7c`, conferida contra o commit remoto `5996574`.

Um commit auxiliar LOCAL foi usado para simular a composição com o mesmo
ancestral comum. Esse identificador auxiliar não é commit do usuário e não é
publicado. O conteúdo composto é identificado pelas árvores acima. A candidata
remota usa o conteúdo real das refs fixadas e deve reproduzir o mesmo resultado.
Qualquer registro de runner/CI posterior é acrescentado ao PR e ao pacote da
conversa, sem atribuir ao teste local uma execução remota que não ocorreu.

## Reconciliação, sem descartar uma iniciativa

| Conflito | Resolução na candidata |
|---|---|
| `CHANGELOG.md` | Conserva literalmente o histórico comum e as inserções de ambas as frentes, uma vez cada; acrescenta a entrada R02-I. |
| `CLAUDE.md` | Mantém a rota do Concierge e a proposta dos READMEs com seus estados distintos. |
| `README.md` | Mantém a narrativa complementar, a cobertura dos READMEs e os valores obtidos pela execução da composição; não altera a evidência histórica remota. |
| `tools/ci_local.py` | Mantém quatro etapas comuns, três do Concierge e uma dos READMEs, sem substituir cinco por sete nem sete por cinco. |

A proposta dos READMEs foi renumerada de ADR-0011 para
[ADR-0012](../../decisions/ADR-0012-readmes-de-objeto.md). O conteúdo proposto,
autoria e status foram preservados; foi anexada uma nota administrativa.
O [ADR-0011 do Concierge](../../decisions/ADR-0011-concierge-hub.md) permanece
byte a byte igual à main. Título, índice e referências ativas dos READMEs foram
ajustados. Relatórios e logs antigos conservam os identificadores da época;
uma ponte datada no checkpoint explica a diferença sem reescrever a evidência.

Instruções, Manual, entradas do produto e documentação de ferramentas foram
revisados também nos pontos que o Git combinou sem marcadores de conflito.
Preservou-se a descoberta solicitada e progressiva e a consulta seletiva aos
READMEs. O Manual recebe as duas camadas, sem catálogo paralelo. A redação
canônica foi sincronizada na raiz e o simulado foi regenerado pelo renderer.

## Documentações alteradas além dos READMEs existentes

A [matriz nominal](MATRIZ_INTEGRACAO_R02.md) separa ajustes da composição,
conteúdo herdado de R01/R02, conteúdo já existente na main, ferramentas e
cópias derivadas. Os principais documentos reconciliados são: `CLAUDE.md`,
`.claude/rules/docs-e-readmes.md`, `docs/decisions/README.md`, a proposta
ADR-0012, `tools/README.md`, os índices de sprints, `PLANO_HUB.md`, o checkpoint
R02 e o índice da iniciativa. `CHANGELOG.md` recebeu somente inserções.

O novo [checkpoint R02-I](CHECKPOINT_INTEGRACAO_R02.md) orienta uma próxima
sessão sem exigir releitura da conversa. Este relatório, a matriz e as evidências
são novos; não substituem os relatórios datados de R01/R02.

As duas cópias do Manual e os arquivos do simulado não representam redação
nova. O README do produto só recebeu, além da composição, uma correção curta
na pergunta de navegação para o Concierge. Imagens e identidade visual não
foram alteradas.

## Validação executada localmente

A baseline main passou em sete etapas antes da composição. A candidata passou
nas oito etapas preservadas. Há dez regressões novas de integração, executadas
na mesma etapa dos READMEs por descoberta `test_readme*.py`; os 39 testes
originais dessa frente continuam executados. Foram exercitados mutantes que
removem etapas, repetem nomes, excluem os testes anteriores ou duplicam ADRs.

| Grupo de testes da candidata | Aprovados | Pulados |
|---|---:|---:|
| Biblioteca | 45 | 0 |
| Ferramentas existentes | 39 | 0 |
| Transição | 36 | 7 |
| READMEs: contrato e integração | 49 | 0 |
| Verificador do Concierge | 14 | 0 |
| Integração do Concierge | 12 | 0 |
| Total por execução | 195 | 7 |

O gate inclui ainda validação do produto e validação estrutural do pacote
Concierge; essas etapas não são contadas como casos unittest adicionais.
Reexecutar o gate não cria testes novos. Subtestes negativos também não foram
somados como casos independentes. A advertência preexistente de parsing de
datas da biblioteca pode aparecer no log; zero falhas no validador não significa
ausência de qualquer warning emitido por dependências.

Os logs [da baseline](evidencias_integracao_r02/gate_main_base.txt),
[da candidata](evidencias_integracao_r02/gate_candidata.txt),
[da validação](evidencias_integracao_r02/validacao.txt) e
[do renderer](evidencias_integracao_r02/render.txt) são saídas reais das
execuções locais. O local usa Python 3.13.5; a repetição no runner deve informar
sua versão real, não copiar essa versão por convenção.

## Preservação verificada

O [verificador reproduzível](evidencias_integracao_r02/verificar_preservacao.py)
compara os bytes atuais com as árvores fixadas; o
[resultado estruturado](evidencias_integracao_r02/preservacao.json) registra
os grupos examinados. Eles podem se sobrepor e não devem ser somados como um
inventário de arquivos únicos.

Foram preservados os 16 arquivos canônicos do Concierge, os 19 do protótipo,
os 11 ADRs da main, os 27 arquivos de padrões/exemplares da R02 e os seis
READMEs piloto. As implementações, fachadas e testes dos helpers (124 arquivos),
os 77 notebooks de exemplo, os 16 formulários operacionais e os 98 assets
permanecem idênticos às bases indicadas no verificador. O restante dos
especialistas e a skill de criação são conferidos contra sua fonte apropriada.

As três cópias do Manual são idênticas. O verificador confere também o espelho
do produto, o histórico do changelog, a preservação do corpo da proposta
renumerada, o controle de migração e os gates herdados. Não se usa AST igual
para ocultar mudanças em comentários: os notebooks desta micro-sprint são
comparados byte a byte com a R02 revisada.

Os workflows permanentes conservam o checkout com histórico completo e sem
credenciais persistidas já introduzido na R01; não foram enfraquecidos para
aceitar a composição. Eventuais workflows/dados temporários de transporte
não fazem parte da árvore final. O histórico preparatório é declarado, não
apagado por force-push.

## Limites e próximo aceite

Os sete testes pulados são de Spark opcional no kit de transição. Nesta etapa
não houve execução adicional de XGBoost, notebooks com escrita persistente,
Spark/Databricks, tracking, publicação ou conversas da Genie Code. As evidências
anteriores dessas frentes não foram recontadas como testes desta integração.

Autorrevisão não é auditoria independente; CI verde não é aceite editorial.
A candidata não torna automaticamente os PRs anteriores integrados nem altera
a instalação do usuário. Antes de qualquer merge, reconfirmar main e candidata,
revisar a composição acumulada e coordenar qual PR será integrado. Uma mudança
posterior na main pode exigir nova composição e nova execução.

R03, congelamento 1.0 e encerramento dos PRs anteriores aguardam autorização.
O presente resultado permite revisar a integração concretamente em vez de
seguir produzindo documentos sobre branches com conflitos não tratados.
