# Plano de simplificação do Hub por sprints

> Análise/plano anteriores à execução. As decisões autorizadas e o estado atual estão no [registro da execução](execucao-faxina-2026-10-07.md); contagens e recomendações abaixo descrevem a baseline analisada.

Data: 07/10/2026 · Autor: Codex · Estado: **PROPOSTA PARA DECISÃO**.
Base: `8dd8da57de89122241890b8b6b059fd2f9be25d0`.
Diagnóstico: [análise detalhada](analise-faxina-2026-10-07.md).
Destino confirmado: **Copilot no VS Code e Databricks**.

Este plano organiza a execução futura. Nesta rodada foram produzidos diagnóstico,
inventário e documentação; renomeações, remoções e mudança de autoridade dos
manuais permanecem propostas. F00 é a análise entregue; F01–F08 não começaram.

## Resultado esperado

Uma pessoa e uma IA devem conseguir identificar rapidamente:

1. Onde usar o Hub e onde editar sua fonte.
2. Qual guia ou contrato rege a tarefa atual.
3. Qual teste executar e o que seu resultado comprova.
4. Qual pacote levar ao Databricks e qual checkout usar para manutenção.
5. Onde recuperar a história, sem tratá-la como instrução atual.

A proposta mantém um Git canônico. A entrega Databricks continua derivada da
fonte; qualquer pacote reduzido para manutenção terá seu próprio contrato de
verificação. Não será criado um segundo código editável em paralelo.

## Decisões a fechar na F01

| Decisão | Recomendação do diagnóstico | Alternativa e consequência |
|---|---|---|
| Layout da fonte | manter `ambiente_databricks` inicialmente | adotar `ambiente_databricks` na F06, com migração completa |
| Claude | manter `.agents` canônica e `.claude/skills` gerada no repositório multiagente | perfil corporativo só Copilot pode omitir o adaptador, com testes próprios |
| Manuais | Manual do Usuário para uso; conteúdo V2 para aprofundamento, após mapa de cobertura | manter duas edições operacionais exige regra clara de precedência e sincronização |
| Conteúdo para o computador do trabalho | checkout completo para manutenção, contexto selecionado por tarefa | pacote reduzido exige desacoplar dependências e certificação específica na F07 |
| Histórico | recuperável por Git completo e manifesto; fora da leitura inicial | retenção física corrente apenas para evidência exigida por contratos ainda ativos |
| CI | preservar cobertura e reorganizar por capacidade | conservar o desenho atual documentado se a redução não compensar o risco |

Essas escolhas podem ser aprovadas por conjunto. Não exigem uma nova confirmação
para cada arquivo depois que objetivo, critérios e efeitos da sprint estiverem
autorizados. Publicação no destino e transferência de dados continuam operações
com alcance próprio.

## Sequência e dependências

| Sprint | Entrega principal | Depende de | Tamanho relativo |
|---|---|---|---|
| F00 | diagnóstico, inventário e README de workflows | baseline sincronizada | entregue |
| F01 | decisões de layout/contexto e perfil Copilot | aceite do diagnóstico | pequeno |
| F02 | documentação viva e contratos separados da cronologia | F01 | grande |
| F03 | manuais consolidados com âncoras e geração | F01 e rotas da F02 | grande |
| F04 | catálogo de ferramentas e CI simplificado com cobertura preservada | F02 | grande |
| F05 | retirada recuperável do protótipo e legado sem consumidores ativos | F02/F04; mapa final de consumidores | médio |
| F06 | renomeação opcional da fonte | F02–F05 estabilizadas | grande, opcional |
| F07 | entrega e manutenção no trabalho com perfil explícito | F03–F06; F06 pode ser dispensada | médio |
| F08 | ensaio integrado, revisão e fechamento | todas as escolhidas | médio |

“Pequeno/médio/grande” indica amplitude de dependências, não prazo garantido.
A disponibilidade do VS Code corporativo e do Databricks determina os ensaios
no destino. Sem acesso, a preparação local pode terminar e o ensaio fica pendente.
Cada sprint deve ser uma mudança revisável e reversível; evitar uma PR única
misturando renomeação, descarte, manuais e CI.

## F00 — Diagnóstico e documentação imediata

**Objetivo:** substituir suposições por inventário, fontes oficiais e referências
concretas antes de mexer na estrutura.

