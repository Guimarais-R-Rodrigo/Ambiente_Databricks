# Análise de simplificação e preparação para o trabalho

> Análise/plano anteriores à execução. As decisões autorizadas e o estado atual estão no [registro da execução](execucao-faxina-2026-10-07.md); contagens e recomendações abaixo descrevem a baseline analisada.

Data: 07/10/2026 · Autor: Codex · Natureza: diagnóstico e recomendação.
Base examinada: `8dd8da57de89122241890b8b6b059fd2f9be25d0`.
Destino informado pelo usuário: **GitHub Copilot no VS Code e Databricks**.
Execução proposta: [plano por sprints](plano-faxina-2026-10-07.md).

## 1. Parecer

O Hub já reúne um produto utilizável e uma infraestrutura extensa de manutenção.
A próxima etapa deve facilitar uso e evolução: uma entrada curta, documentação
atual claramente identificada e histórico consultado somente quando necessário.
Excluir arquivos por terem sido escritos durante uma sprint removeria também
contratos e verificações que continuam ativos.

Recomendo manter um repositório canônico de manutenção e uma entrega de produto
com fronteira explícita. O computador do trabalho pode precisar do primeiro para
edições com Copilot; o workspace Databricks recebe o segundo. O empacotamento atual
já distingue essas camadas. Uma terceira entrega de manutenção reduzida só deve
existir se houver necessidade concreta e fechamento de suas dependências.

| Pedido | Conclusão | Encaminhamento |
|---|---|---|
| Substituir `.claude/` por `.agents/` | suporte a `AGENTS.md` não demonstra descoberta de `.agents/skills` pelo Claude Code | manter fonte em `.agents/skills` e adaptador Claude gerado; avaliar perfil corporativo somente Copilot |
| Manter workflows? | protegem regressões e distribuição; parte já foi consolidada | manter cobertura, documentar os 20 e simplificar receitas por equivalência |
| Renomear `ambiente_databricks` | possível, mas quebra referências e ferramentas se for uma troca isolada | sprint opcional após centralizar a resolução de paths |
| Limpar `docs/` | contém história, guias e dados executáveis misturados | preservar guias/contratos, retirar cronologia da entrada e migrar dependências antes de arquivar |
| Apagar `novas_funcionalidades/` | protótipo já integrado, porém sua retenção é testada | retirar da árvore corrente em migração própria, preservando recuperação e provas |
| Apagar `tools/` | retiraria a manutenção, validação e distribuição | manter núcleo e testes; classificar comandos atuais, auxiliares e históricos |
| Escolher um Manual Técnico | raiz e produto são cópias iguais; V2 é outra edição, mais recente e muito maior | consolidar autoridade editorial e migrar links/âncoras antes de aposentar a edição anterior |

## 2. Método, cobertura e limites

Foi inventariado o conjunto versionado da baseline: **1.874 arquivos**, cerca de
45,1 MB de bytes de trabalho, sem `.git`, caches, `.artifacts/`, arquivos locais
ignorados ou quarentena. Foram analisados os 20 YAMLs, seus triggers/jobs/steps,
o gerador de CI, entradas de documentação, contratos de manutenção, consumidores
críticos de paths e manifestos dos manuais/protótipo.

A [triagem por arquivo](inventario-faxina-2026-10-07.csv) cobre os 828 arquivos de
`docs/` e os 278 de `tools/`, com classe preliminar e ação proposta. Essa triagem
é estrutural e por finalidade; **não é uma revisão semântica integral de cada
relatório histórico nem uma lista de exclusão aprovada**. As análises detalhadas
abaixo verificam os consumidores que tornam cada decisão arriscada. Referências
montadas dinamicamente e dependências fora do repositório exigem a prova de cada
sprint antes da remoção.

O CSV é instrumento transitório deste plano, não outro catálogo operacional:
61 documentos têm referência literal identificada em código/JSON de ferramentas
ou YAMLs de CI. Ausência de match não prova ausência de uso, pois imports, paths
relativos e nomes construídos podem escapar da busca. Ao fechar a limpeza,
preservar a triagem como evidência, fora das rotas de contexto inicial.

