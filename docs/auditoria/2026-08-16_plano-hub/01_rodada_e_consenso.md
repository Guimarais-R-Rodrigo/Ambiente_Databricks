# Auditoria do plano de reestruturação — rodada e consenso

Data: 2026-08-16 · Auditor: Claude em sessão sem contexto, com acesso ao sistema
de arquivos e à CLI · Nível: **A1**

## Desenho da rodada

Primeira auditoria do projeto sobre um artefato que **ainda não foi executado**.
As três anteriores julgaram coisas que existem; esta julgou um plano para coisas
que não existem. A pergunta muda de "isto é verdade?" para "isto sobrevive à
execução?".

A instrução central foi executar o plano sobre um objeto real, numa cópia
temporária fora do repositório, e listar tudo que precisou existir, decidir ou
mudar e que o plano não mencionava. Além dos testes usuais, dois novos: um de
**divergência entre executores**, motivado pela intenção de paralelizar a
execução, e um de **plano contra as regras que o próprio projeto escreveu**.

Bloqueados: `CHANGELOG.md`, `docs/auditoria/` e o histórico do git — este último
porque as mensagens de commit descreviam as correções feitas na véspera.

## Resultado

25 achados, **todos procedentes**, verificados um a um contra o disco. Nove
pertencem à classe que só apareceria depois de dezenas de arquivos escritos.

| Categoria | Achados |
|---|---|
| Passo que não funciona como escrito | 9 |
| Ambiguidade que faria dois executores divergirem | 7 |
| Ordem e dependência invertidas | 6 |
| Custo, excesso e imprecisão | 3 |

## Os cinco de maior impacto

**Os padrões nunca chegariam ao workspace.** `render_simulado.py` copia
exatamente `.assistant_instructions.md` e `.assistant/`. Uma pasta `padroes/` na
raiz do repositório fica invisível para o Genie Code — e a skill
`hub-ml-criar-objeto`, cuja função é aplicar esses templates, roda lá dentro. A
Sprint 11 seria descoberta como inexecutável onze sprints depois de a Sprint 1
colocar os arquivos no lugar errado.

**A Sprint 2 reprovava o próprio critério de aceite.** Simulada, terminava em
`REPROVADO: 40 falha(s)`: são 43 links markdown, em 33 arquivos, apontando para
as três pastas que a sprint remove — 35 deles só para `catalogo_helpers.md`,
citado em 12 `SKILL.md` e nos 16 prompts. Pior, o destino que o plano declarava
para eles só nasceria quatro sprints adiante.

**Nada apagava o workspace.** `import-dir --overwrite` sobrescreve e nunca apaga.
Depois da Sprint 3, `.assistant/skills/` teria 24 pastas — 12 órfãs e 12 novas,
com `description` idêntica duas a duas. É a colisão de roteamento que os forward
tests existem para pegar, criada pelo próprio plano. E a verificação humana que a
Sprint 2 declarava ("as três pastas ausentes") retornaria o resultado errado.

**O `__all__` não tinha regra, e há imports cruzados que dependem dela.** Seis
imports absolutos entre módulos da biblioteca, mais nove em `tests/test_core.py`.
`constants/colors` tem 22 nomes públicos e `section_header` importa três deles;
um executor que interprete "API pública" como curadoria quebra o import — a
auditoria reproduziu o `ImportError`. Trinta e sete dos 51 módulos têm mais de um
nome público, e `smart_sample` é escrito três sprints antes de quem o consome.

**Os números de escopo contradiziam a tabela do próprio plano.** As Sprints 2 e 3
declaravam 601 e 262 ocorrências, medidas sobre um universo que incluía as
camadas que a seção seguinte mandava preservar. O escopo real é 471 e 162 — o
plano superestimava a Sprint 2 em 27% e a Sprint 3 em 62%.

## O que a auditoria produziu além dos achados

**Doze decisões implícitas.** Ao executar o plano sobre um snippet, o auditor
precisou decidir doze coisas que o plano não dizia e que produzem arquivos
diferentes: o preâmbulo de `sys.path` sem o qual nenhum dos 74 notebooks importa
a biblioteca; o formato-fonte do notebook, incluindo que `%pip` escrito do jeito
natural faz a validação reprovar; o nome do arquivo de exemplo, que o plano
grafava de três formas; e onde os notebooks didáticos moram entre a sprint que
apaga a pasta deles e a que os reaproveita.

**Um defeito que já existia.** `GUIA_REPLICACAO_TEMPORARIO.md` está rastreado no
git e afirma na linha 3 não estar.

**Fragilidade na detecção de notebook.** `eh_notebook` lê a primeira linha crua e
falha com BOM, linha em branco ou comentário de encoding antes do marcador —
convenção usada por 11 módulos do repositório. A falha é silenciosa: o notebook é
publicado como arquivo, a conferência aprova, e o smoke test passa a importá-lo.

**A ferramenta de validação é cega para o que virá.** Rodada sobre um resultado
com notebook duplicado, link quebrado e import errado, devolveu `APROVADO, 0
falhas`. O critério de aceite do plano dependia dela.

## O que o auditor confirmou

O desenho do `__init__.py` preserva 226 referências pontilhadas em 59 arquivos, e
só uma referência no repositório inteiro usa caminho de arquivo — a
reestruturação de 51 objetos custa uma linha de documentação. O diagnóstico do
`walk_packages` foi reproduzido, inclusive o mecanismo exato da falha. Todos os
inventários de objeto bateram sem divergência. E o princípio de não falsificar
registro datado foi considerado correto, com a distinção entre registro e
instrumento apontada como acertada.

## O que ficou sem verificação

Se um objeto NOTEBOOK dentro de pasta de pacote aparece como `.py` no mount
`/Workspace` — premissa da única alteração de código da Sprint 0, que exigiria
executar uma célula no laboratório. Se `--execute` publica 74 notebooks a quatro
níveis com o tipo certo, o que exige uma publicação real. E se os 16 módulos da
Sprint 7 **executam**, não só importam, no Free: a bateria atual só testou import
para `ml`.

## Lição para o processo

Quarta rodada em que uma sessão sem contexto encontra defeito relevante em
material já revisado pelo autor: 13 na biblioteca, 22 e 25 na documentação, 25
aqui. A taxa não cai.

O que esta rodada acrescentou ao método foi auditar **antes** de executar. Os
cinco achados de maior impacto custam, agora, uma revisão de plano; descobertos
na Sprint 6, custariam sprints inteiras de retrabalho. É a razão de o plano v2
passar a prever uma rodada de auditoria ao fim de **cada** sprint, com
profundidade variável conforme o que a sprint produz.

O teste de divergência entre executores foi o mais produtivo dos novos: sete
achados que não são erro nenhum para um executor sozinho, e viram 74 arquivos
com caras diferentes quando o trabalho é paralelizado.