Entregas desta rodada:

- relatório com resposta aos sete pontos do pedido;
- triagem de todos os arquivos de `docs/` e `tools/` da baseline;
- [README dos 20 workflows](../../.github/workflows/README.md);
- índice de manutenção, plano por sprints e marco no changelog;
- validação local da documentação entregue.

Critério de conclusão: arquivos locais navegáveis, nenhuma alteração de runtime,
YAML ou policy, e limites da pesquisa/triagem declarados. O relatório não
reclassifica campanhas antigas nem inicia automaticamente F01.

## F01 — Definir as entradas e o perfil de manutenção

**Objetivo:** estabelecer o que Copilot deve consultar e o que realmente precisa
acompanhar o usuário no computador do trabalho.

**Trabalho:**

1. Ratificar as escolhas da tabela de decisões, incluindo executar ou dispensar F06.
2. Acrescentar Copilot no VS Code à matriz de compatibilidade, com versão,
   extensão e interface de agente usadas; distinguir Copilot de Claude Code.
3. Atualizar o registro de fontes oficiais por uma revisão nova, preservando a
   pesquisa de 06/10 e seus hashes históricos.
4. Manter um único núcleo em `AGENTS.md`; revisar se cada frase é necessária
   em quase toda tarefa. Levar procedimentos específicos às skills/rotas existentes.
5. Definir três rotas iniciais: usar recurso, manter recurso, preparar entrega.
   Reaproveitar `task-context.json` em vez de criar outro empacotador.
6. Documentar coexistência de `.agents`/`.claude`, destino da autoria e como
   conferir os arquivos gerados. Se o perfil corporativo omitir Claude, registrar
   isso no manifesto de entrega, não apagar sua compatibilidade do Git por inferência.
7. Registrar a sucessão arquitetural necessária em ADR novo apenas quando houver
   alteração de decisão vigente; citar os ADRs 0010/0025/0026 afetados.

**Superfícies:** `AGENTS.md`, `docs/ai/`, `.agents/skills/`, gerador e manifesto
de adaptadores somente se seu contrato mudar.

**Aceite:** Copilot encontra o núcleo, as cinco skills do mantenedor e a rota
correta sem exigir história integral. Em sessão nativa, discovery é conferido
na interface e uso é conferido por tarefa observável. Documento oficial sozinho
não encerra esse ensaio. Medir baseline de bytes/arquivos carregados por tarefa,
sem converter automaticamente bytes em tokens.

**Verificação:** `ai_controls.py --check`, `ci_workflows.py --check`, testes
`test_ai_controls.py` e de inventário nativo/rastreabilidade quando afetados.
No VS Code: nova sessão, referências de instruções e atividade das ferramentas;
testar uma solicitação positiva e uma fora do escopo de cada skill selecionada.

**Rollback:** restaurar núcleo, mapa, registro e saídas geradas juntos; conservar
o snapshot anterior. Não editar configurações globais como parte desse rollback.

## F02 — Separar operação, contrato e história em `docs/`

**Objetivo:** tornar a documentação navegável sem perder os inputs dos validadores.

**Trabalho:**

1. Revisar a triagem por arquivo em lotes: `ai/decisions/playbooks/manutencao`,
   depois índices vivos de sprints/testes, depois auditorias/histórico/handoffs.
2. Em cada lote, distinguir guia atual, contrato executável, fixture, evidência
   congelada e narrativa histórica. Identificar leitor humano e consumidor de código.
3. Criar mapa de movimentação somente para os caminhos que serão movidos:
   origem, destino, consumidor, hash, motivo, sucessor e rollback.
4. Extrair primeiro os contratos vivos de READMEs, Temas V01/V13/V14 e B0 para
   uma localização operacional aprovada. Pode-se usar `docs/contratos/` para
   contratos de manutenção e manter contratos do produto na sua camada própria.
5. Atualizar leitores, testes, geradores, contextos e links na mesma mudança.
   Não editar baseline histórica para fazê-la parecer a nova configuração.
6. Enxugar `docs/sprints/README.md`: estado vigente primeiro, cronologia datada
   por frente depois; corrigir a ambiguidade V14 S0/S1 sem apagar relato histórico.