Pesquisa de plataforma: fontes oficiais Anthropic, Microsoft e GitHub consultadas
em 07/10/2026. Documento oficial comprova comportamento documentado; o cliente
instalado e as políticas corporativas ainda precisam do ensaio de uso no destino.
Não houve execução de Claude Code, Copilot ou Genie nesta análise.

| Área da baseline | Arquivos | Bytes | Leitura da medida |
|---|---:|---:|---|
| Produto `ambiente_databricks/` | 708 | 25.959.243 | inclui código, documentação e assets |
| Governança/documentação `docs/` | 828 | 13.360.182 | parte é evidência, parte é input de validação |
| Manutenção `tools/` | 278 | 5.225.547 | 196 Python, sendo 100 sob diretórios de testes |
| Workflows | 20 | 84.255 | pequena fração dos bytes, relevante para regressão |
| Protótipo `novas_funcionalidades/` | 19 | 80.366 | baixo ganho de espaço, bom ganho de clareza ao retirar |
| Skills canônicas `.agents/` | 6 | 35.274 | cinco procedimentos e índice |
| Adaptadores `.claude/` versionados | 6 | 34.397 | cinco skills geradas e manifesto |

Bytes e quantidade de arquivos não medem tokens efetivamente carregados. O
problema de contexto depende dos imports, da busca e dos recursos selecionados.
Um arquivo no disco não é necessariamente lido em toda conversa. O controle mais
útil é medir os arquivos realmente usados em tarefas representativas.

## 3. Claude, `.agents` e Copilot no VS Code

### Resultado da pesquisa oficial