7. Completar a rota de `docs/guias/temas` e o índice de playbooks, incluindo
   aceite de Micromodelos. Reconciliar os critérios A1/A2 por uma política dona.
8. Tornar baselines/JSONs extensos acessíveis por consulta dirigida, não por
   import obrigatório nas instruções de sessão.

**Superfícies:** índices de `docs`, contratos ativos identificados, leitores em
`tools`, testes e mapas de referências. Conteúdo congelado só muda de localização
se a migração documentar recuperação exata e revisão do contrato de retenção.

**Aceite:** nenhum contrato operacional depende de uma pasta escolhida para
descarte; links antigos necessários têm destino/sucessor; uma LLM consegue
responder o estado atual sem promover um checkpoint antigo a regra vigente.

**Verificação:** validador com snapshot, `ai_controls`, regressões de história,
READMEs e Temas afetadas; conferir todos os consumidores dos arquivos movidos.
Ensaiar retirada do conjunto candidato num checkout descartável: falha inesperada
interrompe apenas esse lote. Não considerar busca textual como prova suficiente.

**Rollback:** reverter arquivos movidos e todos os leitores juntos. Recuperar
evidências pelo commit/manifesto anterior e conferir hashes.

## F03 — Consolidar os manuais

**Objetivo:** dar ao leitor uma referência de uso e uma técnica, com fonte editorial
única por conteúdo e caminho claro de manutenção.

**Trabalho:**

1. Mapear as seções/âncoras do Manual anterior para Manual do Usuário, V2 ou
   conteúdo ainda não coberto. Cobrir exemplos, catálogo, glossário e Temas.
2. Conferir as afirmações dos trechos migrados contra código/contratos atuais;
   não presumir superioridade factual apenas pela data do V2.
3. Escolher uma fonte: capítulos canônicos com livro gerado, ou livro canônico
   com capítulos gerados. Recomendação: capítulos canônicos para facilitar revisão.
4. Implementar geração determinística de volumes, índices e hashes, com preservação
   de âncoras públicas e resolução de links conforme o destino gerado.
5. Formalizar a sucessão do ADR-0010 e atualizar as regras que ainda exigem
   cópia integral idêntica na raiz. Evitar dois catálogos editáveis concorrentes.
6. Converter a entrada da raiz em portal curto; preservar redirecionamento ou
   mapa explícito das âncoras usadas. Migrar os links consumidores identificados.
7. Definir o que acompanha a instalação: guias e partes relevantes sempre
   acessíveis; volumes integrais opcionais somente por perfil de distribuição
   validado. Não excluir arquivos de um manifesto existente informalmente.
8. Atualizar manifesto V2 somente depois da revisão e da prova de geração.

**Superfícies:** manuais raiz/produto, `manuais_v2`, regras editoriais, links,
manifestos e testes de igualdade/geração afetados.

**Aceite:** cada seção antiga necessária tem sucessor; não há links/âncoras
pendentes; correção é feita em uma fonte e aparece em todas as saídas; a rota de
uma tarefa não exige ler 21 mil linhas. História da edição anterior recuperável.

**Verificação:** comparação do conteúdo fonte/gerado, repetição determinística
da geração, links internos e no pacote extraído, manifesto e validador do produto.
Revisão editorial de exemplos e amostra de tarefas de consulta, com cobertura
declarada. `test_readme_integracao.py` deve ganhar contrato sucessor, não perder
a propriedade de detectar divergência silenciosa.

**Rollback:** restaurar manuais/índices/manifesto e regras de autoridade juntos.
Manter a edição anterior acessível durante a janela de migração.

## F04 — Documentar ferramentas e simplificar CI por capacidade

**Objetivo:** permitir manutenção futura sem exigir conhecimento da cronologia SE/V/MM.

**Trabalho:**

1. Classificar os 278 arquivos de `tools`: comandos operacionais, bibliotecas
   internas, testes/fixtures, autoria visual, probes e certificadores históricos.
2. Completar o README por objetivo com pré-requisitos, efeito, comando, sucesso
   e falha. Criar índices apenas nas coleções ativas que precisem deles.
3. Identificar wrappers ainda chamados por testes/CI/usuário e dar a eles
   disposição explícita: compatibilidade mantida ou sucessor com depreciação.
4. Construir matriz de cobertura de CI: teste/contrato → ambiente → job → artifact
   → status exigido. Comparar com os 20 workflows documentados.
5. Medir ao menos um PR de documentação e um de produto. Usar logs/tempos reais;
   não prometer economia pela mera redução de YAMLs.
6. Consolidar jobs apenas quando comandos, versões, dependências e efeitos forem
   equivalentes. Preservar diferenças Python 3.11/3.12 e Spark/Java/widgets/App.
7. Extrair receitas de campanha que ainda alimentam `ci_workflows.py` antes de
   retirar seus YAMLs. Manter apenas uma fonte para gerar jobs.
8. Atualizar nomes baseados em função e aliases/checks em transição quando
   necessário; consultar required checks no repositório alvo antes de trocar.
9. Separar certificação histórica de regressão corrente. Manter MM01 v1 e SER
   pré-promoção reproduzíveis na base correspondente, sem recalcular seus pins.
10. Reconciliar a documentação de política local-first com triggers reais,
    comportamento de draft e execução manual. Explicar a disposição final no README.

**Superfícies:** `tools/README.md`, coleções de ferramentas, `ci_workflows.py`,
YAMLs, testes de receitas e documentação de certificadores; produto só se algum
contrato efetivamente precisar de mudança autorizada.

**Aceite:** cada proteção antiga tem sucessor equivalente ou decisão explícita
de retirada; falha de upstream continua reprovando; artifacts esperados continuam
disponíveis; filtros não deixam required checks pendentes indefinidamente.

**Verificação:** `ci_workflows --check`, `test_ai_ci_workflows.py`, agregado local
com dependências preparadas, regressões específicas e matriz CI autorizada nas
versões afetadas. Executar negativos de propagação e comparação de inventário
de casos; não aprovar por contagem isolada ou simplesmente por “workflow verde”.

**Rollback:** restaurar YAMLs, gerador, testes e configuração de checks em conjunto.
Uma mudança de branch protection requer retorno à configuração anterior registrada.

## F05 — Retirar o protótipo e o legado já desacoplado

**Objetivo:** remover `novas_funcionalidades/` da árvore de trabalho corrente e
outros candidatos aprovados, sem perder recuperação ou código ainda chamado.

**Trabalho:**

1. Congelar a lista exata de arquivos a retirar e seus consumidores. Para
   Concierge, começar pelos 19 arquivos do manifesto existente.
2. Verificar que recursos/ideias necessários estão presentes no Concierge atual;
   divergências funcionais exigem decisão antes de descartar o protótipo.
3. Preservar bytes por commit completo e manifesto recuperável no ambiente de
   manutenção; se não houver Git acessível no destino, definir arquivo de retenção
   externo e sanitizado com a mesma verificabilidade.
4. Atualizar localizador, links vivos e contrato de retenção. Trocar a exigência
   de arquivos presentes por prova de recuperação exata, preservando negativos.
5. Retirar fisicamente o protótipo somente após os consumidores atuais estarem
   migrados. Não aplicar substituições globais a ADRs e relatórios congelados.
6. Aplicar o mesmo processo aos candidatos de autoria visual v1/campanhas antigas
   que a F04 tiver comprovadamente desacoplado. Não usar padrão `*sprint*` para apagar.
7. Conferir que nenhum material de licença, provenance ou fixture ativa sumiu.

**Superfícies:** `novas_funcionalidades/`, retenção histórica, inventário visual,
testes de preservação e consumidores vivos correspondentes.

**Aceite:** pasta do protótipo ausente da árvore corrente, produto Concierge
inalterado no escopo, recuperação 19/19 conferida e nenhum link vivo quebrado.
Nenhuma exclusão adicional baseada apenas em idade/nome.

**Verificação:** testes de história/inventário/Concierge, validador, paridade do
produto, prova de recuperação e negativo de bytes/hash ausentes ou adulterados.

**Rollback:** recuperar os 19 arquivos e os leitores da revisão anterior; hashes
iguais ao manifesto. Não depender apenas de um ZIP sem commit de origem.

## F06 — Renomear a fonte, se escolhido

**Objetivo:** adotar `ambiente_databricks/` com semântica explícita de fonte canônica.
Esta sprint pode ser dispensada sem comprometer a limpeza restante.

**Trabalho:**