Claude Code documenta leitura direta de `AGENTS.md` desde v2.1.277, condicionada
à configuração e presença de arquivos da família CLAUDE no diretório/ancestrais.
Versões anteriores a v2.1.281 tinham restrições adicionais; plugin desabilitado
também pode impedir a leitura. O import por `CLAUDE.md` permanece alternativa.
Fonte: [memória e AGENTS.md](https://code.claude.com/docs/en/memory#agentsmd).

A documentação de skills do Claude Code lista `.claude/skills/` como diretório
de projeto e outros locais específicos por escopo. **Não encontrei nessa fonte
oficial suporte documentado a `.agents/skills/` como substituto.** Isso é ausência
de confirmação documental, não uma prova experimental de impossibilidade.
Fonte: [locais de skills](https://code.claude.com/docs/en/skills#choose-where-skills-load).

Também não há base para tratar `.agents/` como substituição universal de settings,
regras, hooks e agentes de `.claude/`. São mecanismos distintos. O cliente é
Claude Code; selecionar um modelo Claude dentro do Copilot não transforma o
carregador de contexto do VS Code no carregador do Claude Code.

Para Copilot no VS Code, a documentação lista `.agents/skills/`,
`.github/skills/` e `.claude/skills/` como locais de skills. `AGENTS.md` é uma
opção de instrução do projeto; descoberta depende da interface de agente
selecionada e das configurações aplicáveis. Fontes: [skills no VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)
e [instruções no VS Code](https://code.visualstudio.com/docs/agent-customization/custom-instructions).

### O que existe no projeto

- `AGENTS.md` contém o núcleo comum: 75 linhas e 4.939 bytes na baseline.
- `CLAUDE.md` contém apenas `@AGENTS.md`; não duplica o texto do núcleo.
- As cinco skills editáveis vivem em `.agents/skills/`.
- As cinco de `.claude/skills/` são produzidas por `tools/ai_controls.py`;
  `.generated.json` registra origem, transformação e hashes.
- `docs/ai/compatibility.md` contempla Codex/Claude/Gemini/Grok, mas **não tem uma
  linha específica para Copilot no VS Code**, agora confirmado como destino.

**Opinião:** conservar a fonte neutra e o adaptador mínimo é adequado ao
repositório multiagente. A duplicação física gerada tem custo pequeno e evita
autoria concorrente. Para uma futura entrega somente Copilot, omitir o adaptador
Claude pode fazer sentido, mas exige perfil de empacotamento e teste de descoberta;
apagar arquivos da cópia atual reprovaria o gate que exige as saídas geradas.

No VS Code, conferir descoberta e uso de cada skill, inclusive a coexistência de
nomes iguais em `.agents` e `.claude`. Não presumir deduplicação uniforme entre
clientes. Não criar automaticamente uma terceira cópia em `.github/skills`.

## 4. Workflows: finalidade atual e potencial de simplificação

Foi criado o [README dos workflows](../../.github/workflows/README.md), com cada
arquivo, check, gatilho, cobertura, ambiente e efeito. A ausência desse índice
local era uma lacuna: havia explicação parcial em `docs/manutencao/saida-gerada.md`,
mas era necessário cruzá-la com os YAMLs para compreender o conjunto.

### O que já foi otimizado

O CI central contém cinco perfis comuns e 12 jobs derivados. Os workflows V00 e
V04–V14 são receitas manuais consumidas pelo compilador `tools/ci_workflows.py`.
Apagá-los por parecerem campanhas concluídas faz o compilador perder seus inputs.
Eles já deixaram de disparar individualmente em todo push.

V01–V03, SE01/SE02, Micromodelos e kit mantêm gatilhos próprios. Há oportunidade
de simplificar filtros redundantes e avaliar sobreposição de validações, mas a
equivalência precisa considerar Python, Spark/Java, widgets, dependências App,
seed, runner, artifacts e resultado obrigatório. Testes de interface e de pacote
não se tornam redundantes apenas por importar o mesmo núcleo.

### O que manter

1. Validação estrutural e contratos do produto.
2. Testes que detectam regressões de comportamento e falhas já encontradas.
3. Geração, extração e verificação do pacote no ambiente alvo de compatibilidade.
4. Contratos de skills, núcleo de temas e Micromodelos enquanto integrarem o Hub.
5. Identidade dos checks usados por governança até migrar seus consumidores.

### O que merece revisão

- Nomes baseados em sprints escondem a função atual: `micromodelos-mm01-ci.yml`
  já descobre a família `test_micromodelo*.py`, com alcance além de MM01.
- Há frases de campanha e echoes de estados humanos antigos nas receitas. Não
  devem ser apresentados como uma nova homologação executada pelo CI.
- V08/V12 têm guardas condicionais de escopo de campanha; separar essas guardas
  das regressões permanentes permite esclarecer o que uma release verifica.
- `tools/skill_enforcement/README.md` diz que Actions é reservado a candidata/Ready;
  `ci.yml` roda em todo PR, inclusive draft. A descrição operacional precisa
  distinguir preferência de trabalho e triggers efetivamente implementados.
- Um PR documental estreito ainda pode acionar vários perfis. Medir duração/custo
  antes de acrescentar filtros; preservar a propagação de falha upstream.

Consulta read-only ao GitHub nesta análise: `main.protected=false`, rulesets
visíveis vazios e required checks retornando HTTP 404 `Branch not protected`.
Isso atualiza a observação local de acesso, sem reescrever o relato histórico
de 403. O repositório de destino terá sua própria configuração.

**Opinião:** manter CI para manutenção. Para instalação Databricks, essa pasta
já fica fora do pacote. Para um computador com Copilot, os YAMLs ajudam a IA a
encontrar a receita real; um README claro reduz a necessidade de lê-los todos.
Uma futura consolidação por capacidades é melhor do que apagar a proteção junto
com a nomenclatura de sprint.

## 5. Renomear `ambiente_databricks/`

Primeiro, uma correção do mapa mental: essa pasta é a **fonte editável do produto**.
Quem simula a árvore de workspace é `.artifacts/simulado/`, produzido pelo renderer.
O nome `ambiente_databricks/` é compreensível, mas o README precisaria continuar
dizendo claramente que se trata da fonte e que o espelho é gerado.

Busca literal no texto UTF-8 versionado da baseline encontrou `ambiente_databricks`
em **533 arquivos, com 17.689 ocorrências**: 142 arquivos de `tools`, 13 workflows,
303 documentos em `docs`, além das instruções, produto, manuais e protótipo.
São referências de naturezas distintas, não 17.689 mudanças obrigatórias.
O atlas e mapas extensos ampliam muito a contagem.

| Consumidor confirmado | O que uma renomeação isolada quebra |
|---|---|
| `tools/render_simulado.py`, constante `SOURCE` | procura a raiz antiga e deixa de gerar o produto |
| `tools/validate_assistant.py` e inventário | raiz padrão, varreduras e snapshot deixam de representar o layout |
| `tools/micromodelo_mm01_contract.py` e fachadas irmãs | bootstrap do módulo de domínio aponta ao local antigo |
| `tools/package_boundary.py` e `tools/ai_controls.py` | contratos de payload e igualdade fonte/derivado procuram paths fixos |
| YAMLs, testes e `tools/ci_workflows.py` | filtros, comandos, dependências e receitas ficam incompatíveis |
| `docs/ai/task-context.json` e mapa de controle | seleção de contexto e resolução dos owners falham |
| `tools/tests/test_readme_integracao.py` | comparação do Manual usa path antigo |
| manuais, mapas e manifesto V2 | links e referências à base precisam de revisão; hashes de arquivos alterados mudam |
| evidências históricas e hashes congelados | troca global adulteraria o que foi observado na revisão original |

**Opinião:** o ganho é de clareza, não funcional. Manter o nome atual durante a
limpeza de maior retorno reduz risco. Se o usuário preferir `ambiente_databricks`,
adotar em uma sprint própria, com resolução central de paths, migração dos
consumidores vivos e equivalência do payload extraído. Não usar busca/substituição
global e não manter duas árvores editáveis ou symlink de compatibilidade.

## 6. `docs/`: disposição por área

A pasta representa cerca de 29,6% dos bytes versionados. Dois blocos concentram
a maior parte: auditoria, aproximadamente 7 MB, e sprints, aproximadamente 4,3 MB.
O arquivo `DISPOSICOES.json` da auditoria de READMEs tem sozinho 3.669.901 bytes;
é evidência de uma campanha, inadequada como leitura obrigatória de entrada.

| Área | Arquivos | Avaliação | Recomendação |
|---|---:|---|---|
| `docs/README.md` | 1 | boa separação entre evidência e operação; faltava rota direta de manutenção | manter como índice curto |
| `ai/` | 57 | núcleo útil, porém mapas detalhados e compatibilidade ainda orientada aos clientes anteriores | manter regras/rotas; acrescentar Copilot e consultar JSONs grandes somente por tarefa |
| `auditoria/` | 72 | provas e matrizes de campanha; alguns JSONs são inputs dos gates atuais | manter rastreabilidade; excluir do contexto inicial; extrair inputs ativos antes de arquivar fisicamente |
| `decisions/` | 28 | decisões justificam contratos que continuam válidos | manter índice/status; consultar ADR por tema, sem carregar todos |
| `guias/` | 1 | guia de deploy/rollback App sem README da coleção | integrar rota ao playbook visual ou criar entrada curta |
| `handoffs/` | 11 | índice já distingue consumidos e residual conhecido | manter pendências visíveis; esconder consumidos da entrada diária sem apagar provas |
| `historico/` | 14 | retenção já estruturada e verificada | manter recuperação; evitar impor consulta universal |
| `manutencao/` | 4 na baseline | guias úteis, sem README agregador | criar entrada local; entregue nesta rodada |
| `playbooks/` | 6 | operação útil para transferência; índice não lista o aceite específico de Micromodelos | completar catálogo e separar instalação de manutenção |
| `sprints/` | 582 | mistura registros encerrados, índices vivos, fixtures, schemas e matrizes operacionais | classificar por função; extrair dependências ativas; cronologia fora da rota padrão |
| `testes/` | 52 | protocolos e resultados ambientais necessários para interpretar compatibilidade | manter procedimentos atuais e ligações à evidência; resultados brutos sob consulta |

### Dependências que impedem apagar `docs` ou suas sprints

- `tools/readme_objeto_contract.py` lê
  `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`: é um controle ativo de
  cobertura, não apenas um relato de sprint.
- `tools/temas_v01_contract.py` usa a pasta V01; `tools/temas_v02_check.py` lê
  fixtures e `referencias_assets.json` ali presentes.
- `tools/temas_v13_operacional.py` lê `V13/MATRIZ_OPERACIONAL.json`.
  `tools/temas_v14_ownership.py` valida referências à governança V01 e matriz V13.
- O preflight de execução paralela usa
  `docs/sprints/skill_enforcement_rollout/PARALELO` como parte do contrato.
- `tools/ai_controls.py` depende do mapa/registry e de baseline/proveniência em
  `docs/auditoria/2026-10-06_ai-instrucoes/`.
- `tools/micromodelo_free_kit.py` transporta a instrução `KIT_FREE.md` localizada
  na documentação de Micromodelos.

Arquivar essas pastas sem migrar os leitores tornaria a manutenção incompleta.
A mudança útil é levar contratos vivos para um lugar com nome operacional,
preservar a revisão histórica e atualizar referências/testes como um conjunto.

### Lacunas editoriais concretas

1. `docs/sprints/README.md` ainda contém, numa seção histórica sem destaque
   temporal suficiente, a afirmação de que V14 está na S0 e S1–S8 não começaram.
   O índice vigente de Temas já registra S0/S1 integradas. Colocar estado vivo no
   topo e datar a narrativa evita uma LLM usar o primeiro match como presente.
2. A tabela de auditoria em `docs/auditoria/README.md` fala em A2 para mudança
   estrutural/ida ao trabalho; a regra comum em `docs/ai/rules/colaboracao.md`
   define gatilhos mínimos A1+ e escopo distinto. Centralizar a política e
   explicar quando A2 é exigido, sem escolher silenciosamente a versão mais leve.
3. `tools/README.md` possui inventário seletivo. Muitos comandos de Micromodelos,
   SER e Temas exigem outra busca para saber se são atuais ou históricos.
4. A documentação antiga ainda manda editar o Manual anterior; o V2 declara
   coexistência. É um conflito de orientação editorial a resolver por decisão.
5. O empacotador de contexto oferece `task`, mas `canonical/full` continuam
   podendo levar a história arquivada. Mover pasta não reduz sozinho o contexto
   desses modos: a seleção tem de ser deliberada e identificada.

**Opinião:** a documentação é rica em contratos e evidências, mas ainda custa
muito descobrir a rota corrente. O objetivo é reduzir o percurso de leitura e
as ambiguidades, não adicionar um README em cada pasta histórica nem resumir
toda a história novamente.

## 7. `novas_funcionalidades/`

O conteúdo atual é o protótipo Concierge 0.1.0, com 19 arquivos. A versão em uso
vive em `ambiente_databricks/.assistant/skills/hub-ml-concierge/`. O próprio README
do protótipo já declara finalidade histórica.

Há 29 arquivos com menções literais à pasta; cinco são internos ao protótipo e
24 externos. Os consumidores incluem:

- `docs/historico/concierge-manifest.json`, com paths e hashes dos 19 arquivos;
- `tools/tests/test_ai_history.py`, cujo teste exige esses arquivos na worktree
  e compara os bytes retidos;
- `tools/inventario_visual.py` e seu teste, que classificam a camada experimental;
- links de ADR/relatórios, entradas de `docs/ai/control-map.json` e scripts de
  preservação de campanhas encerradas.

**Resposta direta:** faz sentido retirar essa pasta da árvore ativa. Apagá-la
isoladamente quebra pelo menos o teste de retenção e links. Não é dependência
de execução analítica do Concierge atual identificada nesta análise.

O caminho proposto é uma retenção recuperável por commit completo/manifesto,
com localizador histórico, substituindo a exigência de presença corrente por
prova de recuperação dos mesmos bytes. Scripts históricos continuam na sua
revisão de origem. O teste novo deve detectar perda real do arquivo recuperável;
simplesmente excluir o teste seria perda de garantia.

## 8. `tools/`: o que é e o que deve acompanhar o trabalho

Não há pasta `todos` na baseline; o pedido foi interpretado como `tools/`.
Ela contém as ferramentas usadas **depois** que se altera um módulo, README,
skill, contrato ou pacote. Sua função permanece durante a manutenção.

| Família | Exemplos | Disposição recomendada |
|---|---|---|
| Validação e invariantes | `validate_assistant`, `project_policy`, `repo_inventory`, `readme_objeto_contract`, parsers Markdown | manter na manutenção |
| Geração e distribuição | renderer, `simulado`, bundles, kit, marcadores e aceites | manter; execução conforme operação |
| Regressões | 100 módulos Python sob diretórios de testes, fixtures e contratos | manter; organizar por capacidade/ambiente |
| Qualidade da camada IA | `ai_controls`, `task_context`, `ci_workflows`, `package_boundary` | manter enquanto seus contratos forem ativos |
| Temas operacionais | preflight, diagnóstico, release/rollback, ownership, builders | manter enquanto as respectivas superfícies existirem |
| Micromodelos | fachadas `micromodelo_mm*` e execução local | preservar compatibilidade; implementação principal já pertence ao produto |
| Campanhas Free | scripts `*_free_probe.py`, `free_kit/` | acesso sob demanda; documentar efeitos e alcance, sem rodar na análise |
| Certificadores congelados | MM01 v1 e SER pré-promoção | manter como história reproduzível; afastar da receita corrente |
| Orquestração B0 | `skill_enforcement/parallel/` | opcional para rotina individual, mas atualmente referenciada por gates e catálogos |
| Autoria visual | `readme_visuals/`, renderer v1 e produção v2 | manter produção/ativos/licenças; v1 e `publish_sprint0` candidatos à retenção histórica |

Há 196 Python na pasta, 100 de teste e 96 restantes. Esses números não equivalem
a 96 comandos que o usuário precise aprender. Muitos são módulos de apoio,
fachadas ou implementações internas. O README precisa privilegiar cerca de uma
dezena de operações por objetivo e oferecer inventário completo sob demanda.

Alguns comandos antigos são finas camadas de compatibilidade: por exemplo,
`micromodelo_mm01_contract.py` direciona ao módulo de especificação no produto.
Apagar a fachada não simplifica a implementação central, mas quebra chamadas
que ainda a usam. Registrar consumidores e janela de descontinuação primeiro.

**Opinião:** para manter código com Copilot, conservar `tools` e os testes é
essencial. Para apenas importar bibliotecas no notebook Databricks, não é preciso
copiar toda essa pasta; o pacote atual já seleciona o produto e os aceites próprios.
Um checkout reduzido não pode alegar passar o validador integral atual, que exige
Git e histórico para determinados controles.

## 9. Os três caminhos do Manual Técnico

| Documento | Bytes / linhas na baseline | Situação confirmada |
|---|---:|---|
| `MANUAL_TECNICO.md` na raiz | 244.333 / 2.622 | cópia de leitura da edição anterior |
| `ambiente_databricks/.assistant/MANUAL_TECNICO.md` | 244.333 / 2.622 | fonte editorial dessa mesma edição |
| `ambiente_databricks/.assistant/MANUAL_TECNICO_V2.md` | 3.889.178 / 21.252 | livro técnico novo, edição de 07/10 |
| `ambiente_databricks/.assistant/MANUAL_DO_USUARIO.md` | 500.166 / 3.076 | livro novo para uso do Hub |

As duas cópias sem V2 têm SHA-256 idêntico:
`dfb4a042183d58a4100c6ef1f4b50a0aa5cc82aee605dae2886c164af068f513`.
Ambas foram alteradas mais recentemente no commit `432a051c`, de 06/10/2026;
portanto o manual anterior também recebeu manutenção recente. O V2 entrou em
`cf0bb063`, de 07/10, com base técnica declarada `983c9936`.

O anterior combina fundamentos, operação, catálogo e glossário. O V2 tem
estrutura editorial diferente: arquitetura, objetos, skills, enforcement,
Micromodelos, sistema visual, manutenção, atlas e complementos. Não é uma mera
cópia renomeada, nem se pode garantir que cada trecho anterior tenha sucessor
equivalente apenas porque existe “V2” no nome.

A edição nova também oferece 46 partes de leitura e mapas em `manuais_v2/`.
Essa pasta soma 8.172.308 bytes; junto dos dois livros novos, são 12.561.652 bytes,
cerca de 48,4% do produto. Parte desse volume é deliberadamente duplicada para
permitir leitura do livro inteiro e por capítulos. Importar todos esses arquivos
como contexto seria uma escolha ruim; selecionar capítulo/ficha é mais adequado.

Foi conferido o manifesto: **53 arquivos, zero divergências de tamanho/hash**.
Isso comprova integridade da edição, não uma auditoria de todas as afirmações.
Sua [regra de manutenção](../../ambiente_databricks/.assistant/manuais_v2/MANTER_EDICAO.md)
preserva expressamente a autoridade do manual anterior prevista no ADR-0010.
O teste `test_readme_integracao.py` ainda exige igualdade raiz/produto dessa edição.

**Recomendação editorial:** adotar o Manual do Usuário como entrada de uso e o
conteúdo técnico V2 como referência aprofundada, após uma matriz de cobertura
da edição anterior. Definir uma fonte editorial modular e gerar o volume completo,
ou conservar o volume como fonte e automatizar as partes; escolher apenas uma
dessas direções. Atualmente o roteiro pede sincronização manual das partes.

Depois da migração, a raiz pode ter um pequeno portal de manuais em vez de outra
cópia integral. Preservar as âncoras antigas ou oferecer um mapa de migração antes
de retirar `MANUAL_TECNICO.md`: 168 arquivos contêm 496 menções literais a esse
nome na baseline. A mudança exige sucessão explícita do contrato editorial,
revisão de testes, links e manifesto. Não retirar o antigo agora só por data.

## 10. Posicionamento para uso profissional

### Visão de uso

O usuário encontra o guia do Hub, Manual do Usuário, skill/briefing adequado,
README do objeto e exemplo. Histórias de sprint não integram a orientação inicial.
A pasta `.assistant` continua sendo o produto instalado; regras do mantenedor
não devem ser misturadas às instruções do assistente analítico.

### Visão de manutenção com Copilot

Entrada curta por `AGENTS.md` e README, seguida da rota pertinente em `docs/ai`.
Cada tarefa abre a implementação, seu contrato e os testes afetados. O histórico
é consultável por link/SHA quando uma decisão ou regressão exigir explicação.
Abertura em VS Code e leitura por Copilot precisam ser testadas na versão e
interface de agente efetivamente usadas no trabalho.

### Visão de arquivo e recuperação

Relatórios, campanhas encerradas e protótipos têm índice de recuperação, versão
e hashes. Manter cópia recuperável não obriga carregar seu conteúdo em cada chat.
Mover uma pasta para `historico` é insuficiente quando busca/bundle continuam
incluindo tudo; as rotas de contexto devem tornar a seleção explícita.

Prioridade: melhorar as entradas e separar contratos vivos; depois retirar
protótipo/receitas históricas; por fim considerar renomeação e pacote de
manutenção reduzido. O plano detalha dependências, critérios e rollback.

## 11. Evidência desta rodada

- Inventário do Git completo, parsing dos 20 workflows e busca de referências
  sobre os arquivos UTF-8 versionados. Tamanhos/hashes medidos nos bytes locais;
  `.gitattributes` define normalização, mas não houve export de conteúdo privado.
- Validador da baseline com `--conferir-readme`: aprovado, zero falhas/avisos
  na sincronização imediatamente anterior desta mesma sessão.
- `python -B tools/ci_workflows.py --check`: PASS na análise.
- `python -B tools/ai_controls.py --check`: PASS na análise, cinco skills
  canônicas e cinco saídas geradas, escopo estático.
- Manifesto V2: 53/53 correspondências; Manual anterior raiz/produto idêntico.
- Não foram alterados produto, workflows YAML, policy ou paths nesta entrega.
  A documentação de workflows e o planejamento são as alterações realizadas.
- A validação da documentação entregue e os comandos finais são registrados no
  [plano](plano-faxina-2026-10-07.md#verificacao-desta-entrega).

Revisão desta análise: autorrevisão de contexto completo por Codex; não é
auditoria independente nem homologação do ambiente corporativo.