1. Recontar referências após as sprints anteriores; o inventário de 533 arquivos
   é a baseline, não um plano de substituição automático.
2. Centralizar a resolução da raiz em owner compartilhado e migrar os leitores
   ativos para essa definição antes de mover a pasta.
3. Separar path operacional, path relativo no ZIP, referência editorial e
   evidência histórica. Preservar caminhos de import Python e do payload instalado.
4. Mover a fonte via Git e atualizar defaults, CLI, imports de wrappers, testes,
   filtros de CI, geradores, instruções, mapas e links vivos como uma unidade.
5. Atualizar manuais/gerados pela fonte editorial escolhida, depois seus hashes.
6. Preservar paths antigos em evidências datadas e referenciar o mapa de migração.
   Não deixar alias symlink nem uma segunda árvore editável para esconder lacunas.
7. Gerar espelho e kit a partir da nova raiz em destino inventariado.

**Aceite:** bootstrap, validação, render, pacote extraído e imports funcionam;
nenhum consumidor ativo depende da raiz antiga. Cada ocorrência remanescente é
histórica e justificada. A estrutura instalada no Databricks permanece coerente.

**Verificação:** conteúdo executável e APIs equivalentes antes/depois; mudanças
de documentação manifestadas; testes de source-root/containment, readmes, IA,
Micromodelos, Temas, CI e kit. Validar Windows e Linux, sensibilidade a caixa e
path com espaços. A receita de publicação é conferida em modo de inspeção/local;
escrita no workspace depende do escopo de entrega aprovado.

**Rollback:** reverter rename e todos os consumidores na mesma mudança; regenerar
somente o destino gerido autorizado. Não recuperar apenas a pasta e deixar CI novo.

## F07 — Preparar a entrega para VS Code e Databricks

**Objetivo:** tornar explícita a diferença entre usar o produto e manter o Git.

**Trabalho:**

1. Confirmar como o Git autorizado chegará ao computador do trabalho e quais
   operações de sincronização são permitidas. Conservar um só canônico por mudança.
2. Para manutenção completa, levar o checkout com os commits exigidos pelos
   controles de proveniência; usar contexto por tarefa no Copilot.
3. Se um pacote de manutenção enxuto tiver sido escolhido, calcular o fechamento
   dos contratos/testes necessários e implementar um perfil próprio. Não chamar
   export sem Git de checkout integralmente certificado.
4. Gerar o pacote Databricks com manifesto do commit limpo, através das ferramentas
   existentes. Incluir documentação escolhida na F03 e aceites necessários.
5. Criar uma entrada curta para o usuário: uso do Hub, manutenção com Copilot,
   comandos frequentes, atualização e retorno à versão anterior.
6. Testar extração em path com espaços, imports, recursos de pacote e ausência
   de dependência acidental no checkout original.
7. No VS Code corporativo, confirmar as instruções e skills realmente descobertas,
   inclusive duplicação de adapters e limitações impostas pela organização.
8. Registrar quais testes exigem Databricks/MLflow/Unity Catalog e executá-los
   somente na campanha de destino autorizada. A preparação do kit pode terminar
   antes dessa campanha.

**Aceite:** cada perfil tem inventário exato, proveniência, instrução de uso e
verificação adequada; o usuário sabe onde editar e qual pasta importar. O kit de
produto não transporta histórico e ferramentas de manutenção por acidente.

**Verificação:** build/manifesto/extração, testes de transição e aceite sintético,
rotas de manuais no pacote, sessão nova Copilot e testes de import no destino
quando disponíveis. Registrar separadamente resultados locais e corporativos.

**Rollback:** restaurar release anterior pelo manifesto e backup do destino;
conservar configuração local do usuário. Rastrear mudanças corporativas no fluxo
autorizado sem trazer identificadores/dados privados a este repositório.

## F08 — Ensaiar jornadas e encerrar a limpeza

**Objetivo:** comprovar que a organização ficou mais simples e continua íntegra.

Jornadas de aceite propostas:

| Jornada | Resultado observável |
|---|---|
| Encontrar um helper e seu exemplo | chegar ao contrato atual sem abrir relatório de sprint |
| Alterar um README de objeto | Copilot seleciona padrão e verificação corretos |
| Investigar falha de CI | localizar workflow, ambiente e comando de reprodução pelo índice |
| Preparar atualização do Hub | gerar pacote conferível a partir da fonte certa |
| Consultar Micromodelos/Temas | distinguir uso atual, limite conhecido e prova histórica |
| Recuperar protótipo removido | reconstruir os bytes da revisão indicada pelo manifesto |
| Consultar o Manual | encontrar capítulo e fonte sem carregar volumes duplicados |

Comparar essas jornadas com a baseline F01: quantidade de passos de navegação,
arquivos/bytes efetivamente consultados, instruções duplicadas e decisões erradas
causadas por história antiga. Fixar metas após a medição inicial; não inventar
redução de tokens, tempo ou custo sem observação.

**Aceite técnico:** testes proporcionais aprovados, links/âncoras/manifestos
íntegros, produto/derivado equivalentes, recuperação do legado demonstrada,
nenhuma perda de licença/contrato, pendências ambientais explícitas.

**Aceite de uso:** usuário conclui as jornadas relevantes no perfil escolhido.
Revisão requerida para transferência ampla segue a política reconciliada na F02;
apoio do mesmo agente não é evidência independente.

**Fechamento:** atualizar somente os estados vivos e o marco de changelog,
registrar os resultados finais no owner da entrega e oferecer rollback. Evitar
criar novo volume de diários ou multiplicar índices equivalentes.

## Riscos e condições de parada

| Risco | Sinal | Tratamento |
|---|---|---|
| Perder contrato escondido em história | teste/leitor aponta a pasta candidata | migrar o consumidor antes do descarte |
| Manuais divergentes | uma alteração chega só a uma edição/parte | fonte única e geração verificável |
| Cortar CI por semelhança superficial | ambiente/step/artifact diferente | comparar matriz e manter perfis necessários |
| Reduzir package quebrando manutenção | validador pede Git/input omitido | manter checkout completo ou criar verificador explícito do perfil |
| Copilot carregar instruções erradas | discovery duplicada ou referências ausentes | ensaio na interface real; corrigir adapter/perfil |
| Renomear adulterando evidência | hash/pin histórico recalculado | restaurar original e acrescentar sucessão de contrato |
| Alteração concorrente | consumidor mudou desde a baseline | reconciliar o lote e repetir verificações afetadas |

O usuário deve aprovar escolhas de arquitetura e escopo de descarte; depois disso,
as edições reversíveis necessárias ao lote aprovado podem seguir sem microaprovações.
Conflito real de conteúdo/autoridade interrompe só a parte dependente.

## Verificacao desta entrega

Ambiente observado: Windows, Python 3.12.10. O HEAD permanece a baseline;
documentos entregues pertencem à worktree da branch `codex/plano-faxina-20261007`.
Não se atribui a um commit antigo o conteúdo novo.

| Verificação | Resultado observado |
|---|---|
| `python -B tools/validate_assistant.py --conferir-readme` | PASS, exit 0, zero falhas e zero avisos; 20 linhas do snapshot conferidas |
| `python -B tools/ai_controls.py --check` | PASS, escopo estático; cinco skills canônicas e cinco adaptadores gerados |
| `python -B tools/ci_workflows.py --check` | PASS; nomes, receitas e dependências preservados |
| `python -B tools/render_simulado.py --check` | PASS; fonte e saída equivalentes por paths, bytes, hashes e tipos |
| Links dos quatro Markdown novos | 45 destinos locais resolvidos; zero caminhos ausentes |
| Inventário CSV contra blobs de HEAD | 1.106 caminhos únicos; tamanhos e SHA-256 conferem com a baseline |
| Catálogo de workflows contra os YAMLs | 20/20 arquivos representados |
| Escopo do diff | zero alteração em produto, skills, adaptadores, Python ou YAML |
| `git diff --check` | PASS |

A primeira validação detectou divergência apenas no censo de links após editar
os índices; com os arquivos novos incluídos no inventário Git, também mudou o
censo de identidade. O README foi atualizado pelos valores medidos: 1.766
arquivos de identidade e 1.946 links externos à raiz do produto. A rodada final
passou. Nenhum validador foi relaxado.

Não foram executados CI remoto, clientes nativos, publicação, instalação ou
homologação Databricks. A alteração documental não exige repetir campanhas
analíticas. A conferência desta entrega é autorrevisão Codex de contexto completo.
